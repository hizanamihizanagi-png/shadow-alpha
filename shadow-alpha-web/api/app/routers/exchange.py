"""
Exchange Router - order book, order placement, cancellation, trades.
"""

from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.auth import get_current_user
from app.models.order import OrderCreate, OrderOut, Trade, TradeOut
from app.models.user import User
from app.services.order_matcher import OrderMatcherService
from app.services.market_maker import MarketMakerService
from app.services.pricing_engine import PricingEngineService

router = APIRouter()


@router.get("/orderbook")
async def get_orderbook(
    position_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Get the order book for a position."""
    return await OrderMatcherService.get_orderbook(db, position_id)


@router.post("/place-order", response_model=OrderOut, status_code=201)
async def place_order(
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderOut:
    """Place a buy or sell order on the exchange."""
    order = await OrderMatcherService.place_order(
        db, payload.position_id, current_user.id, payload.order_type, payload.price,
    )
    return OrderOut.model_validate(order)


@router.delete("/cancel/{order_id}", response_model=OrderOut)
async def cancel_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderOut:
    """Cancel an open order."""
    order = await OrderMatcherService.cancel_order(db, order_id, current_user.id)
    return OrderOut.model_validate(order)


@router.get("/my-orders", response_model=List[OrderOut])
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[OrderOut]:
    """List all orders for the current user."""
    from app.models.order import Order
    from sqlalchemy import or_

    result = await db.execute(
        select(Order)
        .where(
            or_(Order.seller_id == current_user.id, Order.buyer_id == current_user.id)
        )
        .order_by(Order.created_at.desc())
    )
    return [OrderOut.model_validate(o) for o in result.scalars().all()]


@router.get("/trades", response_model=List[TradeOut])
async def get_trades(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[TradeOut]:
    """List all trades for the current user."""
    from sqlalchemy import or_

    result = await db.execute(
        select(Trade)
        .where(
            or_(Trade.buyer_id == current_user.id, Trade.seller_id == current_user.id)
        )
        .order_by(Trade.created_at.desc())
    )
    return [TradeOut.model_validate(t) for t in result.scalars().all()]


@router.get("/instant-cashout/quote")
async def instant_cashout_quote(
    position_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Get an instant cashout quote for a position."""
    from app.models.position import Position
    from app.middleware.error_handler import NotFoundError, ValidationError
    from app.models.position import PositionStatus

    result = await db.execute(select(Position).where(Position.id == position_id))
    position = result.scalar_one_or_none()
    if not position:
        raise NotFoundError("Position", str(position_id))
    if position.user_id != current_user.id:
        raise ValidationError("You can only cashout your own positions")
    if position.status != PositionStatus.ACTIVE:
        raise ValidationError("Position must be active")

    implied_prob = PricingEngineService.odds_to_implied_prob(float(position.odds))
    current_prob = position.current_prob or implied_prob
    time_remaining = position.time_remaining or 0.5
    sigma = PricingEngineService.get_sigma("football")

    quote = MarketMakerService.instant_cashout_quote(
        current_prob, implied_prob, sigma, time_remaining,
        position.max_payout, position.stake,
    )
    quote["position_id"] = str(position_id)
    return quote


@router.post("/instant-cashout/execute")
async def execute_instant_cashout(
    position_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Execute instant cashout - sell position to the platform at quoted price."""
    from decimal import Decimal
    from app.models.position import Position, PositionStatus
    from app.middleware.error_handler import NotFoundError, ValidationError
    from app.models.wealth_engine import InstantCashout, InstantCashoutStatus, RevenueMechanism
    from app.services.revenue_ledger import RevenueLedgerService

    result = await db.execute(select(Position).where(Position.id == position_id))
    position = result.scalar_one_or_none()
    if not position:
        raise NotFoundError("Position", str(position_id))
    if position.user_id != current_user.id:
        raise ValidationError("You can only cashout your own positions")
    if position.status != PositionStatus.ACTIVE:
        raise ValidationError("Position must be active")

    # Get quote
    implied_prob = PricingEngineService.odds_to_implied_prob(float(position.odds))
    current_prob = position.current_prob or implied_prob
    time_remaining = position.time_remaining or 0.5
    sigma = PricingEngineService.get_sigma("football")

    quote = MarketMakerService.instant_cashout_quote(
        current_prob, implied_prob, sigma, time_remaining,
        position.max_payout, position.stake,
    )

    # Record cashout
    cashout = InstantCashout(
        position_id=position_id,
        user_id=current_user.id,
        fair_value=quote["fair_value"],
        offered_price=quote["offered_price"],
        spread_pct=quote["spread_pct"],
        status=InstantCashoutStatus.COMPLETED,
    )
    db.add(cashout)

    # Mark position as sold
    position.status = PositionStatus.SOLD
    position.current_value = quote["offered_price"]

    # Log spread revenue
    spread_revenue = quote["spread_amount"]
    if spread_revenue > Decimal("0.00"):
        await RevenueLedgerService.record(
            db,
            mechanism=RevenueMechanism.MARKET_MAKING,
            amount=spread_revenue,
            description=f"Instant cashout spread on position",
            reference_id=str(position_id),
        )

    await db.flush()
    return {
        "message": "Position sold via instant cashout",
        "cashout_id": str(cashout.id),
        **quote,
    }

