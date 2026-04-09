/**
 * knowledge-work-managed-agents
 *
 * 14-layer managed agent runtime for knowledge work.
 * Connects the full stack: circuits → tracers → prompts → tasks →
 * subtasks → subagents → harness → evals, with cross-cutting layers
 * for training, steering, reasoning, behavioral safety, welfare,
 * and governance.
 *
 * Two execution surfaces, one interface:
 *
 *   LOCAL  — @anthropic-ai/claude-agent-sdk (code.claude.com)
 *            Runs on your machine with file/shell/git access.
 *            Use: mode "local" in AgentOptions.
 *
 *   CLOUD  — Managed Agents API (platform.claude.com)
 *            Runs in Anthropic-hosted sandbox via SSE streaming.
 *            Use: mode "cloud" in AgentOptions.
 *
 *   API    — Direct Messages API (fallback, no tools)
 *            Single-turn prompt → response.
 *            Use: mode "api" in AgentOptions (default).
 *
 * MCP server: exposes the 14-layer stack as tools for Claude Code.
 *   Add to .claude/settings.json mcpServers or run standalone.
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 *
 * @packageDocumentation
 */

// ── Core Agent Runtime ───────────────────────────────────────
export {
  KnowledgeWorkAgent,
  type AgentOptions,
  type ExecutionResult,
  type ExecutionMode,
} from "./agent.js";

// ── Claude Code Agent SDK (local execution) ──────────────────
export {
  executeQuery,
  executeTask,
  buildTaskPrompt,
  AgentSession,
  type AgentMessage,
  type QueryOptions,
  type SessionOptions,
  type AgentSDKResult,
} from "./agent-sdk.js";

// ── Managed Agents API (cloud execution) ─────────────────────
export {
  ManagedAgentsClient,
  type ManagedAgentConfig,
  type AgentToolset,
  type CustomTool,
  type MCPServer,
  type EnvironmentConfig,
  type NetworkConfig,
  type NetworkMode,
  type Packages,
  type SessionConfig,
  type GitHubResource,
  type FileResource,
  type SessionResource,
  type SessionStatus,
  type AgentMessageEvent,
  type AgentToolUseEvent,
  type AgentCustomToolUseEvent,
  type SessionStatusEvent,
  type SessionErrorEvent,
  type SpanEvent,
  type SessionEvent as ManagedSessionEvent,
  type InputEvent,
  type CustomToolHandler,
} from "./managed-agents.js";

// ── MCP Server (tool exposure for Claude Code) ───────────────
export {
  createKnowledgeWorkServer,
  startStdioServer,
} from "./mcp.js";

// ── Session Store ────────────────────────────────────────────
export { SessionStore, type SessionEvent } from "./session.js";

// ── Task Router ──────────────────────────────────────────────
export { TaskRouter, type TaskDefinition } from "./router.js";

// ── Layer Registry ───────────────────────────────────────────
export {
  type Layer,
  type LayerResult,
  LAYER_REGISTRY,
  LAYER_IDS,
} from "./layers.js";

// ── GitHub GraphQL ───────────────────────────────────────────
export {
  GitHubGraphQL,
  type RepoInfo,
  type PullRequestInfo,
  type CommitInfo,
} from "./github.js";

// ── Crawler ──────────────────────────────────────────────────
export {
  createHttpCrawler,
  crawlUrls,
  HttpCrawler,
  Dataset,
  KeyValueStore,
  RequestQueue,
  sleep,
  type CrawlResult,
  type CrawlerConfig,
} from "./crawler.js";

// ── Markdown ─────────────────────────────────────────────────
export {
  renderMarkdown,
  parseMarkdown,
  extractFrontmatter,
  extractHeadings,
  extractCodeBlocks,
  extractLinks,
  extractStructure,
  type Heading,
  type CodeBlock,
  type Frontmatter,
  type MarkdownStructure,
} from "./markdown.js";
