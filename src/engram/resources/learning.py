"""Learning resource — outcome recording and implicit feedback detection."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast

from ..types import MutationLog

if TYPE_CHECKING:
    from .._client import AsyncHTTPClient, SyncHTTPClient


class Learning:
    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def record_outcome(
        self,
        *,
        episode_id: str,
        outcome: str,
        memories_used: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Record the outcome of an episode and propagate confidence effects to used memories.

        ``outcome`` must be one of: success, failure, neutral.
        ``memories_used`` is a list of memory UUIDs that were active during the episode.
        """
        body: Dict[str, Any] = {
            "episode_id": episode_id,
            "outcome": outcome,
            "memories_used": memories_used or [],
        }
        return cast(Dict[str, Any], self._client.request("POST", "/v1/learning/outcome", json=body))

    def detect_feedback(
        self,
        *,
        agent_id: str,
        memories: List[Dict[str, str]],
        conversation: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """Detect implicit feedback signals from a conversation.

        ``memories`` is a list of ``{"id": "...", "content": "..."}`` dicts for the
        memories that were active during the conversation.
        ``conversation`` is a list of ``{"role": "...", "content": "..."}`` dicts.

        Returns ``{"detected_count": N, "feedbacks": [...]}``.
        """
        body: Dict[str, Any] = {
            "agent_id": agent_id,
            "memories": memories,
            "conversation": conversation,
        }
        return cast(Dict[str, Any], self._client.request("POST", "/v1/learning/detect-feedback", json=body))

    def get_mutation_history(
        self,
        memory_id: str,
        *,
        limit: int = 50,
    ) -> List[MutationLog]:
        """Get the confidence mutation history for a memory (audit trail)."""
        data = self._client.request(
            "GET",
            f"/v1/memories/{memory_id}/mutations",
            params={"limit": limit},
        )
        return [MutationLog.model_validate(m) for m in (data.get("mutations") or [])]


class AsyncLearning:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def record_outcome(
        self,
        *,
        episode_id: str,
        outcome: str,
        memories_used: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "episode_id": episode_id,
            "outcome": outcome,
            "memories_used": memories_used or [],
        }
        return cast(Dict[str, Any], await self._client.request("POST", "/v1/learning/outcome", json=body))

    async def detect_feedback(
        self,
        *,
        agent_id: str,
        memories: List[Dict[str, str]],
        conversation: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "agent_id": agent_id,
            "memories": memories,
            "conversation": conversation,
        }
        return cast(Dict[str, Any], await self._client.request(
            "POST", "/v1/learning/detect-feedback", json=body
        ))

    async def get_mutation_history(
        self,
        memory_id: str,
        *,
        limit: int = 50,
    ) -> List[MutationLog]:
        data = await self._client.request(
            "GET",
            f"/v1/memories/{memory_id}/mutations",
            params={"limit": limit},
        )
        return [MutationLog.model_validate(m) for m in (data.get("mutations") or [])]
