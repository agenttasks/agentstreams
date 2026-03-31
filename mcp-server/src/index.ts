import { createServer } from "node:http";
import { randomUUID } from "node:crypto";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";
import pg from "pg";
import { renderSvgChart } from "./charts.js";

const NEON_URL = process.env.NEON_DATABASE_URL;

let pool: pg.Pool | null = null;

function getPool(): pg.Pool {
  if (!pool) {
    if (!NEON_URL) {
      throw new Error("NEON_DATABASE_URL environment variable is required");
    }
    pool = new pg.Pool({ connectionString: NEON_URL, ssl: { rejectUnauthorized: false } });
  }
  return pool;
}

// ── Server setup ─────────────────────────────────────────────

const server = new McpServer({
  name: "agentstreams",
  version: "0.1.0",
});

// ── Tool: list_metrics ───────────────────────────────────────

server.tool(
  "list_metrics",
  "List all available metrics with their type, unit, and dimensions",
  {},
  async () => {
    const client = await getPool().connect();
    try {
      const result = await client.query(
        "SELECT name, type, unit, dimensions, description FROM metrics ORDER BY name"
      );
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(result.rows, null, 2),
          },
        ],
      };
    } finally {
      client.release();
    }
  }
);

// ── Tool: query_metric ───────────────────────────────────────

server.tool(
  "query_metric",
  "Query time-series data for a specific metric. Returns recent values with dimensional tags.",
  {
    metric_name: z.string().describe("Metric name (e.g. agentstreams.api.requests)"),
    hours: z.number().default(24).describe("Hours of data to return (default: 24)"),
    tags_filter: z
      .record(z.string(), z.string())
      .optional()
      .describe("Filter by tag values (e.g. {model: 'claude-opus-4-6'})"),
    aggregate: z
      .enum(["none", "avg", "sum", "max", "min"])
      .default("none")
      .describe("Aggregation function (default: none = raw points)"),
    step_minutes: z.number().default(5).describe("Step interval in minutes (default: 5)"),
  },
  async ({ metric_name, hours, tags_filter, aggregate, step_minutes }) => {
    const client = await getPool().connect();
    try {
      let query: string;
      const params: (string | number | undefined)[] = [metric_name, hours];

      if (aggregate === "none") {
        query = `
          SELECT recorded_at, value, tags
          FROM metric_values
          WHERE metric_name = $1
            AND recorded_at > now() - interval '1 hour' * $2
          ORDER BY recorded_at DESC
          LIMIT 1000
        `;
      } else {
        const aggFn = aggregate.toUpperCase();
        query = `
          SELECT
            date_trunc('minute', recorded_at)
              - (EXTRACT(minute FROM recorded_at)::int % ${step_minutes}) * interval '1 minute' AS bucket,
            ${aggFn}(value) AS value,
            tags
          FROM metric_values
          WHERE metric_name = $1
            AND recorded_at > now() - interval '1 hour' * $2
          GROUP BY bucket, tags
          ORDER BY bucket DESC
          LIMIT 500
        `;
      }

      // Add tag filter if provided
      if (tags_filter && Object.keys(tags_filter).length > 0) {
        const tagConditions = Object.entries(tags_filter)
          .map(([key, value]) => {
            params.push(String(value));
            return `tags->>'${key}' = $${params.length}`;
          })
          .join(" AND ");
        query = query.replace(
          "ORDER BY",
          `AND ${tagConditions}\n          ORDER BY`
        );
      }

      const result = await client.query(query, params);
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(
              {
                metric: metric_name,
                hours,
                aggregate,
                count: result.rows.length,
                data: result.rows,
              },
              null,
              2
            ),
          },
        ],
      };
    } finally {
      client.release();
    }
  }
);

// ── Tool: metric_summary ─────────────────────────────────────

server.tool(
  "metric_summary",
  "Get statistical summary (min, max, avg, count, p50, p99) for a metric over a time range",
  {
    metric_name: z.string().describe("Metric name"),
    hours: z.number().default(168).describe("Hours to summarize (default: 168 = 1 week)"),
    group_by_tag: z.string().optional().describe("Tag key to group by (e.g. 'model', 'skill')"),
  },
  async ({ metric_name, hours, group_by_tag }) => {
    const client = await getPool().connect();
    try {
      let query: string;
      const params = [metric_name, hours];

      if (group_by_tag) {
        query = `
          SELECT
            tags->>'${group_by_tag}' AS group_key,
            COUNT(*) AS count,
            ROUND(AVG(value)::numeric, 4) AS avg,
            ROUND(MIN(value)::numeric, 4) AS min,
            ROUND(MAX(value)::numeric, 4) AS max,
            ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY value)::numeric, 4) AS p50,
            ROUND(PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY value)::numeric, 4) AS p99
          FROM metric_values
          WHERE metric_name = $1
            AND recorded_at > now() - interval '1 hour' * $2
          GROUP BY group_key
          ORDER BY avg DESC
        `;
      } else {
        query = `
          SELECT
            COUNT(*) AS count,
            ROUND(AVG(value)::numeric, 4) AS avg,
            ROUND(MIN(value)::numeric, 4) AS min,
            ROUND(MAX(value)::numeric, 4) AS max,
            ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY value)::numeric, 4) AS p50,
            ROUND(PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY value)::numeric, 4) AS p99
          FROM metric_values
          WHERE metric_name = $1
            AND recorded_at > now() - interval '1 hour' * $2
        `;
      }

      const result = await client.query(query, params);
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(
              {
                metric: metric_name,
                hours,
                group_by: group_by_tag || null,
                summary: result.rows,
              },
              null,
              2
            ),
          },
        ],
      };
    } finally {
      client.release();
    }
  }
);

