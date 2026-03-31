# TypeScript Stack Setup

## Installation

```bash
# Initialize project
mkdir vision-project && cd vision-project
npm init -y

# Core Anthropic packages
npm install @anthropic-ai/sdk

# Image processing
npm install sharp                   # Image manipulation, resizing

# Testing
npm install --save-dev vitest
```

## Package Overview

| Package | Version | Purpose |
|---------|---------|---------|
| `@anthropic-ai/sdk` | 0.52.0 | Official TypeScript SDK — messages, vision, files API |
| `sharp` | 0.33.5 | Image manipulation — resize, crop, format conversion |

## Quick Start: Analyze a Single Image

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { readFileSync } from "fs";

const client = new Anthropic();

const imageData = readFileSync("screenshot.png").toString("base64");

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/png",
            data: imageData,
          },
        },
        {
          type: "text",
          text: "Describe what you see in this image.",
        },
      ],
    },
  ],
});

console.log(response.content[0].type === "text" ? response.content[0].text : "");
```

## Image from URL

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: {
            type: "url",
            url: "https://example.com/chart.png",
          },
        },
        {
          type: "text",
          text: "Extract all data points from this chart.",
        },
      ],
    },
  ],
});
```

## Multi-Image Comparison

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { readFileSync } from "fs";
import path from "path";

const client = new Anthropic();

function encodeImage(filePath: string) {
  const data = readFileSync(filePath).toString("base64");
  const ext = path.extname(filePath).slice(1);
  const mediaType = `image/${ext === "jpg" ? "jpeg" : ext}`;
  return {
    type: "image" as const,
    source: { type: "base64" as const, media_type: mediaType, data },
  };
}

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 2048,
  messages: [
    {
      role: "user",
      content: [
        encodeImage("before.png"),
        encodeImage("after.png"),
        { type: "text", text: "Compare these two screenshots. What changed?" },
      ],
    },
  ],
});
```

## Resize Images to Reduce Tokens

```typescript
import sharp from "sharp";

async function resizeForClaude(
  filePath: string,
  maxDim: number = 1024
): Promise<string> {
  const buffer = await sharp(filePath)
    .resize(maxDim, maxDim, { fit: "inside" })
    .png()
    .toBuffer();
  return buffer.toString("base64");
}
```

## MCP SDK Availability

TypeScript MCP SDK: `@modelcontextprotocol/sdk` (npm) — build MCP servers that provide vision tools.

```bash
npm install @modelcontextprotocol/sdk
```
