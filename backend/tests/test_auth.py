import unittest
from sqlalchemy.pool import StaticPool

from app import create_app
from database import db


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


class AuthTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_login_me(self):
        payload = {
            "username": "alice",
            "email": "alice@example.com",
            "password": "demo1234",
        }
        register_response = self.client.post("/api/auth/register", json=payload)
        self.assertEqual(register_response.status_code, 201)

        login_response = self.client.post(
            "/api/auth/login",
            json={"email": payload["email"], "password": payload["password"]},
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.get_json()["token"]

        me_response = self.client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(me_response.status_code, 200)
        me_data = me_response.get_json()
        self.assertEqual(me_data["email"], payload["email"])
