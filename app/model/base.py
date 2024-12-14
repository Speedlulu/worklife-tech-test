import uuid as uid

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import as_declarative


__all__ = (
    "BaseModel",
    "CustomUUID",
)


class CustomUUID(postgresql.UUID):
    """
    Postgres compatible UUID
    """

    python_type = uid.UUID


@as_declarative()
class BaseModel:
    """
    Base for all SQLAlchemy models
    """

    id = Column(
        CustomUUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uid.uuid4,
    )
