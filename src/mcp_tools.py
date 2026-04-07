"""MCP SDK v2 tool server exposing AgentStreams capabilities.

Implements a Model Context Protocol server following the
modelcontextprotocol/sdk-python v2 specification with
Streamable HTTP transport.

Exposes src/ modules as MCP tools:
- bloom_check: Check/add items to persistent bloom filter
- crawl_urls: Execute a crawl pipeline
- dspy_extract: Run DSPy extraction on text
- project_ontology: Generate UDA projections
- query_metrics: Query dimensional metrics
- enqueue_task: Add tasks to processing queue

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolDefinition:
    """MCP v2 tool definition following the spec."""

    name: str
    description: str
    input_schema: dict[str, Any]


@dataclass
class ToolResult:
    """MCP v2 tool execution result."""

    content: list[dict[str, Any]]
    is_error: bool = False


# ── Tool Definitions ────────────────────────────────────────

TOOLS: list[ToolDefinition] = [
    ToolDefinition(
        name="bloom_check",
        description=(
            "Check if an item exists in a persistent bloom filter, "
            "optionally adding it. Uses Neon Postgres for cross-session state."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "filter_name": {
                    "type": "string",
                    "description": "Name of the bloom filter (e.g., 'crawler:docs')",
                },
                "item": {
                    "type": "string",
                    "description": "Item to check (URL, content hash, etc.)",
                },
                "add_if_new": {
                    "type": "boolean",
                    "description": "Add item to filter if not present (default: true)",
                    "default": True,
                },
            },
            "required": ["filter_name", "item"],
        },
    ),
    ToolDefinition(
        name="crawl_urls",
        description=(
            "Execute a Scrapy-pattern crawl pipeline. Fetches pages from "
            "sitemaps or URL lists, deduplicates via bloom filter, and "
            "persists results to Neon Postgres."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Pipeline name for tracking and bloom filter state",
                },
                "sitemap_urls": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Sitemap XML URLs to parse for page discovery",
                },
                "start_urls": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Direct URLs to crawl (alternative to sitemaps)",
                },
                "domains": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Allowed domains for crawling",
                },
                "concurrency": {
                    "type": "integer",
                    "description": "Max parallel requests (default: 20)",
                    "default": 20,
                },
                "max_pages": {
                    "type": "integer",
                    "description": "Maximum pages to crawl (default: 10000)",
                    "default": 10000,
                },
            },
            "required": ["name", "domains"],
        },
    ),
    ToolDefinition(
        name="dspy_extract",
        description=(
            "Run DSPy structured extraction on text using Claude. "
            "Supports entity extraction, content classification, "
            "API pattern extraction, and ontology alignment."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "enum": [
                        "extract_entities",
                        "classify_content",
                        "extract_api_patterns",
                        "align_to_ontology",
                    ],
                    "description": "Extraction task to run",
                },
                "inputs": {
                    "type": "object",
                    "description": "Input fields matching the task's signature",
                },
                "model": {
                    "type": "string",
                    "description": "Claude model to use (default: claude-sonnet-4-6)",
                    "default": "claude-sonnet-4-6",
                },
            },
            "required": ["task", "inputs"],
        },
    ),
    ToolDefinition(
        name="project_ontology",
        description=(
            "Generate UDA projections from the AgentStreams ontology. "
            "Produces Avro, GraphQL, DataContainer, and Mapping files."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "class_name": {
                    "type": "string",
                    "description": "Ontology class to project (or 'all' for everything)",
                },
                "format": {
                    "type": "string",
                    "enum": ["avro", "graphql", "datacontainer", "mapping", "all"],
                    "description": "Output format (default: all)",
                    "default": "all",
                },
                "output_dir": {
                    "type": "string",
                    "description": "Directory to write projection files",
                },
            },
            "required": ["class_name"],
        },
    ),
    ToolDefinition(
        name="query_metrics",
        description=(
            "Query dimensional time-series metrics from Neon Postgres. "
            "Supports filtering by metric name, tags, and time range."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "metric_name": {
                    "type": "string",
                    "description": "Metric name (e.g., 'agentstreams.crawl.pages')",
                },
                "tags": {
                    "type": "object",
                    "description": "Tag filters as key-value pairs",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results to return (default: 100)",
                    "default": 100,
                },
            },
            "required": ["metric_name"],
        },
    ),
    ToolDefinition(
        name="enqueue_task",
        description=(
            "Add a task to the Neon Postgres processing queue. "
            "Tasks are picked up by pgqueuer workers."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "queue_name": {
                    "type": "string",
                    "description": "Queue name (pgqueuer entrypoint)",
                },
                "task_type": {
                    "type": "string",
                    "enum": ["code", "knowledge_work", "financial"],
                    "description": "Task type classification",
                },
                "skill_name": {
                    "type": "string",
                    "description": "Skill to invoke for processing",
                },
                "input": {
                    "type": "object",
                    "description": "Task input payload",
                },
                "priority": {
                    "type": "integer",
                    "description": "Priority (higher = sooner, default: 0)",
                    "default": 0,
                },
            },
            "required": ["queue_name", "task_type"],
        },
    ),
]


# ── Tool Handler ────────────────────────────────────────────


class MCPToolHandler:
    """Handle MCP tool calls by dispatching to src/ modules.

    Following MCP SDK v2 patterns:
    - Tools are listed via list_tools()
    - Tool calls dispatched via call_tool()
    - Results returned as ToolResult with content array
    """

    def __init__(self, neon_url: str = ""):
        self.neon_url = neon_url

    def list_tools(self) -> list[dict]:
        """Return MCP v2 tool definitions."""
        return [
            {
                "name": t.name,
                "description": t.description,
                "inputSchema": t.input_schema,
            }
            for t in TOOLS
        ]

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        """Dispatch a tool call to the appropriate handler."""
        handlers = {
            "bloom_check": self._handle_bloom_check,
            "crawl_urls": self._handle_crawl_urls,
            "dspy_extract": self._handle_dspy_extract,
            "project_ontology": self._handle_project_ontology,
            "query_metrics": self._handle_query_metrics,
            "enqueue_task": self._handle_enqueue_task,
        }

        handler = handlers.get(name)
        if not handler:
            return ToolResult(
                content=[{"type": "text", "text": f"Unknown tool: {name}"}],
                is_error=True,
            )

        try:
            return await handler(arguments)
        except Exception as e:
            return ToolResult(
                content=[{"type": "text", "text": f"Error: {e}"}],
                is_error=True,
            )

    async def _handle_bloom_check(self, args: dict) -> ToolResult:
        from src.bloom import BloomFilter, NeonBloomStore
        from src.neon_db import connection_pool

        filter_name = args["filter_name"]
        item = args["item"]
        add_if_new = args.get("add_if_new", True)

        if self.neon_url:
            async with connection_pool(self.neon_url) as conn:
                store = NeonBloomStore(conn)
                bloom = await store.load(filter_name) or BloomFilter()
                exists = item in bloom
                if add_if_new and not exists:
                    bloom.add(item)
                    await store.save(filter_name, bloom)
        else:
            bloom = BloomFilter()
            exists = item in bloom
            if add_if_new:
                bloom.add(item)

        return ToolResult(content=[{
            "type": "text",
            "text": json.dumps({
                "filter": filter_name,
                "item": item,
                "exists": exists,
                "added": add_if_new and not exists,
                "filter_size": len(bloom),
                "estimated_fp_rate": bloom.estimated_fp_rate,
            }),
        }])

    async def _handle_crawl_urls(self, args: dict) -> ToolResult:
        from src.crawlers import CrawlConfig, UDACrawler

        config = CrawlConfig(
            name=args["name"],
            domains=args["domains"],
            sitemap_urls=args.get("sitemap_urls", []),
            start_urls=args.get("start_urls", []),
            concurrency=args.get("concurrency", 20),
            max_pages=args.get("max_pages", 10000),
            neon_url=self.neon_url,
        )
        crawler = UDACrawler(config)
        results = await crawler.crawl()

        counts = {"pages": 0, "resources": 0, "tasks": 0}
        if self.neon_url:
            counts = await crawler.persist()

        return ToolResult(content=[{
            "type": "text",
            "text": json.dumps({
                "crawled": len(results),
                "success": sum(1 for r in results if r.is_success),
                "errors": sum(1 for r in results if r.error),
                "persisted": counts,
            }),
        }])

    async def _handle_dspy_extract(self, args: dict) -> ToolResult:
        from src.dspy_prompts import (
            ALIGN_TO_ONTOLOGY,
            CLASSIFY_CONTENT,
            EXTRACT_API_PATTERNS,
            EXTRACT_ENTITIES,
            Module,
        )

        signatures = {
            "extract_entities": EXTRACT_ENTITIES,
            "classify_content": CLASSIFY_CONTENT,
            "extract_api_patterns": EXTRACT_API_PATTERNS,
            "align_to_ontology": ALIGN_TO_ONTOLOGY,
        }

        sig = signatures.get(args["task"])
        if not sig:
            return ToolResult(
                content=[{"type": "text", "text": f"Unknown task: {args['task']}"}],
                is_error=True,
            )

        model = args.get("model", "claude-sonnet-4-6")
        module = Module(sig, model=model)
        prediction = await module(**args["inputs"])

        return ToolResult(content=[{
            "type": "text",
            "text": json.dumps({
                "outputs": prediction.outputs,
                "model": prediction.model,
                "tokens": {
                    "input": prediction.input_tokens,
                    "output": prediction.output_tokens,
                },
            }),
        }])

    async def _handle_project_ontology(self, args: dict) -> ToolResult:
        from src.projections import (
            AvroProjection,
            DataContainerProjection,
            GraphQLProjection,
            MappingProjection,
            OntologyParser,
            generate_all_projections,
        )

        class_name = args["class_name"]
        fmt = args.get("format", "all")
        output_dir = args.get("output_dir")

        if class_name == "all":
            results = generate_all_projections(output_dir=output_dir)
            return ToolResult(content=[{
                "type": "text",
                "text": json.dumps({"files_generated": list(results.keys())}),
            }])

        parser = OntologyParser()
        parser.parse()

        output = {}
        if fmt in ("avro", "all"):
            output["avro"] = AvroProjection(parser).generate(class_name)
        if fmt in ("graphql", "all"):
            output["graphql"] = GraphQLProjection(parser).generate(class_name)
        if fmt in ("datacontainer", "all"):
            output["datacontainer"] = DataContainerProjection(parser).generate(class_name)
        if fmt in ("mapping", "all"):
            output["mapping"] = MappingProjection(parser).generate(class_name)

        return ToolResult(content=[{
            "type": "text",
            "text": json.dumps(output, default=str),
        }])

    async def _handle_query_metrics(self, args: dict) -> ToolResult:
        from src.neon_db import connection_pool

        if not self.neon_url:
            return ToolResult(
                content=[{"type": "text", "text": "No NEON_DATABASE_URL configured"}],
                is_error=True,
            )

        async with connection_pool(self.neon_url) as conn:
            tag_filters = args.get("tags", {})
            tag_clause = " AND ".join(
                f"tags->>'{k}' = '{v}'" for k, v in tag_filters.items()
            )
            where = "WHERE metric_name = %s"
            if tag_clause:
                where += f" AND {tag_clause}"

            rows = await (
                await conn.execute(
                    f"""SELECT metric_name, value, tags, recorded_at
                        FROM metric_values {where}
                        ORDER BY recorded_at DESC LIMIT %s""",
                    (args["metric_name"], args.get("limit", 100)),
                )
            ).fetchall()

        return ToolResult(content=[{
            "type": "text",
            "text": json.dumps([
                {
                    "metric": r[0],
                    "value": r[1],
                    "tags": r[2],
                    "recorded_at": r[3].isoformat() if r[3] else None,
                }
                for r in rows
            ]),
        }])

    async def _handle_enqueue_task(self, args: dict) -> ToolResult:
        from src.neon_db import connection_pool, enqueue_task

        if not self.neon_url:
            return ToolResult(
                content=[{"type": "text", "text": "No NEON_DATABASE_URL configured"}],
                is_error=True,
            )

        async with connection_pool(self.neon_url) as conn:
            task_id = await enqueue_task(
                conn,
                queue_name=args["queue_name"],
                task_type=args["task_type"],
                skill_name=args.get("skill_name"),
                task_input=args.get("input"),
                priority=args.get("priority", 0),
            )
            await conn.commit()

        return ToolResult(content=[{
            "type": "text",
            "text": json.dumps({"task_id": task_id, "status": "queued"}),
        }])
