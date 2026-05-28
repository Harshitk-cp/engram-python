"""Cognitive operations — decay, consolidation, working memory, metacognition, confidence."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from ..types import (
    CognitiveHealth,
    ConfidenceAssessment,
    ConfidenceStats,
    ConsolidationResult,
    DecayResult,
    ReflectionResult,
    UncertaintyReport,
    WorkingMemory,
    WorkingMemorySession,
)

if TYPE_CHECKING:
    from .._client import AsyncHTTPClient, SyncHTTPClient


class Cognitive:
    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    # --- Lifecycle ---

    def decay(self, agent_id: str) -> DecayResult:
        """Trigger memory decay for an agent (applies confidence decay and archives weak memories)."""
        data = self._client.request("POST", "/v1/cognitive/decay", json={"agent_id": agent_id})
        return DecayResult.model_validate(data)

    def consolidate(
        self,
        agent_id: str,
        *,
        scope: Optional[str] = None,
    ) -> ConsolidationResult:
        """Run the consolidation pipeline: episodes → beliefs → procedures → schemas.

        ``scope`` is one of: recent (default), full.
        """
        body: Dict[str, Any] = {"agent_id": agent_id}
        if scope is not None:
            body["scope"] = scope
        data = self._client.request("POST", "/v1/cognitive/consolidate", json=body)
        return ConsolidationResult.model_validate(data)

    def health(self) -> CognitiveHealth:
        """Return aggregate memory health statistics."""
        data = self._client.request("GET", "/v1/cognitive/health")
        return CognitiveHealth.model_validate(data)

    # --- Working memory ---

    def activate(
        self,
        *,
        agent_id: str,
        query: str,
        goal: Optional[str] = None,
    ) -> WorkingMemory:
        """Prime working memory for a task: retrieves and activates relevant memories."""
        body: Dict[str, Any] = {"agent_id": agent_id, "query": query}
        if goal is not None:
            body["goal"] = goal
        data = self._client.request("POST", "/v1/cognitive/activate", json=body)
        return WorkingMemory.model_validate(data)

    def get_session(self, agent_id: str) -> WorkingMemorySession:
        """Get the current working memory session for an agent."""
        data = self._client.request(
            "GET", "/v1/cognitive/session", params={"agent_id": agent_id}
        )
        return WorkingMemorySession.model_validate(data)

    def update_goal(self, agent_id: str, goal: str) -> None:
        """Update the active goal in the working memory session."""
        self._client.request(
            "PUT", "/v1/cognitive/goal", json={"agent_id": agent_id, "goal": goal}
        )

    def clear_session(self, agent_id: str) -> None:
        """Clear the working memory session for an agent."""
        self._client.request(
            "DELETE", "/v1/cognitive/session", params={"agent_id": agent_id}
        )

    # --- Metacognition ---

    def reflect(
        self,
        agent_id: str,
        *,
        focus: Optional[str] = None,
    ) -> ReflectionResult:
        """Trigger metacognitive self-assessment.

        ``focus`` is one of: confidence, uncertainty, strategy, all (default).
        """
        body: Dict[str, Any] = {"agent_id": agent_id}
        if focus is not None:
            body["focus"] = focus
        data = self._client.request("POST", "/v1/cognitive/reflect", json=body)
        return ReflectionResult.model_validate(data)

    def assess_confidence(self, *, agent_id: str, query: str) -> ConfidenceAssessment:
        """Assess confidence in a specific query / topic."""
        data = self._client.request(
            "GET",
            "/v1/cognitive/confidence",
            params={"agent_id": agent_id, "query": query},
        )
        return ConfidenceAssessment.model_validate(data)

    def detect_uncertainty(
        self,
        agent_id: str,
        *,
        topic: Optional[str] = None,
    ) -> UncertaintyReport:
        """Surface areas of low confidence or active contradiction."""
        params: Dict[str, Any] = {"agent_id": agent_id}
        if topic is not None:
            params["topic"] = topic
        data = self._client.request("GET", "/v1/cognitive/uncertainty", params=params)
        return UncertaintyReport.model_validate(data)

    # --- Confidence lifecycle ---

    def get_confidence_stats(self, memory_id: str) -> ConfidenceStats:
        data = self._client.request(
            "GET", "/v1/cognitive/confidence/stats", params={"memory_id": memory_id}
        )
        return ConfidenceStats.model_validate(data)

    def reinforce(self, memory_id: str, *, boost: float = 0.1) -> None:
        """Manually boost a memory's confidence."""
        self._client.request(
            "POST",
            "/v1/cognitive/confidence/reinforce",
            json={"memory_id": memory_id, "boost": boost},
        )

    def penalize(self, memory_id: str, *, penalty: float = 0.15) -> None:
        """Manually penalize a memory's confidence."""
        self._client.request(
            "POST",
            "/v1/cognitive/confidence/penalize",
            json={"memory_id": memory_id, "penalty": penalty},
        )


