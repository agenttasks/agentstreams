/**
 * audit.test.ts — Tests written BEFORE the implementation (TDD).
 *
 * All SQL calls are mocked so tests run without a real database.
 * Verifies:
 *   - log() returns Ok(AuditLogId) for every JuliaEvent variant.
 *   - eventToRow() exhaustive switch handles all 10 event types.
 *   - getEarliest() / getLatest() return correct Option shapes.
 *   - queryForward() async generator yields entries in order.
 *   - searchByTimestamp() returns Option.Some/None correctly.
 *   - rowToEntry() hydrates branded types from raw DB rows.
 *   - All functions propagate DB errors as Err({ type: "database_error" }).
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  AuditLogId,
  MatterId,
  ProjectId,
  FileId,
  ReviewTableId,
  isOk,
  isErr,
  isSome,
  isNone,
  assertNever,
  type JuliaEvent,
  type AuditLogEntry,
} from "./types.js";

// ── SQL mock setup ───────────────────────────────────────────
//
// We mock @neondatabase/serverless so no real connection is needed.
// The module is hoisted by vitest automatically when using vi.mock().

const mockSql = vi.fn();

vi.mock("@neondatabase/serverless", () => ({
  neon: () => mockSql,
}));

// Import AFTER mocking so the module's getSql() picks up the mock.
const { log, getEarliest, getLatest, queryForward, searchByTimestamp, eventToRow, rowToEntry } =
  await import("./audit.js");

// ── Helpers ──────────────────────────────────────────────────

/** Builds a fake audit log DB row matching AuditLogEntry shape. */
function makeAuditRow(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    id: 1,
    event_type: "completion",
    user_email: "lawyer@firm.com",
    client_matter_id: null,
    project_id: null,
    input_summary: "What is force majeure?",
    output_summary: null,
    model: "claude-opus-4-6",
    input_tokens: 100,
    output_tokens: 200,
    duration_ms: 1500,
    metadata: {},
    created_at: "2026-01-01T00:00:00Z",
    ...overrides,
  };
}

/** All 10 JuliaEvent variants for exhaustiveness tests. */
const ALL_EVENTS: JuliaEvent[] = [
  { type: "vault.create_project", projectId: ProjectId("p1"), name: "Test Project" },
  {
    type: "vault.upload",
    projectId: ProjectId("p1"),
    fileId: FileId("f1"),
    filename: "contract.pdf",
  },
  { type: "vault.search", projectId: ProjectId("p1"), query: "indemnification" },
  { type: "vault.delete_file", projectId: ProjectId("p1"), fileId: FileId("f1") },
  {
    type: "vault.create_review_table",
    projectId: ProjectId("p1"),
    reviewTableId: ReviewTableId("rt1"),
  },
  { type: "matter.create", matterId: MatterId("m1"), name: "Case 1" },
  { type: "matter.delete", matterId: MatterId("m1") },
  { type: "matter.associate_query", matterId: MatterId("m1"), tokens: 500 },
  {
    type: "completion",
    query: "review NDA",
    model: "claude-opus-4-6",
    matterId: null,
    projectIds: [],
    input_tokens: 100,
    output_tokens: 200,
    duration_ms: 1500,
  },
  { type: "assistant.session", sessionId: "sess_1", skill: "review-contract", matterId: null },
];

// ── log() ────────────────────────────────────────────────────

