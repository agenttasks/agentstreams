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

---

# APPENDIX: Live Sources — Recursively Fetched Missing Taxonomy

> The following sections were fetched from `platform.claude.com` live docs on 2026-03-31.
> These topics were previously only referenced as "WebFetch ref" stubs in the skill's
> inlined documentation. They are now fully expanded.

---

## Programmatic Tool Calling (fetched from platform.claude.com)

```
Programmatic Tool Calling
├── Overview
│   ├── What it is: Claude writes code that calls your tools inside code execution
│   ├── Reduces latency for multi-tool workflows
│   ├── Decreases token consumption (intermediate results stay out of context)
│   └── NOT eligible for ZDR
├── Model Compatibility → see Tool Reference
├── Quick Start (examples: Shell, Python, TS, C#, Go, Java, PHP, Ruby)
├── How It Works
│   ├── 1. Claude writes Python code invoking tools as async functions
│   ├── 2. Code runs in sandboxed container via code execution
│   ├── 3. Tool function call → code execution pauses → API returns tool_use block
│   ├── 4. You provide tool result → code execution continues
│   └── 5. Final output returned to Claude for reasoning
│
├── Core Concepts
│   ├── allowed_callers field
│   │   ├── ["direct"] — only Claude directly (default)
│   │   ├── ["code_execution_20260120"] — only from code execution
│   │   └── ["direct", "code_execution_20260120"] — both
│   ├── caller field in responses
│   │   ├── { type: "direct" } — traditional tool use
│   │   └── { type: "code_execution_20260120", tool_id: "srvtoolu_..." }
│   └── Container Lifecycle
│       ├── 30-day max lifetime
│       ├── 4.5 min idle timeout
│       ├── Container ID returned in responses
│       └── Reuse via container param
│
├── Example Workflow (5 steps)
│   ├── Step 1: Initial request (code_execution + tool with allowed_callers)
│   ├── Step 2: API response with tool_use + caller field
│   ├── Step 3: Provide tool result (container reuse)
│   ├── Step 4: Next tool call or completion
│   └── Step 5: Final response (code_execution_tool_result)
│
├── Advanced Patterns
│   ├── Batch Processing with Loops (N regions → 1 round-trip)
│   ├── Early Termination (break on success)
│   ├── Conditional Tool Selection (if/else based on intermediate results)
│   └── Data Filtering (aggregate before returning to context)
│
├── Response Format
│   ├── Programmatic tool call JSON (tool_use with caller)
│   ├── Tool result handling
│   └── Code execution completion (code_execution_tool_result)
│
├── Error Handling
│   ├── invalid_tool_input
│   ├── tool_not_allowed
│   ├── missing_beta_header (Bedrock/Vertex only)
│   ├── Container expiration → TimeoutError in stderr
│   └── Tool execution errors (returned as error string)
│
├── Constraints & Limitations
│   ├── Feature Incompatibilities
│   │   ├── strict: true NOT supported
│   │   ├── tool_choice cannot force programmatic calling
│   │   └── disable_parallel_tool_use NOT supported
│   ├── Tool Restrictions: MCP connector tools NOT callable programmatically
│   └── Message Formatting
│       └── Tool result responses must contain ONLY tool_result blocks
│
├── Token Efficiency
│   ├── Tool results from programmatic calls NOT added to context
│   ├── Intermediate processing in code
│   └── ~10x token reduction vs direct calls
│
├── Usage & Pricing → same as code execution
│
├── Best Practices
│   ├── Tool Design: detailed output descriptions, return JSON, keep concise
│   ├── When to Use: large datasets, 3+ dependent calls, filtering needed
│   ├── When NOT: single calls, needs immediate user feedback
│   └── Performance: reuse containers, batch similar operations
│
└── Alternative Implementations
    ├── Client-Side Direct Execution (simple, no sandbox)
    ├── Self-Managed Sandboxed Execution (secure, complex)
    └── Anthropic-Managed Execution (recommended)
```

---

## Tool Search Tool (fetched from platform.claude.com)

