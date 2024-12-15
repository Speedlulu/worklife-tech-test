from datetime import date
from enum import IntEnum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, CustomUUID


if TYPE_CHECKING:
    from .employee import EmployeeModel


__all__ = (
    "VacationModel",
    "VacationType",
)


class VacationType(IntEnum):
    """
    Vacation type enum
    """

    PAID = 0
    UNPAID = 1


class VacationModel(BaseModel):
    """
    Vacation model
    """

    __tablename__ = "vacation"

    start_date: Mapped[date]
    end_date: Mapped[date]
    total_work_days: Mapped[int]
    type: Mapped[VacationType]

    employee_id: Mapped[CustomUUID(as_uuid=True)] = mapped_column(
        ForeignKey("employee.id", name="vacation_employee_id_fk"),
        nullable=False,
    )

    employee: Mapped["EmployeeModel"] = relationship()
