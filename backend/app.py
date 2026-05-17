"""
E-Commerce Personalized Recommendation Engine — Flask Backend
"""
import os

from flask import Flask, jsonify, request, abort, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from database import db, User, Product, BrowsingHistory, Purchase, Rating, Cart
from models.collaborative_filtering import CollaborativeFiltering
from models.content_based import ContentBasedFiltering
from models.hybrid import HybridRecommender

# --------------------------------------------------------------------------- #
#  App factory                                                                 #
# --------------------------------------------------------------------------- #
def create_app(config_class=Config):
    static_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist')
    )
    app = Flask(__name__, static_folder=static_dir, static_url_path='/')
    app.config.from_object(config_class)

    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    db.init_app(app)
    JWTManager(app)

    # ---- initialise ML models (rebuilt on first request / reload) ---- #
    cf_model = CollaborativeFiltering()
    cb_model = ContentBasedFiltering()
    hybrid   = HybridRecommender(cf_model, cb_model, cf_weight=0.45, cb_weight=0.55)

    def _get_or_404(model, ident):
        instance = db.session.get(model, ident)
        if instance is None:
            abort(404)
        return instance

    def refresh_models():
        """Re-train recommendation models from the current DB state."""
        with app.app_context():
            ratings  = db.session.query(
                Rating.user_id, Rating.product_id, Rating.rating
            ).all()
            cf_model.build_matrix([(r.user_id, r.product_id, r.rating) for r in ratings])

            products = Product.query.all()
            cb_model.build_profile([p.to_dict() for p in products])

    # ================================================================== #
    #  AUTH ROUTES                                                         #
    # ================================================================== #
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        data = request.get_json()
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'username, email and password are required'}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already taken'}), 409

        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            age=data.get('age'),
            gender=data.get('gender'),
            location=data.get('location')
        )
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))
        return jsonify({'token': token, 'user': user.to_dict()}), 201

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'email and password are required'}), 400
        user = User.query.filter_by(email=data.get('email', '')).first()
        if not user or not check_password_hash(user.password_hash, data.get('password', '')):
            return jsonify({'error': 'Invalid credentials'}), 401

        token = create_access_token(identity=str(user.id))
        return jsonify({'token': token, 'user': user.to_dict()})

    @app.route('/api/auth/me', methods=['GET'])
    @jwt_required()
    def me():
        user_id = int(get_jwt_identity())
        user = _get_or_404(User, user_id)
        return jsonify(user.to_dict())

    # ================================================================== #
    #  PRODUCT ROUTES                                                      #
    # ================================================================== #
    @app.route('/api/products', methods=['GET'])
    def get_products():
        page     = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category')
        search   = request.args.get('search')

        query = Product.query
        if category:
            query = query.filter(Product.category.ilike(f'%{category}%'))
        if search:
            query = query.filter(
                Product.name.ilike(f'%{search}%') |
                Product.description.ilike(f'%{search}%') |
                Product.tags.ilike(f'%{search}%')
            )

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({
            'products': [p.to_dict() for p in paginated.items],
            'total':    paginated.total,
            'pages':    paginated.pages,
            'page':     page
        })

    @app.route('/api/products/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        product = _get_or_404(Product, product_id)
        return jsonify(product.to_dict())

    @app.route('/api/products/categories', methods=['GET'])
    def get_categories():
        cats = db.session.query(Product.category).distinct().all()
        return jsonify([c[0] for c in cats if c[0]])

    # ================================================================== #
    #  BROWSING HISTORY                                                    #
    # ================================================================== #
    @app.route('/api/browse', methods=['POST'])
    @jwt_required()
    def record_browse():
        user_id    = int(get_jwt_identity())
        data       = request.get_json()
        product_id = data.get('product_id')
        if not product_id:
            return jsonify({'error': 'product_id required'}), 400

        _get_or_404(Product, product_id)
        entry = BrowsingHistory(
            user_id=user_id,
            product_id=product_id,
            duration=data.get('duration', 0)
        )
        db.session.add(entry)
        db.session.commit()
        return jsonify({'message': 'Recorded'}), 201

    @app.route('/api/browse/history', methods=['GET'])
    @jwt_required()
    def get_browse_history():
        user_id = int(get_jwt_identity())
        history = (BrowsingHistory.query
                   .filter_by(user_id=user_id)
                   .order_by(BrowsingHistory.timestamp.desc())
                   .limit(20).all())
        product_ids = list(dict.fromkeys([h.product_id for h in history]))   # preserve order, dedupe
        products    = {p.id: p.to_dict() for p in
                       Product.query.filter(Product.id.in_(product_ids)).all()}
        return jsonify([products[pid] for pid in product_ids if pid in products])

    # ================================================================== #
    #  RATINGS                                                             #
    # ================================================================== #
    @app.route('/api/ratings', methods=['POST'])
    @jwt_required()
    def rate_product():
        user_id    = int(get_jwt_identity())
        data       = request.get_json()
        if not data:
            return jsonify({'error': 'product_id and rating required'}), 400
        product_id = data.get('product_id')
        rating_val = data.get('rating')

        if not product_id or rating_val is None:
            return jsonify({'error': 'product_id and rating required'}), 400
        try:
            rating_float = float(rating_val)
        except (TypeError, ValueError):
            return jsonify({'error': 'Rating must be a number between 1 and 5'}), 400
        if not (1.0 <= rating_float <= 5.0):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400

        existing = Rating.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing:
            existing.rating = rating_float
            existing.review = data.get('review', existing.review)
        else:
            db.session.add(Rating(
                user_id=user_id, product_id=product_id,
                rating=rating_float, review=data.get('review')
            ))

        # Update product avg_rating
        product = _get_or_404(Product, product_id)
        all_ratings = [r.rating for r in Rating.query.filter_by(product_id=product_id).all()]
        product.avg_rating    = round(sum(all_ratings) / len(all_ratings), 2)
        product.reviews_count = len(all_ratings)

        db.session.commit()
        refresh_models()
        return jsonify({'message': 'Rating saved'})

    # ================================================================== #
    #  CART                                                                #
    # ================================================================== #
    @app.route('/api/cart', methods=['GET'])
    @jwt_required()
    def get_cart():
        user_id = int(get_jwt_identity())
        items   = Cart.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id':       item.id,
            'product':  item.product.to_dict(),
            'quantity': item.quantity
        } for item in items])

    @app.route('/api/cart', methods=['POST'])
    @jwt_required()
    def add_to_cart():
        user_id    = int(get_jwt_identity())
        data       = request.get_json()
        if not data:
            return jsonify({'error': 'product_id required'}), 400
        product_id = data.get('product_id')
        quantity_raw = data.get('quantity', 1)
        if not product_id:
            return jsonify({'error': 'product_id required'}), 400

        try:
            quantity = int(quantity_raw)
        except (TypeError, ValueError):
            return jsonify({'error': 'quantity must be a positive integer'}), 400
        if quantity <= 0:
            return jsonify({'error': 'quantity must be a positive integer'}), 400

        _get_or_404(Product, product_id)
        existing = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing:
            existing.quantity += quantity
        else:
            db.session.add(Cart(user_id=user_id, product_id=product_id, quantity=quantity))
        db.session.commit()
        return jsonify({'message': 'Added to cart'}), 201

    @app.route('/api/cart/<int:item_id>', methods=['DELETE'])
    @jwt_required()
    def remove_from_cart(item_id):
        user_id = int(get_jwt_identity())
        item    = Cart.query.filter_by(id=item_id, user_id=user_id).first_or_404()
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Removed'})

    @app.route('/api/cart/checkout', methods=['POST'])
    @jwt_required()
    def checkout():
        user_id = int(get_jwt_identity())
        items   = Cart.query.filter_by(user_id=user_id).all()
        if not items:
            return jsonify({'error': 'Cart is empty'}), 400

        for item in items:
            product = _get_or_404(Product, item.product_id)
            if product.stock is not None and item.quantity > product.stock:
                db.session.rollback()
                return jsonify({'error': 'Insufficient stock'}), 400
            db.session.add(Purchase(
                user_id=user_id, product_id=item.product_id,
                quantity=item.quantity, price_paid=product.price * item.quantity
            ))
            if product.stock is not None:
                product.stock -= item.quantity
            db.session.delete(item)

        db.session.commit()
        refresh_models()
        return jsonify({'message': 'Order placed successfully'})

    # ================================================================== #
    #  RECOMMENDATION ROUTES                                               #
    # ================================================================== #
    def _ensure_models_ready():
        """Lazily initialise models if not yet built."""
        if cb_model.tfidf_matrix is None:
            refresh_models()

    @app.route('/api/recommendations', methods=['GET'])
    @jwt_required()
    def get_recommendations():
        """Personalised hybrid recommendations for the logged-in user."""
        _ensure_models_ready()
        user_id = int(get_jwt_identity())
        n       = request.args.get('n', 12, type=int)
        method  = request.args.get('method', 'hybrid')   # hybrid | cf | cb

        browsed = [h.product_id for h in
                   BrowsingHistory.query.filter_by(user_id=user_id)
                   .order_by(BrowsingHistory.timestamp.desc()).limit(30).all()]
        purchased = [p.product_id for p in
                     Purchase.query.filter_by(user_id=user_id).all()]

        if method == 'cf':
            rec_ids = cf_model.get_user_recommendations(user_id, n=n)
        elif method == 'cb':
            rec_ids = cb_model.get_user_profile_recommendations(
                list(set(browsed + purchased)), n=n
            )
        else:
            rec_ids = hybrid.get_recommendations(user_id, browsed, purchased, n=n)

        # Fallback: trending products if no recommendations
        if not rec_ids:
            products = (Product.query
                        .order_by(Product.avg_rating.desc())
                        .limit(n).all())
            return jsonify({
                'recommendations': [p.to_dict() for p in products],
                'method': 'trending_fallback'
            })

        products_map = {p.id: p.to_dict() for p in
                        Product.query.filter(Product.id.in_(rec_ids)).all()}
        ordered      = [products_map[pid] for pid in rec_ids if pid in products_map]
        return jsonify({'recommendations': ordered, 'method': method})

    @app.route('/api/recommendations/similar/<int:product_id>', methods=['GET'])
    def get_similar(product_id):
        """Similar products for the product-detail page (no auth needed)."""
        _ensure_models_ready()
        n       = request.args.get('n', 8, type=int)
        rec_ids = hybrid.get_similar_products(product_id, n=n)

        if not rec_ids:
            product = _get_or_404(Product, product_id)
            others  = (Product.query
                       .filter_by(category=product.category)
                       .filter(Product.id != product_id)
                       .order_by(Product.avg_rating.desc())
                       .limit(n).all())
            return jsonify([p.to_dict() for p in others])

        products_map = {p.id: p.to_dict() for p in
                        Product.query.filter(Product.id.in_(rec_ids)).all()}
        return jsonify([products_map[pid] for pid in rec_ids if pid in products_map])

    @app.route('/api/recommendations/trending', methods=['GET'])
    def get_trending():
        """Top-rated / most-reviewed products — no auth required."""
        n        = request.args.get('n', 10, type=int)
        products = (Product.query
                    .order_by(Product.avg_rating.desc(), Product.reviews_count.desc())
                    .limit(n).all())
        return jsonify([p.to_dict() for p in products])

    @app.route('/api/recommendations/new-arrivals', methods=['GET'])
    def get_new_arrivals():
        n        = request.args.get('n', 10, type=int)
        products = Product.query.order_by(Product.id.desc()).limit(n).all()
        return jsonify([p.to_dict() for p in products])

    # ================================================================== #
    #  HEALTH CHECK                                                        #
    # ================================================================== #
    @app.route('/api/health')
    def health():
        return jsonify({'status': 'ok', 'models_ready': cb_model.tfidf_matrix is not None})

    if os.path.isdir(app.static_folder):
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve_frontend(path):
            if path.startswith('api'):
                abort(404)
            file_path = os.path.join(app.static_folder, path)
            if path and os.path.isfile(file_path):
                return send_from_directory(app.static_folder, path)
            return send_from_directory(app.static_folder, 'index.html')

    return app


# --------------------------------------------------------------------------- #
#  Entry point                                                                 #
# --------------------------------------------------------------------------- #
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
