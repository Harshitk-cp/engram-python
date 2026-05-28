"""Tests for the Engram Python SDK."""

from __future__ import annotations

import pytest
import respx
import httpx

from engram import (
    AsyncEngram,
    Engram,
    Memory,
    MemoryType,
    MemoryTier,
    Tenant,
    Agent,
    RecalledMemory,
)
from engram.exceptions import AuthenticationError, NotFoundError, ValidationError


BASE_URL = "http://test.local"

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sync_client():
    return Engram(base_url=BASE_URL, api_key="test-key")


@pytest.fixture
def async_client():
    return AsyncEngram(base_url=BASE_URL, api_key="test-key")


# ---------------------------------------------------------------------------
# Tenants
# ---------------------------------------------------------------------------

@respx.mock
def test_tenant_create(sync_client: Engram):
    respx.post(f"{BASE_URL}/v1/tenants").mock(
        return_value=httpx.Response(
            201,
            json={"id": "tenant-1", "name": "Test Org", "api_key": "secret-key"},
        )
    )
    tenant = sync_client.tenants.create(name="Test Org")
    assert isinstance(tenant, Tenant)
    assert tenant.id == "tenant-1"
    assert tenant.api_key == "secret-key"


@respx.mock
@pytest.mark.asyncio
async def test_tenant_create_async(async_client: AsyncEngram):
    respx.post(f"{BASE_URL}/v1/tenants").mock(
        return_value=httpx.Response(
            201,
            json={"id": "t-2", "name": "Async Org", "api_key": "async-key"},
        )
    )
    tenant = await async_client.tenants.create(name="Async Org")
    assert tenant.name == "Async Org"


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------

AGENT_PAYLOAD = {
    "id": "agent-uuid",
    "tenant_id": "tenant-1",
    "external_id": "bot-1",
    "name": "My Bot",
    "metadata": None,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
}


@respx.mock
def test_agent_create(sync_client: Engram):
    respx.post(f"{BASE_URL}/v1/agents/").mock(
        return_value=httpx.Response(201, json=AGENT_PAYLOAD)
    )
    agent = sync_client.agents.create(external_id="bot-1", name="My Bot")
    assert isinstance(agent, Agent)
    assert agent.external_id == "bot-1"


@respx.mock
def test_agent_get(sync_client: Engram):
    respx.get(f"{BASE_URL}/v1/agents/agent-uuid").mock(
        return_value=httpx.Response(200, json=AGENT_PAYLOAD)
    )
    agent = sync_client.agents.get("agent-uuid")
    assert agent.id == "agent-uuid"


# ---------------------------------------------------------------------------
# Memories
# ---------------------------------------------------------------------------

MEMORY_PAYLOAD = {
    "id": "mem-1",
    "agent_id": "agent-uuid",
    "tenant_id": "tenant-1",
    "type": "preference",
    "content": "User prefers dark mode",
    "confidence": 0.9,
    "reinforcement_count": 0,
    "tier": "hot",
    "tier_reason": "high confidence",
    "reinforced": False,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
}


@respx.mock
def test_memory_store(sync_client: Engram):
    respx.post(f"{BASE_URL}/v1/memories/").mock(
        return_value=httpx.Response(201, json=MEMORY_PAYLOAD)
    )
    mem = sync_client.memories.store(
        agent_id="agent-uuid",
        content="User prefers dark mode",
        type="preference",
        confidence=0.9,
    )
    assert isinstance(mem, Memory)
    assert mem.type == MemoryType.PREFERENCE
    assert mem.confidence == 0.9
    assert mem.tier == MemoryTier.HOT


@respx.mock
def test_memory_get(sync_client: Engram):
    respx.get(f"{BASE_URL}/v1/memories/mem-1").mock(
        return_value=httpx.Response(200, json=MEMORY_PAYLOAD)
    )
    mem = sync_client.memories.get("mem-1")
    assert mem.id == "mem-1"


@respx.mock
def test_memory_delete(sync_client: Engram):
    respx.delete(f"{BASE_URL}/v1/memories/mem-1").mock(
        return_value=httpx.Response(204)
    )
    # Should not raise
    sync_client.memories.delete("mem-1")


