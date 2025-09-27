from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class FeedBase(SQLModel):
    """Base model with common fields for Feed"""

    title: str = Field(description="Title of the feed")
    link: str = Field(description="Link to the feed")
    description: str = Field(description="Description of the feed")
    last_updated: datetime = Field(description="Last updated timestamp of the feed")
    encoding: str = Field(description="Encoding of the feed")


class Feed(FeedBase, table=True):
    """SQLModel for Feed - works as both Pydantic model and SQLAlchemy ORM"""

    __tablename__ = "feeds"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to articles
    articles: List["Article"] = Relationship(back_populates="feed")


class FeedCreate(FeedBase):
    """Model for creating a new feed (without ID)"""

    pass


class FeedRead(FeedBase):
    """Model for reading a feed (with ID)"""

    id: int


class ArticleBase(SQLModel):
    """Base model with common fields for Article"""

    title: str = Field(description="Title of the article")
    link: str = Field(description="Link to the article")
    summary: str | None = Field(None, description="Summary of the article")
    published: datetime = Field(description="Publication date of the article")


class Article(ArticleBase, table=True):
    """SQLModel for Article - works as both Pydantic model and SQLAlchemy ORM"""

    __tablename__ = "articles"

    id: Optional[int] = Field(default=None, primary_key=True)
    feed_id: int = Field(foreign_key="feeds.id")

    # Relationship to feed
    feed: Optional[Feed] = Relationship(back_populates="articles")


class ArticleCreate(ArticleBase):
    """Model for creating a new article (without ID)"""

    feed_id: int


class ArticleRead(ArticleBase):
    """Model for reading an article (with ID)"""

    id: int
    feed_id: int
