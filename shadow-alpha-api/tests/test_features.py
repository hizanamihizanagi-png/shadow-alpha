"""
Tests for vault, shield, gratitude, and public API endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_vault_deposit(client: AsyncClient, auth_headers: dict):
    """Should deposit into the Shadow Vault."""
    response = await client.post("/vault/deposit", json={
        "amount": "50000.00",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "active"
    assert float(data["amount"]) == 50000.0


@pytest.mark.asyncio
async def test_vault_performance(client: AsyncClient, auth_headers: dict):
    """Should return vault performance data."""
    # Deposit first
    await client.post("/vault/deposit", json={"amount": "100000.00"}, headers=auth_headers)

    response = await client.get("/vault/performance", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_deposited" in data
    assert "net_yield" in data
    assert "apy_estimate" in data


@pytest.mark.asyncio
async def test_gratitude_tip(client: AsyncClient, auth_headers: dict):
    """Should record a gratitude tip."""
    response = await client.post("/gratitude/tip", json={
        "win_amount": "100000.00",
        "tip_pct": "10.00",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert float(data["tip_amount"]) == 10000.0
    assert float(data["tip_pct"]) == 10.0


@pytest.mark.asyncio
async def test_supporters_leaderboard(client: AsyncClient, auth_headers: dict):
    """Should return supporters leaderboard."""
    # Create a tip first
    await client.post("/gratitude/tip", json={
        "win_amount": "50000.00",
        "tip_pct": "5.00",
    }, headers=auth_headers)

    response = await client.get("/gratitude/supporters", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_public_api_evaluate(client: AsyncClient):
    """Public API: evaluate a position (no auth required for public)."""
    response = await client.post("/v1/positions/evaluate", json={
        "sportsbook": "1xBet",
        "teams": "Liverpool vs Chelsea",
        "odds": 2.10,
        "stake": 10000,
        "current_prob": 0.55,
        "time_remaining": 0.75,
    })
    assert response.status_code == 200
    data = response.json()
    assert "fair_value" in data
    assert "ev" in data
    assert "kelly_fraction" in data
    assert "greeks" in data


@pytest.mark.asyncio
async def test_public_api_kelly(client: AsyncClient):
    """Public API: Kelly criterion calculation."""
    response = await client.post("/v1/analytics/kelly", json={
        "odds": 2.50,
        "probability": 0.45,
        "bankroll": 100000,
        "fraction": 0.25,
    })
    assert response.status_code == 200
    data = response.json()
    assert "optimal_stake" in data
    assert "recommendation" in data


@pytest.mark.asyncio
async def test_public_api_live_price(client: AsyncClient):
    """Public API: live position price."""
    response = await client.get("/v1/positions/price", params={
        "odds": 2.0,
        "current_prob": 0.55,
        "time_remaining": 0.75,
        "max_payout": 1000,
    })
    assert response.status_code == 200
    data = response.json()
    assert "fair_value" in data
    assert data["fair_value"] > 0


@pytest.mark.asyncio
async def test_credit_score(client: AsyncClient, auth_headers: dict):
    """Should return a credit score."""
    response = await client.get("/credit/score", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "tier" in data
    assert data["score"] >= 0


@pytest.mark.asyncio
async def test_portfolio_summary(client: AsyncClient, auth_headers: dict):
    """Should return portfolio summary."""
    response = await client.get("/portfolio/summary", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_value" in data
    assert "position_count" in data


@pytest.mark.asyncio
async def test_admin_requires_auth(client: AsyncClient, auth_headers: dict):
    """Admin endpoints should reject non-admin users."""
    response = await client.get("/admin/float-status", headers=auth_headers)
    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_admin_revenue_streams(client: AsyncClient, admin_headers: dict):
    """Admin: revenue streams breakdown."""
    response = await client.get("/admin/revenue-streams", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert "mechanisms" in data
    assert "total_revenue" in data
    assert isinstance(data["mechanisms"], list)
