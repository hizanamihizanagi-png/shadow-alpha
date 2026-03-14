"""
Position model and schemas.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, GUID, TimestampMixin, UUIDPrimaryKeyMixin


# ── Enums ─────────────────────────────────────────────────────────────────
class PositionStatus(str, enum.Enum):
    ACTIVE = "active"
    WON = "won"
    LOST = "lost"
    SOLD = "sold"
    SETTLED = "settled"
    CANCELLED = "cancelled"
    LOCKED = "locked"  # Position used as loan collateral


# ── SQLAlchemy Model ──────────────────────────────────────────────────────
class Position(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "positions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, index=True,
    )
    sportsbook: Mapped[str] = mapped_column(String(100), nullable=False)
    teams: Mapped[str] = mapped_column(String(255), nullable=False)
    league: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    odds: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)
    stake: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    max_payout: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    current_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("0.00"))
    current_prob: Mapped[Optional[float]] = mapped_column(nullable=True)
    time_remaining: Mapped[Optional[float]] = mapped_column(nullable=True)  # 0..1
    status: Mapped[PositionStatus] = mapped_column(
        Enum(PositionStatus), default=PositionStatus.ACTIVE, nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="positions")


# ── Pydantic Schemas ──────────────────────────────────────────────────────
class PositionCreate(BaseModel):
    sportsbook: str = Field(..., min_length=1, max_length=100)
    teams: str = Field(..., min_length=1, max_length=255)
    league: Optional[str] = None
    odds: Decimal = Field(..., gt=Decimal("1.0"))
    stake: Decimal = Field(..., gt=Decimal("0"))
    description: Optional[str] = None


class PositionOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    sportsbook: str
    teams: str
    league: Optional[str] = None
    odds: Decimal
    stake: Decimal
    max_payout: Decimal
    current_value: Decimal
    current_prob: Optional[float] = None
    time_remaining: Optional[float] = None
    status: PositionStatus
    description: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PositionValueOut(BaseModel):
    position_id: uuid.UUID
    fair_value: Decimal
    current_prob: float
    implied_prob: float
    sigma: float
    time_remaining: float
    greeks: Optional[dict] = None
