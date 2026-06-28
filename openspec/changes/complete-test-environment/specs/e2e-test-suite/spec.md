## ADDED Requirements

### Requirement: Full user lifecycle E2E test
The system SHALL include an end-to-end test that exercises the complete user workflow: register, login, create task, update task, verify task, delete task, and confirm deletion.

#### Scenario: Complete lifecycle from registration to deletion
- **WHEN** a user registers, logs in, creates a task, updates its status to completed, retrieves it, deletes it, and tries to retrieve it again
- **THEN** each step SHALL succeed with expected status codes and the final retrieval SHALL return 404

### Requirement: Multiple tasks lifecycle E2E test
The system SHALL include an end-to-end test that creates multiple tasks, lists them, partially completes them, and verifies the correct counts of completed vs pending tasks.

#### Scenario: Create 5 tasks and complete 3
- **WHEN** a user creates 5 tasks with varying priorities, then updates 3 to "completed"
- **THEN** the task list SHALL contain exactly 3 completed and 2 pending tasks

### Requirement: Multi-user isolation E2E test
The system SHALL include an end-to-end test that verifies two users can operate independently without interfering with each other's data.

#### Scenario: Two users with separate task lists
- **WHEN** user A creates 2 tasks and user B creates 1 task
- **THEN** user A's task list SHALL contain only their 2 tasks, user B's list SHALL contain only their 1 task, and user B SHALL NOT be able to delete user A's task (404)

### Requirement: Token reuse E2E test
The system SHALL include an end-to-end test verifying that multiple login sessions produce independent valid tokens that can both be used to create tasks.

#### Scenario: Two separate logins both work
- **WHEN** a user logs in twice, obtaining two different tokens
- **THEN** both tokens SHALL be usable to create tasks successfully

### Requirement: Unauthenticated access block E2E test
The system SHALL include an end-to-end test that verifies all protected endpoints reject requests without authentication.

#### Scenario: All task endpoints reject unauthenticated requests
- **WHEN** GET /api/tasks/, POST /api/tasks/, GET /api/tasks/1, PUT /api/tasks/1, DELETE /api/tasks/1 are called without Authorization header
- **THEN** each request SHALL return 401 or 403

### Requirement: Invalid token rejection E2E test
The system SHALL include an end-to-end test that verifies requests with an invalid Bearer token are rejected.

#### Scenario: Fake token is rejected
- **WHEN** a request is made with `Authorization: Bearer invalidtoken123`
- **THEN** the response SHALL be 401
