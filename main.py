from ai_microservice import WebApp, apply_frontend, apply_middleware
from config import settings
from fastapi import FastAPI
from routers import apply_routers


def create_app():
    app = FastAPI()
    apply_routers(app)
    apply_frontend(app)
    apply_middleware(app, env=settings.env)
    return app

if __name__ == "__main__":
    web_app = WebApp(settings=settings)
    web_app.run("main:create_app")