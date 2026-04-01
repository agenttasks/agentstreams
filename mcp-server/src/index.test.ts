/**
 * Tests for MCP server tools — mocked pg.Pool, tool handler logic.
 */

import { describe, it, expect, vi, beforeEach } from "vitest";

// Mock pg before importing the module
const mockQuery = vi.fn();
const mockRelease = vi.fn();
const mockConnect = vi.fn().mockResolvedValue({
  query: mockQuery,
  release: mockRelease,
});

vi.mock("pg", () => ({
  default: {
    Pool: vi.fn().mockImplementation(() => ({ connect: mockConnect })),
  },
}));

// Mock the MCP SDK to capture tool registrations
const registeredTools: Map<string, { schema: unknown; handler: Function }> = new Map();
const registeredResources: Map<string, Function> = new Map();

vi.mock("@modelcontextprotocol/sdk/server/mcp.js", () => ({
  McpServer: vi.fn().mockImplementation(() => ({
    tool: vi.fn((name: string, _desc: string, schema: unknown, handler: Function) => {
      registeredTools.set(name, { schema, handler });
    }),
    resource: vi.fn((name: string, _uri: string, handler: Function) => {
      registeredResources.set(name, handler);
    }),
    connect: vi.fn(),
  })),
}));

vi.mock("@modelcontextprotocol/sdk/server/stdio.js", () => ({ StdioServerTransport: vi.fn() }));
vi.mock("@modelcontextprotocol/sdk/server/streamableHttp.js", () => ({ StreamableHTTPServerTransport: vi.fn() }));
vi.mock("./charts.js", () => ({ renderSvgChart: vi.fn().mockReturnValue("<svg>mock</svg>") }));

process.env.NEON_DATABASE_URL = "postgres://test:test@localhost/test";
await import("./index.js");

// ── Helpers ──────────────────────────────────────────────────

async function expectListTool(
  toolName: string,
  querySubstring: string,
  mockRows: Record<string, unknown>[],
) {
  mockQuery.mockResolvedValue({ rows: mockRows });
  const handler = registeredTools.get(toolName)!.handler;
  const result = await handler({});
  expect(mockQuery).toHaveBeenCalledWith(expect.stringContaining(querySubstring));
  expect(JSON.parse(result.content[0].text)).toEqual(mockRows);
  expect(mockRelease).toHaveBeenCalled();
}

// ── Tests ────────────────────────────────────────────────────

