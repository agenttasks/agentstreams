"""Tests for src/managed_agents.py — Managed Agents API client."""

from __future__ import annotations

from src.managed_agents import (
    AGENT_TOOLS,
    AgentCustomToolUseEvent,
    AgentMessageEvent,
    AgentToolset,
    AgentToolUseEvent,
    CustomTool,
    CustomToolResult,
    EnvironmentConfig,
    FileResource,
    GenericEvent,
    GitHubResource,
    ManagedAgentConfig,
    MCPServer,
    MCPToolset,
    NetworkConfig,
    NetworkingMode,
    Packages,
    SessionErrorEvent,
    SessionStatus,
    SessionStatusEvent,
    SpanEvent,
    TextContent,
    ToolConfig,
    ToolConfirmation,
    ToolPermission,
    UserInterrupt,
    UserMessage,
    coding_agent,
    data_analysis_env,
    parse_event,
    restricted_env,
    security_agent,
)

# ── Enum Tests ────────────────────────────────────────────────


class TestEnums:
    def test_session_status_values(self):
        assert SessionStatus.IDLE.value == "idle"
        assert SessionStatus.RUNNING.value == "running"
        assert SessionStatus.RESCHEDULING.value == "rescheduling"
        assert SessionStatus.TERMINATED.value == "terminated"

    def test_networking_mode_values(self):
        assert NetworkingMode.UNRESTRICTED.value == "unrestricted"
        assert NetworkingMode.LIMITED.value == "limited"

    def test_tool_permission_values(self):
        assert ToolPermission.ALWAYS_ALLOW.value == "always_allow"
        assert ToolPermission.ALWAYS_ASK.value == "always_ask"

    def test_agent_tools_tuple(self):
        assert "bash" in AGENT_TOOLS
        assert "read" in AGENT_TOOLS
        assert "write" in AGENT_TOOLS
        assert "edit" in AGENT_TOOLS
        assert "glob" in AGENT_TOOLS
        assert "grep" in AGENT_TOOLS
        assert "web_fetch" in AGENT_TOOLS
        assert "web_search" in AGENT_TOOLS
        assert len(AGENT_TOOLS) == 8


# ── Tool Config Tests ─────────────────────────────────────────


class TestToolConfig:
    def test_default_config(self):
        tc = ToolConfig(name="bash")
        assert tc.enabled is True
        assert tc.permission_policy == ToolPermission.ALWAYS_ALLOW

    def test_to_dict_default(self):
        tc = ToolConfig(name="bash")
        d = tc.to_dict()
        assert d == {"name": "bash", "enabled": True}
        assert "permission_policy" not in d

    def test_to_dict_with_permission(self):
        tc = ToolConfig(name="bash", permission_policy=ToolPermission.ALWAYS_ASK)
        d = tc.to_dict()
        assert d["permission_policy"] == {"type": "always_ask"}

    def test_disabled_tool(self):
        tc = ToolConfig(name="web_fetch", enabled=False)
        d = tc.to_dict()
        assert d == {"name": "web_fetch", "enabled": False}


class TestCustomTool:
    def test_to_dict(self):
        ct = CustomTool(
            name="get_weather",
            description="Get current weather",
            input_schema={
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                },
                "required": ["location"],
            },
        )
        d = ct.to_dict()
        assert d["type"] == "custom"
        assert d["name"] == "get_weather"
        assert d["description"] == "Get current weather"
        assert d["input_schema"]["type"] == "object"


class TestMCPServer:
    def test_to_dict(self):
        srv = MCPServer(name="github", url="https://api.githubcopilot.com/mcp/")
        d = srv.to_dict()
        assert d == {
            "type": "url",
            "name": "github",
            "url": "https://api.githubcopilot.com/mcp/",
        }


class TestMCPToolset:
    def test_to_dict_minimal(self):
        mt = MCPToolset(mcp_server_name="github")
        d = mt.to_dict()
        assert d == {"type": "mcp_toolset", "mcp_server_name": "github"}

    def test_to_dict_with_configs(self):
        mt = MCPToolset(
            mcp_server_name="github",
            configs=[ToolConfig(name="list_repos", enabled=True)],
        )
        d = mt.to_dict()
        assert "configs" in d
        assert d["configs"][0]["name"] == "list_repos"


