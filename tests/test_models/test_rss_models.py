import pytest
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from src.thufir.models.rss import Base, Feed, Article


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


def test_create_feed(db_session):
    """Test basic Feed creation with required fields."""
    feed = Feed(
        title="Tech News",
        link="https://example.com/feed.xml",
        description="Latest tech updates",
        last_updated="2023-01-01T12:00:00Z",
        encoding="UTF-8",
    )
    db_session.add(feed)
    db_session.commit()

    assert feed.id is not None
    assert feed.title == "Tech News"
    assert feed.encoding == "UTF-8"

    assert db_session.query(Feed).count() == 1


def test_create_article(db_session):
    """Test basic Article creation with required fields."""
    feed = Feed(
        title="Tech News",
        link="https://example.com/feed.xml",
        description="Latest tech updates",
        last_updated="2023-01-01T12:00:00Z",
        encoding="UTF-8",
    )
    db_session.add(feed)
    db_session.commit()

    article = Article(
        feed_id=feed.id,
        title="New Tech Gadget",
        link="https://example.com/article/1",
        summary="A summary of the new tech gadget.",
        published="2023-01-02T12:00:00Z",
    )
    db_session.add(article)
    db_session.commit()

    assert article.id is not None
    assert article.title == "New Tech Gadget"
    assert article.feed_id == feed.id

    assert db_session.query(Article).count() == 1
