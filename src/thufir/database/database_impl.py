from src.thufir.config.database_config import DatabaseConfig
from src.thufir.abstractions.database import Database
from src.thufir.exceptions.database import EngineCreationError
from src.thufir.models.rss import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from typing import List, Type


class DatabaseImpl(Database):

    def __init__(self, config: DatabaseConfig):
        self._engine = self._create_engine(config.connection_string, config.echo)

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def session(self) -> Session:
        session = Session(self._engine)
        yield session
        session.close()

    def _create_engine(self, connection_string: str, echo: bool) -> Engine:
        try:
            return create_engine(connection_string, echo=echo)
        except Exception as e:
            raise EngineCreationError(f"Failed to create database engine: {e}")

    def _create_query(self, model: Type[Base]):
        with Session(self._engine) as session:
            return session.query(model)

    def put_one(self, model: Type[Base], item: Base) -> None:
        with Session(self._engine) as session:
            session.add(item)
            session.commit()

    def put_many(self, items: list[Base]) -> None:
        with Session(self._engine) as session:
            session.add_all(items)
            session.commit()

    def get_all(self, model: Type[Base]) -> List[Base]:
        return self._create_query(model).all()

    def get_filtered(self, model, **filters):
        return self._create_query(model).filter_by(**filters).all()

    def get_by_id(self, model: Type[Base], item_id: int) -> Base:
        return self._create_query(model).filter_by(id=item_id).first()

    def update_one(self, item: Base) -> None:
        with Session(self._engine) as session:
            session.merge(item)
            session.commit()

    def update_many(self, items: List[Base]) -> None:
        with Session(self._engine) as session:
            for item in items:
                session.merge(item)
            session.commit()

    def delete_one(self, model: Type[Base], item_id: int) -> None:
        with Session(self._engine) as session:
            item = session.query(model).filter_by(id=item_id).first()
            if item:
                session.delete(item)
                session.commit()
            # TODO handle case where item is not found, maybe raise an exception

    def delete_many(self, model: Type[Base], item_ids: List[int]) -> None:
        with Session(self._engine) as session:
            items = session.query(model).filter(model.id.in_(item_ids)).all()
