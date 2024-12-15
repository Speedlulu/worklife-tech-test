from abc import ABC, abstractmethod
from typing import Any, Generic, Literal, TypeAlias, TypeVar

from sqlalchemy import asc, desc
from sqlalchemy.orm import Query, Session

from ..model.base import BaseModel
from ..schema.base import BaseSchema


__all__ = ("BaseRepository",)


Schema = TypeVar("Schema", bound=BaseSchema)
Model = TypeVar("Model", bound=BaseModel)


FilterDef: TypeAlias = dict[str, Any]
OrderByOrdDef: TypeAlias = Literal["ASC", "DESC"]
OrderByDef: TypeAlias = dict[str, OrderByOrdDef]


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
        insert_schema: BaseSchema | None = None,
    ):
        self.model = model
        self.schema = schema
        self.update_schema = update_schema or schema
        self.insert_schema = insert_schema or schema

    def _create_schema_and_assign_model(self, model: Model) -> Schema:
        schema = self.schema.model_validate(model)
        schema._model = model  # pylint:disable=protected-access
        return schema

    def _setup_filters(  # pylint:disable=too-many-arguments,too-many-positional-arguments
        self,
        query: Query,
        gt: FilterDef | None = None,
        ge: FilterDef | None = None,
        lt: FilterDef | None = None,
        le: FilterDef | None = None,
        ne: FilterDef | None = None,
        eq: FilterDef | None = None,
    ) -> Query:
        if gt is not None:
            query = query.filter(*[getattr(self.model, k) > v for k, v in gt.items()])
        if ge is not None:
            query = query.filter(*[getattr(self.model, k) >= v for k, v in ge.items()])
        if lt is not None:
            query = query.filter(*[getattr(self.model, k) < v for k, v in lt.items()])
        if le is not None:
            query = query.filter(*[getattr(self.model, k) <= v for k, v in le.items()])
        if ne is not None:
            query = query.filter(*[getattr(self.model, k) != v for k, v in ne.items()])
        if eq is not None:
            query = query.filter(*[getattr(self.model, k) == v for k, v in eq.items()])
        return query

    def _setup_order_by(self, query: Query, **kwargs: OrderByOrdDef) -> Query:
        mapping = {"ASC": asc, "DESC": desc}
        for key, value in kwargs.items():
            query = query.order_by(mapping[value](getattr(self.model, key)))
        return query

    def _query(  # pylint:disable=too-many-arguments
        self,
        session: Session,
        *_,
        gt: FilterDef | None = None,
        ge: FilterDef | None = None,
        lt: FilterDef | None = None,
        le: FilterDef | None = None,
        ne: FilterDef | None = None,
        eq: FilterDef | None = None,
        order_by: OrderByDef | None = None,
        **kwargs,
    ) -> Query:
        eq = eq or {}
        eq.update(kwargs)
        query = session.query(self.model)
        query = self._setup_filters(query, gt=gt, ge=ge, lt=lt, le=le, ne=ne, eq=eq)
        query = self._setup_order_by(query, **(order_by or {}))
        return query

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

    @abstractmethod
    def create(
        self,
        session: Session,
        schema_in: Schema,
        **kwargs,
    ):
        """
        Create new object in DB
        """
        insert_schema = self.insert_schema(**schema_in.model_dump(), **kwargs)
        return self._create_or_update(session, insert_schema)

    def update(self, session: Session, schema_in: Schema):
        """
        Update an object in DB
        """
        # Only update updatable fields
        model = schema_in._model  # pylint:disable=protected-access
        for key in self.update_schema.model_fields:
            setattr(model, key, getattr(schema_in, key))

        return self._create_or_update(
            session,
            model_in=model,
        )

    def _create_or_update(
        self,
        session: Session,
        schema_in: Schema | None = None,
        *,
        model_in: Model | None = None,
    ) -> Schema:
        """
        Update or insert object in DB
        Should not directly be called in client code
        """
        model = (
            self.model(**schema_in.model_dump()) if schema_in is not None else model_in
        )
        if model is None:
            raise ValueError("Neither a model nor a schema were provided")
        session.add(model)
        session.commit()
        return self._create_schema_and_assign_model(model)

    def delete(self, session: Session, schema_in: Schema):
        """
        Delete object from db
        """
        session.delete(schema_in._model)  # pylint:disable=protected-access
        session.commit()
