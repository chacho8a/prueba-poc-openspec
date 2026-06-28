## ADDED Requirements

### Requirement: System shall provide user registration
The system SHALL allow new users to register by providing a username, email, and password. The system MUST validate that username and email are unique, password meets minimum length requirements (at least 6 characters), and store passwords as bcrypt hashes. The system SHALL return a JWT token upon successful registration.

#### Scenario: Successful user registration
- **WHEN** user submits registration form with username "john", email "john@example.com", and password "secret123"
- **THEN** system creates new user with bcrypt-hashed password, returns JWT token, and redirects to task list

#### Scenario: Registration fails with duplicate username
- **WHEN** user attempts to register with username that already exists
- **THEN** system returns 400 Bad Request with error message "Username already registered"

#### Scenario: Registration fails with duplicate email
- **WHEN** user attempts to register with email that already exists
- **THEN** system returns 400 Bad Request with error message "Email already registered"

#### Scenario: Registration fails with short password
- **WHEN** user submits registration form with password shorter than 6 characters
- **THEN** system returns 400 Bad Request with error message "Password must be at least 6 characters"

#### Scenario: Registration fails with invalid email format
- **WHEN** user submits registration form with invalid email format (missing @ or domain)
- **THEN** system returns 400 Bad Request with error message "Invalid email format"

### Requirement: System shall provide user login
The system SHALL allow registered users to login with their email and password. The system MUST verify the password against the stored bcrypt hash and return a JWT token upon successful authentication. The system SHALL return 401 Unauthorized for invalid credentials.

#### Scenario: Successful login with valid credentials
- **WHEN** user submits login form with registered email "john@example.com" and correct password "secret123"
- **THEN** system verifies password hash, generates JWT token with user ID and expiration, and returns token to client

#### Scenario: Login fails with incorrect password
- **WHEN** user submits login form with registered email but incorrect password
- **THEN** system returns 401 Unauthorized with error message "Invalid email or password"

#### Scenario: Login fails with unregistered email
- **WHEN** user submits login form with email that is not registered
- **THEN** system returns 401 Unauthorized with error message "Invalid email or password"

### Requirement: System shall protect API endpoints with JWT authentication
The system SHALL require a valid JWT token for all task-related API endpoints. The system MUST extract the token from the Authorization header (Bearer scheme), validate the token signature and expiration, and identify the authenticated user. Requests without valid token SHALL return 401 Unauthorized.

#### Scenario: API request with valid JWT token
- **WHEN** client sends GET /api/tasks with Authorization header "Bearer <valid-token>"
- **THEN** system validates token, identifies user, and returns tasks belonging to that user

#### Scenario: API request without Authorization header
- **WHEN** client sends GET /api/tasks without Authorization header
- **THEN** system returns 401 Unauthorized with error message "Not authenticated"

#### Scenario: API request with expired JWT token
- **WHEN** client sends request with expired JWT token
- **THEN** system returns 401 Unauthorized with error message "Token has expired"

#### Scenario: API request with invalid JWT token
- **WHEN** client sends request with malformed or tampered JWT token
- **THEN** system returns 401 Unauthorized with error message "Invalid token"

### Requirement: System shall provide user logout
The system SHALL provide a logout mechanism that clears the JWT token from the client. Since JWT is stateless, logout is handled client-side by removing the token from localStorage. The system SHALL provide a POST /api/auth/logout endpoint for logging the logout event (optional).

#### Scenario: User clicks logout button
- **WHEN** user clicks "Logout" button in the UI
- **THEN** system removes JWT token from localStorage, clears user session state, and redirects to login page

#### Scenario: Protected route access after logout
- **WHEN** user attempts to access task list after logout
- **THEN** system detects missing token and redirects to login page

### Requirement: System shall enforce task ownership
The system SHALL ensure that each task is associated with the user who created it. The system MUST automatically filter task queries by the authenticated user's ID, preventing users from accessing other users' tasks. Task creation SHALL automatically assign the authenticated user as the owner.

#### Scenario: User can only see their own tasks
- **WHEN** user "john" requests GET /api/tasks
- **THEN** system returns only tasks where user_id matches john's ID, excluding tasks created by other users

#### Scenario: Task creation assigns ownership
- **WHEN** authenticated user creates a new task
- **THEN** system automatically sets task's user_id to the authenticated user's ID

#### Scenario: User cannot access another user's task
- **WHEN** user attempts to GET /api/tasks/5 which belongs to another user
- **THEN** system returns 404 Not Found (task not visible to requesting user)

#### Scenario: User cannot update another user's task
- **WHEN** user attempts to PUT /api/tasks/5 which belongs to another user
- **THEN** system returns 404 Not Found

#### Scenario: User cannot delete another user's task
- **WHEN** user attempts to DELETE /api/tasks/5 which belongs to another user
- **THEN** system returns 404 Not Found

### Requirement: System shall use secure password hashing
The system SHALL hash all user passwords using bcrypt before storing in the database. The system MUST NEVER store plain-text passwords. The system SHALL use passlib library with bcrypt scheme for hashing and verification.

#### Scenario: Password hashed on registration
- **WHEN** user registers with password "secret123"
- **THEN** system generates bcrypt hash with random salt and stores only the hash in database

#### Scenario: Password verified on login
- **WHEN** user attempts login with password
- **THEN** system retrieves stored hash, verifies submitted password against hash using bcrypt, and authenticates if match

#### Scenario: Plain-text passwords never stored
- **WHEN** inspecting database users table
- **THEN** only hashed_password column exists; no plain-text password column or data present

### Requirement: System shall generate JWT tokens with expiration
The system SHALL generate JWT tokens containing user ID, username, and expiration timestamp. Tokens MUST be signed with a secret key and have a configurable expiration time (default 30 minutes). The system SHALL use python-jose library for token operations.

#### Scenario: JWT token contains user information
- **WHEN** JWT token is decoded
- **THEN** token payload contains sub (user ID), username, and exp (expiration timestamp)

#### Scenario: JWT token expires after configured time
- **WHEN** JWT token is used after expiration time (30 minutes after issuance)
- **THEN** system rejects token and returns 401 Unauthorized

#### Scenario: JWT secret key configurable via environment variable
- **WHEN** application starts
- **THEN** system reads JWT secret key from SECRET_KEY environment variable or uses default development key
