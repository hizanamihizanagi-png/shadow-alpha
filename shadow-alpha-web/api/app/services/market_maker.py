"""
Market Maker - AMM + Instant Cashout functionality.
"""

from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal

from app.services.pricing_engine import PricingEngineService


class MarketMakerService:
    """Market making for instant cashout and spread management."""

    MIN_SPREAD_PCT = Decimal("5.00")
    MAX_SPREAD_PCT = Decimal("8.00")
    DEFAULT_SPREAD_PCT = Decimal("6.00")

    @classmethod
    def calculate_spread(
        cls,
        fair_value: Decimal,
        liquidity_score: float = 0.5,
        volatility: float = 0.35,
        time_to_event: float = 0.5,
    ) -> Decimal:
        """Calculate optimal spread based on market conditions.

        Higher liquidity -> tighter spread. Higher vol / less time -> wider spread.
        """
        base = float(cls.DEFAULT_SPREAD_PCT)

        # Liquidity factor: more liquidity -> tighter spread
        liquidity_adj = (1.0 - liquidity_score) * 2.0

        # Volatility factor
        vol_adj = (volatility - 0.30) * 5.0

        # Time factor: less time -> wider spread
        time_adj = (1.0 - time_to_event) * 1.5

        spread = base + liquidity_adj + vol_adj + time_adj
        spread = max(float(cls.MIN_SPREAD_PCT), min(float(cls.MAX_SPREAD_PCT), spread))
        return Decimal(str(spread)).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

    @classmethod
    def instant_cashout_quote(
        cls,
        current_prob: float,
        implied_prob: float,
        sigma: float,
        time_remaining: float,
        max_payout: Decimal,
        stake: Decimal,
    ) -> dict:
        """Generate an instant cashout quote for a position.

        Returns the offered price (fair value minus spread).
        """
        fair_value = PricingEngineService.price_position(
            current_prob, implied_prob, sigma, time_remaining, max_payout,
        )

        spread_pct = cls.calculate_spread(
            fair_value,
            liquidity_score=0.5,
            volatility=sigma,
            time_to_event=time_remaining,
        )

        spread_amount = (fair_value * spread_pct / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )
        offered_price = fair_value - spread_amount

        # Never offer less than 0
        offered_price = max(offered_price, Decimal("0.00"))

        pnl = offered_price - stake

        return {
            "fair_value": fair_value,
            "spread_pct": spread_pct,
            "spread_amount": spread_amount,
            "offered_price": offered_price,
            "original_stake": stake,
            "pnl": pnl,
            "pnl_pct": (pnl / stake * Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN) if stake > 0 else Decimal("0.00"),
        }

