from sqlalchemy.orm import Session

from ..repository.employee import EmployeeRepository
from ..schema.employee import EmployeeSchema, EmployeeUpdateSchema


__all__ = ("update_employee",)


def update_employee(
    session: Session,
    employee: EmployeeSchema,
    update_data: EmployeeUpdateSchema,
) -> EmployeeSchema:
    """
    Update employee schema then db
    """
    for key, value in update_data.model_dump().items():
        setattr(employee, key, value)

    return EmployeeRepository.update(session, employee)
