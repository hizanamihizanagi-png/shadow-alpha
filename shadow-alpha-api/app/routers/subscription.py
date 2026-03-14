"""
Subscription Router — plan management, upgrade, and billing.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.auth import get_current_user
from app.models.subscription import (
    PlanInfo,
    Subscription,
    SubscriptionOut,
    SubscriptionStatus,
    SubscriptionUpgrade,
)
from app.models.user import SubscriptionTier, User
from app.models.wealth_engine import RevenueMechanism
from app.services.revenue_ledger import RevenueLedgerService

router = APIRouter()

# Plan pricing (FCFA/month) — match actual SubscriptionTier enum
PLAN_PRICING = {
    SubscriptionTier.FREE: 0,
    SubscriptionTier.ALPHA: 2500,
    SubscriptionTier.PREMIER: 7500,
    SubscriptionTier.BLACK_CARD: 25000,
}

PLAN_FEATURES = {
    SubscriptionTier.FREE: [
        "3 positions/day",
        "Basic analytics",
        "Community access",
    ],
    SubscriptionTier.ALPHA: [
        "10 positions/day",
        "Live pricing engine",
        "Credit score access",
        "Tontine groups",
    ],
    SubscriptionTier.PREMIER: [
        "Unlimited positions",
        "Shield insurance",
        "Position loans",
        "Copy-trading",
        "API access (100 req/day)",
    ],
    SubscriptionTier.BLACK_CARD: [
        "Everything in Premier",
        "Priority support",
        "Vault yield boost +1%",
        "API access (10K req/day)",
        "Custom analytics dashboard",
    ],
}


@router.get("/plans", response_model=List[PlanInfo])
async def list_plans() -> List[PlanInfo]:
    """List all available subscription plans."""
    return [
        PlanInfo(
            name=tier,
            price_fcfa=PLAN_PRICING[tier],
            features=PLAN_FEATURES[tier],
        )
        for tier in SubscriptionTier
    ]


@router.get("/current", response_model=SubscriptionOut)
async def get_current_subscription(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SubscriptionOut:
    """Get your current subscription."""
    result = await db.execute(
        select(Subscription)
        .where(
            Subscription.user_id == current_user.id,
            Subscription.status == SubscriptionStatus.ACTIVE,
        )
        .order_by(Subscription.created_at.desc())
        .limit(1)
    )
    sub = result.scalar_one_or_none()

    if not sub:
        # Create default free sub
        sub = Subscription(
            user_id=current_user.id,
            plan=SubscriptionTier.FREE,
            status=SubscriptionStatus.ACTIVE,
            started_at=datetime.now(timezone.utc),
        )
        db.add(sub)
        await db.flush()

    return SubscriptionOut.model_validate(sub)


@router.post("/upgrade", response_model=SubscriptionOut)
async def upgrade_subscription(
    payload: SubscriptionUpgrade,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SubscriptionOut:
    """Upgrade or change subscription plan."""
    from decimal import Decimal

    # Cancel existing active subscription
    result = await db.execute(
        select(Subscription)
        .where(
            Subscription.user_id == current_user.id,
            Subscription.status == SubscriptionStatus.ACTIVE,
        )
    )
    existing = result.scalars().all()
    for s in existing:
        s.status = SubscriptionStatus.CANCELLED

    # Create new subscription
    now = datetime.now(timezone.utc)
    new_sub = Subscription(
        user_id=current_user.id,
        plan=payload.plan,
        status=SubscriptionStatus.ACTIVE,
        started_at=now,
        expires_at=now + timedelta(days=30),
    )
    db.add(new_sub)

    # Log revenue if paid plan
    price = PLAN_PRICING.get(payload.plan, 0)
    if price > 0:
        await RevenueLedgerService.record(
            db,
            mechanism=RevenueMechanism.SUBSCRIPTION,
            amount=Decimal(str(price)),
            description=f"Subscription upgrade to {payload.plan.value}",
            reference_id=str(current_user.id),
        )

    # Update user tier
    current_user.subscription_tier = payload.plan

    await db.flush()
    return SubscriptionOut.model_validate(new_sub)


@router.post("/cancel")
async def cancel_subscription(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Cancel your current subscription."""
    result = await db.execute(
        select(Subscription)
        .where(
            Subscription.user_id == current_user.id,
            Subscription.status == SubscriptionStatus.ACTIVE,
        )
    )
    subs = result.scalars().all()
    for s in subs:
        s.status = SubscriptionStatus.CANCELLED

    # Revert user to free tier
    current_user.subscription_tier = SubscriptionTier.FREE
    await db.flush()
    return {"message": "Subscription cancelled, reverted to Free tier"}