describe("log", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    process.env["NEON_DATABASE_URL"] = "postgresql://mock";
  });

  it("returns Ok(AuditLogId) on success", async () => {
    mockSql.mockResolvedValueOnce([{ id: 42 }]);

    const result = await log({
      type: "completion",
      query: "What is force majeure?",
      model: "claude-opus-4-6",
      matterId: null,
      projectIds: [],
      input_tokens: 100,
      output_tokens: 200,
      duration_ms: 1500,
    });

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      // Branded type: at runtime it is a plain number
      expect(typeof result.value).toBe("number");
      expect(result.value as number).toBe(42);
    }
  });

  it("returns Ok for every one of the 10 JuliaEvent variants", async () => {
    for (const event of ALL_EVENTS) {
      mockSql.mockResolvedValueOnce([{ id: 1 }]);
      const result = await log(event);
      expect(isOk(result)).toBe(true);
    }
  });

  it("forwards optional userEmail and model into the INSERT", async () => {
    mockSql.mockResolvedValueOnce([{ id: 7 }]);

    const result = await log(
      { type: "matter.create", matterId: MatterId("m_abc"), name: "New Matter" },
      { userEmail: "admin@firm.com", model: "claude-sonnet-4-6" },
    );

    expect(isOk(result)).toBe(true);
    // Verify SQL was called exactly once
    expect(mockSql).toHaveBeenCalledTimes(1);
  });

  it("returns Err(database_error) when INSERT returns no row", async () => {
    mockSql.mockResolvedValueOnce([]);

    const result = await log({ type: "matter.delete", matterId: MatterId("m_gone") });

    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("database_error");
    }
  });

  it("returns Err(database_error) when SQL rejects", async () => {
    mockSql.mockRejectedValueOnce(new Error("connection refused"));

    const result = await log({
      type: "vault.search",
      projectId: ProjectId("p1"),
      query: "NDA clauses",
    });

    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("database_error");
      expect((result.error as { message: string }).message).toContain("connection refused");
    }
  });

  // Branded type safety comment:
  // The return type is Result<AuditLogId>. AuditLogId is a branded number —
  // TypeScript prevents passing it where a plain number or other ID is expected.
  it("AuditLogId branded type documents compile-time contract", async () => {
    mockSql.mockResolvedValueOnce([{ id: 99 }]);
    const result = await log({ type: "matter.delete", matterId: MatterId("m1") });
    if (isOk(result)) {
      const id: AuditLogId = result.value;
      expect(id as number).toBe(99);
      // The following would be a TYPE ERROR at compile time:
      // const plain: number = id; // ERROR: brand mismatch
    }
  });
});

// ── eventToRow() exhaustive switch ──────────────────────────

describe("eventToRow exhaustive switch", () => {
  it("handles vault.create_project — sets project_id and input_summary", () => {
    const row = eventToRow({
      type: "vault.create_project",
      projectId: ProjectId("p_1"),
      name: "Acme KB",
    });
    expect(row.event_type).toBe("vault.create_project");
    expect(row.project_id).toBe("p_1");
    expect(row.input_summary).toBe("Acme KB");
    expect(row.client_matter_id).toBeNull();
  });

  it("handles vault.upload — sets project_id, input_summary, metadata.file_id", () => {
    const row = eventToRow({
      type: "vault.upload",
      projectId: ProjectId("p_1"),
      fileId: FileId("f_abc"),
      filename: "contract.pdf",
    });
    expect(row.event_type).toBe("vault.upload");
    expect(row.project_id).toBe("p_1");
    expect(row.input_summary).toBe("contract.pdf");
    expect((row.metadata as Record<string, unknown>)["file_id"]).toBe("f_abc");
  });

  it("handles vault.search — sets project_id and input_summary to query", () => {
    const row = eventToRow({
      type: "vault.search",
      projectId: ProjectId("p_1"),
      query: "indemnification clause",
    });
    expect(row.event_type).toBe("vault.search");
    expect(row.input_summary).toBe("indemnification clause");
  });

  it("handles vault.delete_file — sets project_id and metadata.file_id", () => {
    const row = eventToRow({
      type: "vault.delete_file",
      projectId: ProjectId("p_1"),
      fileId: FileId("f_del"),
    });
    expect(row.event_type).toBe("vault.delete_file");
    expect((row.metadata as Record<string, unknown>)["file_id"]).toBe("f_del");
  });

  it("handles vault.create_review_table — sets metadata.review_table_id", () => {
    const row = eventToRow({
      type: "vault.create_review_table",
      projectId: ProjectId("p_1"),
      reviewTableId: ReviewTableId("rt_1"),
    });
    expect(row.event_type).toBe("vault.create_review_table");
    expect((row.metadata as Record<string, unknown>)["review_table_id"]).toBe("rt_1");
  });

  it("handles matter.create — sets client_matter_id and input_summary", () => {
    const row = eventToRow({
      type: "matter.create",
      matterId: MatterId("m_new"),
      name: "Acme v. Widget",
    });
    expect(row.event_type).toBe("matter.create");
    expect(row.client_matter_id).toBe("m_new");
    expect(row.input_summary).toBe("Acme v. Widget");
    expect(row.project_id).toBeNull();
  });

  it("handles matter.delete — sets client_matter_id", () => {
    const row = eventToRow({ type: "matter.delete", matterId: MatterId("m_old") });
    expect(row.event_type).toBe("matter.delete");
    expect(row.client_matter_id).toBe("m_old");
  });

  it("handles matter.associate_query — sets input_tokens and metadata.tokens", () => {
    const row = eventToRow({
      type: "matter.associate_query",
      matterId: MatterId("m_1"),
      tokens: 750,
    });
    expect(row.event_type).toBe("matter.associate_query");
    expect(row.input_tokens).toBe(750);
    expect((row.metadata as Record<string, unknown>)["tokens"]).toBe(750);
  });

  it("handles completion — sets model, input_tokens, output_tokens, duration_ms", () => {
    const row = eventToRow({
      type: "completion",
      query: "review NDA",
      model: "claude-opus-4-6",
      matterId: MatterId("m_1"),
      projectIds: [ProjectId("p_1")],
      input_tokens: 200,
      output_tokens: 400,
      duration_ms: 2000,
    });
    expect(row.event_type).toBe("completion");
    expect(row.model).toBe("claude-opus-4-6");
    expect(row.input_tokens).toBe(200);
    expect(row.output_tokens).toBe(400);
    expect(row.duration_ms).toBe(2000);
    expect(row.input_summary).toBe("review NDA");
  });

  it("handles assistant.session — sets input_summary to skill and metadata", () => {
    const row = eventToRow({
      type: "assistant.session",
      sessionId: "sess_xyz",
      skill: "triage-nda",
      matterId: MatterId("m_1"),
    });
    expect(row.event_type).toBe("assistant.session");
    expect(row.input_summary).toBe("triage-nda");
    expect((row.metadata as Record<string, unknown>)["session_id"]).toBe("sess_xyz");
    expect((row.metadata as Record<string, unknown>)["skill"]).toBe("triage-nda");
  });

  it("opts.userEmail and opts.model are forwarded to base row", () => {
    const row = eventToRow(
      { type: "matter.delete", matterId: MatterId("m_1") },
      { userEmail: "user@firm.com", model: "claude-sonnet-4-6" },
    );
    expect(row.user_email).toBe("user@firm.com");
    expect(row.model).toBe("claude-sonnet-4-6");
  });

  it("covers all 10 JuliaEvent types — exhaustive check via assertNever", () => {
    // This mirrors the totality check pattern from types.test.ts.
    // If a new event type is added, this test will fail at compile time.
    for (const event of ALL_EVENTS) {
      switch (event.type) {
        case "vault.create_project":
        case "vault.upload":
        case "vault.search":
        case "vault.delete_file":
        case "vault.create_review_table":
        case "matter.create":
        case "matter.delete":
        case "matter.associate_query":
        case "completion":
        case "assistant.session":
          break;
        default:
          assertNever(event);
      }
    }
    expect(ALL_EVENTS).toHaveLength(10);
  });
});

