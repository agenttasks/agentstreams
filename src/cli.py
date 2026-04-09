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
tools_app = typer.Typer(help="Search, list, and inspect registered tools and skills")
teams_app = typer.Typer(help="Manage and run agent teams for multi-session coordination")
channels_app = typer.Typer(help="Manage and push channel events into Claude Code sessions")
headless_app = typer.Typer(help="Run claude in headless/programmatic mode")
sessions_app = typer.Typer(help="Manage Claude Code session lifecycle (continue/resume/fork)")

app.add_typer(agents_app, name="agents")
app.add_typer(eval_app, name="eval")
app.add_typer(pdf_app, name="pdf")
app.add_typer(pipeline_app, name="pipeline")
app.add_typer(validate_app, name="validate")
app.add_typer(layers_app, name="layers")
app.add_typer(tools_app, name="tools")
app.add_typer(teams_app, name="teams")
app.add_typer(channels_app, name="channels")
app.add_typer(headless_app, name="headless")
app.add_typer(sessions_app, name="sessions")


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
    structured: bool = typer.Option(
        False,
        "--structured",
        help="Emit a structured JSON verdict via Claude (requires CLAUDE_CODE_OAUTH_TOKEN)",
    ),
    model: str = typer.Option("claude-sonnet-4-6", "--model", help="Model for structured output"),
) -> None:
    """Run security audit pipeline.

    With ``--structured`` the command asks Claude to produce a machine-readable
    JSON verdict (VERDICT_SCHEMA) instead of running the audit script.
    """
    if structured:
        from src.structured_output import VERDICT_SCHEMA, run_structured
        import json as _json

        paths_str = ", ".join(paths)
        prompt = (
            f"Perform a security audit of the following paths in the agentstreams project: "
            f"{paths_str}. "
            "Identify any issues relating to credential exposure, unsafe subprocess calls, "
            "unvalidated inputs, or agent boundary violations. "
            "Produce a verdict object."
        )
        try:
            result = run_structured(prompt, VERDICT_SCHEMA, model=model)
            console.print_json(_json.dumps(result, indent=2))
        except RuntimeError as exc:
            console.print(f"[red]Structured output failed: {exc}[/red]")
            raise typer.Exit(1)
        return

    cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "security-audit.py")]
    cmd.extend(["--paths"] + paths)
    if check_only:
        cmd.append("--check-only")
    subprocess.run(cmd, cwd=PROJECT_ROOT)


# ── Validate ────────────────────────────────────────────────────


@validate_app.command("all")
def validate_all(
    structured: bool = typer.Option(
        False,
        "--structured",
        help="Emit a structured JSON task result via Claude (requires CLAUDE_CODE_OAUTH_TOKEN)",
    ),
    model: str = typer.Option("claude-sonnet-4-6", "--model", help="Model for structured output"),
) -> None:
    """Run all validators (skills, ontology, agents).

    With ``--structured`` the command asks Claude to summarise validation
    results as a machine-readable TASK_RESULT_SCHEMA JSON object instead of
    running each script individually.
    """
    if structured:
        from src.structured_output import TASK_RESULT_SCHEMA, run_structured
        import json as _json
        import time

        start_ms = int(time.monotonic() * 1000)
        scripts = ["validate-skills.py", "validate-ontology.py"]
        outputs: list[str] = []
        errors: list[str] = []

        for script in scripts:
            path = PROJECT_ROOT / "scripts" / script
            if path.exists():
                result = subprocess.run(
                    [sys.executable, str(path), "--check-only"],
                    capture_output=True,
                    text=True,
                    cwd=PROJECT_ROOT,
                )
                if result.stdout.strip():
                    outputs.append(f"[{script}] {result.stdout.strip()}")
                if result.returncode != 0 and result.stderr.strip():
                    errors.append(f"[{script}] {result.stderr.strip()}")

        duration_ms = int(time.monotonic() * 1000) - start_ms
        combined_output = "\n".join(outputs) or "No output from validators."
        combined_errors = "\n".join(errors) if errors else None

        prompt = (
            "Summarise the following agentstreams validation run results. "
            "Determine whether validation passed or failed. "
            f"Output:\n{combined_output}\n"
            + (f"Errors:\n{combined_errors}" if combined_errors else "No errors.")
        )
        try:
            structured_result = run_structured(prompt, TASK_RESULT_SCHEMA, model=model)
            # Inject the measured duration if the model left it at 0.
            if structured_result.get("duration_ms", 0) == 0:
                structured_result["duration_ms"] = duration_ms
            console.print_json(_json.dumps(structured_result, indent=2))
        except RuntimeError as exc:
            console.print(f"[red]Structured output failed: {exc}[/red]")
            raise typer.Exit(1)
        return

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


