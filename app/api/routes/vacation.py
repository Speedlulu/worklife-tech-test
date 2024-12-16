from datetime import date

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...model.vacation import VacationType
from ...repository.vacation import VacationRepository
from ...schema.vacation import VacationSchema


router = APIRouter(prefix="/vacation", tags=["Employee"])


@router.get("", tags=["Vacation"])
def get_vacations(
    session: Session = Depends(get_db),
    *,
    start_date: date | None = None,
    end_date: date | None = None,
    team_id: UUID4 | None = None,
    type: VacationType | None = None,  # pylint:disable=redefined-builtin
) -> list[VacationSchema]:
    """
    Get vacations from query params
    """
    return VacationRepository.get_by_query_params(
        session,
        start_date=start_date,
        end_date=end_date,
        team_id=team_id,
        type_=type,
    )
