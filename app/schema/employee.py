from pydantic import BaseModel, UUID4

from .base import BaseSchema
from ..model.employee import EmployeeModel


__all__ = (
    "EmployeeSchema",
    "EmployeeCreateSchema",
    "EmployeeUpdateSchema",
)


class _EmployeeBaseSchema:
    first_name: str
    last_name: str
    team_id: UUID4


class EmployeeSchema(BaseSchema[EmployeeModel], _EmployeeBaseSchema):
    """
    Employee schema
    """


class EmployeeCreateSchema(BaseModel, _EmployeeBaseSchema):
    """
    Employee creation schema
    """


class EmployeeUpdateSchema(BaseModel):
    """
    Employee update schema
    """

    first_name: str = None
    last_name: str = None
    team_id: UUID4 = None
