from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...repository.employee import EmployeeRepository
from ...schema.employee import EmployeeSchema


router = APIRouter(prefix="/employee", tags=["Employee"])


@router.get("/{employee_id}")
def get_employee(
    session: Session = Depends(get_db),
    *,
    employee_id: UUID,
) -> EmployeeSchema:
    """
    Get employee by ID
    """
    if (
        employee := EmployeeRepository.get_by_id(
            session,
            employee_id=employee_id,
        )
    ) is None:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    return employee

