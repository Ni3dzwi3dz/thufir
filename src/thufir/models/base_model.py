from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic.fields import ModelPrivateAttr

from src.thufir.exceptions.models import DatabaseModelNotSet


class ThufirModel(BaseModel):
    """
    Base model for Thufir, providing common functionality for all models.
    """

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    _db_model: Optional[ModelPrivateAttr] = None

    def to_db_model(self) -> BaseModel:
        db_model = type(self)._db_model

        if db_model and db_model.default:
            return db_model.default(**self.model_dump())  # type: ignore
        raise DatabaseModelNotSet(self.__class__.__name__)

    @classmethod
    def from_db_model(cls, db_model: BaseModel) -> "ThufirModel":
        if not cls._db_model:
            raise DatabaseModelNotSet(cls.__name__)
        return cls.model_validate(db_model)

    @classmethod
    def from_request(cls, request_data: dict) -> "ThufirModel":
        """
        Create an instance of the model from request data.
        """
        return cls.model_validate(request_data)

    def to_response(self) -> dict:
        """
        Convert the model instance to a dictionary suitable for response.
        """
        return self.model_dump(exclude_unset=True, by_alias=True)