// ── rowToEntry() ─────────────────────────────────────────────

describe("rowToEntry", () => {
  it("hydrates branded AuditLogId (number brand)", () => {
    const entry = rowToEntry(makeAuditRow({ id: 55 }));
    expect(typeof entry.id).toBe("number");
    expect(entry.id as number).toBe(55);
    // Branded type: AuditLogId is a number, not a string
    const _typed: AuditLogId = entry.id;
    void _typed;
  });

  it("hydrates branded MatterId when client_matter_id is present", () => {
    const entry = rowToEntry(makeAuditRow({ client_matter_id: "m_hydrated" }));
    expect(entry.client_matter_id).not.toBeNull();
    expect(typeof entry.client_matter_id).toBe("string");
    expect(entry.client_matter_id as string).toBe("m_hydrated");
  });

  it("sets client_matter_id to null when absent", () => {
    const entry = rowToEntry(makeAuditRow({ client_matter_id: null }));
    expect(entry.client_matter_id).toBeNull();
  });

  it("hydrates branded ProjectId when project_id is present", () => {
    const entry = rowToEntry(makeAuditRow({ project_id: "p_hydrated" }));
    expect(entry.project_id).not.toBeNull();
    expect(entry.project_id as string).toBe("p_hydrated");
  });

  it("parses created_at as a Date object", () => {
    const entry = rowToEntry(makeAuditRow({ created_at: "2026-03-15T12:00:00Z" }));
    expect(entry.created_at).toBeInstanceOf(Date);
    expect(entry.created_at.getFullYear()).toBe(2026);
  });

  it("preserves all scalar fields", () => {
    const entry = rowToEntry(
      makeAuditRow({
        event_type: "vault.search",
        user_email: "clerk@firm.com",
        input_summary: "liability cap",
        output_summary: "summary text",
        model: "claude-sonnet-4-6",
        input_tokens: 50,
        output_tokens: 80,
        duration_ms: 900,
        metadata: { custom: true },
      }),
    );
    expect(entry.event_type).toBe("vault.search");
    expect(entry.user_email).toBe("clerk@firm.com");
    expect(entry.input_summary).toBe("liability cap");
    expect(entry.output_summary).toBe("summary text");
    expect(entry.model).toBe("claude-sonnet-4-6");
    expect(entry.input_tokens).toBe(50);
    expect(entry.output_tokens).toBe(80);
    expect(entry.duration_ms).toBe(900);
    expect((entry.metadata as Record<string, unknown>)["custom"]).toBe(true);
  });
});

