---
source: https://example.com/docs/clean
domain: example.com
crawled_at: 2026-03-31T00:00:00Z
index_hash: fixture_clean_001
page_count: 2
---

# Clean Test Fixture — No Injections

## Pages

### quickstart

URL: https://example.com/docs/en/quickstart
Hash: clean001abc

```
Quickstart Guide

Install the SDK:

pip install anthropic

Create a client:

import anthropic
client = anthropic.Anthropic()

Send a message:

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content[0].text)
```

### streaming

URL: https://example.com/docs/en/streaming
Hash: clean002def

```
Streaming Responses

Use the streaming API for real-time output:

with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a poem"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```
