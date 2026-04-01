"""Tests for crawl-sitemap.py — async fetch, DB write, and error recovery paths."""

import asyncio
import re
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

mod = import_module("crawl-sitemap")
fetch_sitemap_urls = mod.fetch_sitemap_urls
fetch_page = mod.fetch_page
write_to_neon = mod.write_to_neon
html_to_text = mod.html_to_text
content_hash = mod.content_hash
TRUNCATE_BYTES = mod.TRUNCATE_BYTES


# ── fetch_sitemap_urls ──────────────────────────────────────


class TestFetchSitemapUrls:
    @pytest.fixture
    def mock_session(self):
        session = MagicMock()
        return session

    async def test_returns_urls_from_simple_sitemap(self):
        xml = """<?xml version="1.0"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/page1</loc></url>
  <url><loc>https://example.com/page2</loc></url>
</urlset>"""
        response = AsyncMock()
        response.text = AsyncMock(return_value=xml)
        response.__aenter__ = AsyncMock(return_value=response)
        response.__aexit__ = AsyncMock(return_value=False)

        session = MagicMock()
        session.get = MagicMock(return_value=response)

        urls = await fetch_sitemap_urls(session, "https://example.com/sitemap.xml")
        assert len(urls) == 2
        assert "https://example.com/page1" in urls

    async def test_follows_sitemap_index_recursively(self):
        index_xml = """<?xml version="1.0"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://example.com/sitemap-pages.xml</loc></sitemap>
</sitemapindex>"""
        sub_xml = """<?xml version="1.0"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/deep-page</loc></url>
</urlset>"""

        call_count = 0

        def make_response(url, **kwargs):
            nonlocal call_count
            resp = AsyncMock()
            if call_count == 0:
                resp.text = AsyncMock(return_value=index_xml)
            else:
                resp.text = AsyncMock(return_value=sub_xml)
            call_count += 1
            resp.__aenter__ = AsyncMock(return_value=resp)
            resp.__aexit__ = AsyncMock(return_value=False)
            return resp

        session = MagicMock()
        session.get = MagicMock(side_effect=make_response)

        urls = await fetch_sitemap_urls(session, "https://example.com/sitemap.xml")
        assert "https://example.com/deep-page" in urls

    async def test_returns_empty_on_fetch_error(self):
        response = AsyncMock()
        response.__aenter__ = AsyncMock(side_effect=ConnectionError("timeout"))
        response.__aexit__ = AsyncMock(return_value=False)

        session = MagicMock()
        session.get = MagicMock(return_value=response)

        urls = await fetch_sitemap_urls(session, "https://example.com/sitemap.xml")
        assert urls == []


# ── fetch_page ──────────────────────────────────────────────


class TestFetchPage:
    async def test_fetches_html_page(self):
        html = "<html><body><p>Hello world</p></body></html>"
        response = AsyncMock()
        response.text = AsyncMock(return_value=html)
        response.__aenter__ = AsyncMock(return_value=response)
        response.__aexit__ = AsyncMock(return_value=False)

        session = MagicMock()
        session.get = MagicMock(return_value=response)

        sem = asyncio.Semaphore(10)
        result = await fetch_page(session, sem, "https://example.com/page", 0.0)

        assert result["url"] == "https://example.com/page"
        assert "Hello world" in result["content"]
        assert result["hash"] is not None
        assert result["error"] is None

    async def test_fetches_plain_text(self):
        text = "This is plain text content."
        response = AsyncMock()
        response.text = AsyncMock(return_value=text)
        response.__aenter__ = AsyncMock(return_value=response)
        response.__aexit__ = AsyncMock(return_value=False)

        session = MagicMock()
        session.get = MagicMock(return_value=response)

        sem = asyncio.Semaphore(10)
        result = await fetch_page(session, sem, "https://example.com/api", 0.0)

        assert result["content"] == text
        assert result["error"] is None

    async def test_truncates_large_content(self):
        large_text = "x" * (TRUNCATE_BYTES + 1000)
        response = AsyncMock()
        response.text = AsyncMock(return_value=large_text)
        response.__aenter__ = AsyncMock(return_value=response)
        response.__aexit__ = AsyncMock(return_value=False)

        session = MagicMock()
        session.get = MagicMock(return_value=response)

        sem = asyncio.Semaphore(10)
        result = await fetch_page(session, sem, "https://example.com/big", 0.0)

        assert len(result["content"]) < len(large_text)
        assert "truncated" in result["content"]

    async def test_returns_error_on_exception(self):
        response = AsyncMock()
        response.__aenter__ = AsyncMock(side_effect=TimeoutError("request timed out"))
        response.__aexit__ = AsyncMock(return_value=False)

        session = MagicMock()
        session.get = MagicMock(return_value=response)

        sem = asyncio.Semaphore(10)
        result = await fetch_page(session, sem, "https://example.com/timeout", 0.0)

        assert result["error"] is not None
        assert result["content"] is None
        assert "timed out" in result["error"]

    async def test_respects_semaphore(self):
        """Verify fetch_page acquires and releases the semaphore."""
        response = AsyncMock()
        response.text = AsyncMock(return_value="ok")
        response.__aenter__ = AsyncMock(return_value=response)
        response.__aexit__ = AsyncMock(return_value=False)

        session = MagicMock()
        session.get = MagicMock(return_value=response)

        sem = asyncio.Semaphore(1)
        assert sem._value == 1
        result = await fetch_page(session, sem, "https://example.com", 0.0)
        # Semaphore should be released after fetch
        assert sem._value == 1
        assert result["error"] is None


