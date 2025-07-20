# Development Standards

## Technology Stack
- Backend: Python with FastAPI framework
- Message Queue: RabbitMQ for async processing
- Database: PostgreSQL with SQLAlchemy ORM
- Containerization: Docker with multi-stage builds
- Testing: pytest for unit/integration tests
- Telegram Bot: pyTelegramBotAPI for bot interactions
- AI Translation: Google GenerativeAI (google-genai) for content translation

## Code Style Guidelines
- Follow PEP 8 for Python code formatting
- Use type hints for all function parameters and return values
- Prefer async/await over synchronous operations where applicable
- Use Pydantic models for request/response validation
- Keep functions focused and under 50 lines when possible

## Architecture Patterns
- Implement repository pattern for data access
- Use dependency injection for service layers
- Follow Clean Architecture principles
- Separate business logic from framework concerns

## Telegram Bot Standards
- Use AsyncTeleBot for asynchronous operations with FastAPI compatibility
- Implement rate limiting to respect Telegram's API limits (30 messages per second per bot)

## API Development
- Use FastAPI's automatic documentation generation
- Implement proper HTTP status codes and error responses
- Include comprehensive request/response models
- Use OAuth2 or JWT for authentication when applicable

## Docker Best Practices
- Use multi-stage builds to minimize image size
- Run containers as non-root users
- Use .dockerignore to exclude unnecessary files
- Pin specific versions for base images

## Testing Requirements
- Maintain minimum 80% code coverage
- Write integration tests for API endpoints
- Use factory patterns for test data creation
- Mock external dependencies in unit tests
