---
name: doc-coauthoring
description: Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.
---

# Doc Co-Authoring Workflow

## Overview

Structured guidance for collaborative document creation across three stages.

## Stage 1: Context Gathering

Ask meta-context questions:
1. Document type?
2. Primary audience?
3. Desired impact?
4. Required format or template?
5. Other constraints?

Then request comprehensive context dumps. Generate 5-10 clarifying questions based on gaps identified.

## Stage 2: Refinement & Structure

Build the document section-by-section through:
- Clarifying questions per section
- Brainstorming 5-20 options
- User curates selections
- Draft the section
- Iteratively refine via user feedback

Start with sections containing greatest unknowns.

## Stage 3: Reader Testing

Verify the document works for readers without author context.

**With sub-agent access:** Test directly by predicting reader questions and invoking fresh Claude instances.

**Without sub-agent access:** Provide instructions for manual testing in a new Claude conversation.

## Final Review

Request user's final read-through to verify facts, links, and intended impact.
