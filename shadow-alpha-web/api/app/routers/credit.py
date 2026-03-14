"""
Credit Router — credit score, loan application, repayment.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.auth import get_current_user
from app.middleware.error_handler import NotFoundError, ValidationError
from app.models.loan import Loan, LoanApply, LoanOut, LoanRepay, LoanStatus
from app.models.user import User
from app.services.credit_scorer import CreditScorerService

router = APIRouter()


@router.get("/score")
async def get_credit_score(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Get your credit score."""
    return await CreditScorerService.compute_score(db, current_user.id)


@router.post("/apply", response_model=LoanOut, status_code=201)
async def apply_for_loan(
    payload: LoanApply,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LoanOut:
    """Apply for a credit loan."""
    eligibility = await CreditScorerService.check_eligibility(
        db, current_user.id, payload.amount,
    )
    if not eligibility["eligible"]:
        raise ValidationError(eligibility["reason"], field="amount")

    loan = Loan(
        user_id=current_user.id,
        amount=payload.amount,
        interest_rate=eligibility["interest_rate"],
        status=LoanStatus.ACTIVE,
        due_date=datetime.now(timezone.utc) + timedelta(days=30),
    )
    db.add(loan)
    await db.flush()
    return LoanOut.model_validate(loan)


@router.get("/my-loans", response_model=List[LoanOut])
async def get_my_loans(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[LoanOut]:
    """List all your loans."""
    result = await db.execute(
        select(Loan)
        .where(Loan.user_id == current_user.id)
        .order_by(Loan.created_at.desc())
    )
    return [LoanOut.model_validate(lo) for lo in result.scalars().all()]


@router.post("/repay")
async def repay_loan(
    payload: LoanRepay,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Repay a loan."""
    result = await db.execute(
        select(Loan).where(Loan.id == payload.loan_id)
    )
    loan = result.scalar_one_or_none()
    if not loan:
        raise NotFoundError("Loan", str(payload.loan_id))
    if loan.user_id != current_user.id:
        raise ValidationError("You can only repay your own loans")
    if loan.status != LoanStatus.ACTIVE:
        raise ValidationError("Loan is not active")

    loan.status = LoanStatus.REPAID
    loan.repaid_at = datetime.now(timezone.utc)
    await db.flush()
    return {"message": "Loan repaid successfully", "loan_id": str(loan.id)}
