/**
 * SVG chart generator for Atlas metrics.
 * Renders time-series data as inline SVG — no external deps needed.
 * Matches Atlas chart palette and dimensional series model.
 */

const PALETTE = [
  "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
  "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
];

interface DataPoint {
  recorded_at: string;
  value: number;
  tags: Record<string, string>;
}

interface ChartOptions {
  title: string;
  ylabel: string;
  width?: number;
  height?: number;
}

interface Series {
  label: string;
  points: { t: number; v: number }[];
  color: string;
}

function groupIntoSeries(data: DataPoint[]): Series[] {
  const groups = new Map<string, { tags: Record<string, string>; points: { t: number; v: number }[] }>();

  for (const d of data) {
    const key = JSON.stringify(d.tags);
    if (!groups.has(key)) {
      groups.set(key, { tags: d.tags, points: [] });
    }
    groups.get(key)!.points.push({
      t: new Date(d.recorded_at).getTime(),
      v: d.value,
    });
  }

  let idx = 0;
  const series: Series[] = [];
  for (const [, g] of groups) {
    g.points.sort((a, b) => a.t - b.t);
    const label = Object.entries(g.tags)
      .map(([k, v]) => `${k}=${v}`)
      .join(", ");
    series.push({
      label,
      points: g.points,
      color: PALETTE[idx % PALETTE.length],
    });
    idx++;
  }
  return series;
}

function formatValue(v: number): string {
  if (Math.abs(v) >= 1000) return v.toFixed(0);
  if (Math.abs(v) >= 1) return v.toFixed(2);
  return v.toFixed(4);
}

function formatTime(ms: number): string {
  const d = new Date(ms);
  return `${d.getUTCMonth() + 1}/${d.getUTCDate()} ${String(d.getUTCHours()).padStart(2, "0")}:${String(d.getUTCMinutes()).padStart(2, "0")}`;
}

export function renderSvgChart(data: DataPoint[], options: ChartOptions): string {
  const W = options.width || 900;
  const H = options.height || 400;
  const margin = { top: 40, right: 20, bottom: 80, left: 70 };
  const plotW = W - margin.left - margin.right;
  const plotH = H - margin.top - margin.bottom;

  const allSeries = groupIntoSeries(data);
  if (allSeries.length === 0) {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">
      <text x="${W / 2}" y="${H / 2}" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#666">No data</text>
    </svg>`;
  }

  // Compute global bounds
  let minT = Infinity, maxT = -Infinity, minV = Infinity, maxV = -Infinity;
  for (const s of allSeries) {
    for (const p of s.points) {
      if (p.t < minT) minT = p.t;
      if (p.t > maxT) maxT = p.t;
      if (p.v < minV) minV = p.v;
      if (p.v > maxV) maxV = p.v;
    }
  }

  // Add 5% padding to y-axis
  const yRange = maxV - minV || 1;
  minV -= yRange * 0.05;
  maxV += yRange * 0.05;
  const tRange = maxT - minT || 1;

  function xScale(t: number): number {
    return margin.left + ((t - minT) / tRange) * plotW;
  }
  function yScale(v: number): number {
    return margin.top + plotH - ((v - minV) / (maxV - minV)) * plotH;
  }

  // Build SVG
  const parts: string[] = [];
  parts.push(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">`);
  parts.push(`<style>text{font-family:"Helvetica Neue",Arial,sans-serif}line,path{shape-rendering:crispEdges}</style>`);
  parts.push(`<rect width="${W}" height="${H}" fill="#fafafa" rx="4"/>`);

  // Title
  parts.push(`<text x="${W / 2}" y="24" text-anchor="middle" font-size="14" font-weight="bold" fill="#333">${escapeXml(options.title)}</text>`);

  // Y-axis label
  parts.push(`<text x="14" y="${margin.top + plotH / 2}" text-anchor="middle" font-size="11" fill="#666" transform="rotate(-90,14,${margin.top + plotH / 2})">${escapeXml(options.ylabel)}</text>`);

  // Grid lines + y-axis ticks
  const yTicks = 5;
  for (let i = 0; i <= yTicks; i++) {
    const v = minV + (i / yTicks) * (maxV - minV);
    const y = yScale(v);
    parts.push(`<line x1="${margin.left}" y1="${y}" x2="${margin.left + plotW}" y2="${y}" stroke="#e0e0e0" stroke-width="1"/>`);
    parts.push(`<text x="${margin.left - 8}" y="${y + 4}" text-anchor="end" font-size="10" fill="#666">${formatValue(v)}</text>`);
  }

  // X-axis ticks
  const xTicks = Math.min(6, Math.floor(plotW / 120));
  for (let i = 0; i <= xTicks; i++) {
    const t = minT + (i / xTicks) * tRange;
    const x = xScale(t);
    parts.push(`<line x1="${x}" y1="${margin.top}" x2="${x}" y2="${margin.top + plotH}" stroke="#e8e8e8" stroke-width="1"/>`);
    parts.push(`<text x="${x}" y="${margin.top + plotH + 16}" text-anchor="middle" font-size="10" fill="#666">${formatTime(t)}</text>`);
  }

  // Plot border
  parts.push(`<rect x="${margin.left}" y="${margin.top}" width="${plotW}" height="${plotH}" fill="none" stroke="#ccc" stroke-width="1"/>`);

  // Series lines
  for (const s of allSeries) {
    if (s.points.length < 2) continue;
    const pathParts = s.points.map((p, i) => {
      const x = xScale(p.t);
      const y = yScale(p.v);
      return i === 0 ? `M${x.toFixed(1)},${y.toFixed(1)}` : `L${x.toFixed(1)},${y.toFixed(1)}`;
    });
    parts.push(`<path d="${pathParts.join("")}" fill="none" stroke="${s.color}" stroke-width="1.5" stroke-linejoin="round" style="shape-rendering:auto"/>`);
  }

  // Legend
  const legendY = margin.top + plotH + 35;
  const legendX = margin.left;
  const lineHeight = 16;
  for (let i = 0; i < allSeries.length && i < 10; i++) {
    const s = allSeries[i];
    const y = legendY + i * lineHeight;
    parts.push(`<rect x="${legendX}" y="${y - 8}" width="12" height="3" fill="${s.color}"/>`);
    parts.push(`<text x="${legendX + 16}" y="${y - 4}" font-size="10" fill="#444">${escapeXml(s.label)}</text>`);
  }

  parts.push("</svg>");
  return parts.join("\n");
}

function escapeXml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
