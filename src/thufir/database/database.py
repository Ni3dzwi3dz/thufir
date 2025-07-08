from thufir.config.database_config import DatabaseConfig

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine(config: DatabaseConfig) -> Engine:
    """
    Returns a SQLAlchemy engine based on the provided DatabaseConfig.
    """

    # Create and return the SQLAlchemy engine
    return create_engine(config.connection_string, echo=config.echo)
