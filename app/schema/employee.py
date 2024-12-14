from pydantic import BaseModel

from .base import BaseSchema


__all__ = (
    "EmployeeSchema",
)


class _EmployeeBaseSchema:
    first_name: str
    last_name: str


class EmployeeSchema(BaseSchema, _EmployeeBaseSchema):
    """
    Employee schema
    """

