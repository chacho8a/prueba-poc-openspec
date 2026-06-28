import pytest
from datetime import date


class TestCreateTask:
    def test_create_task_success(self, client, auth_headers):
        response = client.post("/api/tasks/", json={
            "title": "Test Task",
            "description": "A test task",
            "priority": "high"
        }, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["priority"] == "high"
        assert data["status"] == "pending"

    def test_create_task_without_auth(self, client):
        response = client.post("/api/tasks/", json={
            "title": "Unauthorized Task"
        })
        assert response.status_code == 403

    def test_create_task_empty_title(self, client, auth_headers):
        response = client.post("/api/tasks/", json={
            "title": "",
            "priority": "low"
        }, headers=auth_headers)
        assert response.status_code == 422

    def test_create_task_invalid_priority(self, client, auth_headers):
        response = client.post("/api/tasks/", json={
            "title": "Task",
            "priority": "urgent"
        }, headers=auth_headers)
        assert response.status_code == 422

    def test_create_task_with_due_date(self, client, auth_headers):
        response = client.post("/api/tasks/", json={
            "title": "Task with date",
            "due_date": "2026-12-31"
        }, headers=auth_headers)
        assert response.status_code == 201
        assert response.json()["due_date"] == "2026-12-31"


class TestGetTasks:
    def test_get_tasks_empty(self, client, auth_headers):
        response = client.get("/api/tasks/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_get_tasks_returns_user_tasks(self, client, auth_headers):
        client.post("/api/tasks/", json={"title": "Task 1"}, headers=auth_headers)
        client.post("/api/tasks/", json={"title": "Task 2"}, headers=auth_headers)
        response = client.get("/api/tasks/", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_tasks_without_auth(self, client):
        response = client.get("/api/tasks/")
        assert response.status_code == 403

    def test_get_tasks_isolation_between_users(self, client, registered_user, auth_headers):
        client.post("/api/tasks/", json={"title": "User1 Task"}, headers=auth_headers)
        user2_resp = client.post("/api/auth/register", json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "password123"
        })
        user2_token = user2_resp.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        client.post("/api/tasks/", json={"title": "User2 Task"}, headers=user2_headers)
        response = client.get("/api/tasks/", headers=auth_headers)
        titles = [t["title"] for t in response.json()]
        assert "User1 Task" in titles
        assert "User2 Task" not in titles


class TestGetTask:
    def test_get_single_task(self, client, auth_headers):
        create_resp = client.post("/api/tasks/", json={"title": "Specific Task"}, headers=auth_headers)
        task_id = create_resp.json()["id"]
        response = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Specific Task"

    def test_get_nonexistent_task(self, client, auth_headers):
        response = client.get("/api/tasks/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_get_other_users_task(self, client, registered_user, auth_headers):
        user2_resp = client.post("/api/auth/register", json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "password123"
        })
        user2_token = user2_resp.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        create_resp = client.post("/api/tasks/", json={"title": "User2 Task"}, headers=user2_headers)
        task_id = create_resp.json()["id"]
        response = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 404


class TestUpdateTask:
    def test_update_task_status(self, client, auth_headers):
        create_resp = client.post("/api/tasks/", json={"title": "Task"}, headers=auth_headers)
        task_id = create_resp.json()["id"]
        response = client.put(f"/api/tasks/{task_id}", json={"status": "completed"}, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

    def test_update_task_title(self, client, auth_headers):
        create_resp = client.post("/api/tasks/", json={"title": "Old Title"}, headers=auth_headers)
        task_id = create_resp.json()["id"]
        response = client.put(f"/api/tasks/{task_id}", json={"title": "New Title"}, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "New Title"

    def test_update_nonexistent_task(self, client, auth_headers):
        response = client.put("/api/tasks/9999", json={"title": "Updated"}, headers=auth_headers)
        assert response.status_code == 404

    def test_update_invalid_status(self, client, auth_headers):
        create_resp = client.post("/api/tasks/", json={"title": "Task"}, headers=auth_headers)
        task_id = create_resp.json()["id"]
        response = client.put(f"/api/tasks/{task_id}", json={"status": "in_progress"}, headers=auth_headers)
        assert response.status_code == 422

    def test_update_other_users_task(self, client, registered_user, auth_headers):
        user2_resp = client.post("/api/auth/register", json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "password123"
        })
        user2_token = user2_resp.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        create_resp = client.post("/api/tasks/", json={"title": "User2 Task"}, headers=user2_headers)
        task_id = create_resp.json()["id"]
        response = client.put(f"/api/tasks/{task_id}", json={"title": "Hacked"}, headers=auth_headers)
        assert response.status_code == 404


class TestDeleteTask:
    def test_delete_task(self, client, auth_headers):
        create_resp = client.post("/api/tasks/", json={"title": "To Delete"}, headers=auth_headers)
        task_id = create_resp.json()["id"]
        response = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200
        get_resp = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert get_resp.status_code == 404

    def test_delete_nonexistent_task(self, client, auth_headers):
        response = client.delete("/api/tasks/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_other_users_task(self, client, registered_user, auth_headers):
        user2_resp = client.post("/api/auth/register", json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "password123"
        })
        user2_token = user2_resp.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        create_resp = client.post("/api/tasks/", json={"title": "User2 Task"}, headers=user2_headers)
        task_id = create_resp.json()["id"]
        response = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 404
