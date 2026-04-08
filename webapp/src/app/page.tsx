"use client";

import { motion, AnimatePresence } from "motion/react";
import { useState } from "react";

const AGENTS = [
  {
    name: "security-auditor",
    model: "opus",
    color: "#ff4444",
    desc: "Glasswing-depth vulnerability scanning. Prompt injection, sandbox escape, exploit chains.",
    repos: ["auditing-agents", "finetuning-auditor", "lie-detector", "SCONE-bench"],
  },
  {
    name: "alignment-auditor",
    model: "opus",
    color: "#c8ff00",
    desc: "Petri 2.0 methodology — 2,300 investigation sessions. Suspicion scoring 0-100.",
    repos: ["petri", "trusted-monitor", "SHADE-Arena", "ciphered-reasoning-llms"],
  },
  {
    name: "eval-builder",
    model: "sonnet",
    color: "#00d4ff",
    desc: "Behavioral eval suites via bloom. 46 deception tasks from lie-detector.",
    repos: ["bloom", "impossiblebench", "A3", "open-source-alignment-faking"],
  },
  {
    name: "prompt-hardener",
    model: "sonnet",
    color: "#ff9500",
    desc: "Inoculation-prompting, role-anchoring, persona-steering defense.",
    repos: ["inoculation-prompting", "persona_vectors"],
  },
  {
    name: "code-generator",
    model: "sonnet",
    color: "#34d399",
    desc: "Python & TypeScript codegen for Claude Agent SDK applications.",
    repos: [],
  },
  {
    name: "harmlessness-screen",
    model: "haiku",
    color: "#a78bfa",
    desc: "Ultra-fast classification. Ciphered reasoning + persona-steering detection.",
    repos: ["assistant-axis", "ciphered-reasoning-llms", "persona_vectors"],
  },
];

const PIPELINES = [
  { name: "standard-codegen", steps: ["harmlessness-screen", "code-generator", "security-auditor ∥ test-runner", "alignment-auditor"] },
  { name: "security-deep-scan", steps: ["security-auditor", "prompt-hardener", "architecture-reviewer"] },
  { name: "prompt-hardening", steps: ["prompt-hardener", "security-auditor", "↻ iterate"] },
  { name: "eval-suite-creation", steps: ["eval-builder", "test-runner"] },
];

const STATS = [
  { label: "safety-research repos", value: "18", suffix: "" },
  { label: "agent configurations", value: "8", suffix: "" },
  { label: "pipeline definitions", value: "5", suffix: "" },
  { label: "Mythos destructive rate", value: "0.3", suffix: "%" },
];

function AsciiDivider() {
  return (
    <div className="font-mono text-[var(--muted)] text-xs opacity-40 select-none overflow-hidden whitespace-nowrap">
      {"─".repeat(120)}
    </div>
  );
}

