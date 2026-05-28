"""Agent resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import Agent, LearningStats, Memory, MemoryPolicy, Mind, TierStats

if TYPE_CHECKING:
    from .._client import AsyncHTTPClient, SyncHTTPClient


class AgentListResult:
    def __init__(self, agents: List[Agent], count: int, limit: int, offset: int) -> None:
        self.agents = agents
        self.count = count
        self.limit = limit
        self.offset = offset

    def __iter__(self):  # type: ignore[override]
        return iter(self.agents)

    def __len__(self) -> int:
        return self.count


class Agents:
    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def list(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> AgentListResult:
        """List all agents for the authenticated tenant."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        data = self._client.request("GET", "/v1/agents/", params=params)
        agents = [Agent.model_validate(a) for a in (data.get("agents") or [])]
        return AgentListResult(
            agents=agents,
            count=data.get("count", len(agents)),
            limit=data.get("limit", limit),
            offset=data.get("offset", offset),
        )

    def delete(self, agent_id: str) -> None:
        """Delete an agent and all its associated memories."""
        self._client.request("DELETE", f"/v1/agents/{agent_id}/")

    def get_learning_stats(self, agent_id: str) -> Optional[LearningStats]:
        """Return aggregated learning statistics for an agent, or None if not yet computed."""
        data = self._client.request("GET", f"/v1/agents/{agent_id}/learning/stats")
        if data is None or "message" in data:
            return None
        return LearningStats.model_validate(data)

    def create(
        self,
        *,
        external_id: str,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Agent:
        """Register a new agent under the authenticated tenant."""
        body: Dict[str, Any] = {"external_id": external_id, "name": name}
        if metadata is not None:
            body["metadata"] = metadata
        data = self._client.request("POST", "/v1/agents/", json=body)
        return Agent.model_validate(data)

    def get(self, agent_id: str) -> Agent:
        """Fetch an agent by UUID."""
        data = self._client.request("GET", f"/v1/agents/{agent_id}")
        return Agent.model_validate(data)

    def get_mind(self, agent_id: str) -> Mind:
        """Get the agent's full mental state — beliefs, episodes, procedures, schemas."""
        data = self._client.request("GET", f"/v1/agents/{agent_id}/mind")
        return Mind.model_validate(data)

    def get_policies(self, agent_id: str) -> List[MemoryPolicy]:
        data = self._client.request("GET", f"/v1/agents/{agent_id}/policies")
        return [MemoryPolicy.model_validate(p) for p in (data or [])]

    def update_policies(self, agent_id: str, policy: MemoryPolicy) -> MemoryPolicy:
        """Upsert a memory policy for this agent."""
        data = self._client.request(
            "PUT", f"/v1/agents/{agent_id}/policies", json=policy.model_dump()
        )
        return MemoryPolicy.model_validate(data)

    def get_tier_stats(self, agent_id: str) -> TierStats:
        data = self._client.request("GET", f"/v1/agents/{agent_id}/tier-stats")
        return TierStats.model_validate(data)

    def get_hot_memories(self, agent_id: str, *, limit: Optional[int] = None) -> List[Memory]:
        """Return memories currently in the Hot tier (confidence > 0.85)."""
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        data = self._client.request(
            "GET", f"/v1/agents/{agent_id}/hot-memories", params=params or None
        )
        return [Memory.model_validate(m) for m in (data or [])]


class AsyncAgents:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> AgentListResult:
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        data = await self._client.request("GET", "/v1/agents/", params=params)
        agents = [Agent.model_validate(a) for a in (data.get("agents") or [])]
        return AgentListResult(
            agents=agents,
            count=data.get("count", len(agents)),
            limit=data.get("limit", limit),
            offset=data.get("offset", offset),
        )

    async def delete(self, agent_id: str) -> None:
        await self._client.request("DELETE", f"/v1/agents/{agent_id}/")

    async def get_learning_stats(self, agent_id: str) -> Optional[LearningStats]:
        data = await self._client.request(
            "GET", f"/v1/agents/{agent_id}/learning/stats"
        )
        if data is None or "message" in data:
            return None
        return LearningStats.model_validate(data)

    async def create(
        self,
        *,
        external_id: str,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Agent:
        body: Dict[str, Any] = {"external_id": external_id, "name": name}
        if metadata is not None:
            body["metadata"] = metadata
        data = await self._client.request("POST", "/v1/agents/", json=body)
        return Agent.model_validate(data)

    async def get(self, agent_id: str) -> Agent:
        data = await self._client.request("GET", f"/v1/agents/{agent_id}")
        return Agent.model_validate(data)

    async def get_mind(self, agent_id: str) -> Mind:
        data = await self._client.request("GET", f"/v1/agents/{agent_id}/mind")
        return Mind.model_validate(data)

    async def get_policies(self, agent_id: str) -> List[MemoryPolicy]:
        data = await self._client.request("GET", f"/v1/agents/{agent_id}/policies")
        return [MemoryPolicy.model_validate(p) for p in (data or [])]

    async def update_policies(self, agent_id: str, policy: MemoryPolicy) -> MemoryPolicy:
        data = await self._client.request(
            "PUT", f"/v1/agents/{agent_id}/policies", json=policy.model_dump()
        )
        return MemoryPolicy.model_validate(data)

    async def get_tier_stats(self, agent_id: str) -> TierStats:
        data = await self._client.request("GET", f"/v1/agents/{agent_id}/tier-stats")
        return TierStats.model_validate(data)

    async def get_hot_memories(
        self, agent_id: str, *, limit: Optional[int] = None
    ) -> List[Memory]:
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        data = await self._client.request(
            "GET", f"/v1/agents/{agent_id}/hot-memories", params=params or None
        )
        return [Memory.model_validate(m) for m in (data or [])]
