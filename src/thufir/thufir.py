import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel

from src.thufir.container import Container
from src.thufir.api.api import router


def lifespan():
    SQLModel.metadata.create_all()
    yield
    SQLModel.metadata.drop_all()


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(
        title="Thufir",
        description="An RSS feed reader and aggregator",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.container = container
    app.include_router(router)

    return app


def dev():
    uvicorn.run("src.thufir.thufir:create_app", port=8000, reload=True)
