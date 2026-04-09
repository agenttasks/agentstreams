"""agentstreams CLI — unified developer toolkit for Claude Code.

Provides subcommands for all agentstreams operations across device
surfaces: CLI, Desktop, VS Code, JetBrains, Web, and Mobile.

Designed to complement `claude` (Claude Code CLI v2.1.97+):
  - `claude` runs the agent loop
  - `agentstreams` manages the developer toolkit around it

Usage:
  agentstreams --help
  agentstreams agents list
  agentstreams eval codegen --models sonnet
  agentstreams pdf read https://example.com/doc.pdf
  agentstreams pipeline run --stages validate security
  agentstreams validate all

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

PROJECT_ROOT = Path(__file__).parent.parent
console = Console()

app = typer.Typer(
    name="agentstreams",
    help="Developer toolkit for Claude Code CLI — multi-agent orchestration, "
    "evals, PDF reading, and knowledge-work pipelines.",
    no_args_is_help=True,
)

# ── Subcommand groups ───────────────────────────────────────────

agents_app = typer.Typer(help="Manage agents and subagents")
eval_app = typer.Typer(help="Run evaluation suites")
pdf_app = typer.Typer(help="Download and read PDFs with bloom filter dedup")
pipeline_app = typer.Typer(help="Run multi-agent pipelines")
validate_app = typer.Typer(help="Validate skills, agents, and ontology")
layers_app = typer.Typer(help="Inspect the 14-layer knowledge-work architecture")

app.add_typer(agents_app, name="agents")
app.add_typer(eval_app, name="eval")
app.add_typer(pdf_app, name="pdf")
app.add_typer(pipeline_app, name="pipeline")
app.add_typer(validate_app, name="validate")
app.add_typer(layers_app, name="layers")


# ── Agents ──────────────────────────────────────────────────────


@agents_app.command("list")
def agents_list(
    category: str = typer.Option("", help="Filter by plugin category"),
) -> None:
    """List all registered agents with tools and model."""
    agents_dir = PROJECT_ROOT / ".claude" / "agents"
    if not agents_dir.exists():
        console.print("[red]No agents directory found[/red]")
        raise typer.Exit(1)

    table = Table(title="Agents")
    table.add_column("Name", style="cyan")
    table.add_column("Model", style="green")
    table.add_column("Tools", style="yellow")

    for md in sorted(agents_dir.glob("*.md")):
        name = md.stem
        if category and category not in name:
            continue
        # Parse frontmatter
        text = md.read_text(errors="replace")
        model = tools = ""
        if text.startswith("---"):
            end = text.find("---", 3)
            if end != -1:
                for line in text[3:end].split("\n"):
                    if line.strip().startswith("model:"):
                        model = line.split(":", 1)[1].strip()
                    elif line.strip().startswith("tools:"):
                        tools = line.split(":", 1)[1].strip()
        table.add_row(name, model, tools[:60])

    console.print(table)


@agents_app.command("show")
def agents_show(name: str = typer.Argument(..., help="Agent name")) -> None:
    """Show details of a specific agent."""
    md = PROJECT_ROOT / ".claude" / "agents" / f"{name}.md"
    if not md.exists():
        console.print(f"[red]Agent not found: {name}[/red]")
        raise typer.Exit(1)
    console.print(md.read_text(errors="replace"))


# ── Eval ────────────────────────────────────────────────────────


@eval_app.command("codegen")
def eval_codegen(
    models: list[str] = typer.Option(["sonnet", "opus"], help="Model variants"),
    lang: list[str] = typer.Option(["python", "typescript"], help="Languages"),
    samples: int = typer.Option(1, help="Samples per task per model"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show tasks without running"),
) -> None:
    """Run A/B code generation eval (CPU-parallel validation)."""
    cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "run-codegen-eval.py")]
    for m in models:
        cmd.extend(["--models", m])
    for l in lang:
        cmd.extend(["--lang", l])
    cmd.extend(["--samples", str(samples)])
    if dry_run:
        cmd.append("--dry-run")
    subprocess.run(cmd, cwd=PROJECT_ROOT)


@eval_app.command("promptfoo")
def eval_promptfoo(
    suite: str = typer.Argument("", help="Specific suite dir (e.g., codegen-ab)"),
) -> None:
    """Run promptfoo eval suites."""
    evals_dir = PROJECT_ROOT / "evals"
    if suite:
        dirs = [evals_dir / suite]
    else:
        dirs = [d for d in evals_dir.iterdir() if d.is_dir() and (d / "promptfooconfig.yaml").exists()]

    for d in dirs:
        if (d / "promptfooconfig.yaml").exists():
            console.print(f"\n[bold]Running: {d.name}[/bold]")
            subprocess.run(["npx", "promptfoo", "eval"], cwd=d)


# ── PDF ─────────────────────────────────────────────────────────


@pdf_app.command("read")
def pdf_read(
    urls: list[str] = typer.Argument(..., help="PDF URLs to download and extract"),
    pages: str = typer.Option("", help='Page range (e.g., "1-10")'),
    toc: bool = typer.Option(False, help="Print table of contents only"),
    stats: bool = typer.Option(False, help="Print per-page token estimates"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Force re-download"),
) -> None:
    """Download PDFs and extract text with bloom filter dedup."""
    cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "pdf-read.py")]
    if pages:
        cmd.extend(["--pages", pages])
    if toc:
        cmd.append("--toc")
    if stats:
        cmd.append("--stats")
    if no_cache:
        cmd.append("--no-cache")
    cmd.extend(urls)
    subprocess.run(cmd, cwd=PROJECT_ROOT)


# ── Pipeline ────────────────────────────────────────────────────


@pipeline_app.command("run")
def pipeline_run(
    stages: list[str] = typer.Option([], help="Pipeline stages to run"),
    check_only: bool = typer.Option(False, "--check-only", help="Validate without executing"),
) -> None:
    """Run a multi-agent pipeline."""
    cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "run-pipeline.py")]
    if stages:
        cmd.extend(["--stages"] + stages)
    if check_only:
        cmd.append("--check-only")
    subprocess.run(cmd, cwd=PROJECT_ROOT)


@pipeline_app.command("security")
def pipeline_security(
    paths: list[str] = typer.Option(["scripts/", ".claude/"], help="Paths to audit"),
    check_only: bool = typer.Option(False, "--check-only"),
) -> None:
    """Run security audit pipeline."""
    cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "security-audit.py")]
    cmd.extend(["--paths"] + paths)
    if check_only:
        cmd.append("--check-only")
    subprocess.run(cmd, cwd=PROJECT_ROOT)


# ── Validate ────────────────────────────────────────────────────


@validate_app.command("all")
def validate_all() -> None:
    """Run all validators (skills, ontology, agents)."""
    for script in ["validate-skills.py", "validate-ontology.py"]:
        path = PROJECT_ROOT / "scripts" / script
        if path.exists():
            console.print(f"\n[bold]Running: {script}[/bold]")
            subprocess.run([sys.executable, str(path), "--check-only"], cwd=PROJECT_ROOT)


@validate_app.command("agents")
def validate_agents_cmd() -> None:
    """Validate agent boundaries (tool grants, API key ban)."""
    subprocess.run(["make", "validate-agents"], cwd=PROJECT_ROOT)


# ── Layers ──────────────────────────────────────────────────────


@layers_app.command("list")
def layers_list() -> None:
    """Show the 14-layer knowledge-work architecture."""
    from src.knowledge_work.registry import EcosystemRegistry, Layer

    table = Table(title="14-Layer Knowledge-Work Architecture")
    table.add_column("Layer", style="cyan", justify="right")
    table.add_column("Name", style="green")
    table.add_column("Repos", style="yellow", justify="right")
    table.add_column("Stars", style="magenta", justify="right")
    table.add_column("Top Repo")

    reg = EcosystemRegistry()
    for layer in sorted(Layer, key=lambda l: l.value):
        repos = reg.by_layer(layer)
        if repos:
            table.add_row(
                str(layer.value),
                layer.name.lower(),
                str(len(repos)),
                f"{sum(r.stars for r in repos):,}",
                repos[0].full_name,
            )

    console.print(table)


@layers_app.command("repos")
def layers_repos(layer_id: int = typer.Argument(..., help="Layer ID (0-10)")) -> None:
    """Show repos that feed a specific layer."""
    from src.knowledge_work.registry import EcosystemRegistry, Layer

    reg = EcosystemRegistry()
    try:
        layer = Layer(layer_id)
    except ValueError:
        console.print(f"[red]Invalid layer ID: {layer_id}[/red]")
        raise typer.Exit(1)

    repos = reg.by_layer(layer)
    table = Table(title=f"Layer {layer_id}: {layer.name}")
    table.add_column("Repo", style="cyan")
    table.add_column("Stars", style="yellow", justify="right")
    table.add_column("Language", style="green")
    table.add_column("Description")

    for r in repos:
        table.add_row(r.full_name, f"{r.stars:,}", r.language, r.description[:60])

    console.print(table)


@layers_app.command("route")
def layers_route(
    request: str = typer.Argument(..., help="Natural language task request"),
) -> None:
    """Route a request through the task router (Layer 4)."""
    from src.knowledge_work.tasks import TaskRouter

    router = TaskRouter()
    task = router.route(request)
    if task:
        console.print(f"[green]Routed to:[/green] {task.name}")
        console.print(f"  Domain: {task.domain.value}")
        console.print(f"  Plugin: {task.plugin_category}/{task.skill_name}")
        console.print(f"  Complexity: {task.complexity.value}")
    else:
        console.print("[yellow]No matching task found.[/yellow]")


# ── Top-level commands ──────────────────────────────────────────


@app.command("info")
def info() -> None:
    """Show project info and device surface details."""
    import os
    import platform

    table = Table(title="agentstreams")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Version", "0.3.0")
    table.add_row("Platform", platform.platform())
    table.add_row("Python", platform.python_version())
    table.add_row("Project root", str(PROJECT_ROOT))
    table.add_row("Agents", str(len(list((PROJECT_ROOT / ".claude" / "agents").glob("*.md")))))
    table.add_row("Skills", str(len(list((PROJECT_ROOT / "skills").glob("*/SKILL.md")))))
    table.add_row("Eval suites", str(len(list((PROJECT_ROOT / "evals").glob("*/promptfooconfig.yaml")))))
    table.add_row("Scripts", str(len(list((PROJECT_ROOT / "scripts").glob("*.py")))))

    # Check Claude Code
    try:
        result = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=5)
        table.add_row("Claude Code", result.stdout.strip() or "installed")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        table.add_row("Claude Code", "[red]not found[/red]")

    table.add_row("Auth", "CLAUDE_CODE_OAUTH_TOKEN" if os.environ.get("CLAUDE_CODE_OAUTH_TOKEN") else "[red]not set[/red]")

    console.print(table)


@app.command("status")
def status() -> None:
    """Quick status check — git, deps, and validation."""
    import shutil

    checks = []

    # Git
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=PROJECT_ROOT)
    dirty = len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
    checks.append(("Git", "clean" if dirty == 0 else f"{dirty} dirty files", dirty == 0))

    # Python deps
    checks.append(("Python (uv)", "available" if shutil.which("uv") else "missing", bool(shutil.which("uv"))))

    # Node
    checks.append(("Node.js", "available" if shutil.which("node") else "missing", bool(shutil.which("node"))))

    # Ruff
    checks.append(("Ruff", "available" if shutil.which("ruff") else "missing", bool(shutil.which("ruff"))))

    table = Table(title="Status")
    table.add_column("Check", style="cyan")
    table.add_column("Result")
    table.add_column("OK", justify="center")

    for name, result_text, ok in checks:
        style = "green" if ok else "red"
        table.add_row(name, result_text, "[green]✓[/green]" if ok else "[red]✗[/red]")

    console.print(table)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
