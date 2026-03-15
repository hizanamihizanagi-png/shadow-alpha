"""
Shield Engine - insurance pricing, activation, and claims processing.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import ROUND_HALF_EVEN, Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.error_handler import NotFoundError, ValidationError
from app.models.position import Position, PositionStatus
from app.models.shield import ShieldClaim, ShieldContract, ShieldStatus
from app.models.wealth_engine import RevenueMechanism
from app.services.pricing_engine import PricingEngineService
from app.services.revenue_ledger import RevenueLedgerService


class ShieldEngineService:
    """Insurance pricing and claim management for position protection."""

    MIN_PREMIUM_PCT = Decimal("2.00")
    MAX_PREMIUM_PCT = Decimal("5.00")
    PROFIT_MARGIN = Decimal("1.15")  # 15% margin on top of actuarial price
    DEFAULT_COVERAGE = Decimal("70.00")

    @classmethod
    def calculate_premium(
        cls,
        stake: Decimal,
        loss_probability: float,
        coverage_pct: Decimal,
    ) -> dict:
        """Calculate insurance premium using actuarial pricing.

        premium = stake x loss_prob x coverage% x profit_margin
        Clamped between 2-5% of stake.
        """
        actuarial_price = float(stake) * loss_probability * float(coverage_pct) / 100.0
        premium_with_margin = actuarial_price * float(cls.PROFIT_MARGIN)

        # Clamp
        min_premium = float(stake * cls.MIN_PREMIUM_PCT / Decimal("100"))
        max_premium = float(stake * cls.MAX_PREMIUM_PCT / Decimal("100"))
        premium = max(min_premium, min(max_premium, premium_with_margin))

        premium_dec = Decimal(str(premium)).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        estimated_payout = (stake * coverage_pct / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )

        return {
            "premium": premium_dec,
            "coverage_pct": coverage_pct,
            "estimated_payout": estimated_payout,
            "loss_probability": round(loss_probability, 4),
            "premium_pct_of_stake": (premium_dec / stake * Decimal("100")).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_EVEN
            ) if stake > 0 else Decimal("0.00"),
        }

    @classmethod
    async def activate_shield(
        cls,
        db: AsyncSession,
        position_id: uuid.UUID,
        user_id: uuid.UUID,
        coverage_pct: Decimal = Decimal("70.00"),
    ) -> ShieldContract:
        """Activate shield insurance on a position."""
        # Verify position
        result = await db.execute(
            select(Position).where(Position.id == position_id)
        )
        position = result.scalar_one_or_none()
        if not position:
            raise NotFoundError("Position", str(position_id))
        if position.user_id != user_id:
            raise ValidationError("You can only insure your own positions")
        if position.status != PositionStatus.ACTIVE:
            raise ValidationError("Position must be active to insure")

        # Check no existing active shield
        existing = await db.execute(
            select(ShieldContract).where(
                ShieldContract.position_id == position_id,
                ShieldContract.status == ShieldStatus.ACTIVE,
            )
        )
        if existing.scalar_one_or_none():
            raise ValidationError("Position already has active shield insurance")

        # Calculate premium
        implied_prob = PricingEngineService.odds_to_implied_prob(float(position.odds))
        loss_probability = 1.0 - implied_prob
        pricing = cls.calculate_premium(position.stake, loss_probability, coverage_pct)

        contract = ShieldContract(
            position_id=position_id,
            user_id=user_id,
            premium_paid=pricing["premium"],
            coverage_pct=coverage_pct,
            status=ShieldStatus.ACTIVE,
        )
        db.add(contract)

        # Log premium to revenue ledger
        await RevenueLedgerService.record(
            db,
            mechanism=RevenueMechanism.SHIELD_PREMIUM,
            amount=pricing["premium"],
            description=f"Shield premium {coverage_pct}% coverage on position",
            reference_id=str(position_id),
        )

        await db.flush()
        return contract

    @classmethod
    async def process_claim(
        cls,
        db: AsyncSession,
        contract_id: uuid.UUID,
    ) -> ShieldClaim:
        """Process a shield insurance claim on a lost position."""
        result = await db.execute(
            select(ShieldContract).where(ShieldContract.id == contract_id)
        )
        contract = result.scalar_one_or_none()
        if not contract:
            raise NotFoundError("ShieldContract", str(contract_id))
        if contract.status != ShieldStatus.ACTIVE:
            raise ValidationError("Contract is not active")

        # Get position
        pos_result = await db.execute(
            select(Position).where(Position.id == contract.position_id)
        )
        position = pos_result.scalar_one()

        # Calculate payout: coverage% of original stake
        payout = (position.stake * contract.coverage_pct / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )

        claim = ShieldClaim(
            contract_id=contract_id,
            payout_amount=payout,
            claimed_at=datetime.now(timezone.utc),
        )
        db.add(claim)

        contract.status = ShieldStatus.CLAIMED
        await db.flush()
        return claim

