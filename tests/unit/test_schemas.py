import pytest
from pydantic import ValidationError
from datetime import date
from backend.schemas import (
    UserRegister,
    UserLogin,
    TaskCreate,
    TaskUpdate,
)


class TestUserRegister:
    def test_valid_registration(self):
        user = UserRegister(username="john", email="john@example.com", password="password123")
        assert user.username == "john"
        assert user.email == "john@example.com"

    def test_empty_username_raises_error(self):
        with pytest.raises(ValidationError):
            UserRegister(username="", email="john@example.com", password="password123")

    def test_whitespace_username_raises_error(self):
        with pytest.raises(ValidationError):
            UserRegister(username="   ", email="john@example.com", password="password123")

    def test_short_password_raises_error(self):
        with pytest.raises(ValidationError):
            UserRegister(username="john", email="john@example.com", password="12345")

    def test_invalid_email_raises_error(self):
        with pytest.raises(ValidationError):
            UserRegister(username="john", email="notanemail", password="password123")

    def test_username_is_stripped(self):
        user = UserRegister(username="  john  ", email="john@example.com", password="password123")
        assert user.username == "john"


class TestUserLogin:
    def test_valid_login(self):
        login = UserLogin(email="john@example.com", password="password123")
        assert login.email == "john@example.com"

    def test_invalid_email_raises_error(self):
        with pytest.raises(ValidationError):
            UserLogin(email="invalid", password="password123")


class TestTaskCreate:
    def test_valid_task(self):
        task = TaskCreate(title="My Task", priority="high")
        assert task.title == "My Task"
        assert task.priority == "high"

    def test_empty_title_raises_error(self):
        with pytest.raises(ValidationError):
            TaskCreate(title="", priority="low")

    def test_invalid_priority_raises_error(self):
        with pytest.raises(ValidationError):
            TaskCreate(title="Task", priority="urgent")

    def test_default_priority_is_medium(self):
        task = TaskCreate(title="Task")
        assert task.priority == "medium"

    def test_valid_due_date(self):
        task = TaskCreate(title="Task", due_date=date(2026, 12, 31))
        assert task.due_date == date(2026, 12, 31)

    def test_title_is_stripped(self):
        task = TaskCreate(title="  My Task  ")
        assert task.title == "My Task"


class TestTaskUpdate:
    def test_partial_update(self):
        update = TaskUpdate(status="completed")
        assert update.status == "completed"
        assert update.title is None

    def test_invalid_status_raises_error(self):
        with pytest.raises(ValidationError):
            TaskUpdate(status="in_progress")

    def test_invalid_priority_raises_error(self):
        with pytest.raises(ValidationError):
            TaskUpdate(priority="critical")

    def test_empty_string_title_raises_error(self):
        with pytest.raises(ValidationError):
            TaskUpdate(title="   ")

    def test_valid_full_update(self):
        update = TaskUpdate(
            title="Updated",
            description="New desc",
            status="pending",
            priority="low",
            due_date=date(2026, 6, 1)
        )
        assert update.title == "Updated"
        assert update.priority == "low"
