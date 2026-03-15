"""
Auth Router - registration, login, OTP, token refresh, profile.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.middleware.error_handler import DuplicateError, ShadowAlphaError
from app.models.user import TokenPair, TokenRefresh, User, UserCreate, UserLogin, UserOut

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=201)
async def register(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    """Register a new user account."""
    # Check duplicate email
    existing = await db.execute(
        select(User).where(User.email == payload.email)
    )
    if existing.scalar_one_or_none():
        raise DuplicateError("User", "email", payload.email)

    user = User(
        email=payload.email,
        phone=payload.phone,
        display_name=payload.display_name,
        hashed_password=hash_password(payload.password),
        referred_by=payload.invite_code,
    )
    db.add(user)
    await db.flush()
    return UserOut.model_validate(user)


@router.post("/login", response_model=TokenPair)
async def login(
    payload: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> TokenPair:
    """Authenticate and receive JWT token pair."""
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise ShadowAlphaError(
            error="INVALID_CREDENTIALS",
            message="Invalid email or password",
            code=401,
        )

    if not user.is_active:
        raise ShadowAlphaError(
            error="ACCOUNT_DISABLED",
            message="Your account has been deactivated",
            code=403,
        )

    return TokenPair(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/verify-otp")
async def verify_otp() -> dict:
    """Verify OTP code (stub - OTP provider integration pending)."""
    return {"message": "OTP verification stub - integration with SMS provider pending"}


@router.post("/refresh", response_model=TokenPair)
async def refresh_token(
    payload: TokenRefresh,
    db: AsyncSession = Depends(get_db),
) -> TokenPair:
    """Rotate refresh token and issue new access token."""
    decoded = decode_token(payload.refresh_token)
    if decoded.get("type") != "refresh":
        raise ShadowAlphaError(
            error="INVALID_TOKEN_TYPE",
            message="Expected refresh token",
            code=401,
        )

    user_id = uuid.UUID(decoded["sub"])
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise ShadowAlphaError(error="USER_NOT_FOUND", message="User not found", code=401)

    return TokenPair(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.get("/me", response_model=UserOut)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserOut:
    """Get authenticated user profile."""
    return UserOut.model_validate(current_user)

