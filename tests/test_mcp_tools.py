"""Tests for src/mcp_tools.py — MCP SDK v2 tool server."""

from __future__ import annotations

import pytest

from src.mcp_tools import TOOLS, MCPToolHandler, ToolDefinition, ToolResult


class TestToolDefinitions:
    def test_all_tools_have_required_fields(self):
        for tool in TOOLS:
            assert isinstance(tool, ToolDefinition)
            assert tool.name
            assert tool.description
            assert isinstance(tool.input_schema, dict)
            assert tool.input_schema.get("type") == "object"

    def test_expected_tools_exist(self):
        tool_names = {t.name for t in TOOLS}
        expected = {
            "bloom_check",
            "crawl_urls",
            "dspy_extract",
            "project_ontology",
            "query_metrics",
            "enqueue_task",
        }
        assert expected == tool_names

    def test_bloom_check_schema(self):
        tool = next(t for t in TOOLS if t.name == "bloom_check")
        props = tool.input_schema["properties"]
        assert "filter_name" in props
        assert "item" in props
        assert "add_if_new" in props
        required = tool.input_schema["required"]
        assert "filter_name" in required
        assert "item" in required

    def test_crawl_urls_schema(self):
        tool = next(t for t in TOOLS if t.name == "crawl_urls")
        props = tool.input_schema["properties"]
        assert "name" in props
        assert "domains" in props
        assert "sitemap_urls" in props

    def test_dspy_extract_schema(self):
        tool = next(t for t in TOOLS if t.name == "dspy_extract")
        props = tool.input_schema["properties"]
        assert "task" in props
        assert "inputs" in props
        assert set(props["task"]["enum"]) == {
            "extract_entities",
            "classify_content",
            "extract_api_patterns",
            "align_to_ontology",
        }


class TestMCPToolHandler:
    def test_list_tools(self):
        handler = MCPToolHandler()
        tools = handler.list_tools()
        assert len(tools) == len(TOOLS)
        for tool in tools:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool

    @pytest.mark.asyncio
    async def test_unknown_tool_returns_error(self):
        handler = MCPToolHandler()
        result = await handler.call_tool("nonexistent", {})
        assert result.is_error is True
        assert "Unknown tool" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_bloom_check_without_neon(self):
        handler = MCPToolHandler()
        result = await handler.call_tool("bloom_check", {
            "filter_name": "test",
            "item": "hello",
        })
        assert result.is_error is False
        import json
        data = json.loads(result.content[0]["text"])
        assert data["filter"] == "test"
        assert data["item"] == "hello"
        assert data["exists"] is False
        assert data["added"] is True


class TestToolResult:
    def test_default_not_error(self):
        r = ToolResult(content=[{"type": "text", "text": "ok"}])
        assert r.is_error is False

    def test_error_result(self):
        r = ToolResult(content=[{"type": "text", "text": "fail"}], is_error=True)
        assert r.is_error is True
