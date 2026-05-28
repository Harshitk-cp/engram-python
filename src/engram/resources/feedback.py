"""Feedback resource — explicit signal submission for memory quality."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from ..types import Feedback

if TYPE_CHECKING:
    from .._client import AsyncHTTPClient, SyncHTTPClient


class FeedbackResource:
    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def submit(
        self,
        *,
        memory_id: str,
        agent_id: str,
        signal_type: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Feedback:
        """Submit explicit feedback on a memory.

        ``signal_type`` examples: ``positive``, ``negative``, ``correction``.
        """
        body: Dict[str, Any] = {
            "memory_id": memory_id,
            "agent_id": agent_id,
            "signal_type": signal_type,
        }
        if context is not None:
            body["context"] = context
        data = self._client.request("POST", "/v1/feedback", json=body)
        return Feedback.model_validate(data)


class AsyncFeedbackResource:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def submit(
        self,
        *,
        memory_id: str,
        agent_id: str,
        signal_type: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Feedback:
        body: Dict[str, Any] = {
            "memory_id": memory_id,
            "agent_id": agent_id,
            "signal_type": signal_type,
        }
        if context is not None:
            body["context"] = context
        data = await self._client.request("POST", "/v1/feedback", json=body)
        return Feedback.model_validate(data)
