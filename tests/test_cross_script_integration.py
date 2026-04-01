"""Cross-script data flow integration tests.

Verifies that output from one script is valid input for the next:
  crawl-sitemap output -> extract-patterns input -> validate-patterns input
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

crawl_mod = import_module("crawl-sitemap")
extract_mod = import_module("extract-patterns")
convert_mod = import_module("convert-taxonomy")

write_taxonomy = crawl_mod.write_taxonomy
parse_taxonomy_pages = extract_mod.parse_taxonomy_pages
classify_page_type = extract_mod.classify_page_type
extract_topics = extract_mod.extract_topics
detect_code_languages = extract_mod.detect_code_languages
is_pipeline_compatible = convert_mod.is_pipeline_compatible
detect_format = convert_mod.detect_format


class TestCrawlToExtractFlow:
    def test_crawl_output_is_parseable_by_extract(self, tmp_path):
        """write_taxonomy output should be parseable by parse_taxonomy_pages."""
        results = [
            {
                "url": "https://docs.example.com/en/tool-use",
                "content": "# Tool Use\nClaude supports function calling via the tool_use API.\n"
                "Use `claude-sonnet-4-6` for best results.\n"
                "```python\nclient.messages.create(model='claude-sonnet-4-6')\n```",
                "hash": "abc123def456",
                "error": None,
            },
            {
                "url": "https://docs.example.com/en/agents",
                "content": "# Agents\nBuild autonomous agents with Claude.\n"
                "Agents can use tools, make decisions, and complete tasks.",
                "hash": "def456ghi789",
                "error": None,
            },
        ]
        output = str(tmp_path / "taxonomy.md")
        write_taxonomy(results, output, "https://docs.example.com/sitemap.xml", "docs.example.com")

        # Read and parse with extract-patterns
        taxonomy_text = Path(output).read_text()
        pages = parse_taxonomy_pages(taxonomy_text)

        assert len(pages) == 2
        # Verify page structure has required fields
        for page in pages:
            assert "url" in page
            assert "content" in page

    def test_crawl_output_is_pipeline_compatible(self, tmp_path):
        """write_taxonomy output should be detected as pipeline format."""
        results = [
            {
                "url": "https://example.com/page",
                "content": "Page content",
                "hash": "abcdef123456",
                "error": None,
            },
        ]
        output = str(tmp_path / "out.md")
        write_taxonomy(results, output, "https://example.com/sitemap.xml", "example.com")

        text = Path(output).read_text()
        assert detect_format(text) == "pipeline"
        assert is_pipeline_compatible(text)


class TestExtractPatternsOutput:
    def test_classify_page_type_for_api_docs(self):
        content = "# API Reference\nEndpoint: POST /v1/messages\nParameters: model, max_tokens"
        page_type = classify_page_type("https://docs.example.com/en/api-reference", content)
        assert page_type in ("api-reference", "guide", "reference")

    def test_extract_topics_from_content(self):
        content = "Claude supports tool use, function calling, and agent workflows."
        topics = extract_topics(content)
        assert isinstance(topics, list)

    def test_detect_code_languages(self):
        content = """```python
import anthropic
client = anthropic.Anthropic()
```

```typescript
import Anthropic from '@anthropic-ai/sdk';
const client = new Anthropic();
```"""
        langs = detect_code_languages(content)
        assert "python" in langs or "Python" in langs


class TestConvertToExtractFlow:
    def test_converted_plain_text_is_parseable(self, tmp_path):
        """convert-taxonomy plain output should be parseable by extract-patterns."""
        f = tmp_path / "plain.md"
        f.write_text("This is a guide about building agents with Claude SDK.")

        convert_plain = convert_mod.convert_plain
        converted = convert_plain(f.read_text(), f)

        pages = parse_taxonomy_pages(converted)
        assert len(pages) >= 1
        assert pages[0]["content"].strip() != ""

    def test_converted_chapter_tree_is_parseable(self, tmp_path):
        """convert-taxonomy chapter-tree output should parse into multiple pages."""
        f = tmp_path / "chapters.md"
        f.write_text(
            "## Chapter 1: Setup\n"
            "Install the SDK with pip install anthropic.\n\n"
            "## Chapter 2: Usage\n"
            "Create a client and send messages.\n"
        )

        convert_chapter = convert_mod.convert_chapter_tree
        converted = convert_chapter(f.read_text(), f)

        pages = parse_taxonomy_pages(converted)
        assert len(pages) == 2

        # Each page should have URL and content
        for page in pages:
            assert page["url"].startswith("https://")
            assert len(page["content"]) > 0


class TestErrorPropagation:
    def test_crawl_errors_dont_break_extract(self, tmp_path):
        """Taxonomy with error entries should still be parseable."""
        results = [
            {
                "url": "https://example.com/ok",
                "content": "Good content",
                "hash": "aaa111bbb222",
                "error": None,
            },
            {
                "url": "https://example.com/fail",
                "content": None,
                "hash": None,
                "error": "404 Not Found",
            },
        ]
        output = str(tmp_path / "mixed.md")
        write_taxonomy(results, output, "https://example.com/sitemap.xml", "example.com")

        text = Path(output).read_text()
        pages = parse_taxonomy_pages(text)

        # Only successful pages should appear as parseable pages
        assert len(pages) >= 1
        # Error section exists in the file but shouldn't produce pages
        assert "404" in text