@respx.mock
def test_memory_recall(sync_client: Engram):
    recalled = {**MEMORY_PAYLOAD, "score": 0.92, "vector_score": 0.88, "graph_score": 0.41}
    respx.get(f"{BASE_URL}/v1/memories/recall").mock(
        return_value=httpx.Response(
            200,
            json={"memories": [recalled], "query": "dark mode", "count": 1},
        )
    )
    result = sync_client.memories.recall(agent_id="agent-uuid", query="dark mode")
    assert result.count == 1
    assert len(result) == 1
    mem = result.memories[0]
    assert isinstance(mem, RecalledMemory)
    assert mem.score == pytest.approx(0.92)
    assert mem.vector_score == pytest.approx(0.88)


@respx.mock
def test_memory_extract(sync_client: Engram):
    respx.post(f"{BASE_URL}/v1/memories/extract").mock(
        return_value=httpx.Response(
            200,
            json={
                "extracted": [
                    {
                        "id": "mem-2",
                        "type": "preference",
                        "content": "User likes dark mode",
                        "confidence": 0.85,
                        "stored": True,
                        "reinforced": False,
                    }
                ],
                "count": 1,
            },
        )
    )
    result = sync_client.memories.extract(
        agent_id="agent-uuid",
        conversation=[
            {"role": "user", "content": "I always use dark mode"},
            {"role": "assistant", "content": "Noted, I'll keep dark mode enabled."},
        ],
    )
    assert result.count == 1
    item = result.extracted[0]
    assert item.content == "User likes dark mode"
    assert item.stored_id == "mem-2"


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

@respx.mock
def test_not_found_raises(sync_client: Engram):
    respx.get(f"{BASE_URL}/v1/memories/bad-id").mock(
        return_value=httpx.Response(404, json={"error": "memory not found"})
    )
    with pytest.raises(NotFoundError) as exc_info:
        sync_client.memories.get("bad-id")
    assert exc_info.value.status_code == 404


@respx.mock
def test_auth_error_raises(sync_client: Engram):
    respx.post(f"{BASE_URL}/v1/memories/").mock(
        return_value=httpx.Response(401, json={"error": "unauthorized"})
    )
    with pytest.raises(AuthenticationError):
        sync_client.memories.store(agent_id="x", content="y")


@respx.mock
def test_validation_error_raises(sync_client: Engram):
    respx.post(f"{BASE_URL}/v1/memories/").mock(
        return_value=httpx.Response(400, json={"error": "content is required"})
    )
    with pytest.raises(ValidationError) as exc_info:
        sync_client.memories.store(agent_id="x", content="")
    assert "content is required" in str(exc_info.value)


# ---------------------------------------------------------------------------
# API key is sent per-request (dynamic update support)
# ---------------------------------------------------------------------------

@respx.mock
def test_api_key_sent_in_header():
    client = Engram(base_url=BASE_URL, api_key="my-key")

    def check_auth(request: httpx.Request):
        assert request.headers.get("authorization") == "Bearer my-key"
        return httpx.Response(200, json={"status": "ok"})

    respx.get(f"{BASE_URL}/health").mock(side_effect=check_auth)
    client.health()


@respx.mock
def test_api_key_dynamic_update():
    """Updating _http.api_key after construction should take effect on next request."""
    client = Engram(base_url=BASE_URL)  # no key initially

    def check_auth(request: httpx.Request):
        assert request.headers.get("authorization") == "Bearer new-key"
        return httpx.Response(200, json={"status": "ok"})

    respx.get(f"{BASE_URL}/health").mock(side_effect=check_auth)
    client._http.api_key = "new-key"
    client.health()


def test_missing_base_url_raises(monkeypatch):
    """No base_url arg and no ENGRAM_BASE_URL env var must raise ValueError."""
    monkeypatch.delenv("ENGRAM_BASE_URL", raising=False)
    monkeypatch.delenv("ENGRAM_API_KEY", raising=False)
    with pytest.raises(ValueError, match="ENGRAM_BASE_URL"):
        Engram()


def test_base_url_from_env(monkeypatch):
    """ENGRAM_BASE_URL env var is used when no explicit base_url is passed."""
    monkeypatch.setenv("ENGRAM_BASE_URL", BASE_URL)
    monkeypatch.setenv("ENGRAM_API_KEY", "env-key")
    client = Engram()
    assert client._http.base_url == BASE_URL
    assert client._http.api_key == "env-key"


def test_explicit_args_override_env(monkeypatch):
    """Explicit constructor args take precedence over env vars."""
    monkeypatch.setenv("ENGRAM_BASE_URL", "http://should-not-be-used")
    monkeypatch.setenv("ENGRAM_API_KEY", "env-key")
    client = Engram(base_url=BASE_URL, api_key="explicit-key")
    assert client._http.base_url == BASE_URL
    assert client._http.api_key == "explicit-key"
