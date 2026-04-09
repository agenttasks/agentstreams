/**
 * Crawlee integration — HTTP and browser crawling for agentstreams.
 *
 * Re-exports the key Crawlee classes and provides a pre-configured
 * factory for HTTP crawling (the most common mode in agentstreams
 * pipelines: sitemap discovery, doc scraping, RSS feeds).
 *
 * For full control, import directly from crawlee or @crawlee/* packages.
 *
 * Uses CLAUDE_CODE_OAUTH_TOKEN for API auth (never ANTHROPIC_API_KEY).
 */

import { HttpCrawler } from "@crawlee/http";
import { Dataset, KeyValueStore, RequestQueue } from "@crawlee/core";
import { sleep } from "@crawlee/utils";

// ── Re-exports ─────────────────────────────────────────────────

export { HttpCrawler } from "@crawlee/http";
export { Dataset, KeyValueStore, RequestQueue } from "@crawlee/core";
export { sleep } from "@crawlee/utils";

// ── Types ──────────────────────────────────────────────────────

export interface CrawlResult {
  url: string;
  status: number;
  title: string;
  content: string;
  crawledAt: string;
  contentLength: number;
}

export interface CrawlerConfig {
  /** Max concurrent requests (default: 5) */
  maxConcurrency?: number;
  /** Max requests per crawl run (default: 100) */
  maxRequestsPerCrawl?: number;
  /** Request timeout in seconds (default: 30) */
  requestHandlerTimeoutSecs?: number;
  /** Retry count on failure (default: 3) */
  maxRequestRetries?: number;
}

// ── Factory ────────────────────────────────────────────────────

/**
 * Create a pre-configured HTTP crawler that collects results into an array.
 *
 * Usage:
 * ```ts
 * const { crawler, results } = createHttpCrawler({ maxConcurrency: 3 });
 * await crawler.run(["https://docs.anthropic.com/en/docs"]);
 * console.log(results); // CrawlResult[]
 * ```
 */
export function createHttpCrawler(config: CrawlerConfig = {}): {
  crawler: InstanceType<typeof HttpCrawler>;
  results: CrawlResult[];
} {
  const results: CrawlResult[] = [];

  const crawler = new HttpCrawler({
    maxConcurrency: config.maxConcurrency ?? 5,
    maxRequestsPerCrawl: config.maxRequestsPerCrawl ?? 100,
    requestHandlerTimeoutSecs: config.requestHandlerTimeoutSecs ?? 30,
    maxRequestRetries: config.maxRequestRetries ?? 3,

    async requestHandler({ request, body, response }) {
      const html = typeof body === "string" ? body : body.toString("utf-8");
      const titleMatch = html.match(/<title[^>]*>([^<]*)<\/title>/i);

      results.push({
        url: request.loadedUrl ?? request.url,
        status: response.statusCode ?? 0,
        title: titleMatch?.[1]?.trim() ?? "",
        content: html,
        crawledAt: new Date().toISOString(),
        contentLength: html.length,
      });
    },
  });

  return { crawler, results };
}

/**
 * Crawl a list of URLs and return structured results.
 *
 * Convenience wrapper — creates a crawler, runs it, and returns results.
 */
export async function crawlUrls(
  urls: string[],
  config: CrawlerConfig = {},
): Promise<CrawlResult[]> {
  const { crawler, results } = createHttpCrawler(config);
  await crawler.run(urls);
  return results;
}
