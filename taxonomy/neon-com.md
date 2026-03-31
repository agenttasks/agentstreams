---
source: https://neon.com/llms.txt
domain: neon.com
crawled_at: 2026-03-31T18:07:55Z
index_hash: 1d875803d8d0
page_count: 20
---

# neon.com — Documentation Taxonomy

Source: `https://neon.com/llms.txt`
Crawled: 2026-03-31T18:07:55Z

## Index

```
# Neon Postgres

> Neon is a serverless Postgres platform that separates compute and storage to offer autoscaling, branching, instant restore, and scale-to-zero. It's fully compatible with Postgres and works with any language, framework, or ORM that supports Postgres.

Neon docs are available as markdown. Append `.md` to any doc URL or set `Accept: text/markdown`. This is the primary index. Sections with many pages show key pages and link to full sub-indexes.

## Common Queries

- Pricing & Plans: https://neon.com/docs/introduction/plans.md
- Regions: https://neon.com/docs/introduction/regions.md
- API Reference: https://neon.com/docs/reference/api-reference.md

## Introduction

Architecture, features, autoscaling, branching concepts, billing, and plans.

All 33 pages: https://neon.com/docs/introduction/llms.txt — key pages below

- [Autoscaling](https://neon.com/docs/introduction/autoscaling.md): An introduction to Neon's autoscaling
- [Branching](https://neon.com/docs/introduction/branching.md): Branch your data the same way you branch your code
- [Neon Read Replicas](https://neon.com/docs/introduction/read-replicas.md): Scale your app, run ad-hoc queries, and provide read-only access without duplicating data
- [Neon's lakebase architecture](https://neon.com/docs/introduction/architecture-overview.md): Serverless Postgres with decoupled compute and durable storage
- [Plans and billing](https://neon.com/docs/introduction/about-billing.md): Learn about Neon's pricing plans and how to manage billing
- [Scale to Zero](https://neon.com/docs/introduction/scale-to-zero.md): Minimize costs by automatically scaling inactive databases to zero

## Get Started

First-time setup: org/project creation, connection strings, driver installation, optional auth, and initial schema setup.

- [Built to scale](https://neon.com/docs/get-started/built-to-scale.md): Neon supports you from prototype to scale-up
- [Connecting Neon to your stack](https://neon.com/docs/get-started/connect-neon.md): Learn how to integrate Neon into your application
- [Database branching workflow primer](https://neon.com/docs/get-started/workflow-primer.md): An introduction to integrating Postgres branching into your development workflow
- [Getting ready for production](https://neon.com/docs/get-started/production-checklist.md): Guidelines to optimize price, performance, and reliability
- [Learn the basics](https://neon.com/docs/get-started/signing-up.md): Sign up for free and learn the basics of database branching with Neon
- [Neon framework guides](https://neon.com/docs/get-started/frameworks.md): Find detailed instructions for connecting to Neon from various frameworks
- [Neon language guides](https://neon.com/docs/get-started/languages.md): Find detailed instructions for connecting to Neon from various languages
- [Neon ORM guides](https://neon.com/docs/get-started/orms.md): Find detailed instructions for connecting to Neon from various ORMs
- [Our DX Principles](https://neon.com/docs/get-started/dev-experience.md): Neon adapts to your workflow, not the other way around.
- [Query with Neon's SQL Editor](https://neon.com/docs/get-started/query-with-neon-sql-editor.md): Query your database from the Neon Console using the Neon SQL Editor
- [Why Neon?](https://neon.com/docs/get-started/why-neon.md): Serverless Postgres, by Databricks

## Connect

Drivers, connection strings, pooling, local dev tooling, and troubleshooting.

- [Choosing your connection method](https://neon.com/docs/connect/choose-connection.md): Find the right driver and connection type for your deployment platform
- [Connect a GUI application](https://neon.com/docs/connect/connect-postgres-gui.md): Learn how to connect a GUI application to Neon
- [Connect from any application](https://neon.com/docs/connect/connect-from-any-app.md): Learn how to connect to Neon from any application
- [Connect Looker Studio to Neon](https://neon.com/docs/connect/connect-looker-studio.md): Learn how to connect your Neon Postgres database to Looker Studio
- [Connect to Neon](https://neon.com/docs/connect/connect-intro.md): Everything you need to know about connecting to Neon
- [Connect to Neon securely](https://neon.com/docs/connect/connect-securely.md): Learn how to connect to Neon securely when using a connection string
- [Connect with pgcli](https://neon.com/docs/connect/connect-pgcli.md): Learn how to connect to Neon using the interactive pgcli client
- [Connect with psql](https://neon.com/docs/connect/query-with-psql-editor.md): Learn how to connect to Neon using psql
- [Connection errors](https://neon.com/docs/connect/connection-errors.md): Learn how to resolve connection errors
- [Connection latency and timeouts](https://neon.com/docs/connect/connection-latency.md): Learn about strategies to manage connection latencies and timeouts
- [Connection pooling](https://neon.com/docs/connect/connection-pooling.md): Learn how connection pooling works in Neon
- [Neon serverless driver](https://neon.com/docs/serverless/serverless-driver.md): Connect to Neon from serverless environments over HTTP or WebSockets
- [Passwordless auth](https://neon.com/docs/connect/passwordless-connect.md): Learn how to connect to Neon without a password

### Local Development

- [Neon Local](https://neon.com/docs/local/neon-local.md): Use Docker environments to connect to Neon and manage branches automatically
- [Neon VS Code Extension](https://neon.com/docs/local/vscode-extension.md): Connect to Neon and manage your database directly in VS Code, Cursor, and other editors

## Neon CLI

Install: `npm i -g neonctl`. Use this for terminal-first workflows, scripts, and CI/CD automation with `neonctl`.

- [Neon CLI command: auth](https://neon.com/docs/reference/cli-auth.md): Authenticate to Neon via browser or API key and manage credentials
- [Neon CLI command: branches](https://neon.com/docs/reference/cli-branches.md): List, create, rename, and delete branches; set default; run schema diff
- [Neon CLI command: completion](https://neon.com/docs/reference/cli-completion.md): Generate shell completion scripts for neonctl commands and options
- [Neon CLI command: connection-string](https://neon.com/docs/reference/cli-connection-string.md): Get Postgres connection strings for branches and databases
- [Neon CLI command: databases](https://neon.com/docs/reference/cli-databases.md): List, create, and delete databases in a Neon project
- [Neon CLI command: init](https://neon.com/docs/reference/cli-init.md): Initialize an app project with Neon, including auth, MCP server, extensions, and agent skills
- [Neon CLI command: ip-allow](https://neon.com/docs/reference/cli-ip-allow.md): Manage the IP allowlist: list, add, remove, and reset allowed IPs
- [Neon CLI command: me](https://neon.com/docs/reference/cli-me.md): View current user info, login details, and project limits
- [Neon CLI command: operations](https://neon.com/docs/reference/cli-operations.md): List and manage long-running operations for a Neon project
- [Neon CLI command: orgs](https://neon.com/docs/reference/cli-orgs.md): List and manage Neon organizations
- [Neon CLI command: projects](https://neon.com/docs/reference/cli-projects.md): List, create, update, delete, and get Neon projects
- [Neon CLI command: roles](https://neon.com/docs/reference/cli-roles.md): List, create, and delete database roles in a Neon project
- [Neon CLI command: set-context](https://neon.com/docs/reference/cli-set-context.md): Set default project context for CLI sessions to avoid repeating project ID
- [Neon CLI command: vpc](https://neon.com/docs/reference/cli-vpc.md): Manage Private Networking VPC endpoints and project-level restrictions
- [Neon CLI overview](https://neon.com/docs/reference/neon-cli.md): Overview of the Neon CLI: installation, commands, and options
- [Neon CLI quickstart](https://neon.com/docs/reference/cli-quickstart.md): Get set up with the Neon CLI in just a few steps
- [Neon CLI: Install and connect](https://neon.com/docs/reference/cli-install.md): Install the Neon CLI and connect with web auth or API key

## AI

Agent Skills, MCP integrations, vector search, and tools for building AI-powered applications with Neon.

- [Agent Skills](https://neon.com/docs/ai/agent-skills.md): Teach your AI coding assistant how to work with Neon
- [AI Concepts](https://neon.com/docs/ai/ai-concepts.md): Learn how embeddings are used to build AI applications
- [AI Starter Kit](https://neon.com/docs/ai/ai-intro.md): Resources for building AI applications with Neon Postgres
- [AI tools for Agents](https://neon.com/docs/ai/ai-agents-tools.md): AI-powered tools for development and database management
- [Azure Data Studio Notebooks](https://neon.com/docs/ai/ai-azure-notebooks.md): Use Azure Data Studio Notebooks with Neon for vector similarity search
- [Claude Code plugin for Neon](https://neon.com/docs/ai/ai-claude-code-plugin.md)
- [Connect MCP clients to Neon](https://neon.com/docs/ai/connect-mcp-clients-to-neon.md): Learn how to connect MCP clients such as Cursor, Claude Code, VS Code, ChatGPT, and other tools to your Neon Postgres database.
- [Cursor plugin for Neon](https://neon.com/docs/ai/ai-cursor-plugin.md)
- [Database versioning with snapshots](https://neon.com/docs/ai/ai-database-versioning.md): How AI agents and codegen platforms implement database version control using snapshots and preview branches
- [Google Colab](https://neon.com/docs/ai/ai-google-colab.md): Use Google Colab with Neon for vector similarity search
```

## Pages

### autoscaling.md

URL: https://neon.com/docs/introduction/autoscaling.md
Hash: 5ded9ffc261d

```
> This page location: Autoscaling > Overview
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Autoscaling

An introduction to Neon's autoscaling

Neon's _Autoscaling_ feature dynamically adjusts the amount of compute resources allocated to a Neon compute in response to the current load, eliminating the need for manual intervention or restarts.

The following visualization shows how Neon's autoscaling works throughout a typical day. The compute resources scale up or down based on demand, ensuring that your database has the necessary compute resources when it needs them, while conserving resources during off-peak times.

![visualization for autoscaling](https://neon.com/docs/introduction/autoscaling_intro.png)

To dive deeper into how Neon's autoscaling algorithm operates, visit [Understanding Neon's autoscaling algorithm](https://neon.com/docs/guides/autoscaling-algorithm).

## Autoscaling benefits

Neon's Autoscaling feature offers the following benefits:

- **On-demand scaling:** Autoscaling helps with workloads that experience variations over time, such as applications with time-based changes in demand or occasional spikes.
- **Cost-effectiveness**: Autoscaling optimizes resource utilization, ensuring that you only use required resources, rather than over-provisioning to handle peak loads.
- **Resource and cost control**: Autoscaling operates within a user-defined range, ensuring that your compute resources and associated costs do not scale indefinitely.
- **No manual intervention or restarts**: After you enable autoscaling and set scaling limits, no manual intervention or restarts are required, allowing you to focus on your applications.

## Configuring autoscaling

You can enable autoscaling for any compute instance, whether it's a primary compute or a read replica. Simply open the **Edit compute** drawer ([learn how](https://neon.com/docs/guides/autoscaling-guide)) for your compute and set the autoscaling range. This range defines the minimum and maximum compute sizes within which your compute will automatically scale. For example, you might set the minimum to 2 CU (8 GB of RAM) and the maximum to 8 CU (32 GB of RAM). Your compute resources will dynamically adjust within these limits, never dropping below the minimum or exceeding the maximum, regardless of demand.

**Note:** The maximum permitted autoscaling range is 8 CU. This means the difference between your maximum and minimum compute size cannot exceed 8 CU.

We recommend regularly [monitoring](https://neon.com/docs/introduction/monitoring-page) your usage from the **Monitoring Dashboard** to determine if adjustments to this range are needed.

![autoscaling configuration](https://neon.com/docs/introduction/autoscaling_config.png)

For full details about enabling and configuring autoscaling, see [Enabling autoscaling](https://neon.com/docs/guides/autoscaling-guide).

---

## Related docs (Autoscaling)

- [Autoscaling architecture](https://neon.com/docs/introduction/autoscaling-architecture)
- [Autoscaling algorithm](https://neon.com/docs/guides/autoscaling-algorithm)
- [Configure autoscaling](https://neon.com/docs/guides/autoscaling-guide)
```

### branching.md

URL: https://neon.com/docs/introduction/branching.md
Hash: e99ff5f89082

```
> This page location: Branching > About branching
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Branching

Branch your data the same way you branch your code

With Neon, you can quickly branch your data for development, testing, and various other purposes, enabling you to improve developer productivity and optimize continuous integration and delivery (CI/CD) pipelines.

You can also rewind your data or create branches from the past to recover from mistakes or analyze historical states.

## What is a branch?

A branch is a copy-on-write clone of your data. You can create a branch from a current or past state. For example, you can create a branch that includes all data up to the current time or an earlier time.

**Tip: working with sensitive data?** Neon also supports schema-only branching. [Learn more](https://neon.com/docs/guides/branching-schema-only).

A branch is isolated from its originating data, so you are free to play around with it, modify it, or delete it when it's no longer needed. Changes to a branch are independent. A branch and its parent can share the same data but diverge at the point of branch creation. Writes to a branch are saved as a delta.

Creating a branch does not increase load on the parent branch or affect it in any way, which means you can create a branch without impacting the performance of your production database.

Each Neon project is created with a [root branch](https://neon.com/docs/reference/glossary#root-branch) called `main`. The first branch that you create is branched from the project's root branch. Subsequent branches can be branched from the root branch or from a previously created branch.

## Branching workflows

You can use Neon's branching feature in variety workflows.

### Development

You can create a branch of your production database that developers are free to play with and modify. By default, branches are created with all of the data that existed in the parent branch, eliminating the setup time required to deploy and maintain a development database.

![development environment branch](https://neon.com/docs/introduction/branching_dev_env.png)

The following video demonstrates creating a branch in the Neon Console. For step-by-step instructions, see [Create a branch](https://neon.com/docs/manage/branches#create-a-branch).

You can integrate branching into your development workflows and toolchains using the Neon CLI, API, or GitHub Actions. If you use Vercel, you can use the [Neon-managed Vercel integration](https://neon.com/docs/guides/neon-managed-vercel-integration) to create a branch for each preview deployment.

Refer to the following guides for instructions:

- [Branching with the Neon API](https://neon.com/docs/guides/branching-neon-api): Learn how to instantly create and manage branches with the Neon API
- [Branching with the Neon CLI](https://neon.com/docs/guides/branching-neon-cli): Learn how to instantly create and manage branches with the Neon CLI
- [Branching with GitHub Actions](https://neon.com/docs/guides/branching-github-actions): Automate branching with Neon's GitHub Actions for branching
- [The Neon-Managed Vercel Integration](https://neon.com/docs/guides/neon-managed-vercel-integration): Connect your Vercel project and create a branch for each preview deployment

### Testing

Testers can create branches for testing schema changes, validating new queries, or testing potentially destructive queries before deploying them to production. A branch is isolated from its parent branch but has all of the parent branch's data up to the point of branch creation, which eliminates the effort involved in hydrating a database. Tests can also run on separate branches in parallel, with each branch having dedicated compute resources.

![test environment branches](https://neon.com/docs/introduction/branching_test.png)

Refer to the following guide for instructions.

- [Branching: Testing queries](https://neon.com/docs/guides/branching-test-queries): Instantly create a branch to test queries before running them in production

### Temporary environments

Create branches with TTL by [setting an expiration date](https://neon.com/docs/guides/branch-expiration). Perfect for temporary development and testing environments that need automatic deletion.

Branches with expiration are particularly useful for:

- CI/CD pipeline testing environments
- Feature development with known lifespans
- Automated testing scenarios
- AI-driven development workflows

## Restore and recover data

If you lose data due to an unintended deletion or some other event, you can restore a branch to any point in its restore window to recover lost data. You can also create a new restore branch for historical analysis or any other reason.

![Recover from data loss using restore branching](https://neon.com/docs/introduction/branching_data_loss.png)

### Restore window

Neon retains a history of changes for your branches, enabling data recovery features. The restore window determines how far back you can restore data, with defaults of 6 hours on Free plan and 1 day on paid plans.

Increasing your restore window expands your data recovery options but also increases storage costs, as more history is retained. You can configure it up to 7 days on Launch or 30 days on Scale plans.

For complete information about the restore window, including how to configure it, plan limits, storage implications, and how it works, see [Restore window](https://neon.com/docs/introduction/restore-window).

Learn how to use these data recovery features:

- [Instant restore](https://neon.com/docs/guides/branch-restore): Restore a branch to an earlier point in its history
- [Reset from parent](https://neon.com/docs/guides/reset-from-parent): Reset a branch to match its parent
- [Time Travel queries](https://neon.com/docs/guides/time-travel-assist): Run SQL queries against your database's past state

---

## Related docs (Branching)

- [Get started with branching](https://neon.com/docs/guides/branching-intro)
- [Branching workflows](https://neon.com/docs/guides/branching-test-queries)
- [Branch archiving](https://neon.com/docs/guides/branch-archiving)
- [Branch expiration](https://neon.com/docs/guides/branch-expiration)
- [Schema-only branches](https://neon.com/docs/guides/branching-schema-only)
- [Reset from parent](https://neon.com/docs/guides/reset-from-parent)
```

### read-replicas.md

URL: https://neon.com/docs/introduction/read-replicas.md
Hash: 4a872ac7ccbd

