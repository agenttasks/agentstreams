# Go Stack Setup

## Installation

```bash
go mod init crawl-project

# Anthropic SDK
go get github.com/anthropics/anthropic-sdk-go

# Web Crawling
go get github.com/gocolly/colly/v2          # Colly — Go's premier web scraper
go get github.com/PuerkitoBio/goquery       # jQuery-like HTML parsing

# Bloom Filters
go get github.com/bits-and-blooms/bloom/v3  # Most popular Go bloom filter

# MCP SDK (maintained by Google — 4.3k★)
go get github.com/modelcontextprotocol/go-sdk

# HTTP utilities
go get golang.org/x/net/html                # HTML tokenizer/parser
```

## Package Overview

| Package | Purpose |
|---------|---------|
| `github.com/anthropics/anthropic-sdk-go` | Official Go SDK — messages, streaming, tool use |
| `github.com/gocolly/colly/v2` | Web scraping framework (closest to Scrapy/Crawlee) |
| `github.com/PuerkitoBio/goquery` | jQuery-like DOM manipulation |
| `github.com/bits-and-blooms/bloom/v3` | Bloom filter with serialization support |
| `gopls` | Go LSP server (installed separately) |

**Note:** No Agent SDK for Go. MCP SDK is available: `github.com/modelcontextprotocol/go-sdk` (4.3k★, maintained by Google).

## Quick Start: Colly + Claude + Bloom Filter

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "github.com/anthropics/anthropic-sdk-go"
    "github.com/bits-and-blooms/bloom/v3"
    "github.com/gocolly/colly/v2"
)

func main() {
    client := anthropic.NewClient()
    filter := bloom.NewWithEstimates(1_000_000, 0.01)

    c := colly.NewCollector(
        colly.AllowedDomains("example.com"),
        colly.MaxDepth(5),
        colly.Async(true),
    )

    c.Limit(&colly.LimitRule{
        DomainGlob:  "*",
        Parallelism: 4,
        Delay:       500 * time.Millisecond,
    })

    c.OnHTML("a[href]", func(e *colly.HTMLElement) {
        link := e.Request.AbsoluteURL(e.Attr("href"))
        if !filter.TestString(link) {
            filter.AddString(link)
            e.Request.Visit(link)
        }
    })

    c.OnResponse(func(r *colly.Response) {
        url := r.Request.URL.String()
        html := string(r.Body)

        // Claude extraction
        msg, err := client.Messages.New(context.Background(),
            anthropic.MessageNewParams{
                Model:     "claude-opus-4-6",
                MaxTokens: 1024,
                Messages: []anthropic.MessageParam{
                    anthropic.NewUserMessage(
                        anthropic.NewTextBlock(
                            fmt.Sprintf("Extract data from:\n%s", html[:min(len(html), 50000)]),
                        ),
                    ),
                },
            },
        )
        if err != nil {
            log.Printf("Claude error for %s: %v", url, err)
            return
        }

        fmt.Printf("Extracted: %s\n", url)
        // Store msg.Content...
    })

    c.Visit("https://example.com")
    c.Wait()

    // Save bloom filter
    f, _ := os.Create("data/bloom.bin")
    defer f.Close()
    filter.WriteTo(f)
}
```

## Bloom Filter Persistence

```go
// Save
f, _ := os.Create("bloom.bin")
filter.WriteTo(f)
f.Close()

// Load
f, _ = os.Open("bloom.bin")
filter = new(bloom.BloomFilter)
filter.ReadFrom(f)
f.Close()
```

## Go LSP (gopls)

```bash
go install golang.org/x/tools/gopls@latest
# Launch: gopls serve  (or gopls -listen=:8080)
```

Communicate via JSON-RPC over stdio, same pattern as TypeScript/Python LSP.
