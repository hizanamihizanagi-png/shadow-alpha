"""
VaR / CVaR Calculator - risk metrics for portfolio and position level.
Implements Historical, Parametric Gaussian, and Monte Carlo VaR.
"""

from __future__ import annotations

import math
import random
from typing import List, Optional


class RiskMetricsCalculator:
    """Value at Risk (VaR) and Conditional VaR (CVaR / Expected Shortfall).
    
    Three methodologies:
    1. Historical VaR - from observed PnL distribution
    2. Parametric VaR - Gaussian assumption
    3. Monte Carlo VaR - simulated scenarios
    """

    @classmethod
    def historical_var(
        cls,
        pnl_series: List[float],
        confidence: float = 0.95,
    ) -> dict:
        """Historical VaR - percentile-based from actual PnL data.
        
        VaR at 95% means: "We are 95% confident that the loss will not
        exceed this amount in a single period."
        """
        if len(pnl_series) < 5:
            return {"var": 0.0, "cvar": 0.0, "method": "historical", "insufficient_data": True}

        sorted_pnl = sorted(pnl_series)
        n = len(sorted_pnl)

        # VaR index
        var_idx = int(math.floor((1 - confidence) * n))
        var_idx = max(0, min(var_idx, n - 1))
        var = -sorted_pnl[var_idx]  # Positive number = loss amount

        # CVaR (Expected Shortfall) = average of losses beyond VaR
        tail = sorted_pnl[: var_idx + 1]
        cvar = -sum(tail) / len(tail) if tail else var

        return {
            "var": round(var, 2),
            "cvar": round(cvar, 2),
            "confidence": confidence,
            "method": "historical",
            "sample_size": n,
        }

    @classmethod
    def parametric_var(
        cls,
        mean_return: float,
        std_return: float,
        portfolio_value: float,
        confidence: float = 0.95,
    ) -> dict:
        """Parametric VaR - assumes Gaussian returns.
        
        VaR = -(μ - z_α x σ) x Portfolio Value
        """
        # Z-scores for common confidence levels
        z_scores = {0.90: 1.282, 0.95: 1.645, 0.99: 2.326}
        z = z_scores.get(confidence, 1.645)

        var = -(mean_return - z * std_return) * portfolio_value
        var = max(var, 0.0)

        # CVaR for Gaussian: μ - σ x φ(z_α) / (1-α)
        # φ(z) = standard normal PDF
        phi_z = math.exp(-0.5 * z ** 2) / math.sqrt(2 * math.pi)
        cvar_return = mean_return - std_return * phi_z / (1 - confidence)
        cvar = -cvar_return * portfolio_value
        cvar = max(cvar, 0.0)

        return {
            "var": round(var, 2),
            "cvar": round(cvar, 2),
            "confidence": confidence,
            "method": "parametric_gaussian",
            "z_score": z,
        }

    @classmethod
    def monte_carlo_var(
        cls,
        mean_return: float,
        std_return: float,
        portfolio_value: float,
        confidence: float = 0.95,
        n_simulations: int = 10000,
        seed: Optional[int] = None,
    ) -> dict:
        """Monte Carlo VaR - simulated returns.
        
        Generates n random scenarios from the return distribution
        and computes VaR/CVaR from simulated outcomes.
        """
        if seed is not None:
            random.seed(seed)

        simulated_pnl = [
            random.gauss(mean_return, std_return) * portfolio_value
            for _ in range(n_simulations)
        ]

        sorted_pnl = sorted(simulated_pnl)
        var_idx = int(math.floor((1 - confidence) * n_simulations))
        var_idx = max(0, min(var_idx, n_simulations - 1))

        var = -sorted_pnl[var_idx]
        tail = sorted_pnl[: var_idx + 1]
        cvar = -sum(tail) / len(tail) if tail else var

        return {
            "var": round(var, 2),
            "cvar": round(cvar, 2),
            "confidence": confidence,
            "method": "monte_carlo",
            "n_simulations": n_simulations,
        }

    @classmethod
    def portfolio_risk_report(
        cls,
        pnl_series: List[float],
        portfolio_value: float,
        confidence: float = 0.95,
    ) -> dict:
        """Full risk report combining all VaR methodologies.
        
        Returns a dashboard-ready risk summary.
        """
        # Stats from historical data
        n = len(pnl_series)
        if n < 5:
            return {"error": "Insufficient data for risk analysis", "min_required": 5}

        mean_pnl = sum(pnl_series) / n
        std_pnl = math.sqrt(sum((p - mean_pnl) ** 2 for p in pnl_series) / (n - 1))

        mean_return = mean_pnl / portfolio_value if portfolio_value > 0 else 0.0
        std_return = std_pnl / portfolio_value if portfolio_value > 0 else 0.0

        historical = cls.historical_var(pnl_series, confidence)
        parametric = cls.parametric_var(mean_return, std_return, portfolio_value, confidence)
        monte_carlo = cls.monte_carlo_var(mean_return, std_return, portfolio_value, confidence, seed=42)

        # Stress test: what if volatility doubles?
        stress = cls.parametric_var(mean_return, std_return * 2, portfolio_value, confidence)

        return {
            "portfolio_value": round(portfolio_value, 2),
            "confidence": confidence,
            "historical": historical,
            "parametric": parametric,
            "monte_carlo": monte_carlo,
            "stress_test_2x_vol": stress,
            "summary": {
                "mean_daily_pnl": round(mean_pnl, 2),
                "pnl_volatility": round(std_pnl, 2),
                "sharpe_proxy": round(mean_return / std_return, 4) if std_return > 0 else 0.0,
                "worst_day": round(min(pnl_series), 2),
                "best_day": round(max(pnl_series), 2),
            },
        }

