# Ruby Stack Setup

## Gemfile

```ruby
source 'https://rubygems.org'

gem 'anthropic-sdk-ruby'
gem 'kiba', '~> 4.0'           # ETL framework
gem 'kiba-common', '~> 1.5'    # Common transforms
gem 'sidekiq', '~> 7.3'        # Background job orchestration

group :test do
  gem 'rspec', '~> 3.13'
end
```

## Quick Start

```ruby
require 'anthropic'
require 'kiba'

client = Anthropic::Client.new

# Kiba ETL pipeline
job = Kiba.parse do
  source Kiba::Common::Sources::CSV, filename: 'data/input.csv'

  transform do |row|
    row[:name] = row[:name].strip
    row
  end

  transform do |row|
    next if row[:id].nil?
    row
  end

  destination Kiba::Common::Destinations::CSV, filename: 'data/output.csv'
end

Kiba.run(job)
```

## Further Reading

- `shared/pipeline-patterns.md` — Idempotency, backpressure, DLQ
- `shared/orchestration.md` — DAGs, scheduling
