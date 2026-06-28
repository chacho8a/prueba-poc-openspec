import pytest


class TestFullUserWorkflow:
    def test_register_login_create_update_complete_delete(self, client):
        register_resp = client.post("/api/auth/register", json={
            "username": "e2euser",
            "email": "e2e@example.com",
            "password": "securepass123"
        })
        assert register_resp.status_code == 200
        token = register_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        login_resp = client.post("/api/auth/login", json={
            "email": "e2e@example.com",
            "password": "securepass123"
        })
        assert login_resp.status_code == 200

        create_resp = client.post("/api/tasks/", json={
            "title": "E2E Task",
            "description": "Full workflow test",
            "priority": "high"
        }, headers=headers)
        assert create_resp.status_code == 201
        task_id = create_resp.json()["id"]
        assert create_resp.json()["status"] == "pending"

        update_resp = client.put(f"/api/tasks/{task_id}", json={
            "status": "completed",
            "priority": "low"
        }, headers=headers)
        assert update_resp.status_code == 200
        assert update_resp.json()["status"] == "completed"
        assert update_resp.json()["priority"] == "low"

        get_resp = client.get(f"/api/tasks/{task_id}", headers=headers)
        assert get_resp.status_code == 200
        assert get_resp.json()["title"] == "E2E Task"
        assert get_resp.json()["status"] == "completed"

        delete_resp = client.delete(f"/api/tasks/{task_id}", headers=headers)
        assert delete_resp.status_code == 200

        verify_resp = client.get(f"/api/tasks/{task_id}", headers=headers)
        assert verify_resp.status_code == 404

    def test_multiple_tasks_lifecycle(self, client):
        register_resp = client.post("/api/auth/register", json={
            "username": "multitasker",
            "email": "multi@example.com",
            "password": "password123"
        })
        token = register_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        for i in range(5):
            resp = client.post("/api/tasks/", json={
                "title": f"Task {i+1}",
                "priority": ["low", "medium", "high"][i % 3]
            }, headers=headers)
            assert resp.status_code == 201

        list_resp = client.get("/api/tasks/", headers=headers)
        assert len(list_resp.json()) == 5

        task_ids = [t["id"] for t in list_resp.json()]
        for tid in task_ids[:3]:
            resp = client.put(f"/api/tasks/{tid}", json={"status": "completed"}, headers=headers)
            assert resp.status_code == 200

        final_list = client.get("/api/tasks/", headers=headers)
        tasks = final_list.json()
        completed = [t for t in tasks if t["status"] == "completed"]
        pending = [t for t in tasks if t["status"] == "pending"]
        assert len(completed) == 3
        assert len(pending) == 2

    def test_concurrent_users_isolation(self, client):
        user1_resp = client.post("/api/auth/register", json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "password123"
        })
        user1_token = user1_resp.json()["access_token"]
        h1 = {"Authorization": f"Bearer {user1_token}"}

        user2_resp = client.post("/api/auth/register", json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "password123"
        })
        user2_token = user2_resp.json()["access_token"]
        h2 = {"Authorization": f"Bearer {user2_token}"}

        client.post("/api/tasks/", json={"title": "Alice Task 1"}, headers=h1)
        client.post("/api/tasks/", json={"title": "Alice Task 2"}, headers=h1)
        client.post("/api/tasks/", json={"title": "Bob Task 1"}, headers=h2)

        alice_tasks = client.get("/api/tasks/", headers=h1).json()
        bob_tasks = client.get("/api/tasks/", headers=h2).json()

        assert len(alice_tasks) == 2
        assert len(bob_tasks) == 1
        assert all(t["title"].startswith("Alice") for t in alice_tasks)
        assert all(t["title"].startswith("Bob") for t in bob_tasks)

        alice_task_id = alice_tasks[0]["id"]
        bob_delete_resp = client.delete(f"/api/tasks/{alice_task_id}", headers=h2)
        assert bob_delete_resp.status_code == 404

    def test_token_reuse_after_login(self, client):
        client.post("/api/auth/register", json={
            "username": "tokenuser",
            "email": "token@example.com",
            "password": "password123"
        })

        login1 = client.post("/api/auth/login", json={
            "email": "token@example.com",
            "password": "password123"
        })
        token1 = login1.json()["access_token"]

        login2 = client.post("/api/auth/login", json={
            "email": "token@example.com",
            "password": "password123"
        })
        token2 = login2.json()["access_token"]

        h1 = {"Authorization": f"Bearer {token1}"}
        h2 = {"Authorization": f"Bearer {token2}"}

        resp1 = client.post("/api/tasks/", json={"title": "With Token 1"}, headers=h1)
        resp2 = client.post("/api/tasks/", json={"title": "With Token 2"}, headers=h2)

        assert resp1.status_code == 201
        assert resp2.status_code == 201

    def test_unauthenticated_access_blocked(self, client):
        endpoints = [
            ("GET", "/api/tasks/"),
            ("POST", "/api/tasks/"),
            ("GET", "/api/tasks/1"),
            ("PUT", "/api/tasks/1"),
            ("DELETE", "/api/tasks/1"),
        ]
        for method, path in endpoints:
            if method == "GET":
                resp = client.get(path)
            elif method == "POST":
                resp = client.post(path, json={"title": "test"})
            elif method == "PUT":
                resp = client.put(path, json={"title": "test"})
            elif method == "DELETE":
                resp = client.delete(path)
            assert resp.status_code in (401, 403), f"{method} {path} returned {resp.status_code}"

    def test_invalid_token_rejected(self, client):
        headers = {"Authorization": "Bearer invalidtoken123"}
        resp = client.get("/api/tasks/", headers=headers)
        assert resp.status_code == 401
