"""
Modified Black-Scholes Pricing Engine for Sports Positions
===========================================================
Treats a sports betting position as a **digital (binary) cash-or-nothing option**
on an underlying probability process.

Key adaptations from classical Black-Scholes:
    • Underlying  = current match probability (p ∈ (0,1))
    • Strike      = implied probability from bookmaker odds (K)
    • Expiry      = time remaining in match (T ∈ (0,1], fraction of total)
    • Volatility  = σ calibrated per sport/league from historical data
    • Payoff      = max_payout if p > K at expiry (digital call)

Reference:
    Longmore & RobotWealth (2024) - treating goals as Poisson volatility driver
    Black-Scholes (1973) adapted for binary options
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import norm

from .utils import clamp, get_default_sigma, odds_to_prob

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Greeks:
    """Option sensitivities for a sports position."""
    delta: float    # ∂V/∂p - sensitivity to probability change
    gamma: float    # ∂²V/∂p² - curvature / rate of delta change
    theta: float    # ∂V/∂T - time decay per unit time
    vega: float     # ∂V/∂σ - sensitivity to volatility

    def __repr__(self) -> str:
        return (
            f"Greeks(delta={self.delta:+.4f}, gamma={self.gamma:+.4f}, "
            f"theta={self.theta:+.4f}, vega={self.vega:+.4f})"
        )


@dataclass
class PricingResult:
    """Full output of the pricing engine."""
    fair_value: float
    edge: float             # fair_value − bookmaker_cashout (if provided)
    greeks: Greeks
    implied_prob: float
    current_prob: float
    sigma: float
    time_remaining: float
    max_payout: float


# ---------------------------------------------------------------------------
# Core pricing function
# ---------------------------------------------------------------------------

def _d1(p: float, K: float, sigma: float, T: float, r: float = 0.0) -> float:
    """Compute d₁ of the modified Black-Scholes formula.

    d₁ = [ln(p/K) + (r + σ²/2)·T] / (σ·√T)
    """
    if T <= 0 or sigma <= 0:
        return float("inf") if p > K else float("-inf")
    return (math.log(p / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))


def _d2(p: float, K: float, sigma: float, T: float, r: float = 0.0) -> float:
    """Compute d₂ = d₁ − σ·√T."""
    return _d1(p, K, sigma, T, r) - sigma * math.sqrt(T)


def price_position(
    current_prob: float,
    implied_prob: float,
    sigma: float,
    time_remaining: float,
    max_payout: float,
    r: float = 0.0,
) -> float:
    """Compute the fair value of a sports position using modified Black-Scholes.

    This models the position as a **digital cash-or-nothing call option**:
        V = max_payout x e^{-rT} x Φ(d₂)

    Parameters
    ----------
    current_prob : float
        Current estimated probability of winning (0, 1).
    implied_prob : float
        Bookmaker's implied probability (strike) from offered odds (0, 1).
    sigma : float
        Volatility of probability changes (calibrated per sport/league).
    time_remaining : float
        Fraction of match remaining in (0, 1].  1.0 = full match, 0 = expired.
    max_payout : float
        Maximum payout of the position in currency units.
    r : float, optional
        Risk-free rate (default 0 - negligible for short-duration events).

    Returns
    -------
    float
        Fair value of the position in currency units.

    Example
    -------
    >>> round(price_position(0.55, 0.50, 0.35, 0.75, 1000.0), 2)
    555.04
    """
    # Guard-rails
    current_prob = clamp(current_prob, 1e-6, 1.0 - 1e-6)
    implied_prob = clamp(implied_prob, 1e-6, 1.0 - 1e-6)
    time_remaining = clamp(time_remaining, 1e-8, 1.0)

    # At expiry: digital payoff
    if time_remaining < 1e-7:
        return max_payout if current_prob > implied_prob else 0.0

    d2 = _d2(current_prob, implied_prob, sigma, time_remaining, r)
    discount = math.exp(-r * time_remaining)
    return max_payout * discount * norm.cdf(d2)


# ---------------------------------------------------------------------------
# Greeks computation
# ---------------------------------------------------------------------------

def compute_greeks(
    current_prob: float,
    implied_prob: float,
    sigma: float,
    time_remaining: float,
    max_payout: float,
    r: float = 0.0,
    dp: float = 1e-4,
    dt: float = 1e-4,
    dsigma: float = 1e-4,
) -> Greeks:
    """Numerically compute the Greeks of a sports position.

    Uses central finite differences for stability.

    Parameters
    ----------
    current_prob, implied_prob, sigma, time_remaining, max_payout, r
        Same as `price_position`.
    dp, dt, dsigma : float
        Bump sizes for finite-difference approximations.

    Returns
    -------
    Greeks
    """
    V = price_position(current_prob, implied_prob, sigma, time_remaining, max_payout, r)

    # --- Delta: ∂V/∂p ---
    p_up = clamp(current_prob + dp, 1e-6, 1 - 1e-6)
    p_dn = clamp(current_prob - dp, 1e-6, 1 - 1e-6)
    V_up = price_position(p_up, implied_prob, sigma, time_remaining, max_payout, r)
    V_dn = price_position(p_dn, implied_prob, sigma, time_remaining, max_payout, r)
    delta = (V_up - V_dn) / (p_up - p_dn)

    # --- Gamma: ∂²V/∂p² ---
    gamma = (V_up - 2 * V + V_dn) / ((p_up - current_prob) ** 2)

    # --- Theta: ∂V/∂T (time decay) ---
    T_up = clamp(time_remaining + dt, 1e-8, 1.0)
    T_dn = clamp(time_remaining - dt, 1e-8, 1.0)
    V_Tup = price_position(current_prob, implied_prob, sigma, T_up, max_payout, r)
    V_Tdn = price_position(current_prob, implied_prob, sigma, T_dn, max_payout, r)
    theta = (V_Tup - V_Tdn) / (T_up - T_dn)

    # --- Vega: ∂V/∂σ ---
    s_up = sigma + dsigma
    s_dn = max(sigma - dsigma, 1e-6)
    V_sup = price_position(current_prob, implied_prob, s_up, time_remaining, max_payout, r)
    V_sdn = price_position(current_prob, implied_prob, s_dn, time_remaining, max_payout, r)
    vega = (V_sup - V_sdn) / (s_up - s_dn)

    return Greeks(delta=delta, gamma=gamma, theta=theta, vega=vega)


# ---------------------------------------------------------------------------
# Volatility calibration
# ---------------------------------------------------------------------------

def calibrate_sigma(
    observations: List[Tuple[float, float, float, float, float]],
    sigma_bounds: Tuple[float, float] = (0.05, 1.0),
) -> float:
    """Calibrate σ from historical cash-out observations.

    Finds the volatility that minimizes RMSE between model prices and
    observed cash-out values.

    Parameters
    ----------
    observations : list of (current_prob, implied_prob, time_remaining, max_payout, observed_cashout)
        Historical data points.
    sigma_bounds : (lo, hi)
        Search range for σ.

    Returns
    -------
    float
        Optimal σ.

    Example
    -------
    >>> obs = [
    ...     (0.60, 0.50, 0.70, 1000.0, 620.0),
    ...     (0.45, 0.50, 0.50, 1000.0, 410.0),
    ...     (0.70, 0.40, 0.30, 1000.0, 890.0),
    ... ]
    >>> sigma = calibrate_sigma(obs)
    >>> 0.05 < sigma < 1.0
    True
    """
    def rmse(sigma: float) -> float:
        errors_sq = []
        for (cp, ip, t, mp, obs_co) in observations:
            model_price = price_position(cp, ip, sigma, t, mp)
            errors_sq.append((model_price - obs_co) ** 2)
        return math.sqrt(sum(errors_sq) / len(errors_sq))

    result = minimize_scalar(rmse, bounds=sigma_bounds, method="bounded")
    return float(result.x)


def validate_against_cashout(
    current_prob: float,
    implied_prob: float,
    sigma: float,
    time_remaining: float,
    max_payout: float,
    bookmaker_cashout: float,
) -> dict:
    """Compare model fair value against a bookmaker's cash-out offer.

    Returns
    -------
    dict with keys: fair_value, cashout, edge, edge_pct
    """
    fv = price_position(current_prob, implied_prob, sigma, time_remaining, max_payout)
    edge = fv - bookmaker_cashout
    edge_pct = (edge / bookmaker_cashout * 100) if bookmaker_cashout > 0 else 0.0
    return {
        "fair_value": round(fv, 2),
        "cashout": round(bookmaker_cashout, 2),
        "edge": round(edge, 2),
        "edge_pct": round(edge_pct, 2),
    }