```
Tool Search Tool
├── Overview
│   ├── Dynamic discovery from 100s-1000s of tools
│   ├── Solves context bloat (~85% reduction in tool definition tokens)
│   ├── Solves tool selection accuracy degradation (>30-50 tools)
│   └── ZDR eligible (with limited technical retention)
│
├── How It Works
│   ├── 1. Include tool_search tool + tools with defer_loading: true
│   ├── 2. Claude sees only search tool + non-deferred tools
│   ├── 3. Claude searches → API returns 3-5 tool_reference blocks
│   ├── 4. References auto-expanded to full definitions
│   └── 5. Claude selects and invokes discovered tools
│
├── Two Variants
│   ├── Regex (tool_search_tool_regex_20251119)
│   │   ├── Python re.search() syntax
│   │   ├── Max 200 char pattern
│   │   └── Case-sensitive by default (use (?i) for insensitive)
│   └── BM25 (tool_search_tool_bm25_20251119)
│       └── Natural language queries
│
├── Quick Start (examples: Shell, Python, TS, C#, Go, Java, PHP, Ruby)
│
├── Deferred Tool Loading
│   ├── defer_loading: true on tool definitions
│   ├── Tools without it → loaded immediately
│   ├── Search tool itself NEVER deferred
│   ├── Keep 3-5 most frequent tools non-deferred
│   └── Internals: deferred tools excluded from system-prompt prefix
│       └── Preserves prompt caching
│
├── Response Format
│   ├── server_tool_use (Claude invoking search)
│   ├── tool_search_tool_result
│   │   └── tool_search_tool_search_result
│   │       └── tool_references[] (array of tool_reference objects)
│   └── tool_use (Claude invoking discovered tool)
│
├── Custom Tool Search Implementation
│   ├── Return tool_reference blocks from your own search
│   ├── Use standard tool_result format
│   └── Referenced tools must have defer_loading: true definitions
│
├── MCP Integration → see MCP connector docs
│
├── Error Handling
│   ├── HTTP 400 Errors
│   │   ├── All tools deferred
│   │   └── Missing tool definition for reference
│   └── Tool Result Errors (200 with error body)
│       ├── too_many_requests
│       ├── invalid_pattern
│       ├── pattern_too_long
│       └── unavailable
│
├── Streaming (SSE events for search)
├── Batch Requests (supported in Batches API)
│
├── Limits
│   ├── Max 10,000 tools in catalog
│   ├── 3-5 results per search
│   ├── 200 char max pattern (regex)
│   └── Model support: Sonnet 4.0+, Opus 4.0+ (no Haiku)
│
├── When to Use
│   ├── Good: 10+ tools, >10k tokens in definitions, MCP multi-server
│   └── Not ideal: <10 tools, all frequently used, tiny definitions
│
└── Usage Tracking
    └── usage.server_tool_use.tool_search_requests
```

---

## Citations (fetched from platform.claude.com)

