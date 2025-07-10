import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from src.thufir.models.rss import Base, Feed, Article

# TODO: These tests rely on each other, think of a way to make them independent,
# or putting everything in a flow test


@pytest.fixture(scope="module")
def engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    clear_mappers()


@pytest.fixture
def session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_feed(session):
    feed = Feed(
        title="Test Feed",
        link="http://example.com",
        description="A test feed",
        last_updated="2024-07-10",
        encoding="utf-8",
    )
    session.add(feed)
    session.commit()
    assert feed.id is not None


def test_create_article(session):
    feed = Feed(
        title="Feed for Article",
        link="http://feed.com",
        description="Feed desc",
        last_updated="2024-07-10",
        encoding="utf-8",
    )
    session.add(feed)
    session.commit()

    article = Article(
        feed_id=feed.id,
        title="Test Article",
        link="http://article.com",
        summary="Article summary",
        published="2024-07-10",
    )
    session.add(article)
    session.commit()
    assert article.id is not None
    assert article.feed_id == feed.id


def test_query_feed(session):
    feed = session.query(Feed).filter_by(title="Test Feed").first()
    assert feed is not None
    assert feed.title == "Test Feed"
    assert feed.link == "http://example.com"


def test_query_article(session):
    article = session.query(Article).filter_by(title="Test Article").first()
    assert article is not None
    assert article.title == "Test Article"
    assert article.link == "http://article.com"
    assert article.feed_id is not None


def test_number_of_feeds(session):
    count = session.query(Feed).count()
    assert count == 2


def test_number_of_articles(session):
    count = session.query(Article).count()
    assert count == 1
