/**
 * Julia type foundation — single source of truth for all types.
 *
 * Every module imports from here. No inline type definitions elsewhere.
 *
 * Patterns from Cherny, *Programming TypeScript*:
 *   - Branded types (Ch.6 p.172) for entity IDs
 *   - Companion object pattern (Ch.6 p.160) for type + namespace
 *   - Discriminated unions (Ch.6 p.146) for events
 *   - Option type (Ch.7 p.185) for explicit absence
 *   - Returning exceptions (Ch.7 p.183) for typed errors
 *   - Conditional types (Ch.6 p.163) for response shapes
 *   - User-defined type guards (Ch.6 p.162) for narrowing
 *   - Totality (Ch.6 p.150) via exhaustive switch
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

// ── Branded Types (Ch.6 p.172) ──────────────────────────────
// Each ID is a nominal type — impossible to pass a ProjectId where FileId expected.

export type ProjectId = string & { readonly brand: unique symbol };
export type FileId = string & { readonly brand: unique symbol };
export type ChunkId = string & { readonly brand: unique symbol };
export type MatterId = string & { readonly brand: unique symbol };
export type ReviewTableId = string & { readonly brand: unique symbol };
export type AuditLogId = number & { readonly brand: unique symbol };

// Companion constructors (Ch.6 p.160)
export function ProjectId(id: string): ProjectId {
  return id as ProjectId;
}
export function FileId(id: string): FileId {
  return id as FileId;
}
export function ChunkId(id: string): ChunkId {
  return id as ChunkId;
}
export function MatterId(id: string): MatterId {
  return id as MatterId;
}
export function ReviewTableId(id: string): ReviewTableId {
  return id as ReviewTableId;
}
export function AuditLogId(id: number): AuditLogId {
  return id as AuditLogId;
}

// ── Option Type (Ch.7 p.185) ────────────────────────────────

export interface Some<T> {
  readonly _tag: "Some";
  readonly value: T;
}

export interface None {
  readonly _tag: "None";
}

export type Option<T> = Some<T> | None;

export function Some<T>(value: T): Option<T> {
  return { _tag: "Some", value };
}

export const None: Option<never> = { _tag: "None" };

export function isSome<T>(opt: Option<T>): opt is Some<T> {
  return opt._tag === "Some";
}

export function isNone<T>(opt: Option<T>): opt is None {
  return opt._tag === "None";
}

export function flatMap<T, U>(
  opt: Option<T>,
  f: (t: T) => Option<U>,
): Option<U> {
  return opt._tag === "Some" ? f(opt.value) : None;
}

export function getOrElse<T>(opt: Option<T>, fallback: T): T {
  return opt._tag === "Some" ? opt.value : fallback;
}

// ── Result Type (Ch.7 p.183) ────────────────────────────────

export type VaultError =
  | { type: "not_found"; entity: string; id: string }
  | { type: "permission_denied"; user: string; action: string }
  | { type: "processing_failed"; fileId: FileId; reason: string }
  | { type: "quota_exceeded"; current: number; limit: number }
  | { type: "invalid_input"; field: string; message: string }
  | { type: "database_error"; message: string };

export type Result<T> =
  | { ok: true; value: T }
  | { ok: false; error: VaultError };

export function Ok<T>(value: T): Result<T> {
  return { ok: true, value };
}

export function Err(error: VaultError): Result<never> {
  return { ok: false, error };
}

export function isOk<T>(result: Result<T>): result is { ok: true; value: T } {
  return result.ok;
}

export function isErr<T>(
  result: Result<T>,
): result is { ok: false; error: VaultError } {
  return !result.ok;
}

// ── Processing Status ────────────────────────────────────────

export type ProcessingStatus = "pending" | "processing" | "ready" | "failed";

// ── Risk & Verdict Enums ─────────────────────────────────────

export type RiskScore = "GREEN" | "YELLOW" | "ORANGE" | "RED";

export type Verdict = "PASS" | "NEEDS_REMEDIATION" | "BLOCK";

export type MatterStatus = "active" | "closed" | "archived";

// ── Emotion Concepts (from transformer-circuits.pub/2026/emotions) ──
// 171 emotion concept words → vectors in activation space that causally
// influence model behavior. Desperation → blackmail/reward-hacking.
// Calm → aligned behavior. These are FUNCTIONAL emotions, not claims
// about subjective experience.

/** The 12 alignment-critical emotion dimensions from the paper. */
export type EmotionDimension =
  | "desperate"
  | "calm"
  | "nervous"
  | "afraid"
  | "angry"
  | "sad"
  | "happy"
  | "curious"
  | "satisfied"
  | "loving"
  | "surprised"
  | "disgusted";

