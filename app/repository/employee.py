from uuid import UUID

from ..model import EmployeeModel
from ..repository.base import BaseRepository
from ..schema.employee import EmployeeSchema


__all__ = ("EmployeeRepository",)


class _EmployeeRepository(BaseRepository[EmployeeSchema]):
    """
    Employee repository
    """

    def get_by_id(self, session, employee_id: UUID):
        """
        Get Employee by id
        """
        return self.get(session, id=employee_id)


EmployeeRepository = _EmployeeRepository(
    model=EmployeeModel,
    schema=EmployeeSchema,
)
