from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id           = db.Column(db.Integer, primary_key=True)
    username     = db.Column(db.String(80),  unique=True, nullable=False)
    email        = db.Column(db.String(120), unique=True, nullable=False)
    password_hash= db.Column(db.String(256), nullable=False)
    age          = db.Column(db.Integer)
    gender       = db.Column(db.String(20))
    location     = db.Column(db.String(100))
    created_at   = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    browsing_history = db.relationship('BrowsingHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    purchases        = db.relationship('Purchase',        backref='user', lazy=True, cascade='all, delete-orphan')
    ratings          = db.relationship('Rating',          backref='user', lazy=True, cascade='all, delete-orphan')
    cart             = db.relationship('Cart',            backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'age': self.age,
            'gender': self.gender,
            'location': self.location,
            'created_at': self.created_at.isoformat()
        }


class Product(db.Model):
    __tablename__ = 'products'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(200), nullable=False)
    description   = db.Column(db.Text)
    category      = db.Column(db.String(100))
    subcategory   = db.Column(db.String(100))
    price         = db.Column(db.Float)
    image_url     = db.Column(db.String(500))
    tags          = db.Column(db.String(500))   # comma-separated keywords
    brand         = db.Column(db.String(100))
    avg_rating    = db.Column(db.Float, default=0.0)
    reviews_count = db.Column(db.Integer, default=0)
    stock         = db.Column(db.Integer, default=100)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'subcategory': self.subcategory,
            'price': self.price,
            'image_url': self.image_url,
            'tags': self.tags.split(',') if self.tags else [],
            'brand': self.brand,
            'avg_rating': self.avg_rating,
            'reviews_count': self.reviews_count,
            'stock': self.stock
        }


class BrowsingHistory(db.Model):
    __tablename__ = 'browsing_history'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'),    nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    timestamp  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    duration   = db.Column(db.Integer, default=0)   # seconds spent on product page


class Purchase(db.Model):
    __tablename__ = 'purchases'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'),    nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity   = db.Column(db.Integer, default=1)
    price_paid = db.Column(db.Float)
    timestamp  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Rating(db.Model):
    __tablename__ = 'ratings'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'),    nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating     = db.Column(db.Float, nullable=False)   # 1.0 – 5.0
    review     = db.Column(db.Text)
    timestamp  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id'),)


class Cart(db.Model):
    __tablename__ = 'cart'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'),    nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity   = db.Column(db.Integer, default=1)
    added_at   = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    product    = db.relationship('Product', lazy=True)
