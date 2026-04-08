"""Tests for src/agent_tasks.py — Agent SDK v2 task orchestration."""

from __future__ import annotations

from src.agent_tasks import (
    AgentConfig,
    AgentRunner,
    AgentTool,
    TaskResult,
    TaskSpec,
    crawl_agent_config,
    extract_agent_config,
    projection_agent_config,
)


class TestTaskSpec:
    def test_to_xml(self):
        task = TaskSpec(
            task_id="task-001",
            task_type="crawl",
            description="Crawl documentation",
            inputs={"url": "https://example.com"},
            config={"concurrency": "10"},
        )
        xml = task.to_xml()
        assert '<task id="task-001" type="crawl">' in xml
        assert "Crawl documentation" in xml
        assert '<field name="url">https://example.com</field>' in xml
        assert '<param name="concurrency">10</param>' in xml

    def test_to_xml_with_depends(self):
        task = TaskSpec(
            task_id="task-002",
            task_type="extract",
            description="Extract entities",
            depends_on=["task-001"],
        )
        xml = task.to_xml()
        assert "<depends-on>task-001</depends-on>" in xml

    def test_to_xml_without_depends(self):
        task = TaskSpec(
            task_id="task-003",
            task_type="project",
            description="Generate projections",
        )
        xml = task.to_xml()
        assert "depends-on" not in xml


class TestAgentConfig:
    def test_defaults(self):
        config = AgentConfig(name="test-agent")
        assert config.model == "claude-sonnet-4-6"
        assert config.max_turns == 25
        assert config.temperature == 0.0

    def test_custom(self):
        config = AgentConfig(
            name="custom",
            model="claude-opus-4-6",
            max_turns=50,
            tools=[AgentTool(name="t", description="d", input_schema={})],
        )
        assert config.model == "claude-opus-4-6"
        assert len(config.tools) == 1


class TestTaskResult:
    def test_completed(self):
        r = TaskResult(task_id="t1", status="completed", outputs={"result": "ok"})
        assert r.status == "completed"
        assert r.outputs["result"] == "ok"

    def test_failed(self):
        r = TaskResult(task_id="t2", status="failed", error="timeout")
        assert r.status == "failed"
        assert r.error == "timeout"


class TestPreBuiltConfigs:
    def test_crawl_agent_config(self):
        config = crawl_agent_config()
        assert config.name == "crawl-agent"
        tool_names = {t.name for t in config.tools}
        assert "crawl_urls" in tool_names
        assert "bloom_check" in tool_names

    def test_extract_agent_config(self):
        config = extract_agent_config()
        assert config.name == "extract-agent"
        tool_names = {t.name for t in config.tools}
        assert "dspy_extract" in tool_names

    def test_projection_agent_config(self):
        config = projection_agent_config()
        assert config.name == "projection-agent"
        tool_names = {t.name for t in config.tools}
        assert "project_ontology" in tool_names


class TestAgentRunner:
    def test_build_system_prompt(self):
        config = AgentConfig(
            name="test",
            tools=[AgentTool(name="bloom_check", description="Check bloom", input_schema={})],
        )
        runner = AgentRunner(config)
        task = TaskSpec(
            task_id="t1",
            task_type="crawl",
            description="Test crawl",
        )
        prompt = runner._build_system_prompt(task)
        assert "test" in prompt
        assert "bloom_check" in prompt
        assert "ANTHROPIC_API_KEY" in prompt  # warning about not using it
        assert "CLAUDE_CODE_OAUTH_TOKEN" in prompt
