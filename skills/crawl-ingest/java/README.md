# Java Stack Setup

## Installation (Gradle)

```groovy
// build.gradle
plugins {
    id 'java'
    id 'application'
}

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

repositories {
    mavenCentral()
}

dependencies {
    // Anthropic SDK
    implementation 'com.anthropic:anthropic-java:2.5.0'

    // Web Crawling
    implementation 'edu.uci:crawler4j:4.4.0'
    implementation 'org.jsoup:jsoup:1.17.2'

    // Bloom Filters
    implementation 'com.google.guava:guava:33.4.0-jre'

    // LangChain4j (closest to DSPy)
    implementation 'dev.langchain4j:langchain4j:1.0.0'
    implementation 'dev.langchain4j:langchain4j-anthropic:1.0.0'

    // LSP (for programmatic use)
    implementation 'org.eclipse.lsp4j:org.eclipse.lsp4j:0.23.1'

    // JSON processing
    implementation 'com.fasterxml.jackson.core:jackson-databind:2.17.0'

    // SQLite (local storage)
    implementation 'org.xerial:sqlite-jdbc:3.45.0.0'
}
```

## Package Overview

| Package | Coordinates | Purpose |
|---------|-------------|---------|
| Anthropic Java SDK | `com.anthropic:anthropic-java:2.5.0` | Messages API, streaming, tool use, thinking (Kotlin impl) |
| MCP Java SDK | `io.modelcontextprotocol:java-sdk` (3.3k★) | Official MCP SDK — maintained with Spring AI |
| MCP Kotlin SDK | `io.modelcontextprotocol:kotlin-sdk` (1.3k★) | Official Kotlin MCP SDK — maintained by JetBrains |
| crawler4j | `edu.uci:crawler4j:4.4.0` | Lightweight web crawler (closest to Scrapy/Crawlee DX) |
| JSoup | `org.jsoup:jsoup:1.17.2` | HTML parsing, CSS selectors |
| Guava | `com.google.guava:guava:33.4.0-jre` | BloomFilter, Hashing, Collections |
| LangChain4j | `dev.langchain4j:langchain4j:1.0.0` | LLM integration, prompt templates (no DSPy optimizer) |
| LSP4J | `org.eclipse.lsp4j:org.eclipse.lsp4j:0.23.1` | Language Server Protocol bindings |

## Quick Start: crawler4j + Claude + Guava Bloom Filter

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.models.*;
import com.google.common.hash.BloomFilter;
import com.google.common.hash.Funnels;
import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;
import edu.uci.ics.crawler4j.url.WebURL;

public class ProductCrawler extends WebCrawler {
    private static final BloomFilter<String> BLOOM =
        BloomFilter.create(Funnels.unencodedCharsFunnel(), 1_000_000, 0.01);

    private final AnthropicClient client =
        AnthropicClient.builder().build();

    @Override
    public boolean shouldVisit(Page referringPage, WebURL url) {
        String href = url.getURL().toLowerCase();
        return !BLOOM.mightContain(href) && href.startsWith("https://example.com");
    }

    @Override
    public void visit(Page page) {
        String url = page.getWebURL().getURL();
        BLOOM.put(url);

        if (page.getParseData() instanceof HtmlParseData htmlData) {
            String html = htmlData.getHtml();
            String title = htmlData.getTitle();

            // Claude extraction
            Message response = client.messages().create(
                MessageCreateParams.builder()
                    .model("claude-opus-4-6")
                    .maxTokens(1024)
                    .addUserMessage(
                        "Extract product data from:\nTitle: " + title +
                        "\nHTML: " + html.substring(0, Math.min(html.length(), 50000))
                    )
                    .build()
            );

            System.out.println("Extracted: " + url);
            // Store response...
        }
    }

    public static void main(String[] args) throws Exception {
        CrawlConfig config = new CrawlConfig();
        config.setCrawlStorageFolder("./data/crawl");
        config.setPolitenessDelay(500);
        config.setMaxDepthOfCrawling(5);
        config.setMaxPagesToFetch(1000);

        PageFetcher pageFetcher = new PageFetcher(config);
        RobotstxtConfig robotsConfig = new RobotstxtConfig();
        RobotstxtServer robotsServer = new RobotstxtServer(robotsConfig, pageFetcher);

        CrawlController controller = new CrawlController(config, pageFetcher, robotsServer);
        controller.addSeed("https://example.com/products");
        controller.start(ProductCrawler.class, 4); // 4 threads
    }
}
```

## Further Reading

- `java/gradle-setup.md` — Full Gradle configuration
- `java/crawler-patterns.md` — crawler4j and JSoup patterns
- `java/lsp-config.md` — LSP4J configuration
- `shared/bloom-filters.md` — Guava BloomFilter API
- `shared/programmatic-prompts.md` — LangChain4j as DSPy alternative
