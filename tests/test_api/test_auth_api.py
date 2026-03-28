from fastapi.testclient import TestClient

from src.thufir.database.database_impl import DatabaseImpl
from src.thufir.thufir import create_app
from tests.utils.database_config import sqlite_db_config


def create_test_client() -> TestClient:
    database = DatabaseImpl(sqlite_db_config)
    app = create_app(database=database)
    return TestClient(app)


def register_user(client: TestClient, **overrides) -> dict:
    payload = {
        "email": "user@example.com",
        "username": "reader1",
        "password": "supersecret",
    }
    payload.update(overrides)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    return response.json()


def test_register_user_returns_token_and_profile():
    with create_test_client() as client:
        payload = {
            "email": "new@example.com",
            "username": "newuser",
            "password": "supersecret",
        }

        response = client.post("/auth/register", json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["token_type"] == "bearer"
        assert body["access_token"]
        assert body["user"]["email"] == payload["email"]
        assert body["user"]["username"] == payload["username"]
        assert "password_hash" not in body["user"]


def test_register_user_rejects_duplicate_email():
    with create_test_client() as client:
        register_user(client)

        response = client.post(
            "/auth/register",
            json={
                "email": "user@example.com",
                "username": "reader2",
                "password": "supersecret",
            },
        )

        assert response.status_code == 409
        assert response.json()["detail"] == "Email is already registered"


def test_login_returns_token_for_valid_credentials():
    with create_test_client() as client:
        register_user(client)

        response = client.post(
            "/auth/login",
            json={"username": "reader1", "password": "supersecret"},
        )

        assert response.status_code == 200
        body = response.json()
        assert body["access_token"]
        assert body["user"]["username"] == "reader1"


def test_login_rejects_invalid_credentials():
    with create_test_client() as client:
        register_user(client)

        response = client.post(
            "/auth/login",
            json={"username": "reader1", "password": "wrongpass"},
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid username or password"


def test_profile_endpoint_requires_authentication():
    with create_test_client() as client:
        response = client.get("/users/me")

        assert response.status_code == 401
        assert response.json()["detail"] == "Authentication required"


def test_profile_endpoint_returns_current_user():
    with create_test_client() as client:
        register_response = register_user(client)

        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {register_response['access_token']}"},
        )

        assert response.status_code == 200
        assert response.json()["username"] == "reader1"


def test_logout_accepts_authenticated_user():
    with create_test_client() as client:
        register_response = register_user(client)

        response = client.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {register_response['access_token']}"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "reader1 logged out"
