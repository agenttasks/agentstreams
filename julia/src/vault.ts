/**
 * vault.ts — Document storage, semantic search, and review tables.
 *
 * Uses Neon Postgres (SQL-over-HTTP) for persistence and pgvector for
 * cosine-similarity search over 384-dim pseudo-embeddings.
 *
 * All public functions return Result<T> or Option<T> (Cherny Ch.7 p.183/185).
 * Branded types (Cherny Ch.6 p.172) are used for all entity IDs.
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 *
 * TODO: Replace hashEmbedding() with real sentence-transformer embeddings
 *       (e.g. all-MiniLM-L6-v2 via @xenova/transformers) before production use.
 *       The pseudo-embeddings here are deterministic but not semantically meaningful.
 *
 * TODO: completion.ts currently calls semanticSearch(pid, query, { limit: 5 })
 *       with an object argument. That call site must be updated to pass a plain
 *       number: semanticSearch(pid, query, 5) to match this signature.
 */

import { createHash } from "node:crypto";
import { neon, type NeonQueryFunction } from "@neondatabase/serverless";
import {
  Ok,
  Err,
  Some,
  None,
  ProjectId,
  FileId,
  ChunkId,
  ReviewTableId,
  VaultFile,
  type Result,
  type Option,
  type MatterId,
  type ReviewColumn,
  type ReviewTableId as ReviewTableIdType,
  type VaultFile as VaultFileType,
  type ReviewRow,
  type SearchResult,
} from "./types.js";

// ── Lazy SQL connection ───────────────────────────────────────

let _sql: NeonQueryFunction<false, false> | null = null;

/**
 * Returns a cached Neon SQL function constructed from NEON_DATABASE_URL.
 * Initialised once on first call (lazy singleton).
 * Throws if the environment variable is not set.
 */
function getSql(): NeonQueryFunction<false, false> {
  if (_sql === null) {
    const url = process.env["NEON_DATABASE_URL"];
    if (!url) {
      throw new Error("NEON_DATABASE_URL is not set");
    }
    _sql = neon(url);
  }
  return _sql;
}

// ── Helper: overlapping text chunker ─────────────────────────

/**
 * Split `text` into overlapping chunks of `chunkSize` characters,
 * advancing by `(chunkSize - overlap)` characters per step.
 *
 * Returns an empty array for empty input.
 *
 * @param text      - Source text to chunk.
 * @param chunkSize - Maximum characters per chunk (default 512).
 * @param overlap   - Characters shared between adjacent chunks (default 64).
 * @returns Array of `{ text, index }` in order, indices starting at 0.
 */
export function chunkText(
  text: string,
  chunkSize: number = 512,
  overlap: number = 64,
): Array<{ text: string; index: number }> {
  if (text.length === 0) {
    return [];
  }

  const step = chunkSize - overlap;
  const chunks: Array<{ text: string; index: number }> = [];

  let pos = 0;
  let index = 0;

  while (pos < text.length) {
    chunks.push({ text: text.slice(pos, pos + chunkSize), index });
    pos += step;
    index += 1;
  }

  return chunks;
}

// ── Helper: SHA-512 based pseudo-embedding ────────────────────

/**
 * Derive a deterministic, L2-normalised pseudo-embedding vector from `text`
 * using SHA-512 as a pseudo-random number generator.
 *
 * Algorithm:
 *   1. Hash `text` with SHA-512 to get 64 seed bytes.
 *   2. Repeatedly hash the previous digest to produce additional 64-byte
 *      blocks until `dim` float values have been filled.
 *   3. Each byte pair is converted to a signed value in [-1, 1].
 *   4. The resulting vector is L2-normalised to unit length.
 *
 * This is deterministic — identical inputs always yield identical vectors.
 * It is NOT semantically meaningful; replace with a real embedding model
 * before relying on search quality.
 *
 * @param text - Input string to embed.
 * @param dim  - Output dimension (default 384).
 * @returns Normalised Float32Array of length `dim`.
 */
