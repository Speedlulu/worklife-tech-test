from typing import Generic, TypeVar

from pydantic import BaseModel as PyBaseModel, ConfigDict, UUID4

from ..model import BaseModel


__all__ = ("BaseSchema",)


Model = TypeVar("Model", bound=BaseModel)


class BaseSchema(PyBaseModel, Generic[Model]):
    """
    Base for all pydantic schemas
    """

    model_config = ConfigDict(from_attributes=True, validate_assignment=True)
    id: UUID4
    _model: Model | None = None


class UpdateSchema(PyBaseModel):
    """
    Update schemas
    """

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        extra="forbid",
    )

    def model_dump(self, *, exclude_unset: bool = True, **kwargs):
        return super().model_dump(exclude_unset=exclude_unset, **kwargs)
