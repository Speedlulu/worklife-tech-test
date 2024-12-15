from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from sqlalchemy.orm import Query, Session

from ..model.base import BaseModel
from ..schema.base import BaseSchema, validate_selected_fields_from_model


__all__ = ("BaseRepository",)


Schema = TypeVar("Schema", bound=BaseSchema)
Model = TypeVar("Model", bound=BaseModel)


class BaseRepository(Generic[Schema, Model], ABC):
    """
    Generic base class for all repositories
    To get full typing functionnaly define inheriting class like so
    class ConcreteRepository(BaseRepository[Schema, Model])
    """

    def __init__(
        self,
        model: Model,
        schema: Schema,
        *,
        update_schema: BaseSchema | None = None,
    ):
        self.model = model
        self.schema = schema
        self.update_schema = update_schema or schema

    def _create_schema_and_assign_model(self, model: Model) -> Schema:
        schema = self.schema.model_validate(model)
        schema._model = model  # pylint:disable=protected-access
        return schema

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
        return self._create_schema_and_assign_model(model)

    def get_many(self, session, *_, **kwargs) -> list[Schema]:
        """
        Returns a list of objects
        """
        return [
            self._create_schema_and_assign_model(model)
            for model in self._query(session, **kwargs).all()
        ]

    def update(
        self,
        session: Session,
        model_in: Model,
        update_data: dict[str, Any],
    ) -> Schema:
        """
        Update an object in db
        """
        validate_selected_fields_from_model(self.update_schema, update_data)
        for key, value in update_data.items():
            setattr(model_in, key, value)
        return self.create_or_update(session, model_in=model_in)

    @abstractmethod
    def create_or_update(
        self,
        session: Session,
        schema_in: Schema | None = None,
        *,
        model_in: Model | None = None,
    ) -> Schema:
        """
        Insert a new object in db
        """
        model = (
            self.model(**schema_in.model_dump()) if schema_in is not None else model_in
        )
        if model is None:
            raise ValueError("Neither a model nor a schema were provided")
        session.add(model)
        session.commit()
        return self._create_schema_and_assign_model(model)
