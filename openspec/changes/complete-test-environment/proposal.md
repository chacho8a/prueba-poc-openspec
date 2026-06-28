## Why

The Task Manager application (FastAPI backend + vanilla JS frontend) currently has no automated test suite. As the application grows with features like authentication, task CRUD, filtering, and Docker deployment, there is no safety net to catch regressions. A complete test environment is needed to validate critical functionality, ensure code quality, and enable confident refactoring. All tests MUST run inside Docker containers so that developers need only Docker installed locally -- no Python, pip, virtual environments, or any other development dependency is required on the host machine.

## What Changes

- Add a dedicated `Dockerfile.test` for the test environment (installs app + test dependencies)
- Add `docker-compose.test.yml` to orchestrate test execution in an isolated container
- Add a pytest-based test infrastructure with SQLite test database isolation inside the container
- Create unit tests for authentication utilities (password hashing, JWT token creation/verification)
- Create unit tests for Pydantic schema validation (UserRegister, UserLogin, TaskCreate, TaskUpdate)
- Create integration tests for all API endpoints (auth register/login, task CRUD)
- Create end-to-end tests covering full user workflows (multi-user isolation, token reuse, lifecycle)
- Add test dependencies (pytest, httpx, pytest-cov) to a separate `requirements-test.txt`
- Add Makefile targets (`make test`, `make test-cov`) that wrap Docker commands
- Test results and coverage reports are output to the host via volume mounts

## Capabilities

### New Capabilities
- `test-infrastructure`: Docker-based test execution, fixtures, database isolation, coverage configuration, and Makefile integration
- `unit-test-suite`: Unit tests for auth utilities and Pydantic schema validation
- `integration-test-suite`: Integration tests for all REST API endpoints (auth + tasks)
- `e2e-test-suite`: End-to-end workflow tests covering multi-user scenarios and full lifecycles

### Modified Capabilities
<!-- No existing capability requirements are changing -->

## Impact

- **Dependencies**: New `requirements-test.txt` with pytest, httpx, pytest-cov (separate from production requirements.txt)
- **Docker**: New `Dockerfile.test` and `docker-compose.test.yml` for containerized test execution
- **Makefile**: New `test` and `test-cov` targets that run tests via Docker
- **Code**: New `tests/` directory with `unit/`, `integration/`, `e2e/` subdirectories and `conftest.py`
- **APIs**: No changes to existing API; tests exercise existing endpoints via FastAPI TestClient
- **Database**: Tests use an isolated SQLite test database inside the container, created/destroyed per test function
- **Host requirements**: Only Docker and Docker Compose needed. No Python, pip, or venv on the host.
- **CI/CD**: Test suite runs with `make test` (or `docker compose -f docker-compose.test.yml up --build --abort-on-container-exit`)
