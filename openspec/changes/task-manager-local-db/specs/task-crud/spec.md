## ADDED Requirements

### Requirement: System shall create new tasks
The system SHALL allow users to create new tasks by providing a title (required), description (optional), priority (optional, defaults to medium), and due date (optional). The system MUST validate that the title is not empty and assign a unique identifier, creation timestamp, and default status of "pending" to each new task.

#### Scenario: Successful task creation with all fields
- **WHEN** user submits a task with title "Complete project", description "Finish the web application", priority "high", and due date "2026-07-01"
- **THEN** system creates a new task with unique ID, status "pending", all provided fields, creation timestamp, and returns success confirmation

#### Scenario: Successful task creation with minimal fields
- **WHEN** user submits a task with only title "Buy groceries"
- **THEN** system creates a new task with unique ID, status "pending", priority "medium", empty description, no due date, creation timestamp, and returns success confirmation

#### Scenario: Task creation fails with empty title
- **WHEN** user attempts to create a task with an empty or whitespace-only title
- **THEN** system rejects the creation request and returns validation error message indicating title is required

### Requirement: System shall retrieve individual tasks
The system SHALL allow users to retrieve a specific task by its unique identifier. The system MUST return all task fields including id, title, description, status, priority, due date, creation timestamp, and last update timestamp.

#### Scenario: Successful task retrieval
- **WHEN** user requests task with ID "123"
- **THEN** system returns complete task object with all fields (id, title, description, status, priority, due_date, created_at, updated_at)

#### Scenario: Task retrieval fails for non-existent task
- **WHEN** user requests task with ID "999" that does not exist
- **THEN** system returns 404 Not Found error with descriptive message

### Requirement: System shall update existing tasks
The system SHALL allow users to update any mutable field of an existing task (title, description, status, priority, due date). The system MUST validate that the task exists, the title is not empty if provided, and update the last modification timestamp upon successful update.

#### Scenario: Successful task status update
- **WHEN** user updates task ID "123" to change status from "pending" to "completed"
- **THEN** system updates the task status, sets updated_at timestamp to current time, and returns success confirmation with updated task data

#### Scenario: Successful task field update
- **WHEN** user updates task ID "123" to change title to "Updated title" and priority to "high"
- **THEN** system updates both fields, sets updated_at timestamp, and returns success confirmation with updated task data

#### Scenario: Task update fails for non-existent task
- **WHEN** user attempts to update task ID "999" that does not exist
- **THEN** system returns 404 Not Found error with descriptive message

#### Scenario: Task update fails with empty title
- **WHEN** user attempts to update task ID "123" with an empty or whitespace-only title
- **THEN** system rejects the update request and returns validation error message indicating title cannot be empty

### Requirement: System shall delete tasks
The system SHALL allow users to permanently delete existing tasks by their unique identifier. The system MUST validate that the task exists before deletion and remove all associated data from the database.

#### Scenario: Successful task deletion
- **WHEN** user deletes task ID "123"
- **THEN** system permanently removes the task from database and returns success confirmation

#### Scenario: Task deletion fails for non-existent task
- **WHEN** user attempts to delete task ID "999" that does not exist
- **THEN** system returns 404 Not Found error with descriptive message

### Requirement: System shall retrieve all tasks
The system SHALL provide a method to retrieve all tasks from the database. The system MUST return tasks ordered by creation date (newest first) by default.

#### Scenario: Retrieve all tasks when tasks exist
- **WHEN** user requests all tasks and database contains 5 tasks
- **THEN** system returns array of all 5 task objects ordered by created_at descending (newest first)

#### Scenario: Retrieve all tasks when no tasks exist
- **WHEN** user requests all tasks and database is empty
- **THEN** system returns empty array with success status
