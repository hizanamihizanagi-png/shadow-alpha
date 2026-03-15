"""
Credit Scorer - compute credit scores from user activity.
"""

from __future__ import annotations

import uuid
from decimal import ROUND_HALF_EVEN, Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.loan import Loan, LoanStatus
from app.models.position import Position
from app.models.tontine import TontineContribution


class CreditScorerService:
    """Alternative credit scoring based on platform activity."""

    MAX_SCORE = 1000
    BASE_SCORE = 300

    @classmethod
    async def compute_score(cls, db: AsyncSession, user_id: uuid.UUID) -> dict:
        """Compute a credit score (0-1000) for the user."""
        score = cls.BASE_SCORE

        # Factor 1: Position activity (max +200)
        pos_count = await db.scalar(
            select(func.count(Position.id)).where(Position.user_id == user_id)
        ) or 0
        score += min(pos_count * 10, 200)

        # Factor 2: Tontine contributions (max +200)
        contrib_count = await db.scalar(
            select(func.count(TontineContribution.id)).where(TontineContribution.user_id == user_id)
        ) or 0
        score += min(contrib_count * 15, 200)

        # Factor 3: Loan repayment history (max +200)
        repaid = await db.scalar(
            select(func.count(Loan.id)).where(
                Loan.user_id == user_id, Loan.status == LoanStatus.REPAID
            )
        ) or 0
        defaulted = await db.scalar(
            select(func.count(Loan.id)).where(
                Loan.user_id == user_id, Loan.status == LoanStatus.DEFAULTED
            )
        ) or 0
        if repaid > 0:
            repay_ratio = repaid / max(repaid + defaulted, 1)
            score += int(repay_ratio * 200)

        # Factor 4: Account age (max +100) - placeholder
        score += 50  # Base age bonus

        score = min(score, cls.MAX_SCORE)

        # Risk tier
        if score >= 800:
            tier = "A"
        elif score >= 600:
            tier = "B"
        elif score >= 400:
            tier = "C"
        else:
            tier = "D"

        return {
            "score": score,
            "tier": tier,
            "max_loan_amount": cls._max_loan(score),
            "interest_rate": cls._interest_rate(tier),
        }

    @staticmethod
    def _max_loan(score: int) -> Decimal:
        """Max loan amount based on score."""
        if score >= 800:
            return Decimal("500000.00")
        elif score >= 600:
            return Decimal("200000.00")
        elif score >= 400:
            return Decimal("50000.00")
        else:
            return Decimal("10000.00")

    @staticmethod
    def _interest_rate(tier: str) -> Decimal:
        """Monthly interest rate by tier."""
        rates = {"A": Decimal("1.50"), "B": Decimal("3.00"), "C": Decimal("5.00"), "D": Decimal("8.00")}
        return rates.get(tier, Decimal("8.00"))

    @classmethod
    async def check_eligibility(cls, db: AsyncSession, user_id: uuid.UUID, amount: Decimal) -> dict:
        """Check if a user is eligible for a loan."""
        score_data = await cls.compute_score(db, user_id)
        eligible = amount <= score_data["max_loan_amount"]
        return {
            **score_data,
            "requested_amount": amount,
            "eligible": eligible,
            "reason": None if eligible else f"Max loan for tier {score_data['tier']} is {score_data['max_loan_amount']} FCFA",
        }

