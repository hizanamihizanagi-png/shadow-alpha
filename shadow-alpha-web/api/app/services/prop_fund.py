"""
Prop Fund — Anti-Portfolio trading signals (stub).
Does NOT execute real trades. Generates signals only.
"""

from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_classifier import UserClassifierService

import structlog

logger = structlog.get_logger()


class PropFundService:
    """Anti-Portfolio prop trading — inverse Squares, copy Sharps."""

    MAX_POSITION_SIZE = Decimal("100000.00")
    DRAWDOWN_LIMIT_PCT = Decimal("5.00")

    @classmethod
    async def generate_signals(
        cls,
        db: AsyncSession,
        user_ids: list[uuid.UUID],
    ) -> list[dict]:
        """Generate trading signals based on user classifications.

        - Sharp users → copy their trades externally
        - Square users → inverse their trades externally
        """
        signals = []
        for uid in user_ids:
            classification = await UserClassifierService.classify_user(db, uid)
            if not classification.get("actionable"):
                continue

            if classification["classification"] == "sharp":
                signals.append({
                    "user_id": str(uid),
                    "signal_type": "copy",
                    "direction": "same",
                    "confidence": classification["confidence"],
                    "reason": f"Sharp user: {classification['win_rate']:.1%} win rate, {classification['roi']:.1%} ROI",
                })
            elif classification["classification"] == "square":
                signals.append({
                    "user_id": str(uid),
                    "signal_type": "inverse",
                    "direction": "opposite",
                    "confidence": classification["confidence"],
                    "reason": f"Square user: {classification['win_rate']:.1%} win rate, {classification['roi']:.1%} ROI",
                })

        logger.info("prop_fund.signals_generated", count=len(signals))
        return signals

    @classmethod
    async def execute_trade(cls, signal: dict) -> dict:
        """Execute a prop fund trade (STUB — logs only, no real execution)."""
        logger.info("prop_fund.trade_executed_stub", signal=signal)
        return {
            "status": "simulated",
            "signal": signal,
            "message": "Prop fund trade execution is stubbed — no real external API calls",
        }
