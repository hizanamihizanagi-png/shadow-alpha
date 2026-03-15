"""
Admin Router - internal dashboard endpoints for wealth engine monitoring.
Uses RevenueLedgerService for accurate, real-time revenue tracking.
"""

from __future__ import annotations

from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.auth import get_admin_user
from app.models.position import Position, PositionStatus
from app.models.position_loan import PositionLoan, PositionLoanStatus
from app.models.shield import ShieldContract, ShieldStatus
from app.models.user import User
from app.models.vault import VaultDeposit, VaultDepositStatus
from app.services.float_engine import FloatEngineService
from app.services.revenue_ledger import RevenueLedgerService


router = APIRouter()


@router.get("/dashboard")
async def admin_dashboard(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
) -> dict:
    """Full admin dashboard - KPIs at a glance."""
    # Total users
    total_users = await db.scalar(select(func.count(User.id))) or 0

    # Active positions
    active_positions = await db.scalar(
        select(func.count(Position.id))
        .where(Position.status == PositionStatus.ACTIVE)
    ) or 0

    # Total AUM (vault)
    vault_aum = await db.scalar(
        select(func.coalesce(func.sum(VaultDeposit.amount), Decimal("0")))
        .where(VaultDeposit.status == VaultDepositStatus.ACTIVE)
    ) or Decimal("0")

    # Active shield contracts
    active_shields = await db.scalar(
        select(func.count(ShieldContract.id))
        .where(ShieldContract.status == ShieldStatus.ACTIVE)
    ) or 0

    # Active loans
    active_loans = await db.scalar(
        select(func.count(PositionLoan.id))
        .where(PositionLoan.status == PositionLoanStatus.ACTIVE)
    ) or 0

    # Total revenue
    total_revenue = await RevenueLedgerService.get_total_revenue(db)

    return {
        "total_users": total_users,
        "active_positions": active_positions,
        "vault_aum": str(vault_aum),
        "active_shield_contracts": active_shields,
        "active_loans": active_loans,
        "total_revenue": str(total_revenue),
    }


@router.get("/float-status")
async def float_status(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
) -> dict:
    """Get current Shadow Float deployment status."""
    total = await db.scalar(
        select(func.coalesce(func.sum(VaultDeposit.amount), Decimal("0")))
        .where(VaultDeposit.status == VaultDepositStatus.ACTIVE)
    ) or Decimal("0")
    return FloatEngineService.calculate_deployment(total)


@router.get("/prop-fund")
async def prop_fund_status(
    admin: User = Depends(get_admin_user),
) -> dict:
    """Get prop fund P&L and status."""
    return {
        "status": "active",
        "total_capital": "0.00",
        "active_positions": 0,
        "pnl": "0.00",
        "message": "Prop fund trading is stubbed - no live trades",
    }


@router.get("/shield-book")
async def shield_book(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
) -> dict:
    """Get active shield insurance book."""
    active_count = await db.scalar(
        select(func.count(ShieldContract.id))
        .where(ShieldContract.status == ShieldStatus.ACTIVE)
    ) or 0
    total_premium = await db.scalar(
        select(func.coalesce(func.sum(ShieldContract.premium_paid), Decimal("0")))
    ) or Decimal("0")
    return {
        "active_contracts": active_count,
        "total_premium_collected": str(total_premium),
    }


@router.get("/vault-aum")
async def vault_aum(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
) -> dict:
    """Get total vault assets under management."""
    total = await db.scalar(
        select(func.coalesce(func.sum(VaultDeposit.amount), Decimal("0")))
        .where(VaultDeposit.status == VaultDepositStatus.ACTIVE)
    ) or Decimal("0")
    return {
        "total_aum": str(total),
        "performance_fee_rate": "35%",
    }


@router.get("/revenue-streams")
async def revenue_streams(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
) -> dict:
    """Revenue breakdown from the master revenue ledger (all 10+ mechanisms)."""
    streams = await RevenueLedgerService.get_stream_summary(db)
    total = await RevenueLedgerService.get_total_revenue(db)
    return {
        "mechanisms": [
            {
                "name": s["mechanism"].value if hasattr(s["mechanism"], "value") else str(s["mechanism"]),
                "revenue": str(s["total_amount"]),
                "count": s["count"],
            }
            for s in streams
        ],
        "total_revenue": str(total),
    }


@router.get("/revenue-recent")
async def recent_revenue(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user),
) -> dict:
    """Get the most recent revenue events."""
    events = await RevenueLedgerService.get_recent(db, limit=50)
    return {
        "count": len(events),
        "events": [
            {
                "id": str(e.id),
                "mechanism": e.mechanism.value,
                "amount": str(e.amount),
                "description": e.description,
                "reference_id": e.reference_id,
                "created_at": e.created_at.isoformat() if e.created_at else None,
            }
            for e in events
        ],
    }

