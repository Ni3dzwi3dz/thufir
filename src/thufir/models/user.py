from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """Base model with common fields for User"""

    email: str = Field(description="User email address", index=True)
    username: str = Field(description="User name", index=True)


class User(UserBase, table=True):  # type: ignore
    """SQLModel for User - works as both Pydantic model and SQLAlchemy ORM"""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(description="Hashed password")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="User creation timestamp",
    )


class UserCreate(UserBase):
    """Model for creating a new user (without ID, with plain password)"""

    password: str = Field(
        description="Plain text password (will be hashed)", min_length=8
    )


class UserRead(UserBase):
    """Model for reading a user (with ID, without password hash)"""

    id: int
    created_at: datetime


class UserLogin(SQLModel):
    """Model for user login"""

    username: str
    password: str


class UserUpdate(SQLModel):
    """Model for updating user information"""

    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class TokenPayload(SQLModel):
    """Signed authentication token payload."""

    sub: int
    username: str
    exp: int


class AuthResponse(SQLModel):
    """Authentication response payload."""

    access_token: str
    token_type: str = "bearer"
    user: UserRead
