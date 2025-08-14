import pytest

from src.thufir.database.database_impl import DatabaseImpl
from src.thufir.config.database_config import DatabaseConfig
from src.thufir.models.rss import Base, Feed, Article

from tests.utils.database_config import sqlite_db_config


@pytest.fixture
def db_impl():
    db = DatabaseImpl(sqlite_db_config)
    # Ensure the database schema is created
    Base.metadata.create_all(db.engine)
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


def test_sql_errors_raise_correct_exceptions(db_impl: DatabaseImpl):
    """Test that SQL errors raise the correct exceptions."""
    pass


def test_put_many(db_impl: DatabaseImpl):
    """Test inserting multiple records into the database."""
    feed1 = Feed(
        title="Test Feed 2",
        link="http://example.com/feed2",
        description="Test Description 2",
        last_updated="2023-01-02T00:00:00Z",
        encoding="UTF-8",
    )
    feed2 = Feed(
        title="Test Feed 3",
        link="http://example.com/feed3",
        description="Test Description 3",
        last_updated="2023-01-03T00:00:00Z",
        encoding="UTF-8",
    )

    db_impl.put_many([feed1, feed2])

    assert len(db_impl.get_all(Feed)) == 2


def test_get_filtered(db_impl: DatabaseImpl):
    """Test retrieving filtered records from the database."""
    feed1 = Feed(
        title="Test Feed 2",
        link="http://example.com/feed2",
        description="Test Description 2",
        last_updated="2023-01-02T00:00:00Z",
        encoding="UTF-8",
    )
    feed2 = Feed(
        title="Test Feed 3",
        link="http://example.com/feed3",
        description="Test Description 3",
        last_updated="2023-01-03T00:00:00Z",
        encoding="UTF-8",
    )
    feed3 = Feed(
        title="Test Feed 3",
        link="http://example.com/feed3",
        description="Test Description 3",
        last_updated="2023-01-03T00:00:00Z",
        encoding="CP1252",
    )

    db_impl.put_many([feed1, feed2])

    # Test with keyword filters
    test_feeds = db_impl.get_filtered(Feed, Feed.title == "Test Feed 2")
    assert len(test_feeds) == 1
    assert test_feeds[0].description == "Test Description 2"

    # Test with multiple filters
    recent_feeds = db_impl.get_filtered(
        Feed, Feed.encoding == "UTF-8", Feed.title == "Test Feed 3"
    )
    assert len(recent_feeds) == 1
    assert recent_feeds[0].link == "http://example.com/feed3"


def test_get_all(db_impl: DatabaseImpl):
    """Test retrieving all records of a model."""
    feeds = [
        Feed(
            title="Feed 1",
            link="l1",
            description="d1",
            last_updated="2023-01-01",
            encoding="UTF-8",
        ),
        Feed(
            title="Feed 2",
            link="l2",
            description="d2",
            last_updated="2023-01-02",
            encoding="UTF-8",
        ),
    ]
    db_impl.put_many(feeds)

    all_feeds = db_impl.get_all(Feed)
    assert len(all_feeds) == 2
    assert {f.title for f in all_feeds} == {"Feed 1", "Feed 2"}


def test_get_by_id(db_impl: DatabaseImpl):
    """Test retrieving item by ID."""
    feed = Feed(
        title="Test Feed",
        link="http://example.com",
        description="Test",
        last_updated="2023-01-01T00:00:00Z",
        encoding="UTF-8",
    )
    db_impl.put_one(Feed, feed)

    # Test found
    retrieved = db_impl.get_by_id(Feed, 1)
    assert retrieved.id == 1
    assert retrieved.title == "Test Feed"

    # Test not found
    assert db_impl.get_by_id(Feed, 999) is None


def test_update_one(db_impl: DatabaseImpl):
    """Test updating a single record in the database."""
    feed = Feed(
        title="Old Title",
        link="http://example.com/old",
        description="Old Description",
        last_updated="2023-01-01T00:00:00Z",
        encoding="UTF-8",
    )
    db_impl.put_one(Feed, feed)

    # Update the feed
    feed.title = "New Title"
    db_impl.update_one(feed)

    updated_feed = db_impl.get_by_id(Feed, 1)
    assert updated_feed.title == "New Title"


def test_update_many(db_impl: DatabaseImpl):
    """Test updating multiple records in the database."""
    feed1 = Feed(
        title="Feed 1",
        link="http://example.com/feed1",
        description="Description 1",
        last_updated="2023-01-01T00:00:00Z",
        encoding="UTF-8",
    )
    feed2 = Feed(
        title="Feed 2",
        link="http://example.com/feed2",
        description="Description 2",
        last_updated="2023-01-02T00:00:00Z",
        encoding="UTF-8",
    )
    db_impl.put_many([feed1, feed2])

    # Update both feeds
    feed1.title = "Updated Feed 1"
    feed2.title = "Updated Feed 2"
    db_impl.update_many([feed1, feed2])

    updated_feeds = db_impl.get_all(Feed)
    assert len(updated_feeds) == 2
    assert updated_feeds[0].title == "Updated Feed 1"
    assert updated_feeds[1].title == "Updated Feed 2"


def test_delete_one(db_impl: DatabaseImpl):
    """Test deleting a single record from the database."""
    feed = Feed(
        title="Feed to Delete",
        link="http://example.com/delete",
        description="Delete this feed",
        last_updated="2023-01-01T00:00:00Z",
        encoding="UTF-8",
    )
    db_impl.put_one(Feed, feed)

    # Delete the feed
    db_impl.delete_one(Feed, 1)

    assert db_impl.get_by_id(Feed, 1) is None


def test_delete_many(db_impl: DatabaseImpl):
    """Test deleting multiple records from the database."""
    feed1 = Feed(
        title="Feed 1",
        link="http://example.com/feed1",
        description="Description 1",
        last_updated="2023-01-01T00:00:00Z",
        encoding="UTF-8",
    )
    feed2 = Feed(
        title="Feed 2",
        link="http://example.com/feed2",
        description="Description 2",
        last_updated="2023-01-02T00:00:00Z",
        encoding="UTF-8",
    )
    db_impl.put_many([feed1, feed2])

    assert len(db_impl.get_all(Feed)) == 2

    # Delete both feeds
    db_impl.delete_many(Feed, [1, 2])

    assert len(db_impl.get_all(Feed)) == 0
