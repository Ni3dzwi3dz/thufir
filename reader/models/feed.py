from dataclasses import dataclass


@dataclass
class FeedDescription:
    url: str
    title: str
    description: str
    icon: str

    @classmethod
    def from_feed(cls, feed):
        return cls(
            url=feed.url,
            title=feed.title,
            description=feed.description,
            icon=feed.icon,
        )