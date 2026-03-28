from contextlib import contextmanager
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from typing import Generator, List, Type, TypeVar

from src.thufir.config.database_config import DatabaseConfig
from src.thufir.abstractions.database import Database
from src.thufir.exceptions.database import EngineCreationError

# TODO: Handle exceptions in database operations
T = TypeVar("T", bound=SQLModel)


class DatabaseImpl(Database):

    def __init__(self, config: DatabaseConfig):
        self._engine = self._create_engine(config.connection_string, config.echo)

    @property
    def engine(self) -> Engine:
        return self._engine

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session = Session(self._engine)
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def _create_engine(self, connection_string: str, echo: bool) -> Engine:
        try:
            connect_args = {}
            engine_kwargs = {"echo": echo}

            if connection_string.startswith("sqlite"):
                connect_args["check_same_thread"] = False
                if connection_string.endswith(":memory:"):
                    engine_kwargs["poolclass"] = StaticPool

            if connect_args:
                engine_kwargs["connect_args"] = connect_args

            return create_engine(connection_string, **engine_kwargs)
        except Exception as e:
            raise EngineCreationError(f"Failed to create database engine: {e}")

    def put_one(self, model: Type[T], item: T) -> None:
        with self.session() as session:
            session.add(item)
            session.commit()

    def put_many(self, items: list[T]) -> None:
        with self.session() as session:
            session.add_all(items)
            session.commit()

    def get_all(self, model: Type[T]) -> List[T]:
        with self.session() as session:
            return session.query(model).all()

    def get_filtered(self, model, *filters):
        with self.session() as session:
            return session.query(model).filter(*filters).all()

    def get_by_id(self, model: Type[T], item_id: int) -> T | None:
        with self.session() as session:
            stmt = select(model).where(model.id == item_id)  # type: ignore[attr-defined]
            result = session.execute(stmt).scalar_one_or_none()
            return result

    def update_one(self, item: T) -> None:
        with self.session() as session:
            session.merge(item)
            session.commit()

    def update_many(self, items: List[T]) -> None:
        with self.session() as session:
            for item in items:
                session.merge(item)
            session.commit()

    def delete_one(self, model: Type[T], item_id: int) -> None:
        with self.session() as session:
            item = session.query(model).filter_by(id=item_id).first()  # type: ignore[attr-defined]
            if item:
                session.delete(item)
                session.commit()
            # TODO handle case where item is not found, maybe raise an exception

    def delete_many(self, model: Type[T], item_ids: List[int]) -> None:
        with self.session() as session:
            items = session.query(model).filter(model.id.in_(item_ids)).all()  # type: ignore[attr-defined]
            for item in items:
                session.delete(item)
            session.commit()
