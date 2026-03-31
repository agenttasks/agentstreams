# AgentStreams MCP Server

MCP server providing tools for querying Atlas metrics and ontology data from Neon Postgres.

## Tools

| Tool | Description |
|------|-------------|
| `list_metrics` | List all metrics with type, unit, dimensions |
| `query_metric` | Query time-series data with tag filters and aggregation |
| `metric_summary` | Statistical summary (min/max/avg/p50/p99) with grouping |
| `list_skills` | List registered skills and trigger patterns |
| `list_models` | List Claude models with capabilities |

## Resources

| URI | Description |
|-----|-------------|
| `agentstreams://metrics` | Metric catalog (JSON) |

## Setup

```bash
cd mcp-server
npm install
npm run build
```

## Usage with Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agentstreams": {
      "command": "node",
      "args": ["/path/to/agentstreams/mcp-server/dist/index.js"],
      "env": {
        "NEON_DATABASE_URL": "postgresql://user:pass@host/neondb?sslmode=require"
      }
    }
  }
}
```

## Usage with Claude Code

```bash
export NEON_DATABASE_URL="postgresql://..."
claude --mcp-server "node /path/to/mcp-server/dist/index.js"
```

## Example queries

```
# List all metrics
> list_metrics

# API cost breakdown by model (last 2 weeks)
> metric_summary metric_name=agentstreams.api.cost hours=336 group_by_tag=model

# Recent API requests for Opus crawl-ingest
> query_metric metric_name=agentstreams.api.requests hours=6 tags_filter={"model":"claude-opus-4-6","skill":"crawl-ingest"}

# Pipeline duration stats by stage
> metric_summary metric_name=agentstreams.pipeline.duration group_by_tag=stage
```
