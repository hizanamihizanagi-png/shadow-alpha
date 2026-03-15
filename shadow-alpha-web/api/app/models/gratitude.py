"""
Gratitude (tip) model and schemas - voluntary tips on wins.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, GUID, TimestampMixin, UUIDPrimaryKeyMixin


class GratitudeTip(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "gratitude_tips"

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, index=True,
    )
    win_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    tip_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    tip_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)


# ── Pydantic Schemas ──────────────────────────────────────────────────────
class GratitudeTipCreate(BaseModel):
    win_amount: Decimal = Field(..., gt=Decimal("0"))
    tip_pct: Decimal = Field(..., ge=Decimal("1"), le=Decimal("50"))


class GratitudeTipOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    win_amount: Decimal
    tip_pct: Decimal
    tip_amount: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}


class SupporterOut(BaseModel):
    user_id: uuid.UUID
    display_name: str
    total_tips: Decimal
    tip_count: int
    badge: Optional[str] = None

