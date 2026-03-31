# API Client Testing Patterns

## Test Pyramid

```
         ╱╲
        ╱  ╲        Contract Tests (few)
       ╱────╲       API schema validation, backward compat
      ╱      ╲
     ╱  Integ  ╲    Integration Tests (some)
    ╱────────────╲   Real HTTP to staging/sandbox
   ╱              ╲
  ╱   Unit Tests   ╲  Unit Tests (many)
 ╱────────────────────╲ Mocked HTTP, logic validation
```

## Mock Strategies

### 1. Response Recording (Golden Files)

Record real API responses, replay in tests:
- Captures realistic payloads including edge cases
- Requires periodic refresh as APIs evolve
- Good for regression testing

### 2. Schema-Based Mocking

Generate mock responses from OpenAPI spec:
- Always matches the declared contract
- Catches drift between spec and implementation
- Good for new endpoint development

### 3. Claude-Generated Test Cases

Use Claude to analyze the API spec and generate:
- Happy path test cases
- Edge cases (empty responses, max pagination, unicode)
- Error scenarios (auth failure, rate limit, server error)
- Adversarial inputs (SQL injection, XSS in parameters)

## Contract Testing

Verify client expectations match server behavior:

```
Client Stub (expected)  ←→  Provider Contract (actual)
      │                           │
      └─── Compare schemas ───────┘
           Types match?
           Required fields present?
           Enum values valid?
```

## What to Test

| Category | Examples |
|----------|---------|
| **Serialization** | Request body encoding, response parsing, date formats |
| **Auth** | Token refresh, expired token retry, invalid credentials |
| **Retry** | Backoff timing, max retries, non-retryable errors |
| **Rate Limiting** | Queue behavior, backpressure, 429 handling |
| **Pagination** | Cursor-based, offset, link-header following |
| **Errors** | Typed errors per status code, network failures, timeouts |
| **Idempotency** | Duplicate request handling, idempotency key generation |
