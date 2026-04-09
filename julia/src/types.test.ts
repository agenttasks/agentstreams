/**
 * Type foundation tests — written BEFORE any implementation.
 *
 * Tests branded type safety, Option/Result narrowing, companion
 * objects, and discriminated union exhaustiveness.
 */

import { describe, it, expect } from "vitest";
import {
  ProjectId,
  FileId,
  MatterId,
  ChunkId,
  ReviewTableId,
  AuditLogId,
  Some,
  None,
  isSome,
  isNone,
  flatMap,
  getOrElse,
  Ok,
  Err,
  isOk,
  isErr,
  VaultProject,
  ClientMatter,
  isProcessingComplete,
  assertNever,
  LEGAL_SKILLS,
  type Option,
  type Result,
  type VaultError,
  type JuliaEvent,
  type VaultFile,
  type ProcessingStatus,
} from "./types.js";

// ── Branded Type Tests ───────────────────────────────────────

describe("branded types", () => {
  it("ProjectId wraps a string", () => {
    const id = ProjectId("proj_123");
    // At runtime it's just a string
    expect(typeof id).toBe("string");
    expect(id as string).toBe("proj_123");
  });

  it("FileId wraps a string", () => {
    const id = FileId("file_456");
    expect(typeof id).toBe("string");
  });

  it("MatterId wraps a string", () => {
    const id = MatterId("matter_789");
    expect(typeof id).toBe("string");
  });

  it("AuditLogId wraps a number", () => {
    const id = AuditLogId(42);
    expect(typeof id).toBe("number");
    expect(id as number).toBe(42);
  });

  // Type-level test: the following would cause a compile error if uncommented.
  // This documents the branded type safety contract.
  //
  // const projectId = ProjectId("proj_1");
  // const fileId: FileId = projectId;  // ERROR: Type 'ProjectId' is not assignable to type 'FileId'
  //
  // function takesFileId(_id: FileId): void {}
  // takesFileId(projectId);  // ERROR: Argument of type 'ProjectId' is not assignable to parameter of type 'FileId'
});

// ── Option Type Tests ────────────────────────────────────────

describe("Option<T>", () => {
  it("Some wraps a value", () => {
    const opt = Some(42);
    expect(opt._tag).toBe("Some");
    expect(isSome(opt)).toBe(true);
    expect(isNone(opt)).toBe(false);
    if (isSome(opt)) {
      expect(opt.value).toBe(42);
    }
  });

  it("None represents absence", () => {
    const opt: Option<number> = None;
    expect(opt._tag).toBe("None");
    expect(isSome(opt)).toBe(false);
    expect(isNone(opt)).toBe(true);
  });

  it("flatMap chains over Some", () => {
    const opt = Some(10);
    const doubled = flatMap(opt, (n) => Some(n * 2));
    expect(isSome(doubled) && doubled.value).toBe(20);
  });

  it("flatMap short-circuits on None", () => {
    const opt: Option<number> = None;
    const result = flatMap(opt, (n) => Some(n * 2));
    expect(isNone(result)).toBe(true);
  });

  it("getOrElse returns value for Some", () => {
    expect(getOrElse(Some("hello"), "default")).toBe("hello");
  });

  it("getOrElse returns fallback for None", () => {
    expect(getOrElse(None, "default")).toBe("default");
  });
});

// ── Result Type Tests ────────────────────────────────────────

describe("Result<T>", () => {
  it("Ok wraps a success value", () => {
    const result = Ok(ProjectId("proj_1"));
    expect(result.ok).toBe(true);
    expect(isOk(result)).toBe(true);
    if (isOk(result)) {
      expect(typeof result.value).toBe("string");
    }
  });

  it("Err wraps a typed error", () => {
    const result: Result<string> = Err({
      type: "not_found",
      entity: "project",
      id: "proj_missing",
    });
    expect(result.ok).toBe(false);
    expect(isErr(result)).toBe(true);
    if (isErr(result)) {
      expect(result.error.type).toBe("not_found");
    }
  });

  it("VaultError discriminated union covers all cases", () => {
    const errors: VaultError[] = [
      { type: "not_found", entity: "file", id: "f1" },
      { type: "permission_denied", user: "user@test.com", action: "delete" },
      { type: "processing_failed", fileId: FileId("f1"), reason: "timeout" },
      { type: "quota_exceeded", current: 100, limit: 50 },
      { type: "invalid_input", field: "name", message: "too long" },
      { type: "database_error", message: "connection refused" },
    ];

    // All 6 error types should be representable
    expect(errors).toHaveLength(6);

    // Exhaustive switch should handle all
    for (const err of errors) {
      switch (err.type) {
        case "not_found":
        case "permission_denied":
        case "processing_failed":
        case "quota_exceeded":
        case "invalid_input":
        case "database_error":
          break;
        default: {
          const _exhaustive: never = err;
          void _exhaustive;
        }
      }
    }
  });
});