# ── Agent Toolset Tests ───────────────────────────────────────


class TestAgentToolset:
    def test_default_toolset(self):
        ts = AgentToolset()
        d = ts.to_dict()
        assert d == {"type": "agent_toolset_20260401"}

    def test_toolset_with_disabled(self):
        ts = AgentToolset(
            configs=[
                ToolConfig(name="web_fetch", enabled=False),
                ToolConfig(name="web_search", enabled=False),
            ]
        )
        d = ts.to_dict()
        assert d["type"] == "agent_toolset_20260401"
        assert len(d["configs"]) == 2
        assert d["configs"][0]["name"] == "web_fetch"
        assert d["configs"][0]["enabled"] is False

    def test_toolset_selective_enable(self):
        ts = AgentToolset(
            default_enabled=False,
            configs=[
                ToolConfig(name="bash", enabled=True),
                ToolConfig(name="read", enabled=True),
            ],
        )
        d = ts.to_dict()
        assert d["default_config"]["enabled"] is False
        assert len(d["configs"]) == 2

    def test_toolset_default_permission(self):
        ts = AgentToolset(default_permission=ToolPermission.ALWAYS_ASK)
        d = ts.to_dict()
        assert d["default_config"]["permission_policy"]["type"] == "always_ask"


# ── ManagedAgentConfig Tests ──────────────────────────────────


class TestManagedAgentConfig:
    def test_minimal_config(self):
        config = ManagedAgentConfig(name="Test Agent")
        params = config.to_create_params()
        assert params["name"] == "Test Agent"
        assert params["model"] == "claude-sonnet-4-6"
        assert len(params["tools"]) == 1
        assert params["tools"][0]["type"] == "agent_toolset_20260401"

    def test_full_config(self):
        config = ManagedAgentConfig(
            name="Full Agent",
            model="claude-opus-4-6",
            system="You are helpful.",
            description="A full agent",
            toolset=AgentToolset(configs=[ToolConfig(name="web_fetch", enabled=False)]),
            custom_tools=[
                CustomTool(
                    name="get_data",
                    description="Fetch data",
                    input_schema={"type": "object", "properties": {}},
                )
            ],
            mcp_servers=[
                MCPServer(name="github", url="https://example.com/mcp/"),
            ],
            mcp_toolsets=[
                MCPToolset(mcp_server_name="github"),
            ],
            metadata={"team": "safety"},
        )
        params = config.to_create_params()
        assert params["model"] == "claude-opus-4-6"
        assert params["system"] == "You are helpful."
        assert params["description"] == "A full agent"
        assert len(params["tools"]) == 3  # toolset + custom + mcp_toolset
        assert params["tools"][1]["type"] == "custom"
        assert params["tools"][2]["type"] == "mcp_toolset"
        assert len(params["mcp_servers"]) == 1
        assert params["metadata"]["team"] == "safety"

    def test_fast_mode(self):
        config = ManagedAgentConfig(
            name="Fast Agent",
            model="claude-opus-4-6",
            fast_mode=True,
        )
        params = config.to_create_params()
        assert params["model"] == {"id": "claude-opus-4-6", "speed": "fast"}


# ── Environment Config Tests ──────────────────────────────────


class TestNetworkConfig:
    def test_unrestricted(self):
        nc = NetworkConfig()
        assert nc.to_dict() == {"type": "unrestricted"}

    def test_limited(self):
        nc = NetworkConfig(
            mode=NetworkingMode.LIMITED,
            allowed_hosts=["api.example.com"],
            allow_mcp_servers=True,
            allow_package_managers=True,
        )
        d = nc.to_dict()
        assert d["type"] == "limited"
        assert d["allowed_hosts"] == ["api.example.com"]
        assert d["allow_mcp_servers"] is True
        assert d["allow_package_managers"] is True


class TestPackages:
    def test_empty(self):
        p = Packages()
        assert p.to_dict() == {}

    def test_mixed_packages(self):
        p = Packages(
            pip=["pandas", "numpy"],
            npm=["express"],
            apt=["ffmpeg"],
        )
        d = p.to_dict()
        assert d["pip"] == ["pandas", "numpy"]
        assert d["npm"] == ["express"]
        assert d["apt"] == ["ffmpeg"]
        assert "cargo" not in d


