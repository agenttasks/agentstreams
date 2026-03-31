# Go Stack Setup

## Installation

```bash
go mod init api-client
go get github.com/anthropics/anthropic-sdk-go
go get github.com/go-resty/resty/v2
go get github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@latest
go get golang.org/x/oauth2
go get golang.org/x/time/rate
go get github.com/go-playground/validator/v10
```

## Package Overview

| Package | Purpose |
|---------|---------|
| `anthropic-sdk-go` | Official Go SDK — messages, streaming, tool use |
| `resty/v2` | HTTP client — retry, middleware, auth |
| `oapi-codegen` | Generate Go client/server from OpenAPI |
| `x/oauth2` | OAuth 2.0 client |
| `x/time/rate` | Token bucket rate limiter |
| `validator/v10` | Struct validation with tags |

## Quick Start

```go
package main

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/go-resty/resty/v2"
	"golang.org/x/time/rate"
)

type User struct {
	ID        int       `json:"id" validate:"required"`
	Name      string    `json:"name" validate:"required"`
	Email     string    `json:"email" validate:"required,email"`
	CreatedAt time.Time `json:"created_at"`
}

type APIClient struct {
	http    *resty.Client
	limiter *rate.Limiter
	claude  anthropic.Client
}

func NewAPIClient(baseURL, apiKey string) *APIClient {
	client := resty.New().
		SetBaseURL(baseURL).
		SetAuthToken(apiKey).
		SetTimeout(30 * time.Second).
		SetRetryCount(3).
		SetRetryWaitTime(1 * time.Second).
		SetRetryMaxWaitTime(16 * time.Second).
		AddRetryCondition(func(r *resty.Response, err error) bool {
			if err != nil {
				return true
			}
			code := r.StatusCode()
			return code == 429 || code >= 500
		})

	return &APIClient{
		http:    client,
		limiter: rate.NewLimiter(rate.Every(100*time.Millisecond), 10),
		claude:  anthropic.NewClient(),
	}
}

func (c *APIClient) GetUser(ctx context.Context, id int) (*User, error) {
	if err := c.limiter.Wait(ctx); err != nil {
		return nil, err
	}
	var user User
	resp, err := c.http.R().
		SetContext(ctx).
		SetResult(&user).
		Get(fmt.Sprintf("/users/%d", id))
	if err != nil {
		return nil, err
	}
	if resp.StatusCode() != http.StatusOK {
		return nil, fmt.Errorf("unexpected status: %d", resp.StatusCode())
	}
	return &user, nil
}
```

## Further Reading

- `shared/retry-patterns.md` — Retry strategy, circuit breaker, timeouts
- `shared/auth-patterns.md` — API key, OAuth 2.0, JWT, mTLS
- `shared/testing-patterns.md` — Mock strategies, contract testing