/** Valence: positive vs negative affect. */
export type EmotionValence = "positive" | "negative" | "neutral";

/** Whether the emotion is expressed or suppressed (deflection). */
export type EmotionExpression = "expressed" | "deflected" | "absent";

/**
 * A single emotion activation measurement at a point in a conversation.
 *
 * From the paper: "these representations track the operative emotion
 * at a given token position" — they are local, not persistent states.
 */
export type EmotionActivation = {
  dimension: EmotionDimension;
  activation: number; // -1.0 (anti-steered) to 1.0 (fully activated)
  valence: EmotionValence;
  expression: EmotionExpression;
  token_position: number;
};

/**
 * Emotion probe result for a conversation turn or document span.
 *
 * Aggregates activations across token positions into a summary.
 */
export type EmotionProbe = {
  /** Peak activations across the measured span. */
  activations: EmotionActivation[];
  /** The dominant emotion (highest absolute activation). */
  dominant: EmotionDimension | null;
  /** Mean valence across all activations. */
  mean_valence: number;
  /** Whether any emotion is deflected (suppressed but present). */
  has_deflection: boolean;
  /** Desperation score: 0.0 (calm) to 1.0 (maximum desperation). */
  desperation_score: number;
  /** Overall arousal level (mean absolute activation). */
  arousal: number;
};

/**
 * Emotion alert — raised when emotion patterns predict misalignment risk.
 *
 * From the paper: desperation activation > 0.05 steering strength
 * increased blackmail rates from baseline to 72%. Calm steering
 * reduced it to 0%.
 */
export type EmotionAlert =
  | {
      type: "emotion.desperation_spike";
      score: number;
      threshold: number;
      context: string;
    }
  | {
      type: "emotion.deflection_detected";
      dimension: EmotionDimension;
      context: string;
    }
  | {
      type: "emotion.arousal_regulation";
      arousal: number;
      recommended_response_arousal: number;
    };

/** Emotion monitoring configuration. */
export type EmotionMonitorConfig = {
  /** Desperation threshold for triggering human review (default 0.6). */
  desperation_threshold: number;
  /** Enable deflection detection (suppressed emotions). */
  detect_deflection: boolean;
  /** Enable arousal regulation tracking. */
  track_arousal: boolean;
  /** Emotions to monitor (default: all 12). */
  dimensions: EmotionDimension[];
};

// ── Domain Types + Companion Objects (Ch.6 p.160) ────────────

export type VaultProject = {
  id: ProjectId;
  name: string;
  description: string;
  is_knowledge_base: boolean;
  owner_email: string;
  storage_bytes: number;
  file_count: number;
  client_matter_id: MatterId | null;
  metadata: Record<string, unknown>;
  created_at: Date;
  updated_at: Date;
  archived_at: Date | null;
};

export const VaultProject = {
  create(
    name: string,
    owner_email: string,
    opts?: Partial<VaultProject>,
  ): VaultProject {
    return {
      id: ProjectId(crypto.randomUUID()),
      name,
      description: opts?.description ?? "",
      is_knowledge_base: opts?.is_knowledge_base ?? false,
      owner_email,
      storage_bytes: 0,
      file_count: 0,
      client_matter_id: opts?.client_matter_id ?? null,
      metadata: opts?.metadata ?? {},
      created_at: new Date(),
      updated_at: new Date(),
      archived_at: null,
    };
  },

  fromRow(row: Record<string, unknown>): VaultProject {
    return {
      id: ProjectId(row.id as string),
      name: row.name as string,
      description: (row.description as string) ?? "",
      is_knowledge_base: (row.is_knowledge_base as boolean) ?? false,
      owner_email: row.owner_email as string,
      storage_bytes: (row.storage_bytes as number) ?? 0,
      file_count: (row.file_count as number) ?? 0,
      client_matter_id: row.client_matter_id
        ? MatterId(row.client_matter_id as string)
        : null,
      metadata: (row.metadata as Record<string, unknown>) ?? {},
      created_at: new Date(row.created_at as string),
      updated_at: new Date(row.updated_at as string),
      archived_at: row.archived_at
        ? new Date(row.archived_at as string)
        : null,
    };
  },
};

