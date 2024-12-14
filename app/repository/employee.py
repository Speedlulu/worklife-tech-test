from uuid import UUID

from ..model import EmployeeModel
from ..repository.base import BaseRepository
from ..schema.employee import EmployeeSchema, EmployeeCreateSchema


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

    def create(self, session, obj_in: EmployeeCreateSchema):
        return super().create(session, self.model(**obj_in.model_dump()))


EmployeeRepository = _EmployeeRepository(
    model=EmployeeModel,
    schema=EmployeeSchema,
)