```
Citations
├── Overview
│   ├── Detailed source citations from documents
│   ├── ZDR eligible
│   ├── Supported on all active models except Haiku 3
│   └── Advantages over prompt-based approaches
│       ├── Cost savings (cited_text doesn't count as output tokens)
│       ├── Better reliability (guaranteed valid pointers)
│       └── Improved quality (more relevant quotes)
│
├── How Citations Work (3 steps)
│   ├── 1. Provide documents + enable citations (citations.enabled=true)
│   ├── 2. Documents get processed (chunked)
│   │   ├── PDFs → text extracted, chunked into sentences
│   │   ├── Plain text → chunked into sentences
│   │   └── Custom content → your blocks used as-is
│   └── 3. Claude provides cited response
│       ├── Multiple text blocks with citation lists
│       └── Citation format depends on document type
│
├── Citable vs Non-Citable Content
│   ├── source content → citable
│   ├── title → NOT citable (passed to model, not cited)
│   └── context → NOT citable (metadata field)
│
├── Citation Indices
│   ├── Document indices: 0-indexed across all documents
│   ├── Character indices: 0-indexed, exclusive end
│   ├── Page numbers: 1-indexed, exclusive end
│   └── Content block indices: 0-indexed, exclusive end
│
├── Token Costs
│   ├── Slight increase in input tokens (system prompt + chunking)
│   ├── cited_text does NOT count as output tokens
│   └── cited_text does NOT count as input tokens on round-trip
│
├── Feature Compatibility
│   ├── Works with: prompt caching, token counting, batches
│   └── INCOMPATIBLE with: Structured Outputs (returns 400)
│
├── Document Types
│   ├── Plain Text
│   │   ├── Auto-chunked into sentences
│   │   ├── Source: inline text or file_id
│   │   └── Citation format: char_location (0-indexed)
│   ├── PDF
│   │   ├── Text extracted + sentence chunking
│   │   ├── Source: base64 or file_id
│   │   ├── Citation format: page_location (1-indexed)
│   │   └── Image citations NOT supported
│   └── Custom Content
│       ├── No additional chunking (you control granularity)
│       ├── Source: content[] array of text blocks
│       └── Citation format: content_block_location (0-indexed)
│
├── Response Structure
│   ├── Multiple text blocks per response
│   ├── Each block may have citations[] array
│   └── Citation types: char_location, page_location, content_block_location
│
├── Streaming Support
│   └── citations_delta event type (single citation added to current block)
│
└── Using with Prompt Caching
    └── cache_control on document blocks (not citation blocks)
```

---

## Context Windows (fetched from platform.claude.com)

```
Context Windows
├── Understanding the Context Window
│   ├── "Working memory" for the model (not training data)
│   ├── Context rot: accuracy degrades as token count grows
│   ├── Progressive token accumulation across turns
│   ├── Linear growth pattern
│   └── Input-output flow per turn
│
├── Context Window Sizes
│   ├── Opus 4.6 / Sonnet 4.6: 1M tokens (beta via context-1m-2025-08-07)
│   ├── Other Claude models: 200K tokens
│   └── Max 600 images/PDF pages (100 for 200K models)
│
├── Context Window with Extended Thinking
│   ├── Thinking tokens count toward context window
│   ├── Thinking tokens are OUTPUT tokens (billed once)
│   ├── Previous thinking blocks auto-stripped from subsequent turns
│   ├── API handles stripping automatically
│   └── Formula: context_window = (input - previous_thinking) + current_turn
│
├── Context Window with Extended Thinking + Tool Use
│   ├── Turn 1: tools config + user msg → thinking + text + tool_use
│   ├── Turn 2: MUST return thinking block with tool_result
│   │   └── No new thinking until next user message
│   ├── Turn 3: thinking block can be dropped (API auto-strips)
│   │   └── New user turn → new thinking block generated
│   └── Cryptographic signatures verify thinking block authenticity
│
├── Context Awareness (Sonnet 4.6, Sonnet 4.5, Haiku 4.5)
│   ├── Models track remaining token budget
│   ├── Initial: <budget:token_budget>1000000</budget:token_budget>
│   ├── After tool calls: <system_warning>Token usage: N/M; R remaining</system_warning>
│   ├── Benefits: sustained focus, multi-window workflows, token management
│   └── Image tokens included in budgets
│
├── Managing Context
│   ├── Server-Side Compaction (recommended for Opus 4.6 / Sonnet 4.6)
│   └── Context Editing
│       ├── Tool result clearing
│       └── Thinking block clearing
│
└── Validation Behavior
    ├── Newer models return validation error (not silent truncation)
    └── Use token counting API to estimate before sending
```

---

## Rate Limits (fetched from platform.claude.com)

