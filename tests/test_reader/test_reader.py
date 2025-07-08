from thufir.reader.rss_reader import RSSReader
from tests.test_reader.utils import mock_feed_parser


class TestReader:

    def test_feeds_are_parsed_correctly(self):
        reader = RSSReader(
            ["http://example.com/foo", "http://example.com/bar"], mock_feed_parser
        )
        reader.parse_feeds()

        assert len(reader.feeds.keys()) == 2
        assert reader.feeds["Foo Feed"].feed.title == "Foo Feed"
        assert reader.feeds["Bar Feed"].feed.title == "Bar Feed"

    def test_get_all_entries(self):
        reader = RSSReader(
            ["http://example.com/foo", "http://example.com/bar"], mock_feed_parser
        )
        reader.parse_feeds()

        all_entries = reader.get_all_entries()

        assert len(all_entries) == 6
        assert "Foo Entry 1" in all_entries
        assert "Bar Entry 1" in all_entries

    def test_get_entries_from_feed(self):
        reader = RSSReader(
            ["http://example.com/foo", "http://example.com/bar"], mock_feed_parser
        )
        reader.parse_feeds()

        foo_entries = reader.get_entries_from_feed("Foo Feed")
        bar_entries = reader.get_entries_from_feed("Bar Feed")

        assert len(foo_entries) == 3
        assert len(bar_entries) == 3

        assert "Foo Entry 1" in foo_entries
        assert "Foo Entry 1" not in bar_entries
        assert "Bar Entry 1" in bar_entries
        assert "Bar Entry 1" not in foo_entries
