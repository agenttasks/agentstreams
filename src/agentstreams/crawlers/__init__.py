"""Scrapy-based web crawlers with bloom filter deduplication.

Provides Scrapy spiders that crawl sitemaps and web pages, deduplicate
via bloom filters, and persist results to Neon Postgres through the
UDA entity model.
"""
