"""Graph resource — entity and relationship queries."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import Entity, GraphPath, Relationship

if TYPE_CHECKING:
    from .._client import AsyncHTTPClient, SyncHTTPClient


class Graph:
    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def list_entities(
        self,
        agent_id: str,
        *,
        limit: Optional[int] = None,
    ) -> List[Entity]:
        """List entities extracted from an agent's memories."""
        params: Dict[str, Any] = {"agent_id": agent_id}
        if limit is not None:
            params["limit"] = limit
        data = self._client.request("GET", "/v1/graph/entities", params=params)
        entities = data if isinstance(data, list) else (data.get("entities") or [])
        return [Entity.model_validate(e) for e in entities]

    def get_relationships(
        self,
        agent_id: str,
        *,
        entity_id: Optional[str] = None,
    ) -> List[Relationship]:
        """Get memory relationships, optionally filtered by an entity."""
        params: Dict[str, Any] = {"agent_id": agent_id}
        if entity_id is not None:
            params["entity_id"] = entity_id
        data = self._client.request("GET", "/v1/graph/relationships", params=params)
        rels = data if isinstance(data, list) else (data.get("relationships") or [])
        return [Relationship.model_validate(r) for r in rels]

    def traverse(
        self,
        *,
        agent_id: str,
        start_memory_id: str,
        max_hops: int = 2,
    ) -> List[GraphPath]:
        """Traverse the knowledge graph from a starting memory."""
        body: Dict[str, Any] = {
            "agent_id": agent_id,
            "start_memory_id": start_memory_id,
            "max_hops": max_hops,
        }
        data = self._client.request("POST", "/v1/graph/traverse", json=body)
        paths = data if isinstance(data, list) else (data.get("paths") or [])
        return [GraphPath.model_validate(p) for p in paths]


class AsyncGraph:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def list_entities(
        self,
        agent_id: str,
        *,
        limit: Optional[int] = None,
    ) -> List[Entity]:
        params: Dict[str, Any] = {"agent_id": agent_id}
        if limit is not None:
            params["limit"] = limit
        data = await self._client.request("GET", "/v1/graph/entities", params=params)
        entities = data if isinstance(data, list) else (data.get("entities") or [])
        return [Entity.model_validate(e) for e in entities]

    async def get_relationships(
        self,
        agent_id: str,
        *,
        entity_id: Optional[str] = None,
    ) -> List[Relationship]:
        params: Dict[str, Any] = {"agent_id": agent_id}
        if entity_id is not None:
            params["entity_id"] = entity_id
        data = await self._client.request(
            "GET", "/v1/graph/relationships", params=params
        )
        rels = data if isinstance(data, list) else (data.get("relationships") or [])
        return [Relationship.model_validate(r) for r in rels]

    async def traverse(
        self,
        *,
        agent_id: str,
        start_memory_id: str,
        max_hops: int = 2,
    ) -> List[GraphPath]:
        body: Dict[str, Any] = {
            "agent_id": agent_id,
            "start_memory_id": start_memory_id,
            "max_hops": max_hops,
        }
        data = await self._client.request("POST", "/v1/graph/traverse", json=body)
        paths = data if isinstance(data, list) else (data.get("paths") or [])
        return [GraphPath.model_validate(p) for p in paths]
