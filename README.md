# engram

Python SDK for [Engram](https://github.com/engram-labs/engram) — cognitive memory infrastructure for AI agents.

## Installation

```bash
pip install engram
```

## Quick Start

```python
from engram import Engram, MemoryType, Message

# Bootstrap: create a tenant (no auth required)
client = Engram(base_url="http://localhost:3741")
tenant = client.tenants.create(name="my-org")

# Now use the API key for authenticated requests
client = Engram(base_url="http://localhost:3741", api_key=tenant.api_key)

# Register an agent
agent = client.agents.create(external_id="assistant-1", name="My Assistant")

# Store memories
memory = client.memories.create(
    agent_id=agent.id,
    content="User prefers dark mode",
    type=MemoryType.PREFERENCE,
    confidence=0.9,
)

# Recall memories (hybrid vector + graph search)
results = client.memories.recall(
    query="What are the user's UI preferences?",
    agent_id=agent.id,
    top_k=5,
)
for mem in results:
    print(f"[{mem.confidence:.2f}] {mem.content}")

# Extract memories from conversations
extracted = client.memories.extract(
    agent_id=agent.id,
    conversation=[
        Message(role="user", content="I always use vim keybindings"),
        Message(role="assistant", content="Noted! I'll remember your preference for vim."),
    ],
    auto_store=True,
)
```

## Async Support

```python
import asyncio
from engram import AsyncEngram

async def main():
    async with AsyncEngram(api_key="mk_...") as client:
        agent = await client.agents.create(
            external_id="async-agent",
            name="Async Agent",
        )
        memory = await client.memories.create(
            agent_id=agent.id,
            content="User likes Python",
            type="preference",
        )
        print(memory)

asyncio.run(main())
```

## API Reference

### Client

| Resource | Description |
|----------|-------------|
| `client.tenants` | Create tenants and obtain API keys |
| `client.agents` | Register and manage AI agents |
| `client.memories` | Store, recall, and extract semantic memories |
| `client.episodes` | Record and query episodic experiences |
| `client.procedures` | Match and learn procedural skills |
| `client.schemas` | Manage mental models and schemas |
| `client.graph` | Query entity and relationship graphs |
| `client.cognitive` | Decay, consolidation, working memory, reflection |
| `client.feedback` | Submit feedback signals on memories |

### Memories

```python
# Store
client.memories.create(agent_id, content, type=, confidence=, metadata=)

# Retrieve
client.memories.get(memory_id)

# Delete
client.memories.delete(memory_id)

# Hybrid recall (vector + graph)
client.memories.recall(query, agent_id, top_k=, type=, min_confidence=, graph_weight=, max_hops=)

# Extract from conversation
client.memories.extract(agent_id, conversation, auto_store=)
```

### Episodes

```python
client.episodes.create(agent_id, raw_content, outcome=)
client.episodes.get(episode_id)
client.episodes.recall(agent_id, query=, limit=, min_importance=)
client.episodes.record_outcome(episode_id, outcome, description=)
client.episodes.associations(episode_id)
```

### Procedures

```python
client.procedures.match(agent_id, situation, min_success_rate=, min_confidence=)
client.procedures.get(procedure_id)
client.procedures.learn(episode_id, outcome)
client.procedures.record_outcome(procedure_id, success)
```

### Cognitive Operations

```python
# Memory lifecycle
client.cognitive.decay(agent_id)
client.cognitive.consolidate(agent_id, scope="recent")
client.cognitive.health(agent_id)

# Working memory
result = client.cognitive.activate(agent_id, cues=["dark mode"], goal="personalize UI")
client.cognitive.session(agent_id)
client.cognitive.update_goal(agent_id, goal="new goal")
client.cognitive.clear_session(agent_id)

# Metacognition
client.cognitive.reflect(agent_id, focus="all")
client.cognitive.uncertainty(agent_id, topic="preferences")

# Confidence management
client.cognitive.confidence_stats(memory_id)
client.cognitive.reinforce(memory_id)
client.cognitive.penalize(memory_id)
```

### Graph

```python
client.graph.entities(agent_id)
client.graph.relationships(memory_id, depth=2)
client.graph.traverse(start_ids=["..."], max_depth=3)
```

### Agent Mind State

```python
# Get complete mental state
mind = client.agents.mind(agent_id)
print(mind.beliefs)
print(mind.procedures)
print(mind.schemas)
print(mind.stats)

# Tier statistics
stats = client.agents.tier_stats(agent_id)
print(f"Hot: {stats.hot_count}, Warm: {stats.warm_count}")

# Hot memories (auto-injected tier)
hot = client.agents.hot_memories(agent_id, limit=10)
```

## Error Handling

```python
from engram import Engram, AuthenticationError, NotFoundError, ValidationError

client = Engram(api_key="mk_...")

try:
    memory = client.memories.get("nonexistent-id")
except NotFoundError:
    print("Memory not found")
except AuthenticationError:
    print("Invalid API key")
except ValidationError as e:
    print(f"Bad request: {e.message}")
```

## License

Apache 2.0
