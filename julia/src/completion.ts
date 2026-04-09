/**
 * completion.ts — Legal Q&A with optional vault context.
 *
 * Provides a single `complete()` entry point that conditionally
 * attaches citations when project IDs are supplied, using TypeScript
 * conditional types (Cherny Ch.6 p.163) to enforce the contract at
 * compile time.
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 */

import Anthropic from "@anthropic-ai/sdk";
import { semanticSearch } from "./vault.js";
import {
  Ok,
  Err,
  isOk,
  type Result,
  type CompletionResponse,
  type Citation,
  type SearchResult,
  type LegalSkill,
  type ProjectId,
  type MatterId,
  FileId,
  ChunkId,
} from "./types.js";

// ── Request shape (conditional type on HasVault) ──────────────

/**
 * When `projectIds` is provided the request is typed as HasVault=true,
 * which causes CompletionResponse<true> to include `citations`.
 * When omitted (or explicitly typed as `never`) it is HasVault=false.
 */
export type CompletionRequest<HasVault extends boolean> = {
  query: string;
  model?: string;
  matterId?: MatterId;
} & (HasVault extends true
  ? { projectIds: ProjectId[] }
  : { projectIds?: never });

// ── Public API ────────────────────────────────────────────────

/**
 * Complete a legal query, optionally grounded in vault documents.
 *
 * @param request - Query plus optional vault project IDs and matter.
 * @returns Result wrapping a CompletionResponse whose shape depends
 *          on whether projectIds were supplied.
 */
export async function complete<V extends boolean>(
  request: CompletionRequest<V>,
): Promise<Result<CompletionResponse<V>>> {
  const startMs = Date.now();
  const model = request.model ?? "claude-opus-4-6";

  try {
    // Determine whether we have vault context
    const hasVault =
      request.projectIds !== undefined && request.projectIds.length > 0;

    let citations: Citation[] = [];
    let vaultContext: string | undefined;

    if (hasVault && request.projectIds) {
      // Fan out semantic search across all supplied projects
      const searchResultSets = await Promise.all(
        request.projectIds.map((pid) =>
          semanticSearch(pid, request.query, { limit: 5 }),
        ),
      );

      // Collect successful result sets; silently skip failed ones
      const successfulSets: SearchResult[][] = [];
      for (const r of searchResultSets) {
        if (isOk(r)) {
          successfulSets.push(r.value);
        }
      }

      const merged = mergeSearchResults(successfulSets);

      // Build Citation array from merged results
      citations = merged.map((sr) => ({
        file_id: FileId(sr.file_id as string),
        chunk_id: ChunkId(sr.id as string),
        content: sr.content,
        score: sr.score,
      }));

      if (merged.length > 0) {
        vaultContext = buildVaultContext(merged);
      }
    }

    const systemPrompt = buildLegalSystemPrompt(undefined, vaultContext);

    const client = new Anthropic();
    const apiResponse = await client.messages.create({
      model,
      max_tokens: 4096,
      system: systemPrompt,
      messages: [{ role: "user", content: request.query }],
    });

    // Extract text from content blocks
    const text = apiResponse.content
      .filter((block): block is Anthropic.TextBlock => block.type === "text")
      .map((block) => block.text)
      .join("\n");

    const duration_ms = Date.now() - startMs;

    const base = {
      text,
      model: apiResponse.model,
      usage: {
        input_tokens: apiResponse.usage.input_tokens,
        output_tokens: apiResponse.usage.output_tokens,
      },
      duration_ms,
    };

    // Build the response with the correct conditional shape
    const response = hasVault
      ? ({ ...base, citations } as CompletionResponse<V>)
      : (base as CompletionResponse<V>);

    return Ok(response);
  } catch (err) {
    const reason = err instanceof Error ? err.message : String(err);
    return Err({
      type: "processing_failed",
      fileId: FileId(""),
      reason: `Completion failed: ${reason}`,
    });
  }
}

/**
 * Build the legal system prompt, optionally incorporating a skill
 * specialization and vault context.
 *
 * @param skill - Optional LegalSkill that narrows the assistant's focus.
 * @param vaultContext - Pre-formatted vault excerpts to ground the response.
 * @returns The full system prompt string.
 */
export function buildLegalSystemPrompt(
  skill?: LegalSkill,
  vaultContext?: string,
): string {
  const skillLine = skill
    ? `\nYou are operating in "${skill}" mode. Focus your analysis on tasks relevant to that workflow.`
    : "";

  const vaultSection = vaultContext
    ? `\n\n${vaultContext}`
    : "";

  return `You are Julia, a legal analysis assistant that helps legal professionals review documents, assess risk, and draft responses.

IMPORTANT CONSTRAINTS:
- Never provide legal advice — frame all outputs as analysis and professional observations only.
- Always recommend that a licensed attorney review any document before it is relied upon.
- Do not speculate about jurisdiction-specific outcomes unless the relevant law is present in your context.
- Maintain strict confidentiality — do not reference prior conversations or external data sources.${skillLine}${vaultSection}`;
}

// ── Internal helpers ──────────────────────────────────────────

/**
 * Reciprocal rank fusion across multiple per-project search result lists.
 *
 * Each result's RRF score = Σ 1 / (k + rank_i) where k=60 (standard).
 * Results are deduplicated by chunk ID and sorted descending by fused score.
 *
 * @param results - One list of SearchResult per project.
 * @returns Merged, deduplicated, score-sorted SearchResult array.
 */
export function mergeSearchResults(results: SearchResult[][]): SearchResult[] {
  const K = 60;
  // Map from chunk id → { result, fusedScore }
  const scoreMap = new Map<string, { result: SearchResult; fusedScore: number }>();

  for (const list of results) {
    list.forEach((sr, rank) => {
      const key = sr.id as string;
      const rrfScore = 1 / (K + rank + 1);
      const existing = scoreMap.get(key);
      if (existing) {
        existing.fusedScore += rrfScore;
      } else {
        scoreMap.set(key, { result: sr, fusedScore: rrfScore });
      }
    });
  }

  return Array.from(scoreMap.values())
    .sort((a, b) => b.fusedScore - a.fusedScore)
    .map(({ result, fusedScore }) => ({ ...result, score: fusedScore }));
}

/**
 * Format merged search results into a vault context block for the prompt.
 *
 * @param results - Merged search results ordered by relevance.
 * @returns Formatted string suitable for inclusion in a system prompt.
 */
function buildVaultContext(results: SearchResult[]): string {
  const excerpts = results
    .slice(0, 10)
    .map((sr, i) => `[${i + 1}] (score: ${sr.score.toFixed(3)})\n${sr.content}`)
    .join("\n\n");

  return `RELEVANT DOCUMENT EXCERPTS:\n${excerpts}`;
}
