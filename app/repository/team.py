from uuid import UUID

from ..model.team import TeamModel
from ..repository.base import BaseRepository
from ..schema.team import TeamSchema, TeamCreateSchema, TeamUpdateSchema


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

    def create(
        self,
        session,
        schema_in: TeamCreateSchema,
        **kwargs,
    ):
        return super().create(session, schema_in, **kwargs)


TeamRepository = _TeamRepository(
    model=TeamModel,
    schema=TeamSchema,
    update_schema=TeamUpdateSchema,
)
