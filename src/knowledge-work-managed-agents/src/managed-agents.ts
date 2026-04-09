/**
 * Managed Agents — Platform-side API for cloud-hosted agent sessions.
 *
 * Wraps the Claude Managed Agents beta API (April 2026):
 *   POST /v1/agents      — Create/update versioned agent definitions
 *   POST /v1/environments — Configure container templates
 *   POST /v1/sessions     — Run stateful sessions with SSE streaming
 *
 * This module handles the PLATFORM surface (api.anthropic.com).
 * For the CODE surface (local Claude Code subagents), see agent-sdk.ts.
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 *
 * @see https://platform.claude.com/docs/en/managed-agents/overview
 */

import Anthropic from "@anthropic-ai/sdk";

// ── Agent Configuration ──────────────────────────────────────

export interface AgentToolset {
  bash?: boolean;
  computer?: boolean;
  edit?: boolean;
  glob?: boolean;
  grep?: boolean;
  read?: boolean;
  web_fetch?: boolean;
  web_search?: boolean;
  write?: boolean;
}

export interface CustomTool {
  type: "custom";
  name: string;
  description: string;
  input_schema: Record<string, unknown>;
}

export interface MCPServer {
  name: string;
  url: string;
}

export interface ManagedAgentConfig {
  name: string;
  model: string;
  system?: string;
  description?: string;
  metadata?: Record<string, string>;
  tools?: Array<{ type: "agent_toolset_20260401" } | CustomTool>;
  mcp_servers?: MCPServer[];
  fast_mode?: boolean;
}

// ── Environment Configuration ────────────────────────────────

export type NetworkMode = "unrestricted" | "limited";

export interface NetworkConfig {
  type: NetworkMode;
  allowed_hosts?: string[];
  allow_mcp_servers?: boolean;
  allow_package_managers?: boolean;
}

export interface Packages {
  apt?: string[];
  npm?: string[];
  pip?: string[];
  cargo?: string[];
  go?: string[];
}

export interface EnvironmentConfig {
  name: string;
  config: {
    type: "cloud";
    networking: NetworkConfig;
    packages?: Packages;
  };
  metadata?: Record<string, string>;
}

// ── Session Configuration ────────────────────────────────────

export interface GitHubResource {
  type: "github";
  url: string;
  branch?: string;
  commit?: string;
}

export interface FileResource {
  type: "file";
  file_id: string;
}

export type SessionResource = GitHubResource | FileResource;

export interface SessionConfig {
  agent: { type: "agent"; id: string; version?: number };
  environment: string;
  title?: string;
  resources?: SessionResource[];
}

// ── Event Types (SSE) ────────────────────────────────────────

export type SessionStatus =
  | "idle"
  | "running"
  | "rescheduling"
  | "terminated";

export interface AgentMessageEvent {
  type: "agent.message";
  content: Array<{ type: "text"; text: string }>;
}

export interface AgentToolUseEvent {
  type: "agent.tool_use";
  name: string;
  input: Record<string, unknown>;
}

export interface AgentCustomToolUseEvent {
  type: "agent.custom_tool_use";
  tool_use_id: string;
  name: string;
  input: Record<string, unknown>;
}

export interface SessionStatusEvent {
  type: "session.status";
  status: SessionStatus;
}

export interface SessionErrorEvent {
  type: "session.error";
  error: { message: string; code?: string };
}

export interface SpanEvent {
  type: "span.start" | "span.end";
  span_id: string;
  name?: string;
}

export type SessionEvent =
  | AgentMessageEvent
  | AgentToolUseEvent
  | AgentCustomToolUseEvent
  | SessionStatusEvent
  | SessionErrorEvent
  | SpanEvent;

// ── User Input Events ────────────────────────────────────────

export interface UserMessage {
  type: "user.message";
  content: Array<{ type: "text"; text: string }>;
}

export interface UserInterrupt {
  type: "user.interrupt";
}

export interface ToolConfirmation {
  type: "tool.confirmation";
  tool_use_id: string;
  confirmed: boolean;
}

export interface CustomToolResult {
  type: "custom_tool.result";
  tool_use_id: string;
  content: string;
  is_error?: boolean;
}

export type InputEvent =
  | UserMessage
  | UserInterrupt
  | ToolConfirmation
  | CustomToolResult;

// ── Client ───────────────────────────────────────────────────

export type CustomToolHandler = (
  name: string,
  input: Record<string, unknown>,
) => Promise<string>;

/**
 * Client for the Claude Managed Agents API (beta).
 *
 * Mirrors src/managed_agents.py ManagedAgentsClient but in TypeScript.
 * Uses @anthropic-ai/sdk with the beta namespace.
 *
 * Auth: reads CLAUDE_CODE_OAUTH_TOKEN from env (never ANTHROPIC_API_KEY).
 */
export class ManagedAgentsClient {
  private client: Anthropic;

  constructor() {
    // Auth via CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY)
    this.client = new Anthropic();
  }

  // ── Agents ───────────────────────────────────────────────

