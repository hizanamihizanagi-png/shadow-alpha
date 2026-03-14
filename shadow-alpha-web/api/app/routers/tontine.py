"""
Tontine Router — group management, membership, contributions.
"""

from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.auth import get_current_user
from app.models.tontine import (
    ContributionCreate,
    ContributionOut,
    TontineGroupCreate,
    TontineGroupOut,
    TontineJoin,
)
from app.models.user import User
from app.services.tontine_engine import TontineEngineService

router = APIRouter()


@router.post("/create-group", response_model=TontineGroupOut, status_code=201)
async def create_group(
    payload: TontineGroupCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TontineGroupOut:
    """Create a new tontine group."""
    group = await TontineEngineService.create_group(
        db,
        name=payload.name,
        creator_id=current_user.id,
        cycle_type=payload.cycle_type,
        target_amount=payload.target_amount,
        description=payload.description,
    )
    return TontineGroupOut.model_validate(group)


@router.post("/join")
async def join_group(
    payload: TontineJoin,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Join an existing tontine group."""
    member = await TontineEngineService.join_group(db, payload.group_id, current_user.id)
    return {"message": "Successfully joined group", "member_id": str(member.id)}


@router.post("/contribute", response_model=ContributionOut, status_code=201)
async def contribute(
    payload: ContributionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ContributionOut:
    """Make a contribution to a tontine group."""
    contribution = await TontineEngineService.contribute(
        db, payload.group_id, current_user.id, payload.amount,
    )
    return ContributionOut.model_validate(contribution)


@router.get("/groups/my", response_model=List[TontineGroupOut])
async def get_my_groups(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[TontineGroupOut]:
    """List all tontine groups the user belongs to."""
    groups = await TontineEngineService.get_user_groups(db, current_user.id)
    return [TontineGroupOut.model_validate(g) for g in groups]


@router.get("/{group_id}/ledger", response_model=List[ContributionOut])
async def get_ledger(
    group_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[ContributionOut]:
    """Get the contribution ledger for a tontine group."""
    ledger = await TontineEngineService.get_ledger(db, group_id)
    return [ContributionOut.model_validate(c) for c in ledger]
