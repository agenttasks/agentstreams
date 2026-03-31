# Java Stack Setup

## Dependencies (Gradle Kotlin DSL)

```kotlin
dependencies {
    implementation("com.anthropic:anthropic-java:1.5.0")
    implementation("io.temporal:temporal-sdk:1.27.0")
    implementation("org.apache.kafka:kafka-clients:3.9.0")
    implementation("org.apache.spark:spark-sql_2.13:3.5.4")
    implementation("org.apache.parquet:parquet-hadoop:1.14.4")
    testImplementation("org.junit.jupiter:junit-jupiter:5.11.0")
}
```

## Package Overview

| Package | Purpose |
|---------|---------|
| `anthropic-java` | Official Java SDK |
| `temporal-sdk` | Durable workflow orchestration |
| `kafka-clients` | Kafka producer/consumer |
| `spark-sql` | Distributed data processing |
| `parquet-hadoop` | Parquet read/write |

## Quick Start

```java
import com.anthropic.AnthropicClient;
import io.temporal.workflow.WorkflowInterface;
import io.temporal.workflow.WorkflowMethod;
import io.temporal.activity.ActivityInterface;
import io.temporal.activity.ActivityMethod;

@WorkflowInterface
public interface ETLWorkflow {
    @WorkflowMethod
    void run(String source, String target);
}

@ActivityInterface
public interface ETLActivities {
    @ActivityMethod
    List<Record> extract(String source);

    @ActivityMethod
    List<Record> transform(List<Record> records);

    @ActivityMethod
    void load(List<Record> records, String target);
}

public class ETLActivitiesImpl implements ETLActivities {
    private final AnthropicClient claude = AnthropicClient.builder().build();

    @Override
    public List<Record> extract(String source) {
        // Read CSV/Parquet...
        return List.of();
    }

    @Override
    public List<Record> transform(List<Record> records) {
        return records.stream()
            .filter(r -> r.id() != null)
            .distinct()
            .toList();
    }

    @Override
    public void load(List<Record> records, String target) {
        // Write to Parquet/DB...
    }
}
```

## Further Reading

- `shared/pipeline-patterns.md` — Idempotency, backpressure, DLQ
- `shared/orchestration.md` — DAGs, scheduling, Temporal patterns
