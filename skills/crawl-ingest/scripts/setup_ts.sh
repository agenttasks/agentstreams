#!/bin/bash
set -euo pipefail

echo "=== Setting up TypeScript crawl-ingest project ==="

mkdir -p crawl-project && cd crawl-project
npm init -y
npx tsc --init

# Core Anthropic
npm install @anthropic-ai/sdk @anthropic-ai/claude-agent-sdk @anthropic-ai/tokenizer
npm install @modelcontextprotocol/sdk
npm install @anthropic-ai/mcpb @anthropic-ai/sandbox-runtime

# Cloud SDKs (optional)
npm install @anthropic-ai/bedrock-sdk @anthropic-ai/vertex-sdk @anthropic-ai/foundry-sdk

# Crawling
npm install crawlee playwright

# Dedup
npm install bloom-filters

# Programmatic prompts
npm install @ts-dspy/core

# Dev tools
npm install -D typescript-language-server typescript @types/node

# Create directory structure
mkdir -p src data

echo "=== TypeScript setup complete ==="
echo "Run: npx ts-node src/crawler.ts"