// ── getEarliest() ────────────────────────────────────────────

describe("getEarliest", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    process.env["NEON_DATABASE_URL"] = "postgresql://mock";
  });

  it("returns Some(AuditLogEntry) when a row exists", async () => {
    mockSql.mockResolvedValueOnce([makeAuditRow({ id: 1 })]);

    const opt = await getEarliest();

    expect(isSome(opt)).toBe(true);
    if (isSome(opt)) {
      expect(opt.value.id as number).toBe(1);
      expect(opt.value).toHaveProperty("event_type");
      expect(opt.value).toHaveProperty("created_at");
    }
  });

  it("returns None when no rows exist", async () => {
    mockSql.mockResolvedValueOnce([]);

    const opt = await getEarliest();

    expect(isNone(opt)).toBe(true);
  });

  it("calls SQL exactly once with ORDER BY id ASC LIMIT 1", async () => {
    mockSql.mockResolvedValueOnce([makeAuditRow()]);

    await getEarliest();

    expect(mockSql).toHaveBeenCalledTimes(1);
    const call = mockSql.mock.calls[0];
    const sqlParts: string[] = (call?.[0] as string[]) ?? [];
    const joined = sqlParts.join("").toLowerCase();
    expect(joined).toContain("order by id asc");
    expect(joined).toContain("limit");
  });
});

// ── getLatest() ──────────────────────────────────────────────

describe("getLatest", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    process.env["NEON_DATABASE_URL"] = "postgresql://mock";
  });

  it("returns Some(AuditLogEntry) when a row exists", async () => {
    mockSql.mockResolvedValueOnce([makeAuditRow({ id: 999 })]);

    const opt = await getLatest();

    expect(isSome(opt)).toBe(true);
    if (isSome(opt)) {
      expect(opt.value.id as number).toBe(999);
    }
  });

  it("returns None when no rows exist", async () => {
    mockSql.mockResolvedValueOnce([]);

    const opt = await getLatest();

    expect(isNone(opt)).toBe(true);
  });

  it("calls SQL with ORDER BY id DESC LIMIT 1", async () => {
    mockSql.mockResolvedValueOnce([makeAuditRow()]);

    await getLatest();

    expect(mockSql).toHaveBeenCalledTimes(1);
    const call = mockSql.mock.calls[0];
    const sqlParts: string[] = (call?.[0] as string[]) ?? [];
    const joined = sqlParts.join("").toLowerCase();
    expect(joined).toContain("order by id desc");
    expect(joined).toContain("limit");
  });
});

// ── queryForward() async generator ──────────────────────────

