"""
Gratitude Service — voluntary tips, supporters leaderboard, and badge management.
"""

from __future__ import annotations

import uuid
from decimal import ROUND_HALF_EVEN, Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gratitude import GratitudeTip
from app.models.user import User
from app.models.wealth_engine import RevenueMechanism
from app.services.revenue_ledger import RevenueLedgerService


class GratitudeService:
    """Manages the Gratitude Tax — voluntary tip system."""

    @classmethod
    async def record_tip(
        cls,
        db: AsyncSession,
        user_id: uuid.UUID,
        win_amount: Decimal,
        tip_pct: Decimal,
    ) -> GratitudeTip:
        """Record a voluntary tip from a winning user."""
        tip_amount = (win_amount * tip_pct / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )
        tip = GratitudeTip(
            user_id=user_id,
            win_amount=win_amount,
            tip_pct=tip_pct,
            tip_amount=tip_amount,
        )
        db.add(tip)

        # Log to revenue ledger
        await RevenueLedgerService.record(
            db,
            mechanism=RevenueMechanism.GRATITUDE_TIP,
            amount=tip_amount,
            description=f"Tip {tip_pct}% on win of {win_amount} FCFA",
            reference_id=str(user_id),
        )

        await db.flush()
        return tip

    @classmethod
    async def get_supporters_leaderboard(
        cls,
        db: AsyncSession,
        limit: int = 20,
    ) -> list[dict]:
        """Get top supporters ranked by total tips."""
        result = await db.execute(
            select(
                GratitudeTip.user_id,
                User.display_name,
                func.sum(GratitudeTip.tip_amount).label("total_tips"),
                func.count(GratitudeTip.id).label("tip_count"),
            )
            .join(User, User.id == GratitudeTip.user_id)
            .group_by(GratitudeTip.user_id, User.display_name)
            .order_by(func.sum(GratitudeTip.tip_amount).desc())
            .limit(limit)
        )
        supporters = []
        for row in result.all():
            badge = cls._assign_badge(row.total_tips)
            supporters.append({
                "user_id": row.user_id,
                "display_name": row.display_name,
                "total_tips": row.total_tips or Decimal("0.00"),
                "tip_count": row.tip_count or 0,
                "badge": badge,
            })
        return supporters

    @classmethod
    async def get_user_tips(
        cls,
        db: AsyncSession,
        user_id: uuid.UUID,
    ) -> list[GratitudeTip]:
        """Get all tips for a user."""
        result = await db.execute(
            select(GratitudeTip)
            .where(GratitudeTip.user_id == user_id)
            .order_by(GratitudeTip.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    def _assign_badge(total_tips: Decimal) -> str:
        """Assign badge based on lifetime tip amount (FCFA)."""
        total = float(total_tips or 0)
        if total >= 500_000:
            return "diamond"
        elif total >= 100_000:
            return "gold"
        elif total >= 25_000:
            return "silver"
        elif total >= 5_000:
            return "bronze"
        return "supporter"