```
> This page location: Read replicas > Overview
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Neon Read Replicas

Scale your app, run ad-hoc queries, and provide read-only access without duplicating data

Neon read replicas are independent computes designed to perform read operations on the same data as your primary read-write compute. Neon's read replicas do not replicate or duplicate data. Instead, read requests are served from the same storage, as shown in the diagram below. While your read-write queries are directed through your primary compute, read queries can be offloaded to one or more read replicas.

![read replica simple](https://neon.com/docs/introduction/read_replica_simple.png)

You can instantly create read replicas for any branch in your Neon project and configure the compute size allocated to each. Read replicas also support Neon's [Autoscaling](https://neon.com/docs/introduction/autoscaling) and [Scale to Zero](https://neon.com/docs/introduction/scale-to-zero) features, providing you with the same control over compute resources that you have with your primary compute.

## How are Neon read replicas different?

- **No additional storage is required**: With read replicas reading from the same source as your primary read-write compute, no additional storage is required to create a read replica. Data is neither duplicated nor replicated. Creating a read replica involves spinning up a read-only compute instance, which takes a few seconds.
- **You can create them almost instantly**: With no data replication required, you can create read replicas almost instantly.
- **They are cost-efficient**: With no additional storage or transfer of data, costs associated with storage and data transfer are avoided. Neon's read replicas also benefit from Neon's [Autoscaling](https://neon.com/docs/introduction/autoscaling) and [Scale to Zero](https://neon.com/docs/manage/computes#scale-to-zero-configuration) features, which allow you to manage compute usage.
- **They are instantly available**: You can allow read replicas to scale to zero when not in use without introducing lag. When a read replica starts up in response to a query, it is up to date with your primary read-write compute almost instantly.

## How do you create read replicas?

You can create read replicas using the Neon Console, [Neon CLI](https://neon.com/docs/reference/neon-cli), or [Neon API](https://api-docs.neon.tech/reference/getting-started-with-neon-api), providing the flexibility required to integrate read replicas into your workflow or CI/CD processes.

From the Neon Console, it's a simple **Add Read Replica** action on a branch.

**Note:** You can add read replicas to a branch as needed to accommodate your workload. The Free plan is limited to a maximum of 3 read replica computes per project.

![Create a read replica](https://neon.com/docs/introduction/create_read_replica.png)

From the CLI or API:

Tab: CLI

```bash
neon branches add-compute mybranch --type read_only
```

Tab: API

```bash
curl --request POST \
     --url https://console.neon.tech/api/v2/projects/late-bar-27572981/endpoints \
     --header 'Accept: application/json' \
     --header "Authorization: Bearer $NEON_API_KEY" \
     --header 'Content-Type: application/json' \
     --data '
{
  "endpoint": {
    "type": "read_only",
    "branch_id": "br-young-fire-15282225"
  }
}
' | jq
```

For more details and how to connect to a read replica, see [Create and manage Read Replicas](https://neon.com/docs/guides/read-replica-guide).

## Read Replica architecture

The following diagram shows how your primary compute and read replicas send read requests to the same Pageserver, which is the component of the [lakebase architecture](https://neon.com/docs/introduction/architecture-overview) that is responsible for serving read requests.

![read replica computes](https://neon.com/docs/introduction/read_replicas.png)

Neon read replicas are asynchronous, which means they are _eventually consistent_. As updates are made by your primary compute, Safekeepers store the data changes durably until they are processed by Pageservers. At the same time, Safekeepers keep read replica computes up to date with the most recent changes to maintain data consistency.

## Cross-region support

Neon only supports creating read replicas **in the same region** as your database. However, a cross-region replica setup can be achieved by creating a Neon project in a different region and replicating data to that project via [logical replication](https://neon.com/docs/guides/logical-replication-guide). For example, you can replicate data from a Neon project in a US region to a Neon project in a European region following our [Neon-to-Neon logical replication guide](https://neon.com/docs/guides/logical-replication-neon-to-neon). Read-only access to the replicated database can be managed at the application level.

## Use cases

Neon's read replicas have a number of applications:

- **Horizontal scaling**: Scale your application by distributing read requests across replicas to improve performance and increase throughput.
- **Analytics queries**: Offloading resource-intensive analytics and reporting workloads to reduce load on the primary compute.
- **Read-only access**: Granting read-only access to users or applications that don't require write permissions.

## Get started with read replicas

To get started with read replicas, refer to our guides:

- [Create and manage Read Replicas](https://neon.com/docs/guides/read-replica-guide): Learn how to create, connect to, configure, delete, and monitor read replicas
- [Scale your app with Read Replicas](https://neon.com/docs/guides/read-replica-integrations): Scale your app with read replicas using built-in framework support
- [Run analytics queries with Read Replicas](https://neon.com/docs/guides/read-replica-data-analysis): Leverage read replicas for running data-intensive analytics queries
- [Run ad-hoc queries with Read Replicas](https://neon.com/docs/guides/read-replica-adhoc-queries): Leverage read replicas for running ad-hoc queries
- [Provide read-only access with Read Replicas](https://neon.com/docs/guides/read-only-access-read-replicas): Leverage read replicas to provide read-only access to your data

---

## Related docs (Read replicas)

- [Create and manage](https://neon.com/docs/guides/read-replica-guide)
```

### architecture-overview.md

URL: https://neon.com/docs/introduction/architecture-overview.md
Hash: e1c14f1a03d8

```
> This page location: Architecture > Architecture overview
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Neon's lakebase architecture

Serverless Postgres with decoupled compute and durable storage

## Top level overview

Instead of running Postgres as a single stateful system tied to a VM and its filesystem, Neon is a serverless database that splits the system into two independent layers: compute and storage. These layers communicate over the network, with a stream of write-ahead log (WAL) records connecting them.

This separation is what puts Neon in the [lakebase category](https://www.databricks.com/blog/what-is-a-lakebase) of OLTP databases. Compute can scale up, scale down, go idle, and be restarted instantly without risking data loss or requiring data movement.

- **Ephemeral compute layer**: optimized for latency and execution. This layer runs Postgres, executing queries and transactions using RAM and local NVMe for performance. Compute nodes do not own durable state and can be replaced freely.
- **Durable storage layer**: optimized for correctness, history, and scale. This layer defines durability by replicating WAL via quorum, materializes Postgres pages on demand, and stores long-term, immutable history in object storage.

Neon's design intentionally keeps object storage off the critical path. Object storage provides durability and scale, but never sits in front of query execution. Latency-sensitive work stays close to compute, while durability and history are handled asynchronously and independently.

![Neon architecture overview](https://neon.com/docs/introduction/neon-architecture-overview.png)

**Note: What is the difference between Neon and Lakebase?** Both products share the same architectural foundation but Lakebase comes with additional features integrating it with the rest of the Databricks Data and AI platform. For a full comparison, see [Neon and Lakebase](https://neon.com/docs/introduction/neon-and-lakebase).

## Resource hierarchy

While the sections below describe Neon's physical architecture, the platform organizes resources into a logical hierarchy:

| Concept          | Description                                                           | Relationship              |
| ---------------- | --------------------------------------------------------------------- | ------------------------- |
| Organization     | Highest-level container for billing, users, and projects              | Contains Projects         |
| Project          | Primary container for all database resources for an application       | Contains Branches         |
| Branch           | Lightweight, copy-on-write clone of database state                    | Contains Databases, Roles |
| Compute Endpoint | Running PostgreSQL instance (CPU/RAM for queries)                     | Attached to a Branch      |
| Database         | Logical container for data (tables, schemas, views)                   | Exists within a Branch    |
| Role             | PostgreSQL role for authentication and authorization                  | Belongs to a Branch       |
| Operation        | Async action by the control plane (creating branch, starting compute) | Associated with Project   |

For details on each concept, see the [glossary](https://neon.com/docs/reference/glossary).

## Compute layer

The compute layer is where Postgres actually runs. Each Neon compute node is a standard Postgres instance: it parses SQL, plans queries, executes transactions, enforces MVCC, and manages locks and indexes. From the perspective of the query engine, nothing about Postgres itself is rewritten or replaced.

What is different in Neon is what the compute node is responsible for. **It exists to execute work, not to preserve data.** A compute node can start, stop, scale, or fail at any time without putting durability at risk.

### Components

A Neon compute node has access to fast, local resources:

- RAM - used for shared_buffers, session state, and hot data
- Local NVMe - used as a performance cache for data pages

Pages cached in RAM or NVMe avoid network round-trips and keep most reads at memory or microsecond-level latencies.

### How compute fits into the system

When a query runs, the compute node behaves as you would expect:

- SQL is parsed and planned
- Pages are accessed through the buffer manager
- Changes are applied in memory

The Neon difference appears when the system crosses the boundary between execution and durability. **Instead of flushing WAL to a local filesystem, the compute node streams WAL to the storage layer.** A transaction is considered committed once that WAL has been acknowledged by a quorum of safekeepers (more on this later). The compute node does not wait for data pages to be written to disk or object storage.

For reads, **the compute node always prefers local access.** It first looks in memory, then in the local NVMe cache. Only when a page is missing locally does the compute node request it from the pageserver, which reconstructs the correct page version and returns it over the network. At no point does the compute node read directly from object storage.

## Storage layer

If the compute layer is responsible for execution, the storage layer is responsible for correctness, durability, and history. **This layer exists independently of any single compute node and continues to operate even when computes come and go.**

Rather than exposing a traditional filesystem, the Neon storage layer is built around three distinct components, each with a well-defined role:

- Safekeepers: define correctness by replicating WAL
- The pageserver: turns WAL into queryable data pages
- Object storage: holds long-term, immutable history

### Safekeepers: defining correctness via WAL quorum

Safekeepers are responsible for one thing: **durable replication of WAL**. When a compute node generates WAL records, it streams them to multiple safekeepers. A transaction is considered committed once a quorum of safekeepers has acknowledged the WAL record [via the Paxos protocol](https://neon.com/blog/paxos).

This is a fundamental difference from how traditional Postgres works:

- Correctness in Neon is enforced through replication and consensus
- Commit latency depends on network RTT, not disk fsync
- No single machine defines the durable state of the database

### Pageserver: WAL ⇄ pages

The pageserver sits between WAL and data [pages](https://neon.com/docs/reference/glossary#page). Its job is to **materialize page versions** by combining previously materialized base pages and committed WAL records. It is the system's translation layer between the logical history of the database and the physical representation needed to run queries.

When a compute node needs a page at a specific [LSN (Log Sequence Number)](https://neon.com/docs/reference/glossary#lsn), it asks the pageserver. The pageserver checks whether it already has that version available. If not, it reconstructs the page by replaying WAL up to the requested LSN and returns the result. Materialized pages are later persisted into object storage asynchronously, building up the long-term history of the database.

Importantly, page materialization is not on the transaction's critical path. Commits do not wait for pages to be written or uploaded.

### Object storage: long-term, immutable history

Object storage is where Neon keeps the **durable history** of the database. This layer stores materialized page versions, historical snapshots of data, and immutable representations of past states. It is not a query engine, and it is never accessed directly by the compute layer. It backs the pageserver, not Postgres.

This distinction is critical for performance. Object storage is optimal for durability, scale, and cost, not latency. Reads from object storage may take hundreds of milliseconds, but in Neon, those reads happen only inside the pageserver when reconstructing pages, and never on the hot query path.

## Write path: committing a transaction in Neon

![Write path in Neon](https://neon.com/docs/introduction/neon-write-path.png)

When a transaction executes on a compute node:

1. **Postgres applies changes in memory.** Rows are updated in shared buffers, indexes are modified, and WAL records are generated as usual.
2. **WAL is streamed to the safekeepers.** Instead of flushing WAL to a local filesystem, the compute node sends WAL records over the network to multiple safekeepers.
3. **Commit is defined by quorum.** A transaction is considered committed once a quorum of safekeepers has acknowledged the WAL record. At this point, the client receives success.
4. **Page materialization happens later.** Page reconstruction and persistence happen asynchronously in the storage layer.

## Read path: serving data without object-store latency

![Read path in Neon](https://neon.com/docs/introduction/neon-read-path.png)

The obvious concern with running a database on object storage is latency, but Neon's architecture is designed specifically to avoid this. The most important thing to understand about reads in Neon is this: **queries do not read from object storage.** Object storage backs the system, but it is never on the hot query path.

### The preferred path: local first

When Postgres running on a compute node needs to read a page, it follows a preference order:

1. **RAM (shared buffers).** This is the fastest path, just like in traditional Postgres.
2. **Local NVMe cache.** If the page is not in memory, the compute node checks its local NVMe cache. Access here is still fast.

Only if the page is missing locally does the system involve the storage layer (next section).

### Cache miss: requesting a page from the pageserver

On a cache miss, the compute node requests the required page from the pageserver, specifying the page identifier and the logical point in time (LSN). The pageserver then:

1. Checks whether it already has the requested page version materialized
2. If not, loads a base page from object storage, replays WAL records up to the requested LSN and returns the reconstructed page to the compute node

Once returned, the page can be cached in RAM and NVMe, making subsequent reads fast. This reconstruction only happens if needed, and only for the pages actually accessed.

## Durability

Durability in Neon is not a single mechanism but a composition of responsibilities. No single component is responsible for everything, and no single machine defines the state of the database.

This layering is what allows Neon to tolerate failures intrinsically:

- If a compute node dies → queries stop, but data is safe. A new compute attaches immediately and continues from the same history.
- If a pageserver dies → no durable state is lost. Another pageserver can be deployed and it can reconstruct pages using WAL and object storage.
- If a safekeeper dies → another can be deployed, and WAL replication continues as long as quorum remains.
- Object storage is the last line of defense → it holds immutable page history and survives failures across entire failure domains.

## What this architecture enables

**This design turns traditionally heavy-weight database operations (which usually require copying large amounts of data) into simple metadata operations.** These include creating a new branch, restoring from a snapshot, spinning up a read replica, or attaching a new compute node. In Neon, these operations are fast because they operate on references to existing history, not on the data itself.

- **Serverless compute provisioning.** Because durable state lives outside the compute layer, compute endpoints can [automatically scale up and down according to load](https://neon.com/docs/introduction/autoscaling), or [scale to zero](https://neon.com/docs/introduction/scale-to-zero) entirely. When compute starts, it simply attaches to existing database history rather than reconstructing local state.
- **Copy-on-write branching.** When you create a [branch](https://neon.com/docs/introduction/branching) in Neon, the engine does not duplicate files or pages. Instead, the new branch points to an existing point in history and begins diverging from there using copy-on-write semantics. Only new or modified data consumes additional storage.
- **Instant restores.** Because the database's history is preserved as immutable page versions in object storage, [restoring the database](https://neon.com/docs/introduction/branch-restore) does not involve copying data back into place. Compute can reattach to a past point in history, and execution can resume from the restored state. This process is fast and predictable, even for multi-terabyte databases.
- **A unified foundation for OLTP and OLAP.** Once transactional data lives in object storage, it is no longer isolated from analytical or AI workloads. The same underlying history that supports an OLTP engine (Neon) can also support OLAP engines and AI systems. This is the principle behind the [lakebase architecture](https://www.databricks.com/product/lakebase).

## In short

Neon is a serverless Postgres engine that treats:

- compute as ephemeral and replaceable;
- storage as durable, replicated, and shared;
- WAL as the source of truth;
- and object storage as the foundation.

The result is a database architecture that scales, recovers, and evolves without being constrained by a single machine or filesystem. For developers, this means faster iteration, safer workflows, and infrastructure that adapts automatically as applications grow from early prototypes to large-scale production systems. This design also enables advanced lakebase architectures that unify transactional and analytical data platforms.

---

## Related docs (Architecture)

- [Compute lifecycle](https://neon.com/docs/introduction/compute-lifecycle)
- [Serverless](https://neon.com/docs/introduction/serverless)
```

### about-billing.md

URL: https://neon.com/docs/introduction/about-billing.md
Hash: e56408d5d55a

```
> This page location: Plans and billing
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Plans and billing

Learn about Neon's pricing plans and how to manage billing

## Neon plans

- [Plans](https://neon.com/docs/introduction/plans): Learn about Neon's usage-based pricing plans and what's included

## Manage billing

- [Manage billing](https://neon.com/docs/introduction/manage-billing): View and manage your monthly bill and learn how to change your plan
- [Monitor billing and usage](https://neon.com/docs/introduction/monitor-usage): Learn how to monitor billing and usage in Neon
- [Cost optimization](https://neon.com/docs/introduction/cost-optimization): Strategies to manage and reduce your Neon costs
- [Network transfer costs](https://neon.com/docs/introduction/network-transfer): Monitor and reduce network transfer costs

## Neon for Enterprise

- [Neon for the Enterprise](https://neon.com/enterprise): Find out how Enterprises are maximizing engineering efficiency with Neon

---

## Related docs (Plans and billing)

- [Plans](https://neon.com/docs/introduction/plans)
- [Agent plan](https://neon.com/docs/introduction/agent-plan)
- [Manage billing](https://neon.com/docs/introduction/manage-billing)
- [Monitor billing](https://neon.com/docs/introduction/monitor-usage)
- [Cost optimization](https://neon.com/docs/introduction/cost-optimization)
- [Network transfer costs](https://neon.com/docs/introduction/network-transfer)
- [AWS Marketplace](https://neon.com/docs/introduction/billing-aws-marketplace)
```

### scale-to-zero.md

URL: https://neon.com/docs/introduction/scale-to-zero.md
Hash: 22dc078e1462

```
> This page location: Scale to zero
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Scale to Zero

Minimize costs by automatically scaling inactive databases to zero

Neon's _Scale to Zero_ feature suspends the Neon compute that runs your Postgres database after a period of inactivity, which minimizes costs for databases that aren't always active, such as development or test environment databases, and even production databases that aren't used 24/7.

- When your database is inactive, it automatically scales to zero after 5 minutes. This means you pay only for active time instead of 24/7 compute usage. No manual intervention is required.
- Once you query the database again, it reactivates automatically within a few hundred milliseconds.

The diagram below illustrates the _Scale to Zero_ behavior alongside Neon's _Autoscaling_ feature. The compute usage line highlights an _inactive_ period, followed by a period where the compute is automatically suspended until it's accessed again.

![Compute metrics graph](https://neon.com/docs/introduction/compute-usage-graph.jpg)

Neon compute scales to zero after an _inactive_ period of 5 minutes. For Neon Free plan users, this setting is fixed. Paid plan users can disable the scale-to-zero setting to maintain an always-active compute.

**Note:** Scale to zero is only available for computes up to 16 CU in size. Computes larger than 16 CU remain always active to ensure best performance.

You can enable or disable the scale-to-zero setting by editing your compute settings. For detailed instructions, see [Configuring scale to zero for Neon computes](https://neon.com/docs/guides/scale-to-zero-guide).

[Logical replication](https://neon.com/docs/guides/logical-replication-guide) **from** Neon keeps compute active while subscribers are connected, so the database does not scale to zero. See [Logical replication in Neon](https://neon.com/docs/guides/logical-replication-neon#important-notices) for details.

---

## Related docs (Scale to zero)

- [Scale to zero guide](https://neon.com/docs/guides/scale-to-zero-guide)
```

### built-to-scale.md

URL: https://neon.com/docs/get-started/built-to-scale.md
Hash: a4644595131a

