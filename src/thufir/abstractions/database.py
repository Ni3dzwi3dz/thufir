from abc import abstractmethod, ABC
from typing import List, Type
from sqlalchemy import Engine

from src.thufir.models.rss import Base


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
    def put_one(self, model: Type[Base], item: Base) -> None:
        """
        Insert a single item into the database.
        """
        pass

    # Should put_many iterate through list and call put_one for each item?
    # This would mean, putting list is not atomic.
    # If you want atomicity, you might need to use a single transaction.

    @abstractmethod
    def put_many(self, items: List[Base]) -> None:
        """
        Insert multiple items into the database.
        Should be atomic, meaning all items are inserted or none.
        """
        pass

    @abstractmethod
    def get_all(self, model: Type[Base]) -> List[Base]:
        """
        Retrieve all items of a specific model from the database.
        """
        pass

    @abstractmethod
    def get_by_id(self, model: Type[Base], item_id: int) -> Base:
        """
        Retrieve a single item from the database.
        """
        pass

    @abstractmethod
    def get_filtered(self, model: Type[Base], **filters) -> List[Base]:
        """
        Retrieve filtered items of a specific model from the database.
        """
        pass

    @abstractmethod
    def update_one(self, item: Base) -> None:
        """
        Update a single item in the database.
        """
        pass

    @abstractmethod
    def update_many(self, items: List[Base]) -> None:
        """
        Update multiple items in the database.
        Should be atomic, meaning all items are updated or none.
        """
        pass

    @abstractmethod
    def delete_one(self, model: Type[Base], item_id: int) -> None:
        """
        Delete a single item from the database.
        """
        pass

    @abstractmethod
    def delete_many(self, model: Type[Base], items: List[int]) -> None:
        """
        Delete multiple items from the database.
        Should be atomic, meaning all items are deleted or none.
        """
        pass
