"""
ShadowAlpha API — main application entry point.

SHADOW CORE: the invisible infrastructure that makes ShadowAlpha elite.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.session import engine, create_all_tables

logger = structlog.get_logger()


# ── Lifespan ──────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    # Startup
    logger.info("shadow_core.starting", version=settings.APP_VERSION)

    # Auto-create tables for SQLite dev
    _is_sqlite = settings.DATABASE_URL.startswith("sqlite")
    if _is_sqlite:
        await create_all_tables()
        logger.info("shadow_core.sqlite_tables_created")
    else:
        # PostgreSQL — verify connectivity
        import sqlalchemy
        async with engine.begin() as conn:
            await conn.execute(sqlalchemy.text("SELECT 1"))
        logger.info("shadow_core.db_connected")

    # Redis connectivity (optional for dev)
    try:
        import redis.asyncio as aioredis
        redis_client = aioredis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        app.state.redis = redis_client
        logger.info("shadow_core.redis_connected")
    except Exception:
        # Redis is optional for local dev
        class FakeRedis:
            async def ping(self): return True
            async def close(self): pass
            async def get(self, *a, **kw): return None
            async def set(self, *a, **kw): return None
            async def incr(self, *a, **kw): return 1
            async def expire(self, *a, **kw): return None

        app.state.redis = FakeRedis()
        logger.warning("shadow_core.redis_unavailable", msg="Using fake Redis for development")

    yield

    # Shutdown
    if hasattr(app.state, "redis") and hasattr(app.state.redis, "close"):
        try:
            await app.state.redis.close()
        except Exception:
            pass
    await engine.dispose()
    logger.info("shadow_core.shutdown")


# ── App ───────────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "ShadowAlpha — Elite Quantitative Trading Platform API. "
        "Positions, P2P Exchange, Tontine, Credit, Vault, Shield Insurance, and more."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ────────────────────────────────────────────────────────────────
@app.get("/health", tags=["system"])
async def health_check():
    """System health check — verifies DB and Redis are reachable."""
    import sqlalchemy

    db_status = "connected"
    try:
        async with engine.begin() as conn:
            await conn.execute(sqlalchemy.text("SELECT 1"))
    except Exception:
        db_status = "disconnected"

    redis_status = "connected"
    try:
        await app.state.redis.ping()
    except Exception:
        redis_status = "disconnected"

    status = "ok" if db_status == "connected" else "degraded"
    return {"status": status, "db": db_status, "redis": redis_status}


# ── Routers ───────────────────────────────────────────────────────────────
from app.routers import (  # noqa: E402
    admin,
    auth,
    credit,
    exchange,
    gratitude,
    portfolio,
    position_loans,
    positions,
    public_api,
    shield,
    subscription,
    tontine,
    vault,
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(positions.router, prefix="/positions", tags=["positions"])
app.include_router(exchange.router, prefix="/exchange", tags=["exchange"])
app.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
app.include_router(tontine.router, prefix="/tontine", tags=["tontine"])
app.include_router(credit.router, prefix="/credit", tags=["credit"])
app.include_router(vault.router, prefix="/vault", tags=["vault"])
app.include_router(shield.router, prefix="/shield", tags=["shield"])
app.include_router(gratitude.router, prefix="/gratitude", tags=["gratitude"])
app.include_router(position_loans.router, prefix="/loans", tags=["loans"])
app.include_router(subscription.router, prefix="/subscription", tags=["subscription"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(public_api.router, prefix="/v1", tags=["public-api"])
