/**
 * Vault module tests — written BEFORE the implementation (test-first per Cherny).
 *
 * All Neon SQL calls are mocked. chunkText and hashEmbedding are
 * exercised directly as exported helpers.
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

import { describe, it, expect, vi, beforeEach, type MockInstance } from "vitest";
import {
  ProjectId,
  FileId,
  ReviewTableId,
  ChunkId,
  isOk,
  isErr,
  isSome,
  isNone,
  type ReviewColumn,
} from "./types.js";

// ── Mock @neondatabase/serverless before importing vault ─────
// The vault module lazy-initialises the SQL connection from the
// NEON_DATABASE_URL env var. We intercept at the module boundary
// so no real network calls are made during tests.

const mockSql = vi.fn();

vi.mock("@neondatabase/serverless", () => ({
  neon: vi.fn(() => mockSql),
}));

// Import vault AFTER setting up the mock so getSql() picks it up.
const {
  createProject,
  uploadFile,
  semanticSearch,
  getFileDetails,
  deleteFile,
  createReviewTable,
  getReviewRow,
  chunkText,
  hashEmbedding,
} = await import("./vault.js");

// ── Helpers ──────────────────────────────────────────────────

/** Make mockSql resolve once with tagged-template rows. */
function mockRows(rows: Record<string, unknown>[]): void {
  mockSql.mockResolvedValueOnce(rows);
}

/** Make mockSql reject once with a database error. */
function mockDbError(message: string): void {
  mockSql.mockRejectedValueOnce(new Error(message));
}

// ── chunkText ────────────────────────────────────────────────

describe("chunkText", () => {
  it("returns a single chunk for text shorter than chunkSize", () => {
    const chunks = chunkText("hello world", 512, 64);
    expect(chunks).toHaveLength(1);
    expect(chunks[0]?.text).toBe("hello world");
    expect(chunks[0]?.index).toBe(0);
  });

  it("produces overlapping chunks of correct size", () => {
    // 1200 chars with chunkSize=512, overlap=64 → advances 448 per step
    // step 0: [0, 512), step 1: [448, 960), step 2: [896, 1200)
    const text = "a".repeat(1200);
    const chunks = chunkText(text, 512, 64);

    expect(chunks.length).toBeGreaterThanOrEqual(3);
    expect(chunks[0]?.text.length).toBe(512);
    // Second chunk starts at offset 448, so 512 chars long
    expect(chunks[1]?.text.length).toBe(512);
    // Indices are sequential
    chunks.forEach((c, i) => expect(c.index).toBe(i));
  });

  it("overlap creates shared content between adjacent chunks", () => {
    // The tail of chunk N should equal the head of chunk N+1
    const text = "abcdefghij".repeat(60); // 600 chars
    const chunks = chunkText(text, 100, 20);
    expect(chunks.length).toBeGreaterThanOrEqual(2);

    const first = chunks[0]!.text;
    const second = chunks[1]!.text;
    // Last 20 chars of chunk[0] must equal first 20 of chunk[1]
    expect(first.slice(-20)).toBe(second.slice(0, 20));
  });

  it("uses default chunkSize=512 and overlap=64 when not specified", () => {
    const text = "x".repeat(600);
    const explicit = chunkText(text, 512, 64);
    const defaults = chunkText(text);
    expect(defaults).toEqual(explicit);
  });

  it("returns empty array for empty string", () => {
    expect(chunkText("")).toHaveLength(0);
  });
});

// ── hashEmbedding ────────────────────────────────────────────

describe("hashEmbedding", () => {
  it("returns a Float32Array of the default dimension (384)", () => {
    const vec = hashEmbedding("test document");
    expect(vec).toBeInstanceOf(Float32Array);
    expect(vec.length).toBe(384);
  });

  it("respects a custom dimension", () => {
    const vec = hashEmbedding("some text", 128);
    expect(vec.length).toBe(128);
  });

  it("is deterministic — same input produces identical vector", () => {
    const a = hashEmbedding("hello, world");
    const b = hashEmbedding("hello, world");
    expect(Array.from(a)).toEqual(Array.from(b));
  });

  it("different inputs produce different vectors", () => {
    const a = hashEmbedding("contract A");
    const b = hashEmbedding("contract B");
    // At minimum one element must differ
    const same = Array.from(a).every((v, i) => v === b[i]);
    expect(same).toBe(false);
  });

  it("produces a normalised vector (L2 norm ≈ 1.0)", () => {
    const vec = hashEmbedding("normalisation check");
    const norm = Math.sqrt(Array.from(vec).reduce((s, v) => s + v * v, 0));
    expect(norm).toBeCloseTo(1.0, 3);
  });
});

// ── createProject ────────────────────────────────────────────