```
> This page location: Why Neon? > Built to scale
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Built to scale

Neon supports you from prototype to scale-up

Neon fits into every stage of growth, from the first side project to operating large fleets of production databases - without forcing you to rethink your database architecture along the way.

## Stage 1: Side projects

**Real hosted Postgres with zero costs**

When you're looking for a free plan to run Postgres, what you want is simplicity and enough room to build. Neon's Free plan abstracts most configuration work, delivers real-world performance, and gives you access to core Neon features like branching and autoscaling.

- You get a [Free Plan with real resources](https://neon.com/blog/why-so-many-projects-in-the-neon-free-plan), including up to 100 projects, compute endpoints with up to 2 CPUs, and 0.5 GB of storage per project - enough to build and test real applications
- You get a Postgres connection string in a second so you can start building right away
- [Scale to zero](https://neon.com/docs/introduction/scale-to-zero) ensures idle databases don't eat up your compute limits: only active time counts
- Standard Postgres compatibility means you can plug Neon into [any framework, ORM, or tool that speaks Postgres](https://neon.com/docs/get-started/frameworks)
- A [broad catalog of Postgres extensions](https://neon.com/docs/extensions/pg-extensions) unlocks a Postgres-for-everything workflow

## Stage 2: Startups

**Build an iterate fast**

As a project becomes a product, small teams need to ship quickly and support real users. Neon gives these teams a frictionless building experience without compromising on performance and reliability.

> **Production checklist**
>
> Before launching your product, go through this checklist to make sure your DB has the right configuration to support your end users.
>
> [View checklist](https://neon.com/docs/get-started/production-checklist)

- [Autoscaling](https://neon.com/docs/introduction/autoscaling) adapts automatically to unpredictable workloads: you don't have to plan capacity in advance
- [Branching](https://neon.com/branching) lets you spin up development, preview, and test environments instantly, matching the latest production state, without manual work
- [Out-of-the-box integrations](https://neon.com/docs/guides/integrations) with platforms like Vercel further simplify previews and deployments
- [API-first workflows](https://neon.com/docs/reference/api-reference) make it easy to automate almost all database operations
- AI-coding support via [MCP](https://neon.com/docs/ai/neon-mcp-server) and [Agent Skills](https://neon.com/docs/ai/agent-skills) allows tools like Cursor and Claude to fully interact with Neon
- [Instant restores](https://neon.com/docs/guides/backup-restore) lower the stakes for mistakes and accidents
- [Built-in connection pooling](https://neon.com/docs/connect/connection-pooling) takes care of growing connections in your serverless apps
- You get access to [compliance and security features](https://neon.com/blog/why-we-no-longer-lock-premium-features) without enterprise-only contracts

## Stage 3: Scale-ups and large fleets

**Frictionless operations at scale**

At this stage, teams need performance, reliability, isolation, and automation without ballooning costs or operational complexity. Neon's lakebase architecture is built to address their different requirements directly.

### Operational efficiency

- [On-demand storage](https://neon.com/storage#unique-benefits-derived-from-neons-implementation) grows as data demands it, without planning for capacity in advance and without the risk of full-disk errors
- [Built-in high availability](https://neon.com/docs/introduction/high-availability) is provided by default through storage redundancy, with data replicated across availability zones and cloud object storage
- [Backup and restore via snapshots](https://neon.com/docs/guides/backup-restore) allows you to recover multi-terabyte databases in seconds, without full data copies
- You can use [time travel and snapshot inspections](https://neon.com/blog/three-ways-to-use-your-snapshots) to review past database states for auditing, debugging, and incident analysis
- By [creating environments as copy-on-write branches](https://neon.com/blog/how-mindvalley-minimizes-time-to-launch-with-neon-branches), you avoid the management work and costs associated with running separate instances for development, staging, testing, or recovery
- [Programmatic lifecycle management](https://neon.com/blog/how-dispatch-speeds-up-development-with-neon-while-keeping-workloads-on-aurora) lets you create, reset, and delete large numbers of environments without eating up engineering time

### Multi-tenancy

- Neon's [database-per-tenant setup](https://neon.com/use-cases/database-per-tenant) gives each customer a dedicated Neon project, providing strong isolation, eliminating noisy neighbors, and ensuring consistent performance
- [API-first tenant management](https://neon.com/blog/provision-postgres-neon-api) enables programmatic provisioning, configuration, scaling, recovery, and deletion of tenant databases, making it practical for small teams to manage thousands of tenants

### Fleet management for platforms and agents

- Instant, API-driven database provisioning allows to deploy a full serverless Postgres backend as part of your [platform](https://neon.com/docs/guides/embedded-postgres) or [agent](https://neon.com/docs/guides/ai-agent-integration)
- The fully embedded database experience keeps Neon invisible to your end users, with no third-party logins or external configuration required as part of your product workflow
- [Scale to zero](https://neon.com/docs/introduction/scale-to-zero) keeps unit costs low when large numbers of generated apps are never used or only accessed sporadically
- A mature API exposes [fleet management and cost-control capabilities](https://neon.com/docs/guides/consumption-limits) including quotas, usage limits, and lifecycle operations
- You can build versioning, checkpoints, rollbacks, and time-travel workflows with minimal engineering effort via [snapshots](https://neon.com/blog/promoting-postgres-changes-safely-production)
- Built-in app platform services such as [Neon Auth](https://neon.com/docs/auth/overview) and our PostgREST-compatible [Data API](https://neon.com/docs/data-api/get-started) make it easy to to hook full-stack applications out of the box

> **Agent Plan**
>
> If you're building a full-stack agent platform, apply to our Agent Plan for special pricing, resource limits, and assistance. 
>
> [Check it out](https://neon.com/programs/agents)

---

## Related docs (Why Neon?)

- [Our mission](https://neon.com/docs/get-started/why-neon)
- [Developer experience](https://neon.com/docs/get-started/dev-experience)
```

### connect-neon.md

URL: https://neon.com/docs/get-started/connect-neon.md
Hash: 69580a81d973

```
> This page location: Start with Neon > 2 - Connect
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Connecting Neon to your stack

Learn how to integrate Neon into your application

Connecting to Neon works like any Postgres database. You use a standard connection string with your language or framework of choice. This guide shows you the essentials to get connected quickly.

## Get your connection string

From your Neon **Project Dashboard**, click the **Connect** button to open the **Connection Details** modal. Select your branch, database, and role. Your connection string appears automatically.

![Connection details modal](https://neon.com/docs/connect/connection_details.png)

The connection string includes everything you need to connect:

```text
postgresql://alex:AbC123dEf@ep-cool-darkness-a1b2c3d4.us-east-2.aws.neon.tech/dbname?sslmode=require
             ^    ^         ^                                                   ^
       role -|    |         |- hostname                                        |- database
                  |
                  |- password
```

**Note:** Neon supports both pooled and direct connections. Use a pooled connection string (with `-pooler` in the hostname) if your application creates many concurrent connections. See [Connection pooling](https://neon.com/docs/connect/connection-pooling) for details.

## Connect from your application

Use your connection string to connect from any application. Here are examples for various frameworks and languages:

Tab: Neon serverless driver

```javascript
// Works in Node.js, Next.js, serverless, and edge runtimes
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL);

const users = await sql`SELECT * FROM users`;
```

Tab: Next.js

```javascript
// Next.js example
import postgres from 'postgres';

let { PGHOST, PGDATABASE, PGUSER, PGPASSWORD } = process.env;

const conn = postgres({
  host: PGHOST,
  database: PGDATABASE,
  username: PGUSER,
  password: PGPASSWORD,
  port: 5432,
  ssl: 'require',
});

const users = await conn`SELECT * FROM users`;
```

Tab: Drizzle

```javascript
// Drizzle example with the Neon serverless driver
import { neon } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';

const sql = neon(process.env.DATABASE_URL);

const db = drizzle(sql);

const result = await db.select().from(...);
```

Tab: Prisma

```javascript
// Prisma example with the Neon serverless driver
import { neon } from '@neondatabase/serverless';
import { PrismaNeonHTTP } from '@prisma/adapter-neon';
import { PrismaClient } from '@prisma/client';

const sql = neon(process.env.DATABASE_URL);

const adapter = new PrismaNeonHTTP(sql);

const prisma = new PrismaClient({ adapter });
```

Tab: Python

```python
# Python example with psycopg2
import os
import psycopg2

# Load the environment variable
database_url = os.getenv('DATABASE_URL')

# Connect to the PostgreSQL database
conn = psycopg2.connect(database_url)

with conn.cursor() as cur:
    cur.execute("SELECT version()")
    print(cur.fetchone())

# Close the connection
conn.close()
```

Tab: Go

```go
// Go example
package main
import (
    "database/sql"
    "fmt"
    "log"
    "os"

    _ "github.com/lib/pq"
    "github.com/joho/godotenv"
)

func main() {
    err := godotenv.Load()
    if err != nil {
        log.Fatalf("Error loading .env file: %v", err)
    }

    connStr := os.Getenv("DATABASE_URL")
    if connStr == "" {
        panic("DATABASE_URL environment variable is not set")
    }

    db, err := sql.Open("postgres", connStr)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    var version string
    if err := db.QueryRow("select version()").Scan(&version); err != nil {
        panic(err)
    }
    fmt.Printf("version=%s\n", version)
}
```

Tab: .NET

```csharp
# .NET example

## Connection string
"Host=ep-cool-darkness-123456.us-east-2.aws.neon.tech;Database=dbname;Username=alex;Password=AbC123dEf"

## with SSL
"Host=ep-cool-darkness-123456.us-east-2.aws.neon.tech;Database=dbname;Username=alex;Password=AbC123dEf;SSL Mode=Require;Trust Server Certificate=true"

## Entity Framework (appsettings.json)
{
  ...
  "ConnectionStrings": {
    "DefaultConnection": "Host=ep-cool-darkness-123456.us-east-2.aws.neon.tech;Database=dbname;Username=alex;Password=AbC123dEf;SSL Mode=Require;Trust Server Certificate=true"
  },
  ...
}
```

Tab: Ruby

```ruby
# Ruby example
require 'pg'
require 'dotenv'

# Load environment variables from .env file
Dotenv.load

# Connect to the PostgreSQL database using the environment variable
conn = PG.connect(ENV['DATABASE_URL'])

# Execute a query
conn.exec("SELECT version()") do |result|
  result.each do |row|
    puts "Result = #{row['version']}"
  end
end

# Close the connection
conn.close
```

Tab: Rust

```rust
// Rust example
use postgres::Client;
use openssl::ssl::{SslConnector, SslMethod};
use postgres_openssl::MakeTlsConnector;
use std::error;
use std::env;
use dotenv::dotenv;

fn main() -> Result<(), Box<dyn error::Error>> {
    // Load environment variables from .env file
    dotenv().ok();

    // Get the connection string from the environment variable
    let conn_str = env::var("DATABASE_URL")?;

    let builder = SslConnector::builder(SslMethod::tls())?;
    let connector = MakeTlsConnector::new(builder.build());
    let mut client = Client::connect(&conn_str, connector)?;

    for row in client.query("select version()", &[])? {
        let ret: String = row.get(0);
        println!("Result = {}", ret);
    }
    Ok(())
}
```

Tab: psql

```bash
# psql example connection string
psql postgresql://username:password@hostname:5432/database?sslmode=require&channel_binding=require
```

Store your connection string in an environment variable (like `DATABASE_URL`) rather than hardcoding it in your application.

## Next steps

This covers the basics. For more connection options and detailed guidance:

- [Connect documentation](https://neon.com/docs/connect/connect-intro): Comprehensive guide to all connection methods, troubleshooting, and security
- [Framework guides](https://neon.com/docs/get-started/frameworks): Step-by-step guides for Next.js, Remix, Django, Rails, and more
- [Language guides](https://neon.com/docs/get-started/languages): Connection examples for JavaScript, Python, Go, Rust, and other languages
- [Serverless driver](https://neon.com/docs/serverless/serverless-driver): Connect from serverless and edge environments using HTTP or WebSockets

---

## Related docs (Start with Neon)

- [1 - Basics](https://neon.com/docs/get-started/signing-up)
- [3 - Branching](https://neon.com/docs/get-started/workflow-primer)
- [4 - Setup Neon Auth](https://neon.com/docs/auth/overview)
```

### workflow-primer.md

URL: https://neon.com/docs/get-started/workflow-primer.md
Hash: 550527d9e4f6

```
> This page location: Start with Neon > 3 - Branching
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Database branching workflow primer

An introduction to integrating Postgres branching into your development workflow

With Neon, you can work with your data just like you work with your code. The key is Neon's database [branching](https://neon.com/docs/guides/branching-intro) feature, which lets you instantly create branches of your data that you can include in your workflow, as many branches as you need.

Neon branches are:

- **Isolated**: changes made to a branch don't affect its parent.
- **Fast to create**: creating a branch takes ~1 second, regardless of the size of your database.
- **Ready to use**: branches will have the parent branch's schema and all its data (you can also include data up to a certain point in time). If you're working with sensitive data, Neon also supports a [schema-only branching](https://neon.com/docs/guides/branching-schema-only) option.

Every Neon branch has a unique Postgres connection string, so they're completely isolated from one another.

```bash
# Branch 1
postgresql://database_name_owner:AbC123dEf@ep-shiny-cell-a5y2zuu0.us-east-2.aws.neon.tech/dbname?sslmode=require&channel_binding=require

# Branch 2
postgresql://database_name_owner:AbC123dEf@ep-hidden-hall-a5x58cuv.us-east-2.aws.neon.tech/dbname?sslmode=require&channel_binding=require
```

You can create all of your branches from the default branch, or set up a dedicated branch that you use as a base. The first approach is simpler, while the second provides greater data isolation.

![database workflow A B](https://neon.com/docs/get-started/database_workflow_AB.jpg)

## Create branch methods

You can use either the Neon CLI or GitHub actions to incorporate branching into your workflow.

### Neon CLI

Using the [Neon CLI](https://neon.com/docs/reference/neon-cli), you can create branches without leaving your editor or automate branch creation in your CI/CD pipeline.

And here are the key CLI actions you can use:

```bash
# Create branch
neon branches create [options]

# Get Connection string
neon connection-string [branch] [options]

# Delete branch
neon branches delete <id|name> [options]
```

For more information, see:

- [Branching with the Neon CLI](https://neon.com/docs/guides/branching-neon-cli): Learn about branching with the Neon CLI
- [Neon CLI Reference](https://neon.com/docs/reference/neon-cli): Reference for all commands in the Neon CLI

### GitHub Actions

If you're using GitHub Actions for your CI workflows, Neon provides GitHub Actions for [creating](https://neon.com/docs/guides/branching-github-actions#create-branch-action), [deleting](https://neon.com/docs/guides/branching-github-actions#delete-branch-action), and [resetting](https://neon.com/docs/guides/branching-github-actions#reset-from-parent-action) branches, and there's also a [schema diff action](https://neon.com/docs/guides/branching-github-actions#schema-diff-action).

Tab: Create branch

Here is an example of what a create branch action might look like:

```yaml
name: Create Neon Branch with GitHub Actions Demo
run-name: Create a Neon Branch 🚀
jobs:
  Create-Neon-Branch:
    uses: neondatabase/create-branch-action@v5
    with:
      project_id: rapid-haze-373089
      parent_id: br-long-forest-224191
      branch_name: from_action_reusable
      api_key: {{ secrets.NEON_API_KEY }}
    id: create-branch
  - run: echo project_id ${{ steps.create-branch.outputs.project_id}}
  - run: echo branch_id ${{ steps.create-branch.outputs.branch_id}}
```

Tab: Delete branch

Here is an example of what a delete branch action might look like:

```yaml
name: Delete Neon Branch with GitHub Actions
run-name: Delete a Neon Branch 🚀
on:
  push:
    branches:
      - 'production'
jobs:
  delete-neon-branch:
    uses: neondatabase/delete-branch-action@v3
    with:
      project_id: rapid-haze-373089
      branch: br-long-forest-224191
      api_key: { { secrets.NEON_API_KEY } }
```

You can find these GitHub Actions here:

- [Create branch Action](https://github.com/neondatabase/create-branch-action): Create Neon Branch GitHub Action
- [Delete Branch Action](https://github.com/neondatabase/delete-branch-action): Delete Neon Branch GitHub Action
- [Reset Branch Action](https://github.com/neondatabase/reset-branch-action): Reset Neon Branch GitHub Action
- [Schema Diff Action](https://github.com/neondatabase/schema-diff-action): Neon Schema Diff GitHub Action

For more detailed documentation, see [Automate branching with GitHub Actions](https://neon.com/docs/guides/branching-github-actions).

## A branch for every environment

Here's how you can integrate Neon branching into your workflow:

### Development

You can create a Neon branch for every developer on your team. This ensures that every developer has an isolated environment that includes schemas and data. These branches are meant to be long-lived, so each developer can tailor their branch based on their needs. With Neon's [branch reset capability](https://neon.com/docs/manage/branches#reset-a-branch-from-parent), developers can refresh their branch with the latest schemas and data anytime they need. You can invite teammates to your organization so they have access to all your projects. See [Invite members](https://neon.com/docs/manage/orgs-manage#invite-members).

**Tip:**

To easily identify branches dedicated to development, we recommend prefixing the branch name with `dev/<developer-name>` or `dev/<feature-name>` if multiple developers collaborate on the same development branch.

Examples:

```bash
dev/alice             dev/new-onboarding
```

### Preview environments

Whenever you create a pull request, you can create a Neon branch for your preview deployment. This allows you to test your code changes and SQL migrations against production-like data.

**Tip:**

We recommend following this naming convention to identify these branches easily:

```bash
preview/pr-<pull_request_number>-<git_branch_name>
```

Example:

```bash
preview/pr-123-feat/new-login-screen
```

You can also automate branch creation for every preview. These example applications show how to create Neon branches with GitHub Actions for every preview environment.

- [Preview branches with Fly.io](https://github.com/neondatabase/preview-branches-with-fly): Sample project showing you how to create a branch for every Fly.io preview deployment
- [Preview branches with Vercel](https://github.com/neondatabase/preview-branches-with-vercel): Sample project showing you how to create a branch for every Vercel preview deployment

### Testing

When running automated tests that require a database, each test run can have its branch with its own compute resources. You can create a branch at the start of a test run and delete it at the end.

**Tip:**

We recommend following this naming convention to identify these branches easily:

```bash
test/<git_branch_name-test_run_name-commit_SHA-time_of_the_test_execution>
```

The time of the test execution can be an epoch UNIX timestamp (such as 1704305739). For example:

```bash
test/feat/new-login-loginPageFunctionality-1a2b3c4d-20240211T1530
```

You can create test branches from the same date and time or Log Sequence Number (LSN) for tests requiring static or deterministic data.

## Additional branching features

### Working with sensitive data

If you're working with sensitive data and need to avoid copying production data to development or test environments, Neon supports [schema-only branching](https://neon.com/docs/guides/branching-schema-only). This creates branches with only the database schema (tables, indexes, constraints) without any of the actual data, allowing you to populate branches with anonymized or synthetic data instead.

### Automatic branch cleanup

To prevent branch accumulation and manage resources effectively, you can set branches to automatically expire and be deleted after a specified time period. This is particularly useful for temporary environments like CI/CD test branches or time-limited preview deployments. See [Branch expiration](https://neon.com/docs/guides/branch-expiration) for details on configuring automatic branch deletion.

---

## Related docs (Start with Neon)

- [1 - Basics](https://neon.com/docs/get-started/signing-up)
- [2 - Connect](https://neon.com/docs/get-started/connect-neon)
- [4 - Setup Neon Auth](https://neon.com/docs/auth/overview)
```

### production-checklist.md

