"use client";

import { motion, AnimatePresence } from "motion/react";
import { useState, useEffect, useRef, useCallback } from "react";

// ── ASCII character ramps (ASC11-style) ──────────────────────
const RAMPS = {
  standard: " .:-=+*#%@",
  blocks: " ░▒▓█",
  minimal: " ·•●",
  binary: " █",
  braille: " ⠁⠃⠇⡇⡿⣿",
} as const;

type RampKey = keyof typeof RAMPS;

// ── MemPalace wing definitions ───────────────────────────────
const WINGS = [
  { id: "ontology", label: "ontology/", desc: "UDA source of truth", color: "#c8ff00", files: 12 },
  { id: "src", label: "src/", desc: "Programmatic tools", color: "#00d4ff", files: 8 },
  { id: "scripts", label: "scripts/", desc: "CLI crawlers", color: "#ff9500", files: 16 },
  { id: "skills", label: "skills/", desc: "8 languages", color: "#34d399", files: 24 },
  { id: "claude", label: ".claude/", desc: "Agent manifests", color: "#a78bfa", files: 30 },
  { id: "webapp", label: "webapp/", desc: "Next.js 16", color: "#ff4444", files: 6 },
  { id: "github", label: ".github/", desc: "CI/CD workflows", color: "#ff66b2", files: 9 },
  { id: "evals", label: "evals/", desc: "Promptfoo suites", color: "#ffd700", files: 4 },
] as const;

// ── ASCII art renderer (canvas-based, ASC11 technique) ───────
function AsciiCanvas({
  text,
  width = 80,
  ramp = "standard",
  accentColor = "#c8ff00",
}: {
  text: string;
  width?: number;
  ramp?: RampKey;
  accentColor?: string;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const chars = RAMPS[ramp];

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const lines = text.split("\n");
    const maxCols = Math.max(...lines.map((l) => l.length), width);
    const rows = lines.length;

    const charW = 8;
    const charH = 14;
    canvas.width = maxCols * charW;
    canvas.height = rows * charH;

    ctx.fillStyle = "#050505";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.font = "12px 'SF Mono', 'Cascadia Code', monospace";
    ctx.textBaseline = "top";

    for (let y = 0; y < rows; y++) {
      const line = lines[y] || "";
      for (let x = 0; x < line.length; x++) {
        const ch = line[x];
        // Color special characters
        if ("═║╔╗╚╝╠╣╦╩╬┌┐└┘├┤┬┴┼─│".includes(ch)) {
          ctx.fillStyle = accentColor + "80";
        } else if ("●★→←↑↓▶◀∥↻".includes(ch)) {
          ctx.fillStyle = accentColor;
        } else if (ch === "#" || ch === "@" || ch === "%") {
          ctx.fillStyle = "#e8e6e3";
        } else {
          ctx.fillStyle = "#6b6b6b";
        }
        ctx.fillText(ch, x * charW, y * charH + 1);
      }
    }
  }, [text, width, ramp, accentColor, chars]);

  return (
    <canvas
      ref={canvasRef}
      className="block max-w-full h-auto"
      style={{ imageRendering: "pixelated" }}
    />
  );
}

// ── Procedural ASCII art generators ──────────────────────────
function generateWingMap(seed: number): string {
  const rng = mulberry32(seed);
  const w = 72;
  const h = 24;
  const grid: string[][] = Array.from({ length: h }, () =>
    Array(w).fill(" ")
  );

  // Draw wings as connected boxes
  WINGS.forEach((wing, i) => {
    const col = (i % 4) * 18 + 1;
    const row = Math.floor(i / 4) * 10 + 1;
    const bw = 16;
    const bh = 7;

    // Box border
    for (let x = col; x < col + bw && x < w; x++) {
      if (row < h) grid[row][x] = "─";
      if (row + bh - 1 < h) grid[row + bh - 1][x] = "─";
    }
    for (let y = row; y < row + bh && y < h; y++) {
      if (col < w) grid[y][col] = "│";
      if (col + bw - 1 < w) grid[y][col + bw - 1] = "│";
    }
    if (row < h && col < w) grid[row][col] = "┌";
    if (row < h && col + bw - 1 < w) grid[row][col + bw - 1] = "┐";
    if (row + bh - 1 < h && col < w) grid[row + bh - 1][col] = "└";
    if (row + bh - 1 < h && col + bw - 1 < w) grid[row + bh - 1][col + bw - 1] = "┘";

    // Label
    const label = wing.label.slice(0, 14);
    for (let c = 0; c < label.length; c++) {
      if (row + 2 < h && col + 2 + c < w) grid[row + 2][col + 2 + c] = label[c];
    }
    // File count
    const count = `${wing.files} files`;
    for (let c = 0; c < count.length; c++) {
      if (row + 4 < h && col + 2 + c < w) grid[row + 4][col + 2 + c] = count[c];
    }

    // Tunnel connections (random based on seed)
    if (i < WINGS.length - 1 && i % 4 !== 3) {
      const tunnelY = row + 3;
      if (tunnelY < h && col + bw < w) {
        grid[tunnelY][col + bw] = "─";
        if (col + bw + 1 < w) grid[tunnelY][col + bw + 1] = "→";
      }
    }
  });

  // Scatter noise particles (ASC11 texture feel)
  const noiseChars = "·.,:;";
  for (let i = 0; i < 30; i++) {
    const x = Math.floor(rng() * w);
    const y = Math.floor(rng() * h);
    if (grid[y][x] === " ") {
      grid[y][x] = noiseChars[Math.floor(rng() * noiseChars.length)];
    }
  }

  return grid.map((row) => row.join("")).join("\n");
}

