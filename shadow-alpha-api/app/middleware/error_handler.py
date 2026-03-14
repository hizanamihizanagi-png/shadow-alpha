"""
Structured error handling for the API.
"""

from __future__ import annotations

from typing import Optional

from fastapi import HTTPException


class ShadowAlphaError(HTTPException):
    """Base structured error for all ShadowAlpha API errors."""

    def __init__(
        self,
        error: str,
        message: str,
        code: int = 400,
        field: Optional[str] = None,
    ):
        detail = {
            "error": error,
            "message": message,
            "code": code,
        }
        if field:
            detail["field"] = field
        super().__init__(status_code=code, detail=detail)


# ── Common errors ─────────────────────────────────────────────────────────

class NotFoundError(ShadowAlphaError):
    def __init__(self, resource: str, id: str):
        super().__init__(
            error="NOT_FOUND",
            message=f"{resource} with id '{id}' not found",
            code=404,
        )


class InsufficientFundsError(ShadowAlphaError):
    def __init__(self, required: str, available: str):
        super().__init__(
            error="INSUFFICIENT_FUNDS",
            message=f"Required {required} FCFA, available {available} FCFA",
            code=422,
            field="amount",
        )


class InsufficientMarginError(ShadowAlphaError):
    def __init__(self, required: str, available: str):
        super().__init__(
            error="INSUFFICIENT_MARGIN",
            message=f"Position requires {required} FCFA margin, account has {available} FCFA",
            code=422,
            field="margin",
        )


class DuplicateError(ShadowAlphaError):
    def __init__(self, resource: str, field: str, value: str):
        super().__init__(
            error="DUPLICATE",
            message=f"{resource} with {field} '{value}' already exists",
            code=409,
            field=field,
        )


class ForbiddenError(ShadowAlphaError):
    def __init__(self, message: str = "You do not have permission to perform this action"):
        super().__init__(
            error="FORBIDDEN",
            message=message,
            code=403,
        )


class ValidationError(ShadowAlphaError):
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            error="VALIDATION_ERROR",
            message=message,
            code=422,
            field=field,
        )