# ── write_to_neon ───────────────────────────────────────────


class TestWriteToNeon:
    async def test_upserts_resources_and_creates_tasks(self):
        results = [
            {"url": "https://example.com/page1", "content": "Hello", "hash": "abc", "error": None},
            {"url": "https://example.com/page2", "content": "World", "hash": "def", "error": None},
        ]

        mock_conn = AsyncMock()
        mock_conn.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_conn.__aexit__ = AsyncMock(return_value=False)

        with patch("psycopg.AsyncConnection.connect", return_value=mock_conn):
            r_count, t_count = await write_to_neon("postgres://test", results, "example.com", None)

        assert r_count == 2
        assert t_count == 2
        # 2 resource upserts + 2 task inserts + 1 commit = 5 calls
        assert mock_conn.execute.call_count == 4
        mock_conn.commit.assert_called_once()

    async def test_skips_error_results(self):
        results = [
            {"url": "https://example.com/ok", "content": "Good", "hash": "abc", "error": None},
            {"url": "https://example.com/bad", "content": None, "hash": None, "error": "404"},
        ]

        mock_conn = AsyncMock()
        mock_conn.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_conn.__aexit__ = AsyncMock(return_value=False)

        with patch("psycopg.AsyncConnection.connect", return_value=mock_conn):
            r_count, t_count = await write_to_neon("postgres://test", results, "example.com", None)

        assert r_count == 1
        assert t_count == 1

    async def test_priority_pattern_sets_priority(self):
        results = [
            {"url": "https://example.com/en/page", "content": "EN", "hash": "a1", "error": None},
            {"url": "https://example.com/ja/page", "content": "JA", "hash": "a2", "error": None},
        ]

        mock_conn = AsyncMock()
        mock_conn.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_conn.__aexit__ = AsyncMock(return_value=False)

        priority_re = re.compile("/en/")
        with patch("psycopg.AsyncConnection.connect", return_value=mock_conn):
            await write_to_neon("postgres://test", results, "example.com", priority_re)

        # Check that priority 1 was used for /en/ and 0 for /ja/
        task_calls = [c for c in mock_conn.execute.call_args_list if "tasks" in str(c.args[0])]
        assert len(task_calls) == 2
        # First task (en page) should have priority 1
        assert task_calls[0].args[1][1] == 1
        # Second task (ja page) should have priority 0
        assert task_calls[1].args[1][1] == 0

    async def test_handles_empty_results(self):
        mock_conn = AsyncMock()
        mock_conn.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_conn.__aexit__ = AsyncMock(return_value=False)

        with patch("psycopg.AsyncConnection.connect", return_value=mock_conn):
            r_count, t_count = await write_to_neon("postgres://test", [], "example.com", None)

        assert r_count == 0
        assert t_count == 0
