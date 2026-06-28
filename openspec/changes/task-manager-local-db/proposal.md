## Why

Students need to demonstrate proficiency in developing web applications using AI assistants. A task manager with local database persistence, user authentication, and containerized deployment provides a practical, self-contained project that showcases full-stack development capabilities, database integration, security patterns, and modern deployment workflows while meeting academic requirements for evaluating AI-assisted programming skills.

## What Changes

- New web application for task management with complete CRUD functionality
- Local SQLite database integration for persistent task storage
- RESTful API backend for task operations with JWT-based authentication
- User registration and login system with secure password hashing
- Responsive web frontend for user interaction with login/logout flow
- Task attributes: title, description, status (pending/completed), priority, due date, creation timestamp
- Task filtering and sorting capabilities
- Data persistence across application restarts
- Docker and Docker Compose configuration for one-command deployment

## Capabilities

### New Capabilities
- `task-crud`: Core task management operations (create, read, update, delete) with validation and error handling
- `task-persistence`: SQLite database integration for storing and retrieving task data with schema management
- `task-api`: RESTful API endpoints for all task operations with proper HTTP status codes
- `task-ui`: Web-based user interface for interacting with tasks, including forms, lists, and status management
- `task-filtering`: Search, filter, and sort functionality for task lists
- `user-auth`: User registration, login/logout, JWT token management, and protected API routes with password hashing
- `docker-deployment`: Dockerfile and docker-compose.yml for containerized application deployment with volume persistence

### Modified Capabilities
- `task-api`: All task endpoints now require JWT authentication; requests without valid token return 401
- `task-ui`: Added login and registration screens; logout button in header; redirect to login when unauthenticated

## Impact

- **New codebase**: Complete web application structure with frontend and backend components
- **Dependencies**: Web framework (FastAPI), SQLite database driver, python-jose (JWT), passlib+bcrypt (password hashing), python-multipart (form data)
- **Database**: Local SQLite database file for task and user storage
- **API**: New RESTful endpoints for task management and authentication
- **UI**: Browser-based interface with login/registration flow requiring modern web browser
- **Deployment**: Docker and Docker Compose for containerized execution with persistent volumes
- **Development**: All code generated through AI assistant interaction per academic requirements
