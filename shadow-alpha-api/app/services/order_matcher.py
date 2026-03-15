"""
Order Matcher - price-time priority matching engine for the P2P exchange.
"""

from __future__ import annotations

import uuid
from decimal import ROUND_HALF_EVEN, Decimal
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.error_handler import NotFoundError, ValidationError
from app.models.order import Order, OrderStatus, OrderType, Trade
from app.models.position import Position, PositionStatus
from app.models.wealth_engine import RevenueMechanism
from app.services.revenue_ledger import RevenueLedgerService


class OrderMatcherService:
    """Price-time priority order matching for the P2P position exchange."""

    TRADE_FEE_PCT = Decimal("2.00")  # 2% platform fee on trades

    @classmethod
    async def place_order(
        cls,
        db: AsyncSession,
        position_id: uuid.UUID,
        user_id: uuid.UUID,
        order_type: OrderType,
        price: Decimal,
    ) -> Order:
        """Place a new order on the exchange."""
        # Verify position exists and is active
        result = await db.execute(
            select(Position).where(Position.id == position_id)
        )
        position = result.scalar_one_or_none()
        if not position:
            raise NotFoundError("Position", str(position_id))
        if position.status != PositionStatus.ACTIVE:
            raise ValidationError("Position is not active", field="position_id")

        # For sell orders, verify the user owns the position
        if order_type == OrderType.SELL and position.user_id != user_id:
            raise ValidationError("You can only sell positions you own", field="position_id")

        order = Order(
            position_id=position_id,
            seller_id=position.user_id if order_type == OrderType.SELL else user_id,
            buyer_id=user_id if order_type == OrderType.BUY else None,
            order_type=order_type,
            price=price,
            status=OrderStatus.OPEN,
        )
        db.add(order)
        await db.flush()

        # Attempt immediate matching
        await cls._try_match(db, order)

        return order

    @classmethod
    async def _try_match(cls, db: AsyncSession, incoming: Order) -> Optional[Trade]:
        """Try to match an incoming order against the book."""
        if incoming.order_type == OrderType.BUY:
            # Match against sell orders at or below buy price
            result = await db.execute(
                select(Order)
                .where(
                    and_(
                        Order.position_id == incoming.position_id,
                        Order.order_type == OrderType.SELL,
                        Order.status == OrderStatus.OPEN,
                        Order.price <= incoming.price,
                        Order.id != incoming.id,
                    )
                )
                .order_by(Order.price.asc(), Order.created_at.asc())
                .limit(1)
            )
        else:
            # Match against buy orders at or above sell price
            result = await db.execute(
                select(Order)
                .where(
                    and_(
                        Order.position_id == incoming.position_id,
                        Order.order_type == OrderType.BUY,
                        Order.status == OrderStatus.OPEN,
                        Order.price >= incoming.price,
                        Order.id != incoming.id,
                    )
                )
                .order_by(Order.price.desc(), Order.created_at.asc())
                .limit(1)
            )

        match = result.scalar_one_or_none()
        if not match:
            return None

        # Execute trade at the resting order's price
        trade_price = match.price
        fee = (trade_price * cls.TRADE_FEE_PCT / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_EVEN
        )

        # Determine buyer/seller
        if incoming.order_type == OrderType.BUY:
            buyer_id = incoming.buyer_id or incoming.seller_id
            seller_id = match.seller_id
        else:
            buyer_id = match.buyer_id or match.seller_id
            seller_id = incoming.seller_id

        trade = Trade(
            order_id=incoming.id,
            buyer_id=buyer_id,
            seller_id=seller_id,
            price=trade_price,
            fee=fee,
        )
        db.add(trade)

        # Log fee to revenue ledger
        if fee > Decimal("0.00"):
            await RevenueLedgerService.record(
                db,
                mechanism=RevenueMechanism.TRANSACTION_FEE,
                amount=fee,
                description=f"Trade fee {cls.TRADE_FEE_PCT}% on {trade_price}",
                reference_id=str(incoming.id),
            )

        # Update order statuses
        incoming.status = OrderStatus.FILLED
        match.status = OrderStatus.FILLED

        # Transfer position ownership
        position_result = await db.execute(
            select(Position).where(Position.id == incoming.position_id)
        )
        position = position_result.scalar_one()
        position.user_id = buyer_id
        position.current_value = trade_price

        await db.flush()
        return trade

    @classmethod
    async def cancel_order(
        cls,
        db: AsyncSession,
        order_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Order:
        """Cancel an open order."""
        result = await db.execute(
            select(Order).where(Order.id == order_id)
        )
        order = result.scalar_one_or_none()
        if not order:
            raise NotFoundError("Order", str(order_id))
        if order.seller_id != user_id and order.buyer_id != user_id:
            raise ValidationError("You cannot cancel this order")
        if order.status != OrderStatus.OPEN:
            raise ValidationError("Only open orders can be cancelled")

        order.status = OrderStatus.CANCELLED
        await db.flush()
        return order

    @classmethod
    async def get_orderbook(
        cls,
        db: AsyncSession,
        position_id: uuid.UUID,
    ) -> dict:
        """Get the order book for a position (bids + asks)."""
        bids_result = await db.execute(
            select(Order)
            .where(
                and_(
                    Order.position_id == position_id,
                    Order.order_type == OrderType.BUY,
                    Order.status == OrderStatus.OPEN,
                )
            )
            .order_by(Order.price.desc())
            .limit(50)
        )
        asks_result = await db.execute(
            select(Order)
            .where(
                and_(
                    Order.position_id == position_id,
                    Order.order_type == OrderType.SELL,
                    Order.status == OrderStatus.OPEN,
                )
            )
            .order_by(Order.price.asc())
            .limit(50)
        )

        return {
            "bids": [{"price": str(o.price), "id": str(o.id)} for o in bids_result.scalars().all()],
            "asks": [{"price": str(o.price), "id": str(o.id)} for o in asks_result.scalars().all()],
        }

