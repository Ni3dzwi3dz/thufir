from abc import abstractmethod, ABC
from typing import List, Optional, TypeVar
from src.thufir.abstractions.provider import Provider
from src.thufir.abstractions.repository import Repository
from src.thufir.models.base_model import ThufirModel
from src.thufir.abstractions.types import Id
from src.thufir.models.rss import Feed

T = TypeVar("T", bound=ThufirModel)


class Manager(ABC):

    def __init__(self, repository: Repository, provider: Optional[Provider] = None):
        self.provider = provider
        self.repository = repository


class FeedManager(Manager):
    """
    FeedManager is responsible for managing feeds, including their creation, retrieval, and deletion.
    It uses a repository to interact with the data store and a provider for additional functionalities.
    """

    @abstractmethod
    def create_feed(self, feed_data: dict) -> Feed:
        """
        Create a new feed with the provided data.
        """
        pass

    @abstractmethod
    def get_feed(self, feed_id: Id) -> Optional[Feed]:
        """
        Retrieve a feed by its ID.
        """
        pass

    @abstractmethod
    def list_available_feeds(self) -> List[Feed]:
        """
        List all available feeds.
        """
        pass

    @abstractmethod
    def list_user_feeds(self, user_id: Id) -> List[Feed]:
        """
        List all feeds associated with a specific user.
        """
        pass

    @abstractmethod
    def delete_feed(self, feed_id: Id) -> bool:
        """
        Delete a feed by its ID.
        """
        pass

    @abstractmethod
    def update_feed(self, feed_id: Id, feed_data: dict) -> Optional[T]:
        """
        Update a feed by its ID.
        """
        pass

    @abstractmethod
    def parse_feed(self, feed_id: Id) -> Feed:
        """
        Check feed to get new data.
        """
        pass
