## ADDED Requirements

### Requirement: Docker-based test execution
The system SHALL provide a `Dockerfile.test` that builds a container image with all production and test dependencies installed. The test entrypoint SHALL be `pytest`. No Python, pip, or development dependency SHALL be required on the host machine.

#### Scenario: Test image builds successfully
- **WHEN** `docker compose -f docker-compose.test.yml build` is executed
- **THEN** a Docker image is built containing the application code, production dependencies, and test dependencies (pytest, httpx, pytest-cov)

#### Scenario: Tests run without local Python
- **WHEN** a developer with only Docker and Docker Compose installed runs `make test`
- **THEN** all tests execute inside the Docker container and results are printed to stdout

### Requirement: Docker Compose test orchestration
The system SHALL provide a `docker-compose.test.yml` that defines a test service, mounts the source code as a volume, configures the test database URL, and exits with the pytest exit code.

#### Scenario: Compose test service definition
- **WHEN** `docker compose -f docker-compose.test.yml up --build --abort-on-container-exit` is executed
- **THEN** the test container starts, runs pytest, prints results, and exits with the pytest return code

#### Scenario: Source code mounted as volume
- **WHEN** the test container runs
- **THEN** the application source code is bind-mounted so code changes are reflected without rebuilding the image

### Requirement: Separate test dependencies file
The system SHALL provide a `requirements-test.txt` file containing test-only dependencies (pytest, httpx, pytest-cov), separate from the production `requirements.txt`.

#### Scenario: Test dependencies file exists
- **WHEN** the repository is inspected
- **THEN** a `requirements-test.txt` file SHALL exist at the project root containing pytest, httpx, and pytest-cov

#### Scenario: Production dependencies unchanged
- **WHEN** `requirements.txt` is inspected
- **THEN** it SHALL NOT contain pytest, httpx, or pytest-cov (test dependencies remain separate)

### Requirement: Makefile test targets
The system SHALL provide `make test` and `make test-cov` targets that execute tests inside Docker via docker compose.

#### Scenario: make test runs full suite
- **WHEN** `make test` is executed
- **THEN** the Docker test container is built and started, all tests run with verbose output, and the container exits with the test result code

#### Scenario: make test-cov runs with coverage
- **WHEN** `make test-cov` is executed
- **THEN** tests run with `--cov=backend --cov-report=term-missing` and a coverage report is printed to stdout

### Requirement: Test database isolation
The system SHALL provide an isolated SQLite test database for each test function inside the container. The test database MUST be created before the test runs and dropped after it completes, ensuring no state leaks between tests.

#### Scenario: Clean database per test
- **WHEN** a test function requests the `db_session` fixture
- **THEN** a fresh SQLite database is created with all tables, and after the test completes the tables are dropped

#### Scenario: Test database file is separate from production
- **WHEN** tests are executed inside the container
- **THEN** the test database file SHALL be distinct from the production database file

### Requirement: Reusable auth fixtures
The system SHALL provide `registered_user` and `auth_headers` fixtures that create a test user and return valid Bearer token headers for authenticated requests.

#### Scenario: Registered user fixture
- **WHEN** a test requests the `registered_user` fixture
- **THEN** a user is registered via POST /api/auth/register and the fixture returns the token, username, email, and password

#### Scenario: Auth headers fixture
- **WHEN** a test requests the `auth_headers` fixture
- **THEN** it receives a dictionary with `Authorization: Bearer <token>` ready for authenticated requests

### Requirement: Coverage reporting
The system SHALL support coverage measurement for the `backend` package via pytest-cov, reporting uncovered lines to stdout and optionally generating an HTML report.

#### Scenario: Coverage report generation
- **WHEN** `make test-cov` is executed
- **THEN** a coverage report is printed showing statement coverage and lines missing coverage for each backend module
