/**
 * knowledge-work-managed-agents
 *
 * 14-layer managed agent runtime for knowledge work.
 * Connects the full stack: circuits → tracers → prompts → tasks →
 * subtasks → subagents → harness → evals, with cross-cutting layers
 * for training, steering, reasoning, behavioral safety, welfare,
 * and governance.
 *
 * Architecture follows Anthropic's Managed Agents design:
 *   Brain: stateless harness (Claude + system prompt + tools)
 *   Hands: cloud containers with bash, file ops, web access
 *   Session: append-only event log for recovery and context
 *
 * Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
 *
 * @packageDocumentation
 */

export { KnowledgeWorkAgent, type AgentOptions } from "./agent.js";
export { SessionStore, type SessionEvent } from "./session.js";
export { TaskRouter, type TaskDefinition } from "./router.js";
export {
  type Layer,
  type LayerResult,
  LAYER_REGISTRY,
  LAYER_IDS,
} from "./layers.js";
