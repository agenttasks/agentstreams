"""Headless / programmatic Claude Code execution.

Wraps Claude Code's headless mode for running the ``claude`` CLI as a
subprocess from Python.  All invocations use CLAUDE_CODE_OAUTH_TOKEN
(never ANTHROPIC_API_KEY).

Pre-built configs:
    CODEGEN_CONFIG   — code generation (sonnet, non-interactive)
    REVIEW_CONFIG    — code review (opus, temperature 0)
    RESEARCH_CONFIG  — research / summarisation (sonnet, larger context)

Parallel batch execution uses ThreadPoolExecutor capped at 4 workers
to saturate the available CPU cores without oversubscribing.
"""

from __future__ import annotations

import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any

# Maximum workers for parallel headless runs (one per CPU core)
_BATCH_WORKERS: int = 4


# ── Dataclasses ─────────────────────────────────────────────────


@dataclass
class HeadlessConfig:
    """Configuration for a headless Claude Code invocation.

    Args:
        model: Claude model ID (e.g., ``claude-sonnet-4-6``).
        system_prompt: Optional system prompt prepended to the session.
        max_turns: Maximum agent turns before the process exits.
        tools: MCP tool names to enable (passed as ``--tool`` flags).
        output_format: Output format: ``"text"`` (default), ``"json"``,
            or ``"stream-json"``.
    """

    model: str = "claude-sonnet-4-6"
    system_prompt: str = ""
    max_turns: int = 10
    tools: list[str] = field(default_factory=list)
    output_format: str = "text"


@dataclass
class HeadlessResult:
    """Result from a single headless run.

    Args:
        prompt: The prompt that was executed.
        stdout: Raw stdout from the ``claude`` process.
        stderr: Raw stderr (warnings / trace output).
        returncode: Process exit code (0 = success).
    """

    prompt: str
    stdout: str
    stderr: str
    returncode: int

    @property
    def success(self) -> bool:
        """True if the process exited cleanly."""
        return self.returncode == 0

    @property
    def output(self) -> str:
        """Stripped stdout text."""
        return self.stdout.strip()


# ── Internal helpers ─────────────────────────────────────────────


def _build_cmd(
    prompt: str,
    config: HeadlessConfig,
    extra_tools: list[str] | None = None,
) -> list[str]:
    """Build the ``claude`` subprocess argument list.

    Args:
        prompt: The user prompt to pass to claude.
        config: HeadlessConfig driving model, turns, and format.
        extra_tools: Additional tool names appended on top of config.tools.

    Returns:
        Argument list ready for ``subprocess.run``.
    """
    cmd: list[str] = [
        "claude",
        "--model", config.model,
        "--max-turns", str(config.max_turns),
        "--output-format", config.output_format,
        "--print",          # Non-interactive: print response then exit
    ]

    if config.system_prompt:
        cmd.extend(["--system-prompt", config.system_prompt])

    all_tools = list(config.tools) + (extra_tools or [])
    for tool in all_tools:
        cmd.extend(["--tool", tool])

    cmd.append(prompt)
    return cmd


def _run_subprocess(
    prompt: str,
    config: HeadlessConfig,
    extra_tools: list[str] | None = None,
) -> HeadlessResult:
    """Internal: execute the claude CLI and capture output.

    Args:
        prompt: Prompt to execute.
        config: HeadlessConfig for the run.
        extra_tools: Additional tool names beyond config.tools.

    Returns:
        HeadlessResult with captured stdout/stderr and returncode.
    """
    token = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "")
    env: dict[str, str] = {**os.environ, "CLAUDE_CODE_OAUTH_TOKEN": token}

    cmd = _build_cmd(prompt, config, extra_tools)
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env,
    )
    return HeadlessResult(
        prompt=prompt,
        stdout=proc.stdout,
        stderr=proc.stderr,
        returncode=proc.returncode,
    )


# ── Public API ───────────────────────────────────────────────────


def run_headless(prompt: str, config: HeadlessConfig) -> HeadlessResult:
    """Run claude in headless mode for a single prompt.

    Invokes the ``claude`` CLI with ``--print`` so it executes the prompt
    non-interactively and exits.  Auth flows through CLAUDE_CODE_OAUTH_TOKEN.

    Args:
        prompt: The prompt to send to Claude.
        config: HeadlessConfig controlling model, system prompt, and turns.

    Returns:
        HeadlessResult containing stdout, stderr, and exit code.

    Raises:
        FileNotFoundError: If the ``claude`` CLI is not on PATH.
    """
    return _run_subprocess(prompt, config)


def run_headless_with_tools(
    prompt: str,
    tools: list[str],
    config: HeadlessConfig,
) -> HeadlessResult:
    """Run claude in headless mode with additional MCP tools enabled.

    Tools are merged with any tools already declared in ``config.tools``.
    Duplicates are preserved (the CLI de-dupes them transparently).

    Args:
        prompt: The prompt to send to Claude.
        tools: MCP tool names to enable for this run.
        config: Base HeadlessConfig (model, system prompt, etc.).

    Returns:
        HeadlessResult containing stdout, stderr, and exit code.
    """
    return _run_subprocess(prompt, config, extra_tools=tools)


def run_batch(
    prompts: list[str],
    config: HeadlessConfig,
    parallel: int = _BATCH_WORKERS,
) -> list[HeadlessResult]:
    """Run multiple prompts in parallel using a thread pool.

    Submits all prompts to a ThreadPoolExecutor with ``parallel`` workers
    (default 4, one per CPU core).  Results are returned in the same order
    as the input prompts regardless of completion order.

    Args:
        prompts: List of prompts to execute.
        config: HeadlessConfig shared across all runs.
        parallel: Number of concurrent workers (default 4).

    Returns:
        List of HeadlessResult in prompt-order.
    """
    results: dict[int, HeadlessResult] = {}

    with ThreadPoolExecutor(max_workers=parallel) as executor:
        futures = {
            executor.submit(_run_subprocess, prompt, config): idx
            for idx, prompt in enumerate(prompts)
        }
        for future in as_completed(futures):
            idx = futures[future]
            results[idx] = future.result()

    return [results[i] for i in range(len(prompts))]


# ── Pre-built configs ────────────────────────────────────────────

CODEGEN_CONFIG = HeadlessConfig(
    model="claude-sonnet-4-6",
    system_prompt=(
        "You are a senior software engineer. Implement the requested changes "
        "cleanly and idiomatically. Follow existing project conventions. "
        "Never hard-code credentials."
    ),
    max_turns=25,
    output_format="text",
)

REVIEW_CONFIG = HeadlessConfig(
    model="claude-opus-4-6",
    system_prompt=(
        "You are a code reviewer. Analyse the supplied code for correctness, "
        "security issues, and adherence to project conventions. Provide a "
        "structured report: summary, findings (severity + location + "
        "recommendation), and verdict (PASS / NEEDS_REMEDIATION / BLOCK)."
    ),
    max_turns=10,
    output_format="text",
)

RESEARCH_CONFIG = HeadlessConfig(
    model="claude-sonnet-4-6",
    system_prompt=(
        "You are a research assistant. Summarise sources accurately, cite "
        "evidence, and flag uncertainty. Return findings as structured prose "
        "with clear section headings."
    ),
    max_turns=15,
    output_format="text",
)
