"""
User model and schemas.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, GUID, TimestampMixin, UUIDPrimaryKeyMixin


# ── Enums ─────────────────────────────────────────────────────────────────
class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    ALPHA = "alpha"
    PREMIER = "premier"
    BLACK_CARD = "black_card"


class KYCStatus(str, enum.Enum):
    UNVERIFIED = "unverified"
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"


# ── SQLAlchemy Model ──────────────────────────────────────────────────────
class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    tier: Mapped[SubscriptionTier] = mapped_column(
        Enum(SubscriptionTier), default=SubscriptionTier.FREE, nullable=False,
    )
    kyc_status: Mapped[KYCStatus] = mapped_column(
        Enum(KYCStatus), default=KYCStatus.UNVERIFIED, nullable=False,
    )
    promo_code: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True)
    referred_by: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    wallet_balance: Mapped[Optional[float]] = mapped_column(default=0.0, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Relationships
    positions = relationship("Position", back_populates="user", lazy="selectin")


# ── Pydantic Schemas ──────────────────────────────────────────────────────
class UserCreate(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    display_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8)
    invite_code: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: uuid.UUID
    email: str
    phone: Optional[str] = None
    display_name: str
    tier: SubscriptionTier
    kyc_status: KYCStatus
    promo_code: Optional[str] = None
    wallet_balance: float = 0.0
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str
