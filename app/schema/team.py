from pydantic import BaseModel

from .base import BaseSchema, UpdateSchema
from .employee import EmployeeSchema
from ..model.team import TeamModel


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
