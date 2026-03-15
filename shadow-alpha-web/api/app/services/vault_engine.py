"""
Vault Engine - Shadow Vault deposit/withdraw and performance fee management.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import ROUND_HALF_EVEN, Decimal

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.error_handler import NotFoundError, ValidationError
from app.models.vault import VaultDeposit, VaultDepositStatus, VaultYield
from app.services.yield_engine import YieldEngineService


class VaultEngineService:
    """Manages Shadow Vault - user deposits, yields, and performance fees."""

    @classmethod
    async def deposit(
        cls,
        db: AsyncSession,
        user_id: uuid.UUID,
        amount: Decimal,
    ) -> VaultDeposit:
        """Record a vault deposit."""
        deposit = VaultDeposit(
            user_id=user_id,
            amount=amount,
            status=VaultDepositStatus.ACTIVE,
        )
        db.add(deposit)
        await db.flush()
        return deposit

    @classmethod
    async def withdraw(
        cls,
        db: AsyncSession,
        deposit_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> VaultDeposit:
        """Withdraw a vault deposit."""
        result = await db.execute(
            select(VaultDeposit).where(VaultDeposit.id == deposit_id)
        )
        deposit = result.scalar_one_or_none()
        if not deposit:
            raise NotFoundError("VaultDeposit", str(deposit_id))
        if deposit.user_id != user_id:
            raise ValidationError("You can only withdraw your own deposits")
        if deposit.status != VaultDepositStatus.ACTIVE:
            raise ValidationError("Deposit has already been withdrawn")

        deposit.status = VaultDepositStatus.WITHDRAWN
        deposit.withdrawn_at = datetime.now(timezone.utc)
        await db.flush()
        return deposit

    @classmethod
    async def get_performance(
        cls,
        db: AsyncSession,
        user_id: uuid.UUID,
    ) -> dict:
        """Get vault performance for a user."""
        # Total active deposits
        total = await db.scalar(
            select(func.coalesce(func.sum(VaultDeposit.amount), Decimal("0.00")))
            .where(
                and_(
                    VaultDeposit.user_id == user_id,
                    VaultDeposit.status == VaultDepositStatus.ACTIVE,
                )
            )
        ) or Decimal("0.00")

        # Calculate projected yield
        yield_data = YieldEngineService.calculate_monthly_yield(total)
        current_value = (total + yield_data["net_yield"]).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )

        deposits_result = await db.execute(
            select(VaultDeposit)
            .where(VaultDeposit.user_id == user_id)
            .order_by(VaultDeposit.created_at.desc())
        )
        deposits = list(deposits_result.scalars().all())

        return {
            "total_deposited": total,
            "current_value": current_value,
            "gross_yield": yield_data["gross_yield"],
            "performance_fee": yield_data["performance_fee"],
            "net_yield": yield_data["net_yield"],
            "apy_estimate": yield_data["net_apy"],
            "net_apy": yield_data["net_apy"],
            "strategy": "Diversified Arbitrage + T-Bills",
            "deposits": deposits,
        }

