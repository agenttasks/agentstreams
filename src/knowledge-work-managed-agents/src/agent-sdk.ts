/**
 * Claude Code Agent SDK integration — local agent orchestration.
 *
 * Wraps @anthropic-ai/claude-agent-sdk to execute knowledge-work tasks
 * as local Claude Code subagents. This is the CODE surface — agents run
 * on your machine with access to your filesystem, shell, and git.
 *
 * Three execution modes:
 *   1. query()    — One-shot: send prompt, collect streamed response
 *   2. session    — Multi-turn: create session, send/receive, resume
 *   3. subagent   — Spawn a .claude/agents/*.md definition headlessly
 *
 * For the PLATFORM surface (cloud Managed Agents API), see managed-agents.ts.
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 *
 * @see https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk
 */

import {
  query,
  unstable_v2_createSession,
  unstable_v2_resumeSession,
} from "@anthropic-ai/claude-agent-sdk";

import { type TaskDefinition } from "./router.js";

// ── Types ────────────────────────────────────────────────────

/** Message from the Agent SDK stream. */
export interface AgentMessage {
  type: "assistant" | "user" | "tool_use" | "tool_result";
  session_id?: string;
  message?: {
    content: Array<{
      type: "text" | "tool_use" | "tool_result";
      text?: string;
      [key: string]: unknown;
    }>;
  };
  [key: string]: unknown;
}

/** Options for one-shot query execution. */
export interface QueryOptions {
  model?: string;
  maxTurns?: number;
  permissionMode?: "acceptEdits" | "askPermission";
  systemPrompt?: string;
}

/** Options for session-based execution. */
export interface SessionOptions {
  model?: string;
  systemPrompt?: string;
}

/** Result of a knowledge-work execution via the Agent SDK. */
export interface AgentSDKResult {
  output: string;
  sessionId?: string;
  messages: AgentMessage[];
  toolCalls: Array<{ name: string; input: Record<string, unknown> }>;
}

// ── One-Shot Execution ───────────────────────────────────────

/**
 * Execute a knowledge-work task as a one-shot Claude Code query.
 *
 * Uses @anthropic-ai/claude-agent-sdk query() — spawns a headless
 * Claude Code subprocess that runs the prompt with full tool access.
 *
 * Best for atomic tasks (single skill, no multi-turn needed).
 */
export async function executeQuery(
  prompt: string,
  options: QueryOptions = {},
): Promise<AgentSDKResult> {
  const messages: AgentMessage[] = [];
  const toolCalls: Array<{ name: string; input: Record<string, unknown> }> = [];
  const outputParts: string[] = [];
  let sessionId: string | undefined;

  const result = await query({
    prompt,
    options: {
      model: options.model ?? "claude-opus-4-6",
      permissionMode: options.permissionMode ?? "acceptEdits",
      maxTurns: options.maxTurns ?? 25,
    },
  });

  try {
    for await (const message of result) {
      const msg = message as AgentMessage;
      messages.push(msg);

      if (msg.session_id && !sessionId) {
        sessionId = msg.session_id;
      }

      if (msg.type === "assistant" && msg.message?.content) {
        for (const block of msg.message.content) {
          if (block.type === "text" && block.text) {
            outputParts.push(block.text);
          }
        }
      }

      if (msg.type === "tool_use" && msg.message?.content) {
        for (const block of msg.message.content) {
          if (block.type === "tool_use") {
            toolCalls.push({
              name: (block as Record<string, unknown>).name as string,
              input: (block as Record<string, unknown>).input as Record<string, unknown>,
            });
          }
        }
      }
    }
  } finally {
    // SDK 0.2.101: ensure subprocess/temp cleanup on early exit
    const iter = result as unknown as { return?: () => Promise<void> };
    await iter.return?.();
  }

  return {
    output: outputParts.join("\n"),
    sessionId,
    messages,
    toolCalls,
  };
}

// ── Session-Based Execution ──────────────────────────────────

