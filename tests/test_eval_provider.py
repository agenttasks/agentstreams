"""Tests for evals/*/provider.py — promptfoo custom provider."""

import importlib
import sys
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


class TestCallApiMissingKey:
    def test_returns_error_when_no_key(self):
        mock_anthropic, _ = _make_mock_anthropic()
        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch.dict("os.environ", {}, clear=True),
        ):
            importlib.reload(provider)
            result = provider.call_api("hello", {"config": {}}, None)
        assert "error" in result
        assert "No API key" in result["error"]

    def test_returns_error_when_anthropic_not_installed(self):
        original_import = __import__

        def mock_import(name, *args, **kwargs):
            if name == "anthropic":
                raise ImportError("No module named 'anthropic'")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            result = provider.call_api("hello", {"config": {}}, None)
        assert "error" in result
        assert "not installed" in result["error"]


class TestCallApiKeyFallback:
    def test_uses_anthropic_api_key_first(self):
        mock_anthropic, _ = _make_mock_anthropic("response text")
        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch.dict(
                "os.environ",
                {"ANTHROPIC_API_KEY": "key-1", "CLAUDE_CODE_OAUTH_TOKEN": "key-2"},
            ),
        ):
            importlib.reload(provider)
            result = provider.call_api("hello", {"config": {}}, None)

        mock_anthropic.Anthropic.assert_called_once_with(api_key="key-1")
        assert result["output"] == "response text"

    def test_falls_back_to_oauth_token(self):
        mock_anthropic, _ = _make_mock_anthropic()
        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch.dict("os.environ", {"CLAUDE_CODE_OAUTH_TOKEN": "oauth-tok"}, clear=True),
        ):
            importlib.reload(provider)
            provider.call_api("hello", {"config": {}}, None)

        mock_anthropic.Anthropic.assert_called_once_with(api_key="oauth-tok")


class TestCallApiConfig:
    def test_passes_config_to_api(self):
        mock_anthropic, mock_client = _make_mock_anthropic()
        config = {"model": "claude-opus-4-6", "max_tokens": 2048, "temperature": 0.5}

        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}),
        ):
            importlib.reload(provider)
            provider.call_api("test prompt", {"config": config}, None)

        call_kwargs = mock_client.messages.create.call_args
        assert call_kwargs.kwargs["model"] == "claude-opus-4-6"
        assert call_kwargs.kwargs["max_tokens"] == 2048
        assert call_kwargs.kwargs["temperature"] == 0.5

    def test_default_config_values(self):
        mock_anthropic, mock_client = _make_mock_anthropic()
        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}),
        ):
            importlib.reload(provider)
            provider.call_api("test", {"config": {}}, None)

        call_kwargs = mock_client.messages.create.call_args
        assert call_kwargs.kwargs["model"] == "claude-sonnet-4-6"
        assert call_kwargs.kwargs["max_tokens"] == 1024
        assert call_kwargs.kwargs["temperature"] == 0


class TestCallApiTokenUsage:
    def test_returns_token_usage(self):
        mock_anthropic, _ = _make_mock_anthropic("hi", 100, 50)
        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}),
        ):
            importlib.reload(provider)
            result = provider.call_api("test", {"config": {}}, None)

        assert result["tokenUsage"]["total"] == 150
        assert result["tokenUsage"]["prompt"] == 100
        assert result["tokenUsage"]["completion"] == 50


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

        assert "error" in result
        assert "Authentication failed" in result["error"]

    def test_handles_generic_exception(self):
        mock_anthropic = MagicMock()
        mock_anthropic.AuthenticationError = type("AuthErr", (Exception,), {})
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = ConnectionError("network down")
        mock_anthropic.Anthropic.return_value = mock_client

        with (
            patch.dict("sys.modules", {"anthropic": mock_anthropic}),
            patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}),
        ):
            importlib.reload(provider)
            result = provider.call_api("test", {"config": {}}, None)

        assert "error" in result
        assert "network down" in result["error"]
