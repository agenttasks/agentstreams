# TypeScript Stack Setup

## Installation

```bash
# Initialize project
mkdir context-window-project && cd context-window-project
npm init -y

# Core Anthropic packages
npm install @anthropic-ai/sdk

# Token estimation (local)
npm install @anthropic-ai/tokenizer   # Official tokenizer

# Testing
npm install --save-dev vitest
```

## Package Overview

| Package | Version | Purpose |
|---------|---------|---------|
| `@anthropic-ai/sdk` | 0.52.0 | Official TypeScript SDK — messages, token counting, caching |
| `@anthropic-ai/tokenizer` | 0.0.5 | Local token counting — exact counts without API call |

## Quick Start: Count Tokens

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const tokenCount = await client.messages.countTokens({
  model: "claude-sonnet-4-6",
  messages: [
    {
      role: "user",
      content: "Analyze this document: " + largeDocument,
    },
  ],
});

console.log(`Input tokens: ${tokenCount.input_tokens}`);
```

## Prompt Caching

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: "You are an expert analyst. Reference document: " + document,
      cache_control: { type: "ephemeral" },
    },
  ],
  messages: [
    { role: "user", content: "Summarize the key findings." },
  ],
});

console.log(`Cache creation: ${response.usage.cache_creation_input_tokens}`);
console.log(`Cache read: ${response.usage.cache_read_input_tokens}`);
```

## Long Document Chunking

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

function chunkDocument(
  text: string,
  maxTokens: number = 100_000,
  overlap: number = 5_000
): string[] {
  const charsPerToken = 4;
  const maxChars = maxTokens * charsPerToken;
  const overlapChars = overlap * charsPerToken;

  const chunks: string[] = [];
  let start = 0;
  while (start < text.length) {
    let end = start + maxChars;
    if (end < text.length) {
      const boundary = text.lastIndexOf(
        "\n\n",
        start + maxChars - overlapChars
      );
      if (boundary > start) end = boundary;
    }
    chunks.push(text.slice(start, end));
    start = end - overlapChars;
  }
  return chunks;
}

async function analyzeLongDocument(
  document: string,
  question: string
): Promise<string> {
  const chunks = chunkDocument(document);

  // Map phase
  const chunkResults = await Promise.all(
    chunks.map(async (chunk, i) => {
      const response = await client.messages.create({
        model: "claude-sonnet-4-6",
        max_tokens: 2048,
        messages: [
          {
            role: "user",
            content: `Chunk ${i + 1}/${chunks.length}:\n\n${chunk}\n\nQuestion: ${question}`,
          },
        ],
      });
      return response.content[0].type === "text"
        ? response.content[0].text
        : "";
    })
  );

  // Reduce phase
  const combined = chunkResults.join("\n\n---\n\n");
  const response = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: `Findings from ${chunks.length} chunks:\n\n${combined}\n\nSynthesize: ${question}`,
      },
    ],
  });

  return response.content[0].type === "text" ? response.content[0].text : "";
}
```

## Extended Thinking

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 16384,
  thinking: {
    type: "enabled",
    budget_tokens: 10000,
  },
  messages: [
    {
      role: "user",
      content: "Solve this complex optimization problem...",
    },
  ],
});

for (const block of response.content) {
  if (block.type === "thinking") {
    console.log("Thinking:", block.thinking);
  } else if (block.type === "text") {
    console.log("Response:", block.text);
  }
}
```

## MCP SDK Availability

TypeScript MCP SDK: `@modelcontextprotocol/sdk` (npm).

```bash
npm install @modelcontextprotocol/sdk
```
