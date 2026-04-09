/**
 * MCP server — exposes the 14-layer knowledge-work stack as MCP tools.
 *
 * Creates a Model Context Protocol server that Claude Code (or any MCP
 * client) can connect to. Exposes tools for:
 *   - Task routing (Layer 4)
 *   - Layer inspection (Layer registry)
 *   - Ecosystem search (Registry)
 *   - Session management (Layer 7)
 *
 * Transport: stdio (default for Claude Code) or HTTP.
 *
 * Usage in .claude/settings.json:
 *   "mcpServers": {
 *     "knowledge-work": {
 *       "command": "node",
 *       "args": ["dist/mcp.js"]
 *     }
 *   }
 *
 * Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
 *
 * @see https://www.npmjs.com/package/@modelcontextprotocol/sdk
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

import { TaskRouter, type TaskDefinition } from "./router.js";
import { LAYER_REGISTRY, LAYER_IDS, type Layer } from "./layers.js";
import { SessionStore } from "./session.js";

// ── Server Setup ─────────────────────────────────────────────

/**
 * Create the knowledge-work MCP server with all tools registered.
 *
 * Returns the server instance (not yet connected to a transport).
 * Call connectStdio() or provide your own transport.
 */
export function createKnowledgeWorkServer(): McpServer {
  const server = new McpServer({
    name: "knowledge-work",
    version: "0.3.0",
  });

  const router = new TaskRouter();

  // ── Tool: route_task ─────────────────────────────────────

  server.tool(
    "route_task",
    "Route a natural language request to the best matching knowledge-work task. " +
      "Returns the task definition with domain, plugin category, skill, agent, and model.",
    {
      request: z
        .string()
        .describe("Natural language description of the knowledge-work task"),
    },
    async ({ request }) => {
      const task = router.route(request);
      if (!task) {
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify({
                matched: false,
                message: "No matching task found. Available domains: " +
                  router.domains().join(", "),
              }),
            },
          ],
        };
      }
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({ matched: true, task }),
          },
        ],
      };
    },
  );

  // ── Tool: list_tasks ─────────────────────────────────────

  server.tool(
    "list_tasks",
    "List available knowledge-work tasks, optionally filtered by domain. " +
      "Returns task names, descriptions, and agent assignments.",
    {
      domain: z
        .string()
        .optional()
        .describe(
          "Filter by domain (sales, marketing, finance, legal, engineering, " +
            "data, design, human-resources, customer-support, enterprise-search, " +
            "product-management, bio-research)",
        ),
    },
    async ({ domain }) => {
      const tasks = router.list(domain);
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({
              count: tasks.length,
              domains: router.domains(),
              tasks: tasks.map((t: TaskDefinition) => ({
                name: t.name,
                description: t.description,
                domain: t.domain,
                agent: t.agentName,
                complexity: t.complexity,
              })),
            }),
          },
        ],
      };
    },
  );

  // ── Tool: inspect_layer ──────────────────────────────────

  server.tool(
    "inspect_layer",
    "Inspect a specific layer in the 14-layer knowledge-work stack. " +
      "Returns the layer definition with description, associated repos, and concepts.",
    {
      layer_id: z
        .number()
        .describe(
          "Layer ID (0, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 7.5, 8, 9, 10)",
        ),
    },
    async ({ layer_id }) => {
      const layer: Layer | undefined = LAYER_REGISTRY[layer_id];
      if (!layer) {
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify({
                error: `Unknown layer ${layer_id}. Valid IDs: ${LAYER_IDS.join(", ")}`,
              }),
            },
          ],
        };
      }
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(layer),
          },
        ],
      };
    },
  );

  // ── Tool: list_layers ────────────────────────────────────

  server.tool(
    "list_layers",
    "List all 14 layers in the knowledge-work stack from L0 (Training) to L10 (Governance).",
    {},
    async () => {
      const layers = LAYER_IDS.map((id) => {
        const layer = LAYER_REGISTRY[id];
        return {
          id: layer.id,
          name: layer.name,
          description: layer.description,
          repo_count: layer.repos.length,
        };
      });
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({ total: layers.length, layers }),
          },
        ],
      };
    },
  );

  // ── Tool: session_events ─────────────────────────────────

  server.tool(
    "session_events",
    "Query events from a knowledge-work session log. " +
      "Returns events filtered by type and/or layer.",
    {
      session_id: z.string().describe("Session ID to query"),
      event_type: z
        .string()
        .optional()
        .describe("Filter by event type (e.g., 'task.routed', 'harness.complete')"),
      layer: z
        .number()
        .optional()
        .describe("Filter by layer ID"),
      last_n: z
        .number()
        .optional()
        .describe("Return only the last N events"),
    },
    async ({ session_id, event_type, layer, last_n }) => {
      const store = new SessionStore(session_id);
      let events;

      if (last_n) {
        events = await store.tail(last_n);
      } else {
        events = await store.getEvents({
          type: event_type,
          layer,
        });
      }

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({
              session_id,
              event_count: events.length,
              events,
            }),
          },
        ],
      };
    },
  );

  // ── Resource: layer-stack ────────────────────────────────

  server.resource(
    "layer-stack",
    "knowledge-work://layers",
    async () => {
      const stack = LAYER_IDS.map((id) => {
        const l = LAYER_REGISTRY[id];
        return `L${l.id} ${l.name}: ${l.description} [${l.repos.length} repos]`;
      });

      return {
        contents: [
          {
            uri: "knowledge-work://layers",
            mimeType: "text/plain",
            text: stack.join("\n"),
          },
        ],
      };
    },
  );

  return server;
}

// ── Standalone Entry Point ───────────────────────────────────

/**
 * Start the MCP server on stdio transport.
 *
 * Called when this file is run directly:
 *   node dist/mcp.js
 */
export async function startStdioServer(): Promise<void> {
  const server = createKnowledgeWorkServer();
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("knowledge-work MCP server running on stdio");
}

// Auto-start when run as main module
const isMain =
  typeof process !== "undefined" &&
  process.argv[1] &&
  (process.argv[1].endsWith("/mcp.js") || process.argv[1].endsWith("/mcp.ts"));

if (isMain) {
  startStdioServer().catch((err) => {
    console.error("Failed to start MCP server:", err);
    process.exit(1);
  });
}
