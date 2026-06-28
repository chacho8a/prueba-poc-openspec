## ADDED Requirements

### Requirement: Password hashing unit tests
The system SHALL include unit tests for `get_password_hash` and `verify_password` functions covering correct verification, incorrect password rejection, hash uniqueness, and empty password handling.

#### Scenario: Correct password verifies successfully
- **WHEN** a password is hashed and the same password is verified against the hash
- **THEN** `verify_password` SHALL return True

#### Scenario: Incorrect password fails verification
- **WHEN** a password is hashed and a different password is verified against the hash
- **THEN** `verify_password` SHALL return False

#### Scenario: Same password produces different hashes
- **WHEN** the same password is hashed twice
- **THEN** the two hash outputs SHALL be different (due to salt)

#### Scenario: Empty password can be hashed and verified
- **WHEN** an empty string is hashed
- **THEN** the empty string SHALL verify correctly against the hash, and non-empty strings SHALL not

### Requirement: JWT token unit tests
The system SHALL include unit tests for `create_access_token` and `verify_token` functions covering token creation, payload extraction, custom expiry, invalid tokens, and expired tokens.

#### Scenario: Token contains correct payload
- **WHEN** an access token is created with `{"sub": "1", "username": "test"}`
- **THEN** `verify_token` SHALL return a dict with matching `sub` and `username` values

#### Scenario: Token with custom expiry
- **WHEN** a token is created with a custom `expires_delta`
- **THEN** the decoded token SHALL contain an `exp` claim

#### Scenario: Invalid token returns None
- **WHEN** `verify_token` is called with a malformed string
- **THEN** it SHALL return None

#### Scenario: Expired token returns None
- **WHEN** a token is created with a negative expiry delta
- **THEN** `verify_token` SHALL return None (token is expired)

### Requirement: Pydantic schema validation unit tests
The system SHALL include unit tests for all Pydantic schemas (UserRegister, UserLogin, TaskCreate, TaskUpdate) covering valid inputs, validation errors, edge cases, and default values.

#### Scenario: Valid UserRegister succeeds
- **WHEN** a UserRegister is created with valid username, email, and password (>=6 chars)
- **THEN** the schema SHALL be created without errors

#### Scenario: Empty username raises ValidationError
- **WHEN** a UserRegister is created with an empty or whitespace-only username
- **THEN** a ValidationError SHALL be raised

#### Scenario: Short password raises ValidationError
- **WHEN** a UserRegister is created with a password shorter than 6 characters
- **THEN** a ValidationError SHALL be raised

#### Scenario: Invalid email raises ValidationError
- **WHEN** a UserRegister or UserLogin is created with a malformed email
- **THEN** a ValidationError SHALL be raised

#### Scenario: TaskCreate defaults priority to medium
- **WHEN** a TaskCreate is created without specifying priority
- **THEN** the priority SHALL default to "medium"

#### Scenario: Invalid task priority raises ValidationError
- **WHEN** a TaskCreate or TaskUpdate is created with a priority not in ["low", "medium", "high"]
- **THEN** a ValidationError SHALL be raised

#### Scenario: Invalid task status raises ValidationError
- **WHEN** a TaskUpdate is created with a status not in ["pending", "completed"]
- **THEN** a ValidationError SHALL be raised

#### Scenario: Empty task title raises ValidationError
- **WHEN** a TaskCreate is created with an empty title
- **THEN** a ValidationError SHALL be raised

#### Scenario: Username and title are stripped of whitespace
- **WHEN** a UserRegister or TaskCreate is created with leading/trailing whitespace
- **THEN** the values SHALL be stripped
