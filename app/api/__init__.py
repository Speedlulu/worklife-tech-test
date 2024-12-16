import time
from datetime import datetime, timezone

from fastapi import FastAPI, Request

from ..timeseries.mongo import get_mongo_collection
from .routes import employee, health, team, vacation


__all__ = (
    "add_app_routes",
    "stats_middleware",
)


def add_app_routes(app: FastAPI):
    """
    Add all routers
    """
    app.include_router(health.router)
    app.include_router(employee.router)
    app.include_router(team.router)
    app.include_router(vacation.router)


async def stats_middleware(request: Request, call_next):
    """
    Middleware to push time series info
    """

    start_time = time.perf_counter()
    response = await call_next(request)

    get_mongo_collection().insert_one(
        {
            "status_code": response.status_code,
            "response_time": time.perf_counter() - start_time,
            "timestamp": datetime.now(tz=timezone.utc),
        },
    )

    return response
