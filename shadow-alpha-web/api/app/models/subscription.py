"""
Subscription model and schemas.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, GUID, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.user import SubscriptionTier


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    TRIAL = "trial"


class Subscription(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "subscriptions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, index=True,
    )
    plan: Mapped[SubscriptionTier] = mapped_column(
        Enum(SubscriptionTier), default=SubscriptionTier.FREE, nullable=False,
    )
    status: Mapped[SubscriptionStatus] = mapped_column(
        Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False,
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


# ── Pydantic Schemas ──────────────────────────────────────────────────────
class SubscriptionUpgrade(BaseModel):
    plan: SubscriptionTier


class SubscriptionOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    plan: SubscriptionTier
    status: SubscriptionStatus
    started_at: datetime
    expires_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PlanInfo(BaseModel):
    name: SubscriptionTier
    price_fcfa: int
    features: list[str]
