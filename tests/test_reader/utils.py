from dataclasses import dataclass


@dataclass
class MockFeedDescription:
    title: str
    link: str
    description: str


@dataclass
class MockFeed:
    entries: list[str]
    feed: MockFeedDescription
    bozo: dict | None = None


feed_foo = MockFeed(
    entries=[
        "Foo Entry 1",
        "Foo Entry 2",
        "Foo Entry 3",
    ],
    feed=MockFeedDescription(
        title="Foo Feed",
        link="http://example.com/foo",
        description="This is the Foo feed.",
    ),
)

feed_bar = MockFeed(
    entries=[
        "Bar Entry 1",
        "Bar Entry 2",
        "Bar Entry 3",
    ],
    feed=MockFeedDescription(
        title="Bar Feed",
        link="http://example.com/bar",
        description="This is the Bar feed.",
    ),
)


def mock_feed_parser(feed_url: str) -> MockFeed | None:

    if feed_url == "http://example.com/foo":
        return feed_foo
    elif feed_url == "http://example.com/bar":
        return feed_bar
    else:
        return None