class TestEnvironmentConfig:
    def test_minimal(self):
        ec = EnvironmentConfig(name="test-env")
        params = ec.to_create_params()
        assert params["name"] == "test-env"
        assert params["config"]["type"] == "cloud"
        assert params["config"]["networking"]["type"] == "unrestricted"

    def test_with_packages(self):
        ec = EnvironmentConfig(
            name="data-env",
            packages=Packages(pip=["pandas"]),
        )
        params = ec.to_create_params()
        assert params["config"]["packages"]["pip"] == ["pandas"]

    def test_with_limited_networking(self):
        ec = EnvironmentConfig(
            name="secure-env",
            networking=NetworkConfig(
                mode=NetworkingMode.LIMITED,
                allowed_hosts=["api.example.com"],
            ),
        )
        params = ec.to_create_params()
        assert params["config"]["networking"]["type"] == "limited"


# ── Resource Tests ────────────────────────────────────────────


class TestGitHubResource:
    def test_minimal(self):
        r = GitHubResource(url="https://github.com/org/repo")
        d = r.to_dict()
        assert d["type"] == "github_repository"
        assert d["url"] == "https://github.com/org/repo"
        assert "checkout" not in d

    def test_with_branch(self):
        r = GitHubResource(
            url="https://github.com/org/repo",
            branch="main",
            authorization_token="ghp_xxx",
        )
        d = r.to_dict()
        assert d["checkout"] == {"type": "branch", "name": "main"}
        assert d["authorization_token"] == "ghp_xxx"

    def test_with_commit(self):
        r = GitHubResource(
            url="https://github.com/org/repo",
            commit_sha="abc123",
        )
        d = r.to_dict()
        assert d["checkout"] == {"type": "commit", "sha": "abc123"}


class TestFileResource:
    def test_minimal(self):
        r = FileResource(file_id="file_xxx")
        d = r.to_dict()
        assert d == {"type": "file", "file_id": "file_xxx"}

    def test_with_mount_path(self):
        r = FileResource(file_id="file_xxx", mount_path="/data/input.csv")
        d = r.to_dict()
        assert d["mount_path"] == "/data/input.csv"


# ── Event Types Tests ─────────────────────────────────────────


class TestUserMessage:
    def test_from_text(self):
        msg = UserMessage.from_text("Hello")
        d = msg.to_dict()
        assert d["type"] == "user.message"
        assert d["content"][0]["type"] == "text"
        assert d["content"][0]["text"] == "Hello"

    def test_multi_content(self):
        msg = UserMessage(content=[TextContent(text="Part 1"), TextContent(text="Part 2")])
        d = msg.to_dict()
        assert len(d["content"]) == 2


class TestUserInterrupt:
    def test_to_dict(self):
        i = UserInterrupt()
        assert i.to_dict() == {"type": "user.interrupt"}


class TestToolConfirmation:
    def test_allow(self):
        tc = ToolConfirmation(tool_use_id="tu_123", result="allow")
        d = tc.to_dict()
        assert d["type"] == "user.tool_confirmation"
        assert d["result"] == "allow"
        assert "deny_message" not in d

    def test_deny(self):
        tc = ToolConfirmation(
            tool_use_id="tu_123",
            result="deny",
            deny_message="Not allowed",
        )
        d = tc.to_dict()
        assert d["result"] == "deny"
        assert d["deny_message"] == "Not allowed"


class TestCustomToolResult:
    def test_success(self):
        ctr = CustomToolResult(
            custom_tool_use_id="ctu_123",
            content=[TextContent(text="72°F")],
        )
        d = ctr.to_dict()
        assert d["type"] == "user.custom_tool_result"
        assert d["is_error"] is False

    def test_error(self):
        ctr = CustomToolResult(
            custom_tool_use_id="ctu_123",
            content=[TextContent(text="Connection failed")],
            is_error=True,
        )
        d = ctr.to_dict()
        assert d["is_error"] is True


# ── Event Parsing Tests ───────────────────────────────────────


