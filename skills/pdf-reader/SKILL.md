---
name: pdf-reader
description: "Download and read PDFs with bloom filter deduplication and token-optimized extraction. TRIGGER when: user provides PDF URLs to read, asks to download and analyze PDF documents, needs to process system cards or whitepapers from URLs, or asks to batch-read multiple PDFs efficiently. DO NOT TRIGGER for: reading local files already on disk (use Read tool), general web scraping (use crawl-ingest), or image-only PDFs without text layer."
---

# PDF Reader: Bloom-Filtered PDF Download & Token-Optimized Reading

Download PDFs from URLs, deduplicate with bloom filters to avoid re-processing, extract text with PyMuPDF, and read specific page ranges via the Bash tool to minimize token usage and latency.

## Defaults

- Use `claude-opus-4-6` for PDF analysis and summarization
- Bloom filter deduplication enabled by default (FPP: 0.01, expected items: 1000)
- Extract to plaintext with page boundaries for selective reading
- Cache extracted text in `taxonomy/` for re-reads without re-downloading
- Default page chunk: 20 pages per read (keeps tokens under ~15K per chunk)

---

## Architecture

```
URL ──→ Bloom Check ──→ Download ──→ PyMuPDF Extract ──→ Page-Split Text ──→ Selective Read
          │                                                    │
          │ (seen before)                                      ▼
          ▼                                              taxonomy/<slug>.md
     Skip / Read Cache                                   (cached extraction)
```

### Token Budget Strategy

| PDF Size | Pages | Estimated Tokens | Strategy |
|----------|-------|------------------|----------|
| < 10 pages | 1-10 | ~5K-15K | Read all at once |
| 10-50 pages | 10-50 | ~15K-75K | Read in 20-page chunks |
| 50-200 pages | 50-200 | ~75K-300K | TOC scan first, then targeted pages |
| 200+ pages | 200+ | 300K+ | TOC scan → section index → targeted reads |

### Bloom Filter Integration

Uses `src/bloom.py` for URL deduplication:

```python
from src.bloom import BloomFilter

# Session-scoped filter tracks which PDFs have been downloaded
pdf_bloom = BloomFilter(expected_items=1000, fp_rate=0.01)

# Check before downloading
if pdf_bloom.is_new(url):
    download_and_extract(url)
else:
    # Read from cached taxonomy/ file
    read_cached(url)
```

The bloom filter prevents:
1. Re-downloading the same PDF in a session
2. Re-extracting text from already-processed PDFs
3. Wasting tokens on duplicate content across batch operations

---

## Workflow

### Phase 1: Download & Deduplicate

```bash
# Download PDF, skip if bloom filter says we've seen it
uv run scripts/pdf-read.py "https://example.com/document.pdf"

# Batch download with automatic deduplication
uv run scripts/pdf-read.py \
  "https://anthropic.com/system-cards" \
  "https://example.com/whitepaper.pdf" \
  "https://example.com/report.pdf"
```

### Phase 2: Selective Reading (Token-Optimized)

After extraction, the script outputs a taxonomy-format markdown file. Read specific page ranges using the Read tool with offset/limit:

```bash
# See the TOC / page index (first 50 lines = frontmatter + page list)
head -50 taxonomy/document.md

# Read specific pages (e.g., pages 5-10 of a large document)
# Each page section starts with ### page-N
grep -n "^### page-" taxonomy/document.md  # Find page boundaries
sed -n '120,250p' taxonomy/document.md     # Read lines 120-250 (pages 5-10)
```

### Phase 3: Analysis

With targeted page content loaded, analyze with Claude using minimal context:

1. Read TOC/index first (~500 tokens)
2. Identify relevant sections from TOC
3. Read only those sections (~2K-10K tokens per section)
4. Synthesize across sections

---

## Script: `scripts/pdf-read.py`

Core script handles download, bloom check, extraction, and caching. See `scripts/pdf-read.py` for implementation.

**CLI interface:**

```
Usage: uv run scripts/pdf-read.py [OPTIONS] URL [URL...]

Options:
  --pages RANGE    Only extract specific pages (e.g., "1-10", "5,10,15-20")
  --output DIR     Output directory (default: taxonomy/)
  --no-cache       Force re-download even if bloom filter has seen URL
  --toc            Print only the table of contents / page index
  --stats          Print token estimates per page
```

---

## Bash Tool Patterns for Efficient Reading

### Pattern 1: TOC-First Reading

```bash
# Step 1: Get page index (minimal tokens)
head -30 taxonomy/mythos-system-card.md

# Step 2: Find sections of interest
grep -n "^### " taxonomy/mythos-system-card.md | head -20

# Step 3: Read only the pages you need
sed -n '500,600p' taxonomy/mythos-system-card.md
```

### Pattern 2: Keyword-Targeted Reading

```bash
# Find pages containing specific terms
grep -n "calibration\|confidence\|overconfid" taxonomy/mythos-system-card.md

# Read surrounding context (±5 lines around each match)
grep -n -C5 "calibration" taxonomy/mythos-system-card.md
```

### Pattern 3: Section Extraction

```bash
# Extract a single page section (between ### markers)
awk '/^### page-42$/,/^### page-43$/' taxonomy/mythos-system-card.md
```

### Pattern 4: Token Estimation

```bash
# Estimate tokens before loading (rough: 1 token ≈ 4 chars)
wc -c taxonomy/mythos-system-card.md | awk '{printf "~%d tokens\n", $1/4}'

# Per-page token estimates
awk '/^### page-/{section=$0; chars=0; next} {chars+=length} /^### page-/{printf "%s: ~%d tokens\n", section, chars/4}' taxonomy/mythos-system-card.md
```

---

## Integration with Existing Tools

| Tool | Use For |
|------|---------|
| `src/bloom.py` | URL deduplication (BloomFilter class) |
| `scripts/convert-taxonomy.py` | Converts PDF → taxonomy format (existing) |
| `Read` tool | Reading cached taxonomy files with offset/limit |
| `Grep` tool | Finding keywords across cached PDFs |
| `Bash` tool | Running pdf-read.py, awk/sed for targeted extraction |
