from collections.abc import Container
from datetime import date, timedelta

from sqlalchemy.orm import Session

from ..repository.vacation import VacationRepository
from ..schema.employee import EmployeeSchema
from ..schema.vacation import VacationCreateSchema, VacationSchema, VacationUpdateSchema
from .exceptions import (
    BridgingDifferentTypesException,
    NoWorkDaysException,
    VacationAlreadyExistsException,
)


__all__ = (
    "compute_workdays",
    "new_vacation",
    "update_vacation",
)


def compute_workdays(
    start_date: date,
    end_date: date,
    days_off: Container[int] = (5, 6),  # weekend
) -> int:
    """
    Compute days worked between two days.
    Day indexes for `days_off` have the same meaning as `date.weekday`
    """
    return sum(
        day.weekday() not in days_off
        for day in (
            start_date + timedelta(days=i)
            for i in range((end_date - start_date).days + 1)
        )
    )


def new_vacation(
    session: Session,
    vacation_in: VacationCreateSchema | VacationSchema,
    employee: EmployeeSchema,
    *,
    _create: bool = True,
) -> VacationSchema:
    """
    Handle creation of new vacation

    Check if contiguous or overlapping with other vacation

    Computes number of workdays

    This will not join two vacations with a week-end between them
    """
    kwargs = {}
    if not _create:
        kwargs = {"ne": {"id": vacation_in.id}}

    employee_vacation_overlap = VacationRepository.get_many(
        session,
        le={"start_date": vacation_in.end_date + timedelta(days=1)},
        ge={"end_date": vacation_in.start_date - timedelta(days=1)},
        order_by={"start_date": "ASC"},
        employee_id=employee.id,
        **kwargs,
    )

    # Wont iter written as a loop for simplicity
    print(employee_vacation_overlap)
    for overlap in employee_vacation_overlap:
        if (
            overlap.start_date <= vacation_in.start_date
            and overlap.end_date >= vacation_in.end_date
        ):
            raise VacationAlreadyExistsException(
                "Vacation already exists on those dates, if you want to change it update it"
            )

    if (
        len(
            unique_types := set((overlap.type for overlap in employee_vacation_overlap))
        )
        > 1
    ):
        raise BridgingDifferentTypesException(
            "Bridging vacation with following types: "
            f"{', '.join(map(lambda x: x.name, unique_types))}"
        )

    # The filtering in python here should be much less intensive than the one
    # we did to first get the overlaps
    employee_vacation_overlap = [
        overlap
        for overlap in employee_vacation_overlap
        if overlap.type == vacation_in.type
    ]

    if not employee_vacation_overlap:
        # Create new one
        workdays = compute_workdays(vacation_in.start_date, vacation_in.end_date)

        if workdays == 0:
            raise NoWorkDaysException("Trying to create a vacation on not worked days")

        if _create:
            return VacationRepository.create(
                session,
                employee.id,
                workdays,
                vacation_in,
            )

        vacation_in.total_work_days = compute_workdays(
            vacation_in.start_date,
            vacation_in.end_date,
        )
        return VacationRepository.update(session, vacation_in)

    if _create:
        earliest_overlap, *overlaps = employee_vacation_overlap

        earliest_overlap.start_date = min(
            earliest_overlap.start_date, vacation_in.start_date
        )
        earliest_overlap.end_date = max(earliest_overlap.end_date, vacation_in.end_date)
        if overlaps:
            earliest_overlap.end_date = overlaps[-1].end_date
        overlaps_to_delete = overlaps
        to_update = earliest_overlap
    else:
        vacation_in.start_date = min(
            employee_vacation_overlap[0].start_date, vacation_in.start_date
        )
        vacation_in.end_date = max(
            employee_vacation_overlap[-1].end_date, vacation_in.end_date
        )
        to_update = vacation_in
        overlaps_to_delete = employee_vacation_overlap

    for overlap in overlaps_to_delete:
        session.delete(overlap._model)  # pylint:disable=protected-access

    to_update.total_work_days = compute_workdays(
        to_update.start_date,
        to_update.end_date,
    )

    return VacationRepository.update(session, to_update)


def update_vacation(
    session: Session, vacation: VacationSchema, update_data: VacationUpdateSchema
):
    """
    Handle update of vacation
    """
    for key, value in update_data.model_dump().items():
        setattr(vacation, key, value)

    return new_vacation(session, vacation, vacation.employee, _create=False)
