# PHP Stack Setup

## Installation (Composer)

```bash
composer require anthropic-sdk/anthropic-sdk-php
composer require illuminate/pipeline:^11.0   # Laravel Pipeline
composer require league/csv:^9.18
composer require --dev phpunit/phpunit:^11
```

## Quick Start

```php
<?php
use Illuminate\Pipeline\Pipeline;
use League\Csv\Reader;
use League\Csv\Writer;

class ExtractStage {
    public function handle(array $context, \Closure $next) {
        $csv = Reader::createFromPath($context['source'], 'r');
        $csv->setHeaderOffset(0);
        $context['records'] = iterator_to_array($csv->getRecords());
        return $next($context);
    }
}

class TransformStage {
    public function handle(array $context, \Closure $next) {
        $context['records'] = array_filter(
            $context['records'],
            fn($r) => !empty($r['id'])
        );
        $context['records'] = array_map(
            fn($r) => array_merge($r, ['name' => trim($r['name'])]),
            $context['records']
        );
        return $next($context);
    }
}

class LoadStage {
    public function handle(array $context, \Closure $next) {
        $writer = Writer::createFromPath($context['target'], 'w+');
        $writer->insertOne(array_keys($context['records'][0]));
        $writer->insertAll($context['records']);
        return $next($context);
    }
}

// Run pipeline
$result = (new Pipeline(app()))
    ->send(['source' => 'input.csv', 'target' => 'output.csv'])
    ->through([ExtractStage::class, TransformStage::class, LoadStage::class])
    ->thenReturn();
```

## Further Reading

- `shared/pipeline-patterns.md` — Idempotency, backpressure, DLQ
- `shared/orchestration.md` — DAGs, scheduling
