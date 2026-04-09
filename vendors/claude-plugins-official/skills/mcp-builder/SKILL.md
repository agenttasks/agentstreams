---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
license: Complete terms in LICENSE.txt
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools.

## High-Level Workflow

### Phase 1: Deep Research and Planning
- Understand Modern MCP Design (API coverage vs. workflow tools)
- Study MCP Protocol Documentation (modelcontextprotocol.io)
- Study Framework Documentation (TypeScript recommended)
- Plan Your Implementation

### Phase 2: Implementation
- Set Up Project Structure
- Implement Core Infrastructure (API client, error handling, pagination)
- Implement Tools (input schema, output schema, annotations)

### Phase 3: Review and Test
- Code Quality review (DRY, error handling, type coverage)
- Build and Test with MCP Inspector

### Phase 4: Create Evaluations
- Create 10 complex, realistic evaluation questions
- Output as XML qa_pair format

## Reference Files

- `reference/mcp_best_practices.md` - Core MCP guidelines
- `reference/node_mcp_server.md` - TypeScript patterns and examples
- `reference/python_mcp_server.md` - Python patterns and examples
- `reference/evaluation.md` - Evaluation creation guide

## Recommended Stack

- **Language**: TypeScript (high-quality SDK support)
- **Transport**: Streamable HTTP for remote, stdio for local
