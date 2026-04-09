/**
 * index.ts — Public surface of the julia package.
 *
 * Re-exports every public symbol from all modules so consumers can
 * import from "julia" (or from the built dist/index.js) without
 * reaching into internal file paths.
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

// ── types ─────────────────────────────────────────────────────
export {
  // Branded ID constructors + types
  ProjectId,
  FileId,
  ChunkId,
  MatterId,
  ReviewTableId,
  AuditLogId,
  // Option
  Some,
  None,
  isSome,
  isNone,
  flatMap,
  getOrElse,
  // Result
  Ok,
  Err,
  isOk,
  isErr,
  // Domain companion objects
  VaultProject,
  VaultFile,
  ClientMatter,
  // Type guards
  isProcessingComplete,
  // Enums / constants
  LEGAL_SKILLS,
  // Exhaustive check helper
  assertNever,
} from "./types.js";

export type {
  // Branded ID types
  ProjectId,
  FileId,
  ChunkId,
  MatterId,
  ReviewTableId,
  AuditLogId,
  // Option
  Option,
  Some,
  None,
  // Result
  Result,
  VaultError,
  // Status enums
  ProcessingStatus,
  RiskScore,
  Verdict,
  MatterStatus,
  // Domain types
  VaultProject,
  VaultFile,
  VaultChunk,
  ReviewColumnType,
  ReviewColumn,
  ReviewTable,
  ReviewRowStatus,
  ReviewRow,
  ClientMatter,
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