URL: https://neon.com/docs/get-started/production-checklist.md
Hash: 50e1e4065c29

```
> This page location: Neon platform > Operations & maintenance > Production checklist
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Getting ready for production

Guidelines to optimize price, performance, and reliability

## Production checklist

- [ ] [1. Use a paid plan for production workloads](https://neon.com/docs/get-started/production-checklist#use-a-paid-plan-for-production-workloads)
    Paid plans are usage-based, so your app won't stop or be limited as it grows. The Free plan includes compute hour limits, making it better suited for prototyping.
- [ ] [2. Choose a region close to your application](https://neon.com/docs/get-started/production-checklist#choose-a-region-close-to-your-application)
    Deploy your Neon project in the nearest available region to your application to minimize network latency.
- [ ] [3. Keep your production branch as the default](https://neon.com/docs/get-started/production-checklist#keep-your-production-branch-as-the-default)
    Your production branch should be a root branch set as the default to ensure compute availability, enable snapshots, and simplify billing.
- [ ] [4. Protect your production branch](https://neon.com/docs/get-started/production-checklist#protect-your-production-branch)
    Mark production branches as protected to prevent accidental resets or destructive operations.
- [ ] [5. Enable autoscaling and set appropriate limits](https://neon.com/docs/get-started/production-checklist#enable-autoscaling-and-set-appropriate-limits)
    Autoscaling lets your database handle traffic spikes automatically. Set limits that balance performance with cost.
- [ ] [6. Decide whether scale-to-zero is acceptable](https://neon.com/docs/get-started/production-checklist#decide-whether-scale-to-zero-is-acceptable)
    Scale-to-zero is great for development and bursty usage. For production, disable it if you need consistently low latency.
- [ ] [7. Test connection retries using the Neon API](https://neon.com/docs/get-started/production-checklist#test-connection-retries-using-the-neon-api)
    Brief disconnects can happen during scaling or maintenance. Verify your application reconnects automatically.
- [ ] [8. Set an appropriate restore window](https://neon.com/docs/get-started/production-checklist#set-an-appropriate-restore-window)
    Neon keeps 1 day of restore history by default on paid plans. Increasing this gives you more protection, with storage cost tradeoffs.
- [ ] [9. Consider snapshot schedules](https://neon.com/docs/get-started/production-checklist#consider-snapshot-schedules)
    Snapshot schedules provide consistent backups for point-in-time restore, independently of your restore window.
- [ ] [10. Test your restore workflow](https://neon.com/docs/get-started/production-checklist#test-your-restore-workflow)
    Plan whether you'll restore in place or from a snapshot, and how your application will switch if needed.
- [ ] [11. Clean up your branches regularly](https://neon.com/docs/get-started/production-checklist#clean-up-your-branches-regularly)
    Set branch expiration times and add cleanup logic to automated workflows to avoid unnecessary storage costs.
- [ ] [12. Use pooled connections where they make sense](https://neon.com/docs/get-started/production-checklist#use-pooled-connections-where-they-make-sense)
    Connection pooling improves concurrency for web and serverless apps, but may not be appropriate for migrations or long-running tasks.
- [ ] [13. Restrict access to production data](https://neon.com/docs/get-started/production-checklist#restrict-access-to-production-data)
    Limit database access to trusted sources using IP Allow to reduce the risk of unauthorized changes.
- [ ] [14. Install pg_stat_statements](https://neon.com/docs/get-started/production-checklist#install-pgstatstatements)
    Enable query performance monitoring to track execution times and frequency. This helps you troubleshoot performance issues independently.
- [ ] [15. Integrate with your existing observability stack](https://neon.com/docs/get-started/production-checklist#integrate-with-your-existing-observability-stack)
    Export Neon metrics to Datadog, Grafana, or any OTEL-compatible platform to monitor usage and capacity alongside your existing systems.

## Use a paid plan for production workloads

Neon's paid plans are fully usage-based, which means your database is never subject to fixed limits that can stop your application as traffic grows. You pay for the compute and storage you use each month, without minimums.

The Free plan is designed to support experimentation and prototyping and includes compute hour limits. It should be avoided for production workloads where uninterrupted availability matters.

If you need technical support beyond billing, the Scale plan includes priority support with access to Neon's support team.

Keep reading: [Neon plans](https://neon.com/docs/introduction/plans)

## Choose a region close to your application

Network latency is one of the most common contributors to database response time: even a well-tuned database will feel slow if it's geographically far from your application servers. When creating a Neon project, choose the region that is closest to where your application runs.

![Region selection](https://neon.com/docs/introduction/project_creation_regions.png)

Keep reading: [Neon regions](https://neon.com/docs/introduction/regions)

## Keep your production branch as the default root branch

Your production database should run on a [root branch](https://neon.com/docs/reference/glossary#root-branch) that is set as the project's [default branch](https://neon.com/docs/reference/glossary#default-branch). Neon projects are configured this way by default. Using a root branch enables [snapshots](https://neon.com/docs/guides/backup-restore), provides simpler billing (based on actual data size rather than accumulated changes), and prevents accidental deletion.

Keep reading: [Manage branches](https://neon.com/docs/manage/branches)

## Protect your production branch

Neon makes it easy to branch, reset, and restore databases. In production, that power should be paired with explicit safeguards. Branch protection helps ensure that powerful features like restore, reset, and snapshot operations are used deliberately when applied to production data. This is especially important in teams or automated environments.

![Protect branch button](https://neon.com/docs/guides/ip_allow_set_as_protected.png)

Keep reading: [Protected branches](https://neon.com/docs/guides/protected-branches)

## Enable autoscaling and set appropriate limits

Neon autoscaling automatically adjusts compute resources based on your workload, allowing your database to absorb traffic spikes without manual intervention. For production workloads:

- **Minimum compute size**: Set a minimum high enough so your working set (frequently accessed data) can be fully cached in memory. This is important because Neon's [Local File Cache (LFC)](https://neon.com/docs/reference/glossary#local-file-cache) allocation is tied to your compute size. When the compute scales down and the LFC shrinks, frequently accessed data may be evicted and need to be reloaded from storage, which impacts performance.

- **Maximum compute size**: Set a maximum that provides enough extra capacity for traffic spikes. The maximum also determines your available local disk space, which is used for things like temporary files, complex queries, [pg_repack](https://neon.com/docs/extensions/pg_repack), and replication.

A safe minimum combined with a sufficiently high maximum will give you the best performance while avoiding unnecessary baseline cost.

![Autoscaling control](https://neon.com/docs/get-started/autoscaling_control.png)

Keep reading:

- [How to size your compute](https://neon.com/docs/manage/computes#how-to-size-your-compute)
- [Autoscaling configuration](https://neon.com/docs/introduction/autoscaling#configuring-autoscaling)
- [Monitor working set size](https://neon.com/docs/introduction/monitoring-page#working-set-size)
- [How the autoscaling algorithm works](https://neon.com/docs/guides/autoscaling-algorithm)

## Decide whether scale-to-zero is acceptable

Scale-to-zero allows Neon to suspend compute after a period of inactivity. This is a highly effective way to save costs in development environments and workloads with intermittent usage. For production workloads, the decision depends on your latency requirements.

If occasional cold starts are acceptable for your application (for example, for internal tools), leaving scale-to-zero enabled will be the most cost-effective choice.

Consider disabling scale-to-zero if:

- Your application requires consistently low latency
- Cold-start delays are unacceptable for user-facing requests
- You rely on long-lived sessions or in-memory state

**Cache considerations**: When a compute suspends, the cache is cleared. After the compute restarts, rebuilding the cache can take some time and may temporarily degrade query performance. If your workload requires suspension but you want to minimize this impact, consider using the [pg_prewarm](https://neon.com/docs/extensions/pg_prewarm) extension to reload critical data into the cache on startup.

Keep reading: [Scale to zero configuration](https://neon.com/docs/guides/scale-to-zero-guide)

## Test connection retries using the Neon API

In a serverless architecture, brief connection interruptions can occur during scaling events or maintenance. Most database drivers and connection pools already implement retry logic for transient failures, but rather than assuming this works, you should test it.

Our recommended approach:

- Use the Neon API or Console to trigger a compute restart
- Observe how your application behaves during the restart
- Confirm that connections are re-established automatically without user-facing errors

```bash
curl --request POST \
     --url https://console.neon.tech/api/v2/projects/{project_id}/endpoints/{endpoint_id}/restart \
     --header 'accept: application/json' \
     --header 'authorization: Bearer $NEON_API_KEY'
```

Keep reading:

- [Restart a compute](https://neon.com/docs/manage/computes#restart-a-compute)
- [Build connection timeout handling into your application](https://neon.com/docs/connect/connection-latency#build-connection-timeout-handling-into-your-application)
- [Maintenance and updates overview](https://neon.com/docs/manage/maintenance-updates-overview)

## Set an appropriate restore window

Neon retains a history of changes for each project to support branching and instant restores. On paid plans, the default restore window is 1 day, which you can increase up to 30 days.

Increasing the restore window gives you more flexibility to recover from bugs discovered later or accidental data loss. However, longer restore windows retain more historical data, which contributes to storage usage. Choose a window that balances recovery needs with predictable storage costs.

Keep reading: [Storage and billing for restores](https://neon.com/docs/introduction/restore-window#storage-and-billing)

## Consider snapshot schedules

Snapshot schedules provide regular, durable restore points taken daily, weekly, or monthly. While [point-in-time restore](https://neon.com/docs/introduction/branch-restore) lets you roll back to any moment within the restore window, snapshots capture stable points in time that you can return to later, ensuring that recovery points exist even if they fall outside your chosen restore window.

Snapshot schedules are only available on [root branches](https://neon.com/docs/manage/branches#root-branch).

![Snapshot schedule](https://neon.com/docs/guides/backup_restore_ui.png)

Keep reading: [Snapshot schedules](https://neon.com/docs/guides/backup-restore#create-backup-schedules)

## Test your restore workflow

Don't wait for an incident to learn how restore works. Plan and test your recovery process in advance.

Neon supports multiple restore patterns:

- [Instant branch restores](https://neon.com/docs/guides/backup-restore#instantly-restore-a-branch), where the existing branch is restored to a previous state
- [Restore from a snapshot into the same branch](https://neon.com/docs/guides/backup-restore#one-step-restore)
- [Restore from a snapshot into a new branch](https://neon.com/docs/guides/backup-restore#multi-step-restore)

Plan and test which restore method you will use for production incidents, how your application will switch connections if a new branch is created, and how you will validate restored data before resuming traffic.

## Clean up your branches regularly

Neon's branching makes it easy to create preview, test, and temporary environments. Over time, unused branches can accumulate and contribute to unnecessary storage usage. To keep costs and complexity under control:

- Set expiration times for preview and test branches
- Add explicit delete steps to automated branching workflows
- Periodically review and remove branches that are no longer in use

Keep reading:

- [Branch expiration](https://neon.com/docs/guides/branch-expiration)
- [Automate branching with GitHub Actions](https://neon.com/docs/guides/branching-github-actions)
- [Plans and billing](https://neon.com/docs/introduction/plans)

## Use pooled connections where they make sense

Connection pooling increases the number of concurrent clients your database can serve (up to 10,000) by reusing a smaller number of backend connections. This reduces connection overhead and improves performance in web and serverless applications.

However, pooled connections are not appropriate for all workloads. Avoid them for:

- Long-running database migrations
- Workloads that rely on session-level state
- Administrative tasks that require persistent connections (for example, `pg_dump`)
- Logical replication (CDC tools like Fivetran, Airbyte)

Keep reading: [Connection pooling](https://neon.com/docs/connect/connection-pooling)

## Restrict access to production data

Neon's IP Allow feature ensures that only trusted IP addresses can connect to your database, preventing unauthorized access and enhancing security. Combine an allowlist with protected branches for enhanced security.

![IP Allow settings](https://neon.com/docs/get-started/ip_allow_settings.png)

Keep reading: [IP Allow](https://neon.com/docs/introduction/ip-allow)

## Install pg_stat_statements

The [pg_stat_statements extension](https://neon.com/docs/extensions/pg_stat_statements) provides query performance monitoring to track execution times and frequency. Since Neon doesn't log queries and has limited visibility into query performance, this extension helps you troubleshoot issues independently.

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

The statistics gathered by this extension require little overhead and let you quickly access metrics like:

- [Most frequently executed queries](https://neon.com/docs/postgresql/query-performance#most-frequently-executed-queries)
- [Longest running queries](https://neon.com/docs/postgresql/query-performance#long-running-queries)
- [Queries that return the most rows](https://neon.com/docs/postgresql/query-performance#queries-that-return-the-most-rows)

You can also use the **Monitoring Dashboard** in the Neon Console to view live graphs for system and database metrics like CPU, RAM, and connections.

![Monitoring page connections graph](https://neon.com/docs/introduction/monitor_connections.png)

Keep reading:

- [Query performance](https://neon.com/docs/postgresql/query-performance)
- [Monitoring](https://neon.com/docs/introduction/monitoring)

## Integrate with your existing observability stack

If you already operate an observability platform, you can export Neon metrics and logs to monitor database behavior alongside the rest of your system. This helps you:

- Track connection counts and usage patterns
- Monitor compute and storage growth over time
- Correlate database behavior with application-level events

You can export to any OTLP-compatible platform, Datadog, or Grafana Cloud.

Keep reading:

- [OpenTelemetry export guide](https://neon.com/docs/guides/opentelemetry)
- [Datadog export guide](https://neon.com/docs/guides/datadog)
- [Grafana Cloud export guide](https://neon.com/docs/guides/grafana-cloud)

---

## Related docs (Operations & maintenance)

- [Backup & restore](https://neon.com/docs/manage/backups)
- [Updates](https://neon.com/docs/manage/updates)
- [Regions](https://neon.com/docs/introduction/regions)
```

### signing-up.md

URL: https://neon.com/docs/get-started/signing-up.md
Hash: 8eb8a5acbe1f

```
> This page location: Start with Neon > 1 - Basics
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Learn the basics

Sign up for free and learn the basics of database branching with Neon

**What you will learn:**

- How to view and modify data in the console
- Create an isolated database copy per developer
- Reset your branch to production when ready to start new work

**Related topics**

- [About branching](https://neon.com/docs/introduction/branching)
- [Branching workflows](https://neon.com/docs/get-started/workflow-primer)
- [Connect Neon to your stack](https://neon.com/docs/get-started/connect-neon)

This tutorial walks you through your first steps using Neon as your Postgres database. You'll explore the Neon object hierarchy and learn how database branching can simplify your development workflow.

## About branching

Each [branch](https://neon.com/docs/introduction/branching) is a fully-isolated copy of its parent. We suggest creating a long-term branch for each developer on your team to maintain consistent connection strings. You can reset your development branch to production whenever needed.

After signing up, you'll start with a `production` branch:

- `production` is your project's root default branch (default: 0.25-2 CU, adjustable up to 56 CU)

You can create additional branches for development, staging, and other environments. For development branches, consider using a smaller compute size (0.25-1 CU) to optimize costs, while keeping production appropriately sized for your workload.

## Sign up

If you're already signed up, you can skip ahead to [Step 2](https://neon.com/docs/get-started/signing-up#step-2-onboarding-in-the-neon-console).

If you haven't signed up yet, you can sign up for free here:

[https://console.neon.tech/signup](https://console.neon.tech/signup)

Sign up with your email, GitHub, Google, or other partner account.

For information about what's included with the Free and paid plans, see
[Neon plans](https://neon.com/docs/introduction/plans).

![sign\_up](https://neon.com/docs/get-started/sign_up_reduced.png "no-border")

## Onboarding in the Neon Console

After you sign up, you are guided through some onboarding steps that ask you to create a **Project**.

![onboarding](https://neon.com/docs/get-started/onboarding.png)

The steps should be self-explanatory, but it's important to understand a few key points:

- **In Neon, everything starts with the _Project_**

  It is the top-level container that holds your branches, databases, and roles. Typically, you should create a project for each repository in your application. This allows you to manage your database branches just like you manage your code branches: a branch for production, staging, development, new features, previews, and so forth.

- **We create a production branch for you**
  - `production` is the root default branch. It hosts your database, role, and a compute that you can connect your application to
  - You can create additional branches for development, staging, previews, and other workflows as needed

At this point, if you want to just get started connecting Neon to your toolchain, go to [Connecting Neon to your tools](https://neon.com/docs/get-started/connect-neon). Or if you want a more detailed walkthrough of some of our key console and branching features, let's keep going.

**Tip: Working with a team?** Your organization is now set up. You can start inviting teammates immediately. See [Invite members](https://neon.com/docs/manage/orgs-manage#invite-members).

## Add sample data

Let's get familiar with the **SQL Editor**, where you can run queries against your databases directly from the Neon Console, as well as access more advanced features like [Time Travel](https://neon.com/docs/guides/time-travel-assist) and [Explain and Analyze](https://neon.com/docs/get-started/query-with-neon-sql-editor#explain-and-analyze).

From the Neon Console, use the sidebar navigation to open the **SQL Editor** page. Notice that your default branch `production` is already selected, along with the database created during onboarding, `neondb`.

![Neon SQL Editor](https://neon.com/docs/get-started/sql_editor.png)

The first time you open the SQL Editor for a new project, the editor includes placeholder SQL commands to create and populate a new sample table called `playing_with_neon`.

For this tutorial, go ahead and create this sample table: click **Run**.

Every query you run in the SQL Editor is automatically saved with an AI-generated description, making it easy to find and reference your work later. For example, the sample table creation above will be saved with a description like "create and populate sample table in Neon". You can view your query history anytime by clicking the **History** button in the SQL Editor.

Or if you want to add the table from the command line and you already have `psql` installed:

```sql
CREATE TABLE IF NOT EXISTS playing_with_neon(id SERIAL PRIMARY KEY, name TEXT NOT NULL, value REAL);
INSERT INTO playing_with_neon(name, value)
  SELECT LEFT(md5(i::TEXT), 10), random() FROM generate_series(1, 10) s(i);
