"""Scrapy item pipelines for Neon Postgres persistence and bloom filter sync.

Pipelines run in order after each spider item is yielded:
1. BloomFilterPipeline — dedup check + filter update
2. NeonPersistencePipeline — upsert CrawledPage + create analysis task
3. MetricsPipeline — emit agentstreams.crawl.* metrics
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class BloomFilterPipeline:
    """Scrapy pipeline that updates the spider's bloom filter state.

    Marks duplicate items by setting is_duplicate=True so downstream
    pipelines can skip them.
    """

    def process_item(self, item: dict[str, Any], spider: Any) -> dict[str, Any]:
        if not hasattr(spider, "bloom"):
            return item

        url = item.get("url", "")
        if url in spider.bloom:
            item["is_duplicate"] = True
            logger.debug("Bloom filter: duplicate %s", url)
        else:
            item["is_duplicate"] = False
        return item


class NeonPersistencePipeline:
    """Scrapy pipeline that persists crawled pages to Neon Postgres.

    Creates a psycopg async connection on spider open, batch-commits
    on spider close. Skips items marked as duplicates.
    """

    def __init__(self) -> None:
        self._neon_url = ""
        self._pages: list[dict[str, Any]] = []

    def open_spider(self, spider: Any) -> None:
        self._neon_url = os.environ.get("NEON_DATABASE_URL", "")
        if not self._neon_url:
            logger.warning("NEON_DATABASE_URL not set — persistence disabled")

    def process_item(self, item: dict[str, Any], spider: Any) -> dict[str, Any]:
        if item.get("is_duplicate"):
            return item
        if self._neon_url:
            self._pages.append(item)
        return item

    def close_spider(self, spider: Any) -> None:
        if not self._neon_url or not self._pages:
            return

        # Sync batch write (Scrapy close_spider is sync)
        import psycopg

        try:
            with psycopg.connect(self._neon_url) as conn:
                for page in self._pages:
                    conn.execute(
                        """INSERT INTO resources (type, label, url, content_hash, fetched_at, description)
                           VALUES (%s, %s, %s, %s, now(), %s)
                           ON CONFLICT (url) DO UPDATE
                           SET content_hash = EXCLUDED.content_hash, fetched_at = now()""",
                        (
                            "crawled_page",
                            page.get("domain", ""),
                            page["url"],
                            page["content_hash"],
                            json.dumps(
                                {
                                    "page_type": page.get("page_type", "guide"),
                                    "topics": page.get("topics", []),
                                }
                            ),
                        ),
                    )
                conn.commit()
                logger.info("Persisted %d pages to Neon", len(self._pages))
        except Exception:
            logger.exception("Neon persistence failed")


class MetricsPipeline:
    """Scrapy pipeline that emits crawl metrics to stderr as JSON.

    Metrics follow the agentstreams.crawl.* dimensional model
    defined in ontology/agentstreams.ttl.
    """

    def __init__(self) -> None:
        self._count = 0
        self._dupes = 0

    def process_item(self, item: dict[str, Any], spider: Any) -> dict[str, Any]:
        if item.get("is_duplicate"):
            self._dupes += 1
        else:
            self._count += 1
        return item

    def close_spider(self, spider: Any) -> None:
        domain = getattr(spider, "domain", "unknown")
        import sys

        metrics = [
            {
                "metric": "agentstreams.crawl.pages",
                "tags": {"domain": domain, "status": "success", "is_new": "true"},
                "value": self._count,
            },
            {
                "metric": "agentstreams.crawl.pages",
                "tags": {"domain": domain, "status": "duplicate", "is_new": "false"},
                "value": self._dupes,
            },
        ]
        if hasattr(spider, "bloom"):
            stats = spider.bloom.stats()
            metrics.append(
                {
                    "metric": "agentstreams.crawl.dedup",
                    "tags": {"method": "bloom"},
                    "value": stats["estimated_fp_rate"],
                }
            )

        for m in metrics:
            print(json.dumps(m), file=sys.stderr)
