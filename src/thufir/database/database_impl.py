from src.thufir.config.database_config import DatabaseConfig
from src.thufir.abstractions.database import Database
from src.thufir.exceptions.database import EngineCreationError
from src.thufir.models.rss import Base

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class DatabaseImpl(Database):

    def __init__(self, config: DatabaseConfig):
        self._engine = self._create_engine(config.connection_string, config.echo)

    @property
    def engine(self) -> Engine:
        return self._engine

    def _create_engine(self, connection_string: str, echo: bool) -> Engine:
        try:
            return create_engine(connection_string, echo=echo)
        except Exception as e:
            raise EngineCreationError(f"Failed to create database engine: {e}")

    def put_one(self, item: Base) -> None:
        pass
