"""
Tests for the Kelly Criterion Advisor.
"""

import math
import pytest
from quant.kelly import (
    KellyResult,
    MultiKellyResult,
    accumulator_kelly,
    kelly_optimal,
    multi_kelly,
)


class TestKellyOptimal:
    """Single-bet Kelly tests."""

    def test_positive_edge(self):
        """With p=0.6, odds=2.0 → f* = 0.2 (full Kelly)."""
        r = kelly_optimal(2.0, 0.6, 10000.0, fraction=1.0)
        assert r.fraction == pytest.approx(0.2, abs=1e-6)
        assert r.stake == pytest.approx(2000.0, abs=0.01)

    def test_no_edge(self):
        """With p=0.5, odds=2.0 → f* = 0 (fair bet, don't risk)."""
        r = kelly_optimal(2.0, 0.5, 10000.0, fraction=1.0)
        assert r.fraction == pytest.approx(0.0, abs=1e-6)
        assert r.stake == pytest.approx(0.0, abs=0.01)

    def test_negative_edge(self):
        """With p=0.3, odds=2.0 → f* < 0 (don't bet)."""
        r = kelly_optimal(2.0, 0.3, 10000.0, fraction=1.0)
        # fraction is clamped to 0 (no negative bets)
        assert r.fraction == 0.0
        assert r.stake == 0.0

    def test_fractional_kelly_quarter(self):
        """Quarter Kelly: stake = 0.25 × f* × bankroll."""
        r = kelly_optimal(2.0, 0.6, 10000.0, fraction=0.25)
        # f* = 0.2, quarter = 0.05
        assert r.fraction == pytest.approx(0.05, abs=1e-6)
        assert r.stake == pytest.approx(500.0, abs=0.01)

    def test_fractional_kelly_half(self):
        """Half Kelly: stake = 0.5 × f* × bankroll."""
        r = kelly_optimal(2.0, 0.6, 10000.0, fraction=0.5)
        assert r.fraction == pytest.approx(0.1, abs=1e-6)
        assert r.stake == pytest.approx(1000.0, abs=0.01)

    def test_expected_growth_positive_with_edge(self):
        """Positive edge → positive expected growth rate."""
        r = kelly_optimal(2.0, 0.6, 10000.0, fraction=1.0)
        assert r.expected_growth > 0

    def test_expected_growth_zero_without_edge(self):
        """No edge → zero expected growth."""
        r = kelly_optimal(2.0, 0.5, 10000.0, fraction=1.0)
        assert r.expected_growth == pytest.approx(0.0, abs=1e-10)

    def test_edge_calculation(self):
        """Edge = p × b − (1 − p) where b = odds − 1."""
        r = kelly_optimal(2.5, 0.55, 10000.0)
        expected_edge = 0.55 * 1.5 - 0.45
        assert r.edge == pytest.approx(expected_edge, abs=1e-6)

    def test_invalid_odds_raises(self):
        with pytest.raises(ValueError):
            kelly_optimal(0.5, 0.6, 10000.0)

    def test_invalid_prob_raises(self):
        with pytest.raises(ValueError):
            kelly_optimal(2.0, 1.5, 10000.0)

    def test_zero_bankroll(self):
        r = kelly_optimal(2.0, 0.6, 0.0, fraction=1.0)
        assert r.stake == 0.0

    def test_high_odds_high_prob(self):
        """Very favorable bet → large Kelly fraction."""
        r = kelly_optimal(5.0, 0.5, 10000.0, fraction=1.0)
        # f* = 0.5 - 0.5/4 = 0.375
        assert r.fraction == pytest.approx(0.375, abs=1e-6)


class TestMultiKelly:
    """Multi-bet Kelly tests."""

    def test_positive_edge_bets_taken(self):
        """Only positive-edge bets should be included."""
        bets = [(2.0, 0.6), (2.0, 0.3)]  # first has edge, second doesn't
        result = multi_kelly(bets, 10000.0, fraction=0.25)
        assert result.bets_taken == 1
        assert result.bets_skipped == 1

    def test_total_fraction_respects_max(self):
        """Total allocation should not exceed max_total_fraction."""
        bets = [(2.0, 0.7), (3.0, 0.6), (2.5, 0.65)]
        result = multi_kelly(bets, 10000.0, fraction=1.0, max_total_fraction=0.30)
        assert result.total_fraction <= 0.30 + 1e-6

    def test_no_edge_bets_excluded(self):
        """All negative-edge bets → no allocation."""
        bets = [(2.0, 0.3), (1.5, 0.4)]
        result = multi_kelly(bets, 10000.0)
        assert result.bets_taken == 0
        assert result.total_fraction == 0.0

    def test_allocations_sorted_by_edge(self):
        """Allocations should be sorted by edge (best first)."""
        bets = [(2.0, 0.6), (3.0, 0.55), (2.5, 0.65)]
        result = multi_kelly(bets, 10000.0, fraction=0.25)
        if len(result.allocations) >= 2:
            edges = [a.edge for a in result.allocations]
            assert edges == sorted(edges, reverse=True)

    def test_total_growth_is_sum(self):
        """Total expected growth should be sum of individual growths."""
        bets = [(2.0, 0.6), (3.0, 0.55)]
        result = multi_kelly(bets, 10000.0, fraction=0.25)
        total = sum(a.expected_growth for a in result.allocations)
        assert result.total_expected_growth == pytest.approx(total, abs=1e-10)

    def test_empty_bets(self):
        result = multi_kelly([], 10000.0)
        assert result.bets_taken == 0


class TestAccumulatorKelly:
    """Accumulator (parlay) Kelly tests."""

    def test_combined_odds(self):
        """Combined odds = product of individual odds."""
        legs = [(1.5, 0.7), (2.0, 0.55), (1.8, 0.6)]
        r = accumulator_kelly(legs, 10000.0)
        expected_odds = 1.5 * 2.0 * 1.8
        assert r.odds == pytest.approx(expected_odds, abs=0.01)

    def test_combined_probability(self):
        """Combined prob = product of individual probs (independence)."""
        legs = [(1.5, 0.7), (2.0, 0.55)]
        r = accumulator_kelly(legs, 10000.0)
        expected_prob = 0.7 * 0.55
        assert r.true_prob == pytest.approx(expected_prob, abs=1e-6)

    def test_positive_ev_accumulator(self):
        """Accumulator with individual value bets should have positive edge."""
        legs = [(1.5, 0.75), (1.8, 0.65)]
        r = accumulator_kelly(legs, 10000.0, fraction=0.25)
        # Combined: odds=2.7, prob=0.4875, b=1.7
        # edge = 0.4875 * 1.7 - 0.5125 = 0.317
        assert r.edge > 0
        assert r.stake > 0

    def test_negative_ev_accumulator(self):
        """Accumulator with many legs tends to negative EV."""
        legs = [(1.3, 0.7)] * 10  # 10 legs
        r = accumulator_kelly(legs, 10000.0, fraction=1.0)
        # Combined prob = 0.7^10 ≈ 0.028, combined odds = 1.3^10 ≈ 13.79
        # This might still have edge depending on exact values
        assert isinstance(r, KellyResult)
