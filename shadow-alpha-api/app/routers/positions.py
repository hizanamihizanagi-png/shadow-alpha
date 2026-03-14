"""
Positions Router — create, get, list, and live pricing.
"""

from __future__ import annotations

import uuid
from decimal import ROUND_HALF_EVEN, Decimal
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.auth import get_current_user
from app.middleware.error_handler import NotFoundError
from app.models.position import Position, PositionCreate, PositionOut, PositionValueOut
from app.models.user import User
from app.services.pricing_engine import PricingEngineService

router = APIRouter()


@router.post("/create", response_model=PositionOut, status_code=201)
async def create_position(
    payload: PositionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PositionOut:
    """Create a new trading position."""
    max_payout = (payload.stake * payload.odds).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)

    position = Position(
        user_id=current_user.id,
        sportsbook=payload.sportsbook,
        teams=payload.teams,
        league=payload.league,
        odds=payload.odds,
        stake=payload.stake,
        max_payout=max_payout,
        current_value=payload.stake,  # Initial value = stake
        description=payload.description,
    )
    db.add(position)
    await db.flush()
    return PositionOut.model_validate(position)


@router.get("/my", response_model=List[PositionOut])
async def get_my_positions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[PositionOut]:
    """List all positions for the current user."""
    result = await db.execute(
        select(Position)
        .where(Position.user_id == current_user.id)
        .order_by(Position.created_at.desc())
    )
    return [PositionOut.model_validate(p) for p in result.scalars().all()]


@router.get("/{position_id}", response_model=PositionOut)
async def get_position(
    position_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PositionOut:
    """Get a specific position by ID."""
    result = await db.execute(
        select(Position).where(Position.id == position_id)
    )
    position = result.scalar_one_or_none()
    if not position:
        raise NotFoundError("Position", str(position_id))
    return PositionOut.model_validate(position)


@router.get("/{position_id}/value", response_model=PositionValueOut)
async def get_position_value(
    position_id: uuid.UUID,
    current_prob: float = 0.50,
    time_remaining: float = 0.75,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PositionValueOut:
    """Get real-time pricing for a position via the pricing engine."""
    result = await db.execute(
        select(Position).where(Position.id == position_id)
    )
    position = result.scalar_one_or_none()
    if not position:
        raise NotFoundError("Position", str(position_id))

    implied_prob = PricingEngineService.odds_to_implied_prob(float(position.odds))
    sport = "football"  # Default
    sigma = PricingEngineService.get_sigma(sport)

    fair_value = PricingEngineService.price_position(
        current_prob, implied_prob, sigma, time_remaining, position.max_payout,
    )

    greeks = PricingEngineService.compute_greeks(
        current_prob, implied_prob, sigma, time_remaining, position.max_payout,
    )

    # Update stored current value
    position.current_value = fair_value
    await db.flush()

    return PositionValueOut(
        position_id=position.id,
        fair_value=fair_value,
        current_prob=current_prob,
        implied_prob=implied_prob,
        sigma=sigma,
        time_remaining=time_remaining,
        greeks=greeks,
    )
