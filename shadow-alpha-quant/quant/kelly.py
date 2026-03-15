"""
Kelly Criterion Advisor
========================
Optimal bankroll management for sports positions.

Implements:
    1. Full Kelly - maximizes long-run log-growth of capital
    2. Fractional Kelly (¼, ½, etc.) - reduced variance
    3. Multi-bet Kelly - optimal simultaneous allocation across N independent bets

References:
    Kelly, J.L. (1956). "A new interpretation of information rate."
    Bell System Technical Journal, 35(4), 917-926.

    Thorp, E.O. (2006). "The Kelly Criterion in Blackjack, Sports Betting,
    and the Stock Market." Handbook of Asset and Liability Management.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class KellyResult:
    """Output of a Kelly Criterion calculation."""
    fraction: float         # Optimal fraction of bankroll (f*)
    stake: float            # Absolute stake amount
    expected_growth: float  # Expected log-growth rate per bet
    edge: float             # p x b − (1 − p), the expected return per unit
    odds: float             # Input decimal odds
    true_prob: float        # Input true probability

    def __repr__(self) -> str:
        return (
            f"KellyResult(f*={self.fraction:.4f}, stake={self.stake:.2f}, "
            f"growth={self.expected_growth:.6f}, edge={self.edge:.4f})"
        )


@dataclass
class MultiKellyResult:
    """Output of multi-bet Kelly optimization."""
    allocations: List[KellyResult]
    total_fraction: float
    total_expected_growth: float
    bets_taken: int
    bets_skipped: int


# ---------------------------------------------------------------------------
# Single-bet Kelly
# ---------------------------------------------------------------------------

def kelly_optimal(
    odds: float,
    true_prob: float,
    bankroll: float,
    fraction: float = 0.25,
) -> KellyResult:
    """Compute the Kelly-optimal stake for a single bet.

    Formula
    -------
    f* = p − (1 − p) / b

    where:
        p = true probability of winning
        b = net payout per unit staked (decimal_odds − 1)
        f* = fraction of bankroll to wager

    The actual stake = fraction x f* x bankroll  (fractional Kelly).

    Parameters
    ----------
    odds : float
        European decimal odds (e.g. 2.0 for even money).
    true_prob : float
        Your estimated true probability of the bet winning.
    bankroll : float
        Current bankroll in currency units.
    fraction : float
        Kelly fraction to use (1.0 = full Kelly, 0.25 = quarter Kelly).

    Returns
    -------
    KellyResult

    Examples
    --------
    >>> r = kelly_optimal(2.0, 0.6, 10000.0, fraction=1.0)
    >>> round(r.fraction, 4)
    0.2
    >>> round(r.stake, 2)
    2000.0

    >>> r = kelly_optimal(2.0, 0.6, 10000.0, fraction=0.25)
    >>> round(r.stake, 2)
    500.0
    """
    if odds <= 1.0:
        raise ValueError(f"Decimal odds must be > 1.0, got {odds}")
    if not 0.0 < true_prob < 1.0:
        raise ValueError(f"Probability must be in (0, 1), got {true_prob}")
    if bankroll < 0:
        raise ValueError(f"Bankroll must be >= 0, got {bankroll}")

    b = odds - 1.0  # net payout per unit staked
    q = 1.0 - true_prob

    # Kelly fraction (can be negative -> don't bet)
    f_star = true_prob - q / b

    # Edge = expected return per unit staked
    edge = true_prob * b - q

    # Expected log-growth rate
    if f_star > 0:
        growth = true_prob * math.log(1 + f_star * b) + q * math.log(1 - f_star)
    else:
        growth = 0.0

    # Apply fractional Kelly
    actual_fraction = max(f_star * fraction, 0.0)
    stake = actual_fraction * bankroll

    return KellyResult(
        fraction=actual_fraction,
        stake=round(stake, 2),
        expected_growth=growth,
        edge=edge,
        odds=odds,
        true_prob=true_prob,
    )


# ---------------------------------------------------------------------------
# Multi-bet Kelly
# ---------------------------------------------------------------------------

def multi_kelly(
    bets: List[Tuple[float, float]],
    bankroll: float,
    fraction: float = 0.25,
    max_total_fraction: float = 0.30,
) -> MultiKellyResult:
    """Compute Kelly-optimal allocations for multiple independent simultaneous bets.

    Uses the iterative single-Kelly approach: compute Kelly for each bet
    independently, then scale down proportionally if total allocation exceeds
    the maximum portfolio fraction.

    Parameters
    ----------
    bets : list of (odds, true_prob)
        Each bet defined by its decimal odds and your true probability estimate.
    bankroll : float
        Current bankroll.
    fraction : float
        Fractional Kelly to apply per bet (default 0.25 = quarter Kelly).
    max_total_fraction : float
        Maximum total bankroll to risk across all bets (e.g. 0.30 = 30%).

    Returns
    -------
    MultiKellyResult

    Example
    -------
    >>> bets = [(2.0, 0.6), (3.0, 0.4), (1.5, 0.3)]
    >>> result = multi_kelly(bets, 10000.0, fraction=0.25)
    >>> result.total_fraction <= 0.30
    True
    """
    # Step 1: Compute individual Kelly for each bet
    results = []
    for (odds, prob) in bets:
        r = kelly_optimal(odds, prob, bankroll, fraction)
        results.append(r)

    # Step 2: Keep only positive-edge bets
    positive = [r for r in results if r.fraction > 0]
    skipped = len(results) - len(positive)

    if not positive:
        return MultiKellyResult(
            allocations=[],
            total_fraction=0.0,
            total_expected_growth=0.0,
            bets_taken=0,
            bets_skipped=len(results),
        )

    # Step 3: Sort by edge (best first)
    positive.sort(key=lambda r: r.edge, reverse=True)

    # Step 4: Scale down if total allocation exceeds max
    total_frac = sum(r.fraction for r in positive)
    if total_frac > max_total_fraction:
        scale = max_total_fraction / total_frac
        scaled = []
        for r in positive:
            new_frac = r.fraction * scale
            new_stake = round(new_frac * bankroll, 2)
            scaled.append(KellyResult(
                fraction=new_frac,
                stake=new_stake,
                expected_growth=r.expected_growth,
                edge=r.edge,
                odds=r.odds,
                true_prob=r.true_prob,
            ))
        positive = scaled
        total_frac = max_total_fraction

    # Recalculate stakes with bankroll
    final = []
    for r in positive:
        final.append(KellyResult(
            fraction=r.fraction,
            stake=round(r.fraction * bankroll, 2),
            expected_growth=r.expected_growth,
            edge=r.edge,
            odds=r.odds,
            true_prob=r.true_prob,
        ))

    total_growth = sum(r.expected_growth for r in final)

    return MultiKellyResult(
        allocations=final,
        total_fraction=total_frac,
        total_expected_growth=total_growth,
        bets_taken=len(final),
        bets_skipped=skipped,
    )


# ---------------------------------------------------------------------------
# Accumulator Kelly (correlated multi-leg bet)
# ---------------------------------------------------------------------------

def accumulator_kelly(
    legs: List[Tuple[float, float]],
    bankroll: float,
    fraction: float = 0.25,
) -> KellyResult:
    """Kelly for an accumulator (parlay) - all legs must win.

    The accumulator is treated as a single bet with combined odds and
    combined probability.

    Parameters
    ----------
    legs : list of (decimal_odds, true_prob)
        Each leg of the accumulator.
    bankroll : float
        Current bankroll.
    fraction : float
        Fractional Kelly multiplier.

    Returns
    -------
    KellyResult

    Example
    -------
    >>> legs = [(1.5, 0.7), (2.0, 0.55), (1.8, 0.6)]
    >>> r = accumulator_kelly(legs, 10000.0, fraction=0.25)
    >>> r.odds  # combined odds
    5.4
    """
    # Combined odds = product of individual odds
    combined_odds = 1.0
    for (o, _) in legs:
        combined_odds *= o

    # Combined probability = product of individual probabilities (assuming independence)
    combined_prob = 1.0
    for (_, p) in legs:
        combined_prob *= p

    combined_odds = round(combined_odds, 4)

    return kelly_optimal(combined_odds, combined_prob, bankroll, fraction)

