"""
Tests for auth endpoints — register, login, me.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Should register a new user and return 201."""
    response = await client.post("/auth/register", json={
        "email": "newuser@shadowalpha.io",
        "display_name": "New User",
        "password": "securepassword123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@shadowalpha.io"
    assert data["display_name"] == "New User"
    assert data["tier"] == "free"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Should reject duplicate email with 409."""
    payload = {
        "email": "dup@shadowalpha.io",
        "display_name": "User A",
        "password": "password123!",
    }
    await client.post("/auth/register", json=payload)
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Should login and return JWT token pair."""
    # Register first
    await client.post("/auth/register", json={
        "email": "login@shadowalpha.io",
        "display_name": "Login User",
        "password": "mypassword123",
    })

    # Login
    response = await client.post("/auth/login", json={
        "email": "login@shadowalpha.io",
        "password": "mypassword123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    """Should reject invalid password with 401."""
    await client.post("/auth/register", json={
        "email": "wrongpass@shadowalpha.io",
        "display_name": "Wrong Pass",
        "password": "correctpassword",
    })

    response = await client.post("/auth/login", json={
        "email": "wrongpass@shadowalpha.io",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, auth_headers: dict):
    """Should return current user profile."""
    response = await client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@shadowalpha.io"
    assert data["display_name"] == "Test User"


@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    """Should reject unauthenticated request."""
    response = await client.get("/auth/me")
    assert response.status_code in (401, 403)  # No auth header
