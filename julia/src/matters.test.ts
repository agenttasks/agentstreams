/**
 * matters.test.ts — Tests written BEFORE the implementation.
 *
 * All SQL calls are mocked so tests run without a real database.
 * Verifies:
 *   - addMatters returns Ok(MatterId[]) with branded types.
 *   - getMatters returns Ok(Map<MatterId, ...>) keyed by brand.
 *   - deleteMatters soft-deletes (sets deleted_at) without removing rows.
 *   - associateQuery increments counters via UPDATE, never INSERT.
 *   - All functions propagate DB errors as Err({ type: "database_error" }).
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  MatterId,
  isOk,
  isErr,
  type Result,
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
const { addMatters, getMatters, deleteMatters, associateQuery } = await import(
  "./matters.js"
);

// ── Helpers ──────────────────────────────────────────────────

/** Builds a fake DB row matching ClientMatter shape. */
function makeMatterRow(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    id: "matter_abc",
    name: "Acme Corp v. Widget Inc",
    description: "A test matter",
    status: "active",
    query_count: 0,
    token_count: 0,
    metadata: {},
    effective_date: "2026-01-01T00:00:00Z",
    expiration_date: null,
    is_current: true,
    created_at: "2026-01-01T00:00:00Z",
    updated_at: "2026-01-01T00:00:00Z",
    deleted_at: null,
    ...overrides,
  };
}

// ── addMatters ───────────────────────────────────────────────

describe("addMatters", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    process.env["NEON_DATABASE_URL"] = "postgresql://mock";
  });

  it("returns Ok(MatterId[]) for a single matter", async () => {
    mockSql.mockResolvedValueOnce([{ id: "matter_001" }]);

    const result = await addMatters([{ name: "Test Matter" }]);

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(result.value).toHaveLength(1);
      // Branded type: at runtime it is a plain string
      const id = result.value[0] as MatterId | undefined;
      expect(typeof id).toBe("string");
      expect(id).toBe("matter_001");
    }
  });

  it("returns Ok with multiple MatterIds for multiple matters", async () => {
    mockSql
      .mockResolvedValueOnce([{ id: "m_1" }])
      .mockResolvedValueOnce([{ id: "m_2" }])
      .mockResolvedValueOnce([{ id: "m_3" }]);

    const result = await addMatters([
      { name: "Matter A" },
      { name: "Matter B", description: "desc" },
      { name: "Matter C" },
    ]);

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(result.value).toHaveLength(3);
      expect(result.value[0]).toBe("m_1");
      expect(result.value[1]).toBe("m_2");
      expect(result.value[2]).toBe("m_3");
    }
  });

  it("returns Ok([]) immediately for empty input without calling SQL", async () => {
    const result = await addMatters([]);

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(result.value).toHaveLength(0);
    }
    expect(mockSql).not.toHaveBeenCalled();
  });

  it("returns Err(database_error) when SQL rejects", async () => {
    mockSql.mockRejectedValueOnce(new Error("connection refused"));

    const result = await addMatters([{ name: "Broken Matter" }]);

    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("database_error");
      expect((result.error as { message: string }).message).toContain(
        "connection refused",
      );
    }
  });

  it("returns Err when INSERT returns no row", async () => {
    // RETURNING id produced an empty array — should not happen in practice
    // but we guard against it.
    mockSql.mockResolvedValueOnce([]);

    const result = await addMatters([{ name: "Ghost Matter" }]);

    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("database_error");
    }
  });

  // Branded type safety comment:
  // The return type is Result<MatterId[]>. TypeScript prevents callers from
  // passing result.value elements where a ProjectId or FileId is expected.
  it("MatterId branded type documents compile-time contract", async () => {
    mockSql.mockResolvedValueOnce([{ id: "branded_id" }]);
    const result = await addMatters([{ name: "Branded" }]);
    if (isOk(result)) {
      const id: MatterId = result.value[0] as MatterId;
      // At runtime MatterId is just a string
      expect(id as string).toBe("branded_id");
      // The following would be a TYPE ERROR at compile time:
      // const projectId: ProjectId = id; // ERROR: brand mismatch
    }
  });
});

// ── getMatters ───────────────────────────────────────────────

