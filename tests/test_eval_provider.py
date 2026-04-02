"""Tests for evals/*/provider.py — promptfoo custom provider."""

import importlib
import sys
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "evals" / "api-client"))

import provider


def _make_mock_anthropic(response_text="ok", input_tokens=10, output_tokens=20):
    """Build a mock anthropic module with pre-configured client."""
    mock = MagicMock()
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text=response_text)]
    mock_response.usage.input_tokens = input_tokens
    mock_response.usage.output_tokens = output_tokens
    mock_client.messages.create.return_value = mock_response
    mock.Anthropic.return_value = mock_client
    mock.AuthenticationError = Exception
    return mock, mock_client


@contextmanager
def _with_anthropic(response_text="ok", input_tokens=10, output_tokens=20, env=None, **kw):
    """Patch anthropic module, set env, reload provider, yield (mock, client)."""
    mock, client = _make_mock_anthropic(response_text, input_tokens, output_tokens)
    with (
        patch.dict("sys.modules", {"anthropic": mock}),
        patch.dict("os.environ", env or {}, clear=kw.get("clear_env", False)),
    ):
        importlib.reload(provider)
        yield mock, client


class TestCallApiMissingKey:
    def test_returns_error_when_no_key(self):
        with _with_anthropic(env={}, clear_env=True) as (_, __):
            result = provider.call_api("hello", {"config": {}}, None)
        assert "error" in result
        assert "No API key" in result["error"]

    def test_returns_error_when_anthropic_not_installed(self):
        original = __import__

        def mock_import(name, *args, **kwargs):
            if name == "anthropic":
                raise ImportError("No module named 'anthropic'")
            return original(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            result = provider.call_api("hello", {"config": {}}, None)
        assert "not installed" in result["error"]


class TestCallApiKeyFallback:
    def test_uses_anthropic_api_key_first(self):
        env = {"ANTHROPIC_API_KEY": "key-1", "CLAUDE_CODE_OAUTH_TOKEN": "key-2"}
        with _with_anthropic("response text", env=env) as (mock, _):
            result = provider.call_api("hello", {"config": {}}, None)
        mock.Anthropic.assert_called_once_with(api_key="key-1")
        assert result["output"] == "response text"

    def test_falls_back_to_oauth_token(self):
        with _with_anthropic(env={"CLAUDE_CODE_OAUTH_TOKEN": "oauth-tok"}, clear_env=True) as (
            mock,
            _,
        ):
            provider.call_api("hello", {"config": {}}, None)
        mock.Anthropic.assert_called_once_with(api_key="oauth-tok")


class TestCallApiConfig:
    def test_passes_config_to_api(self):
        config = {"model": "claude-opus-4-6", "max_tokens": 2048, "temperature": 0.5}
        with _with_anthropic(env={"ANTHROPIC_API_KEY": "k"}) as (_, client):
            provider.call_api("test", {"config": config}, None)
        kw = client.messages.create.call_args.kwargs
        assert kw["model"] == "claude-opus-4-6"
        assert kw["max_tokens"] == 2048
        assert kw["temperature"] == 0.5

    def test_default_config_values(self):
        with _with_anthropic(env={"ANTHROPIC_API_KEY": "k"}) as (_, client):
            provider.call_api("test", {"config": {}}, None)
        kw = client.messages.create.call_args.kwargs
        assert kw["model"] == "claude-sonnet-4-6"
        assert kw["max_tokens"] == 1024
        assert kw["temperature"] == 0


class TestCallApiTokenUsage:
    def test_returns_token_usage(self):
        with _with_anthropic("hi", 100, 50, env={"ANTHROPIC_API_KEY": "k"}) as (_, __):
            result = provider.call_api("test", {"config": {}}, None)
        assert result["tokenUsage"] == {"total": 150, "prompt": 100, "completion": 50}


class TestCallApiErrorHandling:
    def test_handles_auth_error(self):
        mock_anthropic = MagicMock()

        class FakeAuthError(Exception):
            pass

        mock_anthropic.AuthenticationError = FakeAuthError
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = FakeAuthError("bad key")
        mock_anthropic.Anthropic.return_value = mock_client

        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch.dict("os.environ", {"ANTHROPIC_API_KEY": "bad-key"}),
        ):
            importlib.reload(provider)
            result = provider.call_api("test", {"config": {}}, None)
        assert "Authentication failed" in result["error"]

    def test_handles_generic_exception(self):
        mock_anthropic = MagicMock()
        mock_anthropic.AuthenticationError = type("AuthErr", (Exception,), {})
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = ConnectionError("network down")
        mock_anthropic.Anthropic.return_value = mock_client

        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch.dict("os.environ", {"ANTHROPIC_API_KEY": "k"}),
        ):
            importlib.reload(provider)
            result = provider.call_api("test", {"config": {}}, None)
        assert "network down" in result["error"]
