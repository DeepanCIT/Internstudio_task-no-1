import unittest
from sqlalchemy.pool import StaticPool
from werkzeug.security import generate_password_hash

from app import create_app
from database import db, User, Product, Rating


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


class BrowseAndRecommendationsTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _register_and_login(self, username="alice", email="alice@example.com"):
        payload = {
            "username": username,
            "email": email,
            "password": "demo1234",
        }
        register_response = self.client.post("/api/auth/register", json=payload)
        user_id = register_response.get_json()["user"]["id"]

        login_response = self.client.post(
            "/api/auth/login",
            json={"email": payload["email"], "password": payload["password"]},
        )
        token = login_response.get_json()["token"]
        return token, user_id

    def _create_user(self, username, email):
        with self.app.app_context():
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash("demo1234"),
            )
            db.session.add(user)
            db.session.commit()
            return user.id

    def _add_product(self, name, tags="audio,wireless", stock=10):
        with self.app.app_context():
            product = Product(
                name=name,
                category="Electronics",
                price=19.99,
                tags=tags,
                stock=stock,
            )
            db.session.add(product)
            db.session.commit()
            return product.id

    def test_browse_history_returns_products(self):
        token, _ = self._register_and_login()
        product_id = self._add_product("Test Headphones")

        browse_response = self.client.post(
            "/api/browse",
            json={"product_id": product_id, "duration": 42},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(browse_response.status_code, 201)

        history_response = self.client.get(
            "/api/browse/history",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(history_response.status_code, 200)
        data = history_response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], product_id)

    def test_recommendations_cf(self):
        token, user_id = self._register_and_login()
        other_user_id = self._create_user("bob", "bob@example.com")

        product_1 = self._add_product("Test Camera")
        product_2 = self._add_product("Test Lens")

        with self.app.app_context():
            db.session.add(Rating(user_id=user_id, product_id=product_1, rating=4.0))
            db.session.add(Rating(user_id=other_user_id, product_id=product_1, rating=4.5))
            db.session.add(Rating(user_id=other_user_id, product_id=product_2, rating=5.0))
            db.session.commit()

        response = self.client.get(
            "/api/recommendations?method=cf&n=3",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["method"], "cf")
        rec_ids = [item["id"] for item in data["recommendations"]]
        self.assertIn(product_2, rec_ids)

    def test_recommendations_cb(self):
        token, _ = self._register_and_login()
        product_1 = self._add_product("Test Speaker")
        product_2 = self._add_product("Test Subwoofer")

        self.client.post(
            "/api/browse",
            json={"product_id": product_1},
            headers={"Authorization": f"Bearer {token}"},
        )

        response = self.client.get(
            "/api/recommendations?method=cb&n=2",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["method"], "cb")
        rec_ids = [item["id"] for item in data["recommendations"]]
        self.assertIn(product_2, rec_ids)
        self.assertNotIn(product_1, rec_ids)

    def test_recommendations_hybrid(self):
        token, user_id = self._register_and_login()
        other_user_id = self._create_user("carol", "carol@example.com")

        product_1 = self._add_product("Test Keyboard")
        product_2 = self._add_product("Test Mouse")
        product_3 = self._add_product("Test Monitor")

        self.client.post(
            "/api/browse",
            json={"product_id": product_1},
            headers={"Authorization": f"Bearer {token}"},
        )

        with self.app.app_context():
            db.session.add(Rating(user_id=user_id, product_id=product_1, rating=4.0))
            db.session.add(Rating(user_id=other_user_id, product_id=product_1, rating=4.5))
            db.session.add(Rating(user_id=other_user_id, product_id=product_2, rating=5.0))
            db.session.commit()

        response = self.client.get(
            "/api/recommendations?method=hybrid&n=2",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["method"], "hybrid")
        self.assertGreater(len(data["recommendations"]), 0)
