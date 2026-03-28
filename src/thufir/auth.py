"""Authentication helpers and FastAPI dependencies for Thufir."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from typing import Annotated, Generator

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session
from sqlmodel import select

from src.thufir.models.user import TokenPayload, User, UserCreate

TOKEN_TYPE = "bearer"
TOKEN_TTL_SECONDS = 60 * 60 * 24
PBKDF2_ITERATIONS = 100_000


def get_auth_secret() -> str:
    """Return the auth secret used to sign access tokens."""

    return os.getenv("THUFIR_AUTH_SECRET", "thufir-dev-secret")


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2 with a per-password salt."""

    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return f"{salt.hex()}${password_hash.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a stored PBKDF2 hash."""

    try:
        salt_hex, digest_hex = password_hash.split("$", maxsplit=1)
    except ValueError:
        return False

    calculated_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        PBKDF2_ITERATIONS,
    ).hex()
    return hmac.compare_digest(calculated_hash, digest_hex)


def _urlsafe_b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _urlsafe_b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(f"{data}{padding}".encode("utf-8"))


def create_access_token(user: User, expires_in: int = TOKEN_TTL_SECONDS) -> str:
    """Create a signed access token for a user."""

    if user.id is None:
        raise ValueError("User ID is required to create an access token")

    payload = TokenPayload(
        sub=user.id,
        username=user.username,
        exp=int(time.time()) + expires_in,
    )
    payload_segment = _urlsafe_b64encode(
        json.dumps(payload.model_dump(), separators=(",", ":")).encode("utf-8")
    )
    signature_segment = _urlsafe_b64encode(
        hmac.new(
            get_auth_secret().encode("utf-8"),
            payload_segment.encode("utf-8"),
            hashlib.sha256,
        ).digest()
    )
    return f"{payload_segment}.{signature_segment}"


def decode_access_token(token: str) -> TokenPayload:
    """Decode and verify a signed access token."""

    try:
        payload_segment, signature_segment = token.split(".", maxsplit=1)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        ) from error

    expected_signature = _urlsafe_b64encode(
        hmac.new(
            get_auth_secret().encode("utf-8"),
            payload_segment.encode("utf-8"),
            hashlib.sha256,
        ).digest()
    )

    if not hmac.compare_digest(signature_segment, expected_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    payload = TokenPayload.model_validate(
        json.loads(_urlsafe_b64decode(payload_segment).decode("utf-8"))
    )
    if payload.exp < int(time.time()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired",
        )

    return payload


def get_session(request: Request) -> Generator[Session, None, None]:
    """Provide a database session from the FastAPI application state."""

    with request.app.state.database.session() as session:
        yield session


def get_user_by_email(session: Session, email: str) -> User | None:
    """Find a user by email address."""

    statement = select(User).where(User.email == email)
    return session.execute(statement).scalar_one_or_none()


def get_user_by_username(session: Session, username: str) -> User | None:
    """Find a user by username."""

    statement = select(User).where(User.username == username)
    return session.execute(statement).scalar_one_or_none()


def create_user(session: Session, user_data: UserCreate) -> User:
    """Create and persist a new user after uniqueness validation."""

    if get_user_by_email(session, user_data.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    if get_user_by_username(session, user_data.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken",
        )

    user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hash_password(user_data.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, username: str, password: str) -> User:
    """Authenticate a user by username and password."""

    user = get_user_by_username(session, username)
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return user


def _extract_bearer_token(authorization: str | None) -> str:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != TOKEN_TYPE or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )
    return token


def get_current_user(
    session: Annotated[Session, Depends(get_session)],
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
) -> User:
    """Resolve the current user from a bearer token."""

    token = _extract_bearer_token(authorization)
    payload = decode_access_token(token)
    statement = select(User).where(User.id == payload.sub)
    user = session.execute(statement).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
