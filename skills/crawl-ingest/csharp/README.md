# C# Stack Setup

## Installation (.NET)

```xml
<!-- .csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Anthropic" Version="0.8.0" />
    <PackageReference Include="AngleSharp" Version="1.1.2" />
    <PackageReference Include="Abot" Version="5.1.0" />
    <PackageReference Include="BloomFilter.NetCore" Version="2.1.0" />
    <PackageReference Include="Microsoft.Data.Sqlite" Version="8.0.0" />
  </ItemGroup>
</Project>
```

```bash
dotnet restore
```

## Package Overview

| Package | Purpose |
|---------|---------|
| `Anthropic` | C# SDK — messages, streaming, thinking |
| `AngleSharp` | HTML parsing engine (modern DOM API) |
| `Abot` | Web crawler framework (.NET native) |
| `BloomFilter.NetCore` | Bloom filter implementation |
| `OmniSharp` | C# LSP server |

**Note:** No Agent SDK for C#. MCP SDK is available: `modelcontextprotocol/csharp-sdk` (maintained by Microsoft). Manual tool loop only (no runner).

## Quick Start: Abot + Claude + Bloom Filter

```csharp
using Anthropic;
using Abot2.Crawler;
using Abot2.Poco;
using AngleSharp.Html.Parser;
using BloomFilter;
using System.Text.Json;

var client = new AnthropicClient();
var bloom = FilterBuilder.Build(1_000_000, 0.01);
var parser = new HtmlParser();

var config = new CrawlConfiguration
{
    MaxPagesToCrawl = 1000,
    MaxCrawlDepthInPages = 5,
    MinCrawlDelayPerDomainMilliSeconds = 500,
    IsRespectRobotsDotTextEnabled = true,
    UserAgentString = "MyCrawler/1.0",
};

var crawler = new PoliteWebCrawler(config);

crawler.PageCrawlCompleted += async (sender, args) =>
{
    var page = args.CrawledPage;
    var url = page.Uri.AbsoluteUri;

    if (bloom.Contains(url)) return;
    bloom.Add(url);

    if (page.HttpResponseMessage?.IsSuccessStatusCode != true) return;

    var html = page.Content.Text;
    var doc = parser.ParseDocument(html);
    var title = doc.Title;

    // Claude extraction
    var response = await client.Messages.CreateAsync(new MessageCreateParams
    {
        Model = "claude-opus-4-6",
        MaxTokens = 1024,
        Messages = new[]
        {
            new MessageParam
            {
                Role = "user",
                Content = $"Extract product data:\nTitle: {title}\nHTML: {html[..Math.Min(html.Length, 50000)]}"
            }
        }
    });

    Console.WriteLine($"Extracted: {url}");
    // Store response...
};

await crawler.CrawlAsync(new Uri("https://example.com"));
```

## C# LSP (OmniSharp)

```bash
dotnet tool install -g omnisharp
# Launch: omnisharp --stdio
```

Key features: completions, diagnostics, go-to-definition, refactoring, Roslyn-powered analysis.
