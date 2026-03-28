from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.thufir.auth import (
    TOKEN_TYPE,
    authenticate_user,
    create_access_token,
    create_user,
    get_current_user,
    get_session,
)
from src.thufir.models.user import AuthResponse, UserCreate, UserLogin, UserRead

router = APIRouter()


@router.post("/auth/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    session: Annotated[Session, Depends(get_session)],
) -> AuthResponse:
    user = create_user(session, user_data)
    return AuthResponse(
        access_token=create_access_token(user),
        token_type=TOKEN_TYPE,
        user=UserRead.model_validate(user),
    )


@router.post("/auth/login", response_model=AuthResponse)
def login(
    credentials: UserLogin,
    session: Annotated[Session, Depends(get_session)],
) -> AuthResponse:
    user = authenticate_user(session, credentials.username, credentials.password)
    return AuthResponse(
        access_token=create_access_token(user),
        token_type=TOKEN_TYPE,
        user=UserRead.model_validate(user),
    )


@router.post("/auth/logout")
def logout(
    current_user: Annotated[UserRead, Depends(get_current_user)],
) -> dict[str, str]:
    return {"message": f"{current_user.username} logged out"}


@router.get("/users/me", response_model=UserRead)
def get_profile(
    current_user: Annotated[UserRead, Depends(get_current_user)],
) -> UserRead:
    return UserRead.model_validate(current_user)


@router.get("/articles/")
def get_all_articles():
    return {"message": "List of all articles"}


@router.get("/channels/{channel_id}/articles/")
def get_all_articles_from_channel(channel_id: int):
    return {"message": f"List of articles from channel {channel_id}"}


@router.get("/articles/{article_id}")
def get_article(article_id: int):
    return {"message": f"Details of article {article_id}"}
