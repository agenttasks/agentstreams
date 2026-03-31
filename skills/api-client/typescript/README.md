# TypeScript Stack Setup

## Installation

```bash
# Initialize project
npm init -y && npm pkg set type=module

# Core Anthropic packages
npm install anthropic
npm install @anthropic-ai/sdk

# HTTP Client
npm install axios@1.9

# OpenAPI Code Generation
npm install -D openapi-typescript@7.8

# Validation
npm install zod@3.24

# Rate Limiting
npm install bottleneck@2.19

# Testing
npm install -D vitest@3.1
npm install -D msw@2.7          # Mock Service Worker
```

## Package Overview

| Package | Version | Purpose |
|---------|---------|---------|
| `@anthropic-ai/sdk` | latest | Official TypeScript SDK — messages, streaming, tool use |
| `axios` | 1.9 | HTTP client with interceptors, retry, cancel |
| `openapi-typescript` | 7.8 | Generate TypeScript types from OpenAPI specs |
| `zod` | 3.24 | Runtime type validation and parsing |
| `bottleneck` | 2.19 | Rate limiter — token bucket, clustering |
| `vitest` | 3.1 | Testing framework — fast, ESM-native |
| `msw` | 2.7 | Mock Service Worker — intercept HTTP in tests |

## Quick Start: API Client with Claude + Retry + Validation

```typescript
import Anthropic from '@anthropic-ai/sdk';
import axios, { AxiosError } from 'axios';
import Bottleneck from 'bottleneck';
import { z } from 'zod';

// Initialize Anthropic client (reads CLAUDE_CODE_OAUTH_TOKEN from env)
const anthropic = new Anthropic();

// Rate limiter: 10 requests/second
const limiter = new Bottleneck({
  maxConcurrent: 5,
  minTime: 100, // 100ms between requests
});

// Response schema
const UserSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.string().email(),
  created_at: z.string().datetime(),
});

type User = z.infer<typeof UserSchema>;

// Retry with exponential backoff
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 1000,
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;
      if (error instanceof AxiosError) {
        const status = error.response?.status;
        if (status && ![408, 429, 500, 502, 503, 504].includes(status)) {
          throw error; // Non-retryable
        }
        // Respect Retry-After header
        const retryAfter = error.response?.headers['retry-after'];
        if (retryAfter) {
          await new Promise((r) => setTimeout(r, parseInt(retryAfter) * 1000));
          continue;
        }
      }
      const delay = baseDelay * 2 ** attempt + Math.random() * 1000;
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  throw new Error('Unreachable');
}

// API client
class ApiClient {
  constructor(
    private baseUrl: string,
    private apiKey: string,
  ) {}

  async getUser(id: number): Promise<User> {
    return withRetry(async () => {
      const response = await limiter.schedule(() =>
        axios.get(`${this.baseUrl}/users/${id}`, {
          headers: { Authorization: `Bearer ${this.apiKey}` },
          timeout: 30_000,
        }),
      );
      return UserSchema.parse(response.data);
    });
  }

  // Use Claude to explore an undocumented API
  async exploreEndpoint(url: string): Promise<string> {
    const response = await axios.get(url, {
      headers: { Authorization: `Bearer ${this.apiKey}` },
    });

    const result = await anthropic.messages.create({
      model: 'claude-sonnet-4-6',
      max_tokens: 2048,
      messages: [
        {
          role: 'user',
          content: `Analyze this API response and generate a TypeScript interface for it:\n\nURL: ${url}\nStatus: ${response.status}\nHeaders: ${JSON.stringify(response.headers)}\nBody: ${JSON.stringify(response.data, null, 2).slice(0, 10000)}`,
        },
      ],
    });

    return result.content[0].type === 'text' ? result.content[0].text : '';
  }
}

export { ApiClient, UserSchema, withRetry };
```

## Further Reading

- `shared/retry-patterns.md` — Retry strategy, circuit breaker, timeouts
- `shared/auth-patterns.md` — API key, OAuth 2.0, JWT, mTLS
- `shared/testing-patterns.md` — Mock strategies, contract testing, test pyramid