```

Your default branch `production` now has a table with some data.

## Try the AI Assistant

Now that you have some sample data, let's explore how the AI Assistant can help you write SQL queries using natural language prompts.

From the SQL Editor, click the **AI Assistant** button in the top-right corner and try a few prompts:

- _Add three more rows to the playing_with_neon table with tech company names_
- _Show me the highest value in the table_
- _Calculate the average value grouped by the first letter of the name_

![Neon SQL Editor AI Assistant](https://neon.com/docs/get-started/sql_assistant.png)

Each query you run is automatically saved with an AI-generated description, making it easy to find and reuse queries later. For example, when you ask the AI Assistant to add company data, you should see a response like:

```sql
-- Text to SQL original prompt:
-- Add three more rows to the playing_with_neon table with tech company names
INSERT INTO public.playing_with_neon (name, value) VALUES
('Google', 1000.5),
('Apple', 1200.75),
('Microsoft', 950.25);
```

With the description: "Add tech companies to playing_with_neon table"

Learn more about AI features in the [SQL Editor documentation](https://neon.com/docs/get-started/query-with-neon-sql-editor#ai-features).

## View and modify data in the console

Now that you have some data to play with, let's take a look at it on the **Tables** page in the Neon Console. The **Tables** page, powered by [Drizzle Studio](https://orm.drizzle.team/drizzle-studio/overview), provides a visual interface for exploring and modifying data and schemas directly from the console. The integration with Drizzle Studio provides the ability to add, update, and delete records, filter data, export data in `.json` and `.csv` formats, manage schemas (including creating and altering tables, views, and enums), create Postgres roles, and define RLS policies.

![Tables page Drizzle integration](https://neon.com/docs/get-started/tables_drizzle.png)

For a detailed guide on how to interact with your data using the **Tables** page, visit [Managing your data with interactive tables](https://neon.com/docs/guides/tables).

## Working with your development branch

Let's create a `development` branch and learn how to use the Neon CLI to manage branches and make schema changes in your development environment.

1. **Create a development branch**

   From the Neon Console, navigate to the **Branches** page and click **Create branch**. Name it `development`, select `production` as the parent branch, and click **Create new branch**. This creates an isolated copy of your production data that you can safely modify.

2. **Install CLI with Brew or NPM**

   Depending on your system, you can install the Neon CLI using either Homebrew (for macOS) or NPM (for other platforms).

   - For macOS using Homebrew:

     ```bash
     brew install neonctl
     ```

   - Using NPM (applicable for all platforms that support Node.js):

     ```bash
     npm install -g neonctl
     ```

3. **Authenticate with Neon**

   The `neon auth` command launches a browser window where you can authorize the Neon CLI to access your Neon account.

   ```bash
   neon auth
   ```

   ![neon auth](https://neon.com/docs/get-started/neonctl_auth.png "no-border")

4. **View your branches**

   First, list your projects to get your project ID:

   ```bash
   neon projects list
   ```

   You'll be prompted to select your organization. The output shows your project IDs:

   ```bash
   Projects
   ┌─────────────────────┬────────────┬───────────────┬──────────────────────┐
   │ Id                  │ Name       │ Region Id     │ Created At           │
   ├─────────────────────┼────────────┼───────────────┼──────────────────────┤
   │ cool-forest-12345678│ myproject  │ aws-us-east-2 │ 2025-10-14T14:33:43Z │
   └─────────────────────┴────────────┴───────────────┴──────────────────────┘
   ```

   Now list your branches using your project ID:

   ```bash
   neon branches list --project-id cool-forest-12345678
   ┌──────────────┬────────────────────────────┬───────────────┬──────────────────────┐
   │ Name         │ Id                         │ Current State │ Created At           │
   ├──────────────┼────────────────────────────┼───────────────┼──────────────────────┤
   │ development  │ br-calm-sky-a5xd78mn       │ ready         │ 2025-12-23T21:05:05Z │
   ├──────────────┼────────────────────────────┼───────────────┼──────────────────────┤
   │ ✱ production │ br-bold-wind-a4p92kpx      │ ready         │ 2025-12-23T21:04:57Z │
   └──────────────┴────────────────────────────┴───────────────┴──────────────────────┘
   ```

   This command shows your existing branches, including the `production` branch and the `development` branch you just created.

   **Tip:** To avoid specifying `--project-id` with each command, use `neon set-context` to set your default project and organization. See [set-context](https://neon.com/docs/reference/cli-set-context) for details.

## Make some sample schema changes

First, let's make sure our development branch is in sync with `production`. This ensures we're starting from the same baseline:

```bash
neon branches reset development --parent --project-id cool-forest-12345678
```

Now that our `development` branch matches `production`, we can make some changes. The `playing_with_neon` table from `production` is now available in your `development` branch, and we'll modify its schema and add new data to demonstrate how branches can diverge.

You can use the [Neon SQL Editor](https://neon.com/docs/get-started/query-with-neon-sql-editor) for this, but let's demonstrate how to connect and modify your database from the terminal using `psql`. If you don't have `psql` installed already, follow these steps to get set up:

Tab: Mac

```bash
brew install libpq
echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Tab: Linux

```bash
sudo apt update
sudo apt install postgresql-client
```

Tab: Windows

Download and install PostgreSQL from:

[https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)

Ensure psql is included in the installation.

With `psql` available, let's work from the terminal to connect to your `development` branch's database and make changes.

1. **Connect to your database**

   Get the connection string to your branch and connect to it directly via `psql`:

   ```bash
   neon connection-string development --database-name neondb --project-id cool-forest-12345678 --psql
   ```

   This command establishes the psql terminal connection to the `neondb` database on your development branch.

2. **Modify the schema**

   Add a new column `description` and index it:

   ```sql
   ALTER TABLE playing_with_neon
   ADD COLUMN description TEXT;

   CREATE INDEX idx_playing_with_neon_description ON playing_with_neon (description);
   ```

3. **Insert new data**

   Add new data that will be exclusive to the dev branch.

   ```sql
   INSERT INTO playing_with_neon (name, description)
   VALUES ('Your dev branch', 'Exploring schema changes in the dev branch');
   ```

4. **Verify the schema changes**

   Query the table to verify your schema changes:

   ```sql
   SELECT * FROM playing_with_neon;
   ```

   Your response should include the new description column and a new row where name = `Your dev branch` and description = `Exploring schema changes in the dev branch`:

   ```sql {1,13}
    id |        name        |    value    |                description
   ----+--------------------+-------------+--------------------------------------------
     1 | c4ca4238a0         |   0.5315024 |
     2 | c81e728d9d         |  0.17189825 |
     3 | eccbc87e4b         |  0.21428405 |
     4 | a87ff679a2         |   0.9721639 |
     5 | e4da3b7fbb         |   0.8649301 |
     6 | 1679091c5a         |  0.48413596 |
     7 | 8f14e45fce         |  0.82630277 |
     8 | c9f0f895fb         |  0.99945337 |
     9 | 45c48cce2e         | 0.054623786 |
    10 | d3d9446802         |  0.36634886 |
    11 | Your dev branch    |             | Exploring schema changes in the dev branch
   (11 rows)
   ```

## Check your changes with Schema Diff

