from typing import Optional
from pydantic import BaseModel, ConfigDict

from src.thufir.exceptions.models import DatabaseModelNotSet


class ThufirModel(BaseModel):
    """
    Base model for Thufir, providing common functionality for all models.
    """

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    _db_model: Optional[type] = None

    def to_db_model(self) -> BaseModel:
        if type(self)._db_model:
            return type(self)._db_model(**self.model_dump())  # type: ignore
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
