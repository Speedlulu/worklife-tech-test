from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...domain.employee import update_employee as domain_update_employee
from ...domain.exceptions import DomainException
from ...domain.vacation import new_vacation, update_vacation
from ...repository.employee import EmployeeRepository
from ...repository.vacation import VacationRepository
from ...schema.employee import (
    EmployeeSchema,
    EmployeeCreateSchema,
    EmployeeUpdateSchema,
)
from ...schema.vacation import (
    VacationSchema,
    VacationCreateSchema,
    VacationUpdateSchema,
)


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
    return EmployeeRepository.create(session, employee)


@router.patch("/{employee_id}")
def update_employee(
    update_data: EmployeeUpdateSchema,
    session: Session = Depends(get_db),
    *,
    employee_id: UUID,
) -> EmployeeSchema:
    """
    Update employee
    """
    employee = get_employee(session, employee_id=employee_id)
    return domain_update_employee(session, employee, update_data)


@router.post("/{employee_id}/vacation", status_code=HTTPStatus.CREATED)
def create_employee_vacation(
    vacation: VacationCreateSchema,
    session: Session = Depends(get_db),
    *,
    employee_id: UUID,
) -> VacationSchema:
    """
    Create a vacation for employee
    """
    employee = get_employee(session, employee_id=employee_id)
    try:
        return new_vacation(session, vacation, employee)
    except DomainException as exc:
        raise HTTPException(HTTPStatus.BAD_REQUEST, str(exc)) from exc


@router.get("/{employee_id}/vacation")
def get_employee_vacations(
    session: Session = Depends(get_db),
    *,
    employee_id: UUID,
) -> list[VacationSchema]:
    """
    Get all vacations for employee
    """
    employee = get_employee(session, employee_id=employee_id)
    return VacationRepository.get_by_employee_id(session, employee.id)


@router.get("/{employee_id}/vacation/{vacation_id}")
def get_employee_vacation(
    session: Session = Depends(get_db),
    *,
    employee_id: UUID,
    vacation_id: UUID,
) -> VacationSchema:
    """
    Create a vacation for employee
    """
    employee = get_employee(session, employee_id=employee_id)
    if (
        vacation := VacationRepository.get_by_employee_id_employee_id(
            session, vacation_id, employee.id
        )
    ) is None:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    return vacation


@router.patch("/{employee_id}/vacation/{vacation_id}")
def update_employee_vacation(
    update_data: VacationUpdateSchema,
    session: Session = Depends(get_db),
    *,
    employee_id: UUID,
    vacation_id: UUID,
) -> VacationSchema:
    """
    Update a vacation for employee
    """
    vacation = get_employee_vacation(
        session, employee_id=employee_id, vacation_id=vacation_id
    )

    try:
        return update_vacation(session, vacation, update_data)
    except DomainException as exc:
        raise HTTPException(HTTPStatus.BAD_REQUEST, str(exc)) from exc


@router.delete("/{employee_id}/vacation/{vacation_id}")
def delete_employee_vacation(
    session: Session = Depends(get_db),
    *,
    employee_id: UUID,
    vacation_id: UUID,
) -> VacationSchema:
    """
    Delete a vacation for employee
    """
    vacation = get_employee_vacation(
        session, employee_id=employee_id, vacation_id=vacation_id
    )

    VacationRepository.delete(session, vacation)

    return vacation
