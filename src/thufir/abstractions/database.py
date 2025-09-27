from abc import abstractmethod, ABC
from typing import List, Type, TypeVar
from sqlalchemy import Engine
from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)


class Database(ABC):
    """
    Abstract base class for database operations.
    """

    @abstractmethod
    def _create_engine(self, connection_string: str, echo: bool) -> Engine:
        """
        Create a SQLAlchemy engine with the provided connection string.
        """
        pass

    @abstractmethod
    # Should this be a None?
    def put_one(self, model: Type[T], item: T) -> None:
        """
        Insert a single item into the database.
        """
        pass

    @abstractmethod
    def put_many(self, items: List[T]) -> None:
        """
        Insert multiple items into the database.
        Should be atomic, meaning all items are inserted or none.
        """
        pass

    @abstractmethod
    def get_all(self, model: Type[T]) -> List[T]:
        """
        Retrieve all items of a specific model from the database.
        """
        pass

    @abstractmethod
    def get_by_id(self, model: Type[T], item_id: int) -> T | None:
        """
        Retrieve a single item from the database.
        """
        pass

    @abstractmethod
    def get_filtered(self, model: Type[T], *filters) -> List[T]:
        """
        Retrieve filtered items of a specific model from the database.
        """
        pass

    @abstractmethod
    def update_one(self, item: T) -> None:
        """
        Update a single item in the database.
        """
        pass

    @abstractmethod
    def update_many(self, items: List[T]) -> None:
        """
        Update multiple items in the database.
        Should be atomic, meaning all items are updated or none.
        """
        pass

    @abstractmethod
    def delete_one(self, model: Type[T], item_id: int) -> None:
        """
        Delete a single item from the database.
        """
        pass

    @abstractmethod
    def delete_many(self, model: Type[T], items: List[int]) -> None:
        """
        Delete multiple items from the database.
        Should be atomic, meaning all items are deleted or none.
        """
        pass
