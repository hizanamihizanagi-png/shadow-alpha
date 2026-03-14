"""
Async database session factory and dependency.

Supports both PostgreSQL (production) and SQLite (development).
"""

from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.config import settings

# ── Engine ────────────────────────────────────────────────────────────────
_is_sqlite = settings.DATABASE_URL.startswith("sqlite")

_engine_kwargs = {
    "echo": settings.DEBUG,
}

if _is_sqlite:
    # SQLite requires special handling for async
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
    _engine_kwargs["poolclass"] = StaticPool
else:
    # PostgreSQL pool settings
    _engine_kwargs["pool_size"] = 20
    _engine_kwargs["max_overflow"] = 10
    _engine_kwargs["pool_pre_ping"] = True

engine = create_async_engine(settings.DATABASE_URL, **_engine_kwargs)

# ── Session factory ───────────────────────────────────────────────────────
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ── FastAPI dependency ────────────────────────────────────────────────────
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session, auto-close on exit."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ── Table creation helper (for development) ──────────────────────────────
async def create_all_tables():
    """Create all tables — used for SQLite dev and testing."""
    # Import all models to register them with Base.metadata
    import app.models  # noqa: F401
    from app.db.base import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
