import feedparser
import logging
from typing import Callable, Dict, List

log = logging.getLogger(__name__)


class RSSReader:
    default_feed_parser = feedparser.parse

    def __init__(
        self, feeds: List[str], feed_parser: Callable[[str], Dict] | None = None
    ):

        log.debug("Initializing RSSReader with feeds: %s", feeds)

        self.feed_urls = feeds
        self.feed_parser = feed_parser if feed_parser else self.default_feed_parser
        self.feeds: Dict[str, Dict] = {}

    def parse_feeds(self) -> Dict:
        """Parse all feeds and return a dictionary of feed titles and their parsed data."""

        feeds = {}

        for feed in self.feed_urls:
            parsed_feed = self.feed_parser(feed)
            if parsed_feed.bozo:
                log.error(f"Error parsing feed {feed}: {parsed_feed.bozo_exception}")
                continue

            log.debug(f"Parsed feed: {parsed_feed.feed.title}")

            feeds[parsed_feed.feed.title] = parsed_feed

        self.feeds = feeds
        return feeds

    def get_all_entries(self) -> List:
        """Return all entries from all feeds."""
        log.debug("Getting all entries from all feeds.")
        all_entries = []
        for feed in self.feeds.values():
            all_entries.extend(feed.entries)  # type: ignore

        return all_entries

    def get_entries_from_feed(self, feed_title: str) -> List:
        """Return all entries from a specific feed."""
        if feed_title in self.feeds:
            return self.feeds[feed_title].entries  # type: ignore
        else:
            log.error(f"Feed {feed_title} not found.")
            return []
