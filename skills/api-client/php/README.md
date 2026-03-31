# PHP Stack Setup

## Installation (Composer)

```bash
composer require anthropic-sdk/anthropic-sdk-php
composer require guzzlehttp/guzzle:^7.9
composer require --dev phpunit/phpunit:^11
```

## Quick Start

```php
<?php
use GuzzleHttp\Client;
use GuzzleHttp\Middleware;
use GuzzleHttp\HandlerStack;
use GuzzleHttp\RetryMiddleware;

class ApiClient
{
    private Client $http;

    public function __construct(string $baseUrl, string $apiKey)
    {
        $stack = HandlerStack::create();
        $stack->push(Middleware::retry(
            function ($retries, $request, $response, $exception) {
                if ($retries >= 3) return false;
                if ($response && in_array($response->getStatusCode(), [429, 500, 502, 503, 504])) {
                    return true;
                }
                return $exception !== null;
            },
            function ($retries) {
                return (int) pow(2, $retries) * 1000; // Exponential backoff in ms
            }
        ));

        $this->http = new Client([
            'base_uri' => $baseUrl,
            'handler' => $stack,
            'headers' => ['Authorization' => "Bearer {$apiKey}"],
            'timeout' => 30,
            'connect_timeout' => 5,
        ]);
    }

    public function getUser(int $id): array
    {
        $response = $this->http->get("/users/{$id}");
        return json_decode($response->getBody()->getContents(), true);
    }
}
```

## Further Reading

- `shared/retry-patterns.md` — Retry strategy, circuit breaker, timeouts
- `shared/auth-patterns.md` — API key, OAuth 2.0, JWT, mTLS
