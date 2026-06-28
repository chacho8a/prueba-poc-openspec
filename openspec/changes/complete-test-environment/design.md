## Context

The Task Manager is a full-stack application with a FastAPI backend (Python) providing REST APIs for user authentication (JWT-based) and task CRUD operations, plus a vanilla JS frontend. The backend uses SQLAlchemy with SQLite, Pydantic for schema validation, and passlib/bcrypt for password hashing. Currently there are zero automated tests. The application is already containerized via Docker (Dockerfile + docker-compose.yml + docker-compose.dev.yml) with a Makefile for common operations.

Key modules to test:
- `backend/auth.py`: Password hashing, JWT creation/verification, `get_current_user` dependency
- `backend/schemas.py`: Pydantic models with validators (UserRegister, UserLogin, TaskCreate, TaskUpdate)
- `backend/routers/auth.py`: POST /api/auth/register, POST /api/auth/login
- `backend/routers/tasks.py`: Full CRUD on /api/tasks/ with auth dependency

**Constraint**: All test execution MUST happen inside Docker containers. Developers must only need Docker and Docker Compose installed locally. No Python, pip, virtualenv, or any development dependency is allowed on the host machine.

## Goals / Non-Goals

**Goals:**
- Run all tests inside Docker containers -- zero local dev dependencies required
- Isolate test database from production data using a dedicated SQLite file per test run
- Achieve >90% code coverage on backend modules
- Cover all API endpoints with integration tests including error paths
- Validate multi-user data isolation in end-to-end scenarios
- Keep test execution fast (<30 seconds for full suite, excluding image build)
- Provide simple Makefile targets (`make test`, `make test-cov`) for test execution

**Non-Goals:**
- Frontend/browser-based E2E tests (Selenium/Playwright) - out of scope for this iteration
- Performance/load testing
- Testing Docker deployment configuration itself
- Modifying application code to improve testability
- Supporting local (non-Docker) test execution

## Decisions

**1. Execution environment: Docker-only via `Dockerfile.test`**
- Rationale: A dedicated `Dockerfile.test` extends the base Python image, installs both production and test dependencies, and uses pytest as the entrypoint. This guarantees a consistent, reproducible environment regardless of the host OS. Developers only need Docker installed.
- Alternatives considered: Reusing the production Dockerfile with a test stage (more complex, couples test deps to production image), running tests on the host with a venv (violates the no-local-dependency constraint), using a pre-built test image from a registry (harder to maintain parity with app code).

**2. Test orchestration: `docker-compose.test.yml`**
- Rationale: A dedicated compose file defines the test service, mounts the source code as a volume (for fast iteration without rebuilds), sets `DATABASE_URL` to an in-container test SQLite path, and uses `--abort-on-container-exit` to propagate the test exit code. This mirrors the existing docker-compose pattern used for dev and prod.
- Alternatives considered: Running `docker run` directly (less ergonomic, no compose-level config), adding a test profile to the main docker-compose.yml (couples test config to production compose, harder to reason about).

**3. Test dependencies: separate `requirements-test.txt`**
- Rationale: Keeping test dependencies (pytest, httpx, pytest-cov) in a separate file avoids polluting the production image and makes the dependency boundary explicit. `Dockerfile.test` installs both `requirements.txt` and `requirements-test.txt`.
- Alternatives considered: Adding test deps to the existing `requirements.txt` (increases production image size, blurs dev/prod boundary), using a `[test]` extras in a `pyproject.toml` (project doesn't use pyproject.toml yet, unnecessary migration).

**4. Test framework: pytest + httpx (FastAPI TestClient)**
- Rationale: FastAPI's TestClient is built on httpx and provides synchronous testing of async endpoints. pytest offers rich fixtures, parametrize support, and plugin ecosystem.
- Alternatives considered: unittest (stdlib, less ergonomic fixtures), aiohttp (async-native but less mature ecosystem)

**5. Database isolation: per-function SQLite with create_all/drop_all**
- Rationale: Each test function gets a clean database via SQLAlchemy `Base.metadata.create_all` / `drop_all` in a function-scoped fixture. This prevents test interdependence. The test SQLite file lives inside the container's ephemeral filesystem.
- Alternatives considered: shared database with manual cleanup (fragile), PostgreSQL test container (overkill for SQLite-based app), transaction rollback (complex with FastAPI dependency injection)

**6. Test directory structure: tests/{unit,integration,e2e}/**
- Rationale: Clear separation by test type allows selective execution and different fixture scopes. Unit tests need no app context, integration tests use TestClient, E2E tests compose multiple workflows.
- Alternatives considered: flat structure (harder to navigate), mirror source structure (unnecessary for this size)

**7. Fixtures via conftest.py with dependency injection override**
- Rationale: FastAPI's `app.dependency_overrides` allows replacing `get_db` with a test session. Combined with pytest fixtures, this provides clean test setup without modifying production code.
- Alternatives considered: monkeypatching database URL globally (leaks between tests), mocking at repository level (too much boilerplate)

**8. Coverage reporting: pytest-cov with volume-mounted output**
- Rationale: Measures which lines/branches are exercised. Target 90%+ on backend package. The coverage report is printed to stdout (visible in `docker compose logs`) and an HTML report is written to a volume-mounted directory so developers can inspect it in a browser without entering the container.
- Alternatives considered: coverage.py directly (pytest-cov integrates better), no coverage (no visibility into gaps)

**9. Makefile integration: `make test` and `make test-cov`**
- Rationale: Wraps the docker compose commands in familiar Makefile targets consistent with existing `make docker-build`, `make docker-up`, etc. Lowers the barrier to running tests.
- Alternatives considered: Shell scripts (less discoverable), npm scripts (project is Python, no Node.js)

## Risks / Trade-offs

- [Docker image build adds ~10-20s to each test run] → Mitigation: Mount source code as a volume so code changes don't require a rebuild. Only dependency changes require `--build`. Developers can also use `docker compose -f docker-compose.test.yml run --rm test` for repeated runs.
- [Volume-mounted htmlcov may have permission issues across OS] → Mitigation: Set explicit UID/GID in Dockerfile.test or use `user: "${UID}:${GID}"` in compose. Test first without, add if needed.
- [SQLite test DB differs from production if production uses PostgreSQL] → Mitigation: Current app defaults to SQLite; if production DB changes, add a separate test profile. For now, SQLite-on-SQLite testing is valid.
- [Function-scoped fixtures add overhead from repeated create/drop] → Mitigation: SQLite DDL is fast; full suite runs in <10s inside the container. If it grows slow, switch to class-scoped for integration tests.
- [TestClient is synchronous, doesn't test true async behavior] → Mitigation: All current endpoints are simple CRUD; async behavior is trivial. If complex async logic is added, consider httpx.AsyncClient.
- [No frontend tests] → Mitigation: Explicitly out of scope. Frontend is vanilla JS with minimal logic; API coverage validates backend contracts.
