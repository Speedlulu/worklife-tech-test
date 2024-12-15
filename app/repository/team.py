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

    def create_or_update(
        self,
        session,
        schema_in: TeamCreateSchema | None = None,
        **kwargs,
    ):
        return super().create_or_update(session, schema_in, **kwargs)


TeamRepository = _TeamRepository(
    model=TeamModel,
    schema=TeamSchema,
    update_schema=TeamCreateSchema,
)
