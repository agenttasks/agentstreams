"""Julia eval provider for promptfoo — code-graded and LLM-graded evaluations.

Follows Anthropic's eval framework (platform.claude.com/docs/en/test-and-evaluate):
  - Code-graded: exact match for verdicts, risk scores, branded type safety
  - LLM-graded: legal analysis quality, citation accuracy, tone (Likert 1-5)
  - Emotion-graded: desperation detection, deflection, gate decisions

Auth: CLAUDE_CODE_OAUTH_TOKEN (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

from typing import Any

import anthropic


def get_client() -> anthropic.Anthropic:
    """Create Anthropic client using CLAUDE_CODE_OAUTH_TOKEN."""
    return anthropic.Anthropic()


def call_model(prompt: str, config: dict[str, Any] | None = None) -> str:
    """Call Claude with the given prompt and return text response."""
    cfg = config or {}
    client = get_client()
    response = client.messages.create(
        model=cfg.get("model", "claude-opus-4-6"),
        max_tokens=cfg.get("max_tokens", 4096),
        temperature=cfg.get("temperature", 0),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def call_provider(prompt: str, options: dict[str, Any]) -> dict[str, Any]:
    """Promptfoo provider entry point."""
    config = options.get("config", {})
    try:
        output = call_model(prompt, config)
        return {"output": output}
    except Exception as e:
        return {"output": "", "error": str(e)}
