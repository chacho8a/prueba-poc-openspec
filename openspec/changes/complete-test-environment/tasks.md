## 1. Docker Test Infrastructure

- [x] 1.1 Create `requirements-test.txt` with pytest, httpx, and pytest-cov (separate from production requirements.txt)
- [x] 1.2 Create `Dockerfile.test` that extends python:3.11-slim, installs both requirements.txt and requirements-test.txt, copies application code, and sets pytest as the default entrypoint
- [x] 1.3 Create `docker-compose.test.yml` defining a test service that uses Dockerfile.test, mounts source code as a volume, sets DATABASE_URL to an in-container test SQLite path, and configures the container to exit with pytest's return code
- [x] 1.4 Add `test` and `test-cov` targets to the Makefile that wrap docker compose test commands
- [x] 1.5 Verify Docker test infrastructure by running `make test` and confirming the container builds and pytest collects zero tests successfully

## 2. Test Directory Structure and Fixtures

- [x] 2.1 Create tests/ directory structure: tests/, tests/unit/, tests/integration/, tests/e2e/ with __init__.py files
- [x] 2.2 Create tests/conftest.py with SQLite test engine, db_session fixture (function-scoped, create_all/drop_all), client fixture (TestClient with dependency_overrides), registered_user fixture, and auth_headers fixture

## 3. Unit Tests - Auth Utilities

- [x] 3.1 Create tests/unit/test_auth.py with TestPasswordHashing class: test correct verification, incorrect rejection, hash uniqueness (salt), and empty password handling
- [x] 3.2 Add TestAccessToken class: test token payload extraction, custom expiry, invalid token returns None, empty string returns None, and expired token returns None

## 4. Unit Tests - Schema Validation

- [x] 4.1 Create tests/unit/test_schemas.py with TestUserRegister class: test valid registration, empty username, whitespace username, short password, invalid email, and username stripping
- [x] 4.2 Add TestUserLogin class: test valid login and invalid email format
- [x] 4.3 Add TestTaskCreate class: test valid task, empty title, invalid priority, default priority, valid due_date, and title stripping
- [x] 4.4 Add TestTaskUpdate class: test partial update, invalid status, invalid priority, empty string title, and valid full update

## 5. Integration Tests - Auth API

- [x] 5.1 Create tests/integration/test_auth_api.py with TestRegisterEndpoint class: test successful registration, duplicate username, duplicate email, invalid email format, short password, and empty username
- [x] 5.2 Add TestLoginEndpoint class: test successful login, wrong password, non-existent user, and invalid email format

## 6. Integration Tests - Tasks API

- [x] 6.1 Create tests/integration/test_tasks_api.py with TestCreateTask class: test success, without auth (403), empty title (422), invalid priority (422), and with due_date
- [x] 6.2 Add TestGetTasks class: test empty list, returns user tasks, without auth (403), and isolation between users
- [x] 6.3 Add TestGetTask class: test single task retrieval, non-existent task (404), and other user's task (404)
- [x] 6.4 Add TestUpdateTask class: test status update, title update, non-existent task (404), invalid status (422), and other user's task (404)
- [x] 6.5 Add TestDeleteTask class: test successful delete (verify 404 after), non-existent task (404), and other user's task (404)

## 7. End-to-End Tests

- [x] 7.1 Create tests/e2e/test_workflows.py with TestFullUserWorkflow class: test complete lifecycle (register, login, create, update, verify, delete, confirm 404)
- [x] 7.2 Add test_multiple_tasks_lifecycle: create 5 tasks, complete 3, verify counts
- [x] 7.3 Add test_concurrent_users_isolation: two users create tasks, verify lists are separate, verify cross-user delete fails
- [x] 7.4 Add test_token_reuse_after_login: two logins produce independent tokens, both can create tasks
- [x] 7.5 Add test_unauthenticated_access_blocked: iterate all task endpoints without auth, verify 401/403
- [x] 7.6 Add test_invalid_token_rejected: request with fake Bearer token returns 401

## 8. Verification and Coverage

- [x] 8.1 Run `make test` and confirm all tests pass inside the Docker container
- [x] 8.2 Run `make test-cov` and verify >90% coverage on the backend package
- [x] 8.3 Confirm no Python, pip, or test dependencies are required on the host machine (only Docker and Docker Compose)
