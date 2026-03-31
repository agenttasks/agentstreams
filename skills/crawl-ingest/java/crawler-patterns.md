# Java Crawler Patterns

## crawler4j Configuration

```java
CrawlConfig config = new CrawlConfig();
config.setCrawlStorageFolder("./data/crawl");
config.setPolitenessDelay(500);          // ms between requests
config.setMaxDepthOfCrawling(10);
config.setMaxPagesToFetch(10000);
config.setIncludeBinaryContentInCrawling(false);
config.setResumableCrawling(true);       // Resume after crash
config.setUserAgentString("MyCrawler/1.0 (+https://example.com/bot)");
config.setRespectNoFollow(true);
config.setRespectNoIndex(true);
```

## JSoup Parsing

```java
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

// Parse from string
Document doc = Jsoup.parse(htmlString);

// CSS selectors
String title = doc.select("h1.product-title").text();
String price = doc.select("span.price").text();
Elements links = doc.select("a[href]");

// Extract all text
String bodyText = doc.body().text();

// Parse from URL (standalone, no crawler4j)
Document page = Jsoup.connect("https://example.com")
    .userAgent("MyCrawler/1.0")
    .timeout(5000)
    .get();
```

## Bloom Filter Persistence

```java
import com.google.common.hash.BloomFilter;
import com.google.common.hash.Funnels;
import java.io.*;

public class BloomDedup {
    private BloomFilter<String> filter;
    private final String path;

    public BloomDedup(String path, int expectedUrls, double fpp) {
        this.path = path;
        File file = new File(path);
        if (file.exists()) {
            try (InputStream is = new FileInputStream(file)) {
                this.filter = BloomFilter.readFrom(is, Funnels.unencodedCharsFunnel());
            } catch (IOException e) {
                this.filter = BloomFilter.create(Funnels.unencodedCharsFunnel(), expectedUrls, fpp);
            }
        } else {
            this.filter = BloomFilter.create(Funnels.unencodedCharsFunnel(), expectedUrls, fpp);
        }
    }

    public boolean isNew(String url) {
        return !filter.mightContain(url);
    }

    public void add(String url) {
        filter.put(url);
    }

    public void save() throws IOException {
        try (OutputStream os = new FileOutputStream(path)) {
            filter.writeTo(os);
        }
    }

    public double currentFpp() {
        return filter.expectedFpp();
    }
}
```

## Streaming Extraction with Anthropic SDK

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.models.*;

AnthropicClient client = AnthropicClient.builder().build();

// Streaming response
client.messages().createStreaming(
    MessageCreateParams.builder()
        .model("claude-opus-4-6")
        .maxTokens(1024)
        .addUserMessage("Extract product data from:\n" + html)
        .build()
).subscribe(event -> {
    if (event instanceof ContentBlockDeltaEvent delta) {
        System.out.print(delta.getDelta().getText());
    }
});
```

## LangChain4j Integration (Prompt Templates)

```java
import dev.langchain4j.model.anthropic.AnthropicChatModel;
import dev.langchain4j.service.AiServices;

// Define extraction interface
interface ProductExtractor {
    @UserMessage("Extract product info from this HTML: {{html}}")
    ProductInfo extract(@V("html") String html);
}

record ProductInfo(String name, double price, String description) {}

AnthropicChatModel model = AnthropicChatModel.builder()
    .modelName("claude-sonnet-4-6")
    .build();

ProductExtractor extractor = AiServices.create(ProductExtractor.class, model);
ProductInfo product = extractor.extract(htmlContent);
```
