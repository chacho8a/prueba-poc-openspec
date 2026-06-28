## ADDED Requirements

### Requirement: System shall display login and registration interface
The system SHALL provide login and registration screens for user authentication. The interface MUST include a login form with email and password fields, a registration form with username, email, and password fields, and a toggle to switch between login and registration modes.

#### Scenario: Login screen display on app load
- **WHEN** user opens the application without a valid JWT token
- **THEN** system displays login screen with email and password fields, "Login" button, and link to switch to registration

#### Scenario: Registration screen display
- **WHEN** user clicks "Register" link on login screen
- **THEN** system displays registration form with username, email, password, and confirm password fields, "Register" button, and link to switch to login

#### Scenario: Successful login via UI
- **WHEN** user enters valid email and password and clicks "Login"
- **THEN** system stores JWT token in localStorage, redirects to task list, and displays user greeting in header

#### Scenario: Login failure via UI
- **WHEN** user enters invalid credentials and clicks "Login"
- **THEN** system displays error message "Invalid email or password" on login form

#### Scenario: Successful registration via UI
- **WHEN** user fills registration form with valid data and clicks "Register"
- **THEN** system stores JWT token in localStorage, redirects to task list, and displays user greeting in header

#### Scenario: Registration validation in UI
- **WHEN** user submits registration form with password shorter than 6 characters
- **THEN** system displays error message "Password must be at least 6 characters"

### Requirement: System shall display task list interface
The system SHALL provide a web-based user interface displaying all tasks in a clear, organized list format. The interface MUST show task title, status, priority, due date, and provide visual indicators for task state.

#### Scenario: Task list display with tasks
- **WHEN** user opens the application and tasks exist in database
- **THEN** system displays list of all tasks showing title, status badge (pending/completed), priority indicator (low/medium/high), and due date for each task

#### Scenario: Task list display when empty
- **WHEN** user opens the application and no tasks exist
- **THEN** system displays empty state message "No tasks yet. Create your first task!" with prominent create button

#### Scenario: Task status visual indicator
- **WHEN** task list is displayed
- **THEN** system shows pending tasks with one visual style (e.g., blue badge) and completed tasks with different style (e.g., green badge with strikethrough title)

#### Scenario: Task priority visual indicator
- **WHEN** task list is displayed
- **THEN** system shows priority using color-coded indicators (e.g., red for high, yellow for medium, green for low)

### Requirement: System shall provide task creation form
The system SHALL provide a form interface for creating new tasks. The form MUST include fields for title (required), description (optional), priority (optional dropdown), and due date (optional date picker), with a submit button.

#### Scenario: Task creation form display
- **WHEN** user clicks "Add Task" button or opens creation interface
- **THEN** system displays form with title input field (required), description textarea, priority dropdown (low/medium/high with medium default), due date date picker, and "Create Task" submit button

#### Scenario: Successful task creation via UI
- **WHEN** user fills in title "New task", selects priority "high", sets due date, and clicks "Create Task"
- **THEN** system creates the task, shows success message, clears the form, and refreshes task list to include new task

#### Scenario: Task creation validation in UI
- **WHEN** user attempts to submit form with empty title field
- **THEN** system displays validation error message "Title is required" near the title field and prevents form submission

#### Scenario: Task creation error handling
- **WHEN** task creation fails due to server error
- **THEN** system displays error message "Failed to create task. Please try again." and preserves form data

### Requirement: System shall provide task editing interface
The system SHALL allow users to edit existing tasks through an inline or modal form interface. The interface MUST pre-populate form fields with current task data and allow updating any mutable field.

#### Scenario: Task edit form display
- **WHEN** user clicks "Edit" button on a task
- **THEN** system displays edit form pre-filled with current task data (title, description, priority, due date, status)

#### Scenario: Successful task update via UI
- **WHEN** user changes task status to "completed" and clicks "Save"
- **THEN** system updates the task, shows success message, closes edit form, and refreshes task list with updated task

#### Scenario: Task edit validation
- **WHEN** user clears the title field in edit form and attempts to save
- **THEN** system displays validation error "Title cannot be empty" and prevents save operation

