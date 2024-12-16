from uuid import UUID

from ..model import EmployeeModel
from ..repository.base import BaseRepository
from ..schema.employee import EmployeeCreateSchema, EmployeeSchema, EmployeeUpdateSchema


__all__ = ("EmployeeRepository",)


class _EmployeeRepository(BaseRepository[EmployeeSchema, EmployeeModel]):
    """
    Employee repository
    """

    def get_by_id(self, session, employee_id: UUID):
        """
        Get Employee by id
        """
        return self.get(session, id=employee_id)

    def create(
        self,
        session,
        schema_in: EmployeeCreateSchema,
        **kwargs,
    ):
        return super().create(session, schema_in, **kwargs)


EmployeeRepository = _EmployeeRepository(
    model=EmployeeModel,
    schema=EmployeeSchema,
    update_schema=EmployeeUpdateSchema,
)