// ── Tool: list_skills ────────────────────────────────────────

server.tool(
  "list_skills",
  "List all registered skills with descriptions and trigger patterns",
  {},
  async () => {
    const client = await getPool().connect();
    try {
      const result = await client.query(
        "SELECT name, description, trigger_pattern FROM skills ORDER BY name"
      );
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(result.rows, null, 2),
          },
        ],
      };
    } finally {
      client.release();
    }
  }
);

// ── Tool: list_models ────────────────────────────────────────

server.tool(
  "list_models",
  "List Claude models with capabilities (thinking, tool use, vision)",
  {},
  async () => {
    const client = await getPool().connect();
    try {
      const result = await client.query(
        `SELECT model_id, family, label, supports_thinking, supports_tool_use, supports_vision
         FROM models ORDER BY family DESC, model_id`
      );
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(result.rows, null, 2),
          },
        ],
      };
    } finally {
      client.release();
    }
  }
);

// ── Tool: create_task ─────────────────────────────────────────

server.tool(
  "create_task",
  "Create a new task in the queue for processing",
  {
    queue_name: z.string().describe("Queue/entrypoint name (e.g. 'crawl-ingest', 'api-client')"),
    type: z.enum(["code", "knowledge_work", "financial"]).describe("Task type"),
    input: z.record(z.string(), z.unknown()).describe("Task input payload"),
    config: z.record(z.string(), z.unknown()).optional().describe("Task configuration"),
    skill_name: z.string().optional().describe("Associated skill name"),
    model_id: z.string().optional().describe("Model to use (e.g. claude-opus-4-6)"),
    plugin: z.string().optional().describe("Plugin identifier for knowledge-work tasks"),
    priority: z.number().default(0).describe("Priority (higher = sooner, default: 0)"),
  },
  async ({ queue_name, type, input, config, skill_name, model_id, plugin, priority }) => {
    const client = await getPool().connect();
    try {
      const result = await client.query(
        `INSERT INTO tasks (queue_name, type, input, config, skill_name, model_id, plugin, priority)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
         RETURNING id, queue_name, type, status, priority, created_at`,
        [queue_name, type, JSON.stringify(input), JSON.stringify(config || {}),
         skill_name || null, model_id || null, plugin || null, priority]
      );
      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({ created: result.rows[0] }, null, 2),
        }],
      };
    } finally {
      client.release();
    }
  }
);

// ── Tool: list_tasks ─────────────────────────────────────────

server.tool(
  "list_tasks",
  "List tasks filtered by status, type, or queue",
  {
    status: z.enum(["queued", "processing", "completed", "failed", "cancelled"]).optional(),
    type: z.enum(["code", "knowledge_work", "financial"]).optional(),
    queue_name: z.string().optional(),
    limit: z.number().default(20).describe("Max results (default: 20)"),
  },
  async ({ status, type, queue_name, limit }) => {
    const client = await getPool().connect();
    try {
      const conditions: string[] = [];
      const params: (string | number)[] = [];

      if (status) { params.push(status); conditions.push(`status = $${params.length}`); }
      if (type) { params.push(type); conditions.push(`type = $${params.length}`); }
      if (queue_name) { params.push(queue_name); conditions.push(`queue_name = $${params.length}`); }

      params.push(limit);
      const where = conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";
      const result = await client.query(
        `SELECT id, queue_name, type, status, priority, skill_name, model_id, plugin,
                attempts, created_at, started_at, completed_at
         FROM tasks ${where}
         ORDER BY created_at DESC
         LIMIT $${params.length}`,
        params
      );
      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({ count: result.rows.length, tasks: result.rows }, null, 2),
        }],
      };
    } finally {
      client.release();
    }
  }
);

// ── Tool: task_stats ─────────────────────────────────────────

server.tool(
  "task_stats",
  "Get task queue statistics — counts by status, type, and queue",
  {
    hours: z.number().default(24).describe("Time window in hours (default: 24)"),
  },
  async ({ hours }) => {
    const client = await getPool().connect();
    try {
      const result = await client.query(
        `SELECT
           status,
           type,
           queue_name,
           COUNT(*) as count,
           ROUND(AVG(EXTRACT(EPOCH FROM (completed_at - started_at)))::numeric, 2) as avg_duration_s
         FROM tasks
         WHERE created_at > now() - interval '1 hour' * $1
         GROUP BY status, type, queue_name
         ORDER BY count DESC`,
        [hours]
      );
      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({ hours, stats: result.rows }, null, 2),
        }],
      };
    } finally {
      client.release();
    }
  }
);