# ── Teams ───────────────────────────────────────────────────────


@teams_app.command("list")
def teams_list() -> None:
    """List all pre-built team configs and their members."""
    from src.agent_teams import TEAMS

    for team_name, config in TEAMS.items():
        table = Table(title=f"Team: {team_name}  (max_parallel={config.max_parallel})")
        table.add_column("Agent", style="cyan")
        table.add_column("Role", style="green")
        table.add_column("Model", style="yellow")
        table.add_column("Tools", style="magenta")

        for member in config.members:
            table.add_row(
                member.agent_name,
                member.role,
                member.model,
                ", ".join(member.tools) if member.tools else "-",
            )

        console.print(table)
        if config.shared_context:
            console.print(f"  [dim]Context:[/dim] {config.shared_context[:80]}...")
        console.print()


@teams_app.command("run")
def teams_run(
    team: str = typer.Argument(..., help="Team name (e.g., security-team, research-team)"),
    task: str = typer.Option(..., "--task", "-t", help="Task description to broadcast to all members"),
    member: str = typer.Option("", "--member", "-m", help="Target a single member instead of all"),
    parallel: bool = typer.Option(True, help="Run members in parallel (default: True)"),
) -> None:
    """Run a task against a team or a single member.

    Examples:
      agentstreams teams run security-team --task "Audit src/ for injection flaws"
      agentstreams teams run research-team --task "Summarise Q1 results" --member data-analyst
    """
    from src.agent_teams import TEAMS, TeamOrchestrator

    if team not in TEAMS:
        available = ", ".join(TEAMS.keys())
        console.print(f"[red]Unknown team '{team}'. Available: {available}[/red]")
        raise typer.Exit(1)

    config = TEAMS[team]
    orch = TeamOrchestrator(config)

    if member:
        # Single-member assignment
        names = [m.agent_name for m in config.members]
        if member not in names:
            console.print(f"[red]Member '{member}' not in team '{team}'. Members: {', '.join(names)}[/red]")
            raise typer.Exit(1)
        console.print(f"[bold]Assigning task to {member}...[/bold]")
        result = orch.assign_task(member, task)
        _print_member_result(result)
    elif parallel:
        # Broadcast in parallel
        tasks_list = [(m.agent_name, task) for m in config.members]
        console.print(f"[bold]Running {len(tasks_list)} members in parallel...[/bold]")
        results = orch.run_parallel(tasks_list)
        for res in results:
            _print_member_result(res)
    else:
        # Sequential broadcast
        console.print(f"[bold]Broadcasting to {len(config.members)} members sequentially...[/bold]")
        for m in config.members:
            console.print(f"  -> {m.agent_name}")
            result = orch.assign_task(m.agent_name, task)
            _print_member_result(result)


@teams_app.command("status")
def teams_status() -> None:
    """Show team registry status: member counts and agent file presence."""
    from src.agent_teams import TEAMS

    agents_dir = PROJECT_ROOT / ".claude" / "agents"

    table = Table(title="Agent Teams Status")
    table.add_column("Team", style="cyan")
    table.add_column("Members", justify="right", style="yellow")
    table.add_column("Max Parallel", justify="right", style="green")
    table.add_column("Agents Found", justify="right")
    table.add_column("Missing Agents", style="red")

    for team_name, config in TEAMS.items():
        found = []
        missing = []
        for m in config.members:
            md = agents_dir / f"{m.agent_name}.md"
            if md.exists():
                found.append(m.agent_name)
            else:
                missing.append(m.agent_name)

        table.add_row(
            team_name,
            str(len(config.members)),
            str(config.max_parallel),
            str(len(found)),
            ", ".join(missing) if missing else "[green]none[/green]",
        )

    console.print(table)


