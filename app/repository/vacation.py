from datetime import date
from uuid import UUID

from sqlalchemy import or_

from ..model.employee import EmployeeModel
from ..model.vacation import VacationModel, VacationType
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

    def get_by_query_params(  # pylint:disable=too-many-arguments
        self,
        session,
        start_date: date | None = None,
        end_date: date | None = None,
        type_: VacationType | None = None,
        team_id: UUID | None = None,
    ) -> list[VacationSchema]:
        """
        Get vacation by different query params
        """
        query = self._query(session)
        if start_date is not None:
            query = query.filter(
                self.model.start_date >= start_date,
            ).filter(or_(self.model.end_date >= start_date))
        if end_date is not None:
            query = query.filter(
                self.model.start_date <= end_date,
            ).filter(or_(self.model.end_date <= end_date))
        if type_ is not None:
            query = query.filter(self.model.type == type_)
        if team_id is not None:
            query = query.join(EmployeeModel).filter(EmployeeModel.team_id == team_id)

        return [self._create_schema_and_assign_model(model) for model in query.all()]

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