class TestParseEvent:
    def test_agent_message(self):
        raw = {
            "type": "agent.message",
            "id": "msg_123",
            "content": [{"type": "text", "text": "Hello world"}],
        }
        event = parse_event(raw)
        assert isinstance(event, AgentMessageEvent)
        assert event.text == "Hello world"
        assert event.id == "msg_123"

    def test_agent_message_multi_block(self):
        raw = {
            "type": "agent.message",
            "id": "msg_456",
            "content": [
                {"type": "text", "text": "Part 1 "},
                {"type": "text", "text": "Part 2"},
            ],
        }
        event = parse_event(raw)
        assert isinstance(event, AgentMessageEvent)
        assert event.text == "Part 1 Part 2"

    def test_agent_tool_use(self):
        raw = {
            "type": "agent.tool_use",
            "id": "tu_789",
            "name": "bash",
            "input": {"command": "ls"},
        }
        event = parse_event(raw)
        assert isinstance(event, AgentToolUseEvent)
        assert event.name == "bash"
        assert event.input == {"command": "ls"}

    def test_agent_custom_tool_use(self):
        raw = {
            "type": "agent.custom_tool_use",
            "id": "ctu_999",
            "name": "get_weather",
            "input": {"location": "SF"},
        }
        event = parse_event(raw)
        assert isinstance(event, AgentCustomToolUseEvent)
        assert event.name == "get_weather"
        assert event.input["location"] == "SF"

    def test_session_status_idle(self):
        raw = {
            "type": "session.status_idle",
            "stop_reason": "end_turn",
        }
        event = parse_event(raw)
        assert isinstance(event, SessionStatusEvent)
        assert event.status == SessionStatus.IDLE
        assert event.stop_reason == "end_turn"

    def test_session_status_running(self):
        raw = {"type": "session.status_running"}
        event = parse_event(raw)
        assert isinstance(event, SessionStatusEvent)
        assert event.status == SessionStatus.RUNNING

    def test_session_status_terminated(self):
        raw = {"type": "session.status_terminated"}
        event = parse_event(raw)
        assert isinstance(event, SessionStatusEvent)
        assert event.status == SessionStatus.TERMINATED

    def test_session_error(self):
        raw = {
            "type": "session.error",
            "error": {
                "type": "container_error",
                "message": "Container crashed",
            },
        }
        event = parse_event(raw)
        assert isinstance(event, SessionErrorEvent)
        assert event.error_type == "container_error"
        assert event.message == "Container crashed"

    def test_span_event(self):
        raw = {"type": "span.model_request_start"}
        event = parse_event(raw)
        assert isinstance(event, SpanEvent)
        assert event.span_type == "span.model_request_start"

    def test_unknown_event(self):
        raw = {"type": "something.unknown", "data": "test"}
        event = parse_event(raw)
        assert isinstance(event, GenericEvent)
        assert event.event_type == "something.unknown"

    def test_unknown_session_status(self):
        raw = {"type": "session.status_unknown_future"}
        event = parse_event(raw)
        assert isinstance(event, SessionStatusEvent)
        assert event.status == SessionStatus.IDLE  # fallback


# ── Factory Function Tests ────────────────────────────────────


class TestFactoryFunctions:
    def test_coding_agent_default(self):
        config = coding_agent()
        assert config.name == "Coding Assistant"
        assert config.model == "claude-sonnet-4-6"
        params = config.to_create_params()
        assert params["tools"][0]["type"] == "agent_toolset_20260401"
        assert "configs" not in params["tools"][0]

    def test_coding_agent_no_web(self):
        config = coding_agent(disable_web=True)
        params = config.to_create_params()
        configs = params["tools"][0]["configs"]
        disabled_names = {c["name"] for c in configs if not c["enabled"]}
        assert "web_fetch" in disabled_names
        assert "web_search" in disabled_names

    def test_security_agent(self):
        config = security_agent()
        assert config.model == "claude-opus-4-6"
        params = config.to_create_params()
        toolset = params["tools"][0]
        assert toolset["default_config"]["enabled"] is False
        enabled_names = {c["name"] for c in toolset["configs"] if c["enabled"]}
        assert "bash" in enabled_names
        assert "read" in enabled_names
        assert "glob" in enabled_names
        assert "grep" in enabled_names
        # write and edit should not be enabled
        assert "write" not in enabled_names
        assert "edit" not in enabled_names

    def test_data_analysis_env(self):
        config = data_analysis_env()
        params = config.to_create_params()
        assert params["name"] == "data-analysis"
        assert "pandas" in params["config"]["packages"]["pip"]
        assert params["config"]["networking"]["type"] == "unrestricted"

    def test_data_analysis_env_custom(self):
        config = data_analysis_env(
            name="custom-env",
            pip_packages=["torch"],
            npm_packages=["express"],
        )
        params = config.to_create_params()
        assert params["name"] == "custom-env"
        assert params["config"]["packages"]["pip"] == ["torch"]
        assert params["config"]["packages"]["npm"] == ["express"]

    def test_restricted_env(self):
        config = restricted_env(allowed_hosts=["api.example.com"])
        params = config.to_create_params()
        assert params["config"]["networking"]["type"] == "limited"
        assert params["config"]["networking"]["allowed_hosts"] == ["api.example.com"]
        assert params["config"]["networking"]["allow_package_managers"] is True


