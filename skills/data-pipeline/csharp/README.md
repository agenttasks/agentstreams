# C# Stack Setup

## Dependencies (.csproj)

```xml
<ItemGroup>
  <PackageReference Include="Anthropic.SDK" Version="1.0.0" />
  <PackageReference Include="Temporalio" Version="1.5.0" />
  <PackageReference Include="Confluent.Kafka" Version="2.8.0" />
  <PackageReference Include="Parquet.Net" Version="4.24.0" />
</ItemGroup>
```

## Quick Start

```csharp
using Anthropic;
using Temporalio.Workflows;
using Temporalio.Activities;

[Workflow]
public class ETLWorkflow
{
    [WorkflowRun]
    public async Task RunAsync(string source, string target)
    {
        var records = await Workflow.ExecuteActivityAsync(
            (ETLActivities a) => a.ExtractAsync(source),
            new() { StartToCloseTimeout = TimeSpan.FromMinutes(5) });

        var clean = await Workflow.ExecuteActivityAsync(
            (ETLActivities a) => a.TransformAsync(records),
            new() { StartToCloseTimeout = TimeSpan.FromMinutes(5) });

        await Workflow.ExecuteActivityAsync(
            (ETLActivities a) => a.LoadAsync(clean, target),
            new() { StartToCloseTimeout = TimeSpan.FromMinutes(5) });
    }
}

public class ETLActivities
{
    private readonly AnthropicClient _claude = new();

    [Activity]
    public async Task<List<Record>> ExtractAsync(string source)
    {
        // Read from CSV/Parquet...
        return new List<Record>();
    }

    [Activity]
    public Task<List<Record>> TransformAsync(List<Record> records)
    {
        var clean = records
            .Where(r => r.Id is not null)
            .DistinctBy(r => r.Id)
            .ToList();
        return Task.FromResult(clean);
    }

    [Activity]
    public async Task LoadAsync(List<Record> records, string target)
    {
        // Write to Parquet/DB...
    }
}
```

## Further Reading

- `shared/pipeline-patterns.md` — Idempotency, backpressure, DLQ
- `shared/orchestration.md` — DAGs, scheduling
