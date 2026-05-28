# engram

Python SDK for [Engram](https://github.com/engram-labs/engram) — cognitive memory infrastructure for AI agents.

## Installation

```bash
pip install engram
```

## Quick Start

Set environment variables (the SDK reads these automatically):

```bash
export ENGRAM_BASE_URL=http://localhost:8080
export ENGRAM_API_KEY=your-api-key
```

```python
from engram import Engram, MemoryType, Message

# No args needed — reads ENGRAM_BASE_URL and ENGRAM_API_KEY from env
client = Engram()

# Register an agent
agent = client.agents.create(external_id="assistant-1", name="My Assistant")

# Store a memory
memory = client.memories.store(
    agent_id=agent.id,
    content="User prefers dark mode",
    type=MemoryType.PREFERENCE,
    confidence=0.9,
)

# Recall memories (hybrid vector + graph search)
results = client.memories.recall(
    agent_id=agent.id,
    query="What are the user's UI preferences?",
    top_k=5,
)
for mem in results:
    print(f"[{mem.confidence:.2f}] {mem.content}")

# Extract memories from a conversation
extracted = client.memories.extract(
    agent_id=agent.id,
    conversation=[
        Message(role="user", content="I always use vim keybindings"),
        Message(role="assistant", content="Noted! I'll remember your preference for vim."),
    ],
    auto_store=True,
)
```

You can also pass values explicitly (overrides env vars):

```python
client = Engram(base_url="http://localhost:8080", api_key="your-api-key")
```

## Async Support

```python
import asyncio
from engram import AsyncEngram

async def main():
    # Reads ENGRAM_BASE_URL and ENGRAM_API_KEY from env
    async with AsyncEngram() as client:
        agent = await client.agents.create(
            external_id="async-agent",
            name="Async Agent",
        )
        memory = await client.memories.store(
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
client.memories.store(agent_id=, content=, type=, confidence=, metadata=)

# Retrieve
client.memories.get(memory_id)

# Delete
client.memories.delete(memory_id)

# Hybrid recall (vector + graph)
client.memories.recall(agent_id=, query=, top_k=, type=, min_confidence=, graph_weight=, max_hops=)

# Extract from conversation
client.memories.extract(agent_id=, conversation=, auto_store=)
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
client.cognitive.health()                        # aggregate stats, no agent_id

# Working memory
result = client.cognitive.activate(agent_id=, query=, goal=)
client.cognitive.get_session(agent_id)
client.cognitive.update_goal(agent_id, goal=)
client.cognitive.clear_session(agent_id)

# Metacognition
client.cognitive.reflect(agent_id, focus="all")
client.cognitive.detect_uncertainty(agent_id, topic=)
client.cognitive.assess_confidence(agent_id=, query=)

# Confidence management
client.cognitive.get_confidence_stats(memory_id)
client.cognitive.reinforce(memory_id, boost=0.1)
client.cognitive.penalize(memory_id, penalty=0.15)
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
mind = client.agents.get_mind(agent_id)
print(mind.beliefs)
print(mind.procedures)
print(mind.schemas)
print(mind.stats)

# Tier statistics
stats = client.agents.get_tier_stats(agent_id)
print(f"Hot: {stats.hot_count}, Warm: {stats.warm_count}")

# Hot memories (auto-injected tier)
hot = client.agents.get_hot_memories(agent_id, limit=10)
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
