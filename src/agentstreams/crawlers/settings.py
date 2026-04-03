"""Scrapy settings for AgentStreams crawl pipelines.

Configure spider behavior, item pipelines, and Neon persistence.
Use as SCRAPY_SETTINGS_MODULE or import directly.
"""

BOT_NAME = "agentstreams"
SPIDER_MODULES = ["agentstreams.crawlers"]
NEWSPIDER_MODULE = "agentstreams.crawlers"

USER_AGENT = "agentstreams-crawler/2.0 (scrapy sitemap spider)"
ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 20
DOWNLOAD_DELAY = 0.05
CONCURRENT_REQUESTS_PER_DOMAIN = 10

# Disable cookies and telemetry
COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False

# Item pipelines (order matters)
ITEM_PIPELINES = {
    "agentstreams.crawlers.pipelines.BloomFilterPipeline": 100,
    "agentstreams.crawlers.pipelines.NeonPersistencePipeline": 200,
    "agentstreams.crawlers.pipelines.MetricsPipeline": 300,
}

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"

# AutoThrottle for polite crawling
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 10.0

# Request fingerprinting
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
