from abc import abstractmethod, ABC


class FeedRepository(ABC):
    """
    Abstract base class for feed repository operations.
    """

    @abstractmethod
    def add_feed(self, feed_data: dict) -> None:
        """
        Add a new feed to the repository.
        """
        pass

    @abstractmethod
    def get_feed(self, feed_id: int) -> dict:
        """
        Retrieve a feed by its ID.
        """
        pass

    @abstractmethod
    def update_feed(self, feed_id: int, feed_data: dict) -> None:
        """
        Update an existing feed in the repository.
        """
        pass

    @abstractmethod
    def delete_feed(self, feed_id: int) -> None:
        """
        Delete a feed from the repository.
        """
        pass
