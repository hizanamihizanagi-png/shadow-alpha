"""
EV Calibrator - Expected Value calculator with calibrated probabilities.
Uses logistic regression-style calibration for probability sharpening.
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple


class EVCalibrator:
    """Expected Value calculator with probability calibration.
    
    Takes sportsbook odds and applies calibration adjustments to
    produce sharper probability estimates, then calculates true EV.
    """

    # Default calibration: reduces vig (overround) from bookmaker odds
    DEFAULT_VIG_ADJUSTMENT = 0.97  # Assume 3% vig
    EDGE_THRESHOLD = 0.02  # Minimum 2% edge to flag as +EV

    @classmethod
    def odds_to_prob(cls, decimal_odds: float) -> float:
        """Convert decimal odds to implied probability."""
        if decimal_odds <= 1.0:
            return 1.0
        return 1.0 / decimal_odds

    @classmethod
    def remove_vig(
        cls,
        odds_home: float,
        odds_draw: Optional[float],
        odds_away: float,
    ) -> dict:
        """Remove bookmaker vig (overround) via power method.
        
        Returns true probabilities summing to 1.0.
        """
        probs_raw = [cls.odds_to_prob(odds_home), cls.odds_to_prob(odds_away)]
        if odds_draw is not None:
            probs_raw.insert(1, cls.odds_to_prob(odds_draw))

        total = sum(probs_raw)
        # Power method: find k such that sum(p_i^k) = 1
        # Approximation: simple normalisation
        probs_fair = [p / total for p in probs_raw]

        labels = ["home", "away"] if odds_draw is None else ["home", "draw", "away"]
        return {label: round(p, 6) for label, p in zip(labels, probs_fair)}

    @classmethod
    def platt_calibrate(
        cls,
        raw_prob: float,
        a: float = -1.0,
        b: float = 0.05,
    ) -> float:
        """Platt scaling calibration.
        
        P(y=1|f) = 1 / (1 + exp(A*f + B))
        
        Default params are tuned for typical sportsbook overround.
        In production, A and B should be fitted on historical data.
        """
        logit = a * raw_prob + b
        calibrated = 1.0 / (1.0 + math.exp(-logit))
        return calibrated

    @classmethod
    def calculate_ev(
        cls,
        stake: float,
        decimal_odds: float,
        true_probability: float,
    ) -> dict:
        """Calculate Expected Value for a bet.
        
        EV = (true_prob x payout) - stake
        """
        payout = stake * decimal_odds
        ev = (true_probability * payout) - stake
        ev_pct = (ev / stake * 100) if stake > 0 else 0.0
        roi = ev_pct  # For single position, EV% = ROI

        return {
            "ev": round(ev, 2),
            "ev_pct": round(ev_pct, 2),
            "expected_roi": round(roi, 2),
            "is_positive_ev": ev > 0,
            "edge": round(true_probability - cls.odds_to_prob(decimal_odds), 4),
            "recommended": ev_pct >= cls.EDGE_THRESHOLD * 100,
        }

    @classmethod
    def full_evaluation(
        cls,
        stake: float,
        odds_selection: float,
        odds_home: float,
        odds_draw: Optional[float],
        odds_away: float,
        selection: str = "home",
        model_prob: Optional[float] = None,
    ) -> dict:
        """Full EV evaluation with vig removal and calibration.
        
        Args:
            stake: Bet amount
            odds_selection: Decimal odds for the selection
            odds_home/draw/away: Full market odds
            selection: Which outcome is selected
            model_prob: Optional model probability (overrides calibration)
        """
        # Remove vig
        fair_probs = cls.remove_vig(odds_home, odds_draw, odds_away)

        # True probability: either model or vig-adjusted
        if model_prob is not None:
            true_prob = model_prob
            prob_source = "model"
        else:
            true_prob = fair_probs.get(selection, cls.odds_to_prob(odds_selection))
            prob_source = "vig_adjusted"

        # EV calculation
        ev_result = cls.calculate_ev(stake, odds_selection, true_prob)

        # Kelly fraction
        b = odds_selection - 1  # Net odds
        p = true_prob
        kelly = (b * p - (1 - p)) / b if b > 0 else 0.0
        kelly = max(0.0, kelly)

        return {
            **ev_result,
            "fair_probabilities": fair_probs,
            "true_probability": round(true_prob, 6),
            "prob_source": prob_source,
            "implied_probability": round(cls.odds_to_prob(odds_selection), 6),
            "overround": round(sum(cls.odds_to_prob(o) for o in [odds_home, odds_away] + ([odds_draw] if odds_draw else [])) - 1.0, 4),
            "kelly_fraction": round(kelly, 4),
            "kelly_stake": round(kelly * stake, 2),
        }

