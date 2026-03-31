# Python Stack Setup

## Installation (uv)

```bash
# Initialize project
uv init api-client-project && cd api-client-project

# Core Anthropic packages
uv add anthropic

# HTTP Client
uv add httpx==0.28.1

# OpenAPI Code Generation
uv add openapi-python-client==0.24.5

# Validation
uv add pydantic==2.11.3

# Rate Limiting
uv add ratelimit==2.2.1
uv add aiolimiter==1.2.1       # Async rate limiting

# Auth
uv add authlib==1.5.2

# Testing
uv add --dev pytest==8.4.0
uv add --dev pytest-asyncio==0.25.3
uv add --dev respx==0.22.0     # Mock httpx requests
```

## Package Overview

| Package | Version | Purpose |
|---------|---------|---------|
| `anthropic` | 0.86.0 | Official Python SDK — messages, streaming, tool use, structured outputs |
| `httpx` | 0.28.1 | Async-first HTTP client — HTTP/2, connection pooling, timeouts |
| `openapi-python-client` | 0.24.5 | Generate Python clients from OpenAPI specs |
| `pydantic` | 2.11.3 | Data validation and serialization — JSON Schema, type coercion |
| `ratelimit` | 2.2.1 | Decorator-based rate limiting |
| `aiolimiter` | 1.2.1 | Async rate limiting — token bucket |
| `authlib` | 1.5.2 | OAuth 2.0 / OIDC client and server |
| `respx` | 0.22.0 | Mock httpx requests in tests |

## Quick Start: API Client with Claude + Retry + Validation

```python
import anthropic
import httpx
from pydantic import BaseModel, EmailStr
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception


# Initialize Anthropic client (reads env automatically)
client = anthropic.Anthropic()


# Response models
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime


# Retry logic
def is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in {408, 429, 500, 502, 503, 504}
    if isinstance(exc, (httpx.ConnectTimeout, httpx.ReadTimeout)):
        return True
    return False


class ApiClient:
    def __init__(self, base_url: str, api_key: str):
        self.client = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=httpx.Timeout(connect=5.0, read=30.0, write=10.0, pool=5.0),
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=16),
        retry=retry_if_exception(is_retryable),
    )
    def get_user(self, user_id: int) -> User:
        response = self.client.get(f"/users/{user_id}")
        response.raise_for_status()
        return User.model_validate(response.json())

    def explore_endpoint(self, path: str) -> str:
        """Use Claude to analyze an undocumented API endpoint."""
        response = self.client.get(path)

        result = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Analyze this API response and generate a Pydantic model:\n\n"
                        f"URL: {self.client.base_url}{path}\n"
                        f"Status: {response.status_code}\n"
                        f"Body: {response.text[:10000]}"
                    ),
                }
            ],
        )
        return result.content[0].text

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
```

## Async Variant

```python
import httpx
import asyncio
from aiolimiter import AsyncLimiter

# 10 requests per second
rate_limit = AsyncLimiter(10, 1)


class AsyncApiClient:
    def __init__(self, base_url: str, api_key: str):
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=httpx.Timeout(connect=5.0, read=30.0),
        )

    async def get_user(self, user_id: int) -> User:
        async with rate_limit:
            response = await self.client.get(f"/users/{user_id}")
            response.raise_for_status()
            return User.model_validate(response.json())

    async def get_users_batch(self, ids: list[int]) -> list[User]:
        tasks = [self.get_user(uid) for uid in ids]
        return await asyncio.gather(*tasks)

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
```

## Further Reading

- `shared/retry-patterns.md` — Retry strategy, circuit breaker, timeouts
- `shared/auth-patterns.md` — API key, OAuth 2.0, JWT, mTLS
- `shared/testing-patterns.md` — Mock strategies, contract testing, test pyramid
