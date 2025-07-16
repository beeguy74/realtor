# Reeltor

A Python application that includes RabbitMQ messaging and PostgreSQL database integration.

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
- Docker and Docker Compose (for running services)

## Installation

### 1. Install uv

If you don't have `uv` installed, you can install it using one of the following methods:

```bash
# Using pip
pip install uv

# Using pipx (recommended)
pipx install uv

# Using curl (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Dependencies

Navigate to the project directory and install the dependencies:

```bash
# Install production dependencies
uv sync

# Install with development dependencies
uv sync --group dev
```

This will create a virtual environment and install all dependencies specified in `pyproject.toml`.

## Environment Setup

Create a `.env` file in the project root with the following variables:

```env
# RabbitMQ Configuration
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=password

# Database Configuration
DB_NAME=reeltor_db
DB_USER=reeltor_user
DB_PASSWORD=your_secure_password
```

## Running the Project

### 1. Start Infrastructure Services

Start the required services (RabbitMQ and PostgreSQL) using Docker Compose:

```bash
docker-compose up -d
```

This will start:
- **RabbitMQ** on port 5672 (AMQP) and 15672 (Management UI)
- **PostgreSQL** on port 5432

You can access the RabbitMQ Management UI at http://localhost:15672 using the credentials from your `.env` file.

### 2. Run the Application

Run the main application:

```bash
# Using uv
uv run python main.py

# Or activate the virtual environment and run directly
uv shell
python main.py
```

## Development

### Running Tests

```bash
# Run tests with pytest
uv run pytest

# Run tests with coverage
uv run pytest --cov
```

### Code Formatting and Linting

```bash
# Format code with black
uv run black .

# Lint code with flake8
uv run flake8 .
```

### Adding Dependencies

To add new dependencies:

```bash
# Add production dependency
uv add package_name

# Add development dependency
uv add --group dev package_name
```

## Project Structure

```
reeltor/
├── main.py                 # Main application entry point
├── pyproject.toml          # Project configuration and dependencies
├── docker-compose.yml      # Docker services configuration
├── modules/                # Application modules
│   ├── puller.py          # Data pulling functionality
│   └── rabbit/            # RabbitMQ related modules
│       ├── exchange.py    # Exchange configuration
│       └── producer.py    # Message producer
└── assets/                # Docker assets
    ├── database/          # PostgreSQL Docker configuration
    └── rabbit/            # RabbitMQ Docker configuration
```

## Stopping Services

To stop the infrastructure services:

```bash
docker-compose down
```

To stop and remove all data:

```bash
docker-compose down -v
```

## Dependencies

### Production Dependencies
- `pika` - RabbitMQ client library
- `python-dotenv` - Environment variable management
- `requests` - HTTP library
- `sqlalchemy` - SQL toolkit and ORM

### Development Dependencies
- `black` - Code formatter
- `flake8` - Code linter
- `pytest` - Testing framework

The application will be available at `http://127.0.0.1:8000`.

## Database Migrations

This project uses Alembic to manage database migrations.

### Creating a new migration

To create a new migration script after changing your models, use the following command:

```bash
poetry run alembic revision --autogenerate -m "description of changes"
```

This will generate a new revision file in `alembic/versions/`.

### Applying migrations

To apply all pending migrations to the database, run:

```bash
poetry run alembic upgrade head
```

### Downgrading migrations

To downgrade by one revision:

```bash
poetry run alembic downgrade -1
```

To downgrade to a specific revision, use the revision hash:

```bash
poetry run alembic downgrade <revision>