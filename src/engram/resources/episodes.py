"""Episode resource (episodic memory)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import Episode, EpisodeAssociation, RecalledEpisode

if TYPE_CHECKING:
    from .._client import AsyncHTTPClient, SyncHTTPClient


class Episodes:
    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def store(
        self,
        *,
        agent_id: str,
        content: str,
        conversation_id: Optional[str] = None,
        occurred_at: Optional[str] = None,
        outcome: Optional[str] = None,
    ) -> Episode:
        """Store an episode (rich experience with context).

        ``occurred_at`` should be an RFC 3339 string if provided.
        ``outcome`` is one of: success, failure, neutral, unknown.
        """
        body: Dict[str, Any] = {"agent_id": agent_id, "raw_content": content}
        if conversation_id is not None:
            body["conversation_id"] = conversation_id
        if occurred_at is not None:
            body["occurred_at"] = occurred_at
        if outcome is not None:
            body["outcome"] = outcome
        data = self._client.request("POST", "/v1/episodes/", json=body)
        return Episode.model_validate(data)

    def get(self, episode_id: str) -> Episode:
        data = self._client.request("GET", f"/v1/episodes/{episode_id}")
        return Episode.model_validate(data)

    def recall(
        self,
        *,
        agent_id: str,
        query: Optional[str] = None,
        min_importance: Optional[float] = None,
        limit: int = 10,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> List[RecalledEpisode]:
        """Recall episodes by semantic similarity or time range."""
        params: Dict[str, Any] = {"agent_id": agent_id, "limit": limit}
        if query is not None:
            params["query"] = query
        if min_importance is not None:
            params["min_importance"] = min_importance
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        data = self._client.request("GET", "/v1/episodes/recall", params=params)
        episodes = data.get("episodes") or data if isinstance(data, list) else []
        return [RecalledEpisode.model_validate(e) for e in episodes]

    def record_outcome(
        self,
        episode_id: str,
        *,
        outcome: str,
        description: Optional[str] = None,
    ) -> None:
        """Record the outcome of an episode (success/failure/neutral/unknown)."""
        body: Dict[str, Any] = {"outcome": outcome}
        if description is not None:
            body["description"] = description
        self._client.request("POST", f"/v1/episodes/{episode_id}/outcome", json=body)

    def get_associations(self, episode_id: str) -> List[EpisodeAssociation]:
        data = self._client.request("GET", f"/v1/episodes/{episode_id}/associations")
        return [EpisodeAssociation.model_validate(a) for a in (data or [])]


class AsyncEpisodes:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def store(
        self,
        *,
        agent_id: str,
        content: str,
        conversation_id: Optional[str] = None,
        occurred_at: Optional[str] = None,
        outcome: Optional[str] = None,
    ) -> Episode:
        body: Dict[str, Any] = {"agent_id": agent_id, "raw_content": content}
        if conversation_id is not None:
            body["conversation_id"] = conversation_id
        if occurred_at is not None:
            body["occurred_at"] = occurred_at
        if outcome is not None:
            body["outcome"] = outcome
        data = await self._client.request("POST", "/v1/episodes/", json=body)
        return Episode.model_validate(data)

    async def get(self, episode_id: str) -> Episode:
        data = await self._client.request("GET", f"/v1/episodes/{episode_id}")
        return Episode.model_validate(data)

    async def recall(
        self,
        *,
        agent_id: str,
        query: Optional[str] = None,
        min_importance: Optional[float] = None,
        limit: int = 10,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> List[RecalledEpisode]:
        params: Dict[str, Any] = {"agent_id": agent_id, "limit": limit}
        if query is not None:
            params["query"] = query
        if min_importance is not None:
            params["min_importance"] = min_importance
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        data = await self._client.request("GET", "/v1/episodes/recall", params=params)
        episodes = data.get("episodes") or data if isinstance(data, list) else []
        return [RecalledEpisode.model_validate(e) for e in episodes]

    async def record_outcome(
        self,
        episode_id: str,
        *,
        outcome: str,
        description: Optional[str] = None,
    ) -> None:
        body: Dict[str, Any] = {"outcome": outcome}
        if description is not None:
            body["description"] = description
        await self._client.request(
            "POST", f"/v1/episodes/{episode_id}/outcome", json=body
        )

    async def get_associations(self, episode_id: str) -> List[EpisodeAssociation]:
        data = await self._client.request(
            "GET", f"/v1/episodes/{episode_id}/associations"
        )
        return [EpisodeAssociation.model_validate(a) for a in (data or [])]
