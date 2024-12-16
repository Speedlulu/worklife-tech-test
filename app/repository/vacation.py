from uuid import UUID

from ..model.vacation import VacationModel
from ..repository.base import BaseRepository
from ..schema.vacation import (
    VacationCreateSchema,
    VacationInsertSchema,
    VacationSchema,
    VacationUpdateSchema,
)


__all__ = ("VacationRepository",)


class _VacationRepository(BaseRepository[VacationSchema, VacationModel]):
    """
    Vacation repository
    """

    def get_by_id(self, session, vacation_id: UUID):
        """
        Get Vacation by id
        """
        return self.get(session, id=vacation_id)

    def get_by_employee_id(self, session, employee_id: UUID):
        """
        Get vacations by employee ID
        """
        return self.get_many(session, employee_id=employee_id)

    def get_by_employee_id_employee_id(
        self, session, vacation_id: UUID, employee_id: UUID
    ):
        """
        Get vacations by employee ID and vacation ID
        """
        return self.get(session, id=vacation_id, employee_id=employee_id)

    def create(  # pylint:disable=arguments-differ,arguments-renamed
        self,
        session,
        employee_id: UUID,
        total_work_days: int,
        schema_in: VacationCreateSchema,
    ):
        return super().create(
            session, schema_in, employee_id=employee_id, total_work_days=total_work_days
        )


VacationRepository = _VacationRepository(
    model=VacationModel,
    schema=VacationSchema,
    insert_schema=VacationInsertSchema,
    update_schema=VacationUpdateSchema,
)
