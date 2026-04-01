/**
 * Tests for MCP server tools — mocked pg.Pool, tool handler logic.
 */

import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";

// Mock pg before importing the module
const mockQuery = vi.fn();
const mockRelease = vi.fn();
const mockConnect = vi.fn().mockResolvedValue({
  query: mockQuery,
  release: mockRelease,
});

vi.mock("pg", () => {
  return {
    default: {
      Pool: vi.fn().mockImplementation(() => ({
        connect: mockConnect,
      })),
    },
  };
});

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

vi.mock("@modelcontextprotocol/sdk/server/stdio.js", () => ({
  StdioServerTransport: vi.fn(),
}));

vi.mock("@modelcontextprotocol/sdk/server/streamableHttp.js", () => ({
  StreamableHTTPServerTransport: vi.fn(),
}));

vi.mock("./charts.js", () => ({
  renderSvgChart: vi.fn().mockReturnValue("<svg>mock</svg>"),
}));

// Set env before import
process.env.NEON_DATABASE_URL = "postgres://test:test@localhost/test";

// Import after mocks are set up — this registers all tools
await import("./index.js");

describe("MCP Tool Handlers", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockConnect.mockResolvedValue({
      query: mockQuery,
      release: mockRelease,
    });
  });

  describe("list_metrics", () => {
    it("returns metrics from database", async () => {
      const mockRows = [
        { name: "api.requests", type: "counter", unit: "req/min", dimensions: ["model"], description: "API requests" },
      ];
      mockQuery.mockResolvedValue({ rows: mockRows });

      const handler = registeredTools.get("list_metrics")!.handler;
      const result = await handler({});

      expect(mockQuery).toHaveBeenCalledWith(
        expect.stringContaining("SELECT name, type, unit, dimensions, description FROM metrics")
      );
      expect(result.content[0].type).toBe("text");
      const parsed = JSON.parse(result.content[0].text);
      expect(parsed).toEqual(mockRows);
      expect(mockRelease).toHaveBeenCalled();
    });
  });

  describe("query_metric", () => {
    it("returns raw data without aggregation", async () => {
      const mockRows = [
        { recorded_at: "2024-01-01T00:00:00Z", value: 42, tags: { model: "opus" } },
      ];
      mockQuery.mockResolvedValue({ rows: mockRows });

      const handler = registeredTools.get("query_metric")!.handler;
      const result = await handler({
        metric_name: "api.requests",
        hours: 24,
        aggregate: "none",
        step_minutes: 5,
      });

      const parsed = JSON.parse(result.content[0].text);
      expect(parsed.metric).toBe("api.requests");
      expect(parsed.count).toBe(1);
      expect(parsed.data).toEqual(mockRows);
    });

    it("uses aggregation function when specified", async () => {
      mockQuery.mockResolvedValue({ rows: [] });

      const handler = registeredTools.get("query_metric")!.handler;
      await handler({
        metric_name: "api.requests",
        hours: 48,
        aggregate: "avg",
        step_minutes: 15,
      });

      const queryCall = mockQuery.mock.calls[0][0];
      expect(queryCall).toContain("AVG(value)");
    });

    it("applies tag filters", async () => {
      mockQuery.mockResolvedValue({ rows: [] });

      const handler = registeredTools.get("query_metric")!.handler;
      await handler({
        metric_name: "api.requests",
        hours: 24,
        tags_filter: { model: "opus" },
        aggregate: "none",
        step_minutes: 5,
      });

      const queryCall = mockQuery.mock.calls[0][0];
      expect(queryCall).toContain("tags->>'model'");
    });

    it("releases client on success", async () => {
      mockQuery.mockResolvedValue({ rows: [] });

      const handler = registeredTools.get("query_metric")!.handler;
      await handler({
        metric_name: "test",
        hours: 1,
        aggregate: "none",
        step_minutes: 5,
      });

      expect(mockRelease).toHaveBeenCalled();
    });

    it("releases client on error", async () => {
      mockQuery.mockRejectedValue(new Error("DB error"));

      const handler = registeredTools.get("query_metric")!.handler;
      await expect(
        handler({ metric_name: "test", hours: 1, aggregate: "none", step_minutes: 5 })
      ).rejects.toThrow("DB error");

      expect(mockRelease).toHaveBeenCalled();
    });
  });

  describe("metric_summary", () => {
    it("returns summary statistics", async () => {
      const mockRows = [
        { count: 100, avg: 42.5, min: 1.0, max: 99.0, p50: 40.0, p99: 95.0 },
      ];
      mockQuery.mockResolvedValue({ rows: mockRows });

      const handler = registeredTools.get("metric_summary")!.handler;
      const result = await handler({ metric_name: "api.latency", hours: 168 });

      const parsed = JSON.parse(result.content[0].text);
      expect(parsed.metric).toBe("api.latency");
      expect(parsed.hours).toBe(168);
      expect(parsed.summary).toEqual(mockRows);
    });

    it("supports group_by_tag", async () => {
      mockQuery.mockResolvedValue({ rows: [] });

      const handler = registeredTools.get("metric_summary")!.handler;
      await handler({
        metric_name: "api.latency",
        hours: 24,
        group_by_tag: "model",
      });

      const queryCall = mockQuery.mock.calls[0][0];
      expect(queryCall).toContain("tags->>'model'");
      expect(queryCall).toContain("GROUP BY group_key");
    });
  });

  describe("list_skills", () => {
    it("returns skills from database", async () => {
      const mockRows = [
        { name: "crawl-ingest", description: "Web crawler", trigger_pattern: "crawl" },
      ];
      mockQuery.mockResolvedValue({ rows: mockRows });

      const handler = registeredTools.get("list_skills")!.handler;
      const result = await handler({});

      expect(mockQuery).toHaveBeenCalledWith(
        expect.stringContaining("FROM skills")
      );
      const parsed = JSON.parse(result.content[0].text);
      expect(parsed).toEqual(mockRows);
    });
  });

  describe("list_models", () => {
    it("returns models with capabilities", async () => {
      const mockRows = [
        {
          model_id: "claude-opus-4-6",
          family: "claude-4",
          label: "Opus",
          supports_thinking: true,
          supports_tool_use: true,
          supports_vision: true,
        },
      ];
      mockQuery.mockResolvedValue({ rows: mockRows });

      const handler = registeredTools.get("list_models")!.handler;
      const result = await handler({});

      const parsed = JSON.parse(result.content[0].text);
      expect(parsed[0].model_id).toBe("claude-opus-4-6");
    });
  });

  describe("create_task", () => {
    it("inserts task and returns created record", async () => {
      const mockRow = {
        id: "uuid-123",
        queue_name: "crawl-ingest",
        type: "code",
        status: "queued",
        priority: 5,
        created_at: "2024-01-01T00:00:00Z",
      };
      mockQuery.mockResolvedValue({ rows: [mockRow] });

      const handler = registeredTools.get("create_task")!.handler;
      const result = await handler({
        queue_name: "crawl-ingest",
        type: "code",
        input: { url: "https://example.com" },
        priority: 5,
      });

      const parsed = JSON.parse(result.content[0].text);
      expect(parsed.created.id).toBe("uuid-123");
      expect(parsed.created.queue_name).toBe("crawl-ingest");
    });

    it("passes optional fields correctly", async () => {
      mockQuery.mockResolvedValue({ rows: [{}] });

      const handler = registeredTools.get("create_task")!.handler;
      await handler({
        queue_name: "api-client",
        type: "knowledge_work",
        input: { prompt: "test" },
        config: { max_tokens: 1024 },
        skill_name: "api-client",
        model_id: "claude-opus-4-6",
        plugin: "custom-plugin",
        priority: 10,
      });

      const params = mockQuery.mock.calls[0][1];
      expect(params[0]).toBe("api-client"); // queue_name
      expect(params[1]).toBe("knowledge_work"); // type
      expect(params[4]).toBe("api-client"); // skill_name
      expect(params[5]).toBe("claude-opus-4-6"); // model_id
      expect(params[6]).toBe("custom-plugin"); // plugin
      expect(params[7]).toBe(10); // priority
    });
  });

  describe("list_tasks", () => {
    it("returns tasks without filters", async () => {
      const mockRows = [{ id: "1", status: "queued" }];
      mockQuery.mockResolvedValue({ rows: mockRows });

      const handler = registeredTools.get("list_tasks")!.handler;
      const result = await handler({ limit: 10 });

      const parsed = JSON.parse(result.content[0].text);
      expect(parsed.count).toBe(1);
      expect(parsed.tasks).toEqual(mockRows);
    });

    it("applies status filter", async () => {
      mockQuery.mockResolvedValue({ rows: [] });

      const handler = registeredTools.get("list_tasks")!.handler;
      await handler({ status: "completed", limit: 20 });

      const queryCall = mockQuery.mock.calls[0][0];
      expect(queryCall).toContain("status = $");
    });

    it("applies multiple filters", async () => {
      mockQuery.mockResolvedValue({ rows: [] });

      const handler = registeredTools.get("list_tasks")!.handler;
      await handler({
        status: "queued",
        type: "code",
        queue_name: "crawl-ingest",
        limit: 5,
      });

      const queryCall = mockQuery.mock.calls[0][0];
      expect(queryCall).toContain("status = $");
      expect(queryCall).toContain("type = $");
      expect(queryCall).toContain("queue_name = $");
    });
  });

  describe("task_stats", () => {
    it("returns statistics grouped by status/type/queue", async () => {
      const mockRows = [
        { status: "completed", type: "code", queue_name: "api", count: 42, avg_duration_s: 1.5 },
      ];
      mockQuery.mockResolvedValue({ rows: mockRows });

      const handler = registeredTools.get("task_stats")!.handler;
      const result = await handler({ hours: 24 });

      const parsed = JSON.parse(result.content[0].text);
      expect(parsed.hours).toBe(24);
      expect(parsed.stats).toEqual(mockRows);
    });
  });

  describe("render_chart", () => {
    it("returns error for unknown metric", async () => {
      mockQuery.mockResolvedValueOnce({ rows: [] }); // meta query returns nothing

      const handler = registeredTools.get("render_chart")!.handler;
      const result = await handler({
        metric_name: "nonexistent",
        hours: 168,
        width: 900,
        height: 400,
      });

      expect(result.isError).toBe(true);
      expect(result.content[0].text).toContain("Unknown metric");
    });

    it("returns SVG image for valid metric", async () => {
      mockQuery.mockResolvedValueOnce({
        rows: [{ type: "counter", unit: "req/min", description: "API requests" }],
      });
      mockQuery.mockResolvedValueOnce({
        rows: [{ recorded_at: "2024-01-01T00:00:00Z", value: 42, tags: {} }],
      });

      const handler = registeredTools.get("render_chart")!.handler;
      const result = await handler({
        metric_name: "agentstreams.api.requests",
        hours: 168,
        width: 900,
        height: 400,
      });

      expect(result.content.length).toBe(2);
      expect(result.content[0].type).toBe("text");
      expect(result.content[1].type).toBe("image");
      expect(result.content[1].mimeType).toBe("image/svg+xml");
    });
  });

  describe("metrics-catalog resource", () => {
    it("returns JSON catalog of metrics", async () => {
      const mockRows = [
        { name: "api.requests", type: "counter", unit: "req/min", dimensions: [], description: "test" },
      ];
      mockQuery.mockResolvedValue({ rows: mockRows });

      const handler = registeredResources.get("metrics-catalog")!;
      const result = await handler(new URL("agentstreams://metrics"));

      expect(result.contents[0].mimeType).toBe("application/json");
      const parsed = JSON.parse(result.contents[0].text);
      expect(parsed).toEqual(mockRows);
    });
  });

  describe("connection management", () => {
    it("always releases client in finally block", async () => {
      mockQuery.mockResolvedValue({ rows: [] });

      // Call multiple tools
      for (const toolName of ["list_metrics", "list_skills", "list_models"]) {
        const handler = registeredTools.get(toolName)!.handler;
        await handler({});
      }

      expect(mockRelease).toHaveBeenCalledTimes(3);
    });
  });
});
