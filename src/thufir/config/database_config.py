import os

from pydantic import BaseModel, Field, model_validator


class DatabaseConfig(BaseModel):
    model_config = {
        "extra": "forbid",  # Disallow extra fields
        "frozen": True,  # Make the model immutable
    }

    host: str = Field(description="Database host")
    username: str = Field(description="Database username")
    password: str = Field(description="Database password")
    port: int = Field(description="Database port")
    database: str = Field(description="Database name")
    echo: bool = Field(default=True, description="Enable SQLAlchemy echo")
    type: str = Field(
        default="postgresql", description="Database type (e.g., postgresql, mysql)"
    )

    @model_validator(mode="before")
    @classmethod
    def add_from_env(cls, data: dict) -> dict:
        """
        Add configuration from environment variables.
        """

        for field in cls.model_fields.keys():
            env_value = os.getenv(f"THUFIR_DB_{field.upper()}")
            if env_value is not None:
                data[field] = env_value

        return data

    @property
    def connection_string(self) -> str:
        """
        Returns the database connection string.
        """
        return f"{self.type}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
