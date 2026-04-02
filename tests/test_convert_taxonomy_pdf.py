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


def _mock_pdf(page_texts, title=None):
    """Build a mock pymupdf module that returns pages with given texts."""
    pages = []
    for text in page_texts:
        page = MagicMock()
        page.get_text.return_value = text
        pages.append(page)
    doc = MagicMock()
    doc.__iter__ = MagicMock(return_value=iter(pages))
    doc.metadata = {"title": title} if title else {}
    doc.close = MagicMock()
    pymupdf = MagicMock()
    pymupdf.open.return_value = doc
    return pymupdf, doc


class TestConvertPdf:
    def test_converts_pdf_pages(self, tmp_path):
        pdf_path = tmp_path / "test.pdf"
        pdf_path.touch()
        mock_pymupdf, mock_doc = _mock_pdf(
            ["Page one content here", "Page two content here", ""], title="Test Document"
        )
        with patch.dict("sys.modules", {"pymupdf": mock_pymupdf}):
            result = convert_pdf(pdf_path)
        assert "page_count: 2" in result
        assert "### page-1" in result
        assert "Page one content here" in result
        assert "# Test Document" in result
        mock_doc.close.assert_called_once()

    def test_uses_filename_as_title_fallback(self, tmp_path):
        pdf_path = tmp_path / "my-document.pdf"
        pdf_path.touch()
        mock_pymupdf, _ = _mock_pdf(["Content"])
        with patch.dict("sys.modules", {"pymupdf": mock_pymupdf}):
            result = convert_pdf(pdf_path)
        assert "# my-document" in result

    def test_handles_empty_pdf(self, tmp_path):
        pdf_path = tmp_path / "empty.pdf"
        pdf_path.touch()
        mock_pymupdf, _ = _mock_pdf([], title="Empty")
        with patch.dict("sys.modules", {"pymupdf": mock_pymupdf}):
            result = convert_pdf(pdf_path)
        assert "page_count: 0" in result

    def test_generates_valid_pipeline_format(self, tmp_path):
        pdf_path = tmp_path / "valid.pdf"
        pdf_path.touch()
        mock_pymupdf, _ = _mock_pdf(["Some text"], title="Valid")
        with patch.dict("sys.modules", {"pymupdf": mock_pymupdf}):
            result = convert_pdf(pdf_path)
        assert result.startswith("---\n")
        assert "URL:" in result
        assert is_pipeline_compatible(result)


class TestConvertSectionTree:
    def test_converts_section_headers(self, tmp_path):
        text = "## Introduction\nIntro.\n\n## Methods\nMethods.\n\n## Results\nResults.\n"
        result = convert_section_tree(text, tmp_path / "sections.md")
        assert "### introduction" in result
        assert "### methods" in result
        assert "page_count: 3" in result

    def test_delegates_to_chapter_tree(self, tmp_path):
        result = convert_section_tree("## A\nContent A\n\n## B\nContent B\n", tmp_path / "t.md")
        assert "---" in result
        assert "## Pages" in result


class TestConvertFilePdf:
    def test_returns_none_for_pipeline_format(self, tmp_path):
        f = tmp_path / "already.md"
        f.write_text(
            "---\nsource: t\ndomain: t.com\ncrawled_at: x\npage_count: 1\n---\n\n"
            "## Pages\n\n### p\n\nURL: https://t.com/p\nHash: abc\n\n```\nC\n```\n"
        )
        assert convert_file(f) is None

    def test_converts_plain_text_file(self, tmp_path):
        f = tmp_path / "plain.md"
        f.write_text("Just some plain text without any structure.")
        result = convert_file(f)
        assert result is not None
        assert "page_count: 1" in result

    def test_converts_pdf_file(self, tmp_path):
        f = tmp_path / "doc.pdf"
        f.touch()
        mock_pymupdf, _ = _mock_pdf(["PDF text"], title="Doc")
        with patch.dict("sys.modules", {"pymupdf": mock_pymupdf}):
            result = convert_file(f)
        assert "PDF text" in result

    def test_converts_frontmatter_only(self, tmp_path):
        f = tmp_path / "frontmatter.md"
        f.write_text("---\ntitle: Test\n---\n\n## Section\nContent here.\n")
        assert convert_file(f) is not None


class TestDetectFormatEdgeCases:
    def test_frontmatter_only(self):
        assert detect_format("---\ntitle: Test\n---\nBody.") == "frontmatter-only"

    def test_section_tree(self):
        assert detect_format("## Getting Started\nIntro\n\n## API\nDocs\n") == "section-tree"

    def test_empty_text(self):
        assert detect_format("") == "plain"

    def test_just_text(self):
        assert detect_format("Hello world, no headings.") == "plain"