export function hashEmbedding(text: string, dim: number = 384): Float32Array {
  const vec = new Float32Array(dim);

  // Seed: SHA-512 of the input text
  let currentHash = createHash("sha512").update(text, "utf8").digest();

  let filled = 0;
  while (filled < dim) {
    // Each 64-byte block gives us 32 float values (using 2 bytes each)
    for (let i = 0; i + 1 < currentHash.length && filled < dim; i += 2) {
      // Combine two bytes into a signed value, normalise to [-1, 1]
      const hi = currentHash[i] ?? 0;
      const lo = currentHash[i + 1] ?? 0;
      const raw = ((hi << 8) | lo) - 32768; // signed int16, range [-32768, 32767]
      vec[filled] = raw / 32768;
      filled += 1;
    }

    // Extend by hashing the current digest for the next block
    if (filled < dim) {
      currentHash = createHash("sha512").update(currentHash).digest();
    }
  }

  // L2 normalise
  let norm = 0;
  for (let i = 0; i < dim; i++) {
    const v = vec[i] ?? 0;
    norm += v * v;
  }
  norm = Math.sqrt(norm);

  if (norm > 0) {
    for (let i = 0; i < dim; i++) {
      vec[i] = (vec[i] ?? 0) / norm;
    }
  }

  return vec;
}

// ── Public API ────────────────────────────────────────────────

/**
 * Create a new vault project in `julia_vault_projects`.
 *
 * @param name         - Human-readable project name.
 * @param ownerEmail   - Email address of the project owner.
 * @param opts         - Optional description, knowledge-base flag, and matter ID.
 * @returns Ok(ProjectId) on success, Err on database failure.
 */
export async function createProject(
  name: string,
  ownerEmail: string,
  opts?: {
    description?: string;
    isKnowledgeBase?: boolean;
    clientMatterId?: MatterId;
  },
): Promise<Result<ReturnType<typeof ProjectId>>> {
  try {
    const sql = getSql();
    const description = opts?.description ?? "";
    const isKnowledgeBase = opts?.isKnowledgeBase ?? false;
    const clientMatterId = opts?.clientMatterId ?? null;

    const rows = await sql`
      INSERT INTO julia_vault_projects
        (name, description, is_knowledge_base, owner_email,
         storage_bytes, file_count, client_matter_id,
         metadata, created_at, updated_at)
      VALUES
        (${name},
         ${description},
         ${isKnowledgeBase},
         ${ownerEmail},
         0,
         0,
         ${clientMatterId as string | null},
         '{}',
         now(),
         now())
      RETURNING id
    `;

    const row = rows[0];
    if (!row) {
      return Err({ type: "database_error", message: "INSERT returned no row" });
    }

    return Ok(ProjectId(row["id"] as string));
  } catch (err) {
    return Err({
      type: "database_error",
      message: err instanceof Error ? err.message : String(err),
    });
  }
}

/**
 * Upload a file into a vault project.
 *
 * Steps:
 *   1. INSERT the file row into `julia_vault_files`.
 *   2. Chunk the content (512 chars, 64 overlap).
 *   3. Hash each chunk with SHA-256 for `content_hash`.
 *   4. Compute 384-dim pseudo-embeddings via hashEmbedding().
 *   5. INSERT each chunk into `julia_vault_file_chunks`.
 *   6. UPDATE file milestones: chunked_at → embedded_at → processed_at.
 *   7. UPDATE project `storage_bytes` and `file_count`.
 *
 * @param projectId - Target project.
 * @param filename  - Original filename.
 * @param content   - UTF-8 text content.
 * @param mimeType  - MIME type string (e.g. "text/plain").
 * @returns Ok(FileId) on success, Err on database failure.
 */
