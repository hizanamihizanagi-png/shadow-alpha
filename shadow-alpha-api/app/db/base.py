"""
Database base — declarative base class, common mixins, and DB-agnostic UUID type.

Works with both PostgreSQL (production) and SQLite (development/testing).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String, TypeDecorator, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# ── DB-agnostic UUID column type ──────────────────────────────────────────
class GUID(TypeDecorator):
    """Platform-independent UUID type.

    Uses PostgreSQL's UUID type when available, otherwise stores as
    CHAR(36) in SQLite or other databases.
    """

    impl = String(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if isinstance(value, uuid.UUID):
                return str(value)
            return str(uuid.UUID(value))
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
        return value


# ── Base ──────────────────────────────────────────────────────────────────
class Base(DeclarativeBase):
    """Declarative base for all models."""
    pass


# ── Mixins ────────────────────────────────────────────────────────────────
class TimestampMixin:
    """Adds created_at / updated_at columns to any model."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UUIDPrimaryKeyMixin:
    """UUID v4 primary key mixin — works on both PostgreSQL and SQLite."""

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
    )
