"""
Vault Router - Shadow Vault deposits, withdrawals, and performance.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.vault import VaultDepositCreate, VaultDepositOut, VaultPerformanceOut, VaultWithdraw
from app.services.vault_engine import VaultEngineService

router = APIRouter()


@router.post("/deposit", response_model=VaultDepositOut, status_code=201)
async def vault_deposit(
    payload: VaultDepositCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> VaultDepositOut:
    """Deposit capital into the Shadow Vault yield fund."""
    deposit = await VaultEngineService.deposit(db, current_user.id, payload.amount)
    return VaultDepositOut.model_validate(deposit)


@router.post("/withdraw", response_model=VaultDepositOut)
async def vault_withdraw(
    payload: VaultWithdraw,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> VaultDepositOut:
    """Withdraw capital from the Shadow Vault."""
    deposit = await VaultEngineService.withdraw(db, payload.deposit_id, current_user.id)
    return VaultDepositOut.model_validate(deposit)


@router.get("/performance", response_model=VaultPerformanceOut)
async def vault_performance(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> VaultPerformanceOut:
    """Get vault performance and yield data."""
    data = await VaultEngineService.get_performance(db, current_user.id)
    return VaultPerformanceOut(**data)

