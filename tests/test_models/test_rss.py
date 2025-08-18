from src.thufir.models.rss import Feed


def test_if_conversion_to_db_model_works_for_feed():

    model = Feed(
        id=1,
        title="Test Feed",
        link="http://example.com/feed",
        description="This is a test feed",
        last_updated="2023-10-01T12:00:00Z",
        encoding="UTF-8",
    )
    db_model = Feed.from_db_model(model.to_db_model())

    assert db_model == model
