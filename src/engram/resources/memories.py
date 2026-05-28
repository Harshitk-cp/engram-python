"""Memory resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from ..types import ExtractedMemory, Memory, Message, RecalledMemory

if TYPE_CHECKING:
    from .._client import AsyncHTTPClient, SyncHTTPClient


class RecallResult:
    """Wrapper around a recall response, exposing memories and metadata."""

    def __init__(self, memories: List[RecalledMemory], query: str, count: int) -> None:
        self.memories = memories
        self.query = query
        self.count = count

    def __iter__(self):  # type: ignore[override]
        return iter(self.memories)

    def __len__(self) -> int:
        return self.count

    def __repr__(self) -> str:
        return f"RecallResult(count={self.count}, query={self.query!r})"


class ExtractResult:
    """Wrapper around an extract response."""

    def __init__(self, extracted: List[ExtractedMemory], count: int) -> None:
        self.extracted = extracted
        self.count = count

    def __iter__(self):  # type: ignore[override]
        return iter(self.extracted)

    def __len__(self) -> int:
        return self.count


def _parse_recall(data: Any) -> RecallResult:
    memories = [RecalledMemory.model_validate(m) for m in (data.get("memories") or [])]
    return RecallResult(
        memories=memories,
        query=data.get("query", ""),
        count=data.get("count", len(memories)),
    )


def _parse_extract(data: Any) -> ExtractResult:
    raw = data.get("extracted") or []
    extracted = []
    for item in raw:
        extracted.append(
            ExtractedMemory(
                memory_type=item.get("type", "fact"),
                content=item.get("content", ""),
                confidence=item.get("confidence", 0.0),
                evidence=item.get("evidence_type", "explicit_statement"),
                stored_id=item.get("id"),
            )
        )
    return ExtractResult(extracted=extracted, count=data.get("count", len(extracted)))


class Memories:
    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def store(
        self,
        *,
        agent_id: str,
        content: str,
        type: Optional[str] = None,
        confidence: Optional[float] = None,
        source: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Memory:
        """Store a memory for an agent.

        The server auto-classifies ``type`` via LLM if not provided.
        ``confidence`` defaults to 1.0 server-side if omitted.
        """
        body: Dict[str, Any] = {"agent_id": agent_id, "content": content}
        if type is not None:
            body["type"] = type
        if confidence is not None:
            body["confidence"] = confidence
        if source is not None:
            body["source"] = source
        if metadata is not None:
            body["metadata"] = metadata
        data = self._client.request("POST", "/v1/memories/", json=body)
        return Memory.model_validate(data)

    def get(self, memory_id: str) -> Memory:
        """Fetch a single memory by UUID."""
        data = self._client.request("GET", f"/v1/memories/{memory_id}")
        return Memory.model_validate(data)

    def delete(self, memory_id: str) -> None:
        """Delete a memory. Returns None on success (204)."""
        self._client.request("DELETE", f"/v1/memories/{memory_id}")

    def recall(
        self,
        *,
        agent_id: str,
        query: str,
        top_k: int = 10,
        type: Optional[str] = None,
        min_confidence: Optional[float] = None,
        graph_weight: Optional[float] = None,
        max_hops: Optional[int] = None,
    ) -> RecallResult:
        """Hybrid vector + graph recall.

        Returns a :class:`RecallResult` — iterate it directly for the memory list,
        or access ``.memories``, ``.query``, ``.count``.

        ``graph_weight`` (0–1) controls the graph/vector blend; the complement
        is used as ``vector_weight``. Default server-side split is 0.4/0.6.
        """
        params: Dict[str, Any] = {"agent_id": agent_id, "query": query, "top_k": top_k}
        if type is not None:
            params["type"] = type
        if min_confidence is not None:
            params["min_confidence"] = min_confidence
        if graph_weight is not None:
            params["graph_weight"] = graph_weight
        if max_hops is not None:
            params["max_hops"] = max_hops
        data = self._client.request("GET", "/v1/memories/recall", params=params)
        return _parse_recall(data)

    def extract(
        self,
        *,
        agent_id: str,
        conversation: List[Union[Message, Dict[str, str]]],
        auto_store: bool = True,
    ) -> ExtractResult:
        """Extract memories from a conversation using the LLM.

        ``conversation`` is a list of ``{"role": "user"|"assistant", "content": "..."}``
        dicts or :class:`Message` objects.
        """
        msgs = [
            m.model_dump() if isinstance(m, Message) else m for m in conversation
        ]
        body = {"agent_id": agent_id, "conversation": msgs, "auto_store": auto_store}
        data = self._client.request("POST", "/v1/memories/extract", json=body)
        return _parse_extract(data)


class AsyncMemories:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def store(
        self,
        *,
        agent_id: str,
        content: str,
        type: Optional[str] = None,
        confidence: Optional[float] = None,
        source: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Memory:
        body: Dict[str, Any] = {"agent_id": agent_id, "content": content}
        if type is not None:
            body["type"] = type
        if confidence is not None:
            body["confidence"] = confidence
        if source is not None:
            body["source"] = source
        if metadata is not None:
            body["metadata"] = metadata
        data = await self._client.request("POST", "/v1/memories/", json=body)
        return Memory.model_validate(data)

    async def get(self, memory_id: str) -> Memory:
        data = await self._client.request("GET", f"/v1/memories/{memory_id}")
        return Memory.model_validate(data)

    async def delete(self, memory_id: str) -> None:
        await self._client.request("DELETE", f"/v1/memories/{memory_id}")

    async def recall(
        self,
        *,
        agent_id: str,
        query: str,
        top_k: int = 10,
        type: Optional[str] = None,
        min_confidence: Optional[float] = None,
        graph_weight: Optional[float] = None,
        max_hops: Optional[int] = None,
    ) -> RecallResult:
        params: Dict[str, Any] = {"agent_id": agent_id, "query": query, "top_k": top_k}
        if type is not None:
            params["type"] = type
        if min_confidence is not None:
            params["min_confidence"] = min_confidence
        if graph_weight is not None:
            params["graph_weight"] = graph_weight
        if max_hops is not None:
            params["max_hops"] = max_hops
        data = await self._client.request("GET", "/v1/memories/recall", params=params)
        return _parse_recall(data)

    async def extract(
        self,
        *,
        agent_id: str,
        conversation: List[Union[Message, Dict[str, str]]],
        auto_store: bool = True,
    ) -> ExtractResult:
        msgs = [
            m.model_dump() if isinstance(m, Message) else m for m in conversation
        ]
        body = {"agent_id": agent_id, "conversation": msgs, "auto_store": auto_store}
        data = await self._client.request("POST", "/v1/memories/extract", json=body)
        return _parse_extract(data)