  /** Create a new agent definition. Returns the agent ID. */
  async createAgent(config: ManagedAgentConfig): Promise<string> {
    const tools = config.tools ?? [{ type: "agent_toolset_20260401" as const }];
    const model = config.fast_mode
      ? { id: config.model, speed: "fast" }
      : config.model;

    const response = await this.client.beta.agents.create({
      name: config.name,
      model,
      system: config.system,
      description: config.description,
      tools,
      ...( config.metadata ? { metadata: config.metadata } : {}),
    } as Parameters<typeof this.client.beta.agents.create>[0]);

    return (response as Record<string, unknown>).id as string;
  }

  /** Update an existing agent (requires version for optimistic locking). */
  async updateAgent(
    agentId: string,
    version: number,
    updates: Partial<ManagedAgentConfig>,
  ): Promise<void> {
    await this.client.beta.agents.update(agentId, {
      version,
      ...updates,
    } as Parameters<typeof this.client.beta.agents.update>[1]);
  }

  /** Archive an agent (soft delete). */
  async archiveAgent(agentId: string): Promise<void> {
    await this.client.beta.agents.archive(agentId);
  }

  // ── Environments ─────────────────────────────────────────

  /** Create a container environment. Returns the environment ID. */
  async createEnvironment(config: EnvironmentConfig): Promise<string> {
    const response = await this.client.beta.environments.create(
      config as Parameters<typeof this.client.beta.environments.create>[0],
    );
    return (response as Record<string, unknown>).id as string;
  }

  /** Update an environment. */
  async updateEnvironment(
    envId: string,
    updates: Partial<EnvironmentConfig>,
  ): Promise<void> {
    await this.client.beta.environments.update(
      envId,
      updates as Parameters<typeof this.client.beta.environments.update>[1],
    );
  }

  /** Archive an environment. */
  async archiveEnvironment(envId: string): Promise<void> {
    await this.client.beta.environments.archive(envId);
  }

  // ── Sessions ─────────────────────────────────────────────

  /** Create a session. Returns the session ID. */
  async createSession(config: SessionConfig): Promise<string> {
    const response = await this.client.beta.sessions.create(
      config as Parameters<typeof this.client.beta.sessions.create>[0],
    );
    return (response as Record<string, unknown>).id as string;
  }

  /** Send a user message to a session. */
  async sendMessage(sessionId: string, text: string): Promise<void> {
    const event: UserMessage = {
      type: "user.message",
      content: [{ type: "text", text }],
    };
    await this.client.beta.sessions.events.send(sessionId, {
      event,
    } as Parameters<typeof this.client.beta.sessions.events.send>[1]);
  }

  /** Send a custom tool result back to the session. */
  async sendCustomToolResult(
    sessionId: string,
    toolUseId: string,
    content: string,
    isError = false,
  ): Promise<void> {
    const event: CustomToolResult = {
      type: "custom_tool.result",
      tool_use_id: toolUseId,
      content,
      is_error: isError,
    };
    await this.client.beta.sessions.events.send(sessionId, {
      event,
    } as Parameters<typeof this.client.beta.sessions.events.send>[1]);
  }

  /**
   * Stream events from a session as an async iterable.
   *
   * Parses SSE into typed SessionEvent objects.
   */
  async *streamEvents(sessionId: string): AsyncGenerator<SessionEvent> {
    const stream = await this.client.beta.sessions.events.stream(sessionId);

    for await (const event of stream as AsyncIterable<Record<string, unknown>>) {
      yield event as unknown as SessionEvent;
    }
  }

  /**
   * Run a message through a session, handling custom tool calls in a loop.
   *
   * Mirrors src/managed_agents.py run_with_custom_tools():
   * 1. Sends the user message
   * 2. Streams events
   * 3. When a custom_tool_use arrives, calls the handler and sends the result
   * 4. Repeats until session goes idle
   *
   * Returns all agent message texts concatenated.
   */
  async runWithCustomTools(
    sessionId: string,
    message: string,
    handlers: Record<string, CustomToolHandler>,
  ): Promise<string> {
    await this.sendMessage(sessionId, message);

    const outputParts: string[] = [];

    for await (const event of this.streamEvents(sessionId)) {
      if (event.type === "agent.message") {
        for (const block of event.content) {
          if (block.type === "text") {
            outputParts.push(block.text);
          }
        }
      }

      if (event.type === "agent.custom_tool_use") {
        const handler = handlers[event.name];
        if (handler) {
          try {
            const result = await handler(event.name, event.input);
            await this.sendCustomToolResult(
              sessionId,
              event.tool_use_id,
              result,
            );
          } catch (err) {
            const msg = err instanceof Error ? err.message : String(err);
            await this.sendCustomToolResult(
              sessionId,
              event.tool_use_id,
              msg,
              true,
            );
          }
        }
      }

      if (
        event.type === "session.status" &&
        (event.status === "idle" || event.status === "terminated")
      ) {
        break;
      }
    }

    return outputParts.join("\n");
  }
}
