"""Engram — Python SDK for cognitive memory infrastructure for AI agents."""

from .async_client import AsyncEngram
from .client import Engram
from .exceptions import (
    APIError,
    AuthenticationError,
    ConflictError,
    ConnectionError,
    EngramError,
    NotFoundError,
    ServerError,
    ValidationError,
)
from .types import (
    HealthStatus,
    MemoryTier,
    MemoryType,
    ServerMetrics,
    Tenant,
)

__all__ = [
    # Clients
    "Engram",
    "AsyncEngram",
    # Exceptions
    "EngramError",
    "APIError",
    "AuthenticationError",
    "NotFoundError",
    "ConflictError",
    "ValidationError",
    "ServerError",
    "ConnectionError",
    # Enums
    "MemoryType",
    "MemoryTier",
    # Models
    "Tenant",
    "HealthStatus",
    "ServerMetrics",
]

__version__ = "0.1.0"
