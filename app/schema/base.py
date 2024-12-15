from collections.abc import Iterator
from typing import Any, Generic, TypeVar

from pydantic import (
    BaseModel as PyBaseModel,
    ConfigDict,
    RootModel,
    UUID4,
    ValidationError,
)

from ..model import BaseModel


__all__ = ("BaseSchema",)


Model = TypeVar("Model", bound=BaseModel)


class BaseSchema(PyBaseModel, Generic[Model]):
    """
    Base for all pydantic schemas
    """

    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    _model: Model | None = None


def validate_selected_fields_from_model(
    model: BaseModel,
    data_dict: dict,
) -> Iterator[ValidationError]:
    """
    Validates fields one by one, yielding any ValidationErrors encountered.
    This allows immediate error handling as soon as any validation fails.

    Args:
        model: The Pydantic model to validate against
        data_dict: Dictionary containing data to validate

    Yields:
        ValidationError: Any validation errors encountered during the process

    https://github.com/pydantic/pydantic/discussions/7367#discussioncomment-11023079
    """
    excs = []
    for k, v in data_dict.items():
        try:
            model.__pydantic_validator__.validate_assignment(
                model.model_construct(),
                k,
                v,
            )
        except ValidationError as exc:
            excs.append(exc)

    if excs:
        raise ExceptionGroup("Validation errors", excs)


ArbitraryJsonDict = RootModel[dict[str, Any]]
