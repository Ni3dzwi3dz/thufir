from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from src.thufir.container import Container
from src.thufir.api.api import router
from src.thufir.config.database_config import DatabaseConfig
from src.thufir.database.database_impl import DatabaseImpl
from src.thufir.models.user import User  # noqa: F401


class SQLiteAppDatabaseConfig(DatabaseConfig):
    """SQLite database configuration for local development and tests."""

    host: str = "localhost"
    username: str = ""
    password: str = ""
    port: int = 0
    database: str = "thufir"
    type: str = "sqlite"
    echo: bool = False
    path: str = ""

    @property
    def connection_string(self) -> str:
        return f"sqlite:///{self.path}"


def create_default_database() -> DatabaseImpl:
    """Create the default application database instance."""

    database_path = Path(__file__).resolve().parents[2] / "thufir.db"
    return DatabaseImpl(SQLiteAppDatabaseConfig(path=str(database_path)))


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(app.state.database.engine)
    yield


def create_app(database: DatabaseImpl | None = None) -> FastAPI:
    container = Container()
    database_impl = database or create_default_database()

    app = FastAPI(
        title="Thufir",
        description="An RSS feed reader and aggregator",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.container = container
    app.state.database = database_impl
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)

    return app


def dev():
    uvicorn.run("src.thufir.thufir:create_app", port=8000, reload=True, factory=True)
