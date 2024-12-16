from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship

from .base import BaseModel, CustomUUID


if TYPE_CHECKING:
    from .team import TeamModel


__all__ = ("EmployeeModel",)


class EmployeeModel(BaseModel):
    """
    Employee model
    """

    __tablename__ = "employee"
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)

    team_id = sa.Column(
        CustomUUID(as_uuid=True),
        ForeignKey("team.id", name="employee_team_id_fk"),
        nullable=False,
    )

    team: Mapped["TeamModel"] = relationship(back_populates="employees")
