# Ruby Stack Setup

## Installation

```ruby
# Gemfile
source 'https://rubygems.org'

gem 'anthropic'              # Official Ruby SDK
gem 'mechanize'              # Web crawling with cookie/form support
gem 'nokogiri'               # HTML/XML parsing (C extension, fast)
gem 'bloomer'                # Bloom filter implementation
gem 'concurrent-ruby'        # Thread-safe data structures
gem 'sqlite3'                # Local storage
```

```bash
bundle install
```

## Package Overview

| Gem | Purpose |
|-----|---------|
| `anthropic` | Official Ruby SDK — messages, streaming, tool use |
| `mechanize` | Web crawling with automatic cookie handling, form submission |
| `nokogiri` | HTML/XML parsing with CSS and XPath selectors |
| `bloomer` | Pure Ruby bloom filter with serialization |
| `solargraph` | Ruby LSP server |

**Note:** No Agent SDK for Ruby. MCP SDK is available: `modelcontextprotocol/ruby-sdk` (758★).

## Quick Start: Mechanize + Claude + Bloom Filter

```ruby
require 'anthropic'
require 'mechanize'
require 'bloomer'
require 'json'

client = Anthropic::Client.new
bloom = Bloomer::Scalable.new(capacity: 100_000, error_rate: 0.01)
agent = Mechanize.new

agent.user_agent = 'MyCrawler/1.0'
agent.robots = true  # Respect robots.txt
agent.max_history = 0
agent.open_timeout = 10
agent.read_timeout = 30

def crawl(url, agent, bloom, client, depth: 0, max_depth: 3)
  return if depth > max_depth
  return if bloom.include?(url)
  bloom.add(url)

  begin
    page = agent.get(url)
  rescue StandardError => e
    puts "Error crawling #{url}: #{e.message}"
    return
  end

  # Claude extraction
  response = client.messages(
    model: 'claude-sonnet-4-6',
    max_tokens: 1024,
    messages: [{
      role: 'user',
      content: "Extract data from:\n#{page.body[0..30_000]}"
    }]
  )

  result = {
    url: url,
    title: page.title,
    extracted: response.dig('content', 0, 'text'),
    timestamp: Time.now.iso8601,
  }
  File.open('data/results.jsonl', 'a') { |f| f.puts(result.to_json) }

  # Follow links (same domain)
  page.links.each do |link|
    next_url = link.resolved_uri.to_s rescue next
    if next_url.start_with?(URI(url).origin) && !bloom.include?(next_url)
      crawl(next_url, agent, bloom, client, depth: depth + 1)
    end
  end
end

crawl('https://example.com', agent, bloom, client)
```

## Ruby LSP (Solargraph)

```bash
gem install solargraph
# Launch: solargraph stdio
```

Key features: completions, diagnostics, go-to-definition, hover docs.