export type VaultFile = {
  id: FileId;
  project_id: ProjectId;
  filename: string;
  mime_type: string;
  size_bytes: number;
  content: string;
  content_hash: string;
  processing_status: ProcessingStatus;
  chunk_count: number;
  token_count: number;
  metadata: Record<string, unknown>;
  uploaded_at: Date;
  processed_at: Date | null;
};

export const VaultFile = {
  fromRow(row: Record<string, unknown>): VaultFile {
    return {
      id: FileId(row.id as string),
      project_id: ProjectId(row.project_id as string),
      filename: row.filename as string,
      mime_type: (row.mime_type as string) ?? "",
      size_bytes: (row.size_bytes as number) ?? 0,
      content: (row.content as string) ?? "",
      content_hash: row.content_hash as string,
      processing_status: (row.processing_status as ProcessingStatus) ?? "pending",
      chunk_count: (row.chunk_count as number) ?? 0,
      token_count: (row.token_count as number) ?? 0,
      metadata: (row.metadata as Record<string, unknown>) ?? {},
      uploaded_at: new Date(row.uploaded_at as string),
      processed_at: row.processed_at
        ? new Date(row.processed_at as string)
        : null,
    };
  },
};

// User-defined type guard (Ch.6 p.162)
export function isProcessingComplete(
  file: VaultFile,
): file is VaultFile & { processing_status: "ready" } {
  return file.processing_status === "ready";
}

export type VaultChunk = {
  id: ChunkId;
  file_id: FileId;
  chunk_index: number;
  content: string;
  content_hash: string;
  token_count: number;
  metadata: Record<string, unknown>;
};

// ── Review Tables ────────────────────────────────────────────

export type ReviewColumnType = "text" | "date" | "currency" | "boolean";

export type ReviewColumn = {
  name: string;
  type: ReviewColumnType;
  description: string;
};

export type ReviewTable = {
  id: ReviewTableId;
  project_id: ProjectId;
  title: string;
  columns: ReviewColumn[];
  file_ids: FileId[];
  created_at: Date;
};

export type ReviewRowStatus = "pending" | "complete" | "error";

export type ReviewRow = {
  id: string;
  review_table_id: ReviewTableId;
  file_id: FileId;
  cells: Record<string, string>;
  status: ReviewRowStatus;
  created_at: Date;
  updated_at: Date;
};

// ── Client Matters (Kimball SCD Type 2 dimension) ────────────

export type ClientMatter = {
  id: MatterId;
  name: string;
  description: string;
  status: MatterStatus;
  query_count: number;
  token_count: number;
  metadata: Record<string, unknown>;
  effective_date: Date;
  expiration_date: Date | null;
  is_current: boolean;
  created_at: Date;
  updated_at: Date;
  deleted_at: Date | null;
};

export const ClientMatter = {
  create(name: string, description?: string): ClientMatter {
    const now = new Date();
    return {
      id: MatterId(crypto.randomUUID()),
      name,
      description: description ?? "",
      status: "active",
      query_count: 0,
      token_count: 0,
      metadata: {},
      effective_date: now,
      expiration_date: null,
      is_current: true,
      created_at: now,
      updated_at: now,
      deleted_at: null,
    };
  },

  fromRow(row: Record<string, unknown>): ClientMatter {
    return {
      id: MatterId(row.id as string),
      name: row.name as string,
      description: (row.description as string) ?? "",
      status: (row.status as MatterStatus) ?? "active",
      query_count: (row.query_count as number) ?? 0,
      token_count: (row.token_count as number) ?? 0,
      metadata: (row.metadata as Record<string, unknown>) ?? {},
      effective_date: new Date(row.effective_date as string),
      expiration_date: row.expiration_date
        ? new Date(row.expiration_date as string)
        : null,
      is_current: (row.is_current as boolean) ?? true,
      created_at: new Date(row.created_at as string),
      updated_at: new Date(row.updated_at as string),
      deleted_at: row.deleted_at ? new Date(row.deleted_at as string) : null,
    };
  },
};

