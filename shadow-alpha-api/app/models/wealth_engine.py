"""
Wealth Engine models - Float Deployments, Prop Fund Trades, Instant Cashouts,
User Classifications, API Keys, Promo Codes, Oracle Queries, and Revenue Ledger.

These tables power the Shadow Wealth Engine (10 revenue mechanisms).
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, GUID, TimestampMixin, UUIDPrimaryKeyMixin


# ═══════════════════════════════════════════════════════════════════════════
# FLOAT DEPLOYMENTS (Mécanisme 1 - Shadow Float)
# ═══════════════════════════════════════════════════════════════════════════

class FloatDeployment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Tracks each 6-hour cycle of float deployment into yield protocols."""
    __tablename__ = "float_deployments"

    total_float: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    deployed_to: Mapped[str] = mapped_column(String(200), nullable=False)  # e.g. "DeFi/T-Bills"
    apy: Mapped[Decimal] = mapped_column(Numeric(8, 4), nullable=False)
    interest_accrued: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    cycle_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    cycle_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class FloatDeploymentOut(BaseModel):
    id: uuid.UUID
    total_float: Decimal
    deployed_to: str
    apy: Decimal
    interest_accrued: Decimal
    cycle_start: datetime
    cycle_end: datetime

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════════════════════════════════
# PROP FUND TRADES (Mécanisme 2 - Anti-Portfolio)
# ═══════════════════════════════════════════════════════════════════════════

class PropFundDirection(str, enum.Enum):
    COPY_SHARP = "copy_sharp"
    INVERSE_SQUARE = "inverse_square"


class PropFundTrade(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Internal prop fund trades based on Sharp/Square signals."""
    __tablename__ = "prop_fund_trades"

    signal_user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, index=True,
    )
    signal_type: Mapped[str] = mapped_column(String(20), nullable=False)  # "sharp" or "square"
    direction: Mapped[PropFundDirection] = mapped_column(
        Enum(PropFundDirection), nullable=False,
    )
    stake: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    pnl: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("0.00"))


class PropFundTradeOut(BaseModel):
    id: uuid.UUID
    signal_user_id: uuid.UUID
    signal_type: str
    direction: PropFundDirection
    stake: Decimal
    pnl: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════════════════════════════════
# INSTANT CASHOUTS (Mécanisme 3 - Market Making)
# ═══════════════════════════════════════════════════════════════════════════

class InstantCashoutStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REJECTED = "rejected"


class InstantCashout(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Records of instant cashout market-making transactions."""
    __tablename__ = "instant_cashouts"

    position_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("positions.id"), nullable=False, index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, index=True,
    )
    fair_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    offered_price: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    spread_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    status: Mapped[InstantCashoutStatus] = mapped_column(
        Enum(InstantCashoutStatus), default=InstantCashoutStatus.PENDING, nullable=False,
    )


class InstantCashoutCreate(BaseModel):
    position_id: uuid.UUID


class InstantCashoutOut(BaseModel):
    id: uuid.UUID
    position_id: uuid.UUID
    user_id: uuid.UUID
    fair_value: Decimal
    offered_price: Decimal
    spread_pct: Decimal
    status: InstantCashoutStatus
    created_at: datetime

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════════════════════════════════
# USER CLASSIFICATIONS (Sharp/Square for Anti-Portfolio)
# ═══════════════════════════════════════════════════════════════════════════

class UserClassificationType(str, enum.Enum):
    SHARP = "sharp"
    SQUARE = "square"
    NEUTRAL = "neutral"