def _print_member_result(result: object) -> None:
    """Render a MemberResult to the console."""
    status = "[green]OK[/green]" if result.success else "[red]FAIL[/red]"
    console.print(f"\n[bold]{result.agent_name}[/bold]  {status}  (exit {result.returncode})")
    if result.stdout.strip():
        console.print(result.stdout.strip())
    if result.stderr.strip():
        console.print(f"[dim]{result.stderr.strip()}[/dim]")


# ── Tools ───────────────────────────────────────────────────────


@tools_app.command("search")
def tools_search(
    query: str = typer.Argument(..., help="Keyword query (e.g., 'code review')"),
    max_results: int = typer.Option(5, "--max", "-n", help="Maximum results to return"),
    vendor: bool = typer.Option(False, "--vendor", help="Include vendored kwp: tools"),
) -> None:
    """Search registered tools and skills by keyword."""
    from src.tool_search import DEFAULT_INDEX

    results = DEFAULT_INDEX.search(query, max_results=max_results * 2)
    if not vendor:
        results = [t for t in results if not t.name.startswith("kwp:")]
    results = results[:max_results]

    if not results:
        console.print("[yellow]No tools matched your query.[/yellow]")
        raise typer.Exit(0)

    table = Table(title=f"Tool search: '{query}'")
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("Loaded", justify="center", style="dim")

    for tool in results:
        loaded_mark = "[green]y[/green]" if tool.loaded else "[dim]n[/dim]"
        table.add_row(tool.name, tool.description[:80], loaded_mark)

    console.print(table)


@tools_app.command("list")
def tools_list(
    vendor: bool = typer.Option(False, "--vendor", help="Show only vendored kwp: tools"),
    all_tools: bool = typer.Option(False, "--all", "-a", help="Show all tools including vendored"),
) -> None:
    """List all tools registered in the default index."""
    from src.tool_search import DEFAULT_INDEX

    all_registered = DEFAULT_INDEX.list_all()

    if vendor:
        items = [t for t in all_registered if t.name.startswith("kwp:")]
    elif all_tools:
        items = all_registered
    else:
        items = [t for t in all_registered if not t.name.startswith("kwp:")]

    table = Table(title=f"Registered tools ({len(items)})")
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("Source", style="dim")

    for tool in items:
        source = Path(tool.source_path).name if tool.source_path else "-"
        table.add_row(tool.name, tool.description[:70], source)

    console.print(table)
    console.print(
        f"[dim]Total in index: {len(DEFAULT_INDEX)}  "
        f"(skills: {sum(1 for t in all_registered if not t.name.startswith('kwp:'))}, "
        f"vendor: {sum(1 for t in all_registered if t.name.startswith('kwp:'))})[/dim]"
    )


@tools_app.command("load")
def tools_load(
    name: str = typer.Argument(..., help="Exact tool name to load"),
    json_output: bool = typer.Option(False, "--json", help="Print raw JSON schema"),
) -> None:
    """Load and display the full schema for a named tool."""
    from src.tool_search import DEFAULT_INDEX
    import json as _json

    schema = DEFAULT_INDEX.load(name)
    if schema is None:
        console.print(f"[red]Tool not found: {name}[/red]")
        raise typer.Exit(1)

    tool = DEFAULT_INDEX._tools.get(name)  # noqa: SLF001
    console.print(f"[bold cyan]{name}[/bold cyan]")
    if tool:
        console.print(f"  [green]{tool.description}[/green]")
        if tool.source_path:
            console.print(f"  Source: [dim]{tool.source_path}[/dim]")

    if json_output:
        console.print(_json.dumps(schema, indent=2))
    else:
        props = schema.get("properties", {})
        required = schema.get("required", [])
        if props:
            table = Table(title="Schema properties")
            table.add_column("Property", style="cyan")
            table.add_column("Type", style="yellow")
            table.add_column("Required", justify="center")
            table.add_column("Description")
            for prop_name, prop_schema in props.items():
                req_mark = "[green]y[/green]" if prop_name in required else ""
                prop_type = str(prop_schema.get("type", "any"))
                desc = prop_schema.get("description", "")[:60]
                table.add_row(prop_name, prop_type, req_mark, desc)
            console.print(table)
        else:
            console.print("[dim]No properties defined in schema.[/dim]")


# ── Channels ────────────────────────────────────────────────────


