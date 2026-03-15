"""
Loan model and schemas - micro-credit for informal traders.
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


class LoanStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    REPAID = "repaid"
    DEFAULTED = "defaulted"


class Loan(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "loans"

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    interest_rate: Mapped[Decimal] = mapped_column(Numeric(8, 4), nullable=False)
    status: Mapped[LoanStatus] = mapped_column(
        Enum(LoanStatus), default=LoanStatus.PENDING, nullable=False,
    )
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    repaid_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


# ── Pydantic Schemas ──────────────────────────────────────────────────────
class LoanApply(BaseModel):
    amount: Decimal = Field(..., gt=Decimal("0"))


class LoanOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    amount: Decimal
    interest_rate: Decimal
    status: LoanStatus
    due_date: Optional[datetime] = None
    repaid_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class LoanRepay(BaseModel):
    loan_id: uuid.UUID
    amount: Decimal = Field(..., gt=Decimal("0"))

