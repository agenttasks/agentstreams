# Long Document Processing Reference

## Overview

When a document exceeds the context window (200K tokens ≈ 800K characters), split it into chunks and use map-reduce or sequential processing.

## Chunking Strategies

### Semantic Chunking (Recommended)

Split at natural boundaries:
- Paragraph breaks (`\n\n`)
- Section headings (`# `, `## `)
- Page breaks
- Function/class boundaries (for code)

### Fixed-Size Chunking

Split at fixed token counts with overlap:
- Chunk size: 80-100K tokens
- Overlap: 5-10K tokens (prevents missing context at boundaries)

### Hierarchical Chunking

For very large documents (1M+ characters):
1. Split into major sections
2. Process each section independently
3. Combine section summaries
4. Final synthesis pass

## Processing Patterns

### Map-Reduce

Best for: questions that can be answered from individual chunks

1. **Map**: Send each chunk with the same question
2. **Reduce**: Combine chunk answers into final response

### Sequential (Chain)

Best for: tasks requiring document-order awareness

1. Process chunk 1, save summary
2. Process chunk 2 with previous summary as context
3. Continue until all chunks processed

### Hierarchical

Best for: very large documents (books, codebases)

1. Split into sections → summarize each
2. Group section summaries → synthesize
3. Final answer from top-level synthesis

## Token Budget Planning

For a 200K context window with a long document:

```
System prompt:     ~2K tokens
Tool definitions:  ~3K tokens
Document chunk:    ~150K tokens (max)
Output reserve:    ~16K tokens
Overhead:          ~5K tokens
Available:         ~174K tokens for content
```
