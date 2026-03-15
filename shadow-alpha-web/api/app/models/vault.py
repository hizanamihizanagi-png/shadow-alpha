"""
Shadow Vault model and schemas - yield fund deposits and performance tracking.
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


class VaultDepositStatus(str, enum.Enum):
    ACTIVE = "active"
    WITHDRAWN = "withdrawn"


class VaultDeposit(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "vault_deposits"

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    status: Mapped[VaultDepositStatus] = mapped_column(
        Enum(VaultDepositStatus), default=VaultDepositStatus.ACTIVE, nullable=False,
    )
    withdrawn_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class VaultYield(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "vault_yields"

    cycle_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    gross_yield: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    performance_fee: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    net_yield: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    strategy_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)


# ── Pydantic Schemas ──────────────────────────────────────────────────────
class VaultDepositCreate(BaseModel):
    amount: Decimal = Field(..., gt=Decimal("0"))


class VaultDepositOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    amount: Decimal
    status: VaultDepositStatus
    created_at: datetime
    withdrawn_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class VaultWithdraw(BaseModel):
    deposit_id: uuid.UUID


class VaultPerformanceOut(BaseModel):
    total_deposited: Decimal
    current_value: Decimal
    gross_yield: Decimal
    performance_fee: Decimal
    net_yield: Decimal
    apy_estimate: float
    net_apy: float
    strategy: Optional[str] = None
    deposits: list[VaultDepositOut] = []

