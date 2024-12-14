from pydantic import BaseModel as PyBaseModel, ConfigDict, UUID4


__all__ = ("BaseSchema",)


class BaseSchema(PyBaseModel):
    """
    Base for all pydantic schemas
    """

    model_config = ConfigDict(from_attributes=True)
    id: UUID4
