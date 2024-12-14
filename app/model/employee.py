import sqlalchemy as sa

from .base import BaseModel


__all__ = ("EmployeeModel",)


class EmployeeModel(BaseModel):
    """
    Employee model
    """

    __tablename__ = "employee"
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