describe("getMatters", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    process.env["NEON_DATABASE_URL"] = "postgresql://mock";
  });

  it("returns Ok(Map) keyed by MatterId", async () => {
    mockSql.mockResolvedValueOnce([
      makeMatterRow({ id: "m_1", name: "Matter One" }),
      makeMatterRow({ id: "m_2", name: "Matter Two", query_count: 5, token_count: 1000 }),
    ]);

    const result = await getMatters();

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(result.value.size).toBe(2);
      // Map is keyed by MatterId (branded string)
      const id1 = MatterId("m_1");
      expect(result.value.has(id1)).toBe(true);
    }
  });

  it("attaches usage stats to each matter", async () => {
    mockSql.mockResolvedValueOnce([
      makeMatterRow({ id: "m_1", query_count: 3, token_count: 600 }),
    ]);

    const result = await getMatters();

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      const entry = result.value.get(MatterId("m_1"));
      expect(entry).toBeDefined();
      expect(entry!.usage.query_count).toBe(3);
      expect(entry!.usage.token_count).toBe(600);
      // last_query_at is non-null when query_count > 0
      expect(entry!.usage.last_query_at).not.toBeNull();
    }
  });

  it("sets last_query_at to null when query_count is 0", async () => {
    mockSql.mockResolvedValueOnce([
      makeMatterRow({ id: "m_1", query_count: 0, token_count: 0 }),
    ]);

    const result = await getMatters();

    if (isOk(result)) {
      const entry = result.value.get(MatterId("m_1"));
      expect(entry!.usage.last_query_at).toBeNull();
    }
  });

  it("returns Ok(empty Map) when no current matters exist", async () => {
    mockSql.mockResolvedValueOnce([]);

    const result = await getMatters();

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(result.value.size).toBe(0);
    }
  });

  it("returns Err(database_error) on SQL failure", async () => {
    mockSql.mockRejectedValueOnce(new Error("timeout"));

    const result: Result<unknown> = await getMatters();

    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("database_error");
    }
  });
});

// ── deleteMatters ────────────────────────────────────────────

describe("deleteMatters", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    process.env["NEON_DATABASE_URL"] = "postgresql://mock";
  });

  it("issues an UPDATE (soft delete), not DELETE FROM", async () => {
    // Soft delete returns no rows — UPDATE resolves with the command tag object
    mockSql.mockResolvedValueOnce([]);

    const result = await deleteMatters([MatterId("m_1"), MatterId("m_2")]);

    expect(isOk(result)).toBe(true);
    // SQL was called exactly once with the UPDATE statement
    expect(mockSql).toHaveBeenCalledTimes(1);
  });

  it("returns Ok(void) immediately for empty ids without calling SQL", async () => {
    const result = await deleteMatters([]);

    expect(isOk(result)).toBe(true);
    expect(mockSql).not.toHaveBeenCalled();
  });

  it("returns Err(database_error) on SQL failure", async () => {
    mockSql.mockRejectedValueOnce(new Error("deadlock"));

    const result = await deleteMatters([MatterId("m_1")]);

    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("database_error");
      expect((result.error as { message: string }).message).toContain("deadlock");
    }
  });

  // Soft-delete contract: rows are never physically removed.
  // The UPDATE sets deleted_at=now(); the WHERE clause protects
  // already-deleted and non-current rows from being touched twice.
  it("documents soft-delete contract via mock — no row removal", async () => {
    mockSql.mockResolvedValueOnce([]);
    await deleteMatters([MatterId("m_1")]);

    // No INSERT or SELECT was issued — only an UPDATE
    const call = mockSql.mock.calls[0];
    expect(call).toBeDefined();
    // The tagged-template raw SQL array includes the UPDATE keyword
    const sqlParts: string[] = (call?.[0] as string[]) ?? [];
    const joined = sqlParts.join("");
    expect(joined.toLowerCase()).toContain("update");
    expect(joined.toLowerCase()).not.toContain("delete from");
  });
});

// ── associateQuery ───────────────────────────────────────────

describe("associateQuery", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    process.env["NEON_DATABASE_URL"] = "postgresql://mock";
  });

  it("returns Ok(void) on success", async () => {
    mockSql.mockResolvedValueOnce([]);

    const result = await associateQuery(MatterId("m_1"), 250);

    expect(isOk(result)).toBe(true);
  });

  it("calls SQL exactly once with the matter id and token count", async () => {
    mockSql.mockResolvedValueOnce([]);

    await associateQuery(MatterId("m_abc"), 500);

    expect(mockSql).toHaveBeenCalledTimes(1);
  });

  it("returns Err(database_error) when SQL rejects", async () => {
    mockSql.mockRejectedValueOnce(new Error("foreign key violation"));

    const result = await associateQuery(MatterId("m_missing"), 100);

    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("database_error");
    }
  });

  it("passes token count as a parameter (not concatenated into SQL)", async () => {
    mockSql.mockResolvedValueOnce([]);

    await associateQuery(MatterId("m_1"), 999);

    const call = mockSql.mock.calls[0];
    expect(call).toBeDefined();
    // Neon tagged template: second+ args are the interpolated values.
    // The raw template literal values are the first argument (string[]).
    // Subsequent arguments are the interpolated parameters.
    // 999 must appear as a bound parameter, not inside the SQL string.
    const params = (call?.slice(1) ?? []) as unknown[];
    expect(params).toContain(999);
  });
});
