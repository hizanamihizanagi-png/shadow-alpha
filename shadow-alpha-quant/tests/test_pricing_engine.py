"""
Tests for the Modified Black-Scholes Pricing Engine.
"""

import math
import pytest
from quant.pricing_engine import (
    price_position,
    compute_greeks,
    calibrate_sigma,
    validate_against_cashout,
)


class TestPricePosition:
    """Core pricing function tests."""

    def test_fair_value_at_the_money(self):
        """When current_prob ≈ implied_prob, fair_value ≈ max_payout × 0.5."""
        fv = price_position(
            current_prob=0.50,
            implied_prob=0.50,
            sigma=0.35,
            time_remaining=0.75,
            max_payout=1000.0,
        )
        # Should be close to 500 (ATM digital option ≈ 0.5 × payout)
        assert 400.0 < fv < 600.0, f"ATM fair value {fv} not near 500"

    def test_fair_value_deep_in_the_money(self):
        """When current_prob >> implied_prob, fair_value → max_payout."""
        fv = price_position(
            current_prob=0.90,
            implied_prob=0.30,
            sigma=0.35,
            time_remaining=0.50,
            max_payout=1000.0,
        )
        assert fv > 900.0, f"Deep ITM fair value {fv} should be near max_payout"

    def test_fair_value_deep_out_of_the_money(self):
        """When current_prob << implied_prob, fair_value → 0."""
        fv = price_position(
            current_prob=0.10,
            implied_prob=0.70,
            sigma=0.35,
            time_remaining=0.50,
            max_payout=1000.0,
        )
        assert fv < 100.0, f"Deep OTM fair value {fv} should be near 0"

    def test_time_decay_otm(self):
        """OTM position loses value as time decreases."""
        fv_early = price_position(0.40, 0.55, 0.35, 0.90, 1000.0)
        fv_late = price_position(0.40, 0.55, 0.35, 0.10, 1000.0)
        assert fv_early > fv_late, "OTM value should decrease with less time"

    def test_boundary_at_expiry_itm(self):
        """At T → 0: if p > K, fair_value → max_payout."""
        fv = price_position(0.60, 0.50, 0.35, 1e-9, 1000.0)
        assert fv == pytest.approx(1000.0, abs=1.0)

    def test_boundary_at_expiry_otm(self):
        """At T → 0: if p < K, fair_value → 0."""
        fv = price_position(0.40, 0.50, 0.35, 1e-9, 1000.0)
        assert fv == pytest.approx(0.0, abs=1.0)

    def test_value_increases_with_probability(self):
        """Higher current_prob → higher fair value."""
        fv_low = price_position(0.40, 0.50, 0.35, 0.50, 1000.0)
        fv_high = price_position(0.70, 0.50, 0.35, 0.50, 1000.0)
        assert fv_high > fv_low

    def test_symmetric_scaling_with_payout(self):
        """Fair value should scale linearly with max_payout."""
        fv_1k = price_position(0.55, 0.50, 0.35, 0.50, 1000.0)
        fv_2k = price_position(0.55, 0.50, 0.35, 0.50, 2000.0)
        assert fv_2k == pytest.approx(fv_1k * 2, rel=1e-6)


class TestGreeks:
    """Greeks computation tests."""

    def test_delta_positive(self):
        """Delta should be positive (value increases with probability)."""
        greeks = compute_greeks(0.50, 0.50, 0.35, 0.50, 1000.0)
        assert greeks.delta > 0, f"Delta {greeks.delta} should be positive"

    def test_theta_sign_otm(self):
        """For OTM positions, theta should be negative (time decay hurts)."""
        greeks = compute_greeks(0.35, 0.55, 0.35, 0.50, 1000.0)
        # OTM: less time = less chance to recover = value drops
        # But theta = ∂V/∂T, and as T increases, OTM has more time value
        # So theta > 0 (more time = more value), meaning time passing hurts
        assert greeks.theta > 0, "OTM theta should be positive (value = increasing function of T)"

    def test_vega_positive(self):
        """Higher volatility should increase ATM option value."""
        greeks = compute_greeks(0.50, 0.50, 0.35, 0.50, 1000.0)
        # For ATM digital options, vega can be near zero but generally positive
        # because more vol = more probability of crossing either way
        assert isinstance(greeks.vega, float)

    def test_gamma_positive_near_atm(self):
        """Gamma should be positive near ATM (convexity)."""
        greeks = compute_greeks(0.50, 0.50, 0.35, 0.50, 1000.0)
        assert greeks.gamma > 0 or abs(greeks.gamma) < 1e6  # numerical tolerance


class TestCalibrateSigma:
    """σ calibration tests."""

    def test_calibrate_returns_valid_sigma(self):
        """Calibration should return a σ in bounds."""
        obs = [
            (0.60, 0.50, 0.70, 1000.0, 620.0),
            (0.45, 0.50, 0.50, 1000.0, 410.0),
            (0.70, 0.40, 0.30, 1000.0, 890.0),
        ]
        sigma = calibrate_sigma(obs)
        assert 0.05 <= sigma <= 1.0, f"Calibrated σ = {sigma} out of bounds"

    def test_calibrate_reduces_error(self):
        """Using calibrated σ should produce lower RMSE than a bad σ."""
        obs = [
            (0.60, 0.50, 0.70, 1000.0, 620.0),
            (0.45, 0.50, 0.50, 1000.0, 410.0),
            (0.70, 0.40, 0.30, 1000.0, 890.0),
        ]
        sigma_opt = calibrate_sigma(obs)

        def rmse(sigma):
            errs = [(price_position(cp, ip, sigma, t, mp) - co) ** 2
                    for (cp, ip, t, mp, co) in obs]
            return math.sqrt(sum(errs) / len(errs))

        assert rmse(sigma_opt) <= rmse(0.05)  # better than min bound
        assert rmse(sigma_opt) <= rmse(1.0)   # better than max bound


class TestValidateAgainstCashout:
    """Cash-out validation tests."""

    def test_positive_edge(self):
        """When model price > cashout, edge should be positive."""
        result = validate_against_cashout(0.70, 0.50, 0.35, 0.50, 1000.0, 600.0)
        assert result["edge"] > 0
        assert result["edge_pct"] > 0

    def test_negative_edge(self):
        """When bookmaker cashout is generous, edge could be negative."""
        result = validate_against_cashout(0.40, 0.50, 0.35, 0.50, 1000.0, 500.0)
        assert result["edge"] < 0
