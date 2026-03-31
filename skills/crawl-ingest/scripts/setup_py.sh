#!/bin/bash
set -euo pipefail

echo "=== Setting up Python crawl-ingest project ==="

uv init crawl-project && cd crawl-project

# Core Anthropic
uv add anthropic claude-agent-sdk mcp

# Crawling
uv add scrapy scrapy-playwright

# Dedup
uv add pybloom-live bitarray mmh3

# Programmatic prompts
uv add dspy

# Dev tools
uv add --dev python-lsp-server pylsp-mypy python-lsp-ruff

# Install Playwright browsers
uv run playwright install chromium

# Create directory structure
mkdir -p data spiders

echo "=== Python setup complete ==="
echo "Run: uv run scrapy startproject crawl_project"
