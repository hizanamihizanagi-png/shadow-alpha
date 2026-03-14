"""
Tests for position and exchange endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_position(client: AsyncClient, auth_headers: dict):
    """Should create a new position."""
    response = await client.post("/positions/create", json={
        "sportsbook": "1xBet",
        "teams": "PSG vs Marseille",
        "odds": "2.50",
        "stake": "10000.00",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["sportsbook"] == "1xBet"
    assert data["teams"] == "PSG vs Marseille"
    assert data["status"] == "active"
    assert float(data["max_payout"]) == 25000.0


@pytest.mark.asyncio
async def test_get_my_positions(client: AsyncClient, auth_headers: dict):
    """Should list user's positions."""
    # Create a position first
    await client.post("/positions/create", json={
        "sportsbook": "Melbet",
        "teams": "Real vs Barca",
        "odds": "1.80",
        "stake": "5000.00",
    }, headers=auth_headers)

    response = await client.get("/positions/my", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_create_position_unauthorized(client: AsyncClient):
    """Should reject unauthenticated position creation."""
    response = await client.post("/positions/create", json={
        "sportsbook": "Test",
        "teams": "A vs B",
        "odds": "2.00",
        "stake": "1000.00",
    })
    assert response.status_code in (401, 403)