describe("MCP Tool Handlers", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockConnect.mockResolvedValue({ query: mockQuery, release: mockRelease });
  });

  describe("list tools (batched)", () => {
    it("list_metrics returns metrics", async () => {
      await expectListTool("list_metrics", "FROM metrics", [
        { name: "api.requests", type: "counter", unit: "req/min", dimensions: ["model"], description: "API requests" },
      ]);
    });

    it("list_skills returns skills", async () => {
      await expectListTool("list_skills", "FROM skills", [
        { name: "crawl-ingest", description: "Web crawler", trigger_pattern: "crawl" },
      ]);
    });

    it("list_models returns models", async () => {
      await expectListTool("list_models", "FROM models", [
        { model_id: "claude-opus-4-6", family: "claude-4", label: "Opus", supports_thinking: true, supports_tool_use: true, supports_vision: true },
      ]);
    });
  });

  describe("query_metric", () => {
    it("returns raw data without aggregation", async () => {
      const mockRows = [{ recorded_at: "2024-01-01T00:00:00Z", value: 42, tags: { model: "opus" } }];
      mockQuery.mockResolvedValue({ rows: mockRows });
      const result = await registeredTools.get("query_metric")!.handler({
        metric_name: "api.requests", hours: 24, aggregate: "none", step_minutes: 5,
      });
      const parsed = JSON.parse(result.content[0].text);
      expect(parsed.metric).toBe("api.requests");
      expect(parsed.data).toEqual(mockRows);
    });

    it("uses aggregation function when specified", async () => {
      mockQuery.mockResolvedValue({ rows: [] });
      await registeredTools.get("query_metric")!.handler({
        metric_name: "api.requests", hours: 48, aggregate: "avg", step_minutes: 15,
      });
      expect(mockQuery.mock.calls[0][0]).toContain("AVG(value)");
    });

    it("applies tag filters", async () => {
      mockQuery.mockResolvedValue({ rows: [] });
      await registeredTools.get("query_metric")!.handler({
        metric_name: "api.requests", hours: 24, tags_filter: { model: "opus" }, aggregate: "none", step_minutes: 5,
      });
      expect(mockQuery.mock.calls[0][0]).toContain("tags->>'model'");
    });

    it("releases client on error", async () => {
      mockQuery.mockRejectedValue(new Error("DB error"));
      await expect(
        registeredTools.get("query_metric")!.handler({ metric_name: "test", hours: 1, aggregate: "none", step_minutes: 5 })
      ).rejects.toThrow("DB error");
      expect(mockRelease).toHaveBeenCalled();
    });
  });

  describe("metric_summary", () => {
    it("returns summary statistics", async () => {
      const mockRows = [{ count: 100, avg: 42.5, min: 1.0, max: 99.0, p50: 40.0, p99: 95.0 }];
      mockQuery.mockResolvedValue({ rows: mockRows });
      const result = await registeredTools.get("metric_summary")!.handler({ metric_name: "api.latency", hours: 168 });
      const parsed = JSON.parse(result.content[0].text);
      expect(parsed.summary).toEqual(mockRows);
    });

    it("supports group_by_tag", async () => {
      mockQuery.mockResolvedValue({ rows: [] });
      await registeredTools.get("metric_summary")!.handler({ metric_name: "api.latency", hours: 24, group_by_tag: "model" });
      expect(mockQuery.mock.calls[0][0]).toContain("GROUP BY group_key");
    });
  });

  describe("create_task", () => {
    it("inserts task and returns created record", async () => {
      const mockRow = { id: "uuid-123", queue_name: "crawl-ingest", type: "code", status: "queued", priority: 5, created_at: "2024-01-01T00:00:00Z" };
      mockQuery.mockResolvedValue({ rows: [mockRow] });
      const result = await registeredTools.get("create_task")!.handler({
        queue_name: "crawl-ingest", type: "code", input: { url: "https://example.com" }, priority: 5,
      });
      expect(JSON.parse(result.content[0].text).created.id).toBe("uuid-123");
    });

    it("passes optional fields correctly", async () => {
      mockQuery.mockResolvedValue({ rows: [{}] });
      await registeredTools.get("create_task")!.handler({
        queue_name: "api-client", type: "knowledge_work", input: { prompt: "test" },
        config: { max_tokens: 1024 }, skill_name: "api-client", model_id: "claude-opus-4-6", plugin: "custom-plugin", priority: 10,
      });
      const params = mockQuery.mock.calls[0][1];
      expect(params[0]).toBe("api-client");
      expect(params[5]).toBe("claude-opus-4-6");
      expect(params[7]).toBe(10);
    });
  });

  describe("list_tasks", () => {
    it("returns tasks without filters", async () => {
      mockQuery.mockResolvedValue({ rows: [{ id: "1", status: "queued" }] });
      const result = await registeredTools.get("list_tasks")!.handler({ limit: 10 });
      expect(JSON.parse(result.content[0].text).count).toBe(1);
    });

    it("applies multiple filters", async () => {
      mockQuery.mockResolvedValue({ rows: [] });
      await registeredTools.get("list_tasks")!.handler({ status: "queued", type: "code", queue_name: "crawl-ingest", limit: 5 });
      const query = mockQuery.mock.calls[0][0];
      expect(query).toContain("status = $");
      expect(query).toContain("type = $");
      expect(query).toContain("queue_name = $");
    });
  });

  describe("task_stats", () => {
    it("returns statistics grouped by status/type/queue", async () => {
      const mockRows = [{ status: "completed", type: "code", queue_name: "api", count: 42, avg_duration_s: 1.5 }];
      mockQuery.mockResolvedValue({ rows: mockRows });
      const result = await registeredTools.get("task_stats")!.handler({ hours: 24 });
      expect(JSON.parse(result.content[0].text).stats).toEqual(mockRows);
    });
  });

  describe("render_chart", () => {
    it("returns error for unknown metric", async () => {
      mockQuery.mockResolvedValueOnce({ rows: [] });
      const result = await registeredTools.get("render_chart")!.handler({ metric_name: "nonexistent", hours: 168, width: 900, height: 400 });
      expect(result.isError).toBe(true);
      expect(result.content[0].text).toContain("Unknown metric");
    });

    it("returns SVG image for valid metric", async () => {
      mockQuery.mockResolvedValueOnce({ rows: [{ type: "counter", unit: "req/min", description: "API requests" }] });
      mockQuery.mockResolvedValueOnce({ rows: [{ recorded_at: "2024-01-01T00:00:00Z", value: 42, tags: {} }] });
      const result = await registeredTools.get("render_chart")!.handler({ metric_name: "agentstreams.api.requests", hours: 168, width: 900, height: 400 });
      expect(result.content[1].type).toBe("image");
      expect(result.content[1].mimeType).toBe("image/svg+xml");
    });
  });

  describe("metrics-catalog resource", () => {
    it("returns JSON catalog of metrics", async () => {
      const mockRows = [{ name: "api.requests", type: "counter", unit: "req/min", dimensions: [], description: "test" }];
      mockQuery.mockResolvedValue({ rows: mockRows });
      const result = await registeredResources.get("metrics-catalog")!(new URL("agentstreams://metrics"));
      expect(result.contents[0].mimeType).toBe("application/json");
      expect(JSON.parse(result.contents[0].text)).toEqual(mockRows);
    });
  });
});
