from pydantic import BaseModel, UUID4

from .base import BaseSchema


__all__ = (
    "EmployeeSchema",
    "EmployeeCreateSchema",
)


class _EmployeeBaseSchema:
    first_name: str
    last_name: str
    team_id: UUID4


class EmployeeSchema(BaseSchema, _EmployeeBaseSchema):
    """
    Employee schema
    """


class EmployeeCreateSchema(BaseModel, _EmployeeBaseSchema):
    """
    Employee creation schema
    """
