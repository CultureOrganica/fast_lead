# Fast Lead Backend

FastAPI backend для омниканального appointment-setter.

## Quick Start

### Setup

```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements-dev.txt

# Copy .env.example and configure
cp ../.env.example ../.env
# Edit .env with your settings
```

### Database Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### Run Development Server

```bash
# Start server
uvicorn app.main:app --reload --port 8000

# Server will be available at:
# - http://localhost:8000
# - API docs: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### Run Tests

```bash
pytest

# With coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_health.py -v
```

### Code Quality

```bash
# Format code
black app tests

# Lint
ruff check app tests

# Type check
mypy app
```

## Project Structure

```
backend/
├── alembic/              # Database migrations
│   ├── versions/         # Migration files
│   └── env.py           # Alembic configuration
├── app/
│   ├── api/             # API endpoints
│   │   └── health.py    # Health check endpoint
│   ├── core/            # Core application modules
│   │   ├── config.py    # Configuration
│   │   └── database.py  # Database setup
│   ├── models/          # SQLAlchemy models
│   │   ├── tenant.py    # Tenant model
│   │   ├── user.py      # User model
│   │   └── lead.py      # Lead model
│   ├── schemas/         # Pydantic schemas (TBD)
│   ├── services/        # Business logic (TBD)
│   ├── channels/        # Channel integrations (TBD)
│   └── main.py          # FastAPI application
├── tests/               # Tests
├── alembic.ini          # Alembic config
├── requirements.txt     # Production dependencies
└── requirements-dev.txt # Development dependencies
```

## API Endpoints

### Health Check

- `GET /health` - Full health check (database + Redis)
- `GET /health/live` - Liveness probe
- `GET /health/ready` - Readiness probe

### Coming Soon

- `POST /api/v1/leads` - Create lead
- `GET /api/v1/leads` - List leads
- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login

## Environment Variables

Required variables (see `.env.example`):

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/fast_lead_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Feature Flags
FEATURE_SMS_ENABLED=true
FEATURE_EMAIL_ENABLED=true
FEATURE_VK_ENABLED=true
```

## Development

### Adding New Endpoint

1. Create router in `app/api/`
2. Add models in `app/models/`
3. Add schemas in `app/schemas/`
4. Add business logic in `app/services/`
5. Include router in `app/main.py`

### Creating Database Migration

```bash
# After changing models
alembic revision --autogenerate -m "Add new field to Lead"

# Review generated migration in alembic/versions/
# Apply migration
alembic upgrade head
```

### Adding New Channel Integration

1. Create module in `app/channels/`
2. Implement channel interface
3. Add configuration in `.env`
4. Add feature flag in `app/core/config.py`
5. Add tests

## Deployment

See [docs/deployment.md](../docs/deployment.md) for production deployment instructions.

## Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# Start PostgreSQL
brew services start postgresql@14

# Test connection
psql -U postgres -d fast_lead_dev -c "SELECT 1"
```

### Redis Connection Error

```bash
# Check Redis is running
brew services list | grep redis

# Start Redis
brew services start redis

# Test connection
redis-cli ping
```

### Migration Error

```bash
# Drop database and recreate
dropdb fast_lead_dev
createdb fast_lead_dev

# Reapply migrations
alembic upgrade head
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