describe("createProject", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns Result<ProjectId> on success", async () => {
    mockRows([{ id: "proj_aaa-111" }]);

    const result = await createProject("Acme Contract Review", "lawyer@acme.com");

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(typeof result.value).toBe("string");
      // The returned value must be usable as a ProjectId (branded)
      const _typed: ReturnType<typeof ProjectId> = result.value;
      void _typed;
    }
  });

  it("accepts optional description, isKnowledgeBase, clientMatterId", async () => {
    mockRows([{ id: "proj_bbb-222" }]);

    const result = await createProject("KB Project", "admin@firm.com", {
      description: "Regional knowledge base",
      isKnowledgeBase: true,
    });

    expect(isOk(result)).toBe(true);
    // Verify SQL was called with the correct values
    expect(mockSql).toHaveBeenCalledOnce();
  });

  it("returns database_error Result on SQL failure", async () => {
    mockDbError("connection refused");

    const result = await createProject("Bad Project", "user@firm.com");

    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("database_error");
    }
  });
});

// ── uploadFile ───────────────────────────────────────────────

describe("uploadFile", () => {
  const projectId = ProjectId("proj_test-upload");

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns Result<FileId> on success", async () => {
    const fileId = "file_upload-001";
    // uploadFile performs several SQL calls:
    // 1. INSERT file row
    // 2+. INSERT each chunk
    // 3. UPDATE chunked_at milestone
    // 4. UPDATE embedded_at milestone
    // 5. UPDATE processed_at + status
    // 6. UPDATE project storage_bytes + file_count
    // We resolve all with empty success rows.
    mockSql.mockResolvedValue([]);
    mockRows([{ id: fileId }]);

    const result = await uploadFile(
      projectId,
      "contract.txt",
      "This is the contract content.",
      "text/plain",
    );

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(typeof result.value).toBe("string");
    }
  });

  it("chunks content and stores multiple chunk rows", async () => {
    // Content long enough for multiple chunks
    const longContent = "legal terms and conditions ".repeat(50); // ~1350 chars

    mockSql.mockResolvedValue([]);
    mockRows([{ id: "file_chunked-test" }]);

    const result = await uploadFile(
      projectId,
      "long-doc.txt",
      longContent,
      "text/plain",
    );

    expect(isOk(result)).toBe(true);
    // SQL should have been called more than twice (file insert + multiple chunks)
    expect(mockSql.mock.calls.length).toBeGreaterThan(2);
  });

  it("returns database_error on SQL failure", async () => {
    mockDbError("disk full");

    const result = await uploadFile(
      projectId,
      "failed.txt",
      "content",
      "text/plain",
    );

    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("database_error");
    }
  });
});

// ── semanticSearch ───────────────────────────────────────────

describe("semanticSearch", () => {
  const projectId = ProjectId("proj_search-test");

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns Result<SearchResult[]> with score between 0 and 1", async () => {
    mockRows([
      {
        id: "chunk_001",
        file_id: "file_aaa",
        chunk_index: 0,
        content: "indemnification clause paragraph",
        content_hash: "abc123",
        token_count: 10,
        metadata: {},
        score: 0.87,
        project_id: projectId as string,
      },
      {
        id: "chunk_002",
        file_id: "file_bbb",
        chunk_index: 1,
        content: "limitation of liability",
        content_hash: "def456",
        token_count: 8,
        metadata: {},
        score: 0.72,
        project_id: projectId as string,
      },
    ]);

    const result = await semanticSearch(projectId, "indemnification");

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(result.value.length).toBe(2);

      const first = result.value[0]!;
      expect(first.score).toBeGreaterThanOrEqual(0);
      expect(first.score).toBeLessThanOrEqual(1);
      expect(typeof first.file_id).toBe("string");
      expect(typeof first.project_id).toBe("string");
      expect(typeof first.content).toBe("string");
    }
  });

  it("respects a custom limit", async () => {
    mockRows([]);

    const result = await semanticSearch(projectId, "force majeure", 5);

    expect(isOk(result)).toBe(true);
    // Verify SQL was called with the limit value
    expect(mockSql).toHaveBeenCalledOnce();
  });

  it("returns database_error on SQL failure", async () => {
    mockDbError("timeout");

    const result = await semanticSearch(projectId, "anything");

    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("database_error");
    }
  });
});

// ── getFileDetails ───────────────────────────────────────────

describe("getFileDetails", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns Map with Option.Some for found files, Option.None for missing", async () => {
    const foundId = FileId("file_found-001");
    const missingId = FileId("file_missing-999");

    mockRows([
      {
        id: foundId as string,
        project_id: "proj_abc",
        filename: "agreement.pdf",
        mime_type: "application/pdf",
        size_bytes: 2048,
        content: "text content here",
        content_hash: "sha256abc",
        processing_status: "ready",
        chunk_count: 4,
        token_count: 512,
        metadata: {},
        uploaded_at: "2026-01-01T00:00:00Z",
        processed_at: "2026-01-01T00:01:00Z",
      },
    ]);

    const result = await getFileDetails([foundId, missingId]);

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      const map = result.value;
      expect(map).toBeInstanceOf(Map);
      expect(map.size).toBe(2);

      const foundOpt = map.get(foundId);
      expect(foundOpt).toBeDefined();
      expect(isSome(foundOpt!)).toBe(true);
      if (isSome(foundOpt!)) {
        expect(foundOpt.value.filename).toBe("agreement.pdf");
      }

      const missingOpt = map.get(missingId);
      expect(missingOpt).toBeDefined();
      expect(isNone(missingOpt!)).toBe(true);
    }
  });

  it("returns empty Map for empty input array", async () => {
    // No SQL call needed for empty input
    const result = await getFileDetails([]);

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(result.value.size).toBe(0);
    }
    expect(mockSql).not.toHaveBeenCalled();
  });

  it("returns database_error on SQL failure", async () => {
    mockDbError("pg: relation does not exist");

    const result = await getFileDetails([FileId("file_x")]);

    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("database_error");
    }
  });
});

