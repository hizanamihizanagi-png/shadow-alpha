"""
User Classifier — Sharp/Square classification for the Anti-Portfolio.
"""

from __future__ import annotations

import uuid

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.position import Position, PositionStatus


class UserClassifierService:
    """Classify users as Sharp (top performers) or Square (average)."""

    MIN_POSITIONS = 10
    SHARP_WIN_RATE_THRESHOLD = 0.55
    SHARP_ROI_THRESHOLD = 0.10
    HIGH_CONFIDENCE_THRESHOLD = 0.85

    @classmethod
    async def classify_user(cls, db: AsyncSession, user_id: uuid.UUID) -> dict:
        """Classify a user as Sharp or Square based on their track record."""
        # Get position stats
        total = await db.scalar(
            select(func.count(Position.id)).where(Position.user_id == user_id)
        ) or 0

        if total < cls.MIN_POSITIONS:
            return {
                "classification": "insufficient_data",
                "confidence": 0.0,
                "reason": f"Need at least {cls.MIN_POSITIONS} positions, have {total}",
            }

        wins = await db.scalar(
            select(func.count(Position.id)).where(
                and_(Position.user_id == user_id, Position.status == PositionStatus.WON)
            )
        ) or 0

        losses = await db.scalar(
            select(func.count(Position.id)).where(
                and_(Position.user_id == user_id, Position.status == PositionStatus.LOST)
            )
        ) or 0

        settled = wins + losses
        if settled == 0:
            return {
                "classification": "insufficient_data",
                "confidence": 0.0,
                "reason": "No settled positions yet",
            }

        win_rate = wins / settled

        # Calculate ROI
        total_stake = await db.scalar(
            select(func.coalesce(func.sum(Position.stake), 0))
            .where(Position.user_id == user_id)
        ) or 0

        total_payout = await db.scalar(
            select(func.coalesce(func.sum(Position.max_payout), 0))
            .where(
                and_(Position.user_id == user_id, Position.status == PositionStatus.WON)
            )
        ) or 0

        roi = (float(total_payout) - float(total_stake)) / float(total_stake) if float(total_stake) > 0 else 0

        # Classification logic
        is_sharp = win_rate >= cls.SHARP_WIN_RATE_THRESHOLD and roi >= cls.SHARP_ROI_THRESHOLD

        # Confidence increases with more data
        data_confidence = min(settled / 50.0, 1.0)  # Max confidence at 50+ settled
        perf_confidence = abs(win_rate - 0.5) * 2.0  # Higher divergence = higher confidence
        confidence = round((data_confidence * 0.5 + perf_confidence * 0.5), 4)

        return {
            "classification": "sharp" if is_sharp else "square",
            "confidence": confidence,
            "win_rate": round(win_rate, 4),
            "roi": round(roi, 4),
            "total_positions": total,
            "settled_positions": settled,
            "actionable": confidence >= cls.HIGH_CONFIDENCE_THRESHOLD,
        }
