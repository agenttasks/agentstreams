# TypeScript LSP Configuration

## Setup

```bash
# Install the TypeScript language server
npm install -D typescript-language-server@5.1.3 typescript@5.x

# For Node.js LSP features
npm install -D @types/node
```

## Programmatic LSP Usage

Spawn the language server as a child process and communicate via JSON-RPC:

```typescript
import { spawn } from 'child_process';

const lsp = spawn('npx', ['typescript-language-server', '--stdio'], {
  stdio: ['pipe', 'pipe', 'pipe'],
});

// Send initialize request
const initRequest = {
  jsonrpc: '2.0',
  id: 1,
  method: 'initialize',
  params: {
    processId: process.pid,
    rootUri: `file://${process.cwd()}`,
    capabilities: {},
  },
};

function sendRequest(req: object) {
  const body = JSON.stringify(req);
  const header = `Content-Length: ${Buffer.byteLength(body)}\r\n\r\n`;
  lsp.stdin.write(header + body);
}

sendRequest(initRequest);

// Parse responses from stdout
let buffer = '';
lsp.stdout.on('data', (data) => {
  buffer += data.toString();
  // Parse JSON-RPC messages from buffer
  const match = buffer.match(/Content-Length: (\d+)\r\n\r\n/);
  if (match) {
    const len = parseInt(match[1]);
    const start = match[0].length;
    if (buffer.length >= start + len) {
      const json = JSON.parse(buffer.slice(start, start + len));
      console.log('LSP response:', json);
      buffer = buffer.slice(start + len);
    }
  }
});
```

## Key LSP Capabilities for Crawl Projects

| Feature | Method | Use Case |
|---------|--------|----------|
| **Go to definition** | `textDocument/definition` | Navigate crawler/extractor code |
| **Find references** | `textDocument/references` | Track where extracted fields are used |
| **Completions** | `textDocument/completion` | SDK method autocomplete |
| **Diagnostics** | `textDocument/publishDiagnostics` | Type errors in extraction schemas |
| **Hover** | `textDocument/hover` | Quick docs for Crawlee/SDK APIs |

## tsconfig.json for Crawl Projects

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "resolveJsonModule": true,
    "declaration": true,
    "sourceMap": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "data", "dist"]
}
```
