from uuid import UUID

from ..model.team import TeamModel
from ..repository.base import BaseRepository
from ..schema.team import TeamSchema, TeamCreateSchema


__all__ = ("TeamRepository",)


class _TeamRepository(BaseRepository[TeamSchema, TeamModel]):
    """
    Team repository
    """

    def get_by_id(self, session, team_id: UUID):
        """
        Get Team by id
        """
        return self.get(session, id=team_id)

    def create(self, session, obj_in: TeamCreateSchema):
        return super().create(session, self.model(**obj_in.model_dump()))


TeamRepository = _TeamRepository(
    model=TeamModel,
    schema=TeamSchema,
)
