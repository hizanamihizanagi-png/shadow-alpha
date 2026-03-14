"""
Actuarial Shield Pricing — advanced insurance premium model.
Uses modified Black-Scholes put pricing with sport-specific adjustments.
"""

from __future__ import annotations

import math
from decimal import ROUND_HALF_EVEN, Decimal
from typing import Optional


class ActuarialShieldModel:
    """Calculate insurance premiums using actuarial principles.
    
    The model uses Black-Scholes put option pricing adapted for sports:
    - S (spot): current fair value of the position
    - K (strike): the original stake (guaranteed minimum)
    - σ: sport-specific volatility
    - T: time remaining to event
    - r: risk-free rate
    
    Plus loading factors for operational costs and adverse selection.
    """

    RISK_FREE_RATE = 0.02  # 2% annualised
    LOADING_FACTOR = 1.25  # 25% on top for operational margin
    MIN_PREMIUM_PCT = 3.0  # Floor at 3% of stake
    MAX_PREMIUM_PCT = 30.0  # Cap at 30% of stake

    # Sport volatilities (annualised)
    SPORT_SIGMAS = {
        "football": 0.35,
        "basketball": 0.45,
        "tennis": 0.30,
        "esports": 0.55,
        "default": 0.40,
    }

    @classmethod
    def _norm_cdf(cls, x: float) -> float:
        """Standard normal CDF via error function."""
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    @classmethod
    def _bs_put_price(
        cls,
        S: float,
        K: float,
        T: float,
        sigma: float,
        r: float,
    ) -> float:
        """Black-Scholes put option price."""
        if T <= 0 or S <= 0 or K <= 0:
            return max(K - S, 0.0)

        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        put_price = K * math.exp(-r * T) * cls._norm_cdf(-d2) - S * cls._norm_cdf(-d1)
        return max(put_price, 0.0)

    @classmethod
    def calculate_premium(
        cls,
        stake: float,
        current_prob: float,
        implied_prob: float,
        time_remaining: float,
        coverage_pct: float = 70.0,
        sport: str = "football",
        max_payout: Optional[float] = None,
    ) -> dict:
        """Calculate shield insurance premium.

        Args:
            stake: Original bet stake
            current_prob: Current probability of winning (0-1)
            implied_prob: Implied probability from odds (0-1)
            time_remaining: Time to event normalised (0-1)
            coverage_pct: % of stake covered (default 70%)
            sport: Sport category for volatility
            max_payout: Maximum potential payout

        Returns:
            Premium details dict
        """
        sigma = cls.SPORT_SIGMAS.get(sport, cls.SPORT_SIGMAS["default"])

        # Fair value of position
        if max_payout is None:
            max_payout = stake / implied_prob if implied_prob > 0 else stake * 2

        fair_value = current_prob * max_payout * math.exp(-cls.RISK_FREE_RATE * time_remaining)

        # Strike = coverage amount (what we guarantee)
        coverage_amount = stake * coverage_pct / 100.0

        # BS put price gives the "option" value of the guarantee
        put_price = cls._bs_put_price(
            S=fair_value,
            K=coverage_amount,
            T=time_remaining,
            sigma=sigma,
            r=cls.RISK_FREE_RATE,
        )

        # Apply loading factor
        gross_premium = put_price * cls.LOADING_FACTOR

        # Adverse selection adjustment: if prob is low, premium goes up
        if current_prob < 0.4:
            adverse_adj = 1.0 + (0.4 - current_prob) * 0.5
            gross_premium *= adverse_adj

        # Apply floor and cap
        min_premium = stake * cls.MIN_PREMIUM_PCT / 100.0
        max_premium = stake * cls.MAX_PREMIUM_PCT / 100.0
        final_premium = max(min_premium, min(max_premium, gross_premium))

        premium_pct = (final_premium / stake * 100.0) if stake > 0 else 0.0

        return {
            "premium": round(final_premium, 2),
            "premium_pct": round(premium_pct, 2),
            "coverage_pct": coverage_pct,
            "coverage_amount": round(coverage_amount, 2),
            "fair_value": round(fair_value, 2),
            "put_price_raw": round(put_price, 2),
            "sigma": sigma,
            "sport": sport,
            "model": "bs_put_actuarial_v1",
        }

    @classmethod
    def expected_loss_ratio(
        cls,
        premiums_collected: float,
        claims_paid: float,
    ) -> dict:
        """Calculate the loss ratio and combined ratio for the shield book.
        
        Insurance industry standard metrics.
        """
        loss_ratio = claims_paid / premiums_collected if premiums_collected > 0 else 0.0
        expense_ratio = 0.15  # 15% operating expenses
        combined_ratio = loss_ratio + expense_ratio

        return {
            "loss_ratio": round(loss_ratio, 4),
            "expense_ratio": expense_ratio,
            "combined_ratio": round(combined_ratio, 4),
            "profitable": combined_ratio < 1.0,
            "underwriting_profit_pct": round((1.0 - combined_ratio) * 100, 2),
        }
