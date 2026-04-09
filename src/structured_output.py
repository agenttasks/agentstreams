"""Structured output helpers for the agentstreams toolkit.

Wraps the Claude Code CLI subprocess interface to produce JSON-validated
outputs from natural-language prompts.  Follows the Agent SDK structured
output pattern: the model is instructed to emit only a JSON object matching
a caller-supplied JSON Schema, and the raw response is validated before
being returned to the caller.

Callers supply an arbitrary JSON Schema dict; three pre-built schemas are
provided for the most common agentstreams use-cases:

- ``VERDICT_SCHEMA``       — security/alignment audit verdict
- ``CODE_REVIEW_SCHEMA``   — per-file code review issue list
- ``TASK_RESULT_SCHEMA``   — generic task execution result

Uses CLAUDE_CODE_OAUTH_TOKEN for auth (never ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from typing import Any

# ── Pre-built schemas ────────────────────────────────────────────────────────

VERDICT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["PASS", "NEEDS_REMEDIATION", "BLOCK"],
            "description": "Overall decision from the audit",
        },
        "severity": {
            "type": "string",
            "enum": ["none", "low", "medium", "high", "critical"],
            "description": "Worst-case severity of any finding",
        },
        "findings": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Individual findings or issues discovered",
        },
        "summary": {
            "type": "string",
            "description": "One-paragraph human-readable summary",
        },
    },
    "required": ["verdict", "severity", "findings", "summary"],
    "additionalProperties": False,
}

CODE_REVIEW_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "issues": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "Relative file path"},
                    "line": {
                        "type": "integer",
                        "description": "Line number (1-indexed), 0 if not applicable",
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["none", "low", "medium", "high", "critical"],
                    },
                    "message": {
                        "type": "string",
                        "description": "Description of the issue",
                    },
                },
                "required": ["file", "line", "severity", "message"],
                "additionalProperties": False,
            },
        },
        "summary": {
            "type": "string",
            "description": "Overall review summary",
        },
    },
    "required": ["issues", "summary"],
    "additionalProperties": False,
}

TASK_RESULT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["success", "partial", "failure"],
            "description": "Task completion status",
        },
        "output": {
            "type": "string",
            "description": "Primary output or result of the task",
        },
        "error": {
            "type": ["string", "null"],
            "description": "Error message if status is failure, otherwise null",
        },
        "duration_ms": {
            "type": "integer",
            "description": "Wall-clock execution time in milliseconds",
        },
    },
    "required": ["status", "output", "error", "duration_ms"],
    "additionalProperties": False,
}

# ── StructuredPrompt ─────────────────────────────────────────────────────────


@dataclass
class StructuredPrompt:
    """Declarative specification for a structured-output Claude invocation.

    Attributes:
        prompt: The user-facing instruction sent to Claude.
        output_schema: JSON Schema dict describing the required output shape.
        model: Claude model ID to use.  Defaults to ``claude-sonnet-4-6``.
    """

    prompt: str
    output_schema: dict[str, Any]
    model: str = "claude-sonnet-4-6"


# ── Validation ───────────────────────────────────────────────────────────────


def validate_output(output: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """Validate a parsed JSON object against a JSON Schema dict.

    This is a lightweight structural validator — it checks required fields,
    type constraints, and enum values without pulling in a full JSON Schema
    library.  For production use with complex schemas, wire in ``jsonschema``
    instead.

    Args:
        output: Parsed JSON object to validate.
        schema: JSON Schema dict (``"type": "object"`` at the root).

    Returns:
        List of validation error strings.  An empty list means the output
        is valid.
    """
    errors: list[str] = []

    if schema.get("type") != "object":
        # Only object-root schemas are supported by this validator.
        return errors

    required = schema.get("required", [])
    properties: dict[str, Any] = schema.get("properties", {})

    # Check required fields are present.
    for field_name in required:
        if field_name not in output:
            errors.append(f"Missing required field: '{field_name}'")

    # Validate present fields.
    for field_name, value in output.items():
        prop_schema = properties.get(field_name)
        if prop_schema is None:
            if schema.get("additionalProperties") is False:
                errors.append(f"Unexpected field: '{field_name}'")
            continue

        expected_type = prop_schema.get("type")
        enum_values = prop_schema.get("enum")

        if expected_type:
            # Handle nullable types like ["string", "null"]
            allowed_types = (
                expected_type if isinstance(expected_type, list) else [expected_type]
            )
            python_types = {
                "string": str,
                "integer": int,
                "number": (int, float),
                "boolean": bool,
                "array": list,
                "object": dict,
                "null": type(None),
            }
            valid_python = tuple(
                python_types[t] for t in allowed_types if t in python_types
            )
            if valid_python and not isinstance(value, valid_python):
                errors.append(
                    f"Field '{field_name}' has wrong type: "
                    f"expected {expected_type}, got {type(value).__name__}"
                )

        if enum_values is not None and value not in enum_values:
            errors.append(
                f"Field '{field_name}' value {value!r} not in enum {enum_values}"
            )

        # Recurse into array items if schema present.
        if expected_type == "array" and isinstance(value, list):
            item_schema = prop_schema.get("items", {})
            if item_schema:
                for idx, item in enumerate(value):
                    if isinstance(item, dict):
                        sub_errors = validate_output(item, item_schema)
                        for err in sub_errors:
                            errors.append(f"{field_name}[{idx}].{err}")

    return errors


# ── Core runner ──────────────────────────────────────────────────────────────

_SYSTEM_PROMPT_TEMPLATE = """\
You are a structured-output assistant.
Respond with a single JSON object that strictly conforms to the following JSON Schema.
Do not include markdown code fences, comments, or any text outside the JSON object.