export async function uploadFile(
  projectId: ReturnType<typeof ProjectId>,
  filename: string,
  content: string,
  mimeType: string,
): Promise<Result<ReturnType<typeof FileId>>> {
  try {
    const sql = getSql();

    // 1. Compute file-level content hash
    const fileHash = createHash("sha256").update(content, "utf8").digest("hex");
    const sizeBytes = Buffer.byteLength(content, "utf8");

    // 2. INSERT file row
    const fileRows = await sql`
      INSERT INTO julia_vault_files
        (project_id, filename, mime_type, size_bytes, content,
         content_hash, processing_status, chunk_count, token_count,
         metadata, uploaded_at)
      VALUES
        (${projectId as string},
         ${filename},
         ${mimeType},
         ${sizeBytes},
         ${content},
         ${fileHash},
         'processing',
         0,
         0,
         '{}',
         now())
      RETURNING id
    `;

    const fileRow = fileRows[0];
    if (!fileRow) {
      return Err({ type: "database_error", message: "File INSERT returned no row" });
    }

    const fileId = FileId(fileRow["id"] as string);

    // 3. Chunk the content
    const chunks = chunkText(content);

    // 4. INSERT each chunk with its embedding
    for (const chunk of chunks) {
      const chunkHash = createHash("sha256").update(chunk.text, "utf8").digest("hex");
      const embedding = hashEmbedding(chunk.text);
      // pgvector expects a bracketed float list: '[0.1, 0.2, ...]'
      const embeddingLiteral = `[${Array.from(embedding).join(",")}]`;

      await sql`
        INSERT INTO julia_vault_file_chunks
          (file_id, chunk_index, content, content_hash,
           token_count, metadata, embedding)
        VALUES
          (${fileId as string},
           ${chunk.index},
           ${chunk.text},
           ${chunkHash},
           0,
           '{}',
           ${embeddingLiteral}::vector)
      `;
    }

    // 5. Update chunked_at milestone
    await sql`
      UPDATE julia_vault_files
      SET    chunked_at  = now(),
             chunk_count = ${chunks.length},
             updated_at  = now()
      WHERE  id = ${fileId as string}
    `;

    // 6. Update embedded_at milestone
    await sql`
      UPDATE julia_vault_files
      SET    embedded_at = now(),
             updated_at  = now()
      WHERE  id = ${fileId as string}
    `;

    // 7. Update processed_at + status
    await sql`
      UPDATE julia_vault_files
      SET    processed_at      = now(),
             processing_status = 'ready',
             updated_at        = now()
      WHERE  id = ${fileId as string}
    `;

    // 8. Update project storage_bytes and file_count
    await sql`
      UPDATE julia_vault_projects
      SET    storage_bytes = storage_bytes + ${sizeBytes},
             file_count    = file_count + 1,
             updated_at    = now()
      WHERE  id = ${projectId as string}
    `;

    return Ok(fileId);
  } catch (err) {
    return Err({
      type: "database_error",
      message: err instanceof Error ? err.message : String(err),
    });
  }
}

/**
 * Semantic search over chunks belonging to a project using pgvector cosine
 * distance.
 *
 * The query string is hashed to a 384-dim pseudo-embedding via hashEmbedding(),
 * then compared against stored chunk embeddings using the `<=>` cosine-distance
 * operator. Score = 1 - cosine_distance, so 1.0 is identical and 0.0 is
 * orthogonal.
 *
 * @param projectId - Project to search within.
 * @param query     - Natural-language query string.
 * @param limit     - Maximum number of results to return (default 10).
 * @returns Ok(SearchResult[]) sorted by descending score, Err on failure.
 */
