---
source: file://claude-api.md
domain: local
crawled_at: 2026-03-31T21:40:37Z
index_hash: 401a979429b9
page_count: 1
---

# claude-api

## Pages

### claude-api

URL: https://local.taxonomy/claude-api/claude-api
Hash: 401a979429b9

```
~/agenttasks
❯ claude --dangerously-skip-permissions [Loading...]
▐▛███▜▌ Claude Code v2.1.88
▝▜█████▛▘ Opus 4.6 · Claude Max
▘▘ ▝▝ ~/agenttasks

❯ source /Users/alexzh/agenttasks/agenttasks/.venv/bin/activate

⏺ Bash(source /Users/alexzh/agenttasks/agenttasks/.venv/bin/activate && echo "Activated:  
 $VIRTUAL_ENV")  
 ⎿ Activated: /Users/alexzh/agenttasks/agenttasks/.venv

⏺ The virtual environment is activated at /Users/alexzh/agenttasks/agenttasks/.venv. Note that  
 shell state (like activated venvs) doesn't persist between Bash tool calls — if you need me to
run commands within this venv, I'll prefix them with the activation command each time.

❯ /claude-api

⏺ The Claude API skill is loaded. Based on your project setup, you're working in Python with uv.

What would you like to build or do with the Claude API? For example:

- Basic API calls (messages, streaming, thinking)
- Tool use / agentic loops
- Agent SDK usage
- Structured outputs
- Batch processing
- Something else?  


❯ can you show me the taxonomy for claude-api skill

⏺ Here's the taxonomy of the /claude-api skill documentation:

By Language

┌────────────┬────────────────────────┬───────────────────────┬─────────────┐  
 │ Language │ Claude API │ Agent SDK │ Tool Runner │  
 ├────────────┼────────────────────────┼───────────────────────┼─────────────┤  
 │ Python │ python/claude-api/ │ python/agent-sdk/ │ Yes (beta) │  
 ├────────────┼────────────────────────┼───────────────────────┼─────────────┤  
 │ TypeScript │ typescript/claude-api/ │ typescript/agent-sdk/ │ Yes (beta) │  
 ├────────────┼────────────────────────┼───────────────────────┼─────────────┤  
 │ Java │ java/claude-api.md │ No │ Yes (beta) │  
 ├────────────┼────────────────────────┼───────────────────────┼─────────────┤  
 │ Go │ go/claude-api.md │ No │ Yes (beta) │  
 ├────────────┼────────────────────────┼───────────────────────┼─────────────┤  
 │ Ruby │ ruby/claude-api.md │ No │ Yes (beta) │  
 ├────────────┼────────────────────────┼───────────────────────┼─────────────┤  
 │ C# │ csharp/claude-api.md │ No │ No │  
 ├────────────┼────────────────────────┼───────────────────────┼─────────────┤  
 │ PHP │ php/claude-api.md │ No │ Yes (beta) │  
 ├────────────┼────────────────────────┼───────────────────────┼─────────────┤  
 │ cURL │ curl/examples.md │ N/A │ N/A │  
 └────────────┴────────────────────────┴───────────────────────┴─────────────┘

By Topic (shared across languages)

┌─────────────────────────────┬───────────────────────────────────────────────────────────────┐  
 │ File │ Covers │
├─────────────────────────────┼───────────────────────────────────────────────────────────────┤  
 │ shared/tool-use-concepts.md │ Tool definitions, tool choice, agentic loops, server-side │
│ │ tools (code exec, web search, memory), structured outputs │  
 ├─────────────────────────────┼───────────────────────────────────────────────────────────────┤  
 │ shared/prompt-caching.md │ Cache placement, silent invalidators, optimization workflow │
├─────────────────────────────┼───────────────────────────────────────────────────────────────┤  
 │ shared/error-codes.md │ HTTP errors, typed exceptions, common mistakes │
├─────────────────────────────┼───────────────────────────────────────────────────────────────┤  
 │ shared/models.md │ Model catalog, IDs, capabilities, Models API discovery │
├─────────────────────────────┼───────────────────────────────────────────────────────────────┤  
 │ shared/live-sources.md │ WebFetch URLs for latest docs │
└─────────────────────────────┴───────────────────────────────────────────────────────────────┘

Python-Specific Breakdown

┌────────────────────────────────┬────────────────────────────────────────────────────────────┐  
 │ File │ Covers │
├────────────────────────────────┼────────────────────────────────────────────────────────────┤  
 │ python/claude-api/README.md │ Basic requests, system prompts, vision, caching, thinking, │
│ │ multi-turn, compaction, errors │  
 ├────────────────────────────────┼────────────────────────────────────────────────────────────┤  
 │ python/claude-api/streaming.md │ Stream events, async streaming, progress tracking │
├────────────────────────────────┼────────────────────────────────────────────────────────────┤  
 │ python/claude-api/tool-use.md │ @beta_tool runner, MCP helpers, manual loop, code │
│ │ execution, memory tool, structured outputs │  
 ├────────────────────────────────┼────────────────────────────────────────────────────────────┤
│ python/claude-api/batches.md │ Batch API (async 50% discount) │  
 ├────────────────────────────────┼────────────────────────────────────────────────────────────┤  
 │ python/claude-api/files-api.md │ File upload/download/reference │
├────────────────────────────────┼────────────────────────────────────────────────────────────┤  
 │ python/agent-sdk/README.md │ query(), ClaudeSDKClient, built-in tools, hooks, MCP, │
│ │ subagents │  
 ├────────────────────────────────┼────────────────────────────────────────────────────────────┤
│ python/agent-sdk/patterns.md │ Custom tools, hooks, session resumption, permissions │  
 └────────────────────────────────┴────────────────────────────────────────────────────────────┘

❯ /batch show me the entire taxonomy but i want to recursively see it across all  
channels/devices/platforms/surfaces/languages

⏺ Here's the complete recursive taxonomy of the /claude-api skill:

Top Level

claude-api/  
 ├── shared/ # Language-agnostic concepts  
 │ ├── tool-use-concepts.md  
 │ ├── prompt-caching.md  
 │ ├── error-codes.md  
 │ ├── models.md  
 │ └── live-sources.md  
 │  
 ├── python/  
 │ ├── claude-api/  
 │ │ ├── README.md  
 │ │ ├── streaming.md  
 │ │ ├── tool-use.md  
 │ │ ├── batches.md  
 │ │ └── files-api.md  
 │ └── agent-sdk/  
 │ ├── README.md  
 │ └── patterns.md  
 │  
 ├── typescript/  
 │ ├── claude-api/  
 │ │ ├── README.md  
 │ │ ├── streaming.md  
 │ │ ├── tool-use.md  
 │ │ ├── batches.md  
 │ │ └── files-api.md  
 │ └── agent-sdk/  
 │ ├── README.md  
 │ └── patterns.md  
 │  
 ├── java/  
 │ └── claude-api.md # single file (no agent-sdk)  
 │  
 ├── go/  
 │ └── claude-api.md # single file (no agent-sdk)  
 │  
 ├── ruby/  
 │ └── claude-api.md # single file (no agent-sdk)  
 │  
 ├── csharp/  
 │ └── claude-api.md # single file (no agent-sdk)  
 │  
 ├── php/  
 │ └── claude-api.md # single file (no agent-sdk)  
 │  
 └── curl/  
 └── examples.md # raw HTTP (no SDK)

Recursive Topic Breakdown

shared/models.md

Models  
 ├── Current Models  
 │ ├── Claude Opus 4.6 (claude-opus-4-6) — 200K/1M beta, 128K out  
 │ ├── Claude Sonnet 4.6 (claude-sonnet-4-6) — 200K/1M beta, 64K out  
 │ └── Claude Haiku 4.5 (claude-haiku-4-5) — 200K, 64K out  
 ├── Legacy Models (active)  
 │ ├── Opus 4.5, 4.1, 4.0  
 │ ├── Sonnet 4.5, 4.0  
 │ └── (aliases documented)  
 ├── Deprecated / Retired Models  
 ├── Programmatic Model Discovery (Models API)  
 │ ├── client.models.retrieve(id)  
 │ ├── client.models.list()  
 │ └── capabilities dict (thinking, effort, vision, structured_outputs, context_management)  
 └── User Request Resolution Table

shared/tool-use-concepts.md

Tool Use Concepts  
 ├── User-Defined Tools  
 │ ├── Tool Definition Structure (JSON Schema)  
 │ ├── Tool Choice Options (auto, any, tool, none, disable_parallel)  
 │ ├── Tool Runner vs Manual Loop  
 │ │ ├── Tool Runner (recommended, auto loop)  
 │ │ └── Manual Agentic Loop (fine-grained control)  
 │ ├── Handling Tool Results  
 │ │ ├── Single tool result  
 │ │ ├── Multiple tool calls  
 │ │ └── Error handling (is_error: true)  
 │ └── Stop Reasons (end_turn, tool_use, pause_turn)  
 │  
 ├── Server-Side Tools  
 │ ├── Code Execution (code_execution_20260120)  
 │ │ ├── Sandbox specs (1 CPU, 5 GiB RAM, no internet)  
 │ │ ├── Pre-installed libraries  
 │ │ ├── File upload / download  
 │ │ ├── Container reuse  
 │ │ └── Response structure (bash_code_execution_tool_result,  
 text_editor_code_execution_tool_result)  
 │ ├── Web Search (web_search_20260209)  
 │ │ └── Dynamic filtering (Opus 4.6 / Sonnet 4.6)  
 │ ├── Web Fetch (web_fetch_20260209)  
 │ ├── Bash (bash_20250124)  
 │ ├── Text Editor (text_editor_20250728)  
 │ ├── Memory (memory_20250818)  
 │ │ ├── Commands: view, create, str_replace, insert, delete, rename  
 │ │ └── SDK helpers (Python, TypeScript, Java)  
 │ ├── Programmatic Tool Calling (WebFetch ref)  
 │ └── Tool Search (WebFetch ref)  
 │  
 ├── Computer Use (WebFetch ref)  
 │ ├── Anthropic-hosted (server-side)  
 │ └── Self-hosted (client-side)  
 │  
 ├── Structured Outputs  
 │ ├── JSON outputs (output_config.format)  
 │ ├── Strict tool use (strict: true)  
 │ ├── JSON Schema limitations  
 │ └── Compatibility notes  
 │  
 └── Tool Use Examples (WebFetch ref)

shared/prompt-caching.md

Prompt Caching  
 ├── Core Invariant (prefix match, byte-level)  
 ├── Render Order: tools → system → messages  
 ├── Optimization Workflow  
 │ ├── 1. Trace prompt assembly path  
 │ ├── 2. Classify inputs by stability  
 │ ├── 3. Check rendered order  
 │ ├── 4. Place breakpoints  
 │ └── 5. Audit silent invalidators  
 ├── Placement Patterns  
 │ ├── Large shared system prompt  
 │ ├── Multi-turn conversations  
 │ ├── Shared prefix, varying suffix  
 │ └── Prompts that change every time (don't cache)  
 ├── Architectural Guidance  
 │ ├── Freeze system prompt  
 │ ├── Don't change tools/model mid-conversation  
 │ └── Fork operations reuse parent prefix  
 ├── Silent Invalidators Table  
 │ ├── datetime.now() / Date.now()  
 │ ├── uuid4() / randomUUID()  
 │ ├── Non-deterministic JSON serialization  
 │ ├── Session/user ID interpolation  
 │ ├── Conditional system sections  
 │ └── Per-user tool sets  
 ├── API Reference  
 │ ├── cache_control: {type: "ephemeral"}  
 │ ├── TTL options (5m default, 1h)  
 │ ├── Max 4 breakpoints  
 │ └── Top-level cache_control shortcut  
 └── Verifying Cache Hits  
 ├── cache_creation_input_tokens  
 ├── cache_read_input_tokens  
 └── input_tokens

shared/error-codes.md

Error Codes  
 ├── 400 Bad Request (invalid_request_error)  
 ├── 401 Unauthorized (authentication_error)  
 ├── 403 Forbidden (permission_error)  
 ├── 404 Not Found (not_found_error)  
 ├── 413 Request Too Large (request_too_large)  
 ├── 429 Rate Limited (rate_limit_error) — retryable  
 ├── 500 Internal Server Error (api_error) — retryable  
 ├── 529 Overloaded (overloaded_error) — retryable  
 ├── Common Mistakes Table  
 └── Typed Exceptions (Python + TypeScript SDK classes)

shared/live-sources.md

Live Sources (WebFetch URLs)  
 ├── Claude API Docs (platform.claude.com)  
 │ ├── Models & Pricing  
 │ ├── Core Features (thinking, adaptive thinking, effort, tool use, streaming, caching)  
 │ ├── Media & Files (vision, PDF)  
 │ ├── API Operations (batches, files, token counting, rate limits, errors)  
 │ ├── Tools (code execution, computer use)  
 │ └── Advanced (structured outputs, compaction, citations, context windows)  
 ├── SDK Repositories (GitHub)  
 │ ├── Python, TypeScript, Java, Go, Ruby, C#, PHP  
 │ └── Agent SDK (Python, TypeScript)  
 └── npm / PyPI package links

---

Per-Language: Python Claude API (python/claude-api/)

README.md

├── Installation (pip install anthropic)  
 ├── Client Initialization (sync, async, explicit key)  
 ├── Basic Message Request  
 ├── System Prompts  
 ├── Vision (base64, URL)  
 ├── Prompt Caching  
 │ ├── Automatic (cache_control top-level)  
 │ ├── Manual (per-block cache_control, TTL)  
 │ └── Verifying hits  
 ├── Extended Thinking  
 │ ├── Adaptive (Opus 4.6 / Sonnet 4.6)  
 │ └── Effort parameter (output_config.effort)  
 ├── Error Handling (typed exceptions)  
 ├── Multi-Turn Conversations  
 │ ├── ConversationManager pattern  
 │ └── Compaction (beta, compact-2026-01-12)  
 ├── Stop Reasons table  
 ├── Cost Optimization  
 │ ├── Prompt caching  
 │ ├── Model selection  
 │ └── Token counting  
 └── Retry with Exponential Backoff

streaming.md

├── Quick Start (sync, async)  
 ├── Handling Different Content Types (thinking + text)  
 ├── Streaming with Tool Use  
 ├── Getting the Final Message  
 ├── Streaming with Progress Updates  
 ├── Error Handling in Streams  
 ├── Stream Event Types table  
 └── Best Practices

tool-use.md

├── Tool Runner (@beta_tool decorator)  
 ├── MCP Tool Conversion Helpers  
 │ ├── async_mcp_tool / mcp_tool  
 │ ├── mcp_message (prompts)  
 │ ├── mcp_resource_to_content  
 │ └── mcp_resource_to_file (upload)  
 ├── Manual Agentic Loop  
 ├── Handling Tool Results (single, multiple, errors)  
 ├── Tool Choice  
 ├── Code Execution  
 │ ├── Basic usage  
 │ ├── File upload for analysis  
 │ ├── Retrieve generated files  
 │ ├── Container reuse  
 │ └── Response structure  
 ├── Memory Tool  
 │ ├── Basic usage  
 │ └── SDK helper (BetaAbstractMemoryTool)  
 └── Structured Outputs  
 ├── JSON Outputs (Pydantic — messages.parse())  
 ├── Raw Schema (output_config.format)  
 ├── Strict Tool Use (strict: true)  
 └── Using Both Together

batches.md

├── Key Facts (100K requests, 256MB, 24h max, 50% discount)  
 ├── Create a Batch  
 ├── Poll for Completion  
 ├── Retrieve Results (succeeded, errored, canceled, expired)  
 ├── Cancel a Batch  
 ├── Batch with Prompt Caching  
 └── Full End-to-End Example

files-api.md

├── Key Facts (500MB max, 100GB org, beta header)  
 ├── Upload a File  
 ├── Use in Messages (PDF/text, image)
├── Manage Files (list, metadata, delete, download)  
 └── Full End-to-End Example

---

Per-Language: Python Agent SDK (python/agent-sdk/)

README.md

├── Installation (pip install claude-agent-sdk)  
 ├── Quick Start (query())  
 ├── Built-in Tools table  
 ├── Primary Interfaces  
 │ ├── query() — simple one-shot  
 │ └── ClaudeSDKClient — full control (context manager, interrupt, custom tools)  
 ├── Permission System (default, plan, acceptEdits, bypassPermissions)  
 ├── MCP Support  
 ├── Hooks  
 │ ├── Callback functions  
 │ ├── HookMatcher  
 │ └── Events: PreToolUse, PostToolUse, PostToolUseFailure, UserPromptSubmit, Stop,  
 SubagentStop, PreCompact, Notification, SubagentStart, PermissionRequest  
 ├── Common Options table  
 ├── Message Types  
 │ ├── ResultMessage  
 │ ├── SystemMessage  
 │ ├── AssistantMessage (with usage)  
 │ ├── TaskStartedMessage, TaskProgressMessage, TaskNotificationMessage  
 │ └── RateLimitEvent  
 ├── Subagents (AgentDefinition)  
 ├── Error Handling (CLINotFoundError, CLIConnectionError)  
 ├── Session History (list_sessions, get_session_messages)  
 ├── Session Mutations (rename_session, tag_session)  
 ├── MCP Server Management (reconnect, toggle, status)  
 └── Best Practices

patterns.md

├── Basic Agent  
 ├── Custom Tools (SDK MCP server, @tool decorator, create_sdk_mcp_server)  
 ├── Hooks (PostToolUse audit logging)  
 ├── Subagents  
 ├── MCP Server Integration  
 │ ├── Playwright (browser)  
 │ └── PostgreSQL (database)  
 ├── Permission Modes (all 4)  
 ├── Error Recovery  
 ├── Session Resumption  
 ├── Session History  
 ├── Session Mutations  
 └── Custom System Prompt

---

Per-Language: TypeScript (mirrors Python structure)

typescript/claude-api/README.md — same topics as Python

typescript/claude-api/streaming.md — same topics as Python

typescript/claude-api/tool-use.md

(same as Python, plus:)  
 ├── betaZodTool (Zod schemas instead of @beta_tool)  
 ├── Streaming Manual Loop (stream() + finalMessage())  
 └── Server-Side Tools type/name table  
 typescript/claude-api/batches.md — same as Python

typescript/claude-api/files-api.md — same as Python

typescript/agent-sdk/README.md — same as Python (+ dontAsk mode, forkSession)

typescript/agent-sdk/patterns.md — same as Python

---

Single-File Languages

Each covers a subset of the Python/TS topics in one file:

java/claude-api.md

├── Installation (Maven, Gradle)  
 ├── Client Init  
 ├── Basic Request  
 ├── Streaming  
 ├── Thinking (adaptive)  
 ├── Tool Use (Beta)  
 │ ├── BetaToolRunner (@JsonClassDescription, Supplier<String>)  
 │ ├── Memory Tool (BetaMemoryToolHandler)  
 │ ├── Non-Beta Tool Declaration (manual JSON)  
 │ └── MessageParam round-trip (.contentOfBlockParams)  
 ├── Effort Parameter  
 ├── Prompt Caching  
 ├── Token Counting  
 ├── Structured Output (StructuredMessageCreateParams<T>)  
 ├── PDF / Document Input  
 ├── Server-Side Tools (GA + beta namespace)  
 └── Files API (Beta)

go/claude-api.md

├── Installation  
 ├── Client Init  
 ├── Basic Request  
 ├── Streaming (+ Accumulate pattern)  
 ├── Tool Use  
 │ ├── BetaToolRunner (jsonschema struct tags)  
 │ └── Manual Loop (ToParam, AsAny, NewToolResultBlock)  
 ├── Thinking (adaptive)  
 ├── Prompt Caching  
 ├── Server-Side Tools  
 ├── PDF / Document Input  
 ├── Files API (Beta)  
 └── Context Editing / Compaction (Beta)

ruby/claude-api.md

├── Installation  
 ├── Client Init  
 ├── Basic Request  
 ├── Streaming  
 ├── Tool Use (BaseTool + tool_runner beta)  
 └── Prompt Caching

csharp/claude-api.md

├── Installation  
 ├── Client Init  
 ├── Basic Request  
 ├── Streaming (TryPick\* pattern)  
 ├── Thinking (adaptive)  
 ├── Tool Use (manual, no runner)  
 │ └── Response round-trip (no .ToParam())  
 ├── Context Editing / Compaction (Beta namespace)  
 ├── Effort Parameter  
 ├── Prompt Caching  
 ├── Token Counting  
 ├── Structured Output  
 ├── PDF / Document Input  
 ├── Server-Side Tools  
 └── Files API (Beta)

php/claude-api.md

├── Installation  
 ├── Client Init (API key, Bedrock, Vertex, Foundry)  
 ├── Basic Request  
 ├── Streaming  
 ├── Tool Use  
 │ ├── BetaRunnableTool (runner)  
 │ └── Manual Loop (camelCase keys)  
 ├── Extended Thinking (adaptive)  
 ├── Prompt Caching  
 ├── Structured Outputs (StructuredOutputModel, raw schema)  
 └── Beta Features & Server-Side Tools

curl/examples.md

├── Setup  
 ├── Basic Request + jq parsing  
 ├── Streaming (SSE)  
 ├── Tool Use (request + result round-trip)  
 ├── Prompt Caching  
 ├── Extended Thinking (adaptive)  
 └── Required Headers table

---

Feature Coverage Matrix

┌────────────────────┬─────┬─────┬──────┬─────┬──────┬─────┬─────┬──────┐
│ Feature │ PY │ TS │ Java │ Go │ Ruby │ C# │ PHP │ cURL │  
 ├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Basic messages │ x │ x │ x │ x │ x │ x │ x │ x │  
 ├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Streaming │ x │ x │ x │ x │ x │ x │ x │ x │  
 ├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Adaptive thinking │ x │ x │ x │ x │ - │ x │ x │ x │  
 ├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Tool runner (beta) │ x │ x │ x │ x │ x │ - │ x │ - │
├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Manual tool loop │ x │ x │ x │ x │ x │ x │ x │ x │
├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Code execution │ x │ x │ x │ - │ - │ - │ - │ - │
├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Memory tool │ x │ x │ x │ - │ - │ - │ - │ - │
├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Structured outputs │ x │ x │ x │ - │ - │ x │ x │ - │
├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Prompt caching │ x │ x │ x │ x │ x │ x │ x │ x │
├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Batches │ x │ x │ - │ - │ - │ - │ - │ - │
├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Files API │ x │ x │ x │ x │ - │ x │ - │ - │
├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Compaction │ x │ x │ - │ x │ - │ x │ - │ - │
├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Agent SDK │ x │ x │ - │ - │ - │ - │ - │ - │
├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ MCP helpers │ x │ x │ - │ - │ - │ - │ - │ - │
├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ Vision │ x │ x │ - │ - │ - │ - │ - │ - │
├────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤  
 │ PDF input │ - │ - │ x │ x │ - │ x │ - │ - │
└────────────────────┴─────┴─────┴──────┴─────┴──────┴─────┴─────┴──────┘

✻ Sautéed for 1m 26s
```
