from typing import Any, Optional, Union

from pydantic import MongoDsn, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings
    """

    PROJECT_NAME: str = "technical-test"
    VERSION: str = "0.2.0"
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Union[Optional[PostgresDsn], Optional[str]] = None

    ENABLE_STATS: bool = False
    MONGODB_SERVER: str | None = None
    MONGODB_USER: str | None = None
    MONGODB_PASSWORD: str | None = None
    MONGODB_DATABASE: str | None = None
    MONGODB_COLLECTION: str | None = None
    MONGODB_DSN: MongoDsn | str | None = None

    ENABLE_SENTRY: bool = False
    SENTRY_DSN: str | None = None

    model_config = SettingsConfigDict()

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        """
        Build dsn from settings
        """
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        )

    @field_validator("MONGODB_DSN", mode="before")
    @classmethod
    def assemble_mongo_connection(
        cls,
        v: str | None,
        values: ValidationInfo,
    ) -> str | None | MongoDsn:
        """
        Build dsn from settings
        """
        if isinstance(v, str):
            return v

        if not values.data.get("ENABLE_STATS", False):
            return None

        return PostgresDsn.build(
            scheme="mongodb",
            username=values.data.get("MONGODB_USER"),
            password=values.data.get("MONGODB_PASSWORD"),
            host=values.data.get("MONGODB_SERVER"),
        )

    @field_validator("MONGODB_COLLECTION", "MONGODB_DATABASE", mode="after")
    @classmethod
    def _check_mongodb_collection_data(
        cls,
        v: str | None,
        values: ValidationInfo,
    ) -> str | None | MongoDsn:
        """
        Build dsn from settings
        """
        if isinstance(v, str):
            return v

        if not values.data.get("ENABLE_STATS", False):
            return None

        raise ValueError("Need to specify a value")

    @field_validator("SENTRY_DSN", mode="after")
    @classmethod
    def _check_sentry_dsn(
        cls,
        v: str | None,
        values: ValidationInfo,
    ) -> str | None | MongoDsn:
        """
        Build dsn from settings
        """
        if isinstance(v, str):
            return v

        if not values.data.get("ENABLE_SENTRY", False):
            return None

        raise ValueError("Need to specify a value")


settings = Settings()
