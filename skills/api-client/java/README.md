# Java Stack Setup

## Dependencies (Gradle Kotlin DSL)

```kotlin
dependencies {
    implementation("com.anthropic:anthropic-java:1.5.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("com.squareup.retrofit2:retrofit:2.11.0")
    implementation("com.squareup.retrofit2:converter-jackson:2.11.0")
    implementation("io.github.resilience4j:resilience4j-retry:2.2.0")
    implementation("io.github.resilience4j:resilience4j-ratelimiter:2.2.0")
    implementation("io.github.resilience4j:resilience4j-circuitbreaker:2.2.0")
    testImplementation("org.wiremock:wiremock:3.12.0")
    testImplementation("org.junit.jupiter:junit-jupiter:5.11.0")
}
```

## Package Overview

| Package | Purpose |
|---------|---------|
| `anthropic-java` | Official Java SDK — messages, streaming, tool use |
| `okhttp` | HTTP client — connection pooling, interceptors |
| `retrofit` | Type-safe REST client from interface annotations |
| `resilience4j` | Retry, rate limiting, circuit breaker |
| `wiremock` | HTTP mock server for testing |

## Quick Start

```java
import com.anthropic.AnthropicClient;
import io.github.resilience4j.retry.Retry;
import io.github.resilience4j.retry.RetryConfig;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import java.time.Duration;

public class ApiClient {
    private final OkHttpClient http;
    private final AnthropicClient claude;
    private final Retry retry;

    public ApiClient(String baseUrl, String apiKey) {
        this.http = new OkHttpClient.Builder()
            .connectTimeout(Duration.ofSeconds(5))
            .readTimeout(Duration.ofSeconds(30))
            .addInterceptor(chain -> chain.proceed(
                chain.request().newBuilder()
                    .header("Authorization", "Bearer " + apiKey)
                    .build()))
            .build();

        this.claude = AnthropicClient.builder().build();

        this.retry = Retry.of("api", RetryConfig.custom()
            .maxAttempts(3)
            .waitDuration(Duration.ofSeconds(1))
            .exponentialBackoffMultiplier(2.0)
            .retryOnResult(r -> {
                Response resp = (Response) r;
                int code = resp.code();
                return code == 429 || code >= 500;
            })
            .build());
    }
}
```

## Further Reading

- `shared/retry-patterns.md` — Retry strategy, circuit breaker, timeouts
- `shared/auth-patterns.md` — API key, OAuth 2.0, JWT, mTLS
- `shared/testing-patterns.md` — Mock strategies, contract testing
