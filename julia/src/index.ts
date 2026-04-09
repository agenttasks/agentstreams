/**
 * index.ts — Public surface of the julia package.
 *
 * Re-exports every public symbol from all modules so consumers can
 * import from "julia" (or from the built dist/index.js) without
 * reaching into internal file paths.
 *
 * Names that are both a value and a type (companion pattern, Cherny Ch.6
 * p.160) are listed once in the value export block — TypeScript makes
 * them available as types automatically. Pure types that have no value
 * counterpart are in the `export type` block.
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

// ── types — values (constructors, guards, constants) ─────────
export {
  // Branded ID constructors (also serve as the nominal type)
  ProjectId,
  FileId,
  ChunkId,
  MatterId,
  ReviewTableId,
  AuditLogId,
  // Option constructors + guards
  Some,
  None,
  isSome,
  isNone,
  flatMap,
  getOrElse,
  // Result constructors + guards
  Ok,
  Err,
  isOk,
  isErr,
  // Domain companion objects
  VaultProject,
  VaultFile,
  ClientMatter,
  // Type guard function
  isProcessingComplete,
  // Enum constant
  LEGAL_SKILLS,
  // Exhaustive check helper
  assertNever,
} from "./types.js";

// ── types — pure types (no runtime value) ────────────────────
export type {
  // Option wrapper
  Option,
  // Result wrapper
  Result,
  VaultError,
  // Status / enum types
  ProcessingStatus,
  RiskScore,
  Verdict,
  MatterStatus,
  // Domain model types
  VaultChunk,
  ReviewColumnType,
  ReviewColumn,
  ReviewTable,
  ReviewRowStatus,
  ReviewRow,
  MatterUsageStats,
  AuditLogEntry,
  // Event unions
  VaultEvent,
  MatterEvent,
  CompletionEvent,
  AssistantEvent,
  JuliaEvent,
  // Legal skills
  LegalSkill,
  // Completion
  Citation,
  CompletionResponse,
  SearchResult,
  // Analysis
  Finding,
  AnalysisResult,
  // Emotion types (from transformer-circuits.pub/2026/emotions)
  EmotionDimension,
  EmotionValence,
  EmotionExpression,
  EmotionActivation,
  EmotionProbe,
  EmotionAlert,
  EmotionAlertEvent,
  EmotionMonitorConfig,
} from "./types.js";

// ── vault ─────────────────────────────────────────────────────
export {
  createProject,
  uploadFile,
  semanticSearch,
  getFileDetails,
  deleteFile,
  createReviewTable,
  getReviewRow,
  chunkText,
  hashEmbedding,
} from "./vault.js";

// ── completion ────────────────────────────────────────────────
export { complete, buildLegalSystemPrompt, mergeSearchResults } from "./completion.js";
export type { CompletionRequest } from "./completion.js";

// ── matters ───────────────────────────────────────────────────
export { addMatters, getMatters, deleteMatters, associateQuery } from "./matters.js";

// ── audit ─────────────────────────────────────────────────────
export { log, getEarliest, getLatest, queryForward, searchByTimestamp } from "./audit.js";

// ── assistant ─────────────────────────────────────────────────
export { JuliaSession, JuliaSessionBuilder } from "./assistant.js";

// ── emotions ─────────────────────────────────────────────────
export {
  createEmotionProbe,
  analyzeDesperationRisk,
  detectDeflection,
  computeArousal,
  checkEmotionGate,
  probeTextForEmotions,
  DEFAULT_EMOTION_CONFIG,
  EMOTION_VALENCE_MAP,
} from "./emotions.js";

// ── db ───────────────────────────────────────────────────────
export { getSql } from "./db.js";

// ── pipeline ─────────────────────────────────────────────────
export {
  checkGate,
  executePipeline,
  JULIA_LEGAL_WORKFLOW,
  JULIA_VAULT_REVIEW,
} from "./pipeline.js";
export type {
  PipelineStepResult,
  GateDecision,
  PipelineStep,
  PipelineGate,
  PipelineConfig,
  PipelineExecutionResult,
} from "./pipeline.js";

// ── mcp-server ───────────────────────────────────────────────
export { createJuliaServer, startStdioServer } from "./mcp-server.js";
