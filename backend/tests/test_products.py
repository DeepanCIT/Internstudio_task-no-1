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


class ProductTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _add_product(self, name, category="Electronics"):
        with self.app.app_context():
            product = Product(name=name, category=category, price=9.99)
            db.session.add(product)
            db.session.commit()

    def test_products_empty(self):
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["products"], [])
        self.assertEqual(data["total"], 0)

    def test_products_search(self):
        self._add_product("Test Headphones")
        response = self.client.get("/api/products?search=headphones")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["products"][0]["name"], "Test Headphones")
