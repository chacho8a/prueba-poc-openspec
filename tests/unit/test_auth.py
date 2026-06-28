import pytest
from datetime import timedelta
from backend.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
)


class TestPasswordHashing:
    def test_hash_and_verify_correct_password(self):
        password = "mysecretpassword"
        hashed = get_password_hash(password)
        assert hashed != password
        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        hashed = get_password_hash("correctpassword")
        assert verify_password("wrongpassword", hashed) is False

    def test_hash_produces_different_outputs(self):
        password = "samepassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2

    def test_empty_password_hashes(self):
        hashed = get_password_hash("")
        assert verify_password("", hashed) is True
        assert verify_password("notempty", hashed) is False


class TestAccessToken:
    def test_create_token_contains_sub(self):
        token = create_access_token(data={"sub": "1", "username": "test"})
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "1"
        assert payload["username"] == "test"

    def test_create_token_with_custom_expiry(self):
        delta = timedelta(minutes=5)
        token = create_access_token(data={"sub": "1"}, expires_delta=delta)
        payload = verify_token(token)
        assert payload is not None
        assert "exp" in payload

    def test_verify_invalid_token_returns_none(self):
        result = verify_token("invalid.token.here")
        assert result is None

    def test_verify_empty_string_returns_none(self):
        result = verify_token("")
        assert result is None

    def test_token_expiry_in_past(self):
        delta = timedelta(seconds=-1)
        token = create_access_token(data={"sub": "1"}, expires_delta=delta)
        result = verify_token(token)
        assert result is None