export async function semanticSearch(
  projectId: ReturnType<typeof ProjectId>,
  query: string,
  limit: number = 10,
): Promise<Result<SearchResult[]>> {
  try {
    const sql = getSql();
    const queryVec = hashEmbedding(query);
    const queryLiteral = `[${Array.from(queryVec).join(",")}]`;

    const rows = await sql`
      SELECT
        c.id,
        c.file_id,
        c.chunk_index,
        c.content,
        c.content_hash,
        c.token_count,
        c.metadata,
        f.project_id,
        1 - (c.embedding <=> ${queryLiteral}::vector) AS score
      FROM julia_vault_file_chunks c
      JOIN julia_vault_files f ON f.id = c.file_id
      WHERE f.project_id = ${projectId as string}
      ORDER BY c.embedding <=> ${queryLiteral}::vector
      LIMIT ${limit}
    `;

    const results: SearchResult[] = rows.map((row) => ({
      id: ChunkId(row["id"] as string),
      file_id: FileId(row["file_id"] as string),
      chunk_index: row["chunk_index"] as number,
      content: row["content"] as string,
      content_hash: row["content_hash"] as string,
      token_count: (row["token_count"] as number) ?? 0,
      metadata: (row["metadata"] as Record<string, unknown>) ?? {},
      score: row["score"] as number,
      project_id: ProjectId(row["project_id"] as string),
    }));

    return Ok(results);
  } catch (err) {
    return Err({
      type: "database_error",
      message: err instanceof Error ? err.message : String(err),
    });
  }
}

/**
 * Fetch details for a set of files by ID.
 *
 * Returns a Map keyed by every supplied FileId. Files found in the database
 * are wrapped in Option.Some; IDs with no matching row produce Option.None.
 * This makes missing-file detection explicit at the call site.
 *
 * @param fileIds - Array of FileIds to look up.
 * @returns Ok(Map<FileId, Option<VaultFile>>) on success, Err on failure.
 *          Returns an empty Map immediately if `fileIds` is empty (no SQL call).
 */
export async function getFileDetails(
  fileIds: Array<ReturnType<typeof FileId>>,
): Promise<Result<Map<ReturnType<typeof FileId>, Option<ReturnType<typeof VaultFile.fromRow>>>>> {
  // Short-circuit: nothing to look up
  if (fileIds.length === 0) {
    return Ok(new Map());
  }

  try {
    const sql = getSql();

    const rows = await sql`
      SELECT
        id,
        project_id,
        filename,
        mime_type,
        size_bytes,
        content,
        content_hash,
        processing_status,
        chunk_count,
        token_count,
        metadata,
        uploaded_at,
        processed_at
      FROM julia_vault_files
      WHERE id = ANY(${fileIds as string[]}::text[])
    `;

    // Build a lookup map from the results
    const found = new Map<string, ReturnType<typeof VaultFile.fromRow>>();
    for (const row of rows) {
      const file = VaultFile.fromRow(row as Record<string, unknown>);
      found.set(file.id as string, file);
    }

    // Build the result map: Some for found, None for missing
    const resultMap = new Map<
      ReturnType<typeof FileId>,
      Option<ReturnType<typeof VaultFile.fromRow>>
    >();

    for (const fid of fileIds) {
      const file = found.get(fid as string);
      resultMap.set(fid, file !== undefined ? Some(file) : None);
    }

    return Ok(resultMap);
  } catch (err) {
    return Err({
      type: "database_error",
      message: err instanceof Error ? err.message : String(err),
    });
  }
}

/**
 * Delete a file from a vault project.
 *
 * Deletes the row from `julia_vault_files`; the database CASCADE constraint
 * removes associated chunks from `julia_vault_file_chunks` automatically.
 * Then decrements `file_count` and `storage_bytes` on the parent project.
 *
 * @param projectId - Project that owns the file.
 * @param fileId    - File to delete.
 * @returns Ok(void) on success, Err on database failure.
 */
export async function deleteFile(
  projectId: ReturnType<typeof ProjectId>,
  fileId: ReturnType<typeof FileId>,
): Promise<Result<void>> {
  try {
    const sql = getSql();

    // DELETE cascades to julia_vault_file_chunks via FK constraint
    await sql`
      DELETE FROM julia_vault_files
      WHERE id         = ${fileId as string}
        AND project_id = ${projectId as string}
    `;

    // Decrement project counters (clamp to 0 to guard against drift)
    await sql`
      UPDATE julia_vault_projects
      SET    file_count    = GREATEST(file_count - 1, 0),
             storage_bytes = GREATEST(
               storage_bytes - COALESCE(
                 (SELECT size_bytes FROM julia_vault_files WHERE id = ${fileId as string}),
                 0
               ),
               0
             ),
             updated_at = now()
      WHERE  id = ${projectId as string}
    `;

    return Ok(undefined);
  } catch (err) {
    return Err({
      type: "database_error",
      message: err instanceof Error ? err.message : String(err),
    });
  }
}

