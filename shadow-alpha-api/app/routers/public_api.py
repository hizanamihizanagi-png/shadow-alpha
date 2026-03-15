"""
Public API Router - external API endpoints ("OpenAI for Betting Analytics").
"""

from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.pricing_engine import PricingEngineService

router = APIRouter()


# ── Request schemas ───────────────────────────────────────────────────────
class PositionEvalRequest(BaseModel):
    sportsbook: str
    teams: str
    odds: float = Field(..., gt=1.0)
    stake: float = Field(..., gt=0)
    current_prob: float = Field(default=0.50, ge=0, le=1)
    time_remaining: float = Field(default=0.75, ge=0, le=1)


class BlackScholesRequest(BaseModel):
    current_prob: float = Field(..., ge=0, le=1)
    implied_prob: float = Field(..., ge=0, le=1)
    volatility: float = Field(default=0.35, gt=0)
    time_remaining: float = Field(..., ge=0, le=1)
    max_payout: float = Field(default=1000.0, gt=0)


class KellyRequest(BaseModel):
    odds: float = Field(..., gt=1.0)
    probability: float = Field(..., ge=0, le=1)
    bankroll: float = Field(..., gt=0)
    fraction: float = Field(default=0.25, ge=0.05, le=1.0)


# ── Endpoints ─────────────────────────────────────────────────────────────
@router.post("/positions/evaluate")
async def evaluate_position(payload: PositionEvalRequest) -> dict:
    """Evaluate a bet position - fair value, EV, and Kelly fraction."""
    implied_prob = PricingEngineService.odds_to_implied_prob(payload.odds)
    max_payout = Decimal(str(payload.stake * payload.odds))
    sigma = PricingEngineService.get_sigma("football")

    fair_value = PricingEngineService.price_position(
        payload.current_prob, implied_prob, sigma, payload.time_remaining, max_payout,
    )

    ev = float(fair_value) - payload.stake
    greeks = PricingEngineService.compute_greeks(
        payload.current_prob, implied_prob, sigma, payload.time_remaining, max_payout,
    )

    # Kelly fraction
    p = payload.current_prob
    q = 1 - p
    b = payload.odds - 1
    kelly = (b * p - q) / b if b > 0 else 0
    kelly = max(0, kelly)

    return {
        "fair_value": float(fair_value),
        "stake": payload.stake,
        "ev": round(ev, 2),
        "ev_pct": round(ev / payload.stake * 100, 2) if payload.stake > 0 else 0,
        "implied_prob": round(implied_prob, 4),
        "current_prob": payload.current_prob,
        "kelly_fraction": round(kelly, 4),
        "optimal_stake": round(kelly * payload.stake, 2),
        "confidence": "moderate",
        "greeks": greeks,
    }


@router.post("/analytics/black-scholes")
async def black_scholes_pricing(payload: BlackScholesRequest) -> dict:
    """Run Black-Scholes pricing on arbitrary parameters."""
    max_payout = Decimal(str(payload.max_payout))

    fair_value = PricingEngineService.price_position(
        payload.current_prob, payload.implied_prob, payload.volatility,
        payload.time_remaining, max_payout,
    )

    greeks = PricingEngineService.compute_greeks(
        payload.current_prob, payload.implied_prob, payload.volatility,
        payload.time_remaining, max_payout,
    )

    return {
        "position_value": float(fair_value),
        "greeks": greeks,
    }


@router.post("/analytics/kelly")
async def kelly_criterion(payload: KellyRequest) -> dict:
    """Kelly Criterion optimal stake calculation."""
    p = payload.probability
    q = 1 - p
    b = payload.odds - 1

    full_kelly = (b * p - q) / b if b > 0 else 0
    full_kelly = max(0, full_kelly)

    fractional = full_kelly * payload.fraction
    optimal_stake = fractional * payload.bankroll
    expected_growth = (p * (1 + b * fractional) + q * (1 - fractional)) if fractional > 0 else 1.0

    return {
        "full_kelly_fraction": round(full_kelly, 6),
        "fractional_kelly": round(fractional, 6),
        "fraction_used": payload.fraction,
        "optimal_stake": round(optimal_stake, 2),
        "bankroll": payload.bankroll,
        "expected_growth_rate": round(expected_growth, 6),
        "edge": round((p * b - q), 4),
        "recommendation": "bet" if full_kelly > 0 else "pass",
    }


@router.get("/positions/price")
async def get_live_price(
    odds: float = 2.0,
    current_prob: float = 0.55,
    time_remaining: float = 0.75,
    max_payout: float = 1000.0,
    sport: str = "football",
) -> dict:
    """Get live position pricing."""
    implied_prob = PricingEngineService.odds_to_implied_prob(odds)
    sigma = PricingEngineService.get_sigma(sport)

    fair_value = PricingEngineService.price_position(
        current_prob, implied_prob, sigma, time_remaining, Decimal(str(max_payout)),
    )

    return {
        "fair_value": float(fair_value),
        "implied_prob": round(implied_prob, 4),
        "current_prob": current_prob,
        "sigma": sigma,
        "time_remaining": time_remaining,
    }

