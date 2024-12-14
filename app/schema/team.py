from pydantic import BaseModel

from .base import BaseSchema


__all__ = (
    "TeamSchema",
    "TeamCreateSchema",
)


class _TeamBaseSchema:
    name: str


class TeamSchema(BaseSchema, _TeamBaseSchema):
    """
    Team schema
    """


class TeamCreateSchema(BaseModel, _TeamBaseSchema):
    """
    Employee creation schema
    """
