# Ruby Stack Setup

## Gemfile

```ruby
source 'https://rubygems.org'

gem 'anthropic-sdk-ruby'
gem 'faraday', '~> 2.12'
gem 'faraday-retry', '~> 2.2'
gem 'oauth2', '~> 2.0'

group :test do
  gem 'rspec', '~> 3.13'
  gem 'webmock', '~> 3.24'
end
```

## Quick Start

```ruby
require 'anthropic'
require 'faraday'
require 'faraday/retry'

class ApiClient
  def initialize(base_url:, api_key:)
    retry_options = {
      max: 3,
      interval: 1,
      backoff_factor: 2,
      retry_statuses: [408, 429, 500, 502, 503, 504]
    }

    @http = Faraday.new(url: base_url) do |f|
      f.request :authorization, 'Bearer', api_key
      f.request :retry, retry_options
      f.response :json
      f.adapter Faraday.default_adapter
    end

    @claude = Anthropic::Client.new
  end

  def get_user(id)
    response = @http.get("/users/#{id}")
    raise "HTTP #{response.status}" unless response.success?
    response.body
  end
end
```

## Further Reading

- `shared/retry-patterns.md` — Retry strategy, circuit breaker, timeouts
- `shared/auth-patterns.md` — API key, OAuth 2.0, JWT, mTLS