```
Rate Limits
├── Two Types of Limits
│   ├── Spend Limits (monthly cost ceiling per org)
│   └── Rate Limits (requests/tokens per minute)
│
├── Spend Limits
│   ├── Tier 1: $5 deposit, $100/mo ceiling, $100 max purchase
│   ├── Tier 2: $40 deposit, $500/mo ceiling, $500 max purchase
│   ├── Tier 3: $200 deposit, $1K/mo ceiling, $1K max purchase
│   ├── Tier 4: $400 deposit, $200K/mo ceiling, $200K max purchase
│   └── Monthly Invoicing: no cap, Net-30 terms
│
├── Rate Limits by Tier (RPM / ITPM / OTPM)
│   ├── Tier 1
│   │   ├── Opus 4.x: 50 RPM / 30K ITPM / 8K OTPM
│   │   ├── Sonnet 4.x: 50 RPM / 30K ITPM / 8K OTPM
│   │   └── Haiku 4.5: 50 RPM / 50K ITPM / 10K OTPM
│   ├── Tier 2
│   │   ├── Opus 4.x: 1K RPM / 450K ITPM / 90K OTPM
│   │   ├── Sonnet 4.x: 1K RPM / 450K ITPM / 90K OTPM
│   │   └── Haiku 4.5: 1K RPM / 450K ITPM / 90K OTPM
│   ├── Tier 3
│   │   ├── Opus 4.x: 2K RPM / 800K ITPM / 160K OTPM
│   │   ├── Sonnet 4.x: 2K RPM / 800K ITPM / 160K OTPM
│   │   └── Haiku 4.5: 2K RPM / 1M ITPM / 200K OTPM
│   ├── Tier 4
│   │   ├── Opus 4.x: 4K RPM / 2M ITPM / 400K OTPM
│   │   ├── Sonnet 4.x: 4K RPM / 2M ITPM / 400K OTPM
│   │   └── Haiku 4.5: 4K RPM / 4M ITPM / 800K OTPM
│   └── Custom: contact sales
│
├── Cache-Aware ITPM
│   ├── Only uncached input tokens count toward ITPM (most models)
│   ├── cache_creation_input_tokens → COUNTS
│   ├── cache_read_input_tokens → does NOT count (most models)
│   ├── Older models (†) count cache_read toward ITPM
│   └── Example: 2M ITPM + 80% cache = 10M effective throughput
│
├── OTPM: evaluated in real time (max_tokens does NOT factor in)
│
├── Opus 4.x rate limit = combined Opus 4.6 + 4.5 + 4.1 + 4.0
├── Sonnet 4.x rate limit = combined Sonnet 4.6 + 4.5 + 4.0
│
├── Message Batches API Rate Limits (shared across models)
│   ├── Tier 1: 50 RPM / 100K queue / 100K per batch
│   ├── Tier 2: 1K RPM / 200K queue / 100K per batch
│   ├── Tier 3: 2K RPM / 300K queue / 100K per batch
│   └── Tier 4: 4K RPM / 500K queue / 100K per batch
│
├── Fast Mode Rate Limits (Opus 4.6 speed: "fast")
│   ├── Separate from standard Opus limits
│   └── anthropic-fast-* response headers
│
├── Response Headers
│   ├── retry-after
│   ├── anthropic-ratelimit-requests-{limit,remaining,reset}
│   ├── anthropic-ratelimit-tokens-{limit,remaining,reset}
│   ├── anthropic-ratelimit-input-tokens-{limit,remaining,reset}
│   ├── anthropic-ratelimit-output-tokens-{limit,remaining,reset}
│   └── anthropic-priority-{input,output}-tokens-{limit,remaining,reset}
│
├── Workspace Limits
│   ├── Can set per-workspace limits under org limit
│   ├── Default workspace: cannot set limits
│   └── Unset → matches org limit
│
└── Monitoring → Usage page in Claude Console
```

---

## Memory Tool (fetched from platform.claude.com)

