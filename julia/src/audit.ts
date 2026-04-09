/**
 * audit.ts — Audit log CRUD with cursor-based pagination.
 *
 * julia_audit_logs is a Kimball transaction fact table:
 *   - Every JuliaEvent produces one immutable row.
 *   - Rows are never updated or deleted.
 *   - id is a serial/bigserial — monotonically increasing, used as cursor.
 *
 * eventToRow() uses an exhaustive switch (assertNever totality check)
 * so TypeScript will error at compile time if a new event type is added
 * to JuliaEvent without handling it here.
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

import {
  Ok,
  Err,
  Some,
  None,
  AuditLogId,
  MatterId,
  ProjectId,
  assertNever,
  type Result,
  type Option,
  type AuditLogEntry,
  type JuliaEvent,
} from "./types.js";
import { getSql } from "./db.js";

// ── Row shape written to the database ───────────────────────

type AuditRow = {
  event_type: string;
  user_email: string | null;
  client_matter_id: string | null;
  project_id: string | null;
  input_summary: string | null;
  output_summary: string | null;
  model: string | null;
  input_tokens: number | null;
  output_tokens: number | null;
  duration_ms: number | null;
  metadata: Record<string, unknown>;
};

// ── Helpers ──────────────────────────────────────────────────

/**
 * Converts a JuliaEvent to the column values for julia_audit_logs.
 *
 * Uses an exhaustive switch so the TypeScript compiler enforces totality:
 * adding a new variant to JuliaEvent without handling it here is a
 * compile-time error (Ch.6 p.150, assertNever).
 *
 * @param event - Discriminated union covering all 10 event types.
 * @param opts  - Optional user email and model override.
 */
export function eventToRow(
  event: JuliaEvent,
  opts?: { userEmail?: string; model?: string },
): AuditRow {
  const base: AuditRow = {
    event_type: event.type,
    user_email: opts?.userEmail ?? null,
    client_matter_id: null,
    project_id: null,
    input_summary: null,
    output_summary: null,
    model: opts?.model ?? null,
    input_tokens: null,
    output_tokens: null,
    duration_ms: null,
    metadata: {},
  };

  switch (event.type) {
    case "vault.create_project":
      return {
        ...base,
        project_id: event.projectId,
        input_summary: event.name,
      };

    case "vault.upload":
      return {
        ...base,
        project_id: event.projectId,
        input_summary: event.filename,
        metadata: { file_id: event.fileId },
      };

    case "vault.search":
      return {
        ...base,
        project_id: event.projectId,
        input_summary: event.query,
      };

    case "vault.delete_file":
      return {
        ...base,
        project_id: event.projectId,
        metadata: { file_id: event.fileId },
      };

    case "vault.create_review_table":
      return {
        ...base,
        project_id: event.projectId,
        metadata: { review_table_id: event.reviewTableId },
      };

    case "matter.create":
      return {
        ...base,
        client_matter_id: event.matterId,
        input_summary: event.name,
      };

    case "matter.delete":
      return {
        ...base,
        client_matter_id: event.matterId,
      };

    case "matter.associate_query":
      return {
        ...base,
        client_matter_id: event.matterId,
        input_tokens: event.tokens,
        metadata: { tokens: event.tokens },
      };

    case "completion":
      return {
        ...base,
        client_matter_id: event.matterId,
        input_summary: event.query,
        model: event.model,
        input_tokens: event.input_tokens,
        output_tokens: event.output_tokens,
        duration_ms: event.duration_ms,
        metadata: { project_ids: event.projectIds },
      };

    case "assistant.session":
      return {
        ...base,
        client_matter_id: event.matterId,
        input_summary: event.skill,
        metadata: { session_id: event.sessionId, skill: event.skill },
      };

    default:
      // Totality check — unreachable if all 10 cases are handled above.
      return assertNever(event);
  }
}

/**
 * Hydrates an AuditLogEntry from a raw database row.
 *
 * @param row - Raw object returned by the Neon SQL driver.
 */
export function rowToEntry(row: Record<string, unknown>): AuditLogEntry {
  return {
    id: AuditLogId(row["id"] as number),
    event_type: row["event_type"] as string,
    user_email: (row["user_email"] as string | null) ?? null,
    client_matter_id: row["client_matter_id"]
      ? MatterId(row["client_matter_id"] as string)
      : null,
    project_id: row["project_id"]
      ? ProjectId(row["project_id"] as string)
      : null,
    input_summary: (row["input_summary"] as string | null) ?? null,
    output_summary: (row["output_summary"] as string | null) ?? null,
    model: (row["model"] as string | null) ?? null,
    input_tokens: (row["input_tokens"] as number | null) ?? null,
    output_tokens: (row["output_tokens"] as number | null) ?? null,
    duration_ms: (row["duration_ms"] as number | null) ?? null,
    metadata: (row["metadata"] as Record<string, unknown>) ?? {},
    created_at: new Date(row["created_at"] as string),
  };
}

// ── Public API ───────────────────────────────────────────────

/**
 * Inserts a new audit log entry for the given JuliaEvent.
 *
 * @param event - Any JuliaEvent variant (exhaustive handling guaranteed).
 * @param opts  - Optional user email and model for context columns.
 * @returns Ok(AuditLogId) on success, Err on database failure.
 */
