"""Procedure resource (procedural memory — learned skills and patterns)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import Procedure

if TYPE_CHECKING:
    from .._client import AsyncHTTPClient, SyncHTTPClient


class Procedures:
    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def match(
        self,
        *,
        agent_id: str,
        context: str,
        top_k: int = 5,
    ) -> List[Procedure]:
        """Find procedures matching a context string by trigger similarity."""
        body: Dict[str, Any] = {"agent_id": agent_id, "context": context, "top_k": top_k}
        data = self._client.request("POST", "/v1/procedures/match", json=body)
        procedures = data.get("procedures") or data if isinstance(data, list) else []
        return [Procedure.model_validate(p) for p in procedures]

    def learn(self, *, agent_id: str, episode_id: str) -> Procedure:
        """Derive a procedure from a completed episode."""
        body: Dict[str, Any] = {"agent_id": agent_id, "episode_id": episode_id}
        data = self._client.request("POST", "/v1/procedures/learn", json=body)
        return Procedure.model_validate(data)

    def get(self, procedure_id: str) -> Procedure:
        data = self._client.request("GET", f"/v1/procedures/{procedure_id}")
        return Procedure.model_validate(data)

    def record_outcome(
        self,
        procedure_id: str,
        *,
        success: bool,
        context: Optional[str] = None,
    ) -> None:
        """Record whether a procedure execution succeeded."""
        body: Dict[str, Any] = {"success": success}
        if context is not None:
            body["context"] = context
        self._client.request(
            "POST", f"/v1/procedures/{procedure_id}/outcome", json=body
        )


class AsyncProcedures:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def match(
        self,
        *,
        agent_id: str,
        context: str,
        top_k: int = 5,
    ) -> List[Procedure]:
        body: Dict[str, Any] = {"agent_id": agent_id, "context": context, "top_k": top_k}
        data = await self._client.request("POST", "/v1/procedures/match", json=body)
        procedures = data.get("procedures") or data if isinstance(data, list) else []
        return [Procedure.model_validate(p) for p in procedures]

    async def learn(self, *, agent_id: str, episode_id: str) -> Procedure:
        body: Dict[str, Any] = {"agent_id": agent_id, "episode_id": episode_id}
        data = await self._client.request("POST", "/v1/procedures/learn", json=body)
        return Procedure.model_validate(data)

    async def get(self, procedure_id: str) -> Procedure:
        data = await self._client.request("GET", f"/v1/procedures/{procedure_id}")
        return Procedure.model_validate(data)

    async def record_outcome(
        self,
        procedure_id: str,
        *,
        success: bool,
        context: Optional[str] = None,
    ) -> None:
        body: Dict[str, Any] = {"success": success}
        if context is not None:
            body["context"] = context
        await self._client.request(
            "POST", f"/v1/procedures/{procedure_id}/outcome", json=body
        )
