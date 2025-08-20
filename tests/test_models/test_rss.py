import datetime
from src.thufir.models.rss import Feed


def test_if_conversion_to_db_model_works_for_feed():

    model = Feed(
        id=1,
        title="Test Feed",
        link="http://example.com/feed",
        description="This is a test feed",
        last_updated=datetime.datetime(
            2023, 10, 1, 12, 0, 0, tzinfo=datetime.timezone.utc
        ),
        encoding="UTF-8",
    )
    db_model = Feed.from_db_model(model.to_db_model())

    assert db_model == model
