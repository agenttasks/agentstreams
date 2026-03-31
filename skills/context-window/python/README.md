# Python Stack Setup

## Installation (uv)

```bash
# Initialize project
uv init context-window-project && cd context-window-project

# Core Anthropic packages
uv add anthropic

# Token estimation (local, pre-API)
uv add tiktoken==0.9.0             # Approximate token counting

# Text processing
uv add nltk==3.9.1                 # Sentence/paragraph splitting

# Testing
uv add --dev pytest==8.4.0
```

## Package Overview

| Package | Version | Purpose |
|---------|---------|---------|
| `anthropic` | 0.86.0 | Official Python SDK — messages, token counting, caching |
| `tiktoken` | 0.9.0 | Local token estimation — approximate counts without API call |
| `nltk` | 3.9.1 | Text splitting — sentence and paragraph boundaries |

## Quick Start: Count Tokens

```python
import anthropic

client = anthropic.Anthropic()

# Count tokens before sending
token_count = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    messages=[
        {
            "role": "user",
            "content": "Analyze this document: " + large_document,
        }
    ],
)

print(f"Input tokens: {token_count.input_tokens}")
```

## Prompt Caching

```python
import anthropic

client = anthropic.Anthropic()

# First request — cache the system prompt
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert legal analyst. Here is the full contract text: " + contract_text,
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[
        {"role": "user", "content": "What are the termination clauses?"}
    ],
)

# Check cache performance
print(f"Cache creation tokens: {response.usage.cache_creation_input_tokens}")
print(f"Cache read tokens: {response.usage.cache_read_input_tokens}")

# Subsequent requests reuse the cache — ~90% cheaper
response2 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert legal analyst. Here is the full contract text: " + contract_text,
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[
        {"role": "user", "content": "What are the payment terms?"}
    ],
)
```

## Long Document Chunking

```python
import anthropic

client = anthropic.Anthropic()

def chunk_document(text: str, max_tokens: int = 100_000, overlap: int = 5_000) -> list[str]:
    """Split document into chunks that fit within token limits.

    Uses approximate character-to-token ratio (1 token ≈ 4 chars).
    For exact counting, use client.messages.count_tokens().
    """
    chars_per_token = 4
    max_chars = max_tokens * chars_per_token
    overlap_chars = overlap * chars_per_token

    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        # Find paragraph boundary near the end
        if end < len(text):
            boundary = text.rfind("\n\n", start + max_chars - overlap_chars, end)
            if boundary > start:
                end = boundary
        chunks.append(text[start:end])
        start = end - overlap_chars  # overlap for context continuity
    return chunks

# Map-reduce pattern
def analyze_long_document(document: str, question: str) -> str:
    chunks = chunk_document(document)

    # Map: analyze each chunk
    chunk_results = []
    for i, chunk in enumerate(chunks):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": f"Chunk {i+1}/{len(chunks)}:\n\n{chunk}\n\nQuestion: {question}\n\nProvide relevant findings from this chunk only.",
                }
            ],
        )
        chunk_results.append(response.content[0].text)

    # Reduce: combine results
    combined = "\n\n---\n\n".join(chunk_results)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"Here are findings from {len(chunks)} document chunks:\n\n{combined}\n\nSynthesize a final answer to: {question}",
            }
        ],
    )
    return response.content[0].text
```

## Extended Thinking

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16384,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000,
    },
    messages=[
        {
            "role": "user",
            "content": "Solve this complex optimization problem step by step...",
        }
    ],
)

# Access thinking and response
for block in response.content:
    if block.type == "thinking":
        print(f"Thinking ({response.usage.thinking_tokens} tokens):")
        print(block.thinking)
    elif block.type == "text":
        print(f"\nResponse:")
        print(block.text)
```

## Conversation History Management

```python
import anthropic

client = anthropic.Anthropic()

def manage_conversation(messages: list[dict], max_input_tokens: int = 150_000) -> list[dict]:
    """Trim conversation history to fit within token limits."""
    # Count current tokens
    count = client.messages.count_tokens(
        model="claude-sonnet-4-6",
        messages=messages,
    )

    if count.input_tokens <= max_input_tokens:
        return messages

    # Strategy: summarize oldest messages, keep recent ones
    old_messages = messages[:-4]  # keep last 4 messages intact
    recent_messages = messages[-4:]

    # Summarize old context
    summary_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this conversation in 2-3 sentences:\n\n"
                + "\n".join(f"{m['role']}: {m['content']}" for m in old_messages),
            }
        ],
    )

    # Replace old messages with summary
    return [
        {"role": "user", "content": f"[Previous conversation summary: {summary_response.content[0].text}]"},
        {"role": "assistant", "content": "Understood, I have the context from our previous discussion."},
        *recent_messages,
    ]
```

## MCP SDK Availability

Python MCP SDK: `mcp` (PyPI) — build MCP servers that provide context management tools.

```bash
uv add mcp
```
