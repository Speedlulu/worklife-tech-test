from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.orm import Query, Session

from ..model.base import BaseModel
from ..schema.base import BaseSchema


__all__ = ("BaseRepository",)


Schema = TypeVar("Schema", bound=BaseSchema)


class BaseRepository(Generic[Schema], ABC):
    """
    Generic base class for all repositories
    To get full typing functionnaly define inheriting class like so
    class ConcreteRepository(BaseRepository[Schema, Model])
    """

    def __init__(self, model: Model, schema: Schema):
        self.model = model
        self.schema = schema

    def _query(self, session: Session, *_, **kwargs) -> Query:
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        return session.query(self.model).filter(*filters)

    def get(self, session: Session, *_, **kwargs) -> Schema | None:
        """
        Return a single object or None if not found
        """
        model = self._query(session, **kwargs).one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model)

    def get_many(self, session, *_, **kwargs) -> list[Schema]:
        """
        Returns a list of objects
        """
        return [
            self.schema.model_validate(model)
            for model in self._query(session, **kwargs).all()
        ]

