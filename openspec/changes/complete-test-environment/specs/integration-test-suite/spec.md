## ADDED Requirements

### Requirement: Auth API integration tests
The system SHALL include integration tests for POST /api/auth/register and POST /api/auth/login endpoints covering success cases, duplicate handling, invalid inputs, and authentication failures.

#### Scenario: Successful registration returns token
- **WHEN** a POST request is made to /api/auth/register with valid unique username, email, and password
- **THEN** the response SHALL be 200 with `access_token` and `token_type: "bearer"`

#### Scenario: Duplicate username rejected
- **WHEN** a registration request uses a username that already exists
- **THEN** the response SHALL be 400 with detail "Username already registered"

#### Scenario: Duplicate email rejected
- **WHEN** a registration request uses an email that already exists
- **THEN** the response SHALL be 400 with detail "Email already registered"

#### Scenario: Invalid email format rejected
- **WHEN** a registration or login request uses a malformed email
- **THEN** the response SHALL be 422 (validation error)

#### Scenario: Short password rejected
- **WHEN** a registration request uses a password shorter than 6 characters
- **THEN** the response SHALL be 422

#### Scenario: Empty username rejected
- **WHEN** a registration request uses an empty username
- **THEN** the response SHALL be 422

#### Scenario: Successful login returns token
- **WHEN** a POST request is made to /api/auth/login with correct email and password
- **THEN** the response SHALL be 200 with `access_token`

#### Scenario: Wrong password rejected
- **WHEN** a login request uses an incorrect password
- **THEN** the response SHALL be 401

#### Scenario: Non-existent user login rejected
- **WHEN** a login request uses an email not registered
- **THEN** the response SHALL be 401

### Requirement: Task CRUD integration tests
The system SHALL include integration tests for all task endpoints (POST, GET list, GET single, PUT, DELETE) covering success, authorization, validation, and ownership enforcement.

#### Scenario: Create task with valid data
- **WHEN** an authenticated POST request is made to /api/tasks/ with valid title
- **THEN** the response SHALL be 201 with the created task including status "pending"

#### Scenario: Create task without auth fails
- **WHEN** a POST request is made to /api/tasks/ without Authorization header
- **THEN** the response SHALL be 403

#### Scenario: Create task with empty title fails
- **WHEN** an authenticated POST request has an empty title
- **THEN** the response SHALL be 422

#### Scenario: Get tasks returns only user's tasks
- **WHEN** an authenticated GET request is made to /api/tasks/
- **THEN** only tasks belonging to the authenticated user SHALL be returned

#### Scenario: Get tasks without auth fails
- **WHEN** a GET request is made to /api/tasks/ without Authorization
- **THEN** the response SHALL be 403

#### Scenario: Get single task by ID
- **WHEN** an authenticated GET request is made to /api/tasks/{id}
- **THEN** the correct task SHALL be returned

#### Scenario: Get non-existent task returns 404
- **WHEN** an authenticated GET request is made for a task ID that does not exist
- **THEN** the response SHALL be 404

#### Scenario: Cannot access another user's task
- **WHEN** an authenticated GET request is made for a task belonging to a different user
- **THEN** the response SHALL be 404

#### Scenario: Update task status
- **WHEN** an authenticated PUT request updates a task's status to "completed"
- **THEN** the task SHALL be updated and returned with the new status

#### Scenario: Update with invalid status fails
- **WHEN** an authenticated PUT request sets status to an invalid value
- **THEN** the response SHALL be 422

#### Scenario: Cannot update another user's task
- **WHEN** an authenticated PUT request targets a task belonging to a different user
- **THEN** the response SHALL be 404

#### Scenario: Delete task
- **WHEN** an authenticated DELETE request is made to /api/tasks/{id}
- **THEN** the response SHALL be 200 and subsequent GET SHALL return 404

#### Scenario: Cannot delete another user's task
- **WHEN** an authenticated DELETE request targets a task belonging to a different user
- **THEN** the response SHALL be 404
