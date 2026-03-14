"""
Application configuration — loaded from environment variables.
All secrets and connection strings come from here, never hardcoded.
"""

from __future__ import annotations

import json
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Typed application settings with sensible development defaults."""

    # ── Database ──────────────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./shadow_alpha.db"

    # ── Redis ─────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── JWT Authentication ────────────────────────────────────────────────
    JWT_SECRET: str = "dev-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRY_MINUTES: int = 30
    JWT_REFRESH_EXPIRY_DAYS: int = 7

    # ── CORS ──────────────────────────────────────────────────────────────
    CORS_ORIGINS: str = '["http://localhost:3000"]'

    @property
    def cors_origins_list(self) -> List[str]:
        return json.loads(self.CORS_ORIGINS)

    # ── General ───────────────────────────────────────────────────────────
    APP_NAME: str = "ShadowAlpha API"
    APP_VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False

    # ── Rate Limiting ─────────────────────────────────────────────────────
    RATE_LIMIT_PER_MINUTE: int = 60

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
