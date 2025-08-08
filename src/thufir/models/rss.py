from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Feed(Base):
    __tablename__ = "feeds"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    link: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    last_updated: Mapped[str] = mapped_column()
    encoding: Mapped[str] = mapped_column()


class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(primary_key=True)
    feed_id: Mapped[int] = mapped_column(ForeignKey("feeds.id"))
    title: Mapped[str] = mapped_column()
    link: Mapped[str] = mapped_column()
    summary: Mapped[str] = mapped_column()
    published: Mapped[str] = mapped_column()
