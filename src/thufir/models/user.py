from typing import Optional
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    """Base model with common fields for User"""

    email: str = Field(description="User email address", unique=True)
    name: str = Field(description="User full name")


class User(UserBase, table=True):
    """SQLModel for User - works as both Pydantic model and SQLAlchemy ORM"""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(description="Hashed password")


class UserCreate(UserBase):
    """Model for creating a new user (without ID, with plain password)"""

    password: str = Field(description="Plain text password (will be hashed)")


class UserRead(UserBase):
    """Model for reading a user (with ID, without password hash)"""

    id: int


class UserLogin(SQLModel):
    """Model for user login"""

    email: str
    password: str


class UserUpdate(SQLModel):
    """Model for updating user information"""

    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
