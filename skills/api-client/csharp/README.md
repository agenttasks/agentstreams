# C# Stack Setup

## Dependencies (.csproj)

```xml
<ItemGroup>
  <PackageReference Include="Anthropic.SDK" Version="1.0.0" />
  <PackageReference Include="RestSharp" Version="112.1.0" />
  <PackageReference Include="Polly" Version="8.5.0" />
  <PackageReference Include="FluentValidation" Version="11.11.0" />
  <PackageReference Include="NSwag.MSBuild" Version="14.2.0" />
</ItemGroup>
<ItemGroup Condition="'$(Configuration)' == 'Debug'">
  <PackageReference Include="WireMock.Net" Version="1.6.0" />
  <PackageReference Include="xunit" Version="2.9.0" />
</ItemGroup>
```

## Quick Start

```csharp
using System.Net;
using Polly;
using Polly.Retry;
using RestSharp;

public class ApiClient : IDisposable
{
    private readonly RestClient _http;
    private readonly AnthropicClient _claude;
    private readonly ResiliencePipeline<RestResponse> _retry;

    public ApiClient(string baseUrl, string apiKey)
    {
        _http = new RestClient(baseUrl, configureSerialization: s => s.UseSystemTextJson());
        _http.AddDefaultHeader("Authorization", $"Bearer {apiKey}");

        _claude = new AnthropicClient();

        _retry = new ResiliencePipelineBuilder<RestResponse>()
            .AddRetry(new RetryStrategyOptions<RestResponse>
            {
                MaxRetryAttempts = 3,
                BackoffType = DelayBackoffType.Exponential,
                Delay = TimeSpan.FromSeconds(1),
                ShouldHandle = new PredicateBuilder<RestResponse>()
                    .HandleResult(r => r.StatusCode is
                        HttpStatusCode.TooManyRequests or
                        HttpStatusCode.InternalServerError or
                        HttpStatusCode.BadGateway or
                        HttpStatusCode.ServiceUnavailable or
                        HttpStatusCode.GatewayTimeout)
            })
            .Build();
    }

    public async Task<User> GetUserAsync(int id)
    {
        var request = new RestRequest($"/users/{id}");
        var response = await _retry.ExecuteAsync(
            async ct => await _http.ExecuteAsync<User>(request, ct));
        return response.Data!;
    }

    public void Dispose() => _http.Dispose();
}
```

## Further Reading

- `shared/retry-patterns.md` — Retry strategy, circuit breaker, timeouts
- `shared/auth-patterns.md` — API key, OAuth 2.0, JWT, mTLS