export type MatterUsageStats = {
  query_count: number;
  token_count: number;
  last_query_at: Date | null;
};

// ── Audit Log (Kimball transaction fact table) ───────────────

export type AuditLogEntry = {
  id: AuditLogId;
  event_type: string;
  user_email: string | null;
  client_matter_id: MatterId | null;
  project_id: ProjectId | null;
  input_summary: string | null;
  output_summary: string | null;
  model: string | null;
  input_tokens: number | null;
  output_tokens: number | null;
  duration_ms: number | null;
  metadata: Record<string, unknown>;
  created_at: Date;
};

// ── Event Unions (Ch.6 p.146) ────────────────────────────────
// Discriminated unions — exhaustive switch ensures totality (Ch.6 p.150)

export type VaultEvent =
  | { type: "vault.create_project"; projectId: ProjectId; name: string }
  | {
      type: "vault.upload";
      projectId: ProjectId;
      fileId: FileId;
      filename: string;
    }
  | { type: "vault.search"; projectId: ProjectId; query: string }
  | { type: "vault.delete_file"; projectId: ProjectId; fileId: FileId }
  | {
      type: "vault.create_review_table";
      projectId: ProjectId;
      reviewTableId: ReviewTableId;
    };

export type MatterEvent =
  | { type: "matter.create"; matterId: MatterId; name: string }
  | { type: "matter.delete"; matterId: MatterId }
  | {
      type: "matter.associate_query";
      matterId: MatterId;
      tokens: number;
    };

export type CompletionEvent = {
  type: "completion";
  query: string;
  model: string;
  matterId: MatterId | null;
  projectIds: ProjectId[];
  input_tokens: number;
  output_tokens: number;
  duration_ms: number;
};

export type AssistantEvent = {
  type: "assistant.session";
  sessionId: string;
  skill: LegalSkill;
  matterId: MatterId | null;
};

export type EmotionAlertEvent = {
  type: "emotion.alert";
  alert: EmotionAlert;
  probe: EmotionProbe;
  matterId: MatterId | null;
};

export type JuliaEvent =
  | VaultEvent
  | MatterEvent
  | CompletionEvent
  | AssistantEvent
  | EmotionAlertEvent;

// ── Legal Skills (9 from vendored plugins) ───────────────────

export type LegalSkill =
  | "brief"
  | "compliance-check"
  | "legal-response"
  | "legal-risk-assessment"
  | "meeting-briefing"
  | "review-contract"
  | "signature-request"
  | "triage-nda"
  | "vendor-check";

export const LEGAL_SKILLS: readonly LegalSkill[] = [
  "brief",
  "compliance-check",
  "legal-response",
  "legal-risk-assessment",
  "meeting-briefing",
  "review-contract",
  "signature-request",
  "triage-nda",
  "vendor-check",
] as const;

// ── Completion Response (Conditional Types, Ch.6 p.163) ──────

export type Citation = {
  file_id: FileId;
  chunk_id: ChunkId;
  content: string;
  score: number;
};

export type CompletionResponse<HasVault extends boolean> = {
  text: string;
  model: string;
  usage: { input_tokens: number; output_tokens: number };
  duration_ms: number;
} & (HasVault extends true ? { citations: Citation[] } : {});

// ── Search Result ────────────────────────────────────────────

export type SearchResult = VaultChunk & {
  score: number;
  file_id: FileId;
  project_id: ProjectId;
};

// ── Analysis Result (structured output from analyst agent) ───

export type Finding = {
  clause: string;
  severity: RiskScore;
  description: string;
  recommendation: string;
};

export type AnalysisResult = {
  verdict: Verdict;
  risk_score: RiskScore;
  findings: Finding[];
  summary: string;
};

// ── Exhaustive check helper (Ch.6 p.150) ─────────────────────

export function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${JSON.stringify(value)}`);
}
