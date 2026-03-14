"""
Gratitude Router — tips and supporter leaderboard.
Uses GratitudeService for revenue ledger integration.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.auth import get_current_user
from app.models.gratitude import GratitudeTipCreate, GratitudeTipOut, SupporterOut
from app.models.user import User
from app.services.gratitude_service import GratitudeService

router = APIRouter()


@router.post("/tip", response_model=GratitudeTipOut, status_code=201)
async def create_tip(
    payload: GratitudeTipCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> GratitudeTipOut:
    """Record a gratitude tip after a win (auto-logs to revenue ledger)."""
    tip = await GratitudeService.record_tip(
        db, current_user.id, payload.win_amount, payload.tip_pct,
    )
    return GratitudeTipOut.model_validate(tip)


@router.get("/supporters", response_model=List[SupporterOut])
async def get_supporters(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[SupporterOut]:
    """Get the top supporters leaderboard with badges."""
    supporters = await GratitudeService.get_supporters_leaderboard(db)
    return [SupporterOut(**s) for s in supporters]


@router.get("/my-tips", response_model=List[GratitudeTipOut])
async def get_my_tips(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[GratitudeTipOut]:
    """Get your tip history."""
    tips = await GratitudeService.get_user_tips(db, current_user.id)
    return [GratitudeTipOut.model_validate(t) for t in tips]
