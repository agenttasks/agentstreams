"""Tests for extended-thinking and adaptive-thinking DSPy modules."""

from __future__ import annotations

from src.dspy_prompts import (
    AdaptiveThinking,
    ExtendedThinking,
    Field,
    Prediction,
    Signature,
)


class TestPredictionThinkingFields:
    def test_thinking_defaults_to_zero(self):
        p = Prediction(outputs={"x": 1})
        assert p.thinking_tokens == 0
        assert p.thinking_text == ""

    def test_thinking_fields_set(self):
        p = Prediction(
            outputs={"x": 1},
            thinking_tokens=5000,
            thinking_text="Let me think about this...",
        )
        assert p.thinking_tokens == 5000
        assert "think" in p.thinking_text.lower()


class TestExtendedThinking:
    def test_default_config(self):
        sig = Signature(name="Test", doc="Test task")
        mod = ExtendedThinking(sig)
        assert mod.model == "claude-opus-4-6"
        assert mod.budget_tokens == 10_000
        assert mod.temperature == 1.0  # required for thinking
        assert mod.max_tokens == 16_384

    def test_custom_budget(self):
        sig = Signature(name="Test", doc="Test task")
        mod = ExtendedThinking(sig, budget_tokens=50_000)
        assert mod.budget_tokens == 50_000

    def test_custom_model(self):
        sig = Signature(name="Test", doc="Test task")
        mod = ExtendedThinking(sig, model="claude-sonnet-4-6")
        assert mod.model == "claude-sonnet-4-6"

    def test_builds_messages(self):
        sig = Signature(
            name="Align",
            doc="Align entities",
            inputs=[Field("entities", "Entity list", "list")],
            outputs=[Field("mappings", "Mappings", "list")],
        )
        mod = ExtendedThinking(sig, budget_tokens=15_000)
        messages = mod._build_messages({"entities": "[{name: test}]"})
        assert len(messages) == 1
        assert "Align" in messages[0]["content"]


class TestAdaptiveThinking:
    def test_default_config(self):
        sig = Signature(name="Test", doc="Test task")
        mod = AdaptiveThinking(sig)
        assert mod.model == "claude-opus-4-6"
        assert mod.temperature == 1.0
        assert mod.max_tokens == 16_384

    def test_custom_model(self):
        sig = Signature(name="Test", doc="Test task")
        mod = AdaptiveThinking(sig, model="claude-sonnet-4-6")
        assert mod.model == "claude-sonnet-4-6"

    def test_builds_messages(self):
        sig = Signature(
            name="Classify",
            doc="Classify content",
            inputs=[Field("content", "Text"), Field("title", "Title")],
            outputs=[Field("category", "Category")],
        )
        mod = AdaptiveThinking(sig)
        messages = mod._build_messages({"content": "hello", "title": "test"})
        assert "Classify" in messages[0]["content"]
        assert "hello" in messages[0]["content"]
