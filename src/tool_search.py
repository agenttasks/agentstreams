"""Tool search and discovery for the agentstreams toolkit.

Implements a lightweight in-process tool index that mirrors the
tool-search pattern from the Claude Agent SDK: tools are registered
with a name, description, and JSON Schema, then retrieved by keyword
query or exact name lookup.

Two pre-built loaders are provided:
- from_skills()        — reads SKILL.md frontmatter from a skills/ tree
- from_mcp_servers()   — reads the tools list advertised by MCP server configs

The pre-built singleton ``DEFAULT_INDEX`` is populated at import time from
the project's skills/ directory and the vendored knowledge-work-plugins.

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ── Project root ────────────────────────────────────────────────────────────

_PROJECT_ROOT = Path(__file__).parent.parent

# ── DeferredTool ────────────────────────────────────────────────────────────


@dataclass
class DeferredTool:
    """A lazily-loaded tool registration entry.

    Tools start unloaded (``loaded=False``) so that the index can be built
    quickly from directory scans without reading every schema file up front.
    Call ``ToolIndex.load(name)`` to populate ``schema``.

    Attributes:
        name: Unique tool identifier (matches SKILL.md ``name`` field or MCP
            tool name).
        description: One-line human-readable description used for search
            ranking.
        loaded: True once ``schema`` has been populated from its source file.
        schema: Full JSON Schema dict for the tool's input parameters.
            ``None`` until the tool has been loaded.
        source_path: Filesystem path to the SKILL.md or schema file this
            tool was built from.  May be empty for programmatically-registered
            tools.
    """

    name: str
    description: str
    loaded: bool = False
    schema: dict[str, Any] | None = None
    source_path: str = ""


# ── ToolIndex ───────────────────────────────────────────────────────────────


class ToolIndex:
    """Registry for tool discovery, search, and deferred loading.

    Tools are stored by name in an internal dict.  ``search`` does a simple
    case-insensitive keyword scan across names and descriptions — sufficient
    for the typical "find the right tool" use-case without requiring a vector
    store.

    Example usage::

        index = ToolIndex.from_skills(Path("skills"))
        results = index.search("code review", max_results=3)
        schema  = index.load("code-review")
    """

    def __init__(self) -> None:
        self._tools: dict[str, DeferredTool] = {}

    # ── Registration ────────────────────────────────────────────────────

    def register(
        self,
        name: str,
        description: str,
        schema: dict[str, Any] | None = None,
        source_path: str = "",
    ) -> DeferredTool:
        """Register a tool with the index.

        If a tool with the same ``name`` already exists it is overwritten.

        Args:
            name: Unique tool name (slug-style, e.g. ``"code-review"``).
            description: Short description used for keyword search.
            schema: Optional full JSON Schema dict.  When provided the tool
                is immediately marked as ``loaded=True``.
            source_path: Optional path to the source file for deferred loading.

        Returns:
            The ``DeferredTool`` that was stored.
        """
        tool = DeferredTool(
            name=name,
            description=description,
            loaded=schema is not None,
            schema=schema,
            source_path=source_path,
        )
        self._tools[name] = tool
        return tool

    # ── Search ──────────────────────────────────────────────────────────

    def search(self, query: str, max_results: int = 5) -> list[DeferredTool]:
        """Keyword search over registered tools.

        Ranks results by the number of query tokens that appear in the
        tool's name or description (case-insensitive).  Ties are broken by
        registration order (alphabetical by name).

        Args:
            query: Free-text query string.
            max_results: Maximum number of results to return.

        Returns:
            List of matching ``DeferredTool`` objects, highest-scoring first.
        """
        tokens = [t.lower() for t in re.split(r"[\s\-_/]+", query) if t]
        if not tokens:
            return list(self._tools.values())[:max_results]

        scored: list[tuple[int, str, DeferredTool]] = []
        for name, tool in self._tools.items():
            haystack = f"{tool.name} {tool.description}".lower()
            score = sum(1 for tok in tokens if tok in haystack)
            if score > 0:
                scored.append((score, name, tool))

        scored.sort(key=lambda x: (-x[0], x[1]))
        return [t for _, _, t in scored[:max_results]]

    # ── Load ────────────────────────────────────────────────────────────

    def load(self, name: str) -> dict[str, Any] | None:
        """Load and return the full schema for a registered tool.

        If the tool already has a schema cached it is returned immediately.
        Otherwise the source SKILL.md (or JSON file) is read and a minimal
        schema is synthesised from the frontmatter.

        Args:
            name: Tool name as registered.

        Returns:
            JSON Schema dict, or ``None`` if the tool is not found.
        """
        tool = self._tools.get(name)
        if tool is None:
            return None

        if tool.loaded and tool.schema is not None:
            return tool.schema

        if tool.source_path:
            schema = _load_schema_from_path(Path(tool.source_path))
            tool.schema = schema
            tool.loaded = True
            return schema

        # No source path — mark loaded with an empty schema so we don't retry.
        tool.loaded = True
        tool.schema = {"type": "object", "properties": {}}
        return tool.schema

    # ── Listing ─────────────────────────────────────────────────────────

    def list_all(self) -> list[DeferredTool]:
        """Return all registered tools sorted by name."""
        return sorted(self._tools.values(), key=lambda t: t.name)

    def __len__(self) -> int:
        return len(self._tools)

    # ── Factory: MCP servers ────────────────────────────────────────────

    @classmethod
    def from_mcp_servers(
        cls,
        server_configs: list[dict[str, Any]],
    ) -> "ToolIndex":
        """Build an index from a list of MCP server tool definitions.

        Each entry in ``server_configs`` should follow the MCP tools-list
        response shape::

            {
                "name": "my-tool",
                "description": "Does something useful",
                "inputSchema": { ... }   # JSON Schema
            }

        Both ``inputSchema`` (MCP v2 style) and ``input_schema`` (SDK style)
        key names are accepted.

        Args:
            server_configs: List of MCP tool definition dicts.

        Returns:
            Populated ``ToolIndex``.
        """
        index = cls()
        for entry in server_configs:
            name = entry.get("name", "")
            description = entry.get("description", "")
            # Accept both casing conventions
            schema = entry.get("inputSchema") or entry.get("input_schema")
            if name:
                index.register(name, description, schema=schema)
        return index

    # ── Factory: skills directory ───────────────────────────────────────

    @classmethod
    def from_skills(cls, skills_dir: Path) -> "ToolIndex":
        """Build an index by scanning a skills/ directory tree for SKILL.md files.

        Each SKILL.md must have YAML frontmatter with at minimum a ``name``
        field.  The ``description`` field is used for search ranking.

        Args:
            skills_dir: Path to the root of the skills directory.

        Returns:
            Populated ``ToolIndex``.
        """
        index = cls()
        if not skills_dir.exists():
            return index

        for skill_file in sorted(skills_dir.rglob("SKILL.md")):
            name, description = _parse_skill_frontmatter(skill_file)
            if name:
                index.register(
                    name=name,
                    description=description,
                    source_path=str(skill_file),
                )
        return index


# ── Frontmatter helpers ─────────────────────────────────────────────────────


def _parse_skill_frontmatter(path: Path) -> tuple[str, str]:
    """Parse ``name`` and ``description`` from a SKILL.md YAML frontmatter block.

    Args:
        path: Path to a SKILL.md file.

    Returns:
        Tuple of (name, description).  Either may be an empty string if the
        field is absent or the file cannot be read.
    """
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return "", ""

    if not text.startswith("---"):
        return "", ""

    end = text.find("---", 3)
    if end == -1:
        return "", ""

    frontmatter = text[3:end]
    name = ""
    description = ""

    for line in frontmatter.splitlines():
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            raw = line.split(":", 1)[1].strip().strip('"').strip("'")
            # Descriptions can be long; trim to first sentence for display.
            description = raw.split(".")[0].rstrip(",;") if raw else ""

    return name, description


def _load_schema_from_path(path: Path) -> dict[str, Any]:
    """Synthesise a JSON Schema dict from a SKILL.md file.

    The schema is intentionally minimal — a single ``input`` string property
    derived from the ``argument-hint`` frontmatter field (if present).  Callers
    that need richer schemas should register tools with an explicit ``schema``
    argument.

    Args:
        path: Path to a SKILL.md (or any markdown file with frontmatter).

    Returns:
        JSON Schema dict.
    """
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return {"type": "object", "properties": {}}

    argument_hint = ""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                if line.startswith("argument-hint:"):
                    argument_hint = line.split(":", 1)[1].strip().strip('"').strip("'")

    properties: dict[str, Any] = {
        "input": {
            "type": "string",
            "description": argument_hint or "Input for this skill",
        }
    }
    return {
        "type": "object",
        "properties": properties,
        "required": ["input"],
    }


# ── Pre-built default index ─────────────────────────────────────────────────


def _build_default_index() -> ToolIndex:
    """Build the default singleton index from project skills and vendor plugins."""
    index = ToolIndex()

    # Merge skills/ tree
    skills_index = ToolIndex.from_skills(_PROJECT_ROOT / "skills")
    for tool in skills_index.list_all():
        index._tools[tool.name] = tool  # noqa: SLF001

    # Merge vendors/knowledge-work-plugins/ tree
    vendor_index = ToolIndex.from_skills(
        _PROJECT_ROOT / "vendors" / "knowledge-work-plugins"
    )
    for tool in vendor_index.list_all():
        # Prefix vendor tools to avoid name collisions with first-party skills.
        prefixed_name = f"kwp:{tool.name}"
        existing = index._tools.get(prefixed_name)  # noqa: SLF001
        if existing is None:
            tool.name = prefixed_name
            index._tools[prefixed_name] = tool  # noqa: SLF001

    return index


# Singleton — populated once at first import.
DEFAULT_INDEX: ToolIndex = _build_default_index()
