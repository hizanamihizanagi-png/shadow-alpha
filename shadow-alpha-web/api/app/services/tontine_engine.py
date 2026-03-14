"""
Tontine Engine — group management, contributions, and rotation.
"""

from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.error_handler import DuplicateError, NotFoundError, ValidationError
from app.models.tontine import (
    MemberRole,
    TontineContribution,
    TontineGroup,
    TontineMember,
    TontineStatus,
)


class TontineEngineService:
    """Manages tontine group lifecycle, membership, and contributions."""

    @classmethod
    async def create_group(
        cls,
        db: AsyncSession,
        name: str,
        creator_id: uuid.UUID,
        cycle_type: str,
        target_amount: Decimal,
        description: str | None = None,
    ) -> TontineGroup:
        group = TontineGroup(
            name=name,
            creator_id=creator_id,
            cycle_type=cycle_type,
            target_amount=target_amount,
            description=description,
        )
        db.add(group)
        await db.flush()

        # Creator is auto-joined as creator role
        member = TontineMember(
            group_id=group.id,
            user_id=creator_id,
            role=MemberRole.CREATOR,
        )
        db.add(member)
        await db.flush()

        return group

    @classmethod
    async def join_group(
        cls,
        db: AsyncSession,
        group_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> TontineMember:
        # Verify group exists
        grp_result = await db.execute(
            select(TontineGroup).where(TontineGroup.id == group_id)
        )
        group = grp_result.scalar_one_or_none()
        if not group:
            raise NotFoundError("TontineGroup", str(group_id))
        if group.status != TontineStatus.ACTIVE:
            raise ValidationError("Group is not accepting members")

        # Check not already member
        existing = await db.execute(
            select(TontineMember).where(
                and_(TontineMember.group_id == group_id, TontineMember.user_id == user_id)
            )
        )
        if existing.scalar_one_or_none():
            raise DuplicateError("TontineMember", "user_id", str(user_id))

        member = TontineMember(
            group_id=group_id,
            user_id=user_id,
            role=MemberRole.MEMBER,
        )
        db.add(member)
        await db.flush()
        return member

    @classmethod
    async def contribute(
        cls,
        db: AsyncSession,
        group_id: uuid.UUID,
        user_id: uuid.UUID,
        amount: Decimal,
    ) -> TontineContribution:
        # Verify membership
        member_result = await db.execute(
            select(TontineMember).where(
                and_(TontineMember.group_id == group_id, TontineMember.user_id == user_id)
            )
        )
        member = member_result.scalar_one_or_none()
        if not member:
            raise ValidationError("You are not a member of this group")

        contribution = TontineContribution(
            group_id=group_id,
            user_id=user_id,
            amount=amount,
        )
        db.add(contribution)

        # Update member total
        member.contribution_total += amount

        # Update group total
        grp_result = await db.execute(
            select(TontineGroup).where(TontineGroup.id == group_id)
        )
        group = grp_result.scalar_one()
        group.current_amount += amount

        await db.flush()
        return contribution

    @classmethod
    async def get_user_groups(
        cls,
        db: AsyncSession,
        user_id: uuid.UUID,
    ) -> list[TontineGroup]:
        result = await db.execute(
            select(TontineGroup)
            .join(TontineMember, TontineMember.group_id == TontineGroup.id)
            .where(TontineMember.user_id == user_id)
        )
        return list(result.scalars().all())

    @classmethod
    async def get_ledger(
        cls,
        db: AsyncSession,
        group_id: uuid.UUID,
    ) -> list[TontineContribution]:
        result = await db.execute(
            select(TontineContribution)
            .where(TontineContribution.group_id == group_id)
            .order_by(TontineContribution.created_at.desc())
        )
        return list(result.scalars().all())
