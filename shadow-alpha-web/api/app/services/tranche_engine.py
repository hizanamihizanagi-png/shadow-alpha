"""
Tranche Engine - CDO-style yield tranching for positions.
"""

from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal


class TrancheEngineService:
    """Classify positions into risk tranches (Senior/Mezzanine/Equity)."""

    @classmethod
    def classify_position(cls, win_probability: float) -> dict:
        """Classify a position into a risk tranche."""
        if win_probability >= 0.65:
            tranche = "Senior"
            expected_return = Decimal("4.50")
            risk_rating = "Low"
        elif win_probability >= 0.40:
            tranche = "Mezzanine"
            expected_return = Decimal("12.00")
            risk_rating = "Medium"
        else:
            tranche = "Equity"
            expected_return = Decimal("25.00")
            risk_rating = "High"

        return {
            "tranche": tranche,
            "win_probability": round(win_probability, 4),
            "expected_return_pct": expected_return,
            "risk_rating": risk_rating,
        }

    @classmethod
    def simulate_tranche_payout(
        cls,
        positions: list[dict],
        num_simulations: int = 10000,
    ) -> dict:
        """Monte Carlo simulation of tranche payouts (simplified stub)."""
        import random

        senior_payouts = []
        mezzanine_payouts = []
        equity_payouts = []

        for _ in range(num_simulations):
            total = Decimal("0.00")
            for pos in positions:
                if random.random() < pos.get("win_probability", 0.5):
                    total += Decimal(str(pos.get("max_payout", 0)))

            # Waterfall: Senior gets paid first, then Mezzanine, then Equity
            senior_payouts.append(float(min(total, Decimal("1000000"))))
            remaining = max(total - Decimal("1000000"), Decimal("0"))
            mezzanine_payouts.append(float(min(remaining, Decimal("500000"))))
            remaining = max(remaining - Decimal("500000"), Decimal("0"))
            equity_payouts.append(float(remaining))

        return {
            "num_simulations": num_simulations,
            "senior": {
                "mean_payout": round(sum(senior_payouts) / len(senior_payouts), 2),
                "min_payout": round(min(senior_payouts), 2),
                "max_payout": round(max(senior_payouts), 2),
            },
            "mezzanine": {
                "mean_payout": round(sum(mezzanine_payouts) / len(mezzanine_payouts), 2),
                "min_payout": round(min(mezzanine_payouts), 2),
                "max_payout": round(max(mezzanine_payouts), 2),
            },
            "equity": {
                "mean_payout": round(sum(equity_payouts) / len(equity_payouts), 2),
                "min_payout": round(min(equity_payouts), 2),
                "max_payout": round(max(equity_payouts), 2),
            },
        }