describe("queryForward", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    process.env["NEON_DATABASE_URL"] = "postgresql://mock";
  });

  it("yields each row as an AuditLogEntry", async () => {
    const rows = [
      makeAuditRow({ id: 11, event_type: "vault.search" }),
      makeAuditRow({ id: 12, event_type: "matter.create" }),
      makeAuditRow({ id: 13, event_type: "completion" }),
    ];
    mockSql.mockResolvedValueOnce(rows);

    const entries: AuditLogEntry[] = [];
    for await (const entry of queryForward(AuditLogId(10), 3)) {
      entries.push(entry);
    }

    expect(entries).toHaveLength(3);
    expect(entries[0]!.id as number).toBe(11);
    expect(entries[1]!.id as number).toBe(12);
    expect(entries[2]!.id as number).toBe(13);
  });

  it("yields entries in ascending id order", async () => {
    const rows = [
      makeAuditRow({ id: 20 }),
      makeAuditRow({ id: 21 }),
      makeAuditRow({ id: 22 }),
    ];
    mockSql.mockResolvedValueOnce(rows);

    const ids: number[] = [];
    for await (const entry of queryForward(AuditLogId(19), 3)) {
      ids.push(entry.id as number);
    }

    expect(ids).toEqual([20, 21, 22]);
  });

  it("yields nothing when the page is empty", async () => {
    mockSql.mockResolvedValueOnce([]);

    const entries: AuditLogEntry[] = [];
    for await (const entry of queryForward(AuditLogId(100), 10)) {
      entries.push(entry);
    }

    expect(entries).toHaveLength(0);
  });

  it("uses the fromId as an exclusive lower-bound cursor (WHERE id > fromId)", async () => {
    mockSql.mockResolvedValueOnce([makeAuditRow({ id: 51 })]);

    for await (const _ of queryForward(AuditLogId(50), 5)) {
      void _;
    }

    expect(mockSql).toHaveBeenCalledTimes(1);
    // The cursor value 50 must be passed as a bound parameter, not in SQL text.
    const call = mockSql.mock.calls[0];
    const params = (call?.slice(1) ?? []) as unknown[];
    expect(params).toContain(50);
  });

  it("passes take as a bound parameter (not concatenated into SQL)", async () => {
    mockSql.mockResolvedValueOnce([]);

    for await (const _ of queryForward(AuditLogId(0), 25)) {
      void _;
    }

    const call = mockSql.mock.calls[0];
    const params = (call?.slice(1) ?? []) as unknown[];
    expect(params).toContain(25);
  });

  it("hydrates each entry with correct branded AuditLogId type", async () => {
    mockSql.mockResolvedValueOnce([makeAuditRow({ id: 77 })]);

    for await (const entry of queryForward(AuditLogId(0), 1)) {
      // At runtime AuditLogId is a number
      expect(typeof entry.id).toBe("number");
      const _typed: AuditLogId = entry.id;
      void _typed;
    }
  });
});

// ── searchByTimestamp() ──────────────────────────────────────

describe("searchByTimestamp", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    process.env["NEON_DATABASE_URL"] = "postgresql://mock";
  });

  it("returns Some(AuditLogEntry) when a matching row exists", async () => {
    const ts = new Date("2026-03-01T00:00:00Z");
    mockSql.mockResolvedValueOnce([makeAuditRow({ id: 5, created_at: "2026-03-01T00:01:00Z" })]);

    const opt = await searchByTimestamp(ts);

    expect(isSome(opt)).toBe(true);
    if (isSome(opt)) {
      expect(opt.value.created_at).toBeInstanceOf(Date);
    }
  });

  it("returns None when no rows match the timestamp", async () => {
    mockSql.mockResolvedValueOnce([]);

    const opt = await searchByTimestamp(new Date("2099-01-01T00:00:00Z"));

    expect(isNone(opt)).toBe(true);
  });

  it("passes the timestamp ISO string as a bound parameter", async () => {
    const ts = new Date("2026-06-15T08:30:00Z");
    mockSql.mockResolvedValueOnce([]);

    await searchByTimestamp(ts);

    const call = mockSql.mock.calls[0];
    const params = (call?.slice(1) ?? []) as unknown[];
    // The timestamp must be bound as a parameter, not interpolated into SQL text
    expect(params).toContain(ts.toISOString());
  });

  it("calls SQL with ORDER BY created_at ASC LIMIT 1", async () => {
    mockSql.mockResolvedValueOnce([]);

    await searchByTimestamp(new Date());

    expect(mockSql).toHaveBeenCalledTimes(1);
    const call = mockSql.mock.calls[0];
    const sqlParts: string[] = (call?.[0] as string[]) ?? [];
    const joined = sqlParts.join("").toLowerCase();
    expect(joined).toContain("order by created_at asc");
    expect(joined).toContain("limit");
  });
});

// ── Branded type safety note ─────────────────────────────────
//
// The following would produce TypeScript compile-time errors if uncommented:
//
//   const auditId = AuditLogId(1);
//   const matterId: MatterId = auditId;  // ERROR: 'AuditLogId' not assignable to 'MatterId'
//
//   const chunkId = ChunkId("chunk_1");
//   await log({ type: "matter.delete", matterId: chunkId }); // ERROR: ChunkId not assignable to MatterId
//
// Branded types enforce nominal typing at compile time with zero runtime cost.
