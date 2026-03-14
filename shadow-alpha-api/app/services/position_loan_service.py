"""
Position Loan Service — Lombard lending against live positions.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import ROUND_HALF_EVEN, Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.error_handler import NotFoundError, ValidationError
from app.models.position import Position, PositionStatus
from app.models.position_loan import PositionLoan, PositionLoanStatus
from app.models.wealth_engine import RevenueMechanism
from app.services.pricing_engine import PricingEngineService
from app.services.revenue_ledger import RevenueLedgerService


class PositionLoanService:
    """Lombard-style lending: borrow against position value."""

    MAX_LTV = Decimal("60.00")   # Max 60% of position value
    FEE_PCT = Decimal("1.50")    # 1.5% flat fee

    @classmethod
    async def calculate_loan(
        cls,
        db: AsyncSession,
        position_id: uuid.UUID,
    ) -> dict:
        """Calculate maximum loan for a position."""
        position = await cls._get_position(db, position_id)

        # Use Black-Scholes fair value
        implied_prob = PricingEngineService.odds_to_implied_prob(float(position.odds))
        current_prob = position.current_prob or implied_prob
        time_remaining = position.time_remaining or 0.5

        fair_value = PricingEngineService.price_position(
            current_prob, implied_prob,
            PricingEngineService.DEFAULT_SIGMA,
            time_remaining, position.max_payout,
        )

        max_loan = (fair_value * cls.MAX_LTV / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )
        fee = (max_loan * cls.FEE_PCT / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )

        return {
            "position_id": position_id,
            "fair_value": fair_value,
            "max_loan": max_loan,
            "max_ltv_pct": cls.MAX_LTV,
            "fee_pct": cls.FEE_PCT,
            "fee_amount": fee,
            "net_disbursement": max_loan - fee,
        }

    @classmethod
    async def disburse_loan(
        cls,
        db: AsyncSession,
        position_id: uuid.UUID,
        user_id: uuid.UUID,
        loan_pct: Decimal = Decimal("60.00"),
    ) -> PositionLoan:
        """Disburse a loan against a position."""
        position = await cls._get_position(db, position_id)

        if position.user_id != user_id:
            raise ValidationError("You can only borrow against your own positions")
        if position.status != PositionStatus.ACTIVE:
            raise ValidationError("Position must be active to borrow against")

        # Check no existing loan
        existing = await db.execute(
            select(PositionLoan).where(
                PositionLoan.position_id == position_id,
                PositionLoan.status == PositionLoanStatus.ACTIVE,
            )
        )
        if existing.scalar_one_or_none():
            raise ValidationError("Position already has an active loan")

        # Calculate
        loan_pct = min(loan_pct, cls.MAX_LTV)
        implied_prob = PricingEngineService.odds_to_implied_prob(float(position.odds))
        current_prob = position.current_prob or implied_prob
        time_remaining = position.time_remaining or 0.5

        fair_value = PricingEngineService.price_position(
            current_prob, implied_prob,
            PricingEngineService.DEFAULT_SIGMA,
            time_remaining, position.max_payout,
        )

        loan_amount = (fair_value * loan_pct / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )
        fee = (loan_amount * cls.FEE_PCT / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )

        loan = PositionLoan(
            position_id=position_id,
            user_id=user_id,
            loan_amount=loan_amount,
            collateral_value=fair_value,
            fee=fee,
            status=PositionLoanStatus.ACTIVE,
        )
        db.add(loan)

        # Lock position as collateral
        position.status = PositionStatus.LOCKED

        # Log fee to revenue ledger
        await RevenueLedgerService.record(
            db,
            mechanism=RevenueMechanism.POSITION_LOAN_FEE,
            amount=fee,
            description=f"Loan fee {cls.FEE_PCT}% on {loan_amount} FCFA",
            reference_id=str(position_id),
        )

        await db.flush()
        return loan

    @classmethod
    async def auto_settle(
        cls,
        db: AsyncSession,
        loan_id: uuid.UUID,
    ) -> PositionLoan:
        """Auto-settle a loan when its collateral position resolves."""
        result = await db.execute(
            select(PositionLoan).where(PositionLoan.id == loan_id)
        )
        loan = result.scalar_one_or_none()
        if not loan:
            raise NotFoundError("PositionLoan", str(loan_id))
        if loan.status != PositionLoanStatus.ACTIVE:
            raise ValidationError("Loan is not active")

        # Check position status
        pos_result = await db.execute(
            select(Position).where(Position.id == loan.position_id)
        )
        position = pos_result.scalar_one()

        if position.status == PositionStatus.WON:
            # Auto-repay from winnings
            loan.status = PositionLoanStatus.SETTLED
        elif position.status == PositionStatus.LOST:
            # Collateral seized
            loan.status = PositionLoanStatus.LIQUIDATED
        else:
            raise ValidationError("Position must be resolved (won/lost) to auto-settle")

        loan.repaid_at = datetime.now(timezone.utc)
        await db.flush()
        return loan

    @classmethod
    async def get_user_loans(
        cls,
        db: AsyncSession,
        user_id: uuid.UUID,
    ) -> list[PositionLoan]:
        """Get all loans for a user."""
        result = await db.execute(
            select(PositionLoan)
            .where(PositionLoan.user_id == user_id)
            .order_by(PositionLoan.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def _get_position(db: AsyncSession, position_id: uuid.UUID) -> Position:
        """Get position or raise NotFoundError."""
        result = await db.execute(
            select(Position).where(Position.id == position_id)
        )
        position = result.scalar_one_or_none()
        if not position:
            raise NotFoundError("Position", str(position_id))
        return position
