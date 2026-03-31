# Python LSP Configuration

## Setup

```bash
uv add --dev python-lsp-server==1.14.0
uv add --dev pylsp-mypy==0.7.1        # Type checking
uv add --dev python-lsp-ruff==2.3.0   # Linting + formatting
```

## Programmatic LSP Usage

```python
import subprocess
import json

# Launch pylsp as subprocess
lsp = subprocess.Popen(
    ['pylsp'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

def send_lsp(method: str, params: dict, msg_id: int = 1):
    body = json.dumps({
        'jsonrpc': '2.0',
        'id': msg_id,
        'method': method,
        'params': params,
    })
    header = f'Content-Length: {len(body.encode())}\r\n\r\n'
    lsp.stdin.write((header + body).encode())
    lsp.stdin.flush()

# Initialize
send_lsp('initialize', {
    'processId': None,
    'rootUri': f'file:///path/to/project',
    'capabilities': {},
})
```

## Key LSP Capabilities

| Feature | Method | Plugin |
|---------|--------|--------|
| Completions | `textDocument/completion` | Built-in (jedi) |
| Diagnostics | `textDocument/publishDiagnostics` | pylsp-mypy, python-lsp-ruff |
| Go to definition | `textDocument/definition` | Built-in (jedi) |
| Find references | `textDocument/references` | Built-in (jedi) |
| Hover docs | `textDocument/hover` | Built-in (jedi) |
| Formatting | `textDocument/formatting` | python-lsp-ruff |
| Type checking | via diagnostics | pylsp-mypy |

## pylsp Configuration (pyproject.toml)

```toml
[tool.pylsp.plugins]
# Use ruff for linting (replaces pyflakes, pycodestyle, mccabe)
ruff.enabled = true
ruff.formatEnabled = true
pyflakes.enabled = false
pycodestyle.enabled = false
mccabe.enabled = false

# Type checking with mypy
pylsp_mypy.enabled = true
pylsp_mypy.live_mode = true

# Jedi for completions/definitions
jedi_completion.enabled = true
jedi_definition.enabled = true
jedi_hover.enabled = true
jedi_references.enabled = true
```
