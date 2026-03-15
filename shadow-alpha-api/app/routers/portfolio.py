"""
Portfolio Router - summary, P&L, history.
"""

from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.auth import get_current_user
from app.models.position import Position, PositionStatus
from app.models.user import User

router = APIRouter()


@router.get("/summary")
async def portfolio_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Get portfolio summary - total value, position count, tier breakdown."""
    positions = await db.execute(
        select(Position).where(Position.user_id == current_user.id)
    )
    all_positions = positions.scalars().all()

    total_value = sum((p.current_value for p in all_positions), Decimal("0.00"))
    total_stake = sum((p.stake for p in all_positions), Decimal("0.00"))
    active = [p for p in all_positions if p.status == PositionStatus.ACTIVE]
    won = [p for p in all_positions if p.status == PositionStatus.WON]
    lost = [p for p in all_positions if p.status == PositionStatus.LOST]

    return {
        "total_value": str(total_value),
        "total_invested": str(total_stake),
        "unrealized_pnl": str(total_value - total_stake),
        "position_count": len(all_positions),
        "active_count": len(active),
        "won_count": len(won),
        "lost_count": len(lost),
        "win_rate": round(len(won) / max(len(won) + len(lost), 1), 4),
    }


@router.get("/pnl")
async def portfolio_pnl(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Get detailed P&L breakdown."""
    positions = await db.execute(
        select(Position).where(Position.user_id == current_user.id)
    )
    all_positions = positions.scalars().all()

    realized_pnl = Decimal("0.00")
    for p in all_positions:
        if p.status == PositionStatus.WON:
            realized_pnl += p.max_payout - p.stake
        elif p.status == PositionStatus.LOST:
            realized_pnl -= p.stake

    unrealized_pnl = sum(
        (p.current_value - p.stake)
        for p in all_positions
        if p.status == PositionStatus.ACTIVE
    )

    return {
        "realized_pnl": str(realized_pnl),
        "unrealized_pnl": str(unrealized_pnl),
        "total_pnl": str(realized_pnl + unrealized_pnl),
        "best_trade": str(max((p.max_payout - p.stake for p in all_positions if p.status == PositionStatus.WON), default=Decimal("0.00"))),
        "worst_trade": str(min((-p.stake for p in all_positions if p.status == PositionStatus.LOST), default=Decimal("0.00"))),
    }


@router.get("/history")
async def portfolio_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Get position history (settled positions)."""
    result = await db.execute(
        select(Position)
        .where(
            Position.user_id == current_user.id,
            Position.status.in_([PositionStatus.WON, PositionStatus.LOST, PositionStatus.SOLD]),
        )
        .order_by(Position.updated_at.desc())
        .limit(50)
    )
    positions = result.scalars().all()

    return {
        "count": len(positions),
        "positions": [
            {
                "id": str(p.id),
                "teams": p.teams,
                "stake": str(p.stake),
                "max_payout": str(p.max_payout),
                "status": p.status.value,
                "pnl": str(p.max_payout - p.stake if p.status == PositionStatus.WON else -p.stake),
                "created_at": p.created_at.isoformat(),
                "updated_at": p.updated_at.isoformat(),
            }
            for p in positions
        ],
    }

