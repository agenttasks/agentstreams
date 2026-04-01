"""Tests for convert-taxonomy.py — PDF conversion and section-tree handling."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

mod = import_module("convert-taxonomy")
convert_pdf = mod.convert_pdf
convert_section_tree = mod.convert_section_tree
convert_file = mod.convert_file
detect_format = mod.detect_format
is_pipeline_compatible = mod.is_pipeline_compatible


class TestConvertPdf:
    def test_converts_pdf_pages(self, tmp_path):
        """Test PDF conversion with mocked pymupdf."""
        pdf_path = tmp_path / "test.pdf"
        pdf_path.touch()

        # Create mock pages
        mock_page1 = MagicMock()
        mock_page1.get_text.return_value = "Page one content here"
        mock_page2 = MagicMock()
        mock_page2.get_text.return_value = "Page two content here"
        mock_page3 = MagicMock()
        mock_page3.get_text.return_value = ""  # empty page should be skipped

        mock_doc = MagicMock()
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_page1, mock_page2, mock_page3]))
        mock_doc.metadata = {"title": "Test Document"}
        mock_doc.close = MagicMock()

        mock_pymupdf = MagicMock()
        mock_pymupdf.open.return_value = mock_doc

        with patch.dict("sys.modules", {"pymupdf": mock_pymupdf}):
            result = convert_pdf(pdf_path)

        assert "page_count: 2" in result  # empty page skipped
        assert "### page-1" in result
        assert "### page-2" in result
        assert "Page one content here" in result
        assert "Page two content here" in result
        assert "# Test Document" in result
        assert "source: file://test.pdf" in result
        mock_doc.close.assert_called_once()

    def test_uses_filename_as_title_fallback(self, tmp_path):
        pdf_path = tmp_path / "my-document.pdf"
        pdf_path.touch()

        mock_page = MagicMock()
        mock_page.get_text.return_value = "Content"

        mock_doc = MagicMock()
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_page]))
        mock_doc.metadata = {}  # no title
        mock_doc.close = MagicMock()

        mock_pymupdf = MagicMock()
        mock_pymupdf.open.return_value = mock_doc

        with patch.dict("sys.modules", {"pymupdf": mock_pymupdf}):
            result = convert_pdf(pdf_path)

        assert "# my-document" in result

    def test_handles_empty_pdf(self, tmp_path):
        pdf_path = tmp_path / "empty.pdf"
        pdf_path.touch()

        mock_doc = MagicMock()
        mock_doc.__iter__ = MagicMock(return_value=iter([]))
        mock_doc.metadata = {"title": "Empty"}
        mock_doc.close = MagicMock()

        mock_pymupdf = MagicMock()
        mock_pymupdf.open.return_value = mock_doc

        with patch.dict("sys.modules", {"pymupdf": mock_pymupdf}):
            result = convert_pdf(pdf_path)

        assert "page_count: 0" in result

    def test_generates_valid_pipeline_format(self, tmp_path):
        pdf_path = tmp_path / "valid.pdf"
        pdf_path.touch()

        mock_page = MagicMock()
        mock_page.get_text.return_value = "Some text"

        mock_doc = MagicMock()
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_page]))
        mock_doc.metadata = {"title": "Valid"}
        mock_doc.close = MagicMock()

        mock_pymupdf = MagicMock()
        mock_pymupdf.open.return_value = mock_doc

        with patch.dict("sys.modules", {"pymupdf": mock_pymupdf}):
            result = convert_pdf(pdf_path)

        # Verify pipeline format
        assert result.startswith("---\n")
        assert "URL:" in result
        assert "Hash:" in result
        assert "```" in result
        # Should be detected as pipeline format
        assert is_pipeline_compatible(result)


class TestConvertSectionTree:
    def test_converts_section_headers(self, tmp_path):
        text = """## Introduction
Some intro text here.

## Methods
Description of methods.

## Results
The results are good.
"""
        result = convert_section_tree(text, tmp_path / "sections.md")
        assert "### introduction" in result
        assert "### methods" in result
        assert "### results" in result
        assert "page_count: 3" in result

    def test_delegates_to_chapter_tree(self, tmp_path):
        text = "## Section A\nContent A\n\n## Section B\nContent B\n"
        result = convert_section_tree(text, tmp_path / "test.md")
        assert "---" in result
        assert "## Pages" in result


class TestConvertFile:
    def test_returns_none_for_pipeline_format(self, tmp_path):
        f = tmp_path / "already.md"
        f.write_text("""---
source: test
domain: test.com
crawled_at: 2024-01-01
page_count: 1
---

## Pages

### test-page

URL: https://test.com/page
Hash: abc123

```
Content
```
""")
        result = convert_file(f)
        assert result is None

    def test_converts_plain_text_file(self, tmp_path):
        f = tmp_path / "plain.md"
        f.write_text("Just some plain text without any structure.")
        result = convert_file(f)
        assert result is not None
        assert "---" in result
        assert "page_count: 1" in result

    def test_converts_chapter_tree_file(self, tmp_path):
        f = tmp_path / "chapters.md"
        f.write_text("## Chapter 1: Intro\nContent here\n\n## Chapter 2: Body\nMore content\n")
        result = convert_file(f)
        assert result is not None
        assert "page_count: 2" in result

    def test_converts_pdf_file(self, tmp_path):
        f = tmp_path / "doc.pdf"
        f.touch()

        mock_page = MagicMock()
        mock_page.get_text.return_value = "PDF text"
        mock_doc = MagicMock()
        mock_doc.__iter__ = MagicMock(return_value=iter([mock_page]))
        mock_doc.metadata = {"title": "Doc"}
        mock_doc.close = MagicMock()
        mock_pymupdf = MagicMock()
        mock_pymupdf.open.return_value = mock_doc

        with patch.dict("sys.modules", {"pymupdf": mock_pymupdf}):
            result = convert_file(f)

        assert result is not None
        assert "PDF text" in result

    def test_converts_frontmatter_only(self, tmp_path):
        f = tmp_path / "frontmatter.md"
        f.write_text("---\ntitle: Test\n---\n\n## Section\nContent here.\n")
        result = convert_file(f)
        assert result is not None


class TestDetectFormatEdgeCases:
    def test_frontmatter_only(self):
        text = "---\ntitle: Test\n---\nBody text without proper sections."
        assert detect_format(text) == "frontmatter-only"

    def test_section_tree(self):
        text = "## Getting Started\nIntro\n\n## API Reference\nDocs\n"
        assert detect_format(text) == "section-tree"

    def test_empty_text(self):
        assert detect_format("") == "plain"

    def test_just_text(self):
        assert detect_format("Hello world, no headings.") == "plain"