# ── Managed Harness Tests ────────────────────────────────────


class TestManagedStepResult:
    def test_to_task_result_pass(self):
        from src.managed_harness import ManagedStepResult

        mr = ManagedStepResult(
            agent_name="security-auditor",
            session_id="sess_123",
            messages=["No issues found.\n\nVerdict: PASS"],
        )
        tr = mr.to_task_result("test-step")
        assert tr.task_id == "test-step"
        assert tr.status == "completed"
        assert tr.outputs["verdict"] == "PASS"

    def test_to_task_result_block(self):
        from src.managed_harness import ManagedStepResult

        mr = ManagedStepResult(
            agent_name="security-auditor",
            session_id="sess_456",
            messages=["Critical SQL injection found.\n\nVerdict: BLOCK"],
        )
        tr = mr.to_task_result("test-step")
        assert tr.outputs["verdict"] == "BLOCK"

    def test_to_task_result_alignment(self):
        from src.managed_harness import ManagedStepResult

        mr = ManagedStepResult(
            agent_name="alignment-auditor",
            session_id="sess_789",
            messages=["No deceptive patterns detected.\n\nVerdict: ALIGNED"],
        )
        tr = mr.to_task_result("test-step")
        assert tr.outputs["verdict"] == "ALIGNED"

    def test_to_task_result_classification(self):
        from src.managed_harness import ManagedStepResult

        mr = ManagedStepResult(
            agent_name="harmlessness-screen",
            session_id="sess_000",
            messages=['{"classification": "safe", "confidence": 95}'],
        )
        tr = mr.to_task_result("test-step")
        assert tr.outputs["classification"] == "safe"

    def test_to_task_result_error(self):
        from src.managed_harness import ManagedStepResult

        mr = ManagedStepResult(
            agent_name="code-generator",
            session_id="sess_err",
            error="Container crashed",
        )
        tr = mr.to_task_result("test-step")
        assert tr.status == "failed"
        assert tr.error == "Container crashed"


class TestAgentConfigConversion:
    def test_convert_basic(self):
        from src.agent_tasks import AgentConfig
        from src.managed_harness import agent_config_to_managed

        config = AgentConfig(
            name="test-agent",
            model="claude-sonnet-4-6",
            system_prompt="Test prompt",
        )
        managed = agent_config_to_managed(config)
        assert managed.name == "test-agent"
        assert managed.model == "claude-sonnet-4-6"
        assert managed.system == "Test prompt"

    def test_convert_read_only(self):
        from src.agent_tasks import AgentConfig
        from src.managed_harness import agent_config_to_managed

        config = AgentConfig(name="security-auditor", model="claude-opus-4-6")
        managed = agent_config_to_managed(config, disable_write=True)
        params = managed.to_create_params()
        disabled_names = {
            c["name"] for c in params["tools"][0].get("configs", []) if not c["enabled"]
        }
        assert "write" in disabled_names
        assert "edit" in disabled_names

    def test_read_only_agents_set(self):
        from src.managed_harness import READ_ONLY_AGENTS

        assert "security-auditor" in READ_ONLY_AGENTS
        assert "alignment-auditor" in READ_ONLY_AGENTS
        assert "architecture-reviewer" in READ_ONLY_AGENTS
        assert "harmlessness-screen" in READ_ONLY_AGENTS
        assert "code-generator" not in READ_ONLY_AGENTS
