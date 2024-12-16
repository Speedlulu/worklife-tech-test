from fastapi import FastAPI

from app.api import add_app_routes, stats_middleware
from app.core.config import settings
from app.timeseries.mongo import mongo_lifespan


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=mongo_lifespan,
)

add_app_routes(app)
app.middleware("http")(stats_middleware)