// ── Tool: render_chart ──────────────────────────────────────

server.tool(
  "render_chart",
  "Render an inline SVG chart for a metric over a time range. Returns an SVG image.",
  {
    metric_name: z.string().describe("Metric name (e.g. agentstreams.api.requests)"),
    hours: z.number().default(168).describe("Hours of data to chart (default: 168 = 1 week)"),
    tags_filter: z
      .record(z.string(), z.string())
      .optional()
      .describe("Filter by tag values"),
    width: z.number().default(900).describe("Chart width in pixels"),
    height: z.number().default(400).describe("Chart height in pixels"),
  },
  async ({ metric_name, hours, tags_filter, width, height }) => {
    const client = await getPool().connect();
    try {
      // Look up metric metadata
      const metaResult = await client.query(
        "SELECT type, unit, description FROM metrics WHERE name = $1",
        [metric_name]
      );
      const meta = metaResult.rows[0];
      if (!meta) {
        return {
          content: [{ type: "text" as const, text: `Unknown metric: ${metric_name}` }],
          isError: true,
        };
      }

      // Fetch data
      const params: (string | number)[] = [metric_name, hours];
      let tagClause = "";
      if (tags_filter && Object.keys(tags_filter).length > 0) {
        const conditions = Object.entries(tags_filter).map(([key, value]) => {
          params.push(String(value));
          return `tags->>'${key}' = $${params.length}`;
        });
        tagClause = `AND ${conditions.join(" AND ")}`;
      }

      const dataResult = await client.query(
        `SELECT recorded_at, value, tags
         FROM metric_values
         WHERE metric_name = $1
           AND recorded_at > now() - interval '1 hour' * $2
           ${tagClause}
         ORDER BY recorded_at`,
        params
      );

      const title =
        METRIC_TITLES[metric_name] || meta.description || metric_name;
      const ylabel = meta.unit || "";

      const svg = renderSvgChart(dataResult.rows, { title, ylabel, width, height });

      return {
        content: [
          {
            type: "text" as const,
            text: `SVG chart rendered: ${metric_name} (${dataResult.rows.length} points, ${hours}h window)`,
          },
          {
            type: "image" as const,
            data: Buffer.from(svg).toString("base64"),
            mimeType: "image/svg+xml",
          },
        ],
      };
    } finally {
      client.release();
    }
  }
);

const METRIC_TITLES: Record<string, string> = {
  "agentstreams.pipeline.duration": "Pipeline Stage Duration",
  "agentstreams.api.requests": "Claude API Requests (rate/min)",
  "agentstreams.api.tokens": "Token Usage (rate/min)",
  "agentstreams.api.cost": "API Cost per Request",
  "agentstreams.eval.score": "Eval Pass Rate",
  "agentstreams.crawl.pages": "Pages Crawled (rate/min)",
  "agentstreams.crawl.dedup": "Bloom Filter False Positive Rate",
  "agentstreams.tasks.throughput": "Task Throughput (rate/min)",
  "agentstreams.tasks.duration": "Task Processing Duration",
  "agentstreams.tasks.queue_depth": "Task Queue Depth",
};

// ── Resource: metric catalog ─────────────────────────────────

server.resource("metrics-catalog", "agentstreams://metrics", async (uri) => {
  const client = await getPool().connect();
  try {
    const result = await client.query(
      "SELECT name, type, unit, dimensions, description FROM metrics ORDER BY name"
    );
    return {
      contents: [
        {
          uri: uri.href,
          mimeType: "application/json",
          text: JSON.stringify(result.rows, null, 2),
        },
      ],
    };
  } finally {
    client.release();
  }
});

// ── Start ────────────────────────────────────────────────────

async function main() {
  const mode = process.env.MCP_TRANSPORT || "stdio";

  if (mode === "http") {
    const port = parseInt(process.env.MCP_PORT || "3001", 10);

    const httpServer = createServer(async (req, res) => {
      // Health check
      if (req.method === "GET" && req.url === "/health") {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ status: "ok", server: "agentstreams", version: "0.2.0" }));
        return;
      }

      // MCP endpoint
      if (req.url === "/mcp") {
        const transport = new StreamableHTTPServerTransport({
          sessionIdGenerator: () => randomUUID(),
        });
        await server.connect(transport);
        await transport.handleRequest(req, res);
        return;
      }

      res.writeHead(404);
      res.end("Not found");
    });

    httpServer.listen(port, () => {
      console.error(`AgentStreams MCP server running on http://localhost:${port}/mcp`);
    });
  } else {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("AgentStreams MCP server running on stdio");
  }
}

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