class AsyncCognitive:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def decay(self, agent_id: str) -> DecayResult:
        data = await self._client.request(
            "POST", "/v1/cognitive/decay", json={"agent_id": agent_id}
        )
        return DecayResult.model_validate(data)

    async def consolidate(
        self,
        agent_id: str,
        *,
        scope: Optional[str] = None,
    ) -> ConsolidationResult:
        body: Dict[str, Any] = {"agent_id": agent_id}
        if scope is not None:
            body["scope"] = scope
        data = await self._client.request("POST", "/v1/cognitive/consolidate", json=body)
        return ConsolidationResult.model_validate(data)

    async def health(self) -> CognitiveHealth:
        data = await self._client.request("GET", "/v1/cognitive/health")
        return CognitiveHealth.model_validate(data)

    async def activate(
        self,
        *,
        agent_id: str,
        query: str,
        goal: Optional[str] = None,
    ) -> WorkingMemory:
        body: Dict[str, Any] = {"agent_id": agent_id, "query": query}
        if goal is not None:
            body["goal"] = goal
        data = await self._client.request("POST", "/v1/cognitive/activate", json=body)
        return WorkingMemory.model_validate(data)

    async def get_session(self, agent_id: str) -> WorkingMemorySession:
        data = await self._client.request(
            "GET", "/v1/cognitive/session", params={"agent_id": agent_id}
        )
        return WorkingMemorySession.model_validate(data)

    async def update_goal(self, agent_id: str, goal: str) -> None:
        await self._client.request(
            "PUT", "/v1/cognitive/goal", json={"agent_id": agent_id, "goal": goal}
        )

    async def clear_session(self, agent_id: str) -> None:
        await self._client.request(
            "DELETE", "/v1/cognitive/session", params={"agent_id": agent_id}
        )

    async def reflect(
        self,
        agent_id: str,
        *,
        focus: Optional[str] = None,
    ) -> ReflectionResult:
        body: Dict[str, Any] = {"agent_id": agent_id}
        if focus is not None:
            body["focus"] = focus
        data = await self._client.request("POST", "/v1/cognitive/reflect", json=body)
        return ReflectionResult.model_validate(data)

    async def assess_confidence(
        self, *, agent_id: str, query: str
    ) -> ConfidenceAssessment:
        data = await self._client.request(
            "GET",
            "/v1/cognitive/confidence",
            params={"agent_id": agent_id, "query": query},
        )
        return ConfidenceAssessment.model_validate(data)

    async def detect_uncertainty(
        self,
        agent_id: str,
        *,
        topic: Optional[str] = None,
    ) -> UncertaintyReport:
        params: Dict[str, Any] = {"agent_id": agent_id}
        if topic is not None:
            params["topic"] = topic
        data = await self._client.request(
            "GET", "/v1/cognitive/uncertainty", params=params
        )
        return UncertaintyReport.model_validate(data)

    async def get_confidence_stats(self, memory_id: str) -> ConfidenceStats:
        data = await self._client.request(
            "GET", "/v1/cognitive/confidence/stats", params={"memory_id": memory_id}
        )
        return ConfidenceStats.model_validate(data)

    async def reinforce(self, memory_id: str, *, boost: float = 0.1) -> None:
        await self._client.request(
            "POST",
            "/v1/cognitive/confidence/reinforce",
            json={"memory_id": memory_id, "boost": boost},
        )

    async def penalize(self, memory_id: str, *, penalty: float = 0.15) -> None:
        await self._client.request(
            "POST",
            "/v1/cognitive/confidence/penalize",
            json={"memory_id": memory_id, "penalty": penalty},
        )
