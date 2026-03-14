"""
Position Loan (Lombard) model and schemas — collateralized position loans.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, GUID, TimestampMixin, UUIDPrimaryKeyMixin


class PositionLoanStatus(str, enum.Enum):
    ACTIVE = "active"
    REPAID = "repaid"
    SETTLED = "settled"       # Auto-settled on position win
    LIQUIDATED = "liquidated" # Position lost, collateral seized


class PositionLoan(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "position_loans"

    position_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("positions.id"), nullable=False, index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, index=True,
    )
    loan_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    collateral_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    fee: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    status: Mapped[PositionLoanStatus] = mapped_column(
        Enum(PositionLoanStatus), default=PositionLoanStatus.ACTIVE, nullable=False,
    )
    repaid_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


# ── Pydantic Schemas ──────────────────────────────────────────────────────
class PositionLoanCreate(BaseModel):
    position_id: uuid.UUID
    loan_pct: Decimal = Field(
        default=Decimal("60.00"),
        ge=Decimal("10"),
        le=Decimal("60"),
        description="Percentage of position value to borrow (max 60%)",
    )


class PositionLoanOut(BaseModel):
    id: uuid.UUID
    position_id: uuid.UUID
    user_id: uuid.UUID
    loan_amount: Decimal
    collateral_value: Decimal
    fee: Decimal
    status: PositionLoanStatus
    created_at: datetime
    repaid_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
