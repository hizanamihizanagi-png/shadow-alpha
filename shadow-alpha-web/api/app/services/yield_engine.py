"""
Yield Engine — calculate and distribute yields for tontine groups.
"""

from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal


class YieldEngineService:
    """Calculate yields for tontine pools and vault deposits."""

    BASE_APY = Decimal("9.75")  # Annual percentage yield
    PERFORMANCE_FEE_PCT = Decimal("35.00")  # SA takes 35% of gross yield

    @classmethod
    def calculate_monthly_yield(cls, principal: Decimal) -> dict:
        """Calculate monthly yield on a principal amount."""
        monthly_rate = cls.BASE_APY / Decimal("12") / Decimal("100")
        gross = (principal * monthly_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        fee = (gross * cls.PERFORMANCE_FEE_PCT / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )
        net = gross - fee
        return {
            "principal": principal,
            "gross_yield": gross,
            "performance_fee": fee,
            "net_yield": net,
            "apy": float(cls.BASE_APY),
            "net_apy": float(cls.BASE_APY * (Decimal("100") - cls.PERFORMANCE_FEE_PCT) / Decimal("100")),
        }

    @classmethod
    def calculate_daily_yield(cls, principal: Decimal) -> dict:
        """Calculate daily yield on a principal amount."""
        daily_rate = cls.BASE_APY / Decimal("365") / Decimal("100")
        gross = (principal * daily_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        fee = (gross * cls.PERFORMANCE_FEE_PCT / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )
        net = gross - fee
        return {
            "principal": principal,
            "gross_yield": gross,
            "performance_fee": fee,
            "net_yield": net,
        }
