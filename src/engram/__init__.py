"""Engram — Python SDK for cognitive memory infrastructure for AI agents."""

from .async_client import AsyncEngram
from .client import Engram
from .exceptions import (
    APIError,
    AuthenticationError,
    ConflictError,
    ConnectionError,
    EngramError,
    NotFoundError,
    ServerError,
    ValidationError,
)
from .types import (
    Agent,
    CognitiveHealth,
    ConfidenceAssessment,
    ConfidenceStats,
    ConsolidationResult,
    DecayResult,
    DecayStatus,
    Episode,
    EpisodeAssociation,
    Entity,
    EvidenceType,
    ExtractedMemory,
    Feedback,
    GraphPath,
    HealthStatus,
    LearningStats,
    Memory,
    MemoryPolicy,
    MemoryTier,
    MemoryType,
    Message,
    Mind,
    MutationLog,
    Outcome,
    Procedure,
    ProvenanceType,
    RecalledEpisode,
    RecalledMemory,
    ReflectionFocus,
    ReflectionResult,
    Relationship,
    Schema,
    SchemaMatch,
    ServerMetrics,
    Tenant,
    TierStats,
    UncertaintyReport,
    WorkingMemory,
    WorkingMemorySession,
)

__all__ = [
    # Clients
    "Engram",
    "AsyncEngram",
    # Exceptions
    "EngramError",
    "APIError",
    "AuthenticationError",
    "NotFoundError",
    "ConflictError",
    "ValidationError",
    "ServerError",
    "ConnectionError",
    # Enums
    "MemoryType",
    "MemoryTier",
    "EvidenceType",
    "ProvenanceType",
    "Outcome",
    "DecayStatus",
    "ReflectionFocus",
    # Core models
    "Tenant",
    "Agent",
    "Memory",
    "RecalledMemory",
    "ExtractedMemory",
    "MemoryPolicy",
    "TierStats",
    "Message",
    # Episodic
    "Episode",
    "RecalledEpisode",
    "EpisodeAssociation",
    # Procedural
    "Procedure",
    # Schemas
    "Schema",
    "SchemaMatch",
    # Graph
    "Entity",
    "Relationship",
    "GraphPath",
    # Cognitive
    "WorkingMemory",
    "WorkingMemorySession",
    "DecayResult",
    "ConsolidationResult",
    "CognitiveHealth",
    "ConfidenceAssessment",
    "ConfidenceStats",
    "UncertaintyReport",
    "ReflectionResult",
    # Mind
    "Mind",
    # Feedback
    "Feedback",
    # Learning
    "LearningStats",
    "MutationLog",
    # Server
    "HealthStatus",
    "ServerMetrics",
]

__version__ = "0.1.0"
