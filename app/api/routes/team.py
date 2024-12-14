from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...repository.team import TeamRepository
from ...schema.team import TeamSchema, TeamCreateSchema


router = APIRouter(prefix="/team", tags=["Team"])


@router.get("/{team_id}")
def get_team(
    session: Session = Depends(get_db),
    *,
    team_id: UUID,
) -> TeamSchema:
    """
    Get team by ID
    """
    if (
        team := TeamRepository.get_by_id(
            session,
            team_id=team_id,
        )
    ) is None:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    return team


@router.post("", status_code=HTTPStatus.CREATED)
def create_team(
    team: TeamCreateSchema,
    session: Session = Depends(get_db),
) -> TeamSchema:
    """
    Create a team
    """
    return TeamRepository.create(session, team)