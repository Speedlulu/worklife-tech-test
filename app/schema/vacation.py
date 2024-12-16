from datetime import date
from typing import Annotated

from pydantic import UUID4, BaseModel, Field, ValidationInfo, field_validator

from ..model.vacation import VacationModel, VacationType
from .base import BaseSchema, UpdateSchema
from .employee import EmployeeSchema


__all__ = (
    "VacationSchema",
    "VacationCreateSchema",
    "VacationInsertSchema",
)


class _VacationBaseSchema(BaseModel):
    start_date: date
    end_date: date
    type: VacationType

    @field_validator("start_date", "end_date", mode="after")
    @classmethod
    def _check_dates(cls, v: date, info: ValidationInfo) -> date:
        if info.field_name == "end_date":
            start_date = info.data.get("start_date")
            if start_date is not None and v < start_date:
                raise ValueError("Start date after end date")
            return v

        end_date = info.data.get("end_date")
        if end_date is not None and v > end_date:
            raise ValueError("End date before start date")

        return v


class VacationSchema(BaseSchema[VacationModel], _VacationBaseSchema):
    """
    Vacation schema
    """

    employee: EmployeeSchema
    total_work_days: int


class VacationInsertSchema(_VacationBaseSchema):
    """
    Vacation insert schema
    """

    total_work_days: int
    employee_id: UUID4


class VacationCreateSchema(_VacationBaseSchema):
    """
    Employee creation schema
    """


class VacationUpdateSchema(_VacationBaseSchema, UpdateSchema):
    """
    Vacation update schema
    """

    start_date: date = None
    end_date: date = None
    type: VacationType = None
    total_work_days: Annotated[int, Field(exclude=True)] = None
