# TypeScript Stack Setup

## Installation

```bash
npm init -y && npm pkg set type=module

# Core Anthropic
npm install @anthropic-ai/sdk

# Orchestration
npm install @temporalio/client @temporalio/worker @temporalio/workflow @temporalio/activity

# Data Processing
npm install csv-parse csv-stringify
npm install parquet-wasm          # Parquet read/write via WASM

# Streaming
npm install kafkajs@2.2

# Validation
npm install zod@3.24

# Testing
npm install -D vitest@3.1
```

## Package Overview

| Package | Version | Purpose |
|---------|---------|---------|
| `@anthropic-ai/sdk` | latest | Official TypeScript SDK |
| `@temporalio/*` | 1.11 | Workflow orchestration — durable execution, retry |
| `kafkajs` | 2.2 | Kafka client — producer, consumer, admin |
| `csv-parse` | 5.6 | CSV parsing with streaming support |
| `parquet-wasm` | 0.7 | Parquet read/write via WebAssembly |
| `zod` | 3.24 | Schema validation |

## Quick Start: Temporal + Claude Pipeline

```typescript
import Anthropic from '@anthropic-ai/sdk';
import { createReadStream } from 'fs';
import { parse } from 'csv-parse';
import { z } from 'zod';

const anthropic = new Anthropic();

// Schema
const RecordSchema = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string(),
  category: z.string().optional(),
});

type Record = z.infer<typeof RecordSchema>;

// Pipeline stages
async function extract(sourcePath: string): Promise<Record[]> {
  const records: Record[] = [];
  const parser = createReadStream(sourcePath).pipe(
    parse({ columns: true, trim: true }),
  );
  for await (const row of parser) {
    records.push(RecordSchema.parse(row));
  }
  return records;
}

async function transform(records: Record[]): Promise<Record[]> {
  return records
    .filter((r) => r.id && r.name)
    .map((r) => ({
      ...r,
      name: r.name.trim(),
    }));
}

async function enrichWithClaude(records: Record[]): Promise<Record[]> {
  const batchSize = 50;
  const enriched: Record[] = [];

  for (let i = 0; i < records.length; i += batchSize) {
    const batch = records.slice(i, i + batchSize);
    const descriptions = batch.map((r) => r.description).join('\n');

    const result = await anthropic.messages.create({
      model: 'claude-sonnet-4-6',
      max_tokens: 2048,
      messages: [
        {
          role: 'user',
          content: `Classify each item. Return one category per line:\n\n${descriptions}`,
        },
      ],
    });

    const categories =
      result.content[0].type === 'text'
        ? result.content[0].text.trim().split('\n')
        : [];

    batch.forEach((r, idx) => {
      enriched.push({ ...r, category: categories[idx] ?? 'unknown' });
    });
  }

  return enriched;
}

function qualityCheck(records: Record[]): void {
  if (records.length === 0) throw new Error('No records');
  const ids = new Set(records.map((r) => r.id));
  if (ids.size !== records.length) throw new Error('Duplicate IDs');
}

// Run pipeline
async function run(source: string, target: string) {
  const raw = await extract(source);
  const clean = await transform(raw);
  const enriched = await enrichWithClaude(clean);
  qualityCheck(enriched);
  // Load to target...
  console.log(`Processed ${enriched.length} records`);
}

export { extract, transform, enrichWithClaude, qualityCheck, run };
```

## Further Reading

- `shared/pipeline-patterns.md` — Idempotency, backpressure, DLQ, data quality
- `shared/orchestration.md` — DAGs, scheduling, Temporal/Prefect patterns
