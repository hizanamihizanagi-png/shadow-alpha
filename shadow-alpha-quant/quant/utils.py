"""
Shared math utilities for the Shadow Alpha Quant Engine.
========================================================
Conversion helpers, Poisson PMF, vig removal, and sport-specific constants.
"""

from __future__ import annotations

import math
from typing import List, Tuple

import numpy as np
from scipy.stats import poisson as _poisson


# ---------------------------------------------------------------------------
# Odds / probability conversions
# ---------------------------------------------------------------------------

def odds_to_prob(decimal_odds: float) -> float:
    """Convert European decimal odds to implied probability.

    Example
    -------
    >>> odds_to_prob(2.0)
    0.5
    """
    if decimal_odds <= 1.0:
        raise ValueError(f"Decimal odds must be > 1.0, got {decimal_odds}")
    return 1.0 / decimal_odds


def prob_to_odds(prob: float) -> float:
    """Convert probability to fair European decimal odds.

    Example
    -------
    >>> prob_to_odds(0.5)
    2.0
    """
    if not 0.0 < prob <= 1.0:
        raise ValueError(f"Probability must be in (0, 1], got {prob}")
    return 1.0 / prob


def remove_vig(odds_list: List[float]) -> List[float]:
    """Remove bookmaker margin (vig/juice) from a set of decimal odds.

    Returns the true implied probabilities that sum to 1.0.

    Parameters
    ----------
    odds_list : list of float
        Decimal odds for each outcome (e.g. [1.90, 3.50, 4.20] for H/D/A).

    Returns
    -------
    list of float
        Vig-free implied probabilities.

    Example
    -------
    >>> probs = remove_vig([1.90, 3.50, 4.20])
    >>> abs(sum(probs) - 1.0) < 1e-10
    True
    """
    raw_probs = [1.0 / o for o in odds_list]
    total = sum(raw_probs)
    return [p / total for p in raw_probs]


# ---------------------------------------------------------------------------
# Poisson helpers
# ---------------------------------------------------------------------------

def poisson_pmf(k: int, lam: float) -> float:
    """Poisson probability mass function P(X = k | λ).

    Parameters
    ----------
    k : int >= 0
    lam : float > 0

    Returns
    -------
    float
    """
    if k < 0:
        return 0.0
    return float(_poisson.pmf(k, lam))


def poisson_pmf_array(max_goals: int, lam: float) -> np.ndarray:
    """Return array of Poisson PMFs for k = 0 … max_goals."""
    return np.array([poisson_pmf(k, lam) for k in range(max_goals + 1)])


# ---------------------------------------------------------------------------
# Sport-specific default volatilities (σ)
# ---------------------------------------------------------------------------

# Calibrated from historical score variance across major leagues.
# These are initial estimates - should be refined with calibrate_sigma().
DEFAULT_SIGMA: dict[str, float] = {
    # Football (soccer)
    "EPL":          0.35,   # English Premier League
    "LA_LIGA":      0.33,   # Spain La Liga
    "BUNDESLIGA":   0.37,   # Germany Bundesliga
    "SERIE_A":      0.33,   # Italy Serie A
    "LIGUE_1":      0.38,   # France Ligue 1
    "EREDIVISIE":   0.40,   # Netherlands Eredivisie
    "MLS":          0.39,   # USA Major League Soccer
    "CHAMPIONS_LEAGUE": 0.36,
    # African leagues
    "CAMEROON_ELITE_ONE": 0.42,
    "NIGERIAN_NPFL":      0.44,
    "SA_PSL":             0.38,   # South Africa Premier Soccer League
    # Other sports (placeholder - need calibration)
    "NBA":          0.25,
    "NFL":          0.30,
    "NHL":          0.28,
    "TENNIS":       0.32,
    # Fallback
    "DEFAULT":      0.35,
}


def get_default_sigma(league: str) -> float:
    """Look up default volatility for a sport/league."""
    return DEFAULT_SIGMA.get(league.upper(), DEFAULT_SIGMA["DEFAULT"])


# ---------------------------------------------------------------------------
# Misc helpers
# ---------------------------------------------------------------------------

def clamp(value: float, lo: float, hi: float) -> float:
    """Clamp *value* to the range [lo, hi]."""
    return max(lo, min(hi, value))