class UserClassification(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Sharp/Square classification for the Anti-Portfolio prop fund."""
    __tablename__ = "user_classifications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, unique=True, index=True,
    )
    classification: Mapped[UserClassificationType] = mapped_column(
        Enum(UserClassificationType), nullable=False,
    )
    confidence: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)  # 0.0000-1.0000
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class UserClassificationOut(BaseModel):
    user_id: uuid.UUID
    classification: UserClassificationType
    confidence: Decimal
    last_updated: datetime

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════════════════════════════════
# API KEYS (Public API - "OpenAI for Betting")
# ═══════════════════════════════════════════════════════════════════════════

class APIKeyTier(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class APIKey(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """API keys for the public Shadow Alpha API."""
    __tablename__ = "api_keys"

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, index=True,
    )
    key_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    key_prefix: Mapped[str] = mapped_column(String(20), nullable=False)  # e.g. "sap_live_abc"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    tier: Mapped[APIKeyTier] = mapped_column(
        Enum(APIKeyTier), default=APIKeyTier.FREE, nullable=False,
    )
    usage_count: Mapped[int] = mapped_column(default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)


class APIKeyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class APIKeyOut(BaseModel):
    id: uuid.UUID
    key_prefix: str
    name: str
    tier: APIKeyTier
    usage_count: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class APIKeyCreated(BaseModel):
    """Returned only on creation - full key shown once."""
    id: uuid.UUID
    key: str  # Full key (sap_live_xxxx...) - only shown once
    name: str
    tier: APIKeyTier


# ═══════════════════════════════════════════════════════════════════════════
# PROMO CODES & REFERRALS
# ═══════════════════════════════════════════════════════════════════════════

class PromoCode(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Streamer promo codes for referral tracking."""
    __tablename__ = "promo_codes"

    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    creator_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False,
    )
    uses_remaining: Mapped[int] = mapped_column(default=50, nullable=False)
    commission_rate: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), default=Decimal("15.00"), nullable=False,
    )  # 15% of SA's transaction fee


class Referral(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Tracks referred users and their lifetime revenue contribution."""
    __tablename__ = "referrals"

    promo_code_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("promo_codes.id"), nullable=False, index=True,
    )
    referred_user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False, unique=True,
    )
    lifetime_revenue: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00"), nullable=False,
    )


# ═══════════════════════════════════════════════════════════════════════════
# ORACLE QUERIES (Mécanisme 4 - Shadow Oracle B2B)
# ═══════════════════════════════════════════════════════════════════════════

class OracleQuery(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Tracks B2B queries to the Shadow Oracle credit scoring API."""
    __tablename__ = "oracle_queries"

    institution_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    query_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "credit-score", "batch-score"
    credits_used: Mapped[int] = mapped_column(default=1, nullable=False)


# ═══════════════════════════════════════════════════════════════════════════
# REVENUE LEDGER (Master revenue tracking across all 10 mechanisms)
# ═══════════════════════════════════════════════════════════════════════════

class RevenueMechanism(str, enum.Enum):
    SUBSCRIPTION = "subscription"
    TRANSACTION_FEE = "transaction_fee"
    FLOAT_INTEREST = "float_interest"
    PROP_FUND = "prop_fund"
    MARKET_MAKING = "market_making"
    ORACLE_DATA = "oracle_data"
    PERFORMANCE_FEE = "performance_fee"
    SHIELD_PREMIUM = "shield_premium"
    YIELD_TRANCHE = "yield_tranche"
    EMBEDDED_FINANCE = "embedded_finance"
    GRATITUDE_TIP = "gratitude_tip"
    POSITION_LOAN_FEE = "position_loan_fee"


class RevenueLedger(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Master ledger tracking every revenue event across all mechanisms."""
    __tablename__ = "revenue_ledger"

    mechanism: Mapped[RevenueMechanism] = mapped_column(
        Enum(RevenueMechanism), nullable=False, index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reference_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)


class RevenueLedgerOut(BaseModel):
    id: uuid.UUID
    mechanism: RevenueMechanism
    amount: Decimal
    description: Optional[str] = None
    reference_id: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class RevenueStreamSummary(BaseModel):
    mechanism: RevenueMechanism
    total_amount: Decimal
    count: int