@channels_app.command("list")
def channels_list() -> None:
    """List all registered channels (name, source type, filter)."""
    from src.channels import CI_CHANNEL, GITHUB_CHANNEL, SLACK_CHANNEL, ChannelBridge

    bridge = ChannelBridge()
    for cfg in [CI_CHANNEL, GITHUB_CHANNEL, SLACK_CHANNEL]:
        bridge.register(cfg)

    table = Table(title="Registered Channels")
    table.add_column("Name", style="cyan")
    table.add_column("Source Type", style="green")
    table.add_column("Filter Pattern", style="yellow")

    for cfg in bridge.registered_channels():
        table.add_row(cfg.channel_name, cfg.source_type.value, cfg.filter_pattern or "-")

    console.print(table)


@channels_app.command("push")
def channels_push(
    source: str = typer.Option(..., "--source", "-s", help="Channel name / source (e.g., ci, github)"),
    type_: str = typer.Option(..., "--type", "-t", help="Event type (e.g., ci.failure, pr.comment)"),
    payload: str = typer.Option("{}", "--payload", "-p", help="JSON payload string"),
) -> None:
    """Push an event into the active Claude Code session.

    Example:
      agentstreams channels push -s ci -t ci.failure -p '{"branch":"main"}'
    """
    import json as _json

    from src.channels import ChannelBridge, ChannelMessage

    try:
        data = _json.loads(payload)
    except _json.JSONDecodeError as exc:
        console.print(f"[red]Invalid JSON payload: {exc}[/red]")
        raise typer.Exit(1)

    msg = ChannelMessage(source=source, type=type_, payload=data)
    bridge = ChannelBridge()
    proc = bridge.push(msg)

    if proc.returncode == 0:
        console.print(f"[green]Pushed {type_} to channel '{source}'[/green]")
        if proc.stdout.strip():
            console.print(proc.stdout.strip())
    else:
        console.print(f"[red]Push failed (exit {proc.returncode})[/red]")
        if proc.stderr.strip():
            console.print(f"[dim]{proc.stderr.strip()}[/dim]")
        raise typer.Exit(proc.returncode)


