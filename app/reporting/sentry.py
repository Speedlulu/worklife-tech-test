from contextlib import asynccontextmanager

import sentry_sdk

from ..core.config import settings


@asynccontextmanager
async def init_sentry(_):
    """
    Init sentry sdk
    """
    if settings.ENABLE_SENTRY:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
    yield
