import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import pg from "pg";

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
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("AgentStreams MCP server running on stdio");
}

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
