/**
 * Tests for charts.ts — SVG chart rendering, series grouping, and formatting.
 */

import { describe, it, expect } from "vitest";
import { renderSvgChart } from "./charts.js";

// Re-export internal functions for testing by parsing the module
// Since groupIntoSeries, formatValue, formatTime, escapeXml are not exported,
// we test them through renderSvgChart behavior.

interface DataPoint {
  recorded_at: string;
  value: number;
  tags: Record<string, string>;
}

function makeDataPoint(
  recorded_at: string,
  value: number,
  tags: Record<string, string> = {}
): DataPoint {
  return { recorded_at, value, tags };
}

describe("renderSvgChart", () => {
  it("returns 'No data' SVG for empty data", () => {
    const svg = renderSvgChart([], { title: "Empty", ylabel: "count" });
    expect(svg).toContain("No data");
    expect(svg).toContain("<svg");
    expect(svg).toContain("</svg>");
  });

  it("renders valid SVG with data", () => {
    const data: DataPoint[] = [
      makeDataPoint("2024-01-01T00:00:00Z", 10, { model: "opus" }),
      makeDataPoint("2024-01-01T01:00:00Z", 20, { model: "opus" }),
      makeDataPoint("2024-01-01T02:00:00Z", 15, { model: "opus" }),
    ];
    const svg = renderSvgChart(data, { title: "Test Chart", ylabel: "requests" });

    expect(svg).toContain("<svg");
    expect(svg).toContain("</svg>");
    expect(svg).toContain("Test Chart");
  });

  it("renders title and y-axis label", () => {
    const data: DataPoint[] = [
      makeDataPoint("2024-01-01T00:00:00Z", 100),
      makeDataPoint("2024-01-01T12:00:00Z", 200),
    ];
    const svg = renderSvgChart(data, { title: "My Title", ylabel: "ms" });

    expect(svg).toContain("My Title");
    expect(svg).toContain("ms");
  });

  it("groups data into separate series by tags", () => {
    const data: DataPoint[] = [
      makeDataPoint("2024-01-01T00:00:00Z", 10, { model: "opus" }),
      makeDataPoint("2024-01-01T01:00:00Z", 20, { model: "opus" }),
      makeDataPoint("2024-01-01T00:00:00Z", 5, { model: "sonnet" }),
      makeDataPoint("2024-01-01T01:00:00Z", 8, { model: "sonnet" }),
    ];
    const svg = renderSvgChart(data, { title: "Multi", ylabel: "val" });

    // Should have two path elements (two series)
    const pathCount = (svg.match(/<path /g) || []).length;
    expect(pathCount).toBe(2);

    // Legend should show both series
    expect(svg).toContain("model=opus");
    expect(svg).toContain("model=sonnet");
  });

  it("uses custom dimensions", () => {
    const data: DataPoint[] = [
      makeDataPoint("2024-01-01T00:00:00Z", 10),
      makeDataPoint("2024-01-01T01:00:00Z", 20),
    ];
    const svg = renderSvgChart(data, {
      title: "Custom Size",
      ylabel: "val",
      width: 1200,
      height: 600,
    });

    expect(svg).toContain('width="1200"');
    expect(svg).toContain('height="600"');
  });

  it("defaults to 900x400 dimensions", () => {
    const data: DataPoint[] = [
      makeDataPoint("2024-01-01T00:00:00Z", 10),
      makeDataPoint("2024-01-01T01:00:00Z", 20),
    ];
    const svg = renderSvgChart(data, { title: "Default", ylabel: "val" });

    expect(svg).toContain('width="900"');
    expect(svg).toContain('height="400"');
  });

  it("handles single data point (no path rendered)", () => {
    const data: DataPoint[] = [
      makeDataPoint("2024-01-01T00:00:00Z", 42, { env: "prod" }),
    ];
    const svg = renderSvgChart(data, { title: "Single", ylabel: "val" });

    expect(svg).toContain("<svg");
    // Single point series should not produce a path (needs >= 2 points)
    const pathCount = (svg.match(/<path /g) || []).length;
    expect(pathCount).toBe(0);
  });

  it("limits legend to 10 series", () => {
    const data: DataPoint[] = [];
    for (let i = 0; i < 12; i++) {
      data.push(makeDataPoint("2024-01-01T00:00:00Z", i * 10, { id: `s${i}` }));
      data.push(makeDataPoint("2024-01-01T01:00:00Z", i * 10 + 5, { id: `s${i}` }));
    }
    const svg = renderSvgChart(data, { title: "Many", ylabel: "val" });

    // Legend entries (rect elements after the plot border)
    // Should cap at 10 based on the loop limit
    const legendEntries = (svg.match(/id=s\d+/g) || []).length;
    expect(legendEntries).toBeLessThanOrEqual(10);
  });

  it("escapes XML special characters in title", () => {
    const data: DataPoint[] = [
      makeDataPoint("2024-01-01T00:00:00Z", 10),
      makeDataPoint("2024-01-01T01:00:00Z", 20),
    ];
    const svg = renderSvgChart(data, {
      title: 'Test <script> & "quotes"',
      ylabel: "val",
    });

    expect(svg).not.toContain("<script>");
    expect(svg).toContain("&lt;script&gt;");
    expect(svg).toContain("&amp;");
    expect(svg).toContain("&quot;");
  });

  it("handles all identical values (flat line)", () => {
    const data: DataPoint[] = [
      makeDataPoint("2024-01-01T00:00:00Z", 50),
      makeDataPoint("2024-01-01T06:00:00Z", 50),
      makeDataPoint("2024-01-01T12:00:00Z", 50),
    ];
    const svg = renderSvgChart(data, { title: "Flat", ylabel: "val" });

    expect(svg).toContain("<svg");
    expect(svg).toContain("<path");
  });

  it("handles very large values", () => {
    const data: DataPoint[] = [
      makeDataPoint("2024-01-01T00:00:00Z", 1_000_000),
      makeDataPoint("2024-01-01T01:00:00Z", 2_000_000),
    ];
    const svg = renderSvgChart(data, { title: "Large", ylabel: "count" });

    expect(svg).toContain("<svg");
    // Large values should use toFixed(0) format
    expect(svg).toMatch(/\d{6,}/);
  });

  it("handles very small values", () => {
    const data: DataPoint[] = [
      makeDataPoint("2024-01-01T00:00:00Z", 0.00012),
      makeDataPoint("2024-01-01T01:00:00Z", 0.00034),
    ];
    const svg = renderSvgChart(data, { title: "Small", ylabel: "rate" });

    expect(svg).toContain("<svg");
    // Small values should use toFixed(4) format
    expect(svg).toMatch(/0\.000\d/);
  });

  it("renders grid lines", () => {
    const data: DataPoint[] = [
      makeDataPoint("2024-01-01T00:00:00Z", 10),
      makeDataPoint("2024-01-01T12:00:00Z", 100),
    ];
    const svg = renderSvgChart(data, { title: "Grid", ylabel: "val" });

    // Should have grid lines (stroke="#e0e0e0")
    expect(svg).toContain('stroke="#e0e0e0"');
  });

  it("renders multiple tag dimensions in legend", () => {
    const data: DataPoint[] = [
      makeDataPoint("2024-01-01T00:00:00Z", 10, { model: "opus", env: "prod" }),
      makeDataPoint("2024-01-01T01:00:00Z", 20, { model: "opus", env: "prod" }),
    ];
    const svg = renderSvgChart(data, { title: "Tags", ylabel: "val" });

    expect(svg).toContain("model=opus");
    expect(svg).toContain("env=prod");
  });
});
