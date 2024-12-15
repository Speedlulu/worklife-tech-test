from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...repository.employee import EmployeeRepository
from ...schema.base import ArbitraryJsonDict
from ...schema.employee import EmployeeSchema, EmployeeCreateSchema


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


@router.post("", status_code=HTTPStatus.CREATED)
def create_employee(
    employee: EmployeeCreateSchema,
    session: Session = Depends(get_db),
) -> EmployeeSchema:
    """
    Create an employee
    """
    return EmployeeRepository.create_or_update(session, employee)


@router.patch("/{employee_id}")
def update_employee(
    update_data: ArbitraryJsonDict,
    session: Session = Depends(get_db),
    *,
    employee_id: UUID,
) -> EmployeeSchema:
    """
    Update employee
    """
    employee = get_employee(session, employee_id=employee_id)
    try:
        return EmployeeRepository.update(
            session,
            employee._model,  # pylint:disable=protected-access
            update_data.model_dump(),
        )
    except* ValidationError as excg:
        raise RequestValidationError(
            [err for exc in excg.exceptions for err in exc.errors()],
        ) from excg
