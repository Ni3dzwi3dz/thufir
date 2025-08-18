from src.thufir.config.database_config import DatabaseConfig


class SQLiteDatabaseConfig(DatabaseConfig):
    """SQLite-specific database configuration model."""

    type: str = "sqlite"
    echo: bool = True

    @property
    def connection_string(self) -> str:
        return "sqlite:///:memory:"


sqlite_db_config = SQLiteDatabaseConfig(
    username="Foo", password="Bar", host="localhost", port=5432, database="test_db"
)
