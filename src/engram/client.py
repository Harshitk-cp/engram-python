"""Engram SDK client — synchronous."""

from __future__ import annotations

from typing import Optional

import httpx

from ._client import SyncHTTPClient
from .resources.tenants import Tenants
from .types import HealthStatus, ServerMetrics


class Engram:
    """Synchronous Engram client.

    Usage::

        from engram import Engram

        # Bootstrap: create a tenant (no auth required)
        client = Engram(base_url="http://localhost:3741")
        tenant = client.tenants.create(name="my-org")

        # Use the API key for authenticated requests
        client = Engram(base_url="http://localhost:3741", api_key=tenant.api_key)
    """

    def __init__(
        self,
        base_url: str = "http://localhost:3741",
        api_key: Optional[str] = None,
        timeout: float = 30.0,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self._http = SyncHTTPClient(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            http_client=http_client,
        )

        self.tenants = Tenants(self._http)

    def health(self) -> HealthStatus:
        """Check server health."""
        data = self._http.request("GET", "/health")
        return HealthStatus.model_validate(data)

    def metrics(self) -> ServerMetrics:
        """Get server metrics."""
        data = self._http.request("GET", "/metrics")
        return ServerMetrics.model_validate(data)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    def __enter__(self) -> Engram:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
