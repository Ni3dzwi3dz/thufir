import datetime
from src.thufir.models.rss import (
    Feed,
    FeedCreate,
    FeedRead,
    Article,
    ArticleCreate,
    ArticleRead,
)


def test_feed_creation_and_validation():
    """Test creating a Feed model with SQLModel"""
    feed = Feed(
        id=1,
        title="Test Feed",
        link="http://example.com/feed",
        description="This is a test feed",
        last_updated=datetime.datetime(
            2023, 10, 1, 12, 0, 0, tzinfo=datetime.timezone.utc
        ),
        encoding="UTF-8",
    )

    assert feed.id == 1
    assert feed.title == "Test Feed"
    assert feed.link == "http://example.com/feed"
    assert feed.description == "This is a test feed"
    assert feed.encoding == "UTF-8"


def test_feed_create_model():
    """Test FeedCreate model (without ID)"""
    feed_create = FeedCreate(
        title="New Feed",
        link="http://example.com/new-feed",
        description="A new test feed",
        last_updated=datetime.datetime.now(),
        encoding="UTF-8",
    )

    assert feed_create.title == "New Feed"
    assert feed_create.link == "http://example.com/new-feed"
    # FeedCreate should not have an id field
    assert not hasattr(feed_create, "id")


def test_feed_read_model():
    """Test FeedRead model (with ID)"""
    feed_read = FeedRead(
        id=1,
        title="Read Feed",
        link="http://example.com/read-feed",
        description="A feed for reading",
        last_updated=datetime.datetime.now(),
        encoding="UTF-8",
    )

    assert feed_read.id == 1
    assert feed_read.title == "Read Feed"


def test_article_creation_and_validation():
    """Test creating an Article model with SQLModel"""
    article = Article(
        id=1,
        feed_id=1,
        title="Test Article",
        link="http://example.com/article",
        summary="This is a test article",
        published=datetime.datetime(
            2023, 10, 1, 12, 0, 0, tzinfo=datetime.timezone.utc
        ),
    )

    assert article.id == 1
    assert article.feed_id == 1
    assert article.title == "Test Article"
    assert article.link == "http://example.com/article"
    assert article.summary == "This is a test article"


def test_article_create_model():
    """Test ArticleCreate model (without ID)"""
    article_create = ArticleCreate(
        feed_id=1,
        title="New Article",
        link="http://example.com/new-article",
        summary="A new test article",
        published=datetime.datetime.now(),
    )

    assert article_create.feed_id == 1
    assert article_create.title == "New Article"
    # ArticleCreate should not have an id field
    assert not hasattr(article_create, "id")


def test_article_read_model():
    """Test ArticleRead model (with ID)"""
    article_read = ArticleRead(
        id=1,
        feed_id=1,
        title="Read Article",
        link="http://example.com/read-article",
        summary="An article for reading",
        published=datetime.datetime.now(),
    )

    assert article_read.id == 1
    assert article_read.feed_id == 1
    assert article_read.title == "Read Article"


def test_model_dict_conversion():
    """Test converting models to dictionaries"""
    feed = Feed(
        id=1,
        title="Test Feed",
        link="http://example.com/feed",
        description="This is a test feed",
        last_updated=datetime.datetime.now(),
        encoding="UTF-8",
    )

    feed_dict = feed.dict()
    assert feed_dict["id"] == 1
    assert feed_dict["title"] == "Test Feed"
    assert "last_updated" in feed_dict


def test_model_json_serialization():
    """Test JSON serialization of models"""
    feed_create = FeedCreate(
        title="JSON Feed",
        link="http://example.com/json-feed",
        description="A feed for JSON testing",
        last_updated=datetime.datetime.now(),
        encoding="UTF-8",
    )

    json_str = feed_create.json()
    assert "JSON Feed" in json_str
    assert "json-feed" in json_str


def test_feed_create_to_table_model():
    """Test converting FeedCreate to Feed (table model)"""
    feed_create = FeedCreate(
        title="Create to Table",
        link="http://example.com/create-table",
        description="Converting create model to table model",
        last_updated=datetime.datetime.now(),
        encoding="UTF-8",
    )

    # Convert to table model
    feed = Feed(**feed_create.dict())

    assert feed.title == feed_create.title
    assert feed.link == feed_create.link
    assert feed.description == feed_create.description
    assert feed.id is None  # Should be None until saved to DB
