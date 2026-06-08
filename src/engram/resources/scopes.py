"""Scope-model resources: anchors (subjects), sessions, and canon.

One agent can serve thousands of isolated subjects. See the "Subjects, Sessions
& Canon" guide. ``binding`` on each memory records what it's about; it is derived
server-side from the ids you pass (``anchor_external_id`` → ``anchored``,
``session_id`` → ``session``, neither → ``private``). ``canon`` is tenant-shared
org knowledge, written through its own admin-scoped endpoint.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import Anchor, Memory, Session

if TYPE_CHECKING:
    from .._client import AsyncHTTPClient, SyncHTTPClient


class Anchors:
    """Subjects a memory can be about (customers/guests/patients/cases)."""

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def create(
        self,
        *,
        name: str,
        external_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        agent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Anchor:
        """Create a subject explicitly. (Usually unnecessary — passing
        ``anchor_external_id`` on a memory auto-creates the anchor.)"""
        body: Dict[str, Any] = {"name": name}
        if external_id is not None:
            body["external_id"] = external_id
        if entity_type is not None:
            body["entity_type"] = entity_type
        if agent_id is not None:
            body["agent_id"] = agent_id
        if metadata is not None:
            body["metadata"] = metadata
        return Anchor.model_validate(self._client.request("POST", "/v1/anchors", json=body))

    def list(self, *, entity_type: Optional[str] = None) -> List[Anchor]:
        """List the tenant's subjects."""
        params: Dict[str, Any] = {}
        if entity_type is not None:
            params["entity_type"] = entity_type
        data = self._client.request("GET", "/v1/anchors", params=params)
        return [Anchor.model_validate(a) for a in (data.get("anchors") or data.get("entities") or [])]

    def get(self, anchor_id: str) -> Anchor:
        return Anchor.model_validate(self._client.request("GET", f"/v1/anchors/{anchor_id}"))

    def memories(self, anchor_id: str) -> List[Memory]:
        """A subject's full durable profile."""
        data = self._client.request("GET", f"/v1/anchors/{anchor_id}/memories")
        return [Memory.model_validate(m) for m in (data.get("memories") or [])]

    def delete(self, anchor_id: str, *, purge: bool = False) -> None:
        """Delete a subject. ``purge=True`` performs a GDPR/HIPAA hard-erase —
        the anchor **and every trace bound to it** are deleted (scoped to just
        this subject)."""
        params = {"purge": "true"} if purge else None
        self._client.request("DELETE", f"/v1/anchors/{anchor_id}", params=params)


