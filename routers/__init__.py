from fastapi import FastAPI

from routers import sample_api, picks_api


def apply_routers(app: FastAPI):
    app.include_router(sample_api.router, prefix="/api/v1/sample")
    app.include_router(picks_api.router, prefix="/api/v1/picks")

    return app
