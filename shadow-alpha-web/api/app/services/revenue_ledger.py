"""
Revenue Ledger Service - centralized revenue tracking across all 10 mechanisms.

Every fee, tip, spread, premium, or interest captured is logged here.
This is the single source of truth for Shadow Alpha's revenue.
"""

from __future__ import annotations

import uuid
from decimal import ROUND_HALF_EVEN, Decimal
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wealth_engine import RevenueLedger, RevenueMechanism


class RevenueLedgerService:
    """Unified revenue tracking for all wealth engine mechanisms."""

    @classmethod
    async def record(
        cls,
        db: AsyncSession,
        mechanism: RevenueMechanism,
        amount: Decimal,
        description: Optional[str] = None,
        reference_id: Optional[str] = None,
    ) -> RevenueLedger:
        """Record a revenue event to the master ledger."""
        amount = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        entry = RevenueLedger(
            mechanism=mechanism,
            amount=amount,
            description=description,
            reference_id=reference_id,
        )
        db.add(entry)
        await db.flush()
        return entry

    @classmethod
    async def get_stream_summary(cls, db: AsyncSession) -> list[dict]:
        """Get revenue breakdown by mechanism."""
        result = await db.execute(
            select(
                RevenueLedger.mechanism,
                func.sum(RevenueLedger.amount).label("total"),
                func.count(RevenueLedger.id).label("count"),
            )
            .group_by(RevenueLedger.mechanism)
            .order_by(func.sum(RevenueLedger.amount).desc())
        )
        return [
            {
                "mechanism": row.mechanism,
                "total_amount": row.total or Decimal("0.00"),
                "count": row.count or 0,
            }
            for row in result.all()
        ]

    @classmethod
    async def get_total_revenue(cls, db: AsyncSession) -> Decimal:
        """Get total revenue across all mechanisms."""
        total = await db.scalar(
            select(func.coalesce(func.sum(RevenueLedger.amount), Decimal("0.00")))
        )
        return total or Decimal("0.00")

    @classmethod
    async def get_recent(cls, db: AsyncSession, limit: int = 50) -> list[RevenueLedger]:
        """Get most recent revenue events."""
        result = await db.execute(
            select(RevenueLedger)
            .order_by(RevenueLedger.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

