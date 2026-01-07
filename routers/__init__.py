from fastapi import FastAPI

from routers import sample_api


def apply_routers(app: FastAPI):
    app.include_router(sample_api.router, prefix="/api/v1/sample")

    return app
