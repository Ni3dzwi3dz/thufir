from typing import Optional
from pydantic import Field, PrivateAttr
from datetime import datetime

from src.thufir.models.base_model import ThufirModel
from src.thufir.database.models.rss import Feed as DBFeed, Article as DBArticle


class Feed(ThufirModel):
    """
    Model representing an RSS feed.
    """

    _db_model = PrivateAttr(default=DBFeed)

    id: Optional[int] = Field(default=None)
    title: str = Field(..., description="Title of the feed")
    link: str = Field(..., description="Link to the feed")
    description: str = Field(..., description="Description of the feed")
    last_updated: datetime = Field(
        ..., description="Last updated timestamp of the feed"
    )
    encoding: str = Field(..., description="Encoding of the feed")


class Article(ThufirModel):
    """
    Model representing an article in an RSS feed.
    """

    _db_model = PrivateAttr(default=DBArticle)

    id: Optional[int] = Field(default=None)
    feed_id: int = Field(..., description="ID of the feed this article belongs to")
    title: str = Field(..., description="Title of the article")
    link: str = Field(..., description="Link to the article")
    summary: str = Field(..., description="Summary of the article")
    published: datetime = Field(..., description="Published timestamp of the article")
