import pytest


class TestAuthRegister:
    def test_register_success(self, client):
        resp = client.post("/api/auth/register", json={
            "email": "newuser@example.com",
            "password": "SecurePass123",
            "name": "New User",
        })
        assert resp.status_code == 201
        data = resp.get_json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["name"] == "New User"
        assert data["user"]["role"] == "user"
        assert data["user"]["tier"] == "free"

    def test_register_missing_email(self, client):
        resp = client.post("/api/auth/register", json={
            "password": "SecurePass123",
        })
        assert resp.status_code == 400

    def test_register_missing_password(self, client):
        resp = client.post("/api/auth/register", json={
            "email": "test@example.com",
        })
        assert resp.status_code == 400

    def test_register_duplicate_email(self, client):
        client.post("/api/auth/register", json={
            "email": "dup@example.com",
            "password": "SecurePass123",
        })
        resp = client.post("/api/auth/register", json={
            "email": "dup@example.com",
            "password": "SecurePass123",
        })
        assert resp.status_code == 400
        assert "already registered" in resp.get_json()["error"]

    def test_register_no_body(self, client):
        resp = client.post("/api/auth/register")
        assert resp.status_code == 400


class TestAuthLogin:
    def test_login_success(self, client):
        client.post("/api/auth/register", json={
            "email": "login@example.com",
            "password": "SecurePass123",
            "name": "Login User",
        })
        resp = client.post("/api/auth/login", json={
            "email": "login@example.com",
            "password": "SecurePass123",
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["email"] == "login@example.com"

    def test_login_wrong_password(self, client):
        client.post("/api/auth/register", json={
            "email": "wrong@example.com",
            "password": "SecurePass123",
        })
        resp = client.post("/api/auth/login", json={
            "email": "wrong@example.com",
            "password": "WrongPass456",
        })
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        resp = client.post("/api/auth/login", json={
            "email": "noone@example.com",
            "password": "SecurePass123",
        })
        assert resp.status_code == 401

    def test_login_missing_fields(self, client):
        resp = client.post("/api/auth/login", json={})
        assert resp.status_code == 400


class TestAuthMe:
    def test_me_with_valid_token(self, client, auth_headers):
        resp = client.get("/api/auth/me", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["email"] == "test@example.com"

    def test_me_without_token(self, client):
        resp = client.get("/api/auth/me")
        assert resp.status_code == 401

    def test_me_with_invalid_token(self, client):
        resp = client.get("/api/auth/me", headers={"Authorization": "Bearer invalidtoken"})
        assert resp.status_code == 422


class TestAuthRefresh:
    def test_refresh_token(self, client):
        reg = client.post("/api/auth/register", json={
            "email": "refresh@example.com",
            "password": "SecurePass123",
        })
        refresh_token = reg.get_json()["refresh_token"]
        resp = client.post("/api/auth/refresh", headers={
            "Authorization": f"Bearer {refresh_token}",
        })
        assert resp.status_code == 200
        assert "access_token" in resp.get_json()


class TestAuthAutoLogin:
    def test_auto_login_returns_tokens(self, client, auth_user):
        resp = client.post("/api/auth/auto-login")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "user" in data

    def test_auto_login_returns_first_user(self, client, auth_user):
        resp = client.post("/api/auth/auto-login")
        data = resp.get_json()
        assert data["user"]["email"] == "test@example.com"