// ── Companion Object Tests ───────────────────────────────────

describe("VaultProject companion", () => {
  it("create() produces a VaultProject with generated ID", () => {
    const project = VaultProject.create("Test Project", "user@test.com");
    expect(project.name).toBe("Test Project");
    expect(project.owner_email).toBe("user@test.com");
    expect(typeof project.id).toBe("string");
    expect(project.file_count).toBe(0);
    expect(project.archived_at).toBeNull();
  });

  it("fromRow() hydrates from database row", () => {
    const row = {
      id: "proj_abc",
      name: "From DB",
      description: "desc",
      is_knowledge_base: true,
      owner_email: "admin@test.com",
      storage_bytes: 1024,
      file_count: 5,
      client_matter_id: "matter_xyz",
      metadata: { key: "val" },
      created_at: "2026-01-01T00:00:00Z",
      updated_at: "2026-01-02T00:00:00Z",
      archived_at: null,
    };
    const project = VaultProject.fromRow(row);
    expect(project.name).toBe("From DB");
    expect(project.is_knowledge_base).toBe(true);
    expect(project.file_count).toBe(5);
  });
});

describe("ClientMatter companion", () => {
  it("create() produces an active SCD2 matter", () => {
    const matter = ClientMatter.create("Acme Corp v. Widget Inc");
    expect(matter.status).toBe("active");
    expect(matter.is_current).toBe(true);
    expect(matter.expiration_date).toBeNull();
    expect(matter.query_count).toBe(0);
  });
});

// ── Type Guard Tests ─────────────────────────────────────────

describe("type guards", () => {
  it("isProcessingComplete narrows to ready status", () => {
    const file = {
      processing_status: "ready" as ProcessingStatus,
    } as VaultFile;

    if (isProcessingComplete(file)) {
      // TypeScript narrows: file.processing_status is "ready"
      expect(file.processing_status).toBe("ready");
    }
  });

  it("isProcessingComplete returns false for pending", () => {
    const file = {
      processing_status: "pending" as ProcessingStatus,
    } as VaultFile;
    expect(isProcessingComplete(file)).toBe(false);
  });
});

// ── Event Union Tests ────────────────────────────────────────

describe("JuliaEvent discriminated union", () => {
  it("handles all event types exhaustively", () => {
    const events: JuliaEvent[] = [
      { type: "vault.create_project", projectId: ProjectId("p1"), name: "Test" },
      { type: "vault.upload", projectId: ProjectId("p1"), fileId: FileId("f1"), filename: "contract.pdf" },
      { type: "vault.search", projectId: ProjectId("p1"), query: "indemnification" },
      { type: "vault.delete_file", projectId: ProjectId("p1"), fileId: FileId("f1") },
      { type: "vault.create_review_table", projectId: ProjectId("p1"), reviewTableId: ReviewTableId("rt1") },
      { type: "matter.create", matterId: MatterId("m1"), name: "Case 1" },
      { type: "matter.delete", matterId: MatterId("m1") },
      { type: "matter.associate_query", matterId: MatterId("m1"), tokens: 500 },
      { type: "completion", query: "review NDA", model: "claude-opus-4-6", matterId: null, projectIds: [], input_tokens: 100, output_tokens: 200, duration_ms: 1500 },
      { type: "assistant.session", sessionId: "sess_1", skill: "review-contract", matterId: null },
    ];

    // All 10 event types
    const types = events.map((e) => e.type);
    expect(types).toContain("vault.create_project");
    expect(types).toContain("completion");
    expect(types).toContain("assistant.session");

    // Exhaustive handling
    for (const event of events) {
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
  });
});

// ── Legal Skills ─────────────────────────────────────────────

describe("LEGAL_SKILLS", () => {
  it("contains all 9 skills from vendored legal plugin", () => {
    expect(LEGAL_SKILLS).toHaveLength(9);
    expect(LEGAL_SKILLS).toContain("review-contract");
    expect(LEGAL_SKILLS).toContain("triage-nda");
    expect(LEGAL_SKILLS).toContain("compliance-check");
  });
});

// ── assertNever ──────────────────────────────────────────────

describe("assertNever", () => {
  it("throws on any value", () => {
    expect(() => assertNever("unexpected" as never)).toThrow(
      "Unexpected value",
    );
  });
});
