"""
Order and Trade models and schemas.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, GUID, TimestampMixin, UUIDPrimaryKeyMixin


# ── Enums ─────────────────────────────────────────────────────────────────
class OrderType(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"


class OrderStatus(str, enum.Enum):
    OPEN = "open"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


# ── SQLAlchemy Models ─────────────────────────────────────────────────────
class Order(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "orders"

    position_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("positions.id"), nullable=False, index=True,
    )
    seller_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, index=True,
    )
    buyer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=True,
    )
    order_type: Mapped[OrderType] = mapped_column(Enum(OrderType), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.OPEN, nullable=False,
    )


class Trade(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "trades"

    order_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("orders.id"), nullable=False, index=True,
    )
    buyer_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False,
    )
    seller_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False,
    )
    price: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    fee: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("0.00"))


# ── Pydantic Schemas ──────────────────────────────────────────────────────
class OrderCreate(BaseModel):
    position_id: uuid.UUID
    order_type: OrderType
    price: Decimal = Field(..., gt=Decimal("0"))


class OrderOut(BaseModel):
    id: uuid.UUID
    position_id: uuid.UUID
    seller_id: uuid.UUID
    buyer_id: Optional[uuid.UUID] = None
    order_type: OrderType
    price: Decimal
    status: OrderStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class TradeOut(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    buyer_id: uuid.UUID
    seller_id: uuid.UUID
    price: Decimal
    fee: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}
