"""
Copy-Trading Scorer - evaluate traders for the copy-trading marketplace.
Uses Sharpe Ratio, Sortino Ratio, and consistency metrics.
"""

from __future__ import annotations

import math
from typing import List, Optional


class CopyTradingScorer:
    """Score traders for the copy-trading marketplace.
    
    Uses institutional-grade risk-adjusted return metrics:
    - Sharpe Ratio: excess return / total volatility
    - Sortino Ratio: excess return / downside volatility
    - Calmar Ratio: return / max drawdown
    - Consistency Score: % of winning periods
    """

    RISK_FREE_DAILY = 0.02 / 365  # 2% annualised
    MIN_TRACK_RECORD = 20  # Minimum positions for scoring

    @classmethod
    def compute_returns(cls, pnl_series: List[float], stakes: List[float]) -> List[float]:
        """Compute per-position return %."""
        if len(pnl_series) != len(stakes):
            raise ValueError("pnl_series and stakes must have same length")
        return [
            pnl / stake if stake > 0 else 0.0
            for pnl, stake in zip(pnl_series, stakes)
        ]

    @classmethod
    def sharpe_ratio(cls, returns: List[float]) -> float:
        """Annualised Sharpe Ratio."""
        if len(returns) < 2:
            return 0.0
        mean_r = sum(returns) / len(returns)
        excess = mean_r - cls.RISK_FREE_DAILY
        std = math.sqrt(sum((r - mean_r) ** 2 for r in returns) / (len(returns) - 1))
        if std == 0:
            return 0.0
        # Annualise (assume ~365 positions/year equivalent)
        return (excess / std) * math.sqrt(252)

    @classmethod
    def sortino_ratio(cls, returns: List[float]) -> float:
        """Annualised Sortino Ratio (penalises only downside vol)."""
        if len(returns) < 2:
            return 0.0
        mean_r = sum(returns) / len(returns)
        excess = mean_r - cls.RISK_FREE_DAILY
        downside = [min(r - cls.RISK_FREE_DAILY, 0.0) for r in returns]
        downside_dev = math.sqrt(sum(d ** 2 for d in downside) / (len(downside) - 1))
        if downside_dev == 0:
            return 0.0
        return (excess / downside_dev) * math.sqrt(252)

    @classmethod
    def max_drawdown(cls, cumulative_pnl: List[float]) -> float:
        """Maximum drawdown from cumulative PnL series."""
        if not cumulative_pnl:
            return 0.0
        peak = cumulative_pnl[0]
        max_dd = 0.0
        for val in cumulative_pnl:
            if val > peak:
                peak = val
            dd = (peak - val) / peak if peak > 0 else 0.0
            max_dd = max(max_dd, dd)
        return max_dd

    @classmethod
    def consistency_score(cls, returns: List[float]) -> float:
        """% of positions that were profitable."""
        if len(returns) == 0:
            return 0.0
        wins = sum(1 for r in returns if r > 0)
        return wins / len(returns)

    @classmethod
    def score_trader(
        cls,
        pnl_series: List[float],
        stakes: List[float],
        display_name: str = "Unknown",
    ) -> dict:
        """Compute a comprehensive trader score for copy-trading.
        
        Returns a composite score out of 100 and detailed metrics.
        """
        n = len(pnl_series)
        if n < cls.MIN_TRACK_RECORD:
            return {
                "trader": display_name,
                "eligible": False,
                "reason": f"Need {cls.MIN_TRACK_RECORD}+ positions, have {n}",
                "composite_score": 0,
            }

        returns = cls.compute_returns(pnl_series, stakes)

        sharpe = cls.sharpe_ratio(returns)
        sortino = cls.sortino_ratio(returns)
        consistency = cls.consistency_score(returns)

        # Cumulative PnL for drawdown
        cum_pnl = []
        running = 0.0
        for pnl in pnl_series:
            running += pnl
            cum_pnl.append(running)

        mdd = cls.max_drawdown(cum_pnl) if cum_pnl else 0.0
        total_return = sum(pnl_series)
        avg_return = sum(returns) / len(returns) if returns else 0.0

        # Composite score (0-100)
        # Weights: Sharpe 30%, Sortino 25%, Consistency 25%, Low DD 20%
        sharpe_score = min(max(sharpe / 3.0, 0.0), 1.0) * 30  # 3.0 Sharpe = max
        sortino_score = min(max(sortino / 4.0, 0.0), 1.0) * 25  # 4.0 Sortino = max
        consistency_score_val = consistency * 25
        dd_score = (1.0 - min(mdd, 1.0)) * 20  # Lower DD = higher score

        composite = sharpe_score + sortino_score + consistency_score_val + dd_score

        # Tier based on score
        if composite >= 80:
            tier = "Platinum"
        elif composite >= 60:
            tier = "Gold"
        elif composite >= 40:
            tier = "Silver"
        else:
            tier = "Bronze"

        return {
            "trader": display_name,
            "eligible": True,
            "composite_score": round(composite, 1),
            "tier": tier,
            "metrics": {
                "sharpe_ratio": round(sharpe, 4),
                "sortino_ratio": round(sortino, 4),
                "consistency": round(consistency, 4),
                "max_drawdown": round(mdd, 4),
                "total_return": round(total_return, 2),
                "avg_return_pct": round(avg_return * 100, 2),
                "total_positions": n,
            },
        }

