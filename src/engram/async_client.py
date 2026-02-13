"""Engram SDK client — asynchronous."""

from __future__ import annotations

from typing import Optional

import httpx

from ._client import AsyncHTTPClient
from .resources.tenants import AsyncTenants
from .types import HealthStatus, ServerMetrics


class AsyncEngram:
    """Asynchronous Engram client.

    Usage::

        import asyncio
        from engram import AsyncEngram

        async def main():
            async with AsyncEngram(base_url="http://localhost:3741") as client:
                tenant = await client.tenants.create(name="my-org")
                print(tenant.api_key)

        asyncio.run(main())
    """

    def __init__(
        self,
        base_url: str = "http://localhost:3741",
        api_key: Optional[str] = None,
        timeout: float = 30.0,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self._http = AsyncHTTPClient(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            http_client=http_client,
        )

        self.tenants = AsyncTenants(self._http)

    async def health(self) -> HealthStatus:
        """Check server health."""
        data = await self._http.request("GET", "/health")
        return HealthStatus.model_validate(data)

    async def metrics(self) -> ServerMetrics:
        """Get server metrics."""
        data = await self._http.request("GET", "/metrics")
        return ServerMetrics.model_validate(data)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.close()

    async def __aenter__(self) -> AsyncEngram:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
