from abc import ABC, abstractmethod

from fastapi import APIRouter
from src.thufir.abstractions.manager import Manager
from src.thufir.models.rss import Feed


class API(ABC):

    def __init__(self, manager: Manager, router: APIRouter):
        self.manager = manager
        self.router = router


class FeedAPI(API):

    @abstractmethod
    async def get_all_feeds(self) -> list[Feed]:
        """
        Retrieves a list of all feeds that currently logged in user is subscribed to.

        If the user is not logged in, should return error
        """
        pass

    @abstractmethod
    async def get_feed(self, feed_id: str) -> Feed:
        """
        Retrieves a specific feed by its ID.

        If the feed does not exist, should return error.
        """
        pass

    @abstractmethod
    async def get_all_available_feeds(self) -> list[Feed]:
        """
        Retrieves a list of all available feeds that the user can subscribe to.
        """
        pass

    @abstractmethod
    async def subscribe_to_feed(self, feed_id: str) -> None:
        """
        Subscribes the currently logged in user to a specific feed.

        If the user is not logged in, should return error.
        """
        pass

    @abstractmethod
    async def unsubscribe_from_feed(self, feed_id: str) -> None:
        """
        Unsubscribes the currently logged in user from a specific feed.

        If the user is not logged in, should return error.
        """
        pass

    @abstractmethod
    async def create_feed(self, feed_link: str) -> Feed:
        """
        Creates a new feed for the currently logged in user.
        Accepts link for xml with channel description

        If the user is not logged in, should return error.
        """
        pass

    @abstractmethod
    async def update_feed(self, feed_id: str, feed_link: str) -> Feed:
        """
        Updates an existing feed for the currently logged in user.
        Accepts link for xml with channel description

        If the user is not logged in, should return error.
        """
        pass


class ArticleAPI(API):

    @abstractmethod
    async def get_all_articles(self, feed_id: str) -> list:
        """
        Retrieves a list of all articles for a specific feed.

        If a feed does not exist, should return error.
        If a feed is empty, should return an empty list.
        """
        pass

    @abstractmethod
    async def get_article(self, feed_id: str, article_id: str) -> dict:
        """
        Retrieves a specific article by its ID within a specific feed.

        If the article does not exist, should return error.
        """
        pass

    @abstractmethod
    async def update_read_status(self, feed_id: str, article_id: str) -> None:
        """
        Marks a specific article as read/unread within a specific feed.

        If the article does not exist, should return error.
        """
        pass


class UserAPI(API):
    @abstractmethod
    async def create_user(self, user_data: dict) -> dict:
        """
        Creates a new user.

        If the user already exists, should return error.
        """
        pass

    @abstractmethod
    async def login_user(self, user_id: str) -> dict:  # TODO: rethink signature
        """
        Logs in a user.

        If the user does not exist, should return error.
        """
        pass

    @abstractmethod
    async def logout_user(self, user_id: str) -> None:
        """
        Logs out a user.

        If the user is not logged in, should return error.
        """
        pass
