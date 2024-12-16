from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI

from app.api import add_app_routes, stats_middleware
from app.core.config import settings
from app.reporting.sentry import init_sentry
from app.timeseries.mongo import mongo_lifespan


__all__ = ("app",)


@asynccontextmanager
async def _lifespan(_: FastAPI):
    resource_managers = (
        mongo_lifespan,
        init_sentry,
    )

    async with AsyncExitStack() as stack:
        for manager in resource_managers:
            await stack.enter_async_context(manager(_))
        yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=_lifespan,
)

add_app_routes(app)
app.middleware("http")(stats_middleware)
