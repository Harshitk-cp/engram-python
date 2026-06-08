"""Engram SDK client — asynchronous."""

from __future__ import annotations

from typing import Optional  # noqa: F401 — used in setup() signature

import httpx

from ._client import AsyncHTTPClient
from .resources.agents import AsyncAgents
from .resources.cognitive import AsyncCognitive
from .resources.episodes import AsyncEpisodes
from .resources.feedback import AsyncFeedbackResource
from .resources.keys import AsyncKeys
from .resources.learning import AsyncLearning
from .resources.graph import AsyncGraph
from .resources.memories import AsyncMemories
from .resources.procedures import AsyncProcedures
from .resources.schemas import AsyncSchemas
from .resources.scopes import AsyncAnchors, AsyncCanon, AsyncSessions
from .resources.tenants import AsyncTenants
from .types import HealthStatus, ServerMetrics, SetupResult


class AsyncEngram:
    """Asynchronous Engram client.

    Reads ENGRAM_BASE_URL and ENGRAM_API_KEY from the environment if not passed explicitly.
    ENGRAM_BASE_URL is required (no default) — raises ValueError if neither arg nor env var is set.

    Usage::

        import asyncio
        from engram import AsyncEngram

        async def main():
            # Via environment variables (recommended):
            # export ENGRAM_BASE_URL=http://localhost:8080
            # export ENGRAM_API_KEY=your-api-key
            async with AsyncEngram() as client:
                agent = await client.agents.create(external_id="bot-1", name="My Agent")
                await client.memories.store(agent_id=agent.id, content="User prefers dark mode")
                result = await client.memories.recall(agent_id=agent.id, query="display preferences")

        asyncio.run(main())
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
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
        self.keys = AsyncKeys(self._http)
        self.agents = AsyncAgents(self._http)
        self.memories = AsyncMemories(self._http)
        self.anchors = AsyncAnchors(self._http)
        self.sessions = AsyncSessions(self._http)
        self.canon = AsyncCanon(self._http)
        self.episodes = AsyncEpisodes(self._http)
        self.procedures = AsyncProcedures(self._http)
        self.schemas = AsyncSchemas(self._http)
        self.cognitive = AsyncCognitive(self._http)
        self.graph = AsyncGraph(self._http)
        self.feedback = AsyncFeedbackResource(self._http)
        self.learning = AsyncLearning(self._http)

    async def setup(self, org_name: str, setup_token: Optional[str] = None) -> SetupResult:
        """Bootstrap a new tenant and receive a master API key. See :meth:`Engram.setup`."""
        import os
        token = setup_token or os.environ.get("ENGRAM_SETUP_TOKEN", "")
        data = await self._http.request(
            "POST", "/v1/setup",
            json={"org_name": org_name},
            extra_headers={"X-Setup-Token": token},
        )
        return SetupResult.model_validate(data)

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
