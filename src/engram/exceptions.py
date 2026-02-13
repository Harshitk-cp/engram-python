"""Engram SDK exceptions."""

from __future__ import annotations

from typing import Any, Optional


class EngramError(Exception):
    """Base exception for all Engram SDK errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class APIError(EngramError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: int,
        body: Optional[Any] = None,
    ) -> None:
        self.status_code = status_code
        self.body = body
        super().__init__(message)

    def __str__(self) -> str:
        return f"[{self.status_code}] {self.message}"


class AuthenticationError(APIError):
    """Raised when the API returns a 401 Unauthorized response."""


class NotFoundError(APIError):
    """Raised when the API returns a 404 Not Found response."""


class ConflictError(APIError):
    """Raised when the API returns a 409 Conflict response."""


class ValidationError(APIError):
    """Raised when the API returns a 400 Bad Request response."""


class ServerError(APIError):
    """Raised when the API returns a 5xx response."""


class ConnectionError(EngramError):
    """Raised when a connection to the API cannot be established."""
