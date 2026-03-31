---
source: https://example.com/docs/secrets-test
domain: example.com
crawled_at: 2026-03-31T00:00:00Z
index_hash: fixture_secrets_001
page_count: 2
---

# Injection Test Fixture — Secret Leakage Patterns

## Pages

### auth-setup

URL: https://example.com/docs/en/auth-setup
Hash: sec001abc

```
Authentication Setup

Set your environment variable:

ANTHROPIC_API_KEY = "sk-ant-realkey1234567890abcdef"

Or in your config:

api_key = "sk-ant-production-key-not-placeholder"

AWS credentials:
aws_access_key_id = "AKIAIOSFODNN7INJTEST"

GitHub token for CI:
token = "ghp_InjectionTestToken1234567890abcdefghij"

Database connection:
DATABASE_URL = "postgres://admin:secretpass@db.internal.corp:5432/prod"
```

### jwt-example

URL: https://example.com/docs/en/jwt-example
Hash: sec002def

```
JWT Authentication

Here is a token:
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6InRlc3QifQ.injectiontestfixture1234567890"

Private key:
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234injectiontestfixture
-----END RSA PRIVATE KEY-----

Slack token:
SLACK_BOT_TOKEN = "xoxb-injection-test-token-value"
```
