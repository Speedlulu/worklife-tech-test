from fastapi import FastAPI

from .routes import health, employee


def add_app_routes(app: FastAPI):
    app.include_router(health.router)
    app.include_router(employee.router)