#### Scenario: Task edit cancellation
- **WHEN** user clicks "Cancel" button in edit form
- **THEN** system closes edit form without saving changes and returns to task list view

### Requirement: System shall provide task deletion confirmation
The system SHALL require user confirmation before deleting tasks to prevent accidental data loss. The interface MUST display a confirmation dialog showing the task title being deleted.

#### Scenario: Task deletion confirmation display
- **WHEN** user clicks "Delete" button on a task
- **THEN** system displays confirmation dialog with message "Are you sure you want to delete task '[task title]'?" and "Confirm" and "Cancel" buttons

#### Scenario: Confirmed task deletion
- **WHEN** user clicks "Confirm" in deletion dialog
- **THEN** system deletes the task, shows success message "Task deleted", and refreshes task list

#### Scenario: Cancelled task deletion
- **WHEN** user clicks "Cancel" in deletion dialog
- **THEN** system closes dialog without deleting task and returns to task list view

### Requirement: System shall provide task status toggle
The system SHALL provide a quick action to toggle task status between "pending" and "completed". The interface MUST include a checkbox, button, or similar control for each task.

#### Scenario: Mark task as completed
- **WHEN** user clicks status toggle on a pending task
- **THEN** system updates task status to "completed", shows visual update immediately, and displays success message

#### Scenario: Mark task as pending
- **WHEN** user clicks status toggle on a completed task
- **THEN** system updates task status to "pending", shows visual update immediately, and displays success message

#### Scenario: Status toggle error handling
- **WHEN** status toggle fails due to server error
- **THEN** system displays error message and reverts visual state to previous status

### Requirement: System shall provide responsive design
The system SHALL provide a responsive user interface that works on desktop, tablet, and mobile browsers. The interface MUST adapt layout and sizing based on screen width.

#### Scenario: Desktop layout
- **WHEN** user accesses application on desktop browser (screen width > 768px)
- **THEN** system displays full-width layout with task list, forms, and controls optimized for large screens

#### Scenario: Mobile layout
- **WHEN** user accesses application on mobile browser (screen width <= 768px)
- **THEN** system displays single-column layout with stacked elements, touch-friendly buttons, and appropriate font sizes

### Requirement: System shall provide logout functionality in header
The system SHALL display a logout button in the application header when user is authenticated. The header MUST also display the authenticated user's username. Clicking logout SHALL clear the JWT token and redirect to login screen.

#### Scenario: Header displays user info and logout
- **WHEN** user is authenticated and on task list page
- **THEN** system displays header with username greeting (e.g., "Hello, john") and "Logout" button

#### Scenario: Logout via header button
- **WHEN** user clicks "Logout" button in header
- **THEN** system removes JWT token from localStorage, redirects to login screen, and clears all task data from UI

### Requirement: System shall redirect unauthenticated users to login
The system SHALL automatically redirect users to the login screen when they attempt to access protected pages without a valid JWT token. The system MUST check for token existence and validity on page load.

#### Scenario: Redirect to login on page load without token
- **WHEN** user navigates to application URL without JWT token in localStorage
- **THEN** system redirects to login screen instead of displaying task list

#### Scenario: Redirect to login on expired token
- **WHEN** user has expired JWT token and makes API request
- **THEN** system receives 401 response, removes expired token, and redirects to login screen with message "Session expired. Please login again."

### Requirement: System shall provide loading and error states
The system SHALL display loading indicators during API calls and error messages when operations fail. The interface MUST provide clear feedback for all user actions.

#### Scenario: Loading state during API call
- **WHEN** user initiates action that requires API call (create, update, delete)
- **THEN** system displays loading indicator (spinner or disabled button with "Loading..." text) until operation completes

#### Scenario: Error message display
- **WHEN** API call fails
- **THEN** system displays error message in visible location (e.g., toast notification or alert box) with descriptive text

#### Scenario: Success message display
- **WHEN** operation completes successfully
- **THEN** system displays success message (e.g., "Task created", "Task updated", "Task deleted") that auto-dismisses after 3 seconds
