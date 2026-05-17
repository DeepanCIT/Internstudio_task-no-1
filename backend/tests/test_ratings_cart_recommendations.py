import unittest
from sqlalchemy.pool import StaticPool

from app import create_app
from database import db, Product


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }
    JWT_SECRET_KEY = "test-jwt-secret-key-32-characters-long"
    SECRET_KEY = "test-secret-key-32-characters-long"
    CORS_ORIGINS = ["*"]


class RatingsCartRecommendationsTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _register_and_login(self):
        payload = {
            "username": "alice",
            "email": "alice@example.com",
            "password": "demo1234",
        }
        self.client.post("/api/auth/register", json=payload)
        login_response = self.client.post(
            "/api/auth/login",
            json={"email": payload["email"], "password": payload["password"]},
        )
        return login_response.get_json()["token"]

    def _add_product(self, name, stock=10, avg_rating=0.0):
        with self.app.app_context():
            product = Product(
                name=name,
                category="Electronics",
                price=19.99,
                stock=stock,
                avg_rating=avg_rating,
                tags="audio,wireless",
            )
            db.session.add(product)
            db.session.commit()
            return product.id

    def test_rate_product_invalid_rating(self):
        token = self._register_and_login()
        product_id = self._add_product("Test Headphones")
        response = self.client.post(
            "/api/ratings",
            json={"product_id": product_id, "rating": "bad"},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 400)

    def test_add_to_cart_invalid_quantity(self):
        token = self._register_and_login()
        product_id = self._add_product("Test Mouse")
        response = self.client.post(
            "/api/cart",
            json={"product_id": product_id, "quantity": "bad"},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 400)

    def test_checkout_updates_stock(self):
        token = self._register_and_login()
        product_id = self._add_product("Test Keyboard", stock=3)
        add_response = self.client.post(
            "/api/cart",
            json={"product_id": product_id, "quantity": 2},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(add_response.status_code, 201)

        checkout_response = self.client.post(
            "/api/cart/checkout",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(checkout_response.status_code, 200)

        with self.app.app_context():
            product = db.session.get(Product, product_id)
            self.assertEqual(product.stock, 1)

    def test_checkout_insufficient_stock(self):
        token = self._register_and_login()
        product_id = self._add_product("Test Monitor", stock=1)
        add_response = self.client.post(
            "/api/cart",
            json={"product_id": product_id, "quantity": 2},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(add_response.status_code, 201)

        checkout_response = self.client.post(
            "/api/cart/checkout",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(checkout_response.status_code, 400)

    def test_recommendations_fallback(self):
        token = self._register_and_login()
        self._add_product("Test Camera", avg_rating=4.5)
        self._add_product("Test Speaker", avg_rating=4.2)
        self._add_product("Test Tablet", avg_rating=3.9)

        response = self.client.get(
            "/api/recommendations?n=2",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["method"], "trending_fallback")
        self.assertEqual(len(data["recommendations"]), 2)
