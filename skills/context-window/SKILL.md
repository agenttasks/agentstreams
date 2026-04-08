---
name: context-window
description: "Context window management, token counting, and prompt optimization with Claude. TRIGGER when: user asks about context window limits, token counting, prompt compression, long document processing, conversation management, context caching, or needs to optimize token usage. Also triggers for extended thinking budget, message truncation, sliding window patterns, or context-aware chunking. DO NOT TRIGGER for: image processing (use vision), code execution (use code-execution), or API client generation (use api-client)."
---

# Context Window: Token Management & Prompt Optimization Skill

Manage context windows, count tokens, optimize prompts, cache context, and process long documents — using Claude's token counting API, prompt caching, and extended thinking across TypeScript, Python, or cURL.

## Defaults

- Use `claude-sonnet-4-6` for standard tasks (200K context window)
- Use `claude-opus-4-6` for complex reasoning requiring extended thinking
- Use `claude-mythos-preview` for frontier coding and vulnerability analysis (partner-only)
- Always count tokens before sending large payloads
- Enable prompt caching for repeated system prompts and tool definitions
- Default chunking: 100K tokens per chunk with 5K overlap

---

## Capability Selection

Before reading setup docs, determine which capability the user needs:

1. **Token Counting** — estimate and count tokens before sending
   - Best for: cost estimation, context budget management
   - Read from `shared/token-counting.md`

2. **Prompt Caching** — cache system prompts and tool definitions
   - Best for: repeated conversations, multi-turn with same context
   - Read from `shared/prompt-caching.md`

3. **Long Document Processing** — chunk and process large documents
   - Best for: books, codebases, legal documents, research papers
   - Read from `shared/long-documents.md`

4. **Extended Thinking** — budget and manage thinking tokens
   - Best for: complex reasoning, math, coding, analysis
   - Read from `shared/extended-thinking.md`

---

## Context Window Sizes

| Model | Context Window | Max Output | Availability |
|-------|---------------|------------|--------------|
| `claude-mythos-preview` | 200K tokens | 32K tokens | Partner-only |
| `claude-opus-4-6` | 200K tokens | 32K tokens | GA |
| `claude-sonnet-4-6` | 200K tokens | 16K tokens | GA |
| `claude-haiku-4-5-20251001` | 200K tokens | 8K tokens | GA |

---

## Token Budget Planning

```
Total Context Window (200K)
├── System Prompt          (1-5K typical)
├── Tool Definitions       (2-10K typical)
├── Conversation History   (variable)
├── Current User Message   (variable)
├── Extended Thinking       (configurable budget)
└── Output Reserve         (8-32K depending on model)
```

### Budget Formula

```
available_input = context_window - max_output - thinking_budget
usable_for_content = available_input - system_prompt - tool_definitions
```

---

## Workflow

### Long Document Processing

```
Large Document
      │
      ▼
┌──────────────────┐
│ Count Tokens      │ ← /v1/messages/count_tokens
│                   │
└────────┬─────────┘
         │
    ┌────┴────┐
    │ Fits?   │
    └────┬────┘
    Yes  │  No
    │    │
    │    ▼
    │  ┌──────────────────┐
    │  │ Chunk Document    │ ← Semantic boundaries
    │  │                   │
    │  └────────┬─────────┘
    │           │
    │           ▼
    │  ┌──────────────────┐
    │  │ Process Chunks    │ ← Map-reduce or sequential
    │  │                   │
    │  └────────┬─────────┘
    │           │
    ▼           ▼
┌──────────────────┐
│ Final Response    │
│                   │
└──────────────────┘
```

### Prompt Caching Flow

```
First Request
      │
      ▼
┌──────────────────┐
│ Send with         │ ← cache_control: {"type": "ephemeral"}
│ Cache Markers     │
└────────┬─────────┘
         │
         ▼
Subsequent Requests
      │
      ▼
┌──────────────────┐
│ Cache Hit         │ ← 90% cost reduction, ~85ms latency
│                   │
└──────────────────┘
```

---

## Best Practices

### Token Optimization

1. **Count before sending** — use the token counting endpoint
2. **Trim conversation history** — remove old messages when approaching limits
3. **Summarize periodically** — replace old context with summaries
4. **Cache static content** — system prompts, tool definitions, reference docs

### Chunking Strategy

1. **Semantic boundaries** — split at paragraphs, sections, or functions
2. **Overlap chunks** — 5-10% overlap prevents missing cross-boundary context
3. **Prioritize relevance** — process most relevant chunks first
4. **Map-reduce** — process chunks independently, then combine results

### Extended Thinking

1. **Set budget explicitly** — `thinking: {"type": "enabled", "budget_tokens": 10000}`
2. **Match budget to complexity** — simple tasks need less thinking
3. **Monitor thinking tokens** — check `usage.thinking_tokens` in response
4. **Don't over-allocate** — excess thinking budget wastes tokens
