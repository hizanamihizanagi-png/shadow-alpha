"""
Shield Insurance model and schemas — position insurance contracts and claims.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, GUID, TimestampMixin, UUIDPrimaryKeyMixin


class ShieldStatus(str, enum.Enum):
    ACTIVE = "active"
    CLAIMED = "claimed"
    EXPIRED = "expired"
    VOID = "void"


class ShieldContract(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "shield_contracts"

    position_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("positions.id"), nullable=False, index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, index=True,
    )
    premium_paid: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    coverage_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    hedge_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[ShieldStatus] = mapped_column(
        Enum(ShieldStatus), default=ShieldStatus.ACTIVE, nullable=False,
    )


class ShieldClaim(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "shield_claims"

    contract_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("shield_contracts.id"), nullable=False, index=True,
    )
    payout_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    claimed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


# ── Pydantic Schemas ──────────────────────────────────────────────────────
class ShieldActivate(BaseModel):
    position_id: uuid.UUID
    coverage_pct: Decimal = Field(default=Decimal("70.00"), ge=Decimal("10"), le=Decimal("90"))


class ShieldContractOut(BaseModel):
    id: uuid.UUID
    position_id: uuid.UUID
    user_id: uuid.UUID
    premium_paid: Decimal
    coverage_pct: Decimal
    status: ShieldStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class ShieldQuoteOut(BaseModel):
    position_id: uuid.UUID
    premium: Decimal
    coverage_pct: Decimal
    estimated_payout: Decimal
    loss_probability: float


class ShieldClaimOut(BaseModel):
    id: uuid.UUID
    contract_id: uuid.UUID
    payout_amount: Decimal
    claimed_at: datetime

    model_config = {"from_attributes": True}