class Sessions:
    """Conversations/runs. Session-bound memory is short-term and decays out."""

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def create(
        self,
        *,
        agent_id: str,
        anchor_external_id: Optional[str] = None,
        anchor_id: Optional[str] = None,
        external_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Session:
        """Open a session, optionally about a returning subject."""
        body: Dict[str, Any] = {"agent_id": agent_id}
        if anchor_external_id is not None:
            body["anchor_external_id"] = anchor_external_id
        if anchor_id is not None:
            body["anchor_id"] = anchor_id
        if external_id is not None:
            body["external_id"] = external_id
        if metadata is not None:
            body["metadata"] = metadata
        return Session.model_validate(self._client.request("POST", "/v1/sessions", json=body))

    def get(self, session_id: str) -> Session:
        return Session.model_validate(self._client.request("GET", f"/v1/sessions/{session_id}"))

    def end(self, session_id: str) -> Session:
        """End a session — schedules expiry of its short-term memory."""
        return Session.model_validate(self._client.request("POST", f"/v1/sessions/{session_id}/end"))


class Canon:
    """Tenant-shared, authoritative org knowledge (policies, catalog). Writes are
    admin-scoped; composed into every recall in the tenant."""

    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def create(
        self,
        *,
        agent_id: str,
        content: str,
        type: Optional[str] = None,
        source: Optional[str] = None,
        confidence: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Memory:
        """Add a canon entry (requires an ``admin``-scoped key). Idempotent on
        identical content — re-posting returns the existing entry."""
        body: Dict[str, Any] = {"agent_id": agent_id, "content": content}
        for k, v in (("type", type), ("source", source), ("confidence", confidence), ("metadata", metadata)):
            if v is not None:
                body[k] = v
        return Memory.model_validate(self._client.request("POST", "/v1/canon", json=body))

    def list(self) -> List[Memory]:
        data = self._client.request("GET", "/v1/canon")
        return [Memory.model_validate(m) for m in (data.get("memories") or data.get("canon") or [])]

    def delete(self, canon_id: str) -> None:
        """Delete a canon entry (requires an ``admin``-scoped key)."""
        self._client.request("DELETE", f"/v1/canon/{canon_id}")


# ── async variants ──────────────────────────────────────────────────────────


class AsyncAnchors:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def create(self, *, name: str, external_id: Optional[str] = None,
                     entity_type: Optional[str] = None, agent_id: Optional[str] = None,
                     metadata: Optional[Dict[str, Any]] = None) -> Anchor:
        body: Dict[str, Any] = {"name": name}
        for k, v in (("external_id", external_id), ("entity_type", entity_type),
                     ("agent_id", agent_id), ("metadata", metadata)):
            if v is not None:
                body[k] = v
        return Anchor.model_validate(await self._client.request("POST", "/v1/anchors", json=body))

    async def list(self, *, entity_type: Optional[str] = None) -> List[Anchor]:
        params: Dict[str, Any] = {}
        if entity_type is not None:
            params["entity_type"] = entity_type
        data = await self._client.request("GET", "/v1/anchors", params=params)
        return [Anchor.model_validate(a) for a in (data.get("anchors") or data.get("entities") or [])]

    async def get(self, anchor_id: str) -> Anchor:
        return Anchor.model_validate(await self._client.request("GET", f"/v1/anchors/{anchor_id}"))

    async def memories(self, anchor_id: str) -> List[Memory]:
        data = await self._client.request("GET", f"/v1/anchors/{anchor_id}/memories")
        return [Memory.model_validate(m) for m in (data.get("memories") or [])]

    async def delete(self, anchor_id: str, *, purge: bool = False) -> None:
        params = {"purge": "true"} if purge else None
        await self._client.request("DELETE", f"/v1/anchors/{anchor_id}", params=params)


class AsyncSessions:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def create(self, *, agent_id: str, anchor_external_id: Optional[str] = None,
                     anchor_id: Optional[str] = None, external_id: Optional[str] = None,
                     metadata: Optional[Dict[str, Any]] = None) -> Session:
        body: Dict[str, Any] = {"agent_id": agent_id}
        for k, v in (("anchor_external_id", anchor_external_id), ("anchor_id", anchor_id),
                     ("external_id", external_id), ("metadata", metadata)):
            if v is not None:
                body[k] = v
        return Session.model_validate(await self._client.request("POST", "/v1/sessions", json=body))

    async def get(self, session_id: str) -> Session:
        return Session.model_validate(await self._client.request("GET", f"/v1/sessions/{session_id}"))

    async def end(self, session_id: str) -> Session:
        return Session.model_validate(await self._client.request("POST", f"/v1/sessions/{session_id}/end"))


class AsyncCanon:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def create(self, *, agent_id: str, content: str, type: Optional[str] = None,
                     source: Optional[str] = None, confidence: Optional[float] = None,
                     metadata: Optional[Dict[str, Any]] = None) -> Memory:
        body: Dict[str, Any] = {"agent_id": agent_id, "content": content}
        for k, v in (("type", type), ("source", source), ("confidence", confidence), ("metadata", metadata)):
            if v is not None:
                body[k] = v
        return Memory.model_validate(await self._client.request("POST", "/v1/canon", json=body))

    async def list(self) -> List[Memory]:
        data = await self._client.request("GET", "/v1/canon")
        return [Memory.model_validate(m) for m in (data.get("memories") or data.get("canon") or [])]

    async def delete(self, canon_id: str) -> None:
        await self._client.request("DELETE", f"/v1/canon/{canon_id}")
