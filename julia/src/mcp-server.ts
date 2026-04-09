/**
 * Julia MCP server — exposes legal AI tools for Claude Code and external clients.
 *
 * 13 tools + 3 resources + 9 prompts, following MCP spec (modelcontextprotocol.io).
 *
 * Transport: stdio (Claude Code) or StreamableHTTP (webapp/external).
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 *
 * Register in .claude/settings.json:
 *   "mcpServers": { "julia": { "command": "node", "args": ["julia/dist/mcp-server.js"] } }
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

import {
  ProjectId,
  FileId,
  MatterId,
  ReviewTableId,
  AuditLogId,
  LEGAL_SKILLS,
  type LegalSkill,
} from "./types.js";
import {
  createProject,
  uploadFile,
  semanticSearch,
  getFileDetails,
  deleteFile,
  createReviewTable,
  getReviewRow,
} from "./vault.js";
import { complete, buildLegalSystemPrompt } from "./completion.js";
import { addMatters, getMatters, deleteMatters } from "./matters.js";
import { log, queryForward, searchByTimestamp } from "./audit.js";

// ── Helper: Result → MCP content ─────────────────────────────

function resultToContent<T>(
  result: { ok: true; value: T } | { ok: false; error: unknown },
): { content: Array<{ type: "text"; text: string }>; isError?: boolean } {
  if (result.ok) {
    return {
      content: [
        { type: "text" as const, text: JSON.stringify(result.value) },
      ],
    };
  }
  return {
    content: [
      { type: "text" as const, text: JSON.stringify(result.error) },
    ],
    isError: true,
  };
}

// ── Server Factory (Cherny Ch.5 p.128 Factory Pattern) ───────

export function createJuliaServer(): McpServer {
  const server = new McpServer({
    name: "julia",
    version: "0.1.0",
  });

  // ── Vault Tools ──────────────────────────────────────────

  server.tool(
    "julia_create_project",
    "Create a new vault project for organizing legal documents.",
    {
      name: z.string().describe("Project name"),
      owner_email: z.string().describe("Owner email address"),
      description: z.string().optional().describe("Project description"),
      is_knowledge_base: z.boolean().optional().describe("Regional knowledge base flag"),
      client_matter_id: z.string().optional().describe("Associated client matter ID"),
    },
    async ({ name, owner_email, description, is_knowledge_base, client_matter_id }) => {
      const result = await createProject(name, owner_email, {
        description,
        isKnowledgeBase: is_knowledge_base,
        clientMatterId: client_matter_id ? MatterId(client_matter_id) : undefined,
      });
      return resultToContent(result);
    },
  );

  server.tool(
    "julia_upload_file",
    "Upload a document to a vault project. Extracts text, chunks, and computes embeddings.",
    {
      project_id: z.string().describe("Vault project ID"),
      filename: z.string().describe("Document filename"),
      content: z.string().describe("Document text content"),
      mime_type: z.string().optional().describe("MIME type (default: text/plain)"),
    },
    async ({ project_id, filename, content, mime_type }) => {
      const result = await uploadFile(
        ProjectId(project_id),
        filename,
        content,
        mime_type ?? "text/plain",
      );
      return resultToContent(result);
    },
  );

  server.tool(
    "julia_search",
    "Semantic search over vault documents in a project. Returns ranked chunks with scores.",
    {
      project_id: z.string().describe("Vault project ID to search"),
      query: z.string().describe("Natural language search query"),
      limit: z.number().optional().describe("Max results (default: 10)"),
    },
    async ({ project_id, query, limit }) => {
      const result = await semanticSearch(
        ProjectId(project_id),
        query,
        limit ?? 10,
      );
      return resultToContent(result);
    },
  );

  server.tool(
    "julia_file_details",
    "Get processing status and metadata for one or more vault files.",
    {
      file_ids: z.array(z.string()).describe("Array of file IDs to look up"),
    },
    async ({ file_ids }) => {
      const result = await getFileDetails(file_ids.map(FileId));
      if (result.ok) {
        const serializable: Record<string, unknown> = {};
        for (const [key, val] of result.value.entries()) {
          serializable[key as string] = val;
        }
        return { content: [{ type: "text" as const, text: JSON.stringify(serializable) }] };
      }
      return resultToContent(result);
    },
  );

  server.tool(
    "julia_delete_file",
    "Delete a file from a vault project (cascades to chunks).",
    {
      project_id: z.string().describe("Vault project ID"),
      file_id: z.string().describe("File ID to delete"),
    },
    async ({ project_id, file_id }) => {
      const result = await deleteFile(ProjectId(project_id), FileId(file_id));
      return resultToContent(result);
    },
  );

  server.tool(
    "julia_create_review_table",
    "Create a structured review table for extracting data across multiple documents.",
    {
      project_id: z.string().describe("Vault project ID"),
      title: z.string().describe("Review table title"),
      columns: z.array(z.object({
        name: z.string(),
        type: z.enum(["text", "date", "currency", "boolean"]),
        description: z.string(),
      })).describe("Column definitions"),
      file_ids: z.array(z.string()).describe("File IDs to include in the review"),
    },
    async ({ project_id, title, columns, file_ids }) => {
      const result = await createReviewTable(
        ProjectId(project_id),
        title,
        columns,
        file_ids.map(FileId),
      );
      return resultToContent(result);
    },
  );

  server.tool(
    "julia_get_review_row",
    "Get extracted data for a specific file in a review table.",
    {
      review_table_id: z.string().describe("Review table ID"),
      file_id: z.string().describe("File ID"),
    },
    async ({ review_table_id, file_id }) => {
      const opt = await getReviewRow(
        ReviewTableId(review_table_id),
        FileId(file_id),
      );
      // Unwrap Option to a clean format for MCP clients (not raw _tag)
      const value = opt._tag === "Some" ? opt.value : null;
      return {
        content: [{ type: "text" as const, text: JSON.stringify(value) }],
      };
    },
  );

  // ── Completion Tool ──────────────────────────────────────

  server.tool(
    "julia_completion",
    "Legal-grade Q&A with optional vault context and client matter association. " +
      "Returns analysis (not legal advice) with citations when vault context is provided.",
    {
      query: z.string().describe("Legal question or analysis request"),
      project_ids: z.array(z.string()).optional().describe("Vault project IDs for document context"),
      matter_id: z.string().optional().describe("Client matter ID for billing attribution"),
      model: z.string().optional().describe("Model override (default: claude-opus-4-6)"),
    },
    async ({ query, project_ids, matter_id, model }) => {
      if (project_ids && project_ids.length > 0) {
        const result = await complete({
          query,
          projectIds: project_ids.map(ProjectId),
          matterId: matter_id ? MatterId(matter_id) : undefined,
          model,
        });
        return resultToContent(result);
      } else {
        const result = await complete({
          query,
          matterId: matter_id ? MatterId(matter_id) : undefined,
          model,
        });
        return resultToContent(result);
      }
    },
  );

  // ── Client Matter Tools ──────────────────────────────────

  server.tool(
    "julia_add_matters",
    "Create one or more client matters for billing attribution and access control.",
    {
      matters: z.array(z.object({
        name: z.string().describe("Matter name (e.g., 'Acme Corp v. Widget Inc')"),
        description: z.string().optional(),
      })),
    },
    async ({ matters }) => {
      const result = await addMatters(matters);
      return resultToContent(result);
    },
  );

  server.tool(
    "julia_get_matters",
    "List all active client matters with usage statistics (query count, token count).",
    {},
    async () => {
      const result = await getMatters();
      if (result.ok) {
        const serializable: Record<string, unknown> = {};
        for (const [key, val] of result.value.entries()) {
          serializable[key as string] = val;
        }
        return { content: [{ type: "text" as const, text: JSON.stringify(serializable) }] };
      }
      return resultToContent(result);
    },
  );

  server.tool(
    "julia_delete_matters",
    "Soft-delete client matters (sets deleted_at, preserves audit history).",
    {
      matter_ids: z.array(z.string()).describe("Matter IDs to delete"),
    },
    async ({ matter_ids }) => {
      const result = await deleteMatters(matter_ids.map(MatterId));
      return resultToContent(result);
    },
  );

  // ── Audit Tools ──────────────────────────────────────────

  server.tool(
    "julia_query_audit_logs",
    "Paginate forward through audit logs from a given log ID.",
    {
      from_id: z.number().describe("Start pagination from this audit log ID"),
      take: z.number().describe("Number of entries to fetch"),
    },
    async ({ from_id, take }) => {
      const result = await queryForward(AuditLogId(from_id), take);
      return resultToContent(result);
    },
  );

  server.tool(
    "julia_search_audit_logs",
    "Find the audit log entry at or after a given timestamp.",
    {
      timestamp: z.string().describe("ISO 8601 timestamp to search from"),
    },
    async ({ timestamp }) => {
      const date = new Date(timestamp);
      if (isNaN(date.getTime())) {
        return {
          content: [{ type: "text" as const, text: JSON.stringify({ error: "Invalid timestamp" }) }],
          isError: true,
        };
      }
      const result = await searchByTimestamp(date);
      return resultToContent(result);
    },
  );

  // ── Resources ────────────────────────────────────────────

  server.resource(
    "legal-skills",
    "julia://skills",
    async () => ({
      contents: [{
        uri: "julia://skills",
        mimeType: "application/json",
        text: JSON.stringify(LEGAL_SKILLS),
      }],
    }),
  );

  // ── Prompts (9 legal skills as MCP prompts) ──────────────

  for (const skill of LEGAL_SKILLS) {
    server.prompt(
      `julia-${skill}`,
      `Legal workflow: ${skill}`,
      [{ name: "request", description: "Your legal request", required: true }],
      async ({ request }) => ({
        messages: [{
          role: "user" as const,
          content: {
            type: "text" as const,
            text: `${buildLegalSystemPrompt(skill as LegalSkill)}\n\n---\n\n${request}`,
          },
        }],
      }),
    );
  }

  return server;
}

// ── Standalone Entry Point ───────────────────────────────────

export async function startStdioServer(): Promise<void> {
  const server = createJuliaServer();
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Julia MCP server running on stdio");
}

const isMain =
  typeof process !== "undefined" &&
  process.argv[1] &&
  (process.argv[1].endsWith("/mcp-server.js") ||
    process.argv[1].endsWith("/mcp-server.ts"));

if (isMain) {
  startStdioServer().catch((err) => {
    console.error("Failed to start Julia MCP server:", err);
    process.exit(1);
  });
}
