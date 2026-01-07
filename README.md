# Backend Skeleton

A FastAPI-based backend skeleton project built on the `ai-microservice` framework, providing a clean starting point for building microservices.

## Features

- FastAPI web framework with async support
- Modular router architecture
- Built-in middleware and frontend integration
- Environment-based configuration
- Sample API implementation
- Test structure included
- Ready for development and production deployment

## Project Structure

```
backend-skel/
├── main.py                 # Application entry point
├── config.py              # Configuration loader
├── common/                # Shared utilities and settings
│   └── settings.py        # Project settings
├── routers/               # API route handlers
│   ├── __init__.py        # Router registration
│   └── sample_api.py      # Sample API endpoints
├── dao/                   # Data Access Objects
├── common_types/          # Shared type definitions
├── tests/                 # Test suite
│   └── routers/           # Router tests
├── logs/                  # Application logs
├── frontend/              # Frontend static files
├── .env                   # Environment variables (local)
├── .dev.env              # Development environment
└── pyproject.toml        # Project dependencies
```

## Requirements

- Python >= 3.13
- uv (package manager)
- ai-microservice framework

## Installation

1. Clone the repository:
```bash
git clone http://gitlab.deephigh.ai:8929/deephigh/common/skeleton.git
cd backend-skel
```

2. Install dependencies using uv:
```bash
uv sync
```

The project uses the `ai-microservice` framework which will be installed from the internal GitLab repository.

## Configuration

### Environment Variables

Create or modify `.env` file in the project root:

```env
# Environment settings
ENV=development

# Add your configuration variables here
```

Use `.dev.env.base` as a template for development environment variables.

### Settings

The application uses `ProjectSettings` from `common.settings` which is loaded through `config.py`. Settings are cached using `@lru_cache()` for performance.

## Running the Application

### Development Mode

Start the development server:

```bash
uv run python main.py
```

The server will start with hot-reload enabled (development mode).

### Production Mode

For production deployment, ensure the `ENV` variable is set appropriately in your `.env` file.

## Development

### Adding New API Endpoints

1. Create a new router in `routers/`:
```python
# routers/my_api.py
from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["api/v1/myapi"],
    responses={404: {"description": "Not found"}},
)

@router.get("")
async def get_data():
    return {"data": "value"}
```

2. Register the router in `routers/__init__.py`:
```python
from routers import sample_api, my_api

def apply_routers(app: FastAPI):
    app.include_router(sample_api.router, prefix="/api/v1/sample")
    app.include_router(my_api.router, prefix="/api/v1/myapi")
    return app
```

### Project Organization

- **routers/**: API endpoint definitions grouped by functionality
- **dao/**: Database access layer and data operations
- **common_types/**: Shared type definitions and models
- **common/**: Shared utilities, settings, and helpers
- **tests/**: Test files mirroring the project structure

## Testing

Run tests using pytest:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov=. --cov-report=html
```

## API Documentation

Once the application is running, access the interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Sample Endpoints

- `GET /api/v1/sample` - Sample endpoint returning a greeting message

## Architecture

The application follows a layered architecture:

1. **Presentation Layer** (routers/): API endpoints and request/response handling
2. **Business Logic Layer**: Service layer for business operations
3. **Data Access Layer** (dao/): Database operations and data persistence
4. **Common Layer** (common/): Shared utilities and configurations

## Middleware & Frontend

The application uses the `ai-microservice` framework which provides:

- `apply_middleware()`: Standard middleware stack (CORS, logging, error handling)
- `apply_frontend()`: Serves static frontend files from the `frontend/` directory

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Ensure all tests pass
5. Submit a merge request

## License

Internal project - All rights reserved
