## ADDED Requirements

### Requirement: System shall filter tasks by status
The system SHALL allow users to filter the task list by status (pending, completed, or all). The interface MUST provide filter controls and update the displayed task list based on selected filter.

#### Scenario: Filter by pending status
- **WHEN** user selects "Pending" filter
- **THEN** system displays only tasks with status "pending", hiding completed tasks

#### Scenario: Filter by completed status
- **WHEN** user selects "Completed" filter
- **THEN** system displays only tasks with status "completed", hiding pending tasks

#### Scenario: Show all tasks
- **WHEN** user selects "All" filter
- **THEN** system displays all tasks regardless of status

#### Scenario: Filter persistence
- **WHEN** user has selected a filter and creates a new task
- **THEN** system maintains the selected filter and displays the new task list according to the active filter

### Requirement: System shall filter tasks by priority
The system SHALL allow users to filter the task list by priority level (low, medium, high, or all). The interface MUST provide priority filter controls and update the displayed task list based on selected priority.

#### Scenario: Filter by high priority
- **WHEN** user selects "High" priority filter
- **THEN** system displays only tasks with priority "high", hiding tasks with other priorities

#### Scenario: Filter by medium priority
- **WHEN** user selects "Medium" priority filter
- **THEN** system displays only tasks with priority "medium"

#### Scenario: Filter by low priority
- **WHEN** user selects "Low" priority filter
- **THEN** system displays only tasks with priority "low"

#### Scenario: Show all priorities
- **WHEN** user selects "All" priority filter
- **THEN** system displays all tasks regardless of priority

### Requirement: System shall search tasks by text
The system SHALL allow users to search tasks by text matching against title and description fields. The search MUST be case-insensitive and update the task list in real-time or upon search submission.

#### Scenario: Search matches task title
- **WHEN** user searches for "project" and task exists with title "Complete project"
- **THEN** system displays the matching task in filtered results

#### Scenario: Search matches task description
- **WHEN** user searches for "application" and task exists with description "Finish the web application"
- **THEN** system displays the matching task in filtered results

#### Scenario: Search is case-insensitive
- **WHEN** user searches for "PROJECT" and task exists with title "Complete project"
- **THEN** system displays the matching task in filtered results

#### Scenario: Search with no matches
- **WHEN** user searches for "nonexistent" and no tasks contain that text
- **THEN** system displays empty state message "No tasks match your search"

#### Scenario: Search combined with filters
- **WHEN** user has status filter "pending" active and searches for "project"
- **THEN** system displays only pending tasks that match the search text

### Requirement: System shall sort tasks by different criteria
The system SHALL allow users to sort the task list by creation date, due date, priority, or title. The interface MUST provide sort controls and update the displayed task order based on selected criteria.

#### Scenario: Sort by creation date descending (default)
- **WHEN** user selects "Newest first" sort option
- **THEN** system displays tasks ordered by created_at timestamp in descending order (newest first)

#### Scenario: Sort by creation date ascending
- **WHEN** user selects "Oldest first" sort option
- **THEN** system displays tasks ordered by created_at timestamp in ascending order (oldest first)

#### Scenario: Sort by due date
- **WHEN** user selects "Due date" sort option
- **THEN** system displays tasks ordered by due_date ascending, with tasks without due dates at the end

#### Scenario: Sort by priority
- **WHEN** user selects "Priority" sort option
- **THEN** system displays tasks ordered by priority level (high first, then medium, then low)

#### Scenario: Sort by title
- **WHEN** user selects "Title" sort option
- **THEN** system displays tasks ordered alphabetically by title (A-Z)

### Requirement: System shall combine multiple filters and search
The system SHALL allow users to combine status filter, priority filter, search text, and sort criteria simultaneously. The interface MUST apply all active filters and search criteria together to produce the final task list.

#### Scenario: Combined status and priority filter
- **WHEN** user selects status "pending" and priority "high"
- **THEN** system displays only tasks that are both pending AND have high priority

#### Scenario: Combined filter and search
- **WHEN** user has status filter "pending" active and searches for "project"
- **THEN** system displays only pending tasks that match the search text

#### Scenario: Combined filter, search, and sort
- **WHEN** user has status filter "pending", priority filter "high", searches for "project", and sorts by "due date"
- **THEN** system displays only pending high-priority tasks matching "project", ordered by due date

#### Scenario: Clear all filters
- **WHEN** user clicks "Clear filters" button or resets filter controls
- **THEN** system clears all active filters and search, displaying all tasks with default sort order

### Requirement: System shall display filter and search result counts
The system SHALL display the count of tasks matching current filters and search criteria. The interface MUST show both filtered count and total count when filters are active.

#### Scenario: Filter result count display
- **WHEN** user has filters active showing 3 tasks out of 10 total
- **THEN** system displays "Showing 3 of 10 tasks" or similar count indicator

#### Scenario: No filters active
- **WHEN** no filters or search are active
- **THEN** system displays total task count (e.g., "10 tasks") or no count indicator

#### Scenario: Empty filter results
- **WHEN** filters result in zero matching tasks
- **THEN** system displays "No tasks match your filters" message with option to clear filters