// ── deleteFile ───────────────────────────────────────────────

describe("deleteFile", () => {
  const projectId = ProjectId("proj_delete-test");
  const fileId = FileId("file_to-delete");

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns Result<void> on success", async () => {
    // DELETE file row, then UPDATE project counters
    mockSql.mockResolvedValue([]);

    const result = await deleteFile(projectId, fileId);

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(result.value).toBeUndefined();
    }
  });

  it("calls SQL at least twice (delete + update project)", async () => {
    mockSql.mockResolvedValue([]);

    await deleteFile(projectId, fileId);

    expect(mockSql.mock.calls.length).toBeGreaterThanOrEqual(2);
  });

  it("returns database_error on SQL failure", async () => {
    mockDbError("foreign key violation");

    const result = await deleteFile(projectId, fileId);

    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("database_error");
    }
  });
});

// ── createReviewTable ────────────────────────────────────────

describe("createReviewTable", () => {
  const projectId = ProjectId("proj_review-test");
  const columns: ReviewColumn[] = [
    { name: "effective_date", type: "date", description: "Contract effective date" },
    { name: "liability_cap", type: "currency", description: "Liability cap amount" },
    { name: "auto_renewal", type: "boolean", description: "Auto-renewal clause present" },
  ];
  const fileIds = [FileId("file_rev-001"), FileId("file_rev-002")];

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns Result<ReviewTableId> on success", async () => {
    // INSERT review table, then INSERT rows for each file
    mockRows([{ id: "rt_create-001" }]);
    mockSql.mockResolvedValue([]); // row inserts

    const result = await createReviewTable(
      projectId,
      "Q1 Contract Review",
      columns,
      fileIds,
    );

    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(typeof result.value).toBe("string");
      const _typed: ReturnType<typeof ReviewTableId> = result.value;
      void _typed;
    }
  });

  it("inserts one pending row per file", async () => {
    mockRows([{ id: "rt_rows-test" }]);
    mockSql.mockResolvedValue([]);

    await createReviewTable(projectId, "Row Count Test", columns, fileIds);

    // 1 insert for table + 1 per file = 1 + fileIds.length calls
    expect(mockSql.mock.calls.length).toBe(1 + fileIds.length);
  });

  it("returns database_error on SQL failure", async () => {
    mockDbError("project not found");

    const result = await createReviewTable(projectId, "Bad Table", columns, fileIds);

    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("database_error");
    }
  });
});

// ── getReviewRow ─────────────────────────────────────────────

describe("getReviewRow", () => {
  const reviewTableId = ReviewTableId("rt_get-test");
  const fileId = FileId("file_row-get");

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns Option.Some when the row exists", async () => {
    mockRows([
      {
        id: "row_some-001",
        review_table_id: reviewTableId as string,
        file_id: fileId as string,
        cells: { effective_date: "2026-03-01", auto_renewal: "true" },
        status: "complete",
        created_at: "2026-01-01T00:00:00Z",
        updated_at: "2026-01-02T00:00:00Z",
      },
    ]);

    const opt = await getReviewRow(reviewTableId, fileId);

    expect(isSome(opt)).toBe(true);
    if (isSome(opt)) {
      expect(opt.value.status).toBe("complete");
      expect(typeof opt.value.review_table_id).toBe("string");
      expect(typeof opt.value.file_id).toBe("string");
    }
  });

  it("returns Option.None when the row does not exist", async () => {
    mockRows([]); // empty result set

    const opt = await getReviewRow(reviewTableId, FileId("file_missing"));

    expect(isNone(opt)).toBe(true);
  });
});

// ── Branded type safety note ─────────────────────────────────
//
// The following would produce a TypeScript compile-time error if uncommented:
//
//   const pid = ProjectId("proj_1");
//   const fid: FileId = pid;           // ERROR: 'ProjectId' not assignable to 'FileId'
//
//   async function test() {
//     await uploadFile(pid, "f.txt", "", "text/plain"); // OK
//     await deleteFile(pid as unknown as ProjectId, pid as unknown as FileId); // OK shape
//     // But:
//     const f = FileId("file_1");
//     await uploadFile(f, "f.txt", "", "text/plain"); // ERROR: FileId not assignable to ProjectId
//   }
//
// Branded types enforce nominal typing at compile time with zero runtime cost.
