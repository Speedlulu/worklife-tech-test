from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import BaseModel


if TYPE_CHECKING:
    from .employee import EmployeeModel


__all__ = ("TeamModel",)


class TeamModel(BaseModel):
    """
    Team model
    """

    __tablename__ = "team"

    name: Mapped[str]
    employees: Mapped[list["EmployeeModel"]] = relationship(
        back_populates="team",
    )
