# Cross-Language Package Equivalence Matrix — API Client

## HTTP Clients

| Capability | TypeScript | Python | Java | Go | Ruby | C# | PHP | cURL |
|---|---|---|---|---|---|---|---|---|
| **Primary** | axios 1.9 | httpx 0.28 | OkHttp 4.12 | net/http + resty v2 | Faraday 2.12 | HttpClient | Guzzle 7.9 | curl |
| **Async** | Native fetch | httpx (async) | OkHttp async | Native | Async (Typhoeus) | HttpClient (async) | Guzzle (async) | curl --parallel |
| **HTTP/2** | undici | httpx | OkHttp | net/http | -- | HttpClient | -- | curl --http2 |
| **Interceptors** | axios interceptors | httpx event hooks | OkHttp interceptors | RoundTripper | Faraday middleware | DelegatingHandler | Guzzle middleware | -- |

## OpenAPI Code Generation

| Capability | TypeScript | Python | Java | Go | Ruby | C# | PHP | cURL |
|---|---|---|---|---|---|---|---|---|
| **Codegen** | openapi-typescript 7.8 | openapi-python-client 0.24 | openapi-generator | oapi-codegen 2.4 | openapi-generator | NSwag 14 / Kiota | openapi-generator | N/A |
| **Types Only** | openapi-typescript | datamodel-code-generator | -- | -- | -- | -- | -- | -- |
| **Runtime** | openapi-fetch | -- | -- | -- | -- | -- | -- | -- |

## Validation

| Capability | TypeScript | Python | Java | Go | Ruby | C# | PHP | cURL |
|---|---|---|---|---|---|---|---|---|
| **Schema** | zod 3.24 | pydantic 2.11 | Jakarta Validation 3.1 | validator v10 | dry-validation | FluentValidation 11 | symfony/validator | jq |
| **Runtime** | zod .parse() | model_validate() | @Valid annotations | .Struct() | .call() | .Validate() | validate() | jq test |

## Retry & Resilience

| Capability | TypeScript | Python | Java | Go | Ruby | C# | PHP | cURL |
|---|---|---|---|---|---|---|---|---|
| **Retry** | axios-retry | tenacity | resilience4j-retry | go-retryablehttp | faraday-retry | Polly 8.5 | guzzle-retry | shell loop |
| **Circuit Breaker** | opossum | pybreaker | resilience4j-cb | sony/gobreaker | stoplight | Polly | -- | -- |
| **Rate Limit** | bottleneck 2.19 | ratelimit 2.2 | Bucket4j | x/time/rate | -- | Polly rate limit | -- | sleep |

## API Testing

| Capability | TypeScript | Python | Java | Go | Ruby | C# | PHP | cURL |
|---|---|---|---|---|---|---|---|---|
| **Framework** | vitest 3.1 | pytest 8.4 | JUnit 5 | testing | RSpec 3.13 | xUnit 2.9 | PHPUnit 11 | bats |
| **HTTP Mocking** | msw 2.7 | respx 0.22 | WireMock 3.12 | httptest | WebMock 3.24 | WireMock.Net 1.6 | MockHandler | -- |
| **Contract** | pact-js | pact-python | pact-jvm | pact-go | pact-ruby | pact-net | -- | -- |

## Auth

| Capability | TypeScript | Python | Java | Go | Ruby | C# | PHP | cURL |
|---|---|---|---|---|---|---|---|---|
| **OAuth 2.0** | openid-client 6.4 | authlib 1.5 | Spring Security | x/oauth2 | OmniAuth 2.1 | MSAL | league/oauth2-client | manual |
| **JWT** | jose | PyJWT | nimbus-jose | golang-jwt | ruby-jwt | System.IdentityModel | firebase/jwt | manual |
