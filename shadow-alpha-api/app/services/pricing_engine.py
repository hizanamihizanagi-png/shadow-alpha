"""
Pricing Engine Service — wraps shadow-alpha-quant for async DB context.
All monetary returns as Decimal with banker's rounding.
"""

from __future__ import annotations

import math
from decimal import ROUND_HALF_EVEN, Decimal

from scipy.stats import norm


class PricingEngineService:
    """Modified Black-Scholes pricing for sports positions."""

    FOOTBALL_SIGMA = 0.35
    BASKETBALL_SIGMA = 0.45
    TENNIS_SIGMA = 0.30
    DEFAULT_SIGMA = 0.35

    @staticmethod
    def get_sigma(sport: str = "football") -> float:
        sigmas = {
            "football": PricingEngineService.FOOTBALL_SIGMA,
            "basketball": PricingEngineService.BASKETBALL_SIGMA,
            "tennis": PricingEngineService.TENNIS_SIGMA,
        }
        return sigmas.get(sport.lower(), PricingEngineService.DEFAULT_SIGMA)

    @staticmethod
    def _clamp(val: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, val))

    @staticmethod
    def _d1(p: float, K: float, sigma: float, T: float) -> float:
        if T <= 0 or sigma <= 0:
            return float("inf") if p > K else float("-inf")
        return (math.log(p / K) + 0.5 * sigma ** 2 * T) / (sigma * math.sqrt(T))

    @staticmethod
    def _d2(p: float, K: float, sigma: float, T: float) -> float:
        return PricingEngineService._d1(p, K, sigma, T) - sigma * math.sqrt(T)

    @classmethod
    def price_position(
        cls,
        current_prob: float,
        implied_prob: float,
        sigma: float,
        time_remaining: float,
        max_payout: Decimal,
    ) -> Decimal:
        """Compute fair value using modified Black-Scholes digital option pricing.

        Returns Decimal with banker's rounding.
        """
        p = cls._clamp(current_prob, 1e-6, 1.0 - 1e-6)
        K = cls._clamp(implied_prob, 1e-6, 1.0 - 1e-6)
        T = cls._clamp(time_remaining, 1e-8, 1.0)

        if T < 1e-7:
            return max_payout if p > K else Decimal("0.00")

        d2 = cls._d2(p, K, sigma, T)
        fair_value = float(max_payout) * norm.cdf(d2)
        return Decimal(str(fair_value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

    @classmethod
    def compute_greeks(
        cls,
        current_prob: float,
        implied_prob: float,
        sigma: float,
        time_remaining: float,
        max_payout: Decimal,
        dp: float = 1e-4,
        dt: float = 1e-4,
        dsigma: float = 1e-4,
    ) -> dict:
        """Numerically compute Greeks via central finite differences."""
        V = float(cls.price_position(current_prob, implied_prob, sigma, time_remaining, max_payout))

        # Delta
        p_up = cls._clamp(current_prob + dp, 1e-6, 1 - 1e-6)
        p_dn = cls._clamp(current_prob - dp, 1e-6, 1 - 1e-6)
        V_up = float(cls.price_position(p_up, implied_prob, sigma, time_remaining, max_payout))
        V_dn = float(cls.price_position(p_dn, implied_prob, sigma, time_remaining, max_payout))
        delta = (V_up - V_dn) / (p_up - p_dn)

        # Gamma
        gamma = (V_up - 2 * V + V_dn) / ((p_up - current_prob) ** 2) if (p_up - current_prob) != 0 else 0.0

        # Theta
        T_up = cls._clamp(time_remaining + dt, 1e-8, 1.0)
        T_dn = cls._clamp(time_remaining - dt, 1e-8, 1.0)
        V_Tup = float(cls.price_position(current_prob, implied_prob, sigma, T_up, max_payout))
        V_Tdn = float(cls.price_position(current_prob, implied_prob, sigma, T_dn, max_payout))
        theta = (V_Tup - V_Tdn) / (T_up - T_dn) if (T_up - T_dn) != 0 else 0.0

        # Vega
        s_up = sigma + dsigma
        s_dn = max(sigma - dsigma, 1e-6)
        V_sup = float(cls.price_position(current_prob, implied_prob, s_up, time_remaining, max_payout))
        V_sdn = float(cls.price_position(current_prob, implied_prob, s_dn, time_remaining, max_payout))
        vega = (V_sup - V_sdn) / (s_up - s_dn)

        return {
            "delta": round(delta, 6),
            "gamma": round(gamma, 6),
            "theta": round(theta, 6),
            "vega": round(vega, 6),
        }

    @staticmethod
    def odds_to_implied_prob(odds: float) -> float:
        """Convert decimal odds to implied probability."""
        return 1.0 / odds if odds > 0 else 0.0
