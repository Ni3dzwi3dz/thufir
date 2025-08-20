from abc import abstractmethod, ABC
from typing import Optional, TypeVar

from src.thufir.models.base_model import ThufirModel
from src.thufir.models.user import User
from src.thufir.abstractions.database import Database
from src.thufir.models.rss import Article, Feed

T = TypeVar("T", bound=ThufirModel)


class Repository[T](ABC):

    def __init__(self, database: Database):
        self.database = database

    @abstractmethod
    def get_all(self) -> list[T]:
        """
        Retrieve all records from the repository.
        """
        pass

    @abstractmethod
    def get_by_id(self, record_id: int) -> Optional[T]:
        """
        Retrieve a record by its ID.
        """
        pass

    @abstractmethod
    def save(self, record: T) -> int:
        """
        Save a record to the repository.
        Accepts a record of type T and returns its ID.
        """
        pass

    @abstractmethod
    def update(self, record: T) -> int:
        """
        Update an existing record in the repository.

        Accepts a record of type T and returns its ID.
        """
        pass

    @abstractmethod
    def delete(self, record_id: int) -> bool:
        """
        Delete a record by its ID.

        Returns True if the deletion was successful, False otherwise.
        """
        pass


class FeedRepository(Repository):

    @abstractmethod
    def get_feeds_by_user(self, user_id: int) -> list[Feed]:
        """
        Retrieve all feeds associated with a specific user.
        """
        pass


class ArticleRepository(Repository):

    @abstractmethod
    def get_articles_by_feed(self, feed_id: int) -> list[Article]:
        """
        Retrieve all articles associated with a specific feed.
        """
        pass


class UserRepository(Repository):

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.
        """
        pass

    @abstractmethod
    def get_all_users(self) -> list[User]:
        """
        Retrieve all users.
        """
        pass

    @abstractmethod
    def create_user(self, user: User) -> int:
        """
        Create a new user.
        """
        pass

    @abstractmethod
    def update_user(self, user: User) -> int:
        """
        Update an existing user.
        """
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by their ID.
        """
        pass
