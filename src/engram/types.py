"""Engram SDK data types and models."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# --- Enums ---


class MemoryType(str, Enum):
    PREFERENCE = "preference"
    FACT = "fact"
    DECISION = "decision"
    CONSTRAINT = "constraint"


class MemoryTier(str, Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"
    ARCHIVE = "archive"


class DecayStatus(str, Enum):
    HEALTHY = "healthy"
    DECAYING = "decaying"
    AT_RISK = "at_risk"


class Outcome(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"


class EvidenceType(str, Enum):
    EXPLICIT_STATEMENT = "explicit_statement"
    IMPLICIT_INFERENCE = "implicit_inference"
    BEHAVIORAL_SIGNAL = "behavioral_signal"


class ProvenanceType(str, Enum):
    USER = "user"
    TOOL = "tool"
    AGENT = "agent"
    DERIVED = "derived"
    INFERRED = "inferred"


class ReflectionFocus(str, Enum):
    CONFIDENCE = "confidence"
    UNCERTAINTY = "uncertainty"
    STRATEGY = "strategy"
    ALL = "all"


class ConsolidationScope(str, Enum):
    RECENT = "recent"
    FULL = "full"


# --- Tenant ---


class Tenant(BaseModel):
    id: str
    name: str
    api_key: Optional[str] = None


# --- Agent ---


class Agent(BaseModel):
    id: str
    tenant_id: str
    external_id: str
    name: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MemoryPolicy(BaseModel):
    memory_type: MemoryType
    max_memories: int
    retention_days: Optional[int] = None
    priority_weight: float
    auto_summarize: Optional[bool] = None


class TierStats(BaseModel):
    hot_count: int
    warm_count: int
    cold_count: int
    archive_count: int


# --- Memory ---


class Memory(BaseModel):
    id: str
    agent_id: str
    tenant_id: str
    type: MemoryType
    content: str
    source: Optional[str] = None
    confidence: float
    metadata: Optional[Dict[str, Any]] = None
    reinforced: Optional[bool] = None
    reinforcement_count: Optional[int] = None
    tier: Optional[MemoryTier] = None
    tier_reason: Optional[str] = None
    decay_status: Optional[DecayStatus] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RecalledMemory(Memory):
    score: Optional[float] = None
    vector_score: Optional[float] = None
    graph_score: Optional[float] = None
    graph_path: Optional[List[str]] = None
    path_length: Optional[int] = None


class ExtractedMemory(BaseModel):
    memory_type: MemoryType
    content: str
    confidence: float
    evidence: EvidenceType
    stored_id: Optional[str] = None


# --- Episode ---


class Episode(BaseModel):
    id: str
    agent_id: str
    tenant_id: Optional[str] = None
    raw_content: str
    conversation_id: Optional[str] = None
    occurred_at: Optional[datetime] = None
    outcome: Optional[Outcome] = None
    importance_score: Optional[float] = None
    topics: Optional[List[str]] = None
    consolidation_status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RecalledEpisode(BaseModel):
    id: str
    agent_id: str
    raw_content: str
    occurred_at: Optional[datetime] = None
    importance_score: Optional[float] = None
    score: Optional[float] = None
    outcome: Optional[str] = None


class EpisodeAssociation(BaseModel):
    memory_id: str
    association_type: str
    strength: float


# --- Procedure ---


class ProcedureExample(BaseModel):
    user_input: str
    assistant_response: str


class Procedure(BaseModel):
    id: str
    trigger_pattern: Optional[str] = None
    trigger_keywords: Optional[List[str]] = None
    action_template: Optional[str] = None
    action_type: Optional[str] = None
    use_count: Optional[int] = None
    success_count: Optional[int] = None
    failure_count: Optional[int] = None
    success_rate: Optional[float] = None
    confidence: Optional[float] = None
    version: Optional[int] = None
    score: Optional[float] = None
    examples: Optional[List[ProcedureExample]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# --- Schema ---


class Schema(BaseModel):
    id: str
    agent_id: str
    schema_type: Optional[str] = None
    name: str
    description: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    evidence_count: Optional[int] = None
    confidence: Optional[float] = None
    contradiction_count: Optional[int] = None
    applicable_contexts: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SchemaMatch(BaseModel):
    schema_: Schema = Field(alias="schema")
    match_score: float
    match_reason: Optional[str] = None

    model_config = {"populate_by_name": True}


# --- Graph ---


class Entity(BaseModel):
    id: str
    name: str
    entity_type: str
    aliases: Optional[List[str]] = None
    memory_count: Optional[int] = None


class Relationship(BaseModel):
    source_id: str
    target_id: str
    relation_type: str
    strength: float
    traversal_count: Optional[int] = None


class GraphPath(BaseModel):
    path: List[str]
    path_length: int
    total_strength: float


# --- Cognitive ---


class WorkingMemoryActivation(BaseModel):
    memory_type: str
    memory_id: str
    content: str
    confidence: float
    score: float


class ActiveSchema(BaseModel):
    schema_id: str
    name: str
    description: Optional[str] = None
    match_score: float


class WorkingMemory(BaseModel):
    session_id: Optional[str] = None
    current_goal: Optional[str] = None
    activations: List[WorkingMemoryActivation] = []
    active_schemas: List[ActiveSchema] = []
    slot_usage: Optional[int] = None
    max_slots: Optional[int] = None


class WorkingMemorySession(WorkingMemory):
    agent_id: Optional[str] = None
    active_context: Optional[List[Dict[str, str]]] = None
    reasoning_state: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    last_activity_at: Optional[datetime] = None


class DecayResult(BaseModel):
    memories_decayed: int
    memories_archived: int
    episodes_decayed: int
    episodes_archived: int


class ConsolidationResult(BaseModel):
    episodes_processed: int
    semantic_extracted: int
    semantic_reinforced: int
    procedures_learned: int
    procedures_reinforced: int
    schemas_detected: int
    schemas_updated: int
    memories_decayed: int
    memories_archived: int
    memories_merged: int
    associations_created: int


class CognitiveHealth(BaseModel):
    episodic_count: int
    semantic_count: int
    procedural_count: int
    schema_count: int
    memories_at_risk: int
    recently_reinforced: int
    contradiction_count: int
    uncertainty_areas: Optional[List[str]] = None
    average_confidence: float
    oldest_unprocessed: Optional[datetime] = None


class ConfidenceAssessment(BaseModel):
    memory_id: str
    content: Optional[str] = None
    memory_type: Optional[str] = None
    base_confidence: float
    adjusted_confidence: float
    factors: Optional[Dict[str, Any]] = None
    explanation: Optional[str] = None


class UncertaintyReport(BaseModel):
    topic: Optional[str] = None
    uncertainty_level: float
    contradicted_beliefs: Optional[List[Dict[str, Any]]] = None
    low_confidence_beliefs: Optional[List[Dict[str, Any]]] = None
    stale_beliefs: Optional[List[Dict[str, Any]]] = None
    recommendation: Optional[str] = None


class StrategyReflection(BaseModel):
    effective_strategies: Optional[List[Dict[str, Any]]] = None
    underperforming_strategies: Optional[List[Dict[str, Any]]] = None
    failure_patterns: Optional[List[Dict[str, Any]]] = None
    suggestions: Optional[List[str]] = None


class ReflectionResult(BaseModel):
    confidence_assessments: Optional[List[ConfidenceAssessment]] = None
    uncertainty_report: Optional[UncertaintyReport] = None
    strategy_reflection: Optional[StrategyReflection] = None
    overall_health_score: Optional[float] = None
    action_items: Optional[List[str]] = None


class ConfidenceStats(BaseModel):
    memory_id: str
    raw_confidence: float
    decayed_confidence: float
    reinforcement_count: int
    provenance: Optional[str] = None
    hours_since_access: Optional[float] = None
    decay_factor: Optional[float] = None


# --- Mind ---


class BeliefSummary(BaseModel):
    id: str
    type: MemoryType
    content: str
    confidence: float
    reinforcement_count: Optional[int] = None
    decay_status: Optional[DecayStatus] = None


class ProcedureSummary(BaseModel):
    id: str
    trigger_pattern: Optional[str] = None
    action_template: Optional[str] = None
    action_type: Optional[str] = None
    success_rate: Optional[float] = None
    use_count: Optional[int] = None


class SchemaSummary(BaseModel):
    id: str
    schema_type: Optional[str] = None
    name: str
    description: Optional[str] = None
    confidence: Optional[float] = None
    attributes: Optional[Dict[str, Any]] = None


class EpisodeSummary(BaseModel):
    id: str
    raw_content: str
    occurred_at: Optional[datetime] = None
    importance_score: Optional[float] = None
    outcome: Optional[str] = None
    topics: Optional[List[str]] = None


class MindStats(BaseModel):
    total_memories: int
    total_episodes: int
    total_procedures: int
    total_schemas: int
    archived: int
    avg_confidence: float
    at_risk: int


class Mind(BaseModel):
    agent_id: str
    beliefs: List[BeliefSummary] = []
    procedures: List[ProcedureSummary] = []
    schemas: List[SchemaSummary] = []
    recent_episodes: List[EpisodeSummary] = []
    stats: Optional[MindStats] = None


# --- Feedback ---


class Feedback(BaseModel):
    id: str
    memory_id: str
    agent_id: str
    signal_type: str
    context: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None


# --- Learning ---


class LearningStats(BaseModel):
    id: Optional[str] = None
    agent_id: str
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    helpful_count: int = 0
    unhelpful_count: int = 0
    ignored_count: int = 0
    contradicted_count: int = 0
    outdated_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    neutral_count: int = 0
    confidence_increases: int = 0
    confidence_decreases: int = 0
    memories_reinforced: int = 0
    memories_archived: int = 0
    learning_velocity: Optional[float] = None
    stability_score: Optional[float] = None
    created_at: Optional[datetime] = None


class MutationLog(BaseModel):
    id: str
    memory_id: str
    agent_id: str
    mutation_type: str
    source_type: str
    source_id: Optional[str] = None
    old_confidence: Optional[float] = None
    new_confidence: Optional[float] = None
    old_reinforcement_count: Optional[int] = None
    new_reinforcement_count: Optional[int] = None
    reason: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None


# --- Health & Metrics ---


class HealthStatus(BaseModel):
    status: str


class ServerMetrics(BaseModel):
    uptime_seconds: float
    uptime_human: Optional[str] = None
    request_count: int
    error_count: int
    goroutines: Optional[int] = None
    memory: Optional[Dict[str, Any]] = None
    go_version: Optional[str] = None


# --- Message (used in conversation inputs) ---


class Message(BaseModel):
    role: str
    content: str
