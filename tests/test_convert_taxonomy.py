"""Tests for scripts/convert-taxonomy.py — taxonomy format converter."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

mod = import_module("convert-taxonomy")
detect_format = mod.detect_format
convert_chapter_tree = mod.convert_chapter_tree
convert_plain = mod.convert_plain
convert_file = mod.convert_file
is_pipeline_compatible = mod.is_pipeline_compatible
slugify = mod.slugify
content_hash = mod.content_hash
extract_source_info = mod.extract_source_info

# Also import extract-patterns to verify compatibility
extract_mod = import_module("extract-patterns")
parse_taxonomy_pages = extract_mod.parse_taxonomy_pages


CHAPTER_TREE_INPUT = """# Test Book -- Taxonomy Tree (Chapters 1-2)

Source: Author. *Test Book*, 1st Edition (Publisher, 2024).

---

## Chapter 1: Introduction (pp. 1-20)

```
Chapter 1: Introduction
├── Overview
│   ├── Key concept A
│   └── Key concept B
├── Background
│   ├── Historical context
│   └── Modern approach
```

## Chapter 2: Methods (pp. 21-40)

```
Chapter 2: Methods
├── Quantitative
│   ├── Surveys
│   └── Experiments
├── Qualitative
│   ├── Interviews
│   └── Observations
```
"""

PIPELINE_FORMAT = """---
source: https://example.com/docs
domain: example.com
crawled_at: 2026-01-01T00:00:00Z
index_hash: abc123
page_count: 1
---

# Example

## Pages

### intro

URL: https://example.com/docs/intro
Hash: def456

```
Introduction content here.
```
"""

PLAIN_INPUT = """Just some plain text content.

No headings, no structure, no frontmatter.
This should be wrapped as a single page.
"""


class TestDetectFormat:
    def test_detects_pipeline_format(self):
        assert detect_format(PIPELINE_FORMAT) == "pipeline"

    def test_detects_chapter_tree(self):
        assert detect_format(CHAPTER_TREE_INPUT) == "chapter-tree"

    def test_detects_plain(self):
        assert detect_format(PLAIN_INPUT) == "plain"

    def test_detects_frontmatter_only(self):
        text = "---\nsource: test\n---\n\n# Title\n\nContent"
        assert detect_format(text) == "frontmatter-only"

    def test_detects_section_tree(self):
        text = "# Title\n\n## Section 1\n\nContent\n\n## Section 2\n\nMore content"
        assert detect_format(text) == "section-tree"


class TestSlugify:
    def test_basic(self):
        assert slugify("Hello World") == "hello-world"

    def test_special_chars(self):
        assert slugify("Chapter 1: Introduction (pp. 1-20)") == "chapter-1-introduction-pp-1-20"

    def test_max_length(self):
        result = slugify("A" * 100)
        assert len(result) <= 60

    def test_strips_leading_trailing_hyphens(self):
        assert slugify("--hello--") == "hello"


class TestContentHash:
    def test_deterministic(self):
        assert content_hash("hello") == content_hash("hello")

    def test_different_inputs(self):
        assert content_hash("hello") != content_hash("world")

    def test_length(self):
        assert len(content_hash("test")) == 12


class TestExtractSourceInfo:
    def test_extracts_source_line(self):
        text = "Source: Author. *Book*, 1st Ed.\n\nContent"
        info = extract_source_info(text, Path("test.md"))
        assert "Author" in info["source"]

    def test_extracts_title(self):
        text = "# My Great Title\n\nContent"
        info = extract_source_info(text, Path("test.md"))
        assert info["title"] == "My Great Title"

    def test_defaults_to_filename(self):
        info = extract_source_info("no title here", Path("myfile.md"))
        assert info["title"] == "myfile"


class TestConvertChapterTree:
    def test_produces_pipeline_format(self):
        result = convert_chapter_tree(CHAPTER_TREE_INPUT, Path("test-book.md"))
        assert result.startswith("---\n")
        assert "source:" in result
        assert "domain:" in result
        assert "page_count: 2" in result

    def test_creates_page_sections(self):
        result = convert_chapter_tree(CHAPTER_TREE_INPUT, Path("test-book.md"))
        assert "### chapter-1" in result
        assert "### chapter-2" in result

    def test_includes_urls(self):
        result = convert_chapter_tree(CHAPTER_TREE_INPUT, Path("test-book.md"))
        assert "URL: https://local.taxonomy/" in result

    def test_includes_content_in_fences(self):
        result = convert_chapter_tree(CHAPTER_TREE_INPUT, Path("test-book.md"))
        assert "├── Overview" in result

    def test_parseable_by_extract_patterns(self):
        result = convert_chapter_tree(CHAPTER_TREE_INPUT, Path("test-book.md"))
        pages = parse_taxonomy_pages(result)
        assert len(pages) == 2
        assert all(p["url"].startswith("https://") for p in pages)


class TestConvertPlain:
    def test_wraps_as_single_page(self):
        result = convert_plain(PLAIN_INPUT, Path("notes.md"))
        assert "page_count: 1" in result

    def test_parseable_by_extract_patterns(self):
        result = convert_plain(PLAIN_INPUT, Path("notes.md"))
        pages = parse_taxonomy_pages(result)
        assert len(pages) == 1


class TestConvertFile:
    def test_returns_none_for_compatible(self, tmp_path):
        p = tmp_path / "test.md"
        p.write_text(PIPELINE_FORMAT)
        assert convert_file(p) is None

    def test_converts_chapter_tree(self, tmp_path):
        p = tmp_path / "test.md"
        p.write_text(CHAPTER_TREE_INPUT)
        result = convert_file(p)
        assert result is not None
        assert "### chapter-1" in result

    def test_converts_plain(self, tmp_path):
        p = tmp_path / "test.md"
        p.write_text(PLAIN_INPUT)
        result = convert_file(p)
        assert result is not None
        assert "page_count: 1" in result


class TestIsPipelineCompatible:
    def test_compatible_file(self):
        assert is_pipeline_compatible(PIPELINE_FORMAT)

    def test_incompatible_file(self):
        assert not is_pipeline_compatible(CHAPTER_TREE_INPUT)

    def test_incompatible_plain(self):
        assert not is_pipeline_compatible(PLAIN_INPUT)


class TestRealFixtures:
    """Test against actual taxonomy fixtures if available."""

    def test_converted_kimball_parseable(self):
        """Verify converted kimball files are parseable by extract-patterns."""
        kimball = Path("taxonomy/kimball-ch01-02.md")
        if not kimball.exists():
            return  # skip if not present

        text = kimball.read_text()
        if not is_pipeline_compatible(text):
            return  # skip if not yet converted

        pages = parse_taxonomy_pages(text)
        assert len(pages) >= 1
        assert all(p["url"].startswith("https://") for p in pages)
