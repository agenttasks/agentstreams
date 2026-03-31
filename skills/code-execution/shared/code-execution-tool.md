# Code Execution Tool Reference

## Overview

The code execution tool lets Claude write and run Python or JavaScript code in an Anthropic-managed sandbox. No setup needed — it's built into the Messages API.

## Tool Definition

```json
{
  "type": "code_execution",
  "name": "code_execution"
}
```

No beta header required. Available on all Claude models.

## Capabilities

- **Languages**: Python 3.12, JavaScript (Node.js 20)
- **Libraries**: NumPy, pandas, matplotlib, scipy, sympy, Pillow, and standard libraries
- **File I/O**: Read/write files within the sandbox filesystem
- **Images**: Generate plots and images, returned as base64-encoded content blocks
- **Timeout**: 30 seconds default execution time
- **Memory**: 256MB per execution

## Response Format

Claude returns a `tool_use` block with the code, followed by a `tool_result` block with:

- `stdout` — standard output text
- `stderr` — error output
- `images` — generated images as base64 content blocks
- `files` — generated files

## Limitations

- No network access from sandbox
- No persistent storage between executions
- 30-second timeout per execution
- Limited to pre-installed libraries
- Cannot install additional packages

## Best Practices

1. **Let Claude choose the code** — don't pre-write code, let Claude generate it
2. **Iterate on errors** — if code fails, send the error back for Claude to fix
3. **Use for data analysis** — ideal for calculations, plotting, data transformation
4. **Combine with text** — Claude can explain results alongside code output
