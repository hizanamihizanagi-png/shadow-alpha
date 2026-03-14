"""
Tests for the health endpoint and system checks.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Health check should return ok (with mocked Redis)."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("ok", "degraded")
    assert "db" in data
    assert "redis" in data