/**
 * Create a review table and seed one pending row per file.
 *
 * Inserts a row into `julia_review_tables` then inserts one pending
 * `julia_review_rows` row for each supplied FileId so the review grid
 * is immediately visible (with cells to be filled by the analyst agent).
 *
 * @param projectId - Owning project.
 * @param title     - Human-readable table title.
 * @param columns   - Column schema definitions.
 * @param fileIds   - Files to include as rows.
 * @returns Ok(ReviewTableId) on success, Err on database failure.
 */
export async function createReviewTable(
  projectId: ReturnType<typeof ProjectId>,
  title: string,
  columns: ReviewColumn[],
  fileIds: Array<ReturnType<typeof FileId>>,
): Promise<Result<ReviewTableIdType>> {
  try {
    const sql = getSql();
    const columnsJson = JSON.stringify(columns);
    const fileIdsJson = JSON.stringify(fileIds);

    // 1. INSERT review table row
    const tableRows = await sql`
      INSERT INTO julia_review_tables
        (project_id, title, columns, file_ids, created_at)
      VALUES
        (${projectId as string},
         ${title},
         ${columnsJson}::jsonb,
         ${fileIdsJson}::jsonb,
         now())
      RETURNING id
    `;

    const tableRow = tableRows[0];
    if (!tableRow) {
      return Err({ type: "database_error", message: "Review table INSERT returned no row" });
    }

    const reviewTableId = ReviewTableId(tableRow["id"] as string);

    // 2. INSERT one pending row per file
    for (const fid of fileIds) {
      await sql`
        INSERT INTO julia_review_rows
          (review_table_id, file_id, cells, status, created_at, updated_at)
        VALUES
          (${reviewTableId as string},
           ${fid as string},
           '{}',
           'pending',
           now(),
           now())
      `;
    }

    return Ok(reviewTableId);
  } catch (err) {
    return Err({
      type: "database_error",
      message: err instanceof Error ? err.message : String(err),
    });
  }
}

/**
 * Fetch a single review row by table and file ID.
 *
 * Returns Option.Some when the row exists, Option.None when it does not.
 * Unlike the other functions this returns Option directly rather than
 * Result<Option<T>> because a missing row is an expected outcome, not an
 * error condition; callers should use try/catch or a wrapper if they need
 * to distinguish DB failures from absent rows.
 *
 * @param reviewTableId - The review table to query.
 * @param fileId        - The file whose row to retrieve.
 * @returns Option.Some(ReviewRow) if found, Option.None if absent.
 */
export async function getReviewRow(
  reviewTableId: ReviewTableIdType,
  fileId: ReturnType<typeof FileId>,
): Promise<Option<ReviewRow>> {
  try {
    const sql = getSql();

    const rows = await sql`
      SELECT
        id,
        review_table_id,
        file_id,
        cells,
        status,
        created_at,
        updated_at
      FROM julia_review_rows
      WHERE review_table_id = ${reviewTableId as string}
        AND file_id         = ${fileId as string}
      LIMIT 1
    `;

    const row = rows[0];
    if (!row) {
      return None;
    }

    const reviewRow: ReviewRow = {
      id: row["id"] as string,
      review_table_id: ReviewTableId(row["review_table_id"] as string),
      file_id: FileId(row["file_id"] as string),
      cells: (row["cells"] as Record<string, string>) ?? {},
      status: row["status"] as ReviewRow["status"],
      created_at: new Date(row["created_at"] as string),
      updated_at: new Date(row["updated_at"] as string),
    };

    return Some(reviewRow);
  } catch {
    // getReviewRow returns Option<ReviewRow>, not Result.
    // Failures silently produce None; callers that need error details
    // should use a Result-returning wrapper.
    // TODO: Promote return type to Result<Option<ReviewRow>> if error
    //       distinction becomes necessary.
    return None;
  }
}
