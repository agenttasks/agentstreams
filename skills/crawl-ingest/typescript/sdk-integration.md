# TypeScript SDK v2 Integration

## Core SDK Patterns

### Streaming (recommended for crawl pipelines)

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

// Streaming extraction — prevents timeouts on large pages
const stream = client.messages.stream({
  model: 'claude-opus-4-6',
  max_tokens: 4096,
  thinking: { type: 'adaptive' },
  messages: [{ role: 'user', content: `Extract data from: ${pageContent}` }],
});

const response = await stream.finalMessage();
```

### Structured Outputs (for schema-enforced extraction)

```typescript
import { zodOutputFormat } from '@anthropic-ai/sdk/helpers/zod';
import { z } from 'zod';

const ProductSchema = z.object({
  name: z.string(),
  price: z.number(),
  currency: z.string(),
  description: z.string(),
  in_stock: z.boolean(),
});

const response = await client.messages.parse({
  model: 'claude-opus-4-6',
  max_tokens: 1024,
  output_format: zodOutputFormat(ProductSchema, 'product'),
  messages: [{ role: 'user', content: `Extract product info:\n${html}` }],
});

// response.output is typed as z.infer<typeof ProductSchema>
console.log(response.output.name, response.output.price);
```

### Batch API (50% discount for bulk extraction)

```typescript
const batch = await client.messages.batches.create({
  requests: pages.map((page, i) => ({
    custom_id: `page-${i}`,
    params: {
      model: 'claude-sonnet-4-6',
      max_tokens: 1024,
      messages: [{ role: 'user', content: `Extract: ${page.content}` }],
    },
  })),
});

// Poll for completion
let result = await client.messages.batches.retrieve(batch.id);
while (result.processing_status === 'in_progress') {
  await new Promise(r => setTimeout(r, 10000));
  result = await client.messages.batches.retrieve(batch.id);
}
```

### Tool Use (for multi-step extraction)

```typescript
import { betaZodTool } from '@anthropic-ai/sdk/helpers/zod';

const tools = [
  betaZodTool({
    name: 'save_product',
    description: 'Save an extracted product to the database',
    schema: ProductSchema,
    execute: async (input) => {
      await db.insert('products', input);
      return `Saved product: ${input.name}`;
    },
  }),
  betaZodTool({
    name: 'flag_for_review',
    description: 'Flag a page that needs manual review',
    schema: z.object({ url: z.string(), reason: z.string() }),
    execute: async (input) => {
      await db.insert('review_queue', input);
      return `Flagged: ${input.url}`;
    },
  }),
];

// Tool runner handles the loop automatically
const result = await client.beta.messages.runTools({
  model: 'claude-opus-4-6',
  max_tokens: 4096,
  tools,
  messages: [{ role: 'user', content: `Process this page and save data:\n${html}` }],
});
```

## Agent SDK Integration

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

// One-shot agent for complex crawl orchestration
const result = await query({
  prompt: `Crawl https://example.com, extract all product pages,
           and save structured data to ./data/products.json`,
  options: {
    model: 'claude-opus-4-6',
    permissionMode: 'acceptEdits',
    maxTurns: 50,
  },
});

for await (const message of result) {
  if (message.type === 'assistant') {
    console.log(message.content);
  }
}
```

## MCP Integration

```typescript
import { MCPBundle } from '@anthropic-ai/mcpb';

// Use MCP tools within crawl pipeline
// e.g., Neon Postgres for storage, Slack for notifications
```
