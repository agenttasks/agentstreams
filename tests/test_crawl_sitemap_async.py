"""Tests for crawl-sitemap.py — async fetch, DB write, and error recovery paths."""

import asyncio
import re
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from importlib import import_module

mod = import_module("crawl-sitemap")
fetch_sitemap_urls = mod.fetch_sitemap_urls
fetch_page = mod.fetch_page
write_to_neon = mod.write_to_neon
TRUNCATE_BYTES = mod.TRUNCATE_BYTES


# ── Shared mock factories ───────────────────────────────────


def _mock_response(text=None, *, side_effect=None):
    """Build an AsyncMock HTTP response for aiohttp session.get()."""
    resp = AsyncMock()
    if side_effect:
        resp.__aenter__ = AsyncMock(side_effect=side_effect)
    else:
        resp.text = AsyncMock(return_value=text)
        resp.__aenter__ = AsyncMock(return_value=resp)
    resp.__aexit__ = AsyncMock(return_value=False)
    return resp


def _mock_session(response=None, *, side_effect=None):
    """Build a MagicMock session with a pre-configured get()."""
    session = MagicMock()
    if side_effect:
        session.get = MagicMock(side_effect=side_effect)
    else:
        session.get = MagicMock(return_value=response)
    return session


def _mock_async_conn():
    """Build an AsyncMock psycopg connection."""
    conn = AsyncMock()
    conn.__aenter__ = AsyncMock(return_value=conn)
    conn.__aexit__ = AsyncMock(return_value=False)
    return conn


# ── fetch_sitemap_urls ──────────────────────────────────────


class TestFetchSitemapUrls:
    async def test_returns_urls_from_simple_sitemap(self):
        xml = """<?xml version="1.0"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/page1</loc></url>
  <url><loc>https://example.com/page2</loc></url>
</urlset>"""
        session = _mock_session(_mock_response(xml))
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
            resp = _mock_response(index_xml if call_count == 0 else sub_xml)
            call_count += 1
            return resp

        session = _mock_session(side_effect=make_response)
        urls = await fetch_sitemap_urls(session, "https://example.com/sitemap.xml")
        assert "https://example.com/deep-page" in urls

    async def test_returns_empty_on_fetch_error(self):
        session = _mock_session(_mock_response(side_effect=ConnectionError("timeout")))
        urls = await fetch_sitemap_urls(session, "https://example.com/sitemap.xml")
        assert urls == []


# ── fetch_page ──────────────────────────────────────────────


class TestFetchPage:
    async def test_fetches_html_page(self):
        session = _mock_session(_mock_response("<html><body><p>Hello world</p></body></html>"))
        result = await fetch_page(session, asyncio.Semaphore(10), "https://example.com/page", 0.0)
        assert "Hello world" in result["content"]
        assert result["error"] is None

    async def test_fetches_plain_text(self):
        session = _mock_session(_mock_response("This is plain text content."))
        result = await fetch_page(session, asyncio.Semaphore(10), "https://example.com/api", 0.0)
        assert result["content"] == "This is plain text content."

    async def test_truncates_large_content(self):
        session = _mock_session(_mock_response("x" * (TRUNCATE_BYTES + 1000)))
        result = await fetch_page(session, asyncio.Semaphore(10), "https://example.com/big", 0.0)
        assert "truncated" in result["content"]

    async def test_returns_error_on_exception(self):
        session = _mock_session(_mock_response(side_effect=TimeoutError("request timed out")))
        result = await fetch_page(
            session, asyncio.Semaphore(10), "https://example.com/timeout", 0.0
        )
        assert result["error"] is not None
        assert result["content"] is None

    async def test_respects_semaphore(self):
        session = _mock_session(_mock_response("ok"))
        sem = asyncio.Semaphore(1)
        await fetch_page(session, sem, "https://example.com", 0.0)
        assert sem._value == 1  # released after fetch


# ── write_to_neon ───────────────────────────────────────────


class TestWriteToNeon:
    async def test_upserts_resources_and_creates_tasks(self):
        results = [
            {"url": "https://example.com/page1", "content": "Hello", "hash": "abc", "error": None},
            {"url": "https://example.com/page2", "content": "World", "hash": "def", "error": None},
        ]
        mock_conn = _mock_async_conn()
        with patch.object(mod, "_src_available", False), patch(
            "psycopg.AsyncConnection.connect", return_value=mock_conn
        ):
            r_count, t_count = await write_to_neon("postgres://test", results, "example.com", None)
        assert r_count == 2
        assert t_count == 2
        assert mock_conn.execute.call_count == 4
        mock_conn.commit.assert_called_once()

    async def test_skips_error_results(self):
        results = [
            {"url": "https://example.com/ok", "content": "Good", "hash": "abc", "error": None},
            {"url": "https://example.com/bad", "content": None, "hash": None, "error": "404"},
        ]
        mock_conn = _mock_async_conn()
        with patch.object(mod, "_src_available", False), patch(
            "psycopg.AsyncConnection.connect", return_value=mock_conn
        ):
            r_count, t_count = await write_to_neon("postgres://test", results, "example.com", None)
        assert r_count == 1
        assert t_count == 1

    async def test_priority_pattern_sets_priority(self):
        results = [
            {"url": "https://example.com/en/page", "content": "EN", "hash": "a1", "error": None},
            {"url": "https://example.com/ja/page", "content": "JA", "hash": "a2", "error": None},
        ]
        mock_conn = _mock_async_conn()
        with patch.object(mod, "_src_available", False), patch(
            "psycopg.AsyncConnection.connect", return_value=mock_conn
        ):
            await write_to_neon("postgres://test", results, "example.com", re.compile("/en/"))
        task_calls = [c for c in mock_conn.execute.call_args_list if "tasks" in str(c.args[0])]
        assert task_calls[0].args[1][1] == 1  # /en/ -> priority 1
        assert task_calls[1].args[1][1] == 0  # /ja/ -> priority 0

    async def test_handles_empty_results(self):
        mock_conn = _mock_async_conn()
        with patch.object(mod, "_src_available", False), patch(
            "psycopg.AsyncConnection.connect", return_value=mock_conn
        ):
            r_count, t_count = await write_to_neon("postgres://test", [], "example.com", None)
        assert r_count == 0
        assert t_count == 0


# ── Concurrent fetch failure ────────────────────────────────


class TestFetchPagePartialFailure:
    async def test_concurrent_fetches_with_mixed_results(self):
        """Simulate multiple concurrent fetches where some succeed and some fail."""
        sem = asyncio.Semaphore(5)

        async def mock_fetch(url):
            if "fail" in url:
                resp = _mock_response(side_effect=ConnectionError(f"Failed: {url}"))
            else:
                resp = _mock_response(f"Content of {url}")
            return await fetch_page(_mock_session(resp), sem, url, 0.0)

        urls = [
            "https://example.com/ok1",
            "https://example.com/fail1",
            "https://example.com/ok2",
            "https://example.com/fail2",
            "https://example.com/ok3",
        ]
        results = await asyncio.gather(*[mock_fetch(u) for u in urls])
        assert len([r for r in results if r["error"] is None]) == 3
        assert len([r for r in results if r["error"] is not None]) == 2