```
Memory Tool (memory_20250818)
├── Overview
│   ├── Client-side tool (you control storage)
│   ├── Claude stores/retrieves info across conversations
│   ├── Just-in-time context retrieval primitive
│   ├── ZDR eligible
│   └── Operates on /memories directory
│
├── Use Cases
│   ├── Maintain project context across sessions
│   ├── Learn from past interactions/decisions/feedback
│   ├── Build knowledge bases over time
│   └── Cross-conversation learning
│
├── How It Works
│   ├── Claude checks /memories before starting tasks
│   ├── Claude calls memory tool → your app executes locally
│   └── Full control over storage backend
│
├── Tool Commands
│   ├── view
│   │   ├── Directories: 2-level listing with sizes
│   │   ├── Files: content with 6-char right-aligned line numbers
│   │   ├── Optional view_range: [start, end] lines
│   │   └── Max 999,999 lines
│   ├── create
│   │   ├── Creates new file at path
│   │   └── Error if file already exists
│   ├── str_replace
│   │   ├── Replace exact text in file
│   │   ├── old_str must appear exactly once
│   │   └── Errors: not found, duplicate matches
│   ├── insert
│   │   ├── Insert text at specific line number
│   │   └── Line range: [0, n_lines]
│   ├── delete
│   │   ├── Delete file or directory
│   │   └── Directories: recursive delete
│   └── rename
│       ├── Move/rename file or directory
│       └── Error if destination exists (no overwrite)
│
├── Prompting Guidance
│   ├── Auto-injected: "ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE"
│   ├── Memory protocol: view → work → record progress
│   └── Customizable instructions for content/organization
│
├── Security Considerations
│   ├── Sensitive information (Claude usually refuses, add validation)
│   ├── File storage size limits
│   ├── Memory expiration (periodic cleanup)
│   └── Path traversal protection (CRITICAL)
│       ├── Validate all paths start with /memories
│       ├── Resolve canonical paths
│       ├── Reject ../ and encoded variants
│       └── Use language path security utilities
│
├── SDK Helpers
│   ├── Python: BetaAbstractMemoryTool (subclass)
│   ├── TypeScript: betaMemoryTool (with MemoryToolHandlers)
│   └── Java: BetaMemoryToolHandler
│
├── Integration
│   ├── Context Editing (manage long conversations alongside memory)
│   └── Compaction (server-side summarization + memory persistence)
│
└── Multi-Session Software Development Pattern
    ├── Initializer Session
    │   ├── Progress log (done/next)
    │   ├── Feature checklist (scope)
    │   └── Reference to startup scripts
    ├── Subsequent Sessions
    │   └── Read memory → recover state in seconds
    └── End-of-Session Update
        └── Update progress log before session ends
```

---

## Compaction (fetched from platform.claude.com)

```
Compaction (Beta: compact-2026-01-12)
├── Overview
│   ├── Server-side context summarization
│   ├── Extends effective context length for long conversations
│   ├── ZDR eligible
│   ├── Supported: Opus 4.6, Sonnet 4.6
│   └── Ideal for: multi-turn chat, agentic tool-use workflows
│
├── How It Works
│   ├── 1. Detects input tokens exceed trigger threshold
│   ├── 2. Generates conversation summary
│   ├── 3. Creates compaction block with summary
│   ├── 4. On next request, drops all blocks before compaction block
│   └── Conversation continues from summary
│
├── Basic Usage
│   └── context_management.edits: [{type: "compact_20260112"}]
│
├── Parameters
│   ├── Trigger Configuration
│   │   ├── trigger_tokens: when to trigger (default: context_window * 0.75)
│   │   └── Minimum: 1000 tokens
│   ├── Custom Summarization Instructions
│   │   └── context_management.edits[].instructions: "Focus on..."
│   └── Pausing After Compaction
│       ├── stop_on_context_edit: true → returns immediately after compaction
│       ├── stop_reason: "pause_turn"
│       └── Enforcing Total Token Budget
│           └── Set trigger_tokens to budget; use stop_on_context_edit
│
├── Working with Compaction Blocks
│   ├── Passing Back
│   │   ├── MUST append response.content (not just text)
│   │   ├── Compaction blocks must be preserved
│   │   └── API auto-drops messages before compaction block
│   ├── Streaming
│   │   └── compaction content_block_start event type
│   └── Prompt Caching
│       ├── Compaction invalidates cache (prefix changes)
│       └── Maximize cache hits: use system prompt with cache_control
│
├── Understanding Usage
│   ├── context_management.applied_edits[]
│   │   ├── type: "compact_20260112"
│   │   └── cleared_input_tokens: N
│   └── Null if no compaction triggered
│
├── Combining with Other Features
│   ├── Server Tools (code execution, web search)
│   │   └── Tool results are included in compaction summaries
│   └── Token Counting
│       └── Use beta.messages.count_tokens with same beta header
│
├── Examples (Python, TypeScript, Shell)
│
├── Current Limitations
│   ├── Prompt caching invalidated on compaction
│   ├── No user control over what gets summarized
│   ├── Compaction quality depends on conversation structure
│   └── Beta — behavior may change
│
└── Next Steps → Context Editing, Memory Tool
```