JSON Schema:
{schema}
"""


def run_structured(
    prompt: str,
    schema: dict[str, Any],
    model: str = "claude-sonnet-4-6",
    timeout: int = 120,
) -> dict[str, Any]:
    """Call the Claude CLI and return a validated JSON object.

    The Claude Code CLI (``claude``) is invoked as a subprocess.  Auth is
    provided via the ``CLAUDE_CODE_OAUTH_TOKEN`` environment variable which
    the CLI picks up automatically.

    The system prompt instructs the model to produce only a JSON object
    matching ``schema``.  The raw stdout is parsed, validated, and returned.

    Args:
        prompt: User instruction describing what to produce.
        schema: JSON Schema dict for the expected output.
        model: Claude model ID.
        timeout: Subprocess timeout in seconds.

    Returns:
        Validated JSON object as a Python dict.

    Raises:
        RuntimeError: If the CLI is not found, returns a non-zero exit code,
            or if the output cannot be parsed or fails schema validation.
    """
    system_prompt = _SYSTEM_PROMPT_TEMPLATE.format(
        schema=json.dumps(schema, indent=2)
    )

    env = os.environ.copy()
    # Ensure the CLI can find its OAuth token.
    if "CLAUDE_CODE_OAUTH_TOKEN" not in env:
        raise RuntimeError(
            "CLAUDE_CODE_OAUTH_TOKEN is not set. "
            "Ensure the environment variable is exported before calling run_structured()."
        )

    cmd = [
        "claude",
        "--model", model,
        "--system", system_prompt,
        "--output-format", "text",
        "-p", prompt,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "claude CLI not found. Install Claude Code: "
            "https://code.claude.com/docs/en/get-started/quickstart"
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"claude CLI timed out after {timeout}s"
        ) from exc

    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise RuntimeError(
            f"claude CLI exited with code {result.returncode}: {stderr}"
        )

    raw = result.stdout.strip()
    parsed = _extract_json(raw)

    validation_errors = validate_output(parsed, schema)
    if validation_errors:
        raise RuntimeError(
            "Structured output failed schema validation:\n"
            + "\n".join(f"  - {e}" for e in validation_errors)
        )

    return parsed


def run_structured_prompt(sp: StructuredPrompt, timeout: int = 120) -> dict[str, Any]:
    """Convenience wrapper that accepts a ``StructuredPrompt`` dataclass.

    Args:
        sp: Fully-specified structured prompt.
        timeout: Subprocess timeout in seconds.

    Returns:
        Validated JSON object as a Python dict.
    """
    return run_structured(
        prompt=sp.prompt,
        schema=sp.output_schema,
        model=sp.model,
        timeout=timeout,
    )


# ── JSON extraction helper ───────────────────────────────────────────────────


def _extract_json(text: str) -> dict[str, Any]:
    """Extract a JSON object from model output text.

    The model is instructed to emit only bare JSON, but may occasionally wrap
    output in markdown fences.  This helper strips fences and parses the first
    complete ``{...}`` block found.

    Args:
        text: Raw CLI output text.

    Returns:
        Parsed Python dict.

    Raises:
        RuntimeError: If no valid JSON object can be found in ``text``.
    """
    # Strip markdown code fences if present.
    cleaned = text
    if "```" in cleaned:
        # Remove opening fence (```json or ```)
        cleaned = cleaned.split("```", 2)[-2] if cleaned.count("```") >= 2 else cleaned
        # Remove language tag if present on the first line
        lines = cleaned.splitlines()
        if lines and lines[0].strip() in ("json", ""):
            cleaned = "\n".join(lines[1:])
        # Remove closing fence
        cleaned = cleaned.rsplit("```", 1)[0]

    cleaned = cleaned.strip()

    # Find the outermost { ... } block.
    start = cleaned.find("{")
    if start == -1:
        raise RuntimeError(
            f"No JSON object found in model output. Raw output:\n{text[:500]}"
        )

    # Walk forward to find the matching closing brace.
    depth = 0
    end = -1
    for idx, char in enumerate(cleaned[start:], start=start):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end = idx + 1
                break

    if end == -1:
        raise RuntimeError(
            f"Unbalanced braces in model output. Raw output:\n{text[:500]}"
        )

    try:
        return json.loads(cleaned[start:end])
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Failed to parse JSON from model output: {exc}\n"
            f"Attempted to parse:\n{cleaned[start:end][:500]}"
        ) from exc
