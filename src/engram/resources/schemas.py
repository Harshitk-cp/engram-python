"""Schema resource (mental models / abstract patterns)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import Schema, SchemaMatch

if TYPE_CHECKING:
    from .._client import AsyncHTTPClient, SyncHTTPClient


class Schemas:
    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def list(self, agent_id: str) -> List[Schema]:
        """List all schemas for an agent."""
        data = self._client.request("GET", "/v1/schemas", params={"agent_id": agent_id})
        schemas = data.get("schemas") or data if isinstance(data, list) else []
        return [Schema.model_validate(s) for s in schemas]

    def get(self, schema_id: str) -> Schema:
        data = self._client.request("GET", f"/v1/schemas/{schema_id}")
        return Schema.model_validate(data)

    def delete(self, schema_id: str) -> None:
        self._client.request("DELETE", f"/v1/schemas/{schema_id}")

    def detect(self, agent_id: str) -> List[Schema]:
        """Run pattern detection on the agent's memories to surface new schemas."""
        body: Dict[str, Any] = {"agent_id": agent_id}
        data = self._client.request("POST", "/v1/schemas/detect", json=body)
        schemas = data.get("schemas") or data if isinstance(data, list) else []
        return [Schema.model_validate(s) for s in schemas]

    def match(self, *, agent_id: str, context: str) -> List[SchemaMatch]:
        """Find schemas whose patterns match the given context."""
        body: Dict[str, Any] = {"agent_id": agent_id, "context": context}
        data = self._client.request("POST", "/v1/schemas/match", json=body)
        matches = data.get("matches") or data if isinstance(data, list) else []
        return [SchemaMatch.model_validate(m) for m in matches]

    def validate(self, schema_id: str) -> Schema:
        """Validate and refresh a schema against current evidence."""
        data = self._client.request("POST", f"/v1/schemas/{schema_id}/validate", json={})
        return Schema.model_validate(data)

    def contradict(self, schema_id: str, *, memory_id: Optional[str] = None) -> None:
        """Record a contradiction against a schema (decreases its confidence)."""
        body: Dict[str, Any] = {}
        if memory_id is not None:
            body["memory_id"] = memory_id
        self._client.request("POST", f"/v1/schemas/{schema_id}/contradict", json=body)


class AsyncSchemas:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def list(self, agent_id: str) -> List[Schema]:
        data = await self._client.request(
            "GET", "/v1/schemas", params={"agent_id": agent_id}
        )
        schemas = data.get("schemas") or data if isinstance(data, list) else []
        return [Schema.model_validate(s) for s in schemas]

    async def get(self, schema_id: str) -> Schema:
        data = await self._client.request("GET", f"/v1/schemas/{schema_id}")
        return Schema.model_validate(data)

    async def delete(self, schema_id: str) -> None:
        await self._client.request("DELETE", f"/v1/schemas/{schema_id}")

    async def detect(self, agent_id: str) -> List[Schema]:
        body: Dict[str, Any] = {"agent_id": agent_id}
        data = await self._client.request("POST", "/v1/schemas/detect", json=body)
        schemas = data.get("schemas") or data if isinstance(data, list) else []
        return [Schema.model_validate(s) for s in schemas]

    async def match(self, *, agent_id: str, context: str) -> List[SchemaMatch]:
        body: Dict[str, Any] = {"agent_id": agent_id, "context": context}
        data = await self._client.request("POST", "/v1/schemas/match", json=body)
        matches = data.get("matches") or data if isinstance(data, list) else []
        return [SchemaMatch.model_validate(m) for m in matches]

    async def validate(self, schema_id: str) -> Schema:
        data = await self._client.request(
            "POST", f"/v1/schemas/{schema_id}/validate", json={}
        )
        return Schema.model_validate(data)

    async def contradict(
        self, schema_id: str, *, memory_id: Optional[str] = None
    ) -> None:
        body: Dict[str, Any] = {}
        if memory_id is not None:
            body["memory_id"] = memory_id
        await self._client.request(
            "POST", f"/v1/schemas/{schema_id}/contradict", json=body
        )
