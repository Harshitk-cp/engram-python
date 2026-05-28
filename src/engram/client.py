"""Engram SDK client — synchronous."""

from __future__ import annotations

from typing import Optional

import httpx

from ._client import SyncHTTPClient
from .resources.agents import Agents
from .resources.cognitive import Cognitive
from .resources.episodes import Episodes
from .resources.feedback import FeedbackResource
from .resources.learning import Learning
from .resources.graph import Graph
from .resources.memories import Memories
from .resources.procedures import Procedures
from .resources.schemas import Schemas
from .resources.tenants import Tenants
from .types import HealthStatus, ServerMetrics


class Engram:
    """Synchronous Engram client.

    Reads ENGRAM_BASE_URL and ENGRAM_API_KEY from the environment if not passed explicitly.
    ENGRAM_BASE_URL is required (no default) — raises ValueError if neither arg nor env var is set.

    Usage::

        from engram import Engram

        # Via environment variables (recommended):
        # export ENGRAM_BASE_URL=http://localhost:8080
        # export ENGRAM_API_KEY=your-api-key
        client = Engram()

        # Or pass explicitly:
        client = Engram(base_url="http://localhost:8080", api_key="your-api-key")

        agent = client.agents.create(external_id="bot-1", name="My Agent")
        client.memories.store(agent_id=agent.id, content="User prefers dark mode")
        result = client.memories.recall(agent_id=agent.id, query="display preferences")
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
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
        self.agents = Agents(self._http)
        self.memories = Memories(self._http)
        self.episodes = Episodes(self._http)
        self.procedures = Procedures(self._http)
        self.schemas = Schemas(self._http)
        self.cognitive = Cognitive(self._http)
        self.graph = Graph(self._http)
        self.feedback = FeedbackResource(self._http)
        self.learning = Learning(self._http)

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