After making the schema changes to your development branch, you can use the [Schema Diff](https://neon.com/docs/guides/schema-diff) feature to compare your branch against its parent branch. Schema Diff is a GitHub-style code-comparison tool used to visualize differences between different branch's databases.

For this tutorial, Schema Diff helps with validating isolation: it confirms that schema changes made in your isolated development branch remain separate from the production branch.

From the **Branches** page in the Neon Console:

1. Open the detailed view for your `development` branch and click **Open schema diff**.
2. Verify the right branches are selected and click **Compare**. You can see the schema changes we added to our development branch highlighted in green.

   ![Schema diff from branches page](https://neon.com/docs/get-started/getting_started_schema_diff.png)

### Schema Migrations

A more typical scenario for Schema Diff is when preparing for schema migrations. While Neon does not provide built-in schema migration tools, you can use ORMs like [Drizzle](https://drizzle.team/) or [Prisma](https://www.prisma.io/) to handle schema migrations efficiently. Read more about using Neon in your development workflow in [Connect Neon to your stack](https://neon.com/docs/get-started/connect-neon).

## Reset your development branch to production

After experimenting with changes in your development branch, let's now reset the branch to `production`, its parent branch.

[Branch reset](https://neon.com/docs/guides/reset-from-parent) functions much like a `git reset –hard parent` in traditional Git workflows.

Resetting your development branches to the `production` branch ensures that all changes are discarded, and your branch reflects the latest stable state of `production`. This is key to maintaining a clean slate for new development tasks and is one of the core advantages of Neon's branching capabilities.

You can reset to parent from the **Branches** page of the Neon Console, but here we'll use the Neon CLI.

Use the following command to reset your `development` branch to the state of the `production` branch:

Example:

```bash
neon branches reset development --parent --project-id cool-forest-12345678
```

If you go back to your **Schema Diff** and compare branches again, you'll see they are now identical:

![schema diff after reset](https://neon.com/docs/get-started/getting_started_schema_diff_reset.png)

### When to reset your branch

Depending on your development workflow, you can use branch reset:

- **After a feature is completed and merged**

  Once your changes are merged into `production`, reset the development branch to start on the next feature.

- **When you need to abandon changes**

  If a project direction changes or if experimental changes are no longer needed, resetting the branch quickly reverts to a known good state.

- **As part of your CI/CD automation**

  With the Neon CLI, you can include branch reset as an enforced part of your CI/CD automation, automatically resetting a branch when a feature is closed or started.

Make sure that your development team is always working from the latest schema and data by including branch reset in your workflow. To read more about using branching in your workflows, see [Branching workflows](https://neon.com/docs/get-started/workflow-primer).

**Tip: Additional branching features**

- **Working with sensitive data?** Neon supports [schema-only branching](https://neon.com/docs/guides/branching-schema-only) to create branches with just the database structure, without copying production data.
- **Need automatic cleanup?** Set branches to automatically [expire and be deleted](https://neon.com/docs/guides/branch-expiration) after a specified time period, perfect for temporary test branches or time-limited preview environments.

---

## Related docs (Start with Neon)

- [2 - Connect](https://neon.com/docs/get-started/connect-neon)
- [3 - Branching](https://neon.com/docs/get-started/workflow-primer)
- [4 - Setup Neon Auth](https://neon.com/docs/auth/overview)
```

### frameworks.md

URL: https://neon.com/docs/get-started/frameworks.md
Hash: 7e1a54a84eef

```
> This page location: Frontend & Frameworks > Frameworks
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Neon framework guides

Find detailed instructions for connecting to Neon from various frameworks

- [Node.js](https://neon.com/docs/guides/node): Connect a Node.js application to Neon
- [Next.js](https://neon.com/docs/guides/nextjs): Connect a Next.js application to Neon
- [NestJS](https://neon.com/docs/guides/nestjs): Connect a NestJS application to Neon
- [Astro](https://neon.com/docs/guides/astro): Connect an Astro site or app to Neon
- [Django](https://neon.com/docs/guides/django): Connect a Django application to Neon
- [Encore](https://neon.com/docs/guides/encore): Connect an Encore application to Neon
- [Entity Framework](https://neon.com/docs/guides/dotnet-entity-framework): Connect a Dotnet Entity Framework application to Neon
- [Express](https://neon.com/docs/guides/express): Connect an Express application to Neon
- [Hono](https://neon.com/docs/guides/hono): Connect a Hono application to Neon
- [Laravel](https://neon.com/docs/guides/laravel): Connect a Laravel application to Neon
- [Medusa.js](https://neon.com/docs/guides/medusajs): Use Medusa.js with Neon
- [Micronaut Kotlin](https://neon.com/docs/guides/micronaut-kotlin): Connect a Micronaut Kotlin application to Neon
- [Nuxt](https://neon.com/docs/guides/nuxt): Connect a Nuxt application to Neon
- [OAuth](https://neon.com/docs/guides/oauth-integration): Integrate with Neon using OAuth
- [Phoenix](https://neon.com/docs/guides/phoenix): Connect a Phoenix site or app to Neon
- [Quarkus](https://neon.com/docs/guides/quarkus-jdbc): Connect Quarkus (JDBC) to Neon
- [Quarkus](https://neon.com/docs/guides/quarkus-reactive): Connect Quarkus (Reactive) to Neon
- [React](https://neon.com/docs/guides/react): Connect a React application to Neon
- [RedwoodSDK](https://neon.com/docs/guides/redwoodsdk): Connect a RedwoodSDK application to Neon
- [Reflex](https://neon.com/docs/guides/reflex): Build Python Apps with Reflex and Neon
- [Remix](https://neon.com/docs/guides/remix): Connect a Remix application to Neon
- [Ruby on Rails](https://neon.com/docs/guides/ruby-on-rails): Connect a Ruby on Rails application to Neon
- [Symfony](https://neon.com/docs/guides/symfony): Connect from Symfony with Doctrine to Neon
- [SolidStart](https://neon.com/docs/guides/solid-start): Connect a SolidStart site or app to Neon
- [SQLAlchemy](https://neon.com/docs/guides/sqlalchemy): Connect a SQLAlchemy application to Neon
- [Sveltekit](https://neon.com/docs/guides/sveltekit): Connect a Sveltekit application to Neon
- [TanStack Start](https://neon.com/docs/guides/tanstack-start): Connect a TanStack Start application to Neon
- [Vue](https://neon.com/docs/guides/vue): Connect a Vue.js application to Neon

---

## Related docs (Frontend & Frameworks)

- [Languages](https://neon.com/docs/get-started/languages)
- [ORMs](https://neon.com/docs/get-started/orms)
```

### languages.md

URL: https://neon.com/docs/get-started/languages.md
Hash: bba5816e4156

```
> This page location: Frontend & Frameworks > Languages
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Neon language guides

Find detailed instructions for connecting to Neon from various languages

- [.NET](https://neon.com/docs/guides/dotnet-npgsql): Connect a .NET (C#) application to Neon
- [Elixir](https://neon.com/docs/guides/elixir): Connect an Elixir application to Neon
- [Go](https://neon.com/docs/guides/go): Connect a Go application to Neon
- [Java](https://neon.com/docs/guides/java): Connect a Java application to Neon
- [JavaScript](https://neon.com/docs/guides/javascript): Connect a JavaScript application to Neon
- [Python](https://neon.com/docs/guides/python): Connect a Python application to Neon
- [Rust](https://neon.com/docs/guides/rust): Connect a Rust application to Neon

---

## Related docs (Frontend & Frameworks)

- [Frameworks](https://neon.com/docs/get-started/frameworks)
- [ORMs](https://neon.com/docs/get-started/orms)
```

### orms.md

URL: https://neon.com/docs/get-started/orms.md
Hash: ba1c0661c5f3

```
> This page location: Frontend & Frameworks > ORMs
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Neon ORM guides

Find detailed instructions for connecting to Neon from various ORMs

- [Django](https://neon.com/docs/guides/django): Connect a Django application to Neon
- [Drizzle](https://neon.com/docs/guides/drizzle): Learn how to use Drizzle ORM with your Neon Postgres database (Drizzle docs)
- [Elixir Ecto](https://neon.com/docs/guides/elixir-ecto): Connect from Elixir with Ecto to Neon
- [Kysely](https://neon.com/docs/guides/kysely): Learn how to connect from Kysely to your Neon Postgres database
- [Laravel](https://neon.com/docs/guides/laravel): Connect a Laravel application to Neon
- [Prisma](https://neon.com/docs/guides/prisma): Learn how to connect from Prisma ORM to your Neon Postgres database
- [Rails](https://neon.com/docs/guides/ruby-on-rails): Connect a Rails application to Neon
- [SQLAlchemy](https://neon.com/docs/guides/sqlalchemy): Connect a SQLAlchemy application to Neon
- [TypeORM](https://neon.com/docs/guides/typeorm): Connect a TypeORM application to Neon

---

## Related docs (Frontend & Frameworks)

- [Frameworks](https://neon.com/docs/get-started/frameworks)
- [Languages](https://neon.com/docs/get-started/languages)
```

### dev-experience.md

URL: https://neon.com/docs/get-started/dev-experience.md
Hash: 6c2250ef151f

```
> This page location: Why Neon? > Developer experience
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Our DX Principles

Neon adapts to your workflow, not the other way around.

Our developer experience is anchored by four core pillars:

1. **Invisible infra** - compute and storage adapt to your workload in real-time
2. **No waiting** - deployment of new instances, restores, and rebuilds from past states are instant
3. **Branching-first, API-first, and AI-first workflows** - databases behave like any other modern tool
4. **A composable stack** - based on strong primitives with optional building blocks

## Invisible infra

### Autoscaling compute

Traditional OLTP databases force you to provision compute upfront (i.e., choose an instance size), plan for peak traffic, and manually adjust capacity over time. This adds overhead and leads to either overpaying for idle resources or underprovisioning and risk performance degradation.

You can build your database branching workflows using the [Neon CLI](https://neon.com/docs/reference/neon-cli), [Neon API](https://api-docs.neon.tech/reference/getting-started-with-neon-api), or [GitHub Actions](https://neon.com/docs/guides/branching-github-actions). For example, this example shows how to create a development branch from `main` with a simple CLI command:

**How it works**

Neon runs a continuous autoscaling loop that continuously monitors three core database / compute metrics. The platform then makes its autoscaling decision, adjusting resources in near real time. The three core metrics are:

Also, with Neon, you can easily keep your development branches up-to-date by resetting your schema and data to the latest from `main` with a simple command.

Rather than relying on fixed intervals or manual triggers, Neon's autoscaling algorithm continuously evaluates these three workload signals, adjusting compute up or down based on the live measurements - while always staying within the minimum and maximum limits you configure.

- CPU load and overall memory usage are checked every 5 seconds
- Local File Cache working set size is evaluated every 20 seconds
- Memory usage inside Postgres itself is monitored every 100 milliseconds

**What this means for DX**

You don't need to pick instance sizes when creating a Neon branch: only your max/min autoscaling limits. You also don't have to monitor load capacity to tune capacity or to schedule resizes. Autoscaling happens continuously and transparently as your application runs.

### Scale to zero

When a database is not actively handling queries, Neon [automatically scales compute all the way down to zero](https://neon.com/docs/introduction/scale-to-zero). Unused databases consume no compute resources, eliminating the cost of always-on instances that sit unused for large portions of the day. This happens by default after 5 minutes of inactivity, and when it's time to restart, cold starts take less than 1 second, with less than 500 milliseconds being typical.

**What this means for DX**

Scale to zero is a foundational capability for the Neon experience, allowing us to offer:

- **A free plan developers can actually use**. Neon can offer a generous free tier without subsidizing large amounts of idle infrastructure, something made possible by it's architecture and scale-to-zero capabilities. [We want every Postgres developer building on Neon](https://neon.com/blog/why-so-many-projects-in-the-neon-free-plan), and this starts with hosting their side projects and experiments.

- **Many short-lived, non-production environments**. Scale to zero makes it practical to run [large numbers of ephemeral databases](https://neon.com/use-cases/dev-test) for previews, CI runs, experiments, and testing. Teams can create and discard environments freely, without cost pressure forcing them to share databases or cut corners.

- **A foundation for platforms and AI agents operating at scale**. Full-stack apps can provision and manage thousands of isolated Neon projects programmatically, fully integrating the process within their own product experience, for example to power their own free plans. Without scale-to-zero, this would imply massive infrastructure costs upfront.

### On-demand storage

In traditional Postgres setups, storage is something you plan upfront: you estimate how much data you'll need, provision disk accordingly, and revisit that decision as your application grows. Getting this wrong leads to wasted capacity and full-disk errors. Neon removes this friction by making storage fully on demand.

Neon's storage is [built on object storage](https://neon.com/docs/introduction/architecture-overview), deacoupled from compute. It is reliable by design and it expands automatically as data is written, as scaling storage does not require resizing compute resources or causing downtime. You can start with a small database and grow it continuously, without ever revisiting storage sizing decisions.

**What this means for DX**

Neon developers don't estimate disk sizes or plan storage migrations. Databases grow naturally with the application, without operational intervention or downtime.

## No waiting

### New deployments are fast

With Neon, deploying a new database instance is a fast operation that takes less than a second. Creating a new project or branch does not involve provisioning a new virtual machine, eliminating minutes of provisioning time.

**What this means for DX**

Not only does this provide a better overall user experience - it also makes Neon a natural fit for platforms that need to provision databases programmatically for their users, such as open-source frameworks, developer platforms with their own free plans, or agent-driven systems. Instance creation becomes fast enough to sit directly on the user path.

### A record of all past states, instantly accessible

Storage in Neon is also [history-preserving](https://neon.com/blog/get-page-at-lsn) by design. As data changes over time, Neon efficiently retains past versions of your database state as part of normal operation, making operations that are painfully slow in traditional Postgres (like restores) trivial on Neon.

**Instant restores**

Neon's [Instant Restore](https://neon.com/docs/introduction/branch-restore#how-instant-restore-works) allows you to restore your database to a precise point in time in a few clicks or a single API call. Restore operations are near-instant because Neon doesn't copy data or rebuild the database, it simply re-anchors the database state to a known point in its history.

**Snapshots as checkpoints**

In addition to continuous history, Neon exposes [snapshots](https://neon.com/docs/guides/backup-restore), explicit checkpoints that capture your database state at a moment in time. Snapshots are useful when you want long-lived restore points independent of the [restore window](https://neon.com/docs/introduction/restore-window), a known rollback point before a risky change, or versioned checkpoints for environments or [agent workflows](https://neon.com/docs/ai/ai-database-versioning).

**What this means for DX**

When your database keeps a complete, accessible record of its past, developers can work with a fundamentally different mindset: mistakes are reversible. They iterate more confidently, knowing that mistakes can be undone quickly and precisely.

## Workflows

### Branching-first

Modern software development is built around iteration, but most database setups are still built around a single mutable state. Neon takes a different approach: instead of treating a database as a static resource that must be copied over and over, Neon treats the database as a versioned system using short-lived [branches](https://neon.com/docs/introduction/branching).

**Always lightweight**

Whether your database is 1 GB or 1 TB, creating a branch takes seconds. Branches use a copy-on-write model, so they're instant to create regardless of database size.

**Designed to be discarded**

Neon branching is optimized for short-lived environments or for environments that get to be refreshed often. To support this, Neon provides [branch expiration](https://neon.com/docs/guides/branch-expiration): you can configure branches to automatically expire and be deleted after a set period of time. Neon also allows developers to [reset a branch](https://neon.com/docs/guides/reset-from-parent) to the latest state of its parent instantly, with one click or API call, whenever they need a new starting point.

**What this means for DX**

Teams deploy hundreds of branches as temporary, task-specific environments, substituting additional, long-lived database instances. Some [common patterns](https://neon.com/branching) include:

- **Branch per developer**. Each engineer works against their own isolated database environment (branch), avoiding conflicts when making schema or data changes.
- **Branch per experiment or feature**. Short-lived branches are used to explore changes, run migrations, or validate ideas, then deleted once the work is done.
- **Branch per pull request**. A new branch is created automatically for every PR, powering preview deployments with production-like data.
- **Branch per CI run**. Test suites run against a fresh database branch, ensuring clean state and reproducible results for every pipeline run.

### API-first

Neon is built with an API-first mindset. Every core operation is exposed programmatically, so developers can manage your database environments the same way you manage the rest of their infrastructure.

**Proven at scale**

Neon powers [platforms](https://neon.com/platforms) where thousands of databases are provisioned, scaled, and deleted automatically every day. This includes developer platforms embedding Postgres into their product experience, as well as [AI agents](https://neon.com/use-cases/ai-agents) that provision databases dynamically while building and running applications on behalf of users.

The [Neon API](https://api-docs.neon.tech/reference/getting-started-with-neon-api) has been shaped by real-world requirements, and it's able to

- Manage hundreds of thousands of projects
- Automate database lifecycles with minimal human intervention
- Enforce usage limits and cost controls programmatically, including maximum compute uptime per billing cycle, autoscaling limits, monthly data written limits, storage limits per branch, and more

**CLI and native integrations**

For local development and CI pipelines, the [Neon CLI](https://neon.com/docs/reference/neon-cli) provides a simple scripting interface that builds directly on the same API. Neon also provides native integrations for common workflows:

- GitHub Actions for CI-driven branching and cleanup
- Vercel for automatic database branches per preview deployment
- Neon Data API for querying your database over HTTP

**What this means for DX**

Database workflows stop being special-case operations: teams can create, update, and destroy database environments as part of their deployment pipelines.

### AI-first

AI has changed how developers write code, manage infrastructure, and ship applications, so databases need to fit naturally into these workflows.

**Using Neon with AI IDEs and assistants**

Neon integrates directly with AI IDEs and coding assistants through its [MCP](https://neon.com/docs/ai/neon-mcp-server) and [Agent Skills](https://neon.com/docs/ai/agent-skills). This allows tools like Cursor, Claude, and other MCP-compatible environments to understand and interact with your Neon project in a structured and safe way.

**A Postgres layer for agents**

Neon is also ready to be used as the database layer for [full-stack codegen platforms](https://neon.com/use-cases/ai-agents), or systems where AI agents provision, manage, and operate infrastructure autonomously. Neon's serverless architecture, instant provisioning, and API-first design make it a natural fit for these platforms. AI agents can create thousands of databases programmatically, manage them over their lifecycle, and clean them up automatically, all while staying cost-efficient.

**What this means for DX**

Developers can safely delegate database-related tasks to AI assistants in their IDEs, while platforms and agents can provision and manage databases autonomously.

## Composable stack

Modern application stacks are increasingly modular. Developers mix and match databases, frameworks, hosting platforms, authentication providers, and AI tools based on their needs and expect each component to integrate cleanly without imposing rigid boundaries. Neon is built around this principle of composability - nothing in Neon requires you to adopt a specific framework or vendor-specific workflow. At its core, Neon is Postgres: you can connect with any driver, ORM, or tool in the ecosystem, deploy it anywhere, and integrate it into existing stacks without changing how you build.

At the same time, Neon provides optional building blocks that make common patterns easier, without locking you in, like authentication. [Neon Auth](https://neon.com/docs/auth/overview) provides authentication primitives that live directly alongside your data in Postgres. Users, sessions, organizations, and permissions are stored in your database and follow the same lifecycle as the rest of your application state. Because Neon Auth is integrated into the platform,

- Auth data branches with your database, making it easy to test real authentication flows in preview and development environments
- Auth state is versioned and reversible, benefiting from the same restore and snapshot capabilities
- Auth integrates naturally with database-level concepts like joins, constraints, and row-level security

**What this means for DX**

Developers stay in control of their stack. You can adopt Neon incrementally, use only the primitives you need, and integrate optional building blocks like Auth without committing to a rigid platform model, keeping architectures flexible.

## Build without friction

Neon is designed to remove friction from database workflows without constraining how you build. Our users tell us the best thing about Neon is that building feels intuitive, and that they forget the database is even there. That's exactly the goal. When the database stops getting in the way, teams can move faster, experiment safely, and focus on shipping.

---

## Related docs (Why Neon?)

- [Our mission](https://neon.com/docs/get-started/why-neon)
- [Built to scale](https://neon.com/docs/get-started/built-to-scale)
```

### query-with-neon-sql-editor.md

URL: https://neon.com/docs/get-started/query-with-neon-sql-editor.md
Hash: e1877466fdd6

```
> This page location: Connect to Neon > Neon SQL Editor
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Query with Neon's SQL Editor

Query your database from the Neon Console using the Neon SQL Editor

The Neon SQL Editor allows you to run queries on your Neon databases directly from the Neon Console. In addition, the editor keeps a query history, permits saving queries, and provides [**Explain**](https://www.postgresql.org/docs/current/sql-explain.html) and [**Analyze**](https://www.postgresql.org/docs/current/using-explain.html#USING-EXPLAIN-ANALYZE) features.

To use the SQL Editor:

1. Navigate to the [Neon Console](https://console.neon.tech/).
2. Select your project.
3. Select **SQL Editor**.
4. Select a branch and database.
5. Enter a query into the editor and click **Run** to view the results.

![Neon SQL Editor](https://neon.com/docs/get-started/sql_editor.png)

You can use the following query to try the SQL Editor. The query creates a table, adds data, and retrieves the data from the table.

```sql
CREATE TABLE IF NOT EXISTS playing_with_neon(id SERIAL PRIMARY KEY, name TEXT NOT NULL, value REAL);
INSERT INTO playing_with_neon(name, value)
SELECT LEFT(md5(i::TEXT), 10), random() FROM generate_series(1, 10) s(i);
SELECT * FROM playing_with_neon;
```

Running multiple query statements at once returns a separate result set for each statement. The result sets are displayed in separate tabs, numbered in order of execution, as shown above.

To clear the editor, click **New Query**.

**Tip:** When querying objects such as tables and columns with upper case letters in their name, remember to enclose the identifier name in quotes. For example: `SELECT * FROM "Company"`. Postgres changes identifier names to lower case unless they are quoted. The same applies when creating objects in Postgres. For example, `CREATE TABLE DEPARTMENT(id INT)` creates a table named `department` in Postgres. For more information about how quoted and unquoted identifiers are treated by Postgres, see [Identifiers and Key Words](https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS), in the _PostgreSQL documentation_.

## Save your queries

The SQL Editor allows you to save your queries.

To save a query:

1. Enter the query into the editor.
2. Click **Save** to open the **SAVE QUERY** dialog.
3. Enter a name for the query and click **Save**.

The query is added to the **Saved** list in the left pane of the SQL Editor. You can rerun a query by selecting it from the **Saved** list.

You can rename or delete a saved query by selecting **Rename** or **Delete** from the more options menu associated with the saved query.

## View the query history

The SQL Editor maintains a query history for the project. To view your query history, select **History** in the left pane of the SQL Editor. You can click an item in the **History** list to view the query that was run.

**Note:** Queries saved to **History** are limited to 9 KB in length. While you can execute longer queries from the SQL Editor, any query exceeding 9 KB will be truncated when saved. A `-- QUERY TRUNCATED` comment is added at the beginning of these queries to indicate truncation. Additionally, if you input a query longer than 9 KB in the Neon SQL Editor, a warning similar to the following will appear: `This query will still run, but the last 1234 characters will be truncated from query history`.

## Explain and Analyze

The Neon SQL Editor provides **Explain** and **Analyze** features.

- The **Explain** feature runs the specified query with the Postgres [EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html) command, which returns the execution plan for the query. The **Explain** feature only returns a plan with estimates. It does not execute the query.
- The **Analyze** feature runs the specified query with [EXPLAIN ANALYZE](https://www.postgresql.org/docs/current/using-explain.html#USING-EXPLAIN-ANALYZE). The `ANALYZE` parameter causes the query to be executed and returns actual row counts and run times for plan nodes along with the `EXPLAIN` estimates.

Understanding the information provided by the **Explain** and **Analyze** features requires familiarity with the Postgres [EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html) command and its `ANALYZE` parameter. Refer to the [EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html) documentation and the [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) topic in the _PostgreSQL documentation_.

## Time Travel

You can toggle Time Travel in the SQL Editor to switch from querying your current data to querying against a selected point within your [restore window](https://neon.com/docs/introduction/restore-window).

![time travel in SQL Editor](https://neon.com/docs/get-started/time_travel_sql_editor.png)

For more details about using Time Travel queries, see:

- [Time Travel](https://neon.com/docs/guides/time-travel-assist)
- [Time Travel tutorial](https://neon.com/docs/guides/time-travel-tutorial)

## Export or copy query results

The Neon SQL Editor lets you export data to `CSV`, `JSON`, and `XLSX` formats, or copy query results directly to your clipboard as JSON. Access the download and copy buttons from the bottom right corner of the **SQL Editor** page. These buttons only appear when there is a result set to display.

To copy query results as JSON without downloading a file, click the copy icon button. The JSON will be instantly available in your clipboard, ready to paste into other applications or documentation.

## Expand results section of the SQL Editor window

You can expand the results section of the SQL Editor window by selecting the expand window button from the bottom right corner of the **SQL Editor** page. There must be query results to display, otherwise the expanded results section will appear blank.

## Meta-commands

The Neon SQL Editor supports using Postgres meta-commands, which act like shortcuts for interacting with your database. If you are already familiar with using meta-commands from the `psql` command-line interface, you can use many of those same commands in the SQL Editor.

### Benefits of Meta-Commands

Meta-commands can significantly speed up your workflow by providing quick access to database schemas and other critical information without needing to write full SQL queries. They are especially useful for database management tasks, making it easier to handle administrative duties directly from the Neon Console.

### Available meta-commands

Here are some of the meta-commands that you can use within the Neon SQL Editor:

- `\dt`: List all tables in the current database.
- `\d [table_name]`: Describe a table's structure.
- `\l`: List all databases.
- `\?` - A cheat sheet of available meta-commands
- `\h [NAME]` - Get help for any Postgres command. For example, try `\h SELECT`.

Note that not all meta-commands are supported in the SQL Editor. To get a list of supported commands, use `\?`.

<details>

<summary>Example of supported commands</summary>

```bash
Informational
  (options: S = show system objects, + = additional detail)
  \d[S+]                 list tables, views, and sequences
  \d[S+]  NAME           describe table, view, sequence, or index
  \da[S]  [PATTERN]      list aggregates
  \dA[+]  [PATTERN]      list access methods
  \dAc[+] [AMPTRN [TYPEPTRN]]  list operator classes
  \dAf[+] [AMPTRN [TYPEPTRN]]  list operator families
  \dAo[+] [AMPTRN [OPFPTRN]]   list operators of operator families
  \dAp[+] [AMPTRN [OPFPTRN]]   list support functions of operator families
  \db[+]  [PATTERN]      list tablespaces
  \dc[S+] [PATTERN]      list conversions
  \dconfig[+] [PATTERN]  list configuration parameters
  \dC[+]  [PATTERN]      list casts
  \dd[S]  [PATTERN]      show object descriptions not displayed elsewhere
  \dD[S+] [PATTERN]      list domains
  \ddp    [PATTERN]      list default privileges
  \dE[S+] [PATTERN]      list foreign tables
  \des[+] [PATTERN]      list foreign servers
  \det[+] [PATTERN]      list foreign tables
  \deu[+] [PATTERN]      list user mappings
  \dew[+] [PATTERN]      list foreign-data wrappers
  \df[anptw][S+] [FUNCPTRN [TYPEPTRN ...]]
                         list [only agg/normal/procedure/trigger/window] functions
  \dF[+]  [PATTERN]      list text search configurations
  \dFd[+] [PATTERN]      list text search dictionaries
  \dFp[+] [PATTERN]      list text search parsers
  \dFt[+] [PATTERN]      list text search templates
  \dg[S+] [PATTERN]      list roles
  \di[S+] [PATTERN]      list indexes
  \dl[+]                 list large objects, same as \lo_list
  \dL[S+] [PATTERN]      list procedural languages
  \dm[S+] [PATTERN]      list materialized views
  \dn[S+] [PATTERN]      list schemas
  \do[S+] [OPPTRN [TYPEPTRN [TYPEPTRN]]]
                         list operators
  \dO[S+] [PATTERN]      list collations
  \dp[S]  [PATTERN]      list table, view, and sequence access privileges
  \dP[itn+] [PATTERN]    list [only index/table] partitioned relations [n=nested]
  \drds [ROLEPTRN [DBPTRN]] list per-database role settings
  \drg[S] [PATTERN]      list role grants
  \dRp[+] [PATTERN]      list replication publications
  \dRs[+] [PATTERN]      list replication subscriptions
  \ds[S+] [PATTERN]      list sequences
  \dt[S+] [PATTERN]      list tables
  \dT[S+] [PATTERN]      list data types
  \du[S+] [PATTERN]      list roles
  \dv[S+] [PATTERN]      list views
  \dx[+]  [PATTERN]      list extensions
  \dX     [PATTERN]      list extended statistics
  \dy[+]  [PATTERN]      list event triggers
  \l[+]   [PATTERN]      list databases
  \lo_list[+]            list large objects
  \sf[+]  FUNCNAME       show a function's definition
  \sv[+]  VIEWNAME       show a view's definition
  \z[S]   [PATTERN]      same as \dp
```

</details>

For more information about meta-commands, see [PostgreSQL Meta-Commands](https://www.postgresql.org/docs/current/app-psql.html#APP-PSQL-META-COMMANDS).

### How to Use Meta-Commands

To use a meta-command in the SQL Editor:

1. Enter the meta-command in the editor, just like you would a SQL query.
2. Press **Run**. The result of the meta-command will be displayed in the output pane, similar to how SQL query results are shown.

   For example, here's the schema for the `playing_with_neon` table we created above, using the meta-command `\d playing_with_neon`:

   ![metacommand example](https://neon.com/docs/get-started/sql_editor_metacommand.png)

## AI features

The Neon SQL Editor offers three AI-driven features:

- **SQL generation**: Easily convert natural language requests to SQL. Press the ✨ button or **Cmd/Ctrl+Shift+M**, type your request, and the AI assistant will generate the corresponding SQL for you. It's schema-aware, meaning you can reference any table names, functions, or other objects in your schema.
  ![SQL generation](https://neon.com/docs/get-started/sql_editor_ai.png)
- **Fix with AI**: If your query returns an error, simply click **Fix with AI** next to the error message. The AI assistant will analyze the error, suggest a fix, and update the SQL Editor so you can run the query again.
  ![Fix withn AI](https://neon.com/docs/get-started/fix_with_ai.png)
- **AI-generated query names**: Descriptive names are automatically assigned to your queries in the Neon SQL Editor's **History**. This feature helps you quickly identify and reuse previously executed queries.
  ![AI-generated query names](https://neon.com/docs/get-started/query_names.png)

**Important:** To enhance your experience with the Neon SQL Editor's AI features, we share your database schema with the AI agent. No actual data is shared. We currently use AWS Bedrock as our LLM provider, ensuring all requests remain within AWS's secure infrastructure where other Neon resources are also managed.

_There is a maximum limit of 5 AI requests every 60 seconds._

---

## Related docs (Connect to Neon)

- [Connect to Neon](https://neon.com/docs/connect/connect-intro)
- [Choosing your connection method](https://neon.com/docs/connect/choose-connection)
- [Connect from any app](https://neon.com/docs/connect/connect-from-any-app)
- [Neon serverless driver](https://neon.com/docs/serverless/serverless-driver)
- [Passwordless auth](https://neon.com/docs/connect/passwordless-connect)
- [Securing connections](https://neon.com/docs/connect/connect-securely)
- [Connection pooling](https://neon.com/docs/connect/connection-pooling)
- [Latency benchmarks](https://neon.com/docs/guides/benchmarking-latency)
```

### why-neon.md

URL: https://neon.com/docs/get-started/why-neon.md
Hash: a327ebe3bb6f

```
> This page location: Why Neon? > Our mission
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Why Neon?

Serverless Postgres, by Databricks

## Our mission

**Neon is the Postgres layer for the internet: a fully managed, serverless, open-source Postgres designed to help developers build scalable, dependable applications faster than ever.**

We aim to deliver Postgres as a cloud service that feels effortless, from your first side project to millions of users in production. We believe Postgres should be as universal and accessible as object storage, something every developer can rely on without thinking about infrastructure.

Neon is built on a distributed, cloud-native architecture that separates storage and compute, giving Postgres the scale, reliability, and efficiency modern applications require. This foundation unlocks the features developers expect today (autoscaling, scale-to-zero, instant branching, instant restores, usage-based pricing, and much more) without changing the Postgres you already know.

**Tip: A Databricks company** In May 2025, Neon joined Databricks to shape the future of Postgres and AI-native development. Our mission stayed the same, but we're now backed by the performance, security, and global scale of the Databricks Data Intelligence Platform. Neon's architectural foundation also powers [Lakebase](https://www.databricks.com/product/lakebase); learn more in [Neon and Lakebase](https://neon.com/docs/introduction/neon-and-lakebase).

## What makes Neon different

### Serverless Postgres, built from first principles

Neon isn't "Postgres-like": it is Postgres, with full compatibility across ORMs, extensions, and frameworks. But Neon's defining characteristic lies in its architecture, which translates into serverless behavior that isn't layered on but foundational to the system.

Traditional Postgres providers scale by moving VMs up and down, placing instances behind proxies, or by manual tuning. Neon does none of that. Instead, Neon is serverless, which to us means:

- Storage and compute are fully separated
- Compute is stateless and ephemeral
- Storage is distributed, durable, and versioned
- Scaling involves starting more compute, not moving a monolithic instance

### Developer-first features that fit modern workflows

Neon's architecture lets us design a database platform that behaves the way developers expect modern tools to behave: instant, intuitive, cost-efficient, and safe to experiment with. This modernizes workflows that, in many managed Postgres services, still feel decades old.

- **Scale-to-zero.** Inactive databases shut down automatically to save costs. Ideal for side projects, development environments, and agent-generated apps.
- **Autoscaling.** For your production database, Neon resizes your compute up and down automatically based on traffic. Your performance stays steady without capacity planning.
- **Branching.** In Neon, you can clone your entire database (data and schema) instantly to create dev environments, run migrations safely, automate previews, enable safe staging workflows, and build versioning and checkpoints for agents.
- **Instant restores.** You can also go back to any point in time in seconds, no matter how large your database, or instantly revert to a previously-saved snapshot.
- **Usage-based pricing.** In Neon, you pay only for what you use, without provisioning storage or compute in advance and without being forced into expensive add-ons.
- **A Free Plan developers can actually use.** Our unique architecture makes it incredibly efficient to run a large Free Plan with many projects per account and enough resources to build real apps.

## Who uses Neon and why

### Developers: From side projects to live apps

Independent developers want to build without friction. They don't want to create accounts, configure VMs, or invest large sums just to test an idea. They want something that feels modern, straightforward, and aligned with today's frameworks.

**Why they build on Neon**

- They get a Postgres connection string immediately: no setup
- The Free Plan is generous enough to build real apps
- They can work on multiple projects at once
- Neon integrates easily with Next.js, Remix, Vercel, Prisma, Drizzle, and the broader ecosystem
- Branching, previews, and instant restores let them experiment quickly
- The experience feels lightweight, fast, and developer-first, not enterprise-heavy

  **Tip: Useful links to get started** Check out our [framework guides](https://neon.com/docs/get-started/frameworks), [templates](https://neon.com/templates), [code examples](https://github.com/neondatabase/examples), and join our [community Discord](https://discord.gg/92vNTzKDGp).

### Startups: From dev to scale

Startups want to ship product fast and avoid cloud infrastructure complexity. They need their Postgres to be reliable, scalable, and invisible, something they never have to think about unless something goes wrong.

**Why they build on Neon**

- Its serverless architecture removes most management
- Autoscaling handles unpredictable traffic without overprovisioning or planning compute sizes
- Branching speeds up building - teams can ship safely and quickly
- Neon's straightforward and feature-complete [API](https://neon.com/docs/reference/api-reference)
- Usage-based pricing means no upfront commitments
- Neon delivers on reliability, performance, and compliance

**Tip: Keep reading** Check out our [success stories](https://neon.com/case-studies), [use cases](https://neon.com/use-cases/serverless-apps), and the [Startup Program](https://neon.com/startups).

### Agents & codegen: From prompt to app

Full-stack codegen platforms need to spin up thousands of independent applications instantly, each with its own backend. They need a database that can support a fleet of thousands of mostly inactive databases every day without breaking performance or blowing up costs.

**Why they build on Neon**

- Neon is already tested at scale, powering platforms like Replit
- They can deploy a Postgres backend instantly and transparently, without signup from the end-user
- Thousands of short-lived, low-usage databases can be deployed programmatically
- Scale-to-zero makes per-app databases economically viable, even at scale
- Branching allows for agent-friendly workflows: versioning, snapshots, rollbacks, checkpoints
- Neon Auth + Data API form a backend layer that works directly with the database

**Tip: Join the Agent Program** Building a full-stack agent that needs databases? Apply to our [Agent Program](https://neon.com/programs/agents#agent-plan-pricing) and get access to special pricing, resource limits, and features.

## The architecture that makes it possible: how Neon works

The benefits developers experience with Neon (instant branching, autoscaling, scale-to-zero, and fast recovery) are not product features layered on top of Postgres. They fall out naturally from Neon's architecture.

At the highest level, Neon is built on a simple but powerful idea: Postgres on the object store.

Traditional Postgres systems are designed around local or attached disks. That design couples durability, storage capacity, and compute into a single machine. Neon breaks that coupling by moving durability and history into cloud object storage. Once storage lives in the object store, the rest of the system can be rethought.

### Object store first

Neon treats the object store as the system of record. WAL, page versions, and database history are persisted directly to durable object storage rather than tied to a specific server or disk. The consequences:

- Durability no longer depends on a single machine
- Storage scales independently and effectively without limits
- Recovery becomes a metadata operation, not a data copy
- History is retained natively, not reconstructed from backups

### Separation of storage and compute

With durability and history centralized in storage, compute can be fully decoupled. Data lives in a distributed, durable storage layer. Computes are lightweight and ephemeral processes that attach to that data when needed. This separation is the foundation of everything Neon can do:

- Start and stop compute in seconds
- Scale compute independently of storage
- Attach multiple computes to the same data
- Recover from failures instantly
- Enable true pay-only-for-what-you-use pricing

### A versioned storage engine (copy-on-write)

Separation alone is not enough. Neon's most distinctive capabilities come from its versioned storage engine, which preserves the full history of the database. Every WAL record and every page version is retained in a single, unified system. As a result:

- Entire databases can be branched instantly
- Any past state can be restored without copying data
- Point-in-time recovery is intrinsic, not an add-on
- Development, staging, previews, and rollbacks become cheap and safe

### Stateless, ephemeral compute

The final piece follows naturally from the others. Computes in Neon do not store data. They attach to the storage layer at a specific point in history, execute queries, and disappear when no longer needed. They can be created, resized, or destroyed at any time without risking data loss. This is what allows Neon to:

- Autoscale without downtime
- Scale to zero when idle
- Handle fleets of thousands of short-lived databases
- Support agent-driven and highly dynamic workloads

**Tip: Neon vs Lakebase** For a full breakdown of both products — including when to choose each — see [Neon vs Lakebase](https://neon.com/docs/introduction/neon-and-lakebase).

> **Contact us**
>
> Neon and Lakebase represent two paths built on the same architectural foundation. Explore your options and get help deciding which service is the best fit.
>
> [Reach out](https://www.databricks.com/company/contact)

---

## Related docs (Why Neon?)

- [Developer experience](https://neon.com/docs/get-started/dev-experience)
- [Built to scale](https://neon.com/docs/get-started/built-to-scale)
```

### choose-connection.md

URL: https://neon.com/docs/connect/choose-connection.md
Hash: 05a34711303f

```
> This page location: Connect to Neon > Choosing your connection method
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Choosing your connection method

Find the right driver and connection type for your deployment platform

Your connection method depends on where your code runs. Use the table below for a quick lookup, or read the scenario sections for detailed guidance.

## Quick reference by environment

Each scenario is [described in detail](https://neon.com/docs/connect/choose-connection#find-your-scenario) further down the page.

| Environment                                                                                                                        | Recommended driver         | Pooling                                                                         | Guide                                                                   |
| ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [Any platform (non-JS/TS)](https://neon.com/docs/connect/choose-connection#not-using-javascript-or-typescript)                     | Native Postgres driver     | [Neon pooled connection](https://neon.com/docs/connect/connection-pooling)      | [Language guides](https://neon.com/docs/get-started/languages)          |
| [Railway / Render / VPS / Docker](https://neon.com/docs/connect/choose-connection#running-on-a-long-lived-server-jsts)             | `pg` or `postgres.js`      | Client-side or [Neon pooling](https://neon.com/docs/connect/connection-pooling) | [Framework guides](https://neon.com/docs/get-started/frameworks)        |
| [Vercel (Fluid)](https://neon.com/docs/connect/choose-connection#deploying-to-vercel-or-cloudflare-with-platform-pooling)          | `pg` (node-postgres)       | [`@vercel/functions`](https://www.npmjs.com/package/@vercel/functions)          | [Vercel guide](https://neon.com/docs/guides/vercel-connection-methods)  |
| [Cloudflare + Hyperdrive](https://neon.com/docs/connect/choose-connection#deploying-to-vercel-or-cloudflare-with-platform-pooling) | `pg` (node-postgres)       | [Hyperdrive](https://developers.cloudflare.com/hyperdrive/)                     | [Hyperdrive guide](https://neon.com/docs/guides/cloudflare-hyperdrive)  |
| [Cloudflare Workers](https://neon.com/docs/connect/choose-connection#deploying-to-another-serverless-or-edge-platform)             | `@neondatabase/serverless` | N/A                                                                             | [Serverless driver](https://neon.com/docs/serverless/serverless-driver) |
| [Netlify / Deno Deploy](https://neon.com/docs/connect/choose-connection#deploying-to-another-serverless-or-edge-platform)          | `@neondatabase/serverless` | N/A                                                                             | [Serverless driver](https://neon.com/docs/serverless/serverless-driver) |
| [Client-side (browser)](https://neon.com/docs/connect/choose-connection#building-a-client-side-app-without-a-backend)              | `@neondatabase/neon-js`    | N/A                                                                             | [Data API](https://neon.com/docs/data-api/overview)                     |

## Find your scenario

### Not using JavaScript or TypeScript?

Use a standard TCP-based Postgres driver with a [pooled connection](https://neon.com/docs/connect/connection-pooling). Connect from a secure backend server using your language's native driver.

| Language/Framework  | Guide                                                       |
| ------------------- | ----------------------------------------------------------- |
| Django (Python)     | [Django](https://neon.com/docs/guides/django)               |
| SQLAlchemy (Python) | [SQLAlchemy](https://neon.com/docs/guides/sqlalchemy)       |
| Elixir Ecto         | [Elixir Ecto](https://neon.com/docs/guides/elixir-ecto)     |
| Laravel (PHP)       | [Laravel](https://neon.com/docs/guides/laravel)             |
| Ruby on Rails       | [Ruby on Rails](https://neon.com/docs/guides/ruby-on-rails) |
| Go                  | [Go](https://neon.com/docs/guides/go)                       |
| Rust                | [Rust](https://neon.com/docs/guides/rust)                   |
| Java                | [Java](https://neon.com/docs/guides/java)                   |

For the full list, see [Language quickstarts](https://neon.com/docs/get-started/languages).

### Running on a long-lived server (JS/TS)?

If you deploy a JavaScript or TypeScript app to Railway, Render, a VPS, Docker, or any self-hosted environment with persistent processes, use a standard TCP driver with [connection pooling](https://neon.com/docs/connect/connection-pooling). Your server can maintain a connection pool across requests, making TCP the fastest and most efficient option.

Recommended drivers: [`pg` (node-postgres)](https://node-postgres.com/), [`postgres.js`](https://github.com/porsager/postgres), or [`Bun.SQL`](https://bun.com/docs/runtime/sql#postgresql).

### Deploying to Vercel or Cloudflare with platform pooling?

These platforms provide their own connection pooling, which makes standard TCP the best choice.

**Vercel (Fluid compute):** Use `pg` (node-postgres) with [`@vercel/functions`](https://www.npmjs.com/package/@vercel/functions). Vercel Fluid keeps functions warm long enough to reuse TCP connections, so you skip the connection setup cost on subsequent requests. See the [Vercel connection methods guide](https://neon.com/docs/guides/vercel-connection-methods) for details.

**Cloudflare (Hyperdrive):** Use `pg` (node-postgres) with [Hyperdrive](https://developers.cloudflare.com/hyperdrive/), which provides connection pooling for Workers. See the [Cloudflare Hyperdrive guide](https://neon.com/docs/guides/cloudflare-hyperdrive) for setup.

### Deploying to another serverless or edge platform?

For platforms like Netlify Functions, Deno Deploy, or Cloudflare Workers (without Hyperdrive), use the [Neon serverless driver](https://neon.com/docs/serverless/serverless-driver) (`@neondatabase/serverless`). It connects over HTTP or WebSockets instead of TCP, reducing connection setup latency.

Choose your transport based on your query pattern: use **HTTP** for single queries and non-interactive transactions, or **WebSocket** for interactive transactions and `node-postgres` compatibility. See [HTTP vs. WebSocket](https://neon.com/docs/connect/choose-connection#http-vs-websocket-serverless-driver) for details.

### Building a client-side app without a backend?

Use the [Neon Data API](https://neon.com/docs/data-api/overview) via [`@neondatabase/neon-js`](https://www.npmjs.com/package/@neondatabase/neon-js). Browsers cannot open TCP connections to Postgres, so the Data API provides a secure HTTP interface with Row-Level Security support.

**Note:** The Data API is currently in beta.

See the [JavaScript SDK reference](https://neon.com/docs/reference/javascript-sdk) for full documentation.

## Understanding the options

### Pooled vs. direct connections

A **pooled connection** routes traffic through PgBouncer, which manages a pool of reusable Postgres connections. Use pooled connections by default. They handle up to 10,000 concurrent client connections and work well for serverless apps and high-concurrency workloads.

A **direct connection** connects straight to Postgres without PgBouncer. Use direct connections for operations that require stable, long-lived connections or features PgBouncer does not support, such as:

- Schema migrations (Prisma Migrate, Drizzle Kit, django-admin migrate)
- `CREATE INDEX CONCURRENTLY`
- `LISTEN` / `NOTIFY`
- Temporary tables or prepared statements across multiple queries

Direct connections are limited by `max_connections`, which ranges from about 100 to 4,000 depending on your [compute size](https://neon.com/docs/reference/compatibility#parameter-settings-that-differ-by-compute-size).

You select pooled or direct by choosing the right connection string. Pooled strings include `-pooler` in the hostname:

```text
# Pooled
postgresql://user:pass@ep-cool-rain-123456-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# Direct
postgresql://user:pass@ep-cool-rain-123456.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

See [Connection pooling](https://neon.com/docs/connect/connection-pooling) for details.

### HTTP vs. WebSocket (serverless driver)

The [Neon serverless driver](https://neon.com/docs/serverless/serverless-driver) supports two transports:

- **HTTP** uses `fetch` requests. It is faster for single queries (~3 round trips vs. ~8 for TCP) and supports non-interactive transactions. Choose HTTP when your queries are independent, one-shot operations.
- **WebSocket** maintains a persistent connection within a request. It supports interactive transactions and is compatible with the `node-postgres` API (`Pool`, `Client`). Choose WebSocket when you need multi-step transactions or `pg` compatibility.

### Data API

The [Data API](https://neon.com/docs/data-api/overview) provides a REST interface to your database over HTTP. It works in browsers, edge runtimes, and anywhere you can make HTTP requests. It validates JWTs from any authentication provider and enforces PostgreSQL [Row-Level Security](https://neon.com/docs/guides/row-level-security), making it suitable for client-side apps that query the database directly.

## ORM compatibility

Popular JavaScript and TypeScript ORMs work with Neon across all connection methods. For non-JS/TS ORMs (Django, SQLAlchemy, ActiveRecord, Ecto), use your language's native Postgres driver with a [pooled connection](https://neon.com/docs/connect/choose-connection#pooled-vs-direct-connections).

| ORM     | Supported drivers                               | Guide                                                 |
| ------- | ----------------------------------------------- | ----------------------------------------------------- |
| Drizzle | `pg`, `postgres.js`, `@neondatabase/serverless` | [Drizzle guide](https://neon.com/docs/guides/drizzle) |
| Kysely  | `pg`, `postgres.js`, `@neondatabase/serverless` | [Kysely guide](https://neon.com/docs/guides/kysely)   |
| Prisma  | `pg`, `@neondatabase/serverless`                | [Prisma guide](https://neon.com/docs/guides/prisma)   |
| TypeORM | `pg`                                            | [TypeORM guide](https://neon.com/docs/guides/typeorm) |

Choose the driver based on your platform (see the scenarios above), then configure your ORM to use it.

## Common pitfalls

| Issue                | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Double pooling       | **Neon-side pooling** uses PgBouncer to manage connections between your app and Postgres. **Client-side pooling** occurs within your driver before connections reach PgBouncer.<br/><br/>If you use a pooled Neon connection, avoid adding client-side pooling on top. Let Neon handle it. If you must use client-side pooling, release connections back to the pool promptly to avoid conflicts with PgBouncer.                                                                                                                              |
| Understanding limits | `max_connections` is the maximum number of concurrent Postgres connections, determined by your [compute size](https://neon.com/docs/connect/connection-pooling#connection-limits-without-connection-pooling). `default_pool_size` is the maximum number of backend connections PgBouncer maintains per user/database pair.<br/><br/>Increasing your compute to raise `max_connections` may not help if `default_pool_size` is the bottleneck. To increase `default_pool_size`, contact [Support](https://neon.com/docs/introduction/support). |
| Use request handlers | In serverless environments (Vercel Edge Functions, Cloudflare Workers), WebSocket connections cannot outlive a single request. Create, use, and close `Pool` or `Client` objects **within the same request handler**. Do not create them outside a handler or reuse them across handlers. See [Pool and Client](https://github.com/neondatabase/serverless?tab=readme-ov-file#pool-and-client) for details.                                                                                                                                   |

---

## Related docs (Connect to Neon)

- [Connect to Neon](https://neon.com/docs/connect/connect-intro)
- [Connect from any app](https://neon.com/docs/connect/connect-from-any-app)
- [Neon serverless driver](https://neon.com/docs/serverless/serverless-driver)
- [Neon SQL Editor](https://neon.com/docs/get-started/query-with-neon-sql-editor)
- [Passwordless auth](https://neon.com/docs/connect/passwordless-connect)
- [Securing connections](https://neon.com/docs/connect/connect-securely)
- [Connection pooling](https://neon.com/docs/connect/connection-pooling)
- [Latency benchmarks](https://neon.com/docs/guides/benchmarking-latency)
```

### connect-postgres-gui.md

URL: https://neon.com/docs/connect/connect-postgres-gui.md
Hash: 1e25df5ad738

```
> This page location: Clients & tools > GUI applications
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Connect a GUI application

Learn how to connect a GUI application to Neon

This topic describes how to connect to a Neon database from a GUI application or IDE. Most GUI applications and IDEs that support connecting to a Postgres database also support connecting to Neon.

## Gather your connection details

The following details are typically required when configuring a connection:

- hostname
- port
- database name
- role (user)
- password

You can gather these details by clicking the **Connect** button on your **Project Dashboard** to open the **Connect to your database** modal. Select a branch, a role, and the database you want to connect to. A connection string is constructed for you.

![Connection details modal](https://neon.com/docs/connect/connection_details.png)

**Note:** Neon supports pooled and direct connections to the database. Use a pooled connection string if your application uses a high number of concurrent connections. For more information, see [Connection pooling](https://neon.com/docs/connect/connection-pooling#connection-pooling).

The connection string includes the role, password, hostname, and database name.

```text
postgresql://alex:AbC123dEf@ep-cool-darkness-123456.us-east-2.aws.neon.tech/dbname?sslmode=require&channel_binding=require
             ^              ^                                               ^
             |- <role>      |- <hostname>                                   |- <database>
```

- role name: `alex`
- hostname: `ep-cool-darkness-123456.us-east-2.aws.neon.tech`
- database name: `dbname`

Neon uses the default Postgres port, `5432`.

## Connect to the database

In the GUI application or IDE, enter the connection details into the appropriate fields and connect. Some applications permit specifying a connection string while others require entering connection details into separate fields. In the pgAdmin example below, connection details are entered into separate fields, and clicking **Save** establishes the database connection.

![Register - Server](https://neon.com/docs/connect/pgadmin4.png)

Some Java-based tools that use the pgJDBC driver for connecting to Postgres, such as DBeaver, DataGrip, and CLion, do not support including a role name and password in a database connection string or URL field. When you find that a connection string is not accepted, try entering the database name, role, and password values in the appropriate fields in the tool's connection UI when configuring a connection to Neon. For example, the DBeaver client has a **URL** field, but connecting to Neon requires specifying the connection details as shown:

![DBeaver connection](https://neon.com/docs/connect/dbeaver_connection.png)

## Tested GUI applications and IDEs

Connections from the GUI applications and IDEs in the table below have been tested with Neon.

**Note:** Some applications require an Server Name Indication (SNI) workaround. Neon uses compute domain names to route incoming connections. However, the Postgres wire protocol does not transfer the server domain name, so Neon relies on the Server Name Indication (SNI) extension of the TLS protocol to do this. Not all application clients support SNI. In these cases, a workaround is required. For more information, see [Connection errors](https://neon.com/docs/connect/connection-errors).

| Application or IDE                                                                                                            | Notes                                                                                                                                                                                                                                                                                                                                                                                                   |
| :---------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Appsmith](https://www.appsmith.com/)                                                                                         |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [AskYourDatabase](https://www.askyourdatabase.com/)                                                                           |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)                                                           | Use [SNI workaround D](https://neon.com/docs/connect/connection-errors#d-specify-the-endpoint-id-in-the-password-field). Use a `$` character as a separator between the `endpoint` option and password. For example: `endpoint=<endpoint_id>$<password>`. Also, you must set **Secure Socket Layer (SSL) mode** to `require`. See [Migrate with AWS DMS](https://neon.com/docs/import/migrate-aws-dms). |
| [Azure Data Studio](https://azure.microsoft.com/en-us/products/data-studio/)                                                  | Requires the [PostgreSQL extension](https://learn.microsoft.com/en-us/sql/azure-data-studio/extensions/postgres-extension?view=sql-server-ver16) and [SNI workaround D](https://neon.com/docs/connect/connection-errors#d-specify-the-endpoint-id-in-the-password-field)                                                                                                                                |
| [Beekeeper Studio](https://www.beekeeperstudio.io/)                                                                           | Requires the **Enable SSL** option                                                                                                                                                                                                                                                                                                                                                                      |
| [CLion](https://www.jetbrains.com/clion/)                                                                                     |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Datagran](https://www.datagran.io/)                                                                                          | Requires [SNI workaround D](https://neon.com/docs/connect/connection-errors#d-specify-the-endpoint-id-in-the-password-field) connection workaround                                                                                                                                                                                                                                                      |
| [DataGrip](https://www.jetbrains.com/datagrip/)                                                                               |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [DBeaver](https://dbeaver.io/)                                                                                                | To prevent scale-to-zero from interrupting an idle connection, go to **Edit Connection** > **Connection Settings** > **Initialization** and set **Keep-Alive (seconds)** to `60`.                                                                                                                                                                                                                       |
| [dbForge](https://www.devart.com/dbforge/)                                                                                    |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [DbVisualizer](https://www.dbvis.com/)                                                                                        |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [DBX](https://getdbx.com/)                                                                                                    |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [DB Pro](https://dbpro.app)                                                                                                   |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Draxlr](https://www.draxlr.com/)                                                                                             |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [DronaHQ hosted cloud version](https://www.dronahq.com/)                                                                      | Requires selecting **Connect using SSL** when creating a connector                                                                                                                                                                                                                                                                                                                                      |
| [Forest Admin](https://www.forestadmin.com/)                                                                                  | The database requires at least one table                                                                                                                                                                                                                                                                                                                                                                |
| [Grafana](https://grafana.com/docs/grafana/latest/datasources/postgres/)                                                      | Requires `sslmode=verify-full`. See [SNI workaround C](https://neon.com/docs/connect/connection-errors#c-set-verify-full-for-golang-based-clients).                                                                                                                                                                                                                                                     |
| [Google Looker Studio](https://lookerstudio.google.com/)                                                                      | Requires **Enable SSL** and uploading the PEM-encoded ISRG Root X1 public root certificate issued by Let's Encrypt, which you can find here: [isrgrootx1.pem](https://letsencrypt.org/certs/isrgrootx1.pem). See the [Looker Studio guide](https://neon.com/docs/connect/connect-looker-studio) for detailed connection instructions.                                                                   |
| [Google Cloud Platform (GCP)](https://cloud.google.com/gcp)                                                                   | May require uploading the PEM-encoded ISRG Root X1 public root certificate issued by Let's Encrypt, which you can find here: [isrgrootx1.pem](https://letsencrypt.org/certs/isrgrootx1.pem).                                                                                                                                                                                                            |
| [Google Colab](https://colab.research.google.com/)                                                                            | See [Use Google Colab with Neon](https://neon.com/docs/ai/ai-google-colab).                                                                                                                                                                                                                                                                                                                             |
| [Luna Modeler](https://www.datensen.com/data-modeling/luna-modeler-for-relational-databases.html)                             | Requires enabling the SSL/TLS option                                                                                                                                                                                                                                                                                                                                                                    |
| [Metabase](https://www.metabase.com/)                                                                                         |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Postico](https://eggerapps.at/postico2/)                                                                                     | SNI support since v1.5.21. For older versions, use [SNI workaround B](https://neon.com/docs/connect/connection-errors#b-use-libpq-keyvalue-syntax-in-the-database-field). Postico's [keep-connection-alive mechanism](https://eggerapps.at/postico/docs/v1.2/changelist.html), enabled by default, may prevent your compute from scaling to zero.                                                       |
| [PostgreSQL VS Code Extension by Chris Kolkman](https://marketplace.visualstudio.com/items?itemName=ckolkman.vscode-postgres) |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [pgAdmin 4](https://www.pgadmin.org/)                                                                                         |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Retool](https://retool.com/)                                                                                                 |                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Tableau](https://www.tableau.com/)                                                                                           | Use the PostgreSQL connector with the **Require SSL** option selected                                                                                                                                                                                                                                                                                                                                   |
| [TablePlus](https://tableplus.com/)                                                                                           | SNI support on macOS since build 436, and on Windows since build 202. No SNI support on Linux currently. For older versions, use [SNI workaround B](https://neon.com/docs/connect/connection-errors#b-use-libpq-keyvalue-syntax-in-the-database-field).                                                                                                                                                 |
| [Segment](https://segment.com/)                                                                                               | Requires [SNI workaround D](https://neon.com/docs/connect/connection-errors#d-specify-the-endpoint-id-in-the-password-field)                                                                                                                                                                                                                                                                            |
| [Skyvia](https://skyvia.com/)                                                                                                 | Requires setting the **SSL Mode** option to `Require`, and **SSL TLS Protocol** to 1.2. The other SSL fields are not required for **SSL Mode**: `Require`.                                                                                                                                                                                                                                              |
| [Zoho Analytics](https://www.zoho.com/analytics/)                                                                             | Requires selecting **Other Cloud Services** as the Cloud Service Provider, and the **Connect directly using IP address** and **Use SSL** options when configuring a PostgreSQL connection.                                                                                                                                                                                                              |

## Connecting from Business Intelligence (BI) tools

When connecting from BI tools like Metabase, Tableau, or Power BI, we recommend using a **read replica** instead of your main database compute. BI tools often run long or resource-intensive queries, which can impact performance on your primary branch. Read replicas can scale independently and handle these workloads without affecting your main production traffic. To learn more, see [Neon read replicas](https://neon.com/docs/introduction/read-replicas).

## Connection issues

Applications that use older client libraries or drivers that do not support Server Name Indication (SNI) may not permit connecting to Neon. If you encounter the following error, refer to [Connection errors](https://neon.com/docs/connect/connection-errors) for possible workarounds.

```txt
ERROR: The endpoint ID is not specified. Either upgrade the Postgres client library (libpq) for SNI support or pass the endpoint ID (the first part of the domain name) as a parameter: '&options=endpoint%3D'. See [https://neon.com/sni](https://neon.com/sni) for more information.
```

---

## Related docs (Clients & tools)

- [psql](https://neon.com/docs/connect/query-with-psql-editor)
- [pgcli](https://neon.com/docs/connect/connect-pgcli)
- [Looker Studio](https://neon.com/docs/connect/connect-looker-studio)
```

### connect-from-any-app.md

URL: https://neon.com/docs/connect/connect-from-any-app.md
Hash: d09cb8a3b0e6

```
> This page location: Connect to Neon > Connect from any app
> Full Neon documentation index: https://neon.com/docs/llms.txt

# Connect from any application

Learn how to connect to Neon from any application

**What you will learn:**

- Where to find database connections details
- Where to find example connection snippets
- Protocols supported by Neon

**Related topics**

- [Choosing a driver and connection type](https://neon.com/docs/connect/choose-connection)
- [Neon VS Code Extension](https://neon.com/docs/local/vscode-extension)
- [Connect to Neon securely](https://neon.com/docs/connect/connect-securely)
- [Connection pooling](https://neon.com/docs/connect/connection-pooling)
- [Connect with psql](https://neon.com/docs/connect/query-with-psql-editor)

You can connect to your Neon database from any application. The standard method is to copy your [connection string](https://neon.com/docs/connect/connect-from-any-app#get-a-connection-string-from-the-neon-console) from the Neon console and use it in your app or client. For a streamlined development experience, you can also use the [Neon VS Code extension](https://neon.com/docs/connect/connect-from-any-app#connect-with-the-neon-vs-code-extension) to manage connections, browse schemas, and run queries directly in your editor.

**Important:** You are responsible for maintaining the records and associations of any connection strings in your environment and systems.

## Get a connection string from the Neon console

When connecting to Neon from an application or client, you connect to a database in your Neon project. In Neon, a database belongs to a branch, which may be the default branch of your project (`main`) or a child branch.

You can find the connection details for your database by clicking the **Connect** button on your **Project Dashboard**. This opens the **Connect to your database** modal. Select a branch, a compute, a database, and a role. A connection string is constructed for you.

![Connection details modal](https://neon.com/docs/connect/connection_details.png)

Neon supports both pooled and direct connections to your database. Neon's connection pooler supports a higher number of concurrent connections, so we provide pooled connection details in the **Connect to your database** modal by default, which adds a `-pooler` option to your connection string. If needed, you can get direct database connection details from the modal disabling the **Connection pooling** toggle. For more information about pooled connections, see [Connection pooling](https://neon.com/docs/connect/connection-pooling#connection-pooling).

A Neon connection string includes the role, password, hostname, and database name.

```text
postgresql://alex:AbC123dEf@ep-cool-darkness-a1b2c3d4-pooler.us-east-2.aws.neon.tech/dbname?sslmode=require&channel_binding=require
             ^    ^         ^                         ^                              ^
       role -|    |         |- hostname               |- pooler option               |- database
                  |
                  |- password
```

**Note:** The hostname includes the ID of the compute, which has an `ep-` prefix: `ep-cool-darkness-123456`. For more information about Neon connection strings, see [connection string](https://neon.com/docs/reference/glossary#connection-string).

You can use the details from the **Connect to your database** modal to configure your database connection. For example, you might place the connection details in an `.env` file, assign the connection string to a variable, or pass the connection string on the command-line.

**.env file**

```text
PGHOST=ep-cool-darkness-a1b2c3d4-pooler.us-east-2.aws.neon.tech
PGDATABASE=dbname
PGUSER=alex
PGPASSWORD=AbC123dEf
PGPORT=5432
```

**Variable**

```text
DATABASE_URL="postgresql://alex:AbC123dEf@ep-cool-darkness-a1b2c3d4-pooler.us-east-2.aws.neon.tech/dbname?sslmode=require&channel_binding=require"
```

**Command-line**

```bash
psql postgresql://alex:AbC123dEf@ep-cool-darkness-a1b2c3d4-pooler.us-east-2.aws.neon.tech/dbname?sslmode=require&channel_binding=require
```

**Note:** Neon requires that all connections use SSL/TLS encryption, but you can increase the level of protection by configuring the `sslmode` option. For more information, see [Connect to Neon securely](https://neon.com/docs/connect/connect-securely).

## Connect with the Neon VS Code extension

The [Neon VS Code extension](https://neon.com/docs/local/vscode-extension) lets you connect to any Neon branch and manage your database directly in your IDE. Available for VS Code, Cursor, and other VS Code-compatible editors, this extension lets you:

- Connect to any Neon project and branch with automatic detection of connection strings in your workspace
- Copy connection strings directly to your `.env` file
- Browse database schemas, run SQL queries, and edit table data
- Create and manage branches directly from your editor
- Enable AI-powered database features with automatic MCP Server configuration

The extension provides a streamlined workflow for working with Neon during development without leaving your editor.

## Where can I find my password?

It's included in your Neon connection string. Click the **Connection** button on your **Project Dashboard** to open the **Connect to your database** modal.

### Save your connection details to 1Password

If have a [1Password](https://1password.com/) browser extension, you can save your database connection details to 1Password directly from the Neon Console. In your **Project Dashboard**, click **Connect**, then click **Save in 1Password**.

![1Password button on connection modal](https://neon.com/docs/connect/1_password_button.png)

## What port does Neon use?

Neon uses the default Postgres port, `5432`.

## Connection examples

The **Connect to your database** modal provides connection examples for different frameworks and languages, constructed for the branch, database, and role that you select.

![Language and framework connection examples](https://neon.com/docs/connect/code_connection_examples.png)

See our [frameworks](https://neon.com/docs/get-started/frameworks) and [languages](https://neon.com/docs/get-started/languages) guides for more connection examples.

## Network protocol support

Neon projects provisioned on AWS support both [IPv4](https://en.wikipedia.org/wiki/Internet_Protocol_version_4) and [IPv6](https://en.wikipedia.org/wiki/IPv6) addresses. Neon projects provisioned on Azure support IPv4.

Additionally, Neon provides a low-latency serverless driver that supports connections over WebSockets and HTTP. Great for serverless or edge environments where connections over TCP may not be not supported. For further information, refer to our [Neon serverless driver](https://neon.com/docs/serverless/serverless-driver) documentation.

## Connection notes

- Some older Postgres client libraries and drivers, including older `psql` executables, are built without [Server Name Indication (SNI)](https://neon.com/docs/reference/glossary#sni) support, which means that a connection workaround may be required. For more information, see [Connection errors: The endpoint ID is not specified](https://neon.com/docs/connect/connection-errors#the-endpoint-id-is-not-specified).
- Some Java-based tools that use the pgJDBC driver for connecting to Postgres, such as DBeaver, DataGrip, and CLion, do not support including a role name and password in a database connection string or URL field. When you find that a connection string is not accepted, try entering the database name, role, and password values in the appropriate fields in the tool's connection UI when configuring a connection to Neon. For examples, see [Connect a GUI or IDE](https://neon.com/docs/connect/connect-postgres-gui#connect-to-the-database).
- When connecting from BI tools like Metabase, Tableau, or Power BI, we recommend using a **read replica** instead of your main database compute. BI tools often run long or resource-intensive queries, which can impact performance on your primary branch. Read replicas can scale independently and handle these workloads without affecting your main production traffic. To learn more, see [Neon read replicas](https://neon.com/docs/introduction/read-replicas).

---

## Related docs (Connect to Neon)

- [Connect to Neon](https://neon.com/docs/connect/connect-intro)
- [Choosing your connection method](https://neon.com/docs/connect/choose-connection)
- [Neon serverless driver](https://neon.com/docs/serverless/serverless-driver)
- [Neon SQL Editor](https://neon.com/docs/get-started/query-with-neon-sql-editor)
- [Passwordless auth](https://neon.com/docs/connect/passwordless-connect)
- [Securing connections](https://neon.com/docs/connect/connect-securely)
- [Connection pooling](https://neon.com/docs/connect/connection-pooling)
- [Latency benchmarks](https://neon.com/docs/guides/benchmarking-latency)
```

---

Crawl complete: 20 pages fetched, 0 errors
