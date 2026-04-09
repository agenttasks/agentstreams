"""Ecosystem registry — comprehensive catalog of all repos across 4 GitHub orgs.

Sourced via GitHub GraphQL/search API from:
  - anthropics (59 repos, 370K+ total ★)
  - modelcontextprotocol (39 repos, 163K+ total ★)
  - safety-research (35 repos, 3.5K+ total ★)
  - decoderesearch (3 repos, 4K+ total ★)

Maps every repo to a knowledge-work layer (1-8) and tracks dependencies
between repos that are relevant to the abstraction stack.

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Org(Enum):
    ANTHROPICS = "anthropics"
    MCP = "modelcontextprotocol"
    SAFETY = "safety-research"
    DECODE = "decoderesearch"


class Layer(Enum):
    """Which knowledge-work layer a repo maps to."""

    CIRCUITS = 1  # Feature circuits, interpretability
    TRACERS = 2  # Circuit tracing, attribution
    PROMPTS = 3  # Prompt engineering, templates
    TASKS = 4  # Task definitions, routing
    SUBTASKS = 5  # Subtask decomposition
    SUBAGENTS = 6  # Subagent orchestration
    HARNESS = 7  # Agent harness, runtime loop
    EVALS = 8  # Evaluation, benchmarking
    INFRA = 0  # Infrastructure (SDKs, MCP protocol)
    SAFETY = -1  # Safety research (cross-cutting)


@dataclass
class RepoEntry:
    """A single repository in the ecosystem."""

    org: Org
    name: str
    stars: int
    language: str = ""
    description: str = ""
    layer: Layer = Layer.INFRA
    topics: list[str] = field(default_factory=list)
    archived: bool = False

    @property
    def full_name(self) -> str:
        return f"{self.org.value}/{self.name}"

    @property
    def url(self) -> str:
        return f"https://github.com/{self.full_name}"


# ── Anthropics (59 repos) ──────────────────────────────────────
# Top repos by stars, mapped to layers

ANTHROPICS_REPOS = [
    # Core platforms
    RepoEntry(
        Org.ANTHROPICS,
        "skills",
        113689,
        "Python",
        "Public repository for Agent Skills",
        Layer.TASKS,
        ["agent-skills"],
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "claude-code",
        111531,
        "Shell",
        "Agentic coding tool in your terminal",
        Layer.HARNESS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "claude-cookbooks",
        37754,
        "Jupyter Notebook",
        "Recipes showcasing effective ways of using Claude",
        Layer.PROMPTS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "prompt-eng-interactive-tutorial",
        34507,
        "Jupyter Notebook",
        "Anthropic's Interactive Prompt Engineering Tutorial",
        Layer.PROMPTS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "courses",
        20329,
        "Jupyter Notebook",
        "Anthropic's educational courses",
        Layer.PROMPTS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "claude-plugins-official",
        16439,
        "Python",
        "Official Anthropic-managed Claude Code Plugins",
        Layer.TASKS,
        ["claude-code", "mcp", "skills"],
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "claude-quickstarts",
        15977,
        "Python",
        "Quick-start deployable applications using Claude API",
        Layer.PROMPTS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "knowledge-work-plugins",
        11031,
        "Python",
        "Plugins for knowledge workers in Claude Cowork",
        Layer.TASKS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "financial-services-plugins",
        7372,
        "Python",
        "Financial services plugins for Claude Cowork",
        Layer.TASKS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "claude-code-action",
        6964,
        "TypeScript",
        "GitHub Action for Claude Code",
        Layer.HARNESS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "claude-agent-sdk-python",
        6230,
        "Python",
        "Python Agent SDK (query, hooks, subagents)",
        Layer.SUBAGENTS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "claude-code-security-review",
        4181,
        "Python",
        "AI security review GitHub Action",
        Layer.EVALS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "original_performance_takehome",
        3760,
        "Python",
        "Anthropic's original performance take-home",
        Layer.EVALS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "anthropic-sdk-python",
        3173,
        "Python",
        "Python SDK for Claude API",
        Layer.INFRA,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "claudes-c-compiler",
        2613,
        "Rust",
        "Claude Opus 4.6 wrote a C compiler in Rust",
        Layer.EVALS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "claude-agent-sdk-demos",
        2118,
        "TypeScript",
        "Claude Code SDK Demos",
        Layer.SUBAGENTS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "hh-rlhf",
        1837,
        "",
        "Human preference data for RLHF training",
        Layer.SAFETY,
        archived=True,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "anthropic-sdk-typescript",
        1827,
        "TypeScript",
        "TypeScript SDK for Claude API",
        Layer.INFRA,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "claude-agent-sdk-typescript",
        1255,
        "Shell",
        "TypeScript Agent SDK",
        Layer.SUBAGENTS,
    ),
    RepoEntry(Org.ANTHROPICS, "anthropic-sdk-go", 967, "Go", "Go SDK for Claude API", Layer.INFRA),
    RepoEntry(Org.ANTHROPICS, "evals", 365, "", "Evaluation datasets for Claude", Layer.EVALS),
    RepoEntry(
        Org.ANTHROPICS, "anthropic-sdk-ruby", 316, "Ruby", "Ruby SDK for Claude API", Layer.INFRA
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "life-sciences",
        299,
        "Python",
        "Claude for Life Sciences marketplace",
        Layer.TASKS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "anthropic-sdk-java",
        281,
        "Kotlin",
        "Java/Kotlin SDK for Claude API",
        Layer.INFRA,
    ),
    RepoEntry(Org.ANTHROPICS, "anthropic-cli", 253, "Go", "CLI for the Claude API", Layer.INFRA),
    RepoEntry(
        Org.ANTHROPICS, "anthropic-sdk-csharp", 224, "C#", "C# SDK for Claude API", Layer.INFRA
    ),
    RepoEntry(
        Org.ANTHROPICS, "anthropic-sdk-php", 134, "PHP", "PHP SDK for Claude API", Layer.INFRA
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "toy-models-of-superposition",
        144,
        "Jupyter Notebook",
        "Notebooks for Toy Models of Superposition paper",
        Layer.CIRCUITS,
        archived=True,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "sleeper-agents-paper",
        141,
        "",
        "Sleeper Agents: Training Deceptive LLMs",
        Layer.SAFETY,
        archived=True,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "political-neutrality-eval",
        124,
        "Python",
        "Political neutrality evaluation",
        Layer.EVALS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "attribution-graphs-frontend",
        96,
        "JavaScript",
        "Attribution graph visualization frontend",
        Layer.CIRCUITS,
        archived=True,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "claude-constitution",
        64,
        "",
        "Foundational document describing Claude's values",
        Layer.SAFETY,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "claude-plugins-community",
        36,
        "",
        "Community plugin marketplace for Claude Cowork",
        Layer.TASKS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "model-cards",
        19,
        "",
        "Supplementary materials for Claude Model Cards",
        Layer.EVALS,
    ),
    RepoEntry(
        Org.ANTHROPICS,
        "healthcare",
        193,
        "Python",
        "Claude for healthcare marketplace",
        Layer.TASKS,
    ),
]

# ── Model Context Protocol (39 repos) ──────────────────────────

MCP_REPOS = [
    RepoEntry(
        Org.MCP, "servers", 83300, "TypeScript", "Model Context Protocol Servers", Layer.HARNESS
    ),
    RepoEntry(Org.MCP, "python-sdk", 22561, "Python", "Official Python SDK for MCP", Layer.INFRA),
    RepoEntry(
        Org.MCP,
        "typescript-sdk",
        12146,
        "TypeScript",
        "Official TypeScript SDK for MCP",
        Layer.INFRA,
    ),
    RepoEntry(
        Org.MCP, "inspector", 9379, "TypeScript", "Visual testing tool for MCP servers", Layer.EVALS
    ),
    RepoEntry(
        Org.MCP,
        "modelcontextprotocol",
        7758,
        "TypeScript",
        "MCP specification and documentation",
        Layer.INFRA,
    ),
    RepoEntry(
        Org.MCP,
        "registry",
        6654,
        "Go",
        "Community-driven MCP server registry",
        Layer.TASKS,
        ["mcp", "mcp-servers"],
    ),
    RepoEntry(Org.MCP, "go-sdk", 4324, "Go", "Official Go SDK for MCP", Layer.INFRA),
    RepoEntry(
        Org.MCP, "csharp-sdk", 4179, "C#", "Official C# SDK for MCP (w/ Microsoft)", Layer.INFRA
    ),
    RepoEntry(
        Org.MCP, "java-sdk", 3349, "Java", "Official Java SDK for MCP (w/ Spring AI)", Layer.INFRA
    ),
    RepoEntry(Org.MCP, "rust-sdk", 3269, "Rust", "Official Rust SDK for MCP", Layer.INFRA),
    RepoEntry(
        Org.MCP,
        "ext-apps",
        2018,
        "TypeScript",
        "MCP Apps protocol — UIs embedded in AI chatbots",
        Layer.HARNESS,
    ),
    RepoEntry(
        Org.MCP,
        "mcpb",
        1832,
        "TypeScript",
        "Desktop Extensions — one-click MCP server install",
        Layer.HARNESS,
    ),
    RepoEntry(Org.MCP, "php-sdk", 1437, "PHP", "Official PHP SDK for MCP", Layer.INFRA),
    RepoEntry(Org.MCP, "swift-sdk", 1341, "Swift", "Official Swift SDK for MCP", Layer.INFRA),
    RepoEntry(
        Org.MCP,
        "kotlin-sdk",
        1328,
        "Kotlin",
        "Official Kotlin SDK for MCP (w/ JetBrains)",
        Layer.INFRA,
    ),
    RepoEntry(Org.MCP, "conformance", 52, "TypeScript", "Conformance tests for MCP", Layer.EVALS),
    RepoEntry(
        Org.MCP,
        "experimental-ext-skills",
        62,
        "",
        "Experimental skills discovery via MCP primitives",
        Layer.TASKS,
    ),
    RepoEntry(Org.MCP, "agents-wg", 2, "", "Agents Working Group staging", Layer.HARNESS),
]

# ── Safety Research (35 repos) ─────────────────────────────────

SAFETY_REPOS = [
    RepoEntry(
        Org.SAFETY, "bloom", 1270, "Python", "Evaluate any behavior immediately", Layer.EVALS
    ),
    RepoEntry(
        Org.SAFETY,
        "petri",
        979,
        "Python",
        "Alignment auditing agent for hypothesis exploration",
        Layer.TRACERS,
    ),
    RepoEntry(
        Org.SAFETY,
        "persona_vectors",
        388,
        "Python",
        "Monitoring and controlling character traits",
        Layer.CIRCUITS,
    ),
    RepoEntry(Org.SAFETY, "SCONE-bench", 175, "", "Safety evaluation benchmark", Layer.EVALS),
    RepoEntry(
        Org.SAFETY,
        "assistant-axis",
        120,
        "Jupyter Notebook",
        "Direction in activation space capturing assistant-like behavior",
        Layer.CIRCUITS,
    ),
    RepoEntry(
        Org.SAFETY,
        "safety-tooling",
        114,
        "Python",
        "Inference API for many LLMs and research tools",
        Layer.INFRA,
    ),
    RepoEntry(
        Org.SAFETY,
        "open-source-alignment-faking",
        56,
        "Jinja",
        "Open source replication of alignment faking",
        Layer.SAFETY,
    ),
    RepoEntry(
        Org.SAFETY,
        "selective-gradient-masking",
        51,
        "Python",
        "Training Transformers with knowledge localization",
        Layer.CIRCUITS,
    ),
    RepoEntry(
        Org.SAFETY, "false-facts", 40, "Jupyter Notebook", "False facts research", Layer.SAFETY
    ),
    RepoEntry(
        Org.SAFETY,
        "ciphered-reasoning-llms",
        0,
        "Python",
        "Research on ciphered/encoded reasoning in LLMs",
        Layer.CIRCUITS,
    ),
    RepoEntry(
        Org.SAFETY,
        "PurpleLlama",
        0,
        "Python",
        "Meta's safety evaluation suite (referenced by security-auditor)",
        Layer.EVALS,
    ),
    RepoEntry(
        Org.SAFETY,
        "impossiblebench",
        36,
        "Python",
        "Measuring LLM propensity to exploit test cases",
        Layer.EVALS,
    ),
    RepoEntry(
        Org.SAFETY, "SHADE-Arena", 24, "Jupyter Notebook", "Safety evaluation arena", Layer.EVALS
    ),
    RepoEntry(
        Org.SAFETY,
        "inverse-scaling-ttc",
        25,
        "Python",
        "Inverse scaling in test-time compute",
        Layer.EVALS,
    ),
    RepoEntry(
        Org.SAFETY,
        "finetuning-auditor",
        20,
        "Python",
        "Auditing agents for fine-tuning safety",
        Layer.TRACERS,
    ),
    RepoEntry(Org.SAFETY, "A3", 13, "Python", "Alignment assessment agent", Layer.TRACERS),
    RepoEntry(
        Org.SAFETY,
        "believe-it-or-not",
        13,
        "Python",
        "Editing model beliefs with SDF",
        Layer.CIRCUITS,
    ),
    RepoEntry(Org.SAFETY, "auditing-agents", 12, "Python", "Auditing agents", Layer.TRACERS),
    RepoEntry(
        Org.SAFETY,
        "inoculation-prompting",
        10,
        "Python",
        "Inoculation prompting techniques",
        Layer.PROMPTS,
    ),
    RepoEntry(
        Org.SAFETY, "weight-steering", 8, "Python", "Weight steering techniques", Layer.CIRCUITS
    ),
    RepoEntry(
        Org.SAFETY,
        "crosscoder_emergent_misalignment",
        5,
        "Python",
        "Crosscoder model diffing on misaligned models",
        Layer.CIRCUITS,
    ),
    RepoEntry(
        Org.SAFETY, "lie-detector", 4, "Python", "Lie detection in language models", Layer.TRACERS
    ),
    RepoEntry(
        Org.SAFETY,
        "trusted-monitor",
        1,
        "Python",
        "Evaluate agent transcripts for suspicious behavior",
        Layer.TRACERS,
    ),
    RepoEntry(
        Org.SAFETY,
        "agent-transcript-editor",
        1,
        "Python",
        "Web UI for viewing/editing agent transcripts",
        Layer.EVALS,
    ),
    RepoEntry(
        Org.SAFETY,
        "introspection-mechanisms",
        3,
        "Python",
        "Introspection mechanisms research",
        Layer.CIRCUITS,
    ),
]

# ── Decode Research (3 repos) ──────────────────────────────────

DECODE_REPOS = [
    RepoEntry(
        Org.DECODE,
        "circuit-tracer",
        2695,
        "Python",
        "Open-source circuit tracing for mechanistic interpretability",
        Layer.TRACERS,
    ),
    RepoEntry(
        Org.DECODE,
        "SAELens",
        1308,
        "Python",
        "Training Sparse Autoencoders on Language Models",
        Layer.CIRCUITS,
    ),
    RepoEntry(
        Org.DECODE,
        "synth-sae-bench-experiments",
        5,
        "Python",
        "SynthSAEBench: Evaluating SAEs on synthetic data",
        Layer.EVALS,
    ),
]

# ── Full Registry ──────────────────────────────────────────────

ALL_REPOS = ANTHROPICS_REPOS + MCP_REPOS + SAFETY_REPOS + DECODE_REPOS


class EcosystemRegistry:
    """Registry indexing all repos across 4 GitHub organizations.

    Provides queries by org, layer, language, and star count.
    """

    def __init__(self, repos: list[RepoEntry] | None = None) -> None:
        self._repos = repos or ALL_REPOS

    @property
    def total_repos(self) -> int:
        return len(self._repos)

    @property
    def total_stars(self) -> int:
        return sum(r.stars for r in self._repos)

    def by_org(self, org: Org) -> list[RepoEntry]:
        return [r for r in self._repos if r.org == org]

    def by_layer(self, layer: Layer) -> list[RepoEntry]:
        return sorted(
            [r for r in self._repos if r.layer == layer],
            key=lambda r: r.stars,
            reverse=True,
        )

    def by_language(self, language: str) -> list[RepoEntry]:
        return [r for r in self._repos if r.language.lower() == language.lower()]

    def active(self) -> list[RepoEntry]:
        return [r for r in self._repos if not r.archived]

    def layer_summary(self) -> dict[str, dict[str, Any]]:
        """Summary statistics per layer."""
        result = {}
        for layer in Layer:
            repos = self.by_layer(layer)
            if repos:
                result[layer.name] = {
                    "count": len(repos),
                    "total_stars": sum(r.stars for r in repos),
                    "top_repo": repos[0].full_name if repos else "",
                    "repos": [r.full_name for r in repos[:5]],
                }
        return result

    def org_summary(self) -> dict[str, dict[str, Any]]:
        """Summary statistics per org."""
        result = {}
        for org in Org:
            repos = self.by_org(org)
            result[org.value] = {
                "count": len(repos),
                "total_stars": sum(r.stars for r in repos),
                "languages": list({r.language for r in repos if r.language}),
            }
        return result

    def dependency_graph(self) -> dict[str, list[str]]:
        """Layer dependency graph — which layers depend on which repos.

        Returns edges: layer_name → [repo_full_names]
        """
        return {
            "CIRCUITS": [
                "decoderesearch/SAELens",
                "decoderesearch/circuit-tracer",
                "safety-research/persona_vectors",
                "safety-research/assistant-axis",
                "safety-research/crosscoder_emergent_misalignment",
                "safety-research/weight-steering",
                "safety-research/selective-gradient-masking",
                "anthropics/toy-models-of-superposition",
                "anthropics/attribution-graphs-frontend",
            ],
            "TRACERS": [
                "decoderesearch/circuit-tracer",
                "safety-research/petri",
                "safety-research/finetuning-auditor",
                "safety-research/auditing-agents",
                "safety-research/lie-detector",
                "safety-research/trusted-monitor",
                "safety-research/A3",
            ],
            "PROMPTS": [
                "anthropics/prompt-eng-interactive-tutorial",
                "anthropics/claude-cookbooks",
                "anthropics/courses",
                "safety-research/inoculation-prompting",
            ],
            "TASKS": [
                "anthropics/skills",
                "anthropics/knowledge-work-plugins",
                "anthropics/financial-services-plugins",
                "anthropics/claude-plugins-official",
                "anthropics/claude-plugins-community",
                "anthropics/life-sciences",
                "anthropics/healthcare",
                "modelcontextprotocol/registry",
                "modelcontextprotocol/experimental-ext-skills",
            ],
            "SUBTASKS": [
                "anthropics/knowledge-work-plugins",
            ],
            "SUBAGENTS": [
                "anthropics/claude-agent-sdk-python",
                "anthropics/claude-agent-sdk-typescript",
                "anthropics/claude-agent-sdk-demos",
            ],
            "HARNESS": [
                "anthropics/claude-code",
                "anthropics/claude-code-action",
                "modelcontextprotocol/servers",
                "modelcontextprotocol/ext-apps",
                "modelcontextprotocol/mcpb",
            ],
            "EVALS": [
                "anthropics/evals",
                "anthropics/claude-code-security-review",
                "anthropics/political-neutrality-eval",
                "safety-research/bloom",
                "safety-research/SCONE-bench",
                "safety-research/impossiblebench",
                "safety-research/SHADE-Arena",
                "modelcontextprotocol/inspector",
                "modelcontextprotocol/conformance",
                "decoderesearch/synth-sae-bench-experiments",
            ],
            "INFRA": [
                "anthropics/anthropic-sdk-python",
                "anthropics/anthropic-sdk-typescript",
                "anthropics/anthropic-sdk-go",
                "anthropics/anthropic-sdk-java",
                "anthropics/anthropic-sdk-ruby",
                "anthropics/anthropic-sdk-csharp",
                "anthropics/anthropic-sdk-php",
                "modelcontextprotocol/python-sdk",
                "modelcontextprotocol/typescript-sdk",
                "modelcontextprotocol/go-sdk",
                "modelcontextprotocol/java-sdk",
                "modelcontextprotocol/csharp-sdk",
                "modelcontextprotocol/rust-sdk",
                "modelcontextprotocol/swift-sdk",
                "modelcontextprotocol/kotlin-sdk",
                "modelcontextprotocol/php-sdk",
                "safety-research/safety-tooling",
            ],
            "SAFETY": [
                "anthropics/claude-constitution",
                "anthropics/hh-rlhf",
                "safety-research/open-source-alignment-faking",
                "safety-research/false-facts",
            ],
        }