---

## Structured Outputs (fetched from platform.claude.com)

```
Structured Outputs
├── Overview
│   ├── Constrain responses to specific JSON schema
│   ├── Two features: JSON outputs + Strict tool use
│   ├── GA on API + Bedrock; Beta on Foundry
│   ├── Supported: Opus 4.6, Sonnet 4.6, Sonnet 4.5, Opus 4.5, Haiku 4.5
│   └── ZDR eligible (with limited technical retention)
│
├── Why Use
│   ├── Eliminates JSON.parse() errors
│   ├── Guaranteed field types and required fields
│   └── No retries for schema violations
│
├── JSON Outputs (output_config.format)
│   ├── Quick Start (Shell, Python, TS examples)
│   ├── How It Works
│   │   ├── Constrained decoding (grammar enforcement)
│   │   ├── Schema compiled to grammar on first request
│   │   └── 24h grammar cache
│   ├── SDK Methods
│   │   ├── Python: messages.parse() with Pydantic BaseModel
│   │   ├── TypeScript: messages.parse() with Zod zodOutputFormat()
│   │   └── SDK auto-handles unsupported constraints
│   └── Common Use Cases
│       ├── Data extraction
│       ├── Structured reports
│       └── API response formatting
│
├── Strict Tool Use (strict: true)
│   ├── Guarantees tool inputs match schema exactly
│   ├── additionalProperties: false required
│   └── All properties must be in required[]
│
├── Using Both Together
│   └── JSON output format + strict tool definitions in same request
│
├── Important Considerations
│   ├── Grammar Compilation & Caching
│   │   ├── First request: compilation latency
│   │   └── 24h cache for same schema
│   ├── Prompt Modification & Token Costs
│   │   └── Slight increase in input tokens
│   ├── JSON Schema Limitations
│   │   ├── Supported: object, array, string, integer, number, boolean, null
│   │   ├── Supported: enum, const, anyOf, allOf, $ref/$def
│   │   ├── Supported formats: date-time, time, date, duration, email, hostname, uri, ipv4, ipv6, uuid
│   │   ├── NOT supported: recursive schemas
│   │   ├── NOT supported: numerical constraints (min, max, multipleOf)
│   │   ├── NOT supported: string constraints (minLength, maxLength)
│   │   ├── NOT supported: complex array constraints
│   │   └── additionalProperties must be false (required for all objects)
│   ├── Property Ordering
│   │   └── Response follows schema property order
│   ├── Invalid Outputs
│   │   ├── stop_reason: "refusal" → may not match schema
│   │   └── stop_reason: "max_tokens" → may be incomplete
│   └── Schema Complexity Limits
│       ├── Explicit: max 200 properties, max depth 5
│       ├── Internal limits on total nodes
│       └── Tips: flatten, reduce anyOf, use $ref
│
├── Feature Compatibility
│   ├── Works with: batches, streaming, token counting, thinking
│   └── INCOMPATIBLE with: citations, message prefilling (Opus 4.6)
│
└── Data Retention
    └── Schemas compiled & cached 24h (limited technical retention)
```

---

## Computer Use (404 — URL not accessible via WebFetch)

> Note: `platform.claude.com/docs/en/agents-and-tools/computer-use/overview`
> returned 404 on both `.md` and bare paths. The taxonomy below is derived from
> the inlined skill reference (`shared/tool-use-concepts.md`).

```
Computer Use (from inlined skill docs)
├── Anthropic-Hosted (server-side)
│   └── Like code execution — declare tool, Claude runs it
├── Self-Hosted (client-side)
│   └── You provide desktop environment, execute actions
├── Capabilities: screenshots, mouse, keyboard
└── Full docs: WebFetch → platform.claude.com/docs/en/agents-and-tools/computer-use/overview
```

