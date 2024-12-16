from contextlib import asynccontextmanager
from functools import lru_cache
from unittest.mock import MagicMock

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from ..core.config import settings


__all__ = (
    "get_mongo_collection",
    "mongo_lifespan",
)


@lru_cache
def get_mongo() -> AsyncIOMotorClient:
    """
    Instanciate and cache mongo client
    """
    if not settings.ENABLE_STATS:
        return MagicMock()

    return AsyncIOMotorClient(settings.MONGODB_DSN.unicode_string())


@lru_cache
def get_mongo_collection() -> AsyncIOMotorCollection:
    """
    Get mongo collection
    """
    return (
        get_mongo()
        .get_database(
            settings.MONGODB_DATABASE,
        )
        .get_collection(settings.MONGODB_COLLECTION)
    )


@asynccontextmanager
async def mongo_lifespan(_):
    """
    Create and close mongo client with app
    """
    mongo = get_mongo()
    get_mongo_collection()  # Fail early
    yield
    mongo.close()
