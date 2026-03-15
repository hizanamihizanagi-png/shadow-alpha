"""
Models package - imports all models so SQLAlchemy registers them with Base.metadata.

This is imported by session.create_all_tables() and alembic env.py to ensure
all tables are discovered during migration generation and table creation.
"""

# Core models
from app.models.user import User  # noqa: F401
from app.models.position import Position  # noqa: F401
from app.models.order import Order, Trade  # noqa: F401
from app.models.tontine import TontineGroup, TontineMember, TontineContribution  # noqa: F401
from app.models.loan import Loan  # noqa: F401
from app.models.subscription import Subscription  # noqa: F401

# Shadow Wealth Engine models
from app.models.vault import VaultDeposit, VaultYield  # noqa: F401
from app.models.shield import ShieldContract, ShieldClaim  # noqa: F401
from app.models.gratitude import GratitudeTip  # noqa: F401
from app.models.position_loan import PositionLoan  # noqa: F401
from app.models.wealth_engine import (  # noqa: F401
    FloatDeployment,
    PropFundTrade,
    InstantCashout,
    UserClassification,
    APIKey,
    PromoCode,
    Referral,
    OracleQuery,
    RevenueLedger,
)

__all__ = [
    # Core
    "User",
    "Position",
    "Order",
    "Trade",
    "TontineGroup",
    "TontineMember",
    "TontineContribution",
    "Loan",
    "Subscription",
    # Wealth Engine
    "VaultDeposit",
    "VaultYield",
    "ShieldContract",
    "ShieldClaim",
    "GratitudeTip",
    "PositionLoan",
    "FloatDeployment",
    "PropFundTrade",
    "InstantCashout",
    "UserClassification",
    "APIKey",
    "PromoCode",
    "Referral",
    "OracleQuery",
    "RevenueLedger",
]

