"""
Tontine models and schemas — groups, members, contributions.
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


class CycleType(str, enum.Enum):
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


class TontineStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class MemberRole(str, enum.Enum):
    CREATOR = "creator"
    MEMBER = "member"


class TontineGroup(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "tontine_groups"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    creator_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False,
    )
    cycle_type: Mapped[CycleType] = mapped_column(Enum(CycleType), nullable=False)
    target_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    current_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("0.00"))
    status: Mapped[TontineStatus] = mapped_column(
        Enum(TontineStatus), default=TontineStatus.ACTIVE, nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    members = relationship("TontineMember", back_populates="group", lazy="selectin")


class TontineMember(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "tontine_members"

    group_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("tontine_groups.id"), nullable=False, index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, index=True,
    )
    role: Mapped[MemberRole] = mapped_column(Enum(MemberRole), default=MemberRole.MEMBER)
    contribution_total: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("0.00"))

    group = relationship("TontineGroup", back_populates="members")


class TontineContribution(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "tontine_contributions"

    group_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("tontine_groups.id"), nullable=False, index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)


# ── Pydantic Schemas ──────────────────────────────────────────────────────
class TontineGroupCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    cycle_type: CycleType
    target_amount: Decimal = Field(..., gt=Decimal("0"))
    description: Optional[str] = None


class TontineGroupOut(BaseModel):
    id: uuid.UUID
    name: str
    creator_id: uuid.UUID
    cycle_type: CycleType
    target_amount: Decimal
    current_amount: Decimal
    status: TontineStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class TontineJoin(BaseModel):
    group_id: uuid.UUID


class ContributionCreate(BaseModel):
    group_id: uuid.UUID
    amount: Decimal = Field(..., gt=Decimal("0"))


class ContributionOut(BaseModel):
    id: uuid.UUID
    group_id: uuid.UUID
    user_id: uuid.UUID
    amount: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}
