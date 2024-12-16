from pydantic import BaseModel

from ..model.team import TeamModel
from .base import BaseSchema, UpdateSchema
from .employee import EmployeeSchema


__all__ = (
    "TeamSchema",
    "TeamCreateSchema",
    "TeamUpdateSchema",
)


class _TeamBaseSchema:
    name: str


class TeamSchema(BaseSchema[TeamModel], _TeamBaseSchema):
    """
    Team schema
    """

    employees: list[EmployeeSchema]


class TeamCreateSchema(BaseModel, _TeamBaseSchema):
    """
    Employee creation schema
    """


class TeamUpdateSchema(_TeamBaseSchema, UpdateSchema):
    """
    Team update schema
    """
