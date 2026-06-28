## Context

This is a new web application project for academic purposes, demonstrating AI-assisted development of a full-stack task management system. The application must be self-contained, easy to deploy locally, and showcase fundamental web development patterns including CRUD operations, database persistence, RESTful API design, and responsive user interfaces.

The target users are students and instructors evaluating the effectiveness of AI-assisted programming workflows. The application will run entirely on localhost with no external dependencies or cloud services.

## Goals / Non-Goals

**Goals:**
- Build a fully functional task management web application with local data persistence
- Demonstrate clean separation between frontend, API, and database layers
- Provide intuitive user interface for creating, viewing, updating, and deleting tasks
- Ensure data survives application restarts through SQLite persistence
- Generate all code through AI assistant interaction per academic requirements
- Support task filtering, sorting, and status management
- Create maintainable, well-structured codebase with clear documentation
- Implement user authentication with JWT tokens and secure password storage
- Provide Docker and Docker Compose configuration for reproducible deployment

**Non-Goals:**
- Cloud deployment or remote database
- Real-time collaboration features
- Mobile native applications
- Integration with external services or APIs
- Advanced task features like attachments, comments, or history tracking
- Complex role-based access control (admin/user roles)
- OAuth or third-party authentication providers

## Decisions

**Decision 1: Backend Framework - Python FastAPI**
- **Choice**: FastAPI over Flask, Django, or Node.js Express
- **Rationale**: Modern async framework with automatic API documentation, type hints, and excellent performance. Simpler than Django, more features than Flask, and aligns with Python's popularity in academic settings. Auto-generated OpenAPI docs aid debugging and testing.
- **Alternatives considered**: Flask (simpler but lacks built-in validation), Django (overkill for this scope), Express (requires JavaScript ecosystem knowledge)

**Decision 2: Database - SQLite with SQLAlchemy ORM**
- **Choice**: SQLite database with SQLAlchemy ORM
- **Rationale**: Zero-configuration, file-based database perfect for local development. SQLAlchemy provides database abstraction, migration support, and Pythonic query syntax. Single-file deployment simplifies distribution and backup.
- **Alternatives considered**: Raw SQL queries (more error-prone), PostgreSQL/MySQL (require server setup), NoSQL (unnecessary complexity for structured task data)

**Decision 3: Frontend - Vanilla HTML/CSS/JavaScript**
- **Choice**: Vanilla web technologies without frameworks
- **Rationale**: No build step required, immediate browser compatibility, simpler debugging, and easier to understand for academic evaluation. Fetch API for AJAX calls to backend. Keeps focus on core functionality rather than framework complexity.
- **Alternatives considered**: React/Vue (require build tools and add complexity), server-rendered templates (less interactive, harder to demonstrate API usage)

**Decision 4: Architecture - Layered Monolith**
- **Choice**: Single repository with clear separation: frontend (static files), API (FastAPI routes), database (SQLAlchemy models)
- **Rationale**: Simplifies deployment and development while maintaining clean boundaries. Easy to understand, test, and modify. API-first design allows future frontend changes without backend modifications.
- **Alternatives considered**: Microservices (over-engineering for this scope), monolithic templates (tighter coupling, harder to test)

**Decision 5: Task Data Model**
- **Choice**: Tasks with id, title, description, status, priority, due_date, created_at, updated_at fields
- **Rationale**: Covers essential task management requirements without over-complication. Status as enum (pending/completed), priority as enum (low/medium/high). Timestamps for tracking and sorting.
- **Alternatives considered**: Minimal fields only (insufficient for filtering/sorting), complex fields like tags/categories (scope creep)

**Decision 6: Authentication - JWT with bcrypt password hashing**
- **Choice**: JWT (JSON Web Tokens) for session management with bcrypt password hashing via passlib
- **Rationale**: Stateless authentication suitable for REST APIs. JWT tokens stored in localStorage on frontend, sent as Bearer token in API requests. bcrypt provides secure password hashing with salt. python-jose library handles token creation/verification. Simple to implement, well-documented, and appropriate for academic scope.
- **Alternatives considered**: Session cookies (requires CSRF protection, more complex for SPA), OAuth2 with providers (overkill for local app), plain password storage (security risk), Django auth (too heavy for FastAPI)

**Decision 7: User Model**
- **Choice**: Users table with id, username (unique), email (unique), hashed_password, created_at fields
- **Rationale**: Minimal user model sufficient for authentication. Username for display, email for login identification. Passwords never stored in plain text. Created_at for audit trail.
- **Alternatives considered**: Complex user profiles (scope creep), email-only authentication (less flexible), multiple authentication methods (over-engineering)

**Decision 8: Containerization - Docker with Docker Compose**
- **Choice**: Multi-stage Dockerfile for Python application with Docker Compose orchestration
- **Rationale**: Docker ensures consistent environment across development and deployment. Docker Compose simplifies running application with single command (docker-compose up). Volume mounting preserves SQLite database across container restarts. Multi-stage build reduces final image size.
- **Alternatives considered**: Single container without Compose (less flexible), Kubernetes (overkill for single app), Vagrant (heavier, less portable), manual virtual environment setup (not reproducible)

**Decision 9: Task Ownership**
- **Choice**: Each task belongs to a user (user_id foreign key); users can only see and manage their own tasks
- **Rationale**: Multi-user support requires task ownership. API queries automatically filter by authenticated user's ID. Prevents unauthorized access to other users' data at the database query level.
- **Alternatives considered**: Shared tasks visible to all users (no privacy), complex permission system (scope creep), no ownership (defeats purpose of authentication)

## Risks / Trade-offs

**[Risk] SQLite concurrency limitations** → Mitigation: Application designed for single-user local use; WAL mode enabled for better concurrent read performance. Document limitations for multi-user scenarios.

**[Risk] Frontend maintainability without framework** → Mitigation: Keep JavaScript modular with clear separation of concerns. Use modern ES6+ features. Document code structure thoroughly. Acceptable trade-off for academic simplicity.

**[Risk] Database schema changes require manual migration** → Mitigation: Use SQLAlchemy migrations (Alembic) from start. Define clear schema versioning. For academic scope, schema changes are minimal and can be handled with simple drop/recreate during development.

**[Risk] Browser compatibility issues with vanilla JS** → Mitigation: Target modern browsers (Chrome, Firefox, Edge). Use established APIs (Fetch, localStorage for UI state). Provide clear browser requirements in documentation.

**[Risk] JWT token theft via XSS** → Mitigation: Tokens stored in localStorage (acceptable for academic project). For production, httpOnly cookies recommended. Set short token expiration (30 minutes). Document this limitation.

**[Risk] Docker image size** → Mitigation: Use multi-stage build to separate build and runtime stages. Use slim Python base image. Exclude development dependencies from production image.

**[Trade-off] Vanilla frontend less interactive than framework-based** → Acceptable trade-off for simplicity and educational value. Core CRUD operations fully functional. Future enhancement could add React/Vue if needed.

**[Trade-off] JWT in localStorage instead of httpOnly cookie** → Less secure against XSS but simpler to implement with vanilla JS. Acceptable for academic scope. Documented as known limitation.

**[Trade-off] Single-user per container** → Each Docker instance serves one user context. No shared data between users. Acceptable for academic demonstration.
