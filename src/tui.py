"""AgentStreams Textual TUI dashboard.

Four-screen terminal UI for monitoring metrics, tasks, agents, and
running ad-hoc SQL queries against Neon Postgres.

Launch: agentstreams tui  (or: make tui)
"""

from __future__ import annotations

from pathlib import Path

from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    DataTable,
    Footer,
    Header,
    Label,
    RichLog,
    Static,
    TextArea,
)

PROJECT_ROOT = Path(__file__).parent.parent


# ── Helpers ────────────────────────────────────────────────


async def _query(sql: str, params: tuple = ()) -> list[tuple]:
    """Run a read-only query and return rows."""
    from src.neon_db import connection_pool

    async with connection_pool() as conn:
        rows = await (await conn.execute(sql, params)).fetchall()
        return rows


# ── Metrics Screen ─────────────────────────────────────────


class MetricsScreen(Screen):
    BINDINGS = [Binding("r", "refresh_data", "Refresh")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(" Metrics Catalog", id="screen-title")
        yield DataTable(id="metrics-table")
        yield Label(" Recent Values (select a metric above)", id="values-title")
        yield DataTable(id="values-table")
        yield Footer()

    async def on_mount(self) -> None:
        table = self.query_one("#metrics-table", DataTable)
        table.add_columns("Name", "Type", "Unit", "Dimensions", "Description")
        table.cursor_type = "row"
        vtable = self.query_one("#values-table", DataTable)
        vtable.add_columns("Recorded At", "Value", "Tags")
        self.load_metrics()

    @work(thread=False)
    async def load_metrics(self) -> None:
        rows = await _query(
            "SELECT name, type, unit, dimensions, description FROM metrics ORDER BY name"
        )
        table = self.query_one("#metrics-table", DataTable)
        table.clear()
        for r in rows:
            dims = ", ".join(r[3]) if r[3] else ""
            table.add_row(r[0], r[1], r[2] or "", dims, (r[4] or "")[:60])

    async def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        table = self.query_one("#metrics-table", DataTable)
        row_data = table.get_row(event.row_key)
        metric_name = row_data[0]
        self.load_values(metric_name)

    @work(thread=False)
    async def load_values(self, metric_name: str) -> None:
        rows = await _query(
            """SELECT recorded_at, value, tags FROM metric_values
               WHERE metric_name = %s ORDER BY recorded_at DESC LIMIT 50""",
            (metric_name,),
        )
        vtable = self.query_one("#values-table", DataTable)
        vtable.clear()
        for r in rows:
            ts = r[0].strftime("%Y-%m-%d %H:%M:%S") if r[0] else ""
            vtable.add_row(ts, f"{r[1]:.4f}", str(r[2] or ""))
        title = self.query_one("#values-title", Label)
        title.update(f" Recent Values: {metric_name} ({len(rows)} rows)")

    def action_refresh_data(self) -> None:
        self.load_metrics()


# ── Tasks Screen ───────────────────────────────────────────


class TasksScreen(Screen):
    BINDINGS = [Binding("r", "refresh_data", "Refresh")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(" Task Queue", id="screen-title")
        yield Static("Loading stats...", id="task-stats")
        yield DataTable(id="tasks-table")
        yield Footer()

    async def on_mount(self) -> None:
        table = self.query_one("#tasks-table", DataTable)
        table.add_columns("ID", "Queue", "Type", "Status", "Skill", "Model", "Created")
        table.cursor_type = "row"
        self.load_tasks()
        self.set_interval(3.0, self.load_tasks)

    @work(thread=False)
    async def load_tasks(self) -> None:
        stats_rows = await _query(
            """SELECT status, COUNT(*) FROM tasks
               WHERE created_at > now() - interval '24 hours'
               GROUP BY status ORDER BY COUNT(*) DESC"""
        )
        stats_text = " | ".join(f"{r[0]}: {r[1]}" for r in stats_rows) if stats_rows else "No tasks"
        self.query_one("#task-stats", Static).update(f" 24h: {stats_text}")

        rows = await _query(
            """SELECT id, queue_name, type, status, skill_name, model_id, created_at
               FROM tasks ORDER BY created_at DESC LIMIT 50"""
        )
        table = self.query_one("#tasks-table", DataTable)
        table.clear()
        for r in rows:
            ts = r[6].strftime("%Y-%m-%d %H:%M") if r[6] else ""
            table.add_row(str(r[0]), r[1], r[2], r[3], r[4] or "", r[5] or "", ts)

    def action_refresh_data(self) -> None:
        self.load_tasks()


# ── Agents Screen ──────────────────────────────────────────


class AgentsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(" Agent Roster", id="screen-title")
        with Horizontal():
            yield DataTable(id="agents-table")
            yield RichLog(id="agent-detail", markup=True, wrap=True)
        yield Footer()

    async def on_mount(self) -> None:
        table = self.query_one("#agents-table", DataTable)
        table.add_columns("Name", "Model", "Tools")
        table.cursor_type = "row"
        self.load_agents()

    @work(thread=False)
    async def load_agents(self) -> None:
        rows = await _query(
            "SELECT name, model_id, allowed_tools, description FROM agent_manifests ORDER BY name"
        )
        table = self.query_one("#agents-table", DataTable)
        table.clear()
        for r in rows:
            tools = ", ".join(r[2][:3]) + ("..." if r[2] and len(r[2]) > 3 else "") if r[2] else ""
            table.add_row(r[0], r[1] or "", tools)

    async def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        table = self.query_one("#agents-table", DataTable)
        row_data = table.get_row(event.row_key)
        agent_name = row_data[0]
        self.show_agent_detail(agent_name)

    @work(thread=False)
    async def show_agent_detail(self, name: str) -> None:
        detail = self.query_one("#agent-detail", RichLog)
        detail.clear()
        md_path = PROJECT_ROOT / ".claude" / "agents" / f"{name}.md"
        if md_path.exists():
            detail.write(md_path.read_text()[:2000])
        else:
            row = await _query(
                "SELECT name, model_id, allowed_tools, denied_tools, description "
                "FROM agent_manifests WHERE name = %s",
                (name,),
            )
            if row:
                r = row[0]
                detail.write(f"Name: {r[0]}\nModel: {r[1]}\n")
                detail.write(f"Allowed: {r[2]}\nDenied: {r[3]}\n")
                detail.write(f"Description: {r[4]}")


# ── SQL Query Screen ───────────────────────────────────────


class QueryScreen(Screen):
    BINDINGS = [Binding("ctrl+r", "run_query", "Run Query")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(" SQL Query Editor (Ctrl+R to run)", id="screen-title")
        with Vertical():
            yield TextArea("SELECT name, type, unit FROM metrics LIMIT 10;", id="sql-input")
            yield Static("", id="query-status")
            yield DataTable(id="query-results")
        yield Footer()

    async def on_mount(self) -> None:
        results = self.query_one("#query-results", DataTable)
        results.cursor_type = "row"

    def action_run_query(self) -> None:
        editor = self.query_one("#sql-input", TextArea)
        sql = editor.text.strip()
        if sql:
            self.execute_query(sql)

    @work(thread=False)
    async def execute_query(self, sql: str) -> None:
        status = self.query_one("#query-status", Static)
        results = self.query_one("#query-results", DataTable)
        results.clear(columns=True)
        status.update(" Running...")
        try:
            from src.neon_db import connection_pool

            async with connection_pool() as conn:
                cursor = await conn.execute(sql)
                if cursor.description:
                    col_names = [desc[0] for desc in cursor.description]
                    results.add_columns(*col_names)
                    rows = await cursor.fetchall()
                    for row in rows[:500]:
                        results.add_row(*[str(v)[:80] if v is not None else "" for v in row])
                    status.update(f" {len(rows)} row(s) returned")
                else:
                    await conn.commit()
                    status.update(" Statement executed (no rows returned)")
        except Exception as e:
            status.update(f" Error: {e}")


# ── Main App ───────────────────────────────────────────────

SCREENS = {
    "metrics": MetricsScreen,
    "tasks": TasksScreen,
    "agents": AgentsScreen,
    "query": QueryScreen,
}


class AgentStreamsTUI(App):
    """AgentStreams terminal dashboard."""

    TITLE = "AgentStreams"
    CSS = """
    #screen-title { background: $accent; color: $text; padding: 0 1; }
    #task-stats { background: $surface; padding: 0 1; }
    #query-status { background: $surface; padding: 0 1; height: 1; }
    #sql-input { height: 8; }
    #agent-detail { width: 1fr; min-width: 40; }
    #agents-table { width: 1fr; }
    """
    SCREENS = SCREENS
    BINDINGS = [
        Binding("m", "switch_screen('metrics')", "Metrics"),
        Binding("t", "switch_screen('tasks')", "Tasks"),
        Binding("a", "switch_screen('agents')", "Agents"),
        Binding("s", "switch_screen('query')", "SQL"),
        Binding("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.push_screen("metrics")


def main() -> None:
    """Entry point for the TUI dashboard."""
    app = AgentStreamsTUI()
    app.run()


if __name__ == "__main__":
    main()
