"""
Shield Router - insurance activation and claims.
"""

from __future__ import annotations

import uuid
from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.auth import get_current_user
from app.models.shield import (
    ShieldActivate,
    ShieldClaimOut,
    ShieldContract,
    ShieldContractOut,
    ShieldQuoteOut,
)
from app.models.user import User
from app.services.shield_engine import ShieldEngineService
from app.services.pricing_engine import PricingEngineService

router = APIRouter()


@router.post("/activate", response_model=ShieldContractOut, status_code=201)
async def activate_shield(
    payload: ShieldActivate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ShieldContractOut:
    """Activate Shield insurance on a position."""
    contract = await ShieldEngineService.activate_shield(
        db, payload.position_id, current_user.id, payload.coverage_pct,
    )
    return ShieldContractOut.model_validate(contract)


@router.post("/claim/{contract_id}", response_model=ShieldClaimOut)
async def process_claim(
    contract_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ShieldClaimOut:
    """Process a shield insurance claim."""
    claim = await ShieldEngineService.process_claim(db, contract_id)
    return ShieldClaimOut.model_validate(claim)


@router.get("/quote", response_model=ShieldQuoteOut)
async def get_quote(
    position_id: uuid.UUID,
    coverage_pct: float = 70.0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ShieldQuoteOut:
    """Get a Shield insurance premium quote."""
    from app.models.position import Position
    from sqlalchemy import select
    from app.middleware.error_handler import NotFoundError

    result = await db.execute(select(Position).where(Position.id == position_id))
    position = result.scalar_one_or_none()
    if not position:
        raise NotFoundError("Position", str(position_id))

    implied_prob = PricingEngineService.odds_to_implied_prob(float(position.odds))
    loss_prob = 1.0 - implied_prob

    pricing = ShieldEngineService.calculate_premium(
        position.stake, loss_prob, Decimal(str(coverage_pct)),
    )

    return ShieldQuoteOut(
        position_id=position_id,
        premium=pricing["premium"],
        coverage_pct=Decimal(str(coverage_pct)),
        estimated_payout=pricing["estimated_payout"],
        loss_probability=loss_prob,
    )


@router.get("/my", response_model=List[ShieldContractOut])
async def get_my_contracts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[ShieldContractOut]:
    """List shield contracts for the current user."""
    result = await db.execute(
        select(ShieldContract)
        .where(ShieldContract.user_id == current_user.id)
        .order_by(ShieldContract.created_at.desc())
    )
    return [ShieldContractOut.model_validate(c) for c in result.scalars().all()]

