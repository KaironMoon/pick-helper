# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run development server
uv run python main.py

# Run tests (requires running server on localhost:8000)
uv run pytest

# Run tests with coverage
uv run pytest --cov=. --cov-report=html
```

## Architecture

This is a FastAPI backend skeleton built on the `ai-microservice` framework (internal GitLab dependency). The project uses Python 3.13+ with `uv` as the package manager.

### Application Initialization (main.py)
- `create_app()` factory pattern creates the FastAPI instance
- `apply_routers()` registers all API routers
- `apply_frontend()` serves static files from `frontend/`
- `apply_middleware()` adds framework middleware (CORS, logging, error handling)
- `WebApp` from ai-microservice handles the uvicorn server

### Configuration System (common/settings.py)
Settings follow a layered YAML approach with three config sources:
- `yaml/configmap.yaml` - general configuration
- `yaml/configmap-domain.yaml` - domain/URL settings
- `yaml/secret.yaml` - secrets (base64 encoded values auto-decoded)

`ProjectSettings` extends `WebAppSettings` from ai-microservice. Settings are cached via `@lru_cache()` in `config.py`.

### Layer Structure
- **routers/**: API endpoints - register new routers in `routers/__init__.py` via `apply_routers()`
- **dao/**: Data access layer (empty placeholder)
- **worker/**: Background workers/schedulers
- **common_types/**: Shared type definitions
- **common/**: Utilities and settings

### Adding New Endpoints
1. Create router file in `routers/` with `APIRouter()`
2. Register in `routers/__init__.py`: `app.include_router(my_router.router, prefix="/api/v1/myroute")`
