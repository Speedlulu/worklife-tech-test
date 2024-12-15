from sqlalchemy.orm import Session

from ..schema.team import TeamSchema, TeamUpdateSchema
from ..repository.team import TeamRepository


__all__ = ("update_team",)


def update_team(
    session: Session, team: TeamSchema, update_data: TeamUpdateSchema
) -> TeamSchema:
    """
    Update team schema then db
    """
    for key, value in update_data.model_dump().items():
        setattr(team, key, value)
    return TeamRepository.update(session, team)