function generatePipelineFlow(seed: number): string {
  const steps = [
    ["screen", "haiku"],
    ["codegen", "sonnet"],
    ["security ∥ test", "opus ∥ sonnet"],
    ["alignment", "opus"],
  ];
  const lines: string[] = [
    "  ╔══════════════════════════════════════════════════╗",
    "  ║  standard-codegen pipeline                      ║",
    "  ╚══════════════════════════════════════════════════╝",
    "",
  ];

  steps.forEach(([name, model], i) => {
    const box = `┌${"─".repeat(name.length + 2)}┐`;
    const mid = `│ ${name} │`;
    const bot = `└${"─".repeat(name.length + 2)}┘`;
    const pad = "  " + "          ".repeat(i);

    lines.push(`${pad}${box}  [${model}]`);
    lines.push(`${pad}${mid}`);
    lines.push(`${pad}${bot}`);
    if (i < steps.length - 1) {
      lines.push(`${pad}  ${"  ".repeat(Math.floor(name.length / 2))}↓`);
    }
  });

  return lines.join("\n");
}

function generateAgentMatrix(seed: number): string {
  const rng = mulberry32(seed);
  const agents = [
    { name: "security-auditor", model: "opus", repos: 6 },
    { name: "alignment-auditor", model: "opus", repos: 8 },
    { name: "architecture-rev", model: "opus", repos: 3 },
    { name: "code-generator", model: "sonnet", repos: 0 },
    { name: "test-runner", model: "sonnet", repos: 0 },
    { name: "prompt-hardener", model: "sonnet", repos: 2 },
    { name: "eval-builder", model: "sonnet", repos: 6 },
    { name: "harmless-screen", model: "haiku", repos: 3 },
  ];

  const lines: string[] = [
    "  ┌──────────────────┬────────┬───────┬" + "─".repeat(20) + "┐",
    "  │ Agent            │ Model  │ Repos │ Boundary           │",
    "  ├──────────────────┼────────┼───────┼" + "─".repeat(20) + "┤",
  ];

  agents.forEach((a) => {
    const bar = "█".repeat(Math.min(a.repos * 2, 18));
    const pad = " ".repeat(18 - bar.length);
    lines.push(
      `  │ ${a.name.padEnd(16)} │ ${a.model.padEnd(6)} │  ${String(a.repos).padStart(2)}   │ ${bar}${pad} │`
    );
  });

  lines.push(
    "  └──────────────────┴────────┴───────┴" + "─".repeat(20) + "┘"
  );
  lines.push(`  seed: ${seed}  ·  18 safety-research repos  ·  4 model tiers`);

  return lines.join("\n");
}