export async function log(
  event: JuliaEvent,
  opts?: { userEmail?: string; model?: string },
): Promise<Result<AuditLogId>> {
  try {
    const sqlResult = getSql();
    if (!sqlResult.ok) return sqlResult;
    const sql = sqlResult.value;
    const r = eventToRow(event, opts);

    const rows = await sql`
      INSERT INTO julia_audit_logs
        (event_type, user_email, client_matter_id, project_id,
         input_summary, output_summary, model,
         input_tokens, output_tokens, duration_ms,
         metadata, created_at)
      VALUES
        (${r.event_type},
         ${r.user_email},
         ${r.client_matter_id},
         ${r.project_id},
         ${r.input_summary},
         ${r.output_summary},
         ${r.model},
         ${r.input_tokens},
         ${r.output_tokens},
         ${r.duration_ms},
         ${JSON.stringify(r.metadata)},
         now())
      RETURNING id
    `;

    const row = rows[0];
    if (!row) {
      return Err({ type: "database_error", message: "INSERT returned no row" });
    }
    return Ok(AuditLogId(row["id"] as number));
  } catch (err) {
    return Err({
      type: "database_error",
      message: err instanceof Error ? err.message : String(err),
    });
  }
}

/**
 * Returns the earliest audit log entry (lowest id).
 *
 * @returns Ok(Some(AuditLogEntry)) if found, Ok(None) if empty, Err on failure.
 */
export async function getEarliest(): Promise<Result<Option<AuditLogEntry>>> {
  try {
    const sqlResult = getSql();
    if (!sqlResult.ok) return sqlResult;
    const sql = sqlResult.value;
    const rows = await sql`
      SELECT
        id, event_type, user_email, client_matter_id, project_id,
        input_summary, output_summary, model,
        input_tokens, output_tokens, duration_ms,
        metadata, created_at
      FROM julia_audit_logs
      ORDER BY id ASC
      LIMIT 1
    `;
    const row = rows[0];
    return Ok(row ? Some(rowToEntry(row as Record<string, unknown>)) : None);
  } catch (err) {
    return Err({
      type: "database_error",
      message: err instanceof Error ? err.message : String(err),
    });
  }
}

/**
 * Returns the latest audit log entry (highest id).
 *
 * @returns Ok(Some(AuditLogEntry)) if found, Ok(None) if empty, Err on failure.
 */
export async function getLatest(): Promise<Result<Option<AuditLogEntry>>> {
  try {
    const sqlResult = getSql();
    if (!sqlResult.ok) return sqlResult;
    const sql = sqlResult.value;
    const rows = await sql`
      SELECT
        id, event_type, user_email, client_matter_id, project_id,
        input_summary, output_summary, model,
        input_tokens, output_tokens, duration_ms,
        metadata, created_at
      FROM julia_audit_logs
      ORDER BY id DESC
      LIMIT 1
    `;
    const row = rows[0];
    return Ok(row ? Some(rowToEntry(row as Record<string, unknown>)) : None);
  } catch (err) {
    return Err({
      type: "database_error",
      message: err instanceof Error ? err.message : String(err),
    });
  }
}

/**
 * Pages forward through audit logs starting after the given cursor id.
 *
 * Returns Result wrapping the entries array instead of an async generator,
 * so SQL errors are captured in the Result rather than thrown from next().
 *
 * @param fromId - Exclusive lower-bound cursor (entries with id > fromId).
 * @param take   - Maximum number of entries to return.
 */
export async function queryForward(
  fromId: AuditLogId,
  take: number,
): Promise<Result<AuditLogEntry[]>> {
  try {
    const sqlResult = getSql();
    if (!sqlResult.ok) return sqlResult;
    const sql = sqlResult.value;
    const rows = await sql`
      SELECT
        id, event_type, user_email, client_matter_id, project_id,
        input_summary, output_summary, model,
        input_tokens, output_tokens, duration_ms,
        metadata, created_at
      FROM julia_audit_logs
      WHERE id > ${fromId as number}
      ORDER BY id ASC
      LIMIT ${take}
    `;
    return Ok(rows.map((row) => rowToEntry(row as Record<string, unknown>)));
  } catch (err) {
    return Err({
      type: "database_error",
      message: err instanceof Error ? err.message : String(err),
    });
  }
}

/**
 * Returns the first audit log entry whose created_at is >= the given
 * timestamp (i.e., the closest entry at or after that point in time).
 *
 * @param timestamp - Lower-bound timestamp for the search.
 * @returns Ok(Some(AuditLogEntry)) if found, Ok(None) otherwise, Err on failure.
 */
export async function searchByTimestamp(
  timestamp: Date,
): Promise<Result<Option<AuditLogEntry>>> {
  try {
    if (isNaN(timestamp.getTime())) {
      return Err({
        type: "invalid_input",
        field: "timestamp",
        message: "Invalid date",
      });
    }
    const sqlResult = getSql();
    if (!sqlResult.ok) return sqlResult;
    const sql = sqlResult.value;
    const rows = await sql`
      SELECT
        id, event_type, user_email, client_matter_id, project_id,
        input_summary, output_summary, model,
        input_tokens, output_tokens, duration_ms,
        metadata, created_at
      FROM julia_audit_logs
      WHERE created_at >= ${timestamp.toISOString()}
      ORDER BY created_at ASC
      LIMIT 1
    `;
    const row = rows[0];
    return Ok(row ? Some(rowToEntry(row as Record<string, unknown>)) : None);
  } catch (err) {
    return Err({
      type: "database_error",
      message: err instanceof Error ? err.message : String(err),
    });
  }
}
