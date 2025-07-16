import pytest

from src.thufir.database.database_impl import DatabaseImpl
from src.thufir.config.database_config import DatabaseConfig
from src.thufir.models.rss import Base, Feed, Article

from tests.utils.database_config import sqlite_db_config


@pytest.fixture
def db_impl():
    db = DatabaseImpl(sqlite_db_config)
    Base.metadata.create_all(db.engine)  # Ensure the database schema is created
    yield db


def test_put_one(db_impl: DatabaseImpl):
    """Test inserting a single record into the database."""
    feed = Feed(
        id=1,
        title="Test Feed",
        link="http://example.com/feed",
        description="Test Description",
        last_updated="2023-01-01T00:00:00Z",
        encoding="UTF-8",
    )
    article = Article(
        id=1,
        title="Test Article",
        link="http://example.com/article",
        feed_id=feed.id,
        summary="Test Summary",
        published="2023-01-01T00:00:00Z",
    )

    db_impl.put_one(Feed, feed)
    db_impl.put_one(Article, article)

    assert len(db_impl.get_all(Feed)) == 1
    assert len(db_impl.get_all(Article)) == 1
