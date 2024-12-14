from fastapi import FastAPI

from .routes import health, employee, team


def add_app_routes(app: FastAPI):
    """
    Add all routers
    """
    app.include_router(health.router)
    app.include_router(employee.router)
    app.include_router(team.router)
