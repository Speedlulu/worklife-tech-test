from pydantic import BaseModel

from .base import BaseSchema
from .employee import EmployeeSchema
from ..model.team import TeamModel


__all__ = (
    "TeamSchema",
    "TeamCreateSchema",
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