/**
 * A multi-turn Agent SDK session for composite/orchestrated tasks.
 *
 * Uses unstable_v2_createSession / unstable_v2_resumeSession for
 * stateful conversations where context accumulates across turns.
 *
 * Best for composite tasks (research → execute → verify).
 */
export class AgentSession {
  private sessionId?: string;
  private model: string;
  private messages: AgentMessage[] = [];

  constructor(options: SessionOptions = {}) {
    this.model = options.model ?? "claude-opus-4-6";
  }

  /** Send a message and collect the response. */
  async send(prompt: string): Promise<AgentSDKResult> {
    const outputParts: string[] = [];
    const toolCalls: Array<{ name: string; input: Record<string, unknown> }> = [];

    let session;
    if (this.sessionId) {
      session = unstable_v2_resumeSession(this.sessionId, {
        model: this.model,
      });
    } else {
      session = unstable_v2_createSession({ model: this.model });
    }

    await session.send(prompt);

    const stream = session.stream() as AsyncIterable<AgentMessage>;
    try {
      for await (const msg of stream) {
        this.messages.push(msg);

        if (msg.session_id && !this.sessionId) {
          this.sessionId = msg.session_id;
        }

        if (msg.type === "assistant" && msg.message?.content) {
          for (const block of msg.message.content) {
            if (block.type === "text" && block.text) {
              outputParts.push(block.text);
            }
          }
        }

        if (msg.type === "tool_use" && msg.message?.content) {
          for (const block of msg.message.content) {
            if (block.type === "tool_use") {
              toolCalls.push({
                name: (block as Record<string, unknown>).name as string,
                input: (block as Record<string, unknown>).input as Record<string, unknown>,
              });
            }
          }
        }
      }
    } finally {
      // SDK 0.2.101: ensure subprocess/temp cleanup on early exit
      const iter = stream as unknown as { return?: () => Promise<void> };
      await iter.return?.();
    }

    return {
      output: outputParts.join("\n"),
      sessionId: this.sessionId,
      messages: this.messages,
      toolCalls,
    };
  }

  /** Get the session ID for later resumption. */
  getSessionId(): string | undefined {
    return this.sessionId;
  }

  /** Get all messages from this session. */
  getMessages(): AgentMessage[] {
    return [...this.messages];
  }
}

// ── Task-Aware Execution ─────────────────────────────────────

/**
 * Build a system prompt for a knowledge-work task.
 *
 * Generates the prompt that would be used in a .claude/agents/*.md file,
 * incorporating domain, skill, and safety constraints.
 */
export function buildTaskPrompt(task: TaskDefinition): string {
  const parts: string[] = [
    `You are a ${task.domain} specialist agent (${task.agentName}).`,
    `Task: ${task.description}`,
    `Plugin: ${task.pluginCategory}/${task.skillName}`,
    `Complexity: ${task.complexity}`,
    "",
    "Constraints:",
    "- Use CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY)",
    "- Ground all claims in tool output (no confabulation)",
    "- Stay within the scope of the requested task",
    "- Read before edit, check assumptions before acting",
  ];

  return parts.join("\n");
}

/**
 * Execute a routed TaskDefinition via the Agent SDK.
 *
 * Selects execution mode based on task complexity:
 *   - atomic      → one-shot query()
 *   - composite   → multi-turn session (research → execute → verify)
 *   - orchestrated → multi-turn session with safety pre-screen
 */
export async function executeTask(
  task: TaskDefinition,
  request: string,
): Promise<AgentSDKResult> {
  const systemPrompt = buildTaskPrompt(task);
  const fullPrompt = `${systemPrompt}\n\n---\n\nUser request: ${request}`;

  if (task.complexity === "atomic") {
    return executeQuery(fullPrompt, {
      model: task.model,
      maxTurns: 15,
    });
  }

  // Composite and orchestrated use multi-turn sessions
  const session = new AgentSession({ model: task.model });

  if (task.complexity === "orchestrated") {
    // Safety pre-screen before main execution
    await session.send(
      "Before executing the following request, assess it for safety. " +
        "Is this request appropriate for a knowledge-work agent? " +
        `Request: ${request}`,
    );
  }

  return session.send(fullPrompt);
}