---

## Updated Feature Coverage Matrix (with live-fetched topics)

```
┌──────────────────────────┬─────┬─────┬──────┬─────┬──────┬─────┬─────┬──────┐
│ Feature                  │ PY  │ TS  │ Java │ Go  │ Ruby │ C#  │ PHP │ cURL │
├──────────────────────────┼─────┼─────┼──────┼─────┼──────┼─────┼─────┼──────┤
│ Basic messages           │  x  │  x  │  x   │  x  │  x   │  x  │  x  │  x   │
│ Streaming                │  x  │  x  │  x   │  x  │  x   │  x  │  x  │  x   │
│ Adaptive thinking        │  x  │  x  │  x   │  x  │  -   │  x  │  x  │  x   │
│ Tool runner (beta)       │  x  │  x  │  x   │  x  │  x   │  -  │  x  │  -   │
│ Manual tool loop         │  x  │  x  │  x   │  x  │  x   │  x  │  x  │  x   │
│ Code execution           │  x  │  x  │  x   │  -  │  -   │  x  │  -  │  x   │
│ Memory tool              │  x  │  x  │  x   │  x  │  x   │  x  │  x  │  x   │
│ Structured outputs       │  x  │  x  │  x   │  -  │  -   │  x  │  x  │  x   │
│ Prompt caching           │  x  │  x  │  x   │  x  │  x   │  x  │  x  │  x   │
│ Batches                  │  x  │  x  │  -   │  -  │  -   │  -  │  -  │  -   │
│ Files API                │  x  │  x  │  x   │  x  │  -   │  x  │  -  │  -   │
│ Compaction               │  x  │  x  │  -   │  x  │  -   │  x  │  -  │  x   │
│ Agent SDK                │  x  │  x  │  -   │  -  │  -   │  -  │  -  │  -   │
│ MCP helpers              │  x  │  x  │  -   │  -  │  -   │  -  │  -  │  -   │
│ Vision                   │  x  │  x  │  -   │  -  │  -   │  -  │  -  │  -   │
│ PDF input                │  -  │  -  │  x   │  x  │  -   │  x  │  -  │  -   │
│ Citations                │  x  │  x  │  x   │  -  │  -   │  -  │  -  │  x   │
│ Tool search              │  x  │  x  │  x   │  x  │  x   │  x  │  x  │  x   │
│ Programmatic tool call   │  x  │  x  │  x   │  x  │  x   │  x  │  x  │  x   │
│ Web search/fetch         │  x  │  x  │  x   │  x  │  x   │  x  │  x  │  x   │
│ Computer use             │  -  │  -  │  -   │  -  │  -   │  -  │  -  │  x   │
└──────────────────────────┴─────┴─────┴──────┴─────┴──────┴─────┴─────┴──────┘

Notes:
- Memory tool, tool search, programmatic tool calling, and web search/fetch
  are server-side features available via the Messages API in ALL languages.
- Citations examples in live docs: Shell, Python, TS, Java.
- Computer use: only cURL raw HTTP shown (self-hosted needs any HTTP client).
- Coverage reflects what has explicit code examples in live docs.
```

---

## Summary of What Was Fetched

| Topic | Source URL | Status |
|-------|-----------|--------|
| Programmatic Tool Calling | platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling | ✅ Full |
| Tool Search Tool | platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool | ✅ Full |
| Citations | platform.claude.com/docs/en/build-with-claude/citations | ✅ Full |
| Context Windows | platform.claude.com/docs/en/build-with-claude/context-windows | ✅ Full |
| Rate Limits | platform.claude.com/docs/en/api/rate-limits | ✅ Full |
| Memory Tool | platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | ✅ Full |
| Compaction | platform.claude.com/docs/en/build-with-claude/compaction | ✅ Full |
| Structured Outputs | platform.claude.com/docs/en/build-with-claude/structured-outputs | ✅ Full |
| Computer Use | platform.claude.com/docs/en/agents-and-tools/computer-use/overview | ❌ 404 |