function AgentCard({
  agent,
  index,
  isSelected,
  onClick,
}: {
  agent: (typeof AGENTS)[0];
  index: number;
  isSelected: boolean;
  onClick: () => void;
}) {
  return (
    <motion.button
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.08, duration: 0.5 }}
      whileHover={{ scale: 1.02, borderColor: agent.color + "40" }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={`group relative w-full text-left p-6 rounded-none border transition-all duration-300 cursor-pointer ${
        isSelected
          ? "border-[var(--accent)]/30 bg-[var(--surface-raised)]"
          : "border-[var(--border)] bg-[var(--surface)] hover:bg-[var(--surface-raised)]"
      }`}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-3 mb-2">
            <span
              className="inline-block w-2 h-2 rounded-full"
              style={{ backgroundColor: agent.color }}
            />
            <span className="font-mono text-sm font-medium text-[var(--fg)]">
              {agent.name}
            </span>
            <span className="font-mono text-xs px-2 py-0.5 bg-white/5 text-[var(--muted)]">
              {agent.model}
            </span>
          </div>
          <p className="font-serif text-sm text-[var(--muted)] leading-relaxed">
            {agent.desc}
          </p>
        </div>
        <motion.span
          animate={{ rotate: isSelected ? 45 : 0 }}
          className="font-mono text-lg text-[var(--muted)] group-hover:text-[var(--accent)] transition-colors shrink-0"
        >
          +
        </motion.span>
      </div>

      <AnimatePresence>
        {isSelected && agent.repos.length > 0 && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="mt-4 pt-4 border-t border-[var(--border)]">
              <span className="font-mono text-xs text-[var(--accent-dim)] mb-2 block">
                // safety-research tooling
              </span>
              <div className="flex flex-wrap gap-2">
                {agent.repos.map((repo) => (
                  <span
                    key={repo}
                    className="font-mono text-xs px-2 py-1 bg-[var(--accent)]/5 text-[var(--accent)] border border-[var(--accent)]/10"
                  >
                    {repo}
                  </span>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.button>
  );
}

export default function Home() {
  const [selectedAgent, setSelectedAgent] = useState<number | null>(null);

  return (
    <div className="min-h-screen bg-[var(--bg)] relative">
      {/* ── Hero ─────────────────────────────────────────── */}
      <section className="relative min-h-screen flex flex-col justify-center px-8 md:px-16 lg:px-24 overflow-hidden">
        {/* Background grid */}
        <div
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage:
              "linear-gradient(var(--muted) 1px, transparent 1px), linear-gradient(90deg, var(--muted) 1px, transparent 1px)",
            backgroundSize: "60px 60px",
          }}
        />

        {/* Accent glow */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 2, delay: 0.5 }}
          className="absolute top-1/4 -right-32 w-[500px] h-[500px] rounded-full blur-[150px] pointer-events-none"
          style={{ background: "radial-gradient(circle, var(--glow), transparent 70%)" }}
        />

        <div className="relative z-10 max-w-5xl">
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="font-mono text-xs text-[var(--accent-dim)] mb-6 tracking-widest uppercase"
          >
            ┌ opus 4.6 orchestrator ┐
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.1 }}
            className="font-sans text-5xl md:text-7xl lg:text-8xl font-extrabold tracking-tighter leading-[0.95] mb-8"
          >
            agent
            <br />
            <span className="text-[var(--accent)]">streams</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.3 }}
            className="font-serif text-xl md:text-2xl text-[var(--muted)] max-w-2xl leading-relaxed italic"
          >
            Safety-grounded multi-agent orchestration with Mythos-grade
            methodology. Composable pipelines across codegen, security,
            alignment, and evaluation — powered by 18 open-source
            safety-research tools.
          </motion.p>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="mt-12 flex gap-4"
          >
            <a
              href="#agents"
              className="group font-mono text-sm px-6 py-3 bg-[var(--accent)] text-[var(--bg)] font-medium hover:bg-[var(--accent)]/90 transition-colors"
            >
              Explore agents{" "}
              <span className="inline-block transition-transform group-hover:translate-x-1">
                →
              </span>
            </a>
            <a
              href="#pipelines"
              className="font-mono text-sm px-6 py-3 border border-[var(--border)] text-[var(--fg)] hover:border-[var(--border-hover)] transition-colors"
            >
              View pipelines
            </a>
          </motion.div>
        </div>

        {/* Scroll indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.4, y: [0, 8, 0] }}
          transition={{ opacity: { delay: 1.5 }, y: { repeat: Infinity, duration: 2 } }}
          className="absolute bottom-12 left-1/2 -translate-x-1/2 font-mono text-xs text-[var(--muted)]"
        >
          ↓ scroll
        </motion.div>
      </section>

      {/* ── Stats bar ────────────────────────────────────── */}
      <section className="border-y border-[var(--border)] bg-[var(--surface)]">
        <div className="max-w-7xl mx-auto px-8 md:px-16 py-8 grid grid-cols-2 md:grid-cols-4 gap-8">
          {STATS.map((stat, i) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="text-center md:text-left"
            >
              <div className="font-sans text-3xl md:text-4xl font-bold text-[var(--accent)] tabular-nums">
                {stat.value}
                <span className="text-lg text-[var(--accent-dim)]">{stat.suffix}</span>
              </div>
              <div className="font-mono text-xs text-[var(--muted)] mt-1 tracking-wide">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── Agents ───────────────────────────────────────── */}
      <section id="agents" className="max-w-7xl mx-auto px-8 md:px-16 py-24">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mb-12"
        >
          <span className="font-mono text-xs text-[var(--accent-dim)] tracking-widest uppercase block mb-3">
            // subagent roster
          </span>
          <h2 className="font-sans text-4xl md:text-5xl font-bold tracking-tight">
            Agent configurations
          </h2>
          <p className="font-serif text-lg text-[var(--muted)] mt-4 max-w-xl italic">
            Each agent runs in isolated context with least-privilege tool grants,
            grounded in open-source safety-research methodology.
          </p>
        </motion.div>

        <AsciiDivider />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-px mt-8 bg-[var(--border)]">
          {AGENTS.map((agent, i) => (
            <AgentCard
              key={agent.name}
              agent={agent}
              index={i}
              isSelected={selectedAgent === i}
              onClick={() => setSelectedAgent(selectedAgent === i ? null : i)}
            />
          ))}
        </div>
      </section>

      {/* ── Pipelines ────────────────────────────────────── */}
      <section id="pipelines" className="border-t border-[var(--border)] bg-[var(--surface)]">
        <div className="max-w-7xl mx-auto px-8 md:px-16 py-24">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="mb-12"
          >
            <span className="font-mono text-xs text-[var(--accent-dim)] tracking-widest uppercase block mb-3">
              // composable workflows
            </span>
            <h2 className="font-sans text-4xl md:text-5xl font-bold tracking-tight">
              Pipeline definitions
            </h2>
          </motion.div>

          <div className="space-y-6">
            {PIPELINES.map((pipeline, i) => (
              <motion.div
                key={pipeline.name}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="group p-6 border border-[var(--border)] hover:border-[var(--border-hover)] transition-colors"
              >
                <div className="flex items-start justify-between gap-4 mb-4">
                  <h3 className="font-mono text-base font-medium text-[var(--fg)]">
                    {pipeline.name}
                  </h3>
                  <span className="font-mono text-xs text-[var(--muted)]">
                    {pipeline.steps.length} steps
                  </span>
                </div>
                <div className="flex items-center gap-2 flex-wrap">
                  {pipeline.steps.map((step, j) => (
                    <div key={j} className="flex items-center gap-2">
                      <span className="font-mono text-xs px-3 py-1.5 bg-[var(--accent)]/5 text-[var(--accent)] border border-[var(--accent)]/10">
                        {step}
                      </span>
                      {j < pipeline.steps.length - 1 && (
                        <span className="font-mono text-[var(--muted)] text-xs">→</span>
                      )}
                    </div>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Model hierarchy ──────────────────────────────── */}
      <section className="max-w-7xl mx-auto px-8 md:px-16 py-24">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mb-12"
        >
          <span className="font-mono text-xs text-[var(--accent-dim)] tracking-widest uppercase block mb-3">
            // model selection
          </span>
          <h2 className="font-sans text-4xl md:text-5xl font-bold tracking-tight">
            Model hierarchy
          </h2>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            {
              tier: "opus",
              model: "claude-opus-4-6",
              role: "Complex reasoning, security audit, alignment",
              bench: "SWE-bench 80.8% · GPQA 91.3%",
              agents: ["security-auditor", "alignment-auditor", "architecture-reviewer"],
              accent: "#c8ff00",
            },
            {
              tier: "sonnet",
              model: "claude-sonnet-4-6",
              role: "Fast codegen, test execution, prompt hardening",
              bench: "CyberGym 0.65",
              agents: ["code-generator", "test-runner", "prompt-hardener", "eval-builder"],
              accent: "#00d4ff",
            },
            {
              tier: "haiku",
              model: "claude-haiku-4-5",
              role: "Ultra-fast screening, classification",
              bench: "Fastest response latency",
              agents: ["harmlessness-screen"],
              accent: "#a78bfa",
            },
          ].map((model, i) => (
            <motion.div
              key={model.tier}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.15 }}
              className="p-6 border border-[var(--border)] bg-[var(--surface)] relative overflow-hidden"
            >
              <div
                className="absolute top-0 left-0 w-full h-px"
                style={{ background: `linear-gradient(90deg, ${model.accent}, transparent)` }}
              />
              <div className="font-mono text-2xl font-bold mb-1" style={{ color: model.accent }}>
                {model.tier}
              </div>
              <div className="font-mono text-xs text-[var(--muted)] mb-4">{model.model}</div>
              <p className="font-serif text-sm text-[var(--fg)]/70 mb-4">{model.role}</p>
              <div className="font-mono text-xs text-[var(--accent-dim)] mb-3">{model.bench}</div>
              <div className="flex flex-wrap gap-1">
                {model.agents.map((a) => (
                  <span
                    key={a}
                    className="font-mono text-[10px] px-1.5 py-0.5 bg-white/5 text-[var(--muted)]"
                  >
                    {a}
                  </span>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── Footer ───────────────────────────────────────── */}
      <footer className="border-t border-[var(--border)] py-12 px-8 md:px-16">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="font-mono text-xs text-[var(--muted)]">
            agentstreams · safety-grounded orchestration
          </div>
          <div className="font-mono text-xs text-[var(--muted)] flex gap-6">
            <span>claude-opus-4-6</span>
            <span>·</span>
            <span>18 safety-research repos</span>
            <span>·</span>
            <span>mythos methodology</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