@channels_app.command("status")
def channels_status() -> None:
    """Show channel status: pre-built configs and auth token presence."""
    import os

    from src.channels import CI_CHANNEL, GITHUB_CHANNEL, SLACK_CHANNEL

    table = Table(title="Channel Status")
    table.add_column("Channel", style="cyan")
    table.add_column("Source Type", style="green")
    table.add_column("Filter", style="yellow")
    table.add_column("Status")

    for cfg in [CI_CHANNEL, GITHUB_CHANNEL, SLACK_CHANNEL]:
        table.add_row(
            cfg.channel_name,
            cfg.source_type.value,
            cfg.filter_pattern or "-",
            "[green]ready[/green]",
        )

    console.print(table)

    token_present = bool(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"))
    auth_label = (
        "[green]CLAUDE_CODE_OAUTH_TOKEN set[/green]"
        if token_present
        else "[red]CLAUDE_CODE_OAUTH_TOKEN not set[/red]"
    )
    console.print(f"\nAuth: {auth_label}")


# ── Headless ─────────────────────────────────────────────────────


@headless_app.command("run")
def headless_run(
    prompt: str = typer.Argument(..., help="Prompt to send to Claude"),
    model: str = typer.Option("", help="Model ID (overrides config default)"),
    config_name: str = typer.Option(
        "codegen",
        "--config",
        "-c",
        help="Pre-built config: codegen, review, research",
    ),
    system_prompt: str = typer.Option("", "--system-prompt", help="Override system prompt"),
    max_turns: int = typer.Option(0, help="Override max turns (0 = use config default)"),
    tools: list[str] = typer.Option([], "--tool", help="MCP tool names to enable"),
    output_format: str = typer.Option("", "--output-format", "-o", help="text, json, stream-json"),
) -> None:
    """Run a single prompt in headless mode.

    Example:
      agentstreams headless run "Add type hints to src/bloom.py" --config codegen
    """
    from src.headless import (
        CODEGEN_CONFIG,
        RESEARCH_CONFIG,
        REVIEW_CONFIG,
        HeadlessConfig,
        run_headless,
        run_headless_with_tools,
    )

    _configs = {"codegen": CODEGEN_CONFIG, "review": REVIEW_CONFIG, "research": RESEARCH_CONFIG}
    base = _configs.get(config_name)
    if base is None:
        console.print(f"[red]Unknown config '{config_name}'. Choose: codegen, review, research[/red]")
        raise typer.Exit(1)

    cfg = HeadlessConfig(
        model=model or base.model,
        system_prompt=system_prompt or base.system_prompt,
        max_turns=max_turns if max_turns > 0 else base.max_turns,
        tools=list(base.tools),
        output_format=output_format or base.output_format,
    )

    console.print(f"[bold]Running headless ({cfg.model}, {cfg.max_turns} turns max)...[/bold]")

    if tools:
        result = run_headless_with_tools(prompt, list(tools), cfg)
    else:
        result = run_headless(prompt, cfg)

    if result.success:
        console.print(result.output)
    else:
        console.print(f"[red]claude exited {result.returncode}[/red]")
        if result.stderr.strip():
            console.print(f"[dim]{result.stderr.strip()}[/dim]")
        raise typer.Exit(result.returncode)


@headless_app.command("batch")
def headless_batch(
    prompts_file: str = typer.Option(
        "",
        "--file",
        "-f",
        help="Path to a file with one prompt per line",
    ),
    prompts: list[str] = typer.Option([], "--prompt", "-p", help="Prompt(s) to run (repeatable)"),
    config_name: str = typer.Option(
        "codegen",
        "--config",
        "-c",
        help="Pre-built config: codegen, review, research",
    ),
    parallel: int = typer.Option(4, help="Number of parallel workers (default 4)"),
    output_format: str = typer.Option("", "--output-format", "-o", help="text, json, stream-json"),
) -> None:
    """Run multiple prompts in parallel headless mode.

    Prompts may be supplied via --prompt (repeatable) or --file (one per line).

    Example:
      agentstreams headless batch --file prompts.txt --parallel 4
      agentstreams headless batch -p "task 1" -p "task 2" --config review
    """
    from src.headless import (
        CODEGEN_CONFIG,
        RESEARCH_CONFIG,
        REVIEW_CONFIG,
        HeadlessConfig,
        run_batch,
    )

    all_prompts: list[str] = list(prompts)

    if prompts_file:
        ppath = Path(prompts_file)
        if not ppath.exists():
            console.print(f"[red]File not found: {prompts_file}[/red]")
            raise typer.Exit(1)
        lines = [line.strip() for line in ppath.read_text().splitlines() if line.strip()]
        all_prompts.extend(lines)

    if not all_prompts:
        console.print("[red]No prompts provided. Use --prompt or --file.[/red]")
        raise typer.Exit(1)

    _configs = {"codegen": CODEGEN_CONFIG, "review": REVIEW_CONFIG, "research": RESEARCH_CONFIG}
    base = _configs.get(config_name)
    if base is None:
        console.print(f"[red]Unknown config '{config_name}'. Choose: codegen, review, research[/red]")
        raise typer.Exit(1)

    cfg = HeadlessConfig(
        model=base.model,
        system_prompt=base.system_prompt,
        max_turns=base.max_turns,
        tools=list(base.tools),
        output_format=output_format or base.output_format,
    )

    console.print(
        f"[bold]Running {len(all_prompts)} prompts "
        f"({parallel} parallel, {cfg.model})...[/bold]"
    )

    results = run_batch(all_prompts, cfg, parallel=parallel)

    failed = 0
    for i, res in enumerate(results, start=1):
        run_status = "[green]OK[/green]" if res.success else "[red]FAIL[/red]"
        snippet = res.prompt[:80] + ("..." if len(res.prompt) > 80 else "")
        console.print(f"\n[bold]Prompt {i}/{len(results)}[/bold]  {run_status}")
        console.print(f"  [dim]{snippet}[/dim]")
        if res.output:
            console.print(res.output)
        if not res.success:
            failed += 1
            if res.stderr.strip():
                console.print(f"  [dim]{res.stderr.strip()}[/dim]")

    if failed:
        console.print(f"\n[red]{failed}/{len(results)} prompts failed.[/red]")
        raise typer.Exit(1)
    else:
        console.print(f"\n[green]All {len(results)} prompts completed.[/green]")


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
