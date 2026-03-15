"""
Test configuration - async test fixtures using SQLite in-memory.
"""

from __future__ import annotations

import uuid
from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app as fastapi_app
from app.middleware.auth import create_access_token, hash_password

# Import all models so tables are registered with Base.metadata
import app.models  # noqa: F401


# ── Test DB engine (SQLite in-memory) ─────────────────────────────────────
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
test_session_factory = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False,
)


# ── Fixtures ──────────────────────────────────────────────────────────────
@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create tables and yield a fresh session per test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_session_factory() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP test client with overridden DB dependency."""

    async def override_get_db():
        yield db_session

    fastapi_app.dependency_overrides[get_db] = override_get_db

    # Mock Redis on app.state
    class FakeRedis:
        async def ping(self):
            return True
        async def close(self):
            pass
        async def get(self, *a, **kw):
            return None
        async def set(self, *a, **kw):
            return None
        async def incr(self, *a, **kw):
            return 1
        async def expire(self, *a, **kw):
            return None

    fastapi_app.state.redis = FakeRedis()

    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    fastapi_app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession):
    """Create a test user and return it."""
    from app.models.user import User

    user = User(
        id=uuid.uuid4(),
        email="test@shadowalpha.io",
        display_name="Test User",
        hashed_password=hash_password("testpassword123"),
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest_asyncio.fixture
async def auth_headers(test_user) -> dict:
    """Return Authorization headers with a valid JWT."""
    token = create_access_token(test_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def admin_user(db_session: AsyncSession):
    """Create an admin user."""
    from app.models.user import User

    user = User(
        id=uuid.uuid4(),
        email="admin@shadowalpha.io",
        display_name="Admin",
        hashed_password=hash_password("adminpassword123"),
        is_active=True,
        is_admin=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest_asyncio.fixture
async def admin_headers(admin_user) -> dict:
    """Return Authorization headers for admin."""
    token = create_access_token(admin_user.id)
    return {"Authorization": f"Bearer {token}"}

