# Go Stack Setup

## Installation

```bash
go mod init data-pipeline
go get github.com/anthropics/anthropic-sdk-go
go get go.temporal.io/sdk
go get github.com/confluentinc/confluent-kafka-go/v2/kafka
go get github.com/apache/arrow-go/v18/arrow
go get github.com/parquet-go/parquet-go
```

## Package Overview

| Package | Purpose |
|---------|---------|
| `anthropic-sdk-go` | Official Go SDK |
| `temporal-sdk` | Durable workflow orchestration |
| `confluent-kafka-go` | Kafka producer/consumer |
| `arrow-go` | Apache Arrow columnar format |
| `parquet-go` | Parquet read/write |

## Quick Start

```go
package main

import (
	"context"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
	"go.temporal.io/sdk/activity"
	"go.temporal.io/sdk/workflow"
)

type Record struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	Description string `json:"description"`
	Category    string `json:"category,omitempty"`
}

func ExtractActivity(ctx context.Context, source string) ([]Record, error) {
	activity.GetLogger(ctx).Info("Extracting", "source", source)
	// Read from CSV/Parquet...
	return nil, nil
}

func TransformActivity(ctx context.Context, records []Record) ([]Record, error) {
	var clean []Record
	seen := make(map[string]bool)
	for _, r := range records {
		if r.ID == "" || seen[r.ID] {
			continue
		}
		seen[r.ID] = true
		clean = append(clean, r)
	}
	return clean, nil
}

func EnrichActivity(ctx context.Context, records []Record) ([]Record, error) {
	client := anthropic.NewClient()
	// Batch classify with Claude...
	_ = client
	return records, nil
}

func ETLWorkflow(ctx workflow.Context, source, target string) error {
	opts := workflow.ActivityOptions{StartToCloseTimeout: 5 * 60}
	ctx = workflow.WithActivityOptions(ctx, opts)

	var records []Record
	if err := workflow.ExecuteActivity(ctx, ExtractActivity, source).Get(ctx, &records); err != nil {
		return fmt.Errorf("extract: %w", err)
	}
	if err := workflow.ExecuteActivity(ctx, TransformActivity, records).Get(ctx, &records); err != nil {
		return fmt.Errorf("transform: %w", err)
	}
	return nil
}
```

## Further Reading

- `shared/pipeline-patterns.md` — Idempotency, backpressure, DLQ, data quality
- `shared/orchestration.md` — DAGs, scheduling, Temporal patterns
