import os

from pydantic import BaseModel, Field, model_validator


class DatabaseConfig(BaseModel):
    model_config = {
        "extra": "forbid",  # Disallow extra fields
        "frozen": True,  # Make the model immutable
    }

    host: str = Field(default="localhost", description="Database host")
    username: str = Field(default="user", description="Database username")
    password: str = Field(default="password", description="Database password")
    port: int = Field(default=5432, description="Database port")
    database: str = Field(default="mydatabase", description="Database name")
    echo: bool = Field(default=True, description="Enable SQLAlchemy echo")

    @model_validator(mode="before")
    def add_from_env(self):
        """
        Add configuration from environment variables.
        """

        self.username = os.getenv("DB_USERNAME", self.username)
        self.password = os.getenv("DB_PASSWORD", self.password)
        self.host = os.getenv("DB_HOST", self.host)
        self.port = int(os.getenv("DB_PORT", self.port))
        self.database = os.getenv("DB_DATABASE", self.database)
        self.echo = bool(os.getenv("DB_ECHO", self.echo))

    @property
    def connection_string(self) -> str:
        """
        Returns the database connection string.
        """
        return (
            f"{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        )
