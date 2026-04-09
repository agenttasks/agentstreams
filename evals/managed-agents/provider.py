"""Custom promptfoo provider using anthropic SDK with CLAUDE_CODE_OAUTH_TOKEN.

Never use ANTHROPIC_API_KEY — all auth flows through CLAUDE_CODE_OAUTH_TOKEN.
"""

import os


def call_api(prompt, options, context):
    """promptfoo custom provider entry point."""
    try:
        import anthropic
    except ImportError:
        return {"error": "anthropic package not installed. Run: pip install anthropic"}

    config = options.get("config", {})
    model = config.get("model", "claude-sonnet-4-6")
    max_tokens = config.get("max_tokens", 1024)
    temperature = config.get("temperature", 0)

    # Auth flows through CLAUDE_CODE_OAUTH_TOKEN (never use ANTHROPIC_API_KEY).
    api_key = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "")
    if not api_key:
        return {"error": "No API key found. Set CLAUDE_CODE_OAUTH_TOKEN."}

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        output = response.content[0].text
        token_usage = {
            "total": response.usage.input_tokens + response.usage.output_tokens,
            "prompt": response.usage.input_tokens,
            "completion": response.usage.output_tokens,
        }
        return {"output": output, "tokenUsage": token_usage}
    except anthropic.AuthenticationError:
        return {"error": "Authentication failed. Check CLAUDE_CODE_OAUTH_TOKEN."}
    except Exception as e:
        return {"error": str(e)}
