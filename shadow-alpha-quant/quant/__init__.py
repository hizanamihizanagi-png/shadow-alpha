"""
Shadow Alpha Quantitative Engine
=================================
Agent 12 — QUANT: Core mathematical models for sports position pricing,
match prediction, bankroll management, risk metrics, and insurance pricing.

Modules:
    pricing_engine      — Modified Black-Scholes for position fair-value
    match_model         — Dixon-Coles bivariate Poisson match predictor
    kelly               — Kelly Criterion bankroll advisor
    actuarial_model     — Shield insurance actuarial pricing
    copy_trading_scorer — Sharpe/Sortino trader scoring
    risk_metrics        — VaR/CVaR portfolio risk
    ev_calibrator       — EV with vig removal and probability calibration
    utils               — Shared math utilities
"""

from .pricing_engine import price_position, compute_greeks, calibrate_sigma
from .match_model import DixonColesModel, predict_match
from .kelly import kelly_optimal, multi_kelly
from .actuarial_model import ActuarialShieldModel
from .copy_trading_scorer import CopyTradingScorer
from .risk_metrics import RiskMetricsCalculator
from .ev_calibrator import EVCalibrator

__version__ = "0.2.0"

__all__ = [
    "price_position",
    "compute_greeks",
    "calibrate_sigma",
    "DixonColesModel",
    "predict_match",
    "kelly_optimal",
    "multi_kelly",
    "ActuarialShieldModel",
    "CopyTradingScorer",
    "RiskMetricsCalculator",
    "EVCalibrator",
]