// ── Seeded PRNG (mulberry32) ─────────────────────────────────
function mulberry32(a: number) {
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ── Art pieces tied to PR features ───────────────────────────
const ART_PIECES = [
  {
    id: "wings",
    title: "MemPalace Wings",
    desc: "8 wings of the Memory Palace — file domains connected by tunnels",
    generate: generateWingMap,
    color: "#c8ff00",
  },
  {
    id: "pipeline",
    title: "Pipeline Flow",
    desc: "standard-codegen pipeline — 4 steps through the orchestrator",
    generate: generatePipelineFlow,
    color: "#00d4ff",
  },
  {
    id: "agents",
    title: "Agent Matrix",
    desc: "8 agents with model tiers and safety-research repo counts",
    generate: generateAgentMatrix,
    color: "#ff9500",
  },
];

// ── Main page ────────────────────────────────────────────────
export default function ArtPage() {
  const [seed, setSeed] = useState(42);
  const [selectedPiece, setSelectedPiece] = useState(0);
  const [ramp, setRamp] = useState<RampKey>("standard");

  const piece = ART_PIECES[selectedPiece];
  const asciiText = piece.generate(seed);

  const nextSeed = useCallback(() => setSeed((s) => s + 1), []);
  const prevSeed = useCallback(() => setSeed((s) => Math.max(1, s - 1)), []);
  const randomSeed = useCallback(
    () => setSeed(Math.floor(Math.random() * 99999) + 1),
    []
  );

  return (
    <div className="min-h-screen bg-[var(--bg)]">
      {/* Header */}
      <header className="border-b border-[var(--border)] px-8 py-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <a href="/" className="font-mono text-xs text-[var(--accent-dim)] hover:text-[var(--accent)] transition-colors">
              ← agentstreams
            </a>
            <h1 className="font-sans text-3xl font-bold tracking-tight mt-1">
              art<span className="text-[var(--accent)]">/</span>
            </h1>
            <p className="font-serif text-sm text-[var(--muted)] italic mt-1">
              ASCII architecture diagrams — MemPalace visualization layer
            </p>
          </div>
          <div className="flex items-center gap-4">
            <span className="font-mono text-xs text-[var(--muted)]">
              seed: {seed}
            </span>
            <div className="flex gap-1">
              <button
                onClick={prevSeed}
                className="font-mono text-xs px-2 py-1 border border-[var(--border)] text-[var(--muted)] hover:text-[var(--fg)] hover:border-[var(--border-hover)] transition-colors"
              >
                ←
              </button>
              <button
                onClick={nextSeed}
                className="font-mono text-xs px-2 py-1 border border-[var(--border)] text-[var(--muted)] hover:text-[var(--fg)] hover:border-[var(--border-hover)] transition-colors"
              >
                →
              </button>
              <button
                onClick={randomSeed}
                className="font-mono text-xs px-2 py-1 border border-[var(--border)] text-[var(--accent-dim)] hover:text-[var(--accent)] hover:border-[var(--accent)]/30 transition-colors"
              >
                random
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-8 py-8 grid grid-cols-1 lg:grid-cols-[1fr_280px] gap-8">
        {/* Main canvas area */}
        <div>
          <AnimatePresence mode="wait">
            <motion.div
              key={`${selectedPiece}-${seed}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3 }}
              className="border border-[var(--border)] bg-[var(--surface)] p-6 overflow-x-auto"
            >
              <AsciiCanvas
                text={asciiText}
                accentColor={piece.color}
                ramp={ramp}
              />
            </motion.div>
          </AnimatePresence>

          {/* Raw text view */}
          <details className="mt-4">
            <summary className="font-mono text-xs text-[var(--muted)] cursor-pointer hover:text-[var(--fg)]">
              // raw text
            </summary>
            <pre className="mt-2 p-4 bg-[var(--surface)] border border-[var(--border)] text-xs text-[var(--muted)] overflow-x-auto font-mono leading-snug">
              {asciiText}
            </pre>
          </details>
        </div>

        {/* Sidebar */}
        <aside className="space-y-6">
          {/* Piece selector */}
          <div>
            <span className="font-mono text-xs text-[var(--accent-dim)] tracking-widest uppercase block mb-3">
              // visualization
            </span>
            <div className="space-y-2">
              {ART_PIECES.map((p, i) => (
                <button
                  key={p.id}
                  onClick={() => setSelectedPiece(i)}
                  className={`w-full text-left p-3 border transition-all ${
                    selectedPiece === i
                      ? "border-[var(--accent)]/30 bg-[var(--surface-raised)]"
                      : "border-[var(--border)] bg-[var(--surface)] hover:bg-[var(--surface-raised)]"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <span
                      className="w-2 h-2 rounded-full"
                      style={{ backgroundColor: p.color }}
                    />
                    <span className="font-mono text-sm">{p.title}</span>
                  </div>
                  <p className="font-serif text-xs text-[var(--muted)] mt-1 italic">
                    {p.desc}
                  </p>
                </button>
              ))}
            </div>
          </div>

          {/* Ramp selector */}
          <div>
            <span className="font-mono text-xs text-[var(--accent-dim)] tracking-widest uppercase block mb-3">
              // character ramp
            </span>
            <div className="space-y-1">
              {(Object.keys(RAMPS) as RampKey[]).map((r) => (
                <button
                  key={r}
                  onClick={() => setRamp(r)}
                  className={`w-full text-left font-mono text-xs px-3 py-2 border transition-colors ${
                    ramp === r
                      ? "border-[var(--accent)]/30 text-[var(--accent)]"
                      : "border-[var(--border)] text-[var(--muted)] hover:text-[var(--fg)]"
                  }`}
                >
                  {r}: <span className="opacity-60">{RAMPS[r]}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Info */}
          <div className="border border-[var(--border)] p-4 bg-[var(--surface)]">
            <span className="font-mono text-xs text-[var(--accent-dim)] block mb-2">
              // about
            </span>
            <p className="font-serif text-xs text-[var(--muted)] leading-relaxed">
              ASCII architecture diagrams inspired by{" "}
              <span className="text-[var(--fg)]">asc11.com</span>. Each
              visualization renders the MemPalace structure — wings, halls, and
              tunnels — as interactive ASCII art with seeded variation.
            </p>
            <p className="font-mono text-[10px] text-[var(--muted)] mt-3">
              art/ folder: monotonically prefixed .txt files
            </p>
          </div>
        </aside>
      </div>
    </div>
  );
}
