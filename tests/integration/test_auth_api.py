import pytest


class TestRegisterEndpoint:
    def test_register_success(self, client):
        response = client.post("/api/auth/register", json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_register_duplicate_username(self, client, registered_user):
        response = client.post("/api/auth/register", json={
            "username": registered_user["username"],
            "email": "different@example.com",
            "password": "password123"
        })
        assert response.status_code == 400
        assert "Username already registered" in response.json()["detail"]

    def test_register_duplicate_email(self, client, registered_user):
        response = client.post("/api/auth/register", json={
            "username": "differentuser",
            "email": registered_user["email"],
            "password": "password123"
        })
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        response = client.post("/api/auth/register", json={
            "username": "user",
            "email": "invalid",
            "password": "password123"
        })
        assert response.status_code == 422

    def test_register_short_password(self, client):
        response = client.post("/api/auth/register", json={
            "username": "user",
            "email": "user@example.com",
            "password": "123"
        })
        assert response.status_code == 422

    def test_register_empty_username(self, client):
        response = client.post("/api/auth/register", json={
            "username": "",
            "email": "user@example.com",
            "password": "password123"
        })
        assert response.status_code == 422


class TestLoginEndpoint:
    def test_login_success(self, client, registered_user):
        response = client.post("/api/auth/login", json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_login_wrong_password(self, client, registered_user):
        response = client.post("/api/auth/login", json={
            "email": registered_user["email"],
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post("/api/auth/login", json={
            "email": "nobody@example.com",
            "password": "password123"
        })
        assert response.status_code == 401

    def test_login_invalid_email_format(self, client):
        response = client.post("/api/auth/login", json={
            "email": "notanemail",
            "password": "password123"
        })
        assert response.status_code == 422
