# Authentication Patterns

## API Key

Simplest auth. Key passed in header, query param, or cookie.

### Header (Recommended)

```
Authorization: Bearer <api-key>
# or
X-API-Key: <api-key>
```

### Security Rules

- Never hardcode API keys in source code
- Use environment variables or secret managers
- Rotate keys on a schedule (90 days recommended)
- Use separate keys per environment (dev/staging/prod)

## OAuth 2.0

### Client Credentials (Machine-to-Machine)

```
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=<id>
&client_secret=<secret>
&scope=read:data write:data
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

### Token Refresh

```
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
&refresh_token=<token>
&client_id=<id>
```

### Token Lifecycle

1. **Acquire** token on first request or startup
2. **Cache** token until `expires_in - buffer` (60s buffer)
3. **Refresh** proactively before expiry
4. **Retry** with fresh token on 401

## JWT Bearer

For service accounts with pre-shared keys:

```
1. Create JWT payload: {iss, sub, aud, exp, iat}
2. Sign with private key (RS256 or ES256)
3. POST to token endpoint with assertion
4. Receive access_token
```

## mTLS (Mutual TLS)

For high-security APIs:

```
Client presents:
  - Client certificate (public)
  - Client private key

Server validates:
  - Client cert signed by trusted CA
  - Client cert not revoked
  - Client cert CN/SAN matches allowed list
```
