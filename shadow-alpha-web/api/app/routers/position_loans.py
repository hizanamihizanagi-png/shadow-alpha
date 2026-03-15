"""
Position Loans Router - Lombard lending against position collateral.
Uses PositionLoanService for Black-Scholes collateral valuation + revenue logging.
"""

from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.auth import get_current_user
from app.models.position_loan import PositionLoanCreate, PositionLoanOut
from app.models.user import User
from app.services.position_loan_service import PositionLoanService

router = APIRouter()


@router.get("/quote/{position_id}")
async def get_loan_quote(
    position_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Get a loan quote for a position (how much you can borrow)."""
    return await PositionLoanService.calculate_loan(db, position_id)


@router.post("/position-collateral", response_model=PositionLoanOut, status_code=201)
async def create_position_loan(
    payload: PositionLoanCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PositionLoanOut:
    """Borrow cash by collateralizing an active position (max 60% LTV).
    Auto-logs fee to revenue ledger.
    """
    loan = await PositionLoanService.disburse_loan(
        db, payload.position_id, current_user.id, payload.loan_pct,
    )
    return PositionLoanOut.model_validate(loan)


@router.post("/repay/{loan_id}")
async def repay_position_loan(
    loan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Repay a position-collateralized loan and unlock the position."""
    from datetime import datetime, timezone
    from sqlalchemy import select
    from app.models.position_loan import PositionLoan, PositionLoanStatus
    from app.models.position import Position, PositionStatus
    from app.middleware.error_handler import NotFoundError, ValidationError

    result = await db.execute(
        select(PositionLoan).where(PositionLoan.id == loan_id)
    )
    loan = result.scalar_one_or_none()
    if not loan:
        raise NotFoundError("PositionLoan", str(loan_id))
    if loan.user_id != current_user.id:
        raise ValidationError("You can only repay your own loans")
    if loan.status != PositionLoanStatus.ACTIVE:
        raise ValidationError("Loan is not active")

    loan.status = PositionLoanStatus.REPAID
    loan.repaid_at = datetime.now(timezone.utc)

    # Unlock position
    pos_result = await db.execute(
        select(Position).where(Position.id == loan.position_id)
    )
    position = pos_result.scalar_one_or_none()
    if position and position.status == PositionStatus.LOCKED:
        position.status = PositionStatus.ACTIVE

    await db.flush()
    return {"message": "Position loan repaid, position unlocked", "loan_id": str(loan.id)}


@router.get("/my-loans", response_model=List[PositionLoanOut])
async def get_my_position_loans(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[PositionLoanOut]:
    """Get all your position-collateralized loans."""
    loans = await PositionLoanService.get_user_loans(db, current_user.id)
    return [PositionLoanOut.model_validate(lo) for lo in loans]

