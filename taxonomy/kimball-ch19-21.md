---
source: file://kimball-ch19-21.md
domain: local
crawled_at: 2026-03-31T21:40:31Z
index_hash: 09de02cdb60c
page_count: 3
---

# Kimball Data Warehouse Toolkit 3e -- Chapters 19-21 Taxonomy

## Pages

### chapter-19-etl-subsystems-and-techniques-pp-443-496

URL: https://local.taxonomy/kimball-ch19-21/chapter-19-etl-subsystems-and-techniques-pp-443-496
Hash: ea99522e5efd

```
### Overview
- ETL = Extract, Transform, Load (also ELT)
- 34 subsystems organized into 4 major categories
- ETL system is the foundation of the data warehouse

### Category 1: EXTRACTING (Subsystems 1-3)

#### Subsystem 1: Data Profiling
- Investigate source data content, structure, and quality
- Technical profiling
  - Column analysis (nulls, distinct values, distributions, min/max, patterns)
  - Structure analysis (key relationships, orphan records, functional dependencies)
  - Metadata verification
- Business profiling
  - Business rule validation
  - Domain integrity
- Profiling tools vs hand-coded SQL
- Should be iterative and continuous, not one-time

#### Subsystem 2: Change Data Capture (CDC) System
- Techniques for detecting changes in source data
  - Audit columns (date/time stamps, update flags)
    - Relies on source system discipline
    - Fragile if source system changes
  - Timed extracts
    - Periodic snapshots based on time windows
    - May miss intra-period changes
  - Full diff compare
    - Compare current extract to prior extract
    - Resource-intensive but reliable
    - Useful when source has no audit columns
  - Database log scraping
    - Read database transaction logs
    - Near-real-time capability
    - Database-vendor specific
    - Requires DBA cooperation
  - Message queue monitoring
    - Intercept application-layer messages
    - Closest to real-time
    - Requires application integration
- CDC choice depends on source system capabilities and latency requirements

#### Subsystem 3: Extract System
- File-based extraction
  - Flat files (delimited, fixed-width)
  - XML files
  - Spreadsheets
  - Full vs incremental extracts
- Streaming extraction
  - Real-time feeds
  - Message queues
  - Change data streams
- Extract considerations
  - Source system impact (query load)
  - Extract scheduling and windows
  - Data staging area design
  - File naming conventions and manifests

---

### Category 2: CLEANING AND CONFORMING (Subsystems 4-8)

#### Subsystem 4: Data Cleansing System
- Quality screens (filters applied to data stream)
  - Column screens
    - Null value checks
    - Valid value range checks
    - Pattern/format checks
    - Domain membership checks
  - Structure screens
    - Referential integrity checks
    - Primary key uniqueness
    - Foreign key validity
    - Cross-column dependency checks
  - Business rule screens
    - Complex multi-column validations
    - Cross-table consistency
    - Temporal consistency
    - Business logic enforcement
- Screen severity levels
  - Fatal: halt processing
  - Warning: flag and continue
  - Information: log only
- Responding to quality events
  - Halt and fix
  - Send to suspense file for later resolution
  - Tag and publish with quality indicators
  - Correct automatically (with audit trail)
- Data quality measurement and reporting

#### Subsystem 5: Error Event Schema
- Dimensional model for tracking ETL errors
- Error event fact table
  - One row per error event
  - Grain: individual error occurrence
  - Measures: error severity score, record counts
- Error event detail fact table
  - Specific field-level error details
  - Before/after values
- Key dimensions
  - Screen dimension (which quality screen fired)
  - Batch dimension (which ETL batch)
  - Date dimension
  - Time dimension
  - Source system dimension
  - Error type dimension
- Enables quality trend analysis and accountability

#### Subsystem 6: Audit Dimension Assembler
- Captures ETL processing metadata alongside fact rows
- Audit dimension attributes
  - Source system identifier
  - Extract timestamp
  - Load timestamp
  - Quality score/confidence level
  - Screen results summary
  - Batch identifier
  - ETL version information
- Attached to fact tables as a regular dimension
- Enables end-user visibility into data lineage and trustworthiness
- Supports regulatory compliance requirements

#### Subsystem 7: Deduplication System
- Matching techniques
  - Exact matching (deterministic)
  - Fuzzy/probabilistic matching
  - Phonetic algorithms (Soundex, Metaphone)
  - Edit distance / string similarity
  - Address standardization and matching
- Survivorship rules
  - Which record "wins" for each attribute
  - Most recent, most complete, most trusted source
  - Golden record construction
- Householding (grouping related entities)
- Master data management integration
- Match/merge vs link/reference approaches

#### Subsystem 8: Conforming System
- Conformed dimensions
  - Shared dimensions used across multiple fact tables
  - Identical dimension tables or proper subsets
  - Enable drill-across queries
  - Managed centrally
  - Examples: customer, product, date, employee
- Conformed facts
  - Consistent fact definitions across business processes
  - Same units of measure
  - Same calculation formulas
  - Enable meaningful cross-process comparisons
- Conforming techniques
  - Master data standardization
  - Code translation and mapping
  - Value normalization
  - Hierarchical alignment

---

### Category 3: DELIVERING (Subsystems 9-21)

#### Subsystem 9: Slowly Changing Dimension (SCD) Manager
- Type 0: Retain Original
  - Never change the dimension attribute
  - Appropriate for original/initial values
- Type 1: Overwrite
  - Replace old value with new value
  - No history preserved
  - Simplest approach
- Type 2: Add New Row
  - Create new dimension row with new value
  - Preserve full history
  - Uses surrogate keys, effective dates, current flag
  - Most common for tracking history
- Type 3: Add New Attribute
  - Add new column for prior value
  - Limited history (current + previous only)
  - Useful for "alternate rollup" tracking
- Type 4: Mini-Dimension
  - Split rapidly changing attributes into separate dimension
  - Reduces Type 2 row explosion
  - Mini-dimension joined to fact via separate key
- Type 5: Type 4 + Type 1 Outrigger
  - Mini-dimension plus Type 1 reference on base dimension
  - Provides current mini-dimension profile on base dimension
- Type 6: Type 1 + Type 2 + Type 3 Hybrid
  - Adds Type 1 overwritten current value column to Type 2 row
  - Enables both historical and current-value analysis
- Type 7: Dual Type 1 and Type 2 Dimensions
  - Fact table has both surrogate key (Type 2) and durable natural key (Type 1)
  - Two dimension table joins possible
  - Maximizes analytical flexibility

#### Subsystem 10: Surrogate Key Generator
- Assign integer surrogate keys to all dimension rows
- Independent of source system natural keys
- Key generation approaches
  - Sequential integer assignment
  - Database sequence/identity columns
  - ETL-managed counters
- Benefits
  - Insulate from source system key changes
  - Enable Type 2 SCD tracking
  - Improve join performance (integer vs string)
  - Handle multiple source systems
  - Support null/unknown/not applicable members

#### Subsystem 11: Hierarchy Manager
- Fixed-depth hierarchies
  - Known number of levels
  - Separate columns for each level
  - Simplest to query
- Variable-depth (ragged) hierarchies
  - Unknown number of levels
  - Recursive parent-child structure
  - Bridge table approach for flattening
  - Pathstring column approach
- Hierarchy flattening techniques
- Multiple simultaneous hierarchies on same dimension

#### Subsystem 12: Special Dimensions Manager
- Date dimension
  - Calendar attributes, fiscal attributes, holiday flags
  - Pre-loaded for many years
- Time-of-day dimension
  - Separate from date for finer granularity
- Junk dimension
  - Combine miscellaneous low-cardinality flags/indicators
  - Cartesian product of possible combinations
  - Avoid proliferating foreign keys on fact table
- Mini-dimensions
  - Rapidly changing attributes separated from base dimension
  - Band/bucket demographic-style attributes
- Shrunken/subset dimensions
  - Strict subset of rows and/or columns from base dimension
  - Conformed subset for higher-grain fact tables
- Small static dimensions
  - Transaction type, status codes
  - Loaded once, rarely change
- User-maintained dimensions
  - Business users maintain attributes directly
  - Spreadsheet-fed dimensions

#### Subsystem 13: Fact Table Builders
- Transaction grain fact table loader
  - One row per transaction event
  - Insert-only (generally no updates)
  - Most fundamental grain
- Periodic snapshot fact table loader
  - One row per entity per time period
  - Full replacement or insert for each period
  - Cumulative or status measures
- Accumulating snapshot fact table loader
  - One row per entity lifecycle
  - Multiple date stamps for milestones
  - Updated as entity progresses through process
  - Lag calculations between milestones

#### Subsystem 14: Surrogate Key Pipeline
- Look up surrogate keys for all dimension references in fact rows
- Pipeline architecture for high-volume lookups
- In-memory hash tables for lookup performance
- Handle lookup failures (late-arriving dimensions)
- Multi-pass processing for complex key relationships
- Critical performance bottleneck -- must be optimized

#### Subsystem 15: Multivalued Dimension Bridge Table Builder
- Handle many-to-many relationships between facts and dimensions
- Bridge table sits between fact and dimension
- Weighting factors for allocation
- Examples
  - Multiple diagnoses per patient encounter
  - Multiple authors per publication
  - Multiple account holders per account
- Group keys for managing sets of related dimension members

#### Subsystem 16: Late Arriving Data Handler
- Late arriving facts
  - Facts that arrive after their normal processing window
  - Insert with correct date key based on event date
  - May affect previously published aggregates
- Late arriving dimension rows
  - Dimension context arrives after related facts
  - Create inferred/placeholder dimension member
  - Update inferred member when full data arrives
  - Must handle Type 2 corrections retroactively

#### Subsystem 17: Dimension Manager System
- Centralized management of conformed dimensions
- Single authoritative source for shared dimensions
- Publication and distribution to multiple data marts
- Version control of dimension content
- Coordinated updates across consuming systems
- Gold, silver, bronze dimension quality tiers

#### Subsystem 18: Fact Provider System
- Counterpart to Dimension Manager for facts
- Coordinate fact table loading across data marts
- Ensure consistent grain and measures
- Manage fact table partitioning
- Handle incremental loads and full refreshes

#### Subsystem 19: Aggregate Builder
- Create and maintain aggregate (summary) tables
- Aggregate navigation (transparent query redirection)
- Shrunken dimensions for aggregate fact tables
- Aggregate strategies
  - Pre-built static aggregates
  - Dynamic aggregation
  - Materialized views
- Aggregate maintenance on dimension changes
- Balance storage cost vs query performance

#### Subsystem 20: OLAP Cube Builder
- Build multidimensional cubes from dimensional models
- MOLAP vs ROLAP vs HOLAP considerations
- Cube partitioning strategies
- Calculated measures and MDX expressions
- Cube refresh and incremental processing
- Security and access control at cube level

#### Subsystem 21: Data Propagation Manager
- Distribute data from DW/BI to downstream systems
- Backroom-to-front-room data movement
- Publication to operational systems (reverse ETL)
- Data feeds to external partners
- Export format management
- Scheduling and dependency management

---

### Category 4: MANAGING (Subsystems 22-34)

#### Subsystem 22: Job Scheduler
- Job definition and dependency management
- Scheduling (time-based, event-based, dependency-based)
- Metadata capture during execution
- Logging (start/end times, row counts, status)
- Notification (success, failure, warning alerts)
- Restart and recovery integration
- Workload balancing

#### Subsystem 23: Backup System
- Backup strategies
  - Full, differential, incremental
  - Hot vs cold backups
- Archive and retrieval
  - Long-term data retention
  - Regulatory compliance
  - Tiered storage
- Backup of ETL code, metadata, and configurations
- Disaster recovery planning

#### Subsystem 24: Recovery and Restart System
- Checkpoint/restart capabilities
- Rollback on failure
- Idempotent processing (safe to re-run)
- Partial load recovery
- Transaction management in ETL context
- Graceful degradation strategies

#### Subsystem 25: Version Control System
- Version control of ETL jobs and code
- Mapping specifications versioning
- Configuration management
- Development/test/production promotion paths
- Source code repository integration

#### Subsystem 26: Version Migration System
- Migrate ETL changes between environments
- Development to test to production promotion
- Rollback capabilities
- Environment-specific configuration management
- Release packaging and deployment

#### Subsystem 27: Workflow Monitor
- Real-time visibility into ETL processing
- Dashboard for job status
- Performance metrics and trends
- Bottleneck identification
- SLA compliance tracking
- Historical run analysis

#### Subsystem 28: Sorting System
- High-performance sorting for large data volumes
- Sort key optimization
- External sort algorithms for datasets exceeding memory
- Sort as prerequisite for merge, dedup, and lookup operations
- Parallel sort capabilities

#### Subsystem 29: Lineage and Dependency Analyzer
- Data lineage tracking (source to target mapping)
- Impact analysis (what breaks if source changes)
- Forward and backward tracing
- Column-level lineage
- Business glossary integration
- Regulatory audit support

#### Subsystem 30: Problem Escalation System
- Automated escalation procedures
- Tiered support levels
- Notification chains
- Issue tracking integration
- Root cause analysis support
- Runbook automation

#### Subsystem 31: Parallelizing/Pipelining System
- Parallel processing strategies
  - Pipeline parallelism (stages run concurrently)
  - Data parallelism (partition data across processors)
  - Component parallelism (independent tasks run simultaneously)
- Thread and process management
- Resource contention management
- Scalability considerations

#### Subsystem 32: Security System
- Authentication and authorization for ETL processes
- Data encryption (in transit, at rest)
- Sensitive data masking/tokenization
- Role-based access control
- Audit trail of data access
- Compliance with privacy regulations

#### Subsystem 33: Compliance Manager
- Regulatory compliance enforcement
- Data retention policies
- Right-to-be-forgotten support
- Audit readiness
- Policy-driven data handling
- Compliance reporting and documentation

#### Subsystem 34: Metadata Repository Manager
- Technical metadata (table definitions, ETL mappings, schedules)
- Business metadata (definitions, owners, stewards)
- Process metadata (run statistics, data quality scores)
- Metadata integration across tools
- Metadata browsing and search
- Impact analysis from metadata relationships

---
```

### chapter-20-etl-system-design-and-development-process-pp-497-

URL: https://local.taxonomy/kimball-ch19-21/chapter-20-etl-system-design-and-development-process-pp-497-
Hash: 61be3ed95643

```
### The 10-Step ETL System Design Process

#### Step 1: Draw the High-Level Plan
- Map source systems to target dimensional model
- Identify all source-to-target data flows
- Document at logical level before physical design
- Create visual data flow diagrams
- Identify major transformation requirements

#### Step 2: Choose an ETL Tool
- Hand-coded vs commercial ETL tool decision
- Evaluation criteria
  - Connectivity to source and target systems
  - Transformation capabilities
  - Metadata management
  - Scalability and performance
  - Developer productivity
  - Monitoring and operations support
- Build vs buy trade-offs
- Team skill assessment

#### Step 3: Develop Default Strategies
- Standard approaches for common ETL patterns
  - SCD handling defaults (which types for which attributes)
  - Surrogate key assignment strategy
  - Null handling conventions
  - Error handling defaults
  - Audit dimension population
  - Naming conventions
  - Logging standards
- Document in ETL standards guide
- Reduces per-table design effort

#### Step 4: Drill Down by Target Table
- Detailed source-to-target mapping for each table
- Column-level transformation specifications
- Data type conversions
- Business rule documentation
- Lookup and reference data requirements
- Exception handling per column/table

#### Step 5: Populate Dimension Tables with Historic Data
- Initial/historical load of dimension tables
- Establish surrogate key assignments
- Build Type 2 history from available snapshots
- Handle missing history gracefully
- Quality assurance of dimension content
- Performance considerations for large dimensions

#### Step 6: Perform the Fact Table Historic Load
- Initial load of fact tables with historical data
- Surrogate key lookup for all dimensions
- Handle orphan fact rows (missing dimension members)
- Grain verification
- Partitioning strategy for large fact loads
- Validation and reconciliation

#### Step 7: Dimension Table Incremental Processing
- Ongoing dimension updates
- Apply SCD logic per attribute
- Process new members
- Handle deleted source records
- Coordinate timing with fact table loads
- Conformed dimension synchronization

#### Step 8: Fact Table Incremental Processing
- Ongoing fact table loads
- Late arriving fact handling
- Surrogate key pipeline for lookups
- Incremental aggregation updates
- Partition management
- Error handling and reprocessing

#### Step 9: Aggregate Table and OLAP Loads
- Build and maintain aggregate tables
- Cube processing
- Aggregate navigation metadata
- Refresh strategies (rebuild vs incremental)
- Performance monitoring and tuning

#### Step 10: ETL System Operation and Automation
- Production deployment
- Job scheduling and orchestration
- Monitoring and alerting
- Capacity planning
- Documentation and runbooks
- Ongoing performance tuning

### Real-Time ETL Implications

#### Triage: Three Levels of Real-Time
- Daily (batch)
  - Traditional nightly/periodic batch processing
  - Most common and well-understood
  - Acceptable for many business requirements
- Intra-day (micro-batch)
  - Multiple batches per day (hourly, every 15 minutes)
  - Mini-batch approach
  - Moderate complexity increase
  - Suitable for semi-urgent business needs
- Instantaneous (streaming)
  - Near-zero latency
  - Event-driven processing
  - Significant architecture changes required
  - Reserved for truly time-critical needs

#### Real-Time Architecture Considerations
- Real-time partition in presentation server
  - Separate real-time partition from static partition
  - Union at query time
  - Real-time partition rebuilt frequently
  - Static partition loaded traditionally
- Hot partition design
  - Small, frequently refreshed
  - Merged into main fact table periodically
- Dual-speed architecture trade-offs
- Impact on dimensions (real-time dimension updates)
- Impact on aggregates

---
```

### chapter-21-big-data-analytics-pp-527-542

URL: https://local.taxonomy/kimball-ch19-21/chapter-21-big-data-analytics-pp-527-542
Hash: 51d5cf052732

```
### Big Data Overview
- Volume, Velocity, Variety characteristics
- Use cases for big data in DW/BI context
- Complement to (not replacement for) traditional DW
- Structured, semi-structured, unstructured data integration

### Big Data Architecture Approaches

#### Extended RDBMS Architecture
- Scale-up traditional relational databases
- Columnar storage engines
- In-memory databases
- Massively Parallel Processing (MPP) appliances
- Enhanced SQL capabilities (window functions, analytics)
- Familiar tooling and skill sets

#### MapReduce/Hadoop Architecture
- Distributed file system (HDFS)
- MapReduce processing paradigm
- Map phase: distribute and filter
- Reduce phase: aggregate and combine
- Hadoop ecosystem components
  - Hive (SQL-like interface)
  - Pig (data flow scripting)
  - HBase (NoSQL columnar store)
  - Sqoop (RDBMS-Hadoop data transfer)
  - Flume (log/event data collection)
- Schema-on-read vs schema-on-write
- Commodity hardware, horizontal scaling

#### Comparison of Architectures
- RDBMS strengths: mature, SQL-based, ACID compliance, tooling
- Hadoop strengths: cost, scalability, unstructured data, schema flexibility
- Convergence trends: SQL-on-Hadoop, NewSQL
- Hybrid architectures combining both

### Recommended Best Practices

#### Management Best Practices
- Structure organizational efforts around analytics outcomes
- Delay building legacy-style environments for new data types
- Build production systems from successful sandbox/prototype results
- Try simple applications first before complex ones
- Manage expectations about big data capabilities

#### Architecture Best Practices
- Plan a data highway with 5 caches of increasing latency
  - Cache 1: Raw ingestion (landing zone)
  - Cache 2: Cleaned/standardized staging
  - Cache 3: Detailed dimensional model
  - Cache 4: Aggregated/curated data marts
  - Cache 5: Published analytics/reporting layer
- Build fact extractor components from big data sources
- Build comprehensive data ecosystems (not isolated silos)
- Plan for data quality from the start
- Add value to data as soon as possible after ingestion
- Implement backflow to earlier caches (feedback loops)
- Implement streaming data capabilities where needed
- Avoid boundary crashes (design for graceful scaling)
- Move successful prototypes from sandbox to private cloud
- Strive for continuous performance improvements
- Monitor compute resources proactively
- Exploit in-database analytics (push computation to data)

#### Data Modeling Best Practices
- Think dimensionally even in big data contexts
- Integrate with conformed dimensions (bridge big data to enterprise DW)
- Anchor with durable surrogate keys
- Expect to integrate structured and unstructured data
- Use Slowly Changing Dimensions in big data
- Declare data structure at analysis time (schema-on-read)
- Load data as name-value pairs when structure is variable
- Rapidly prototype using data virtualization

#### Governance Best Practices
- No such thing as "big data governance" in isolation
  - Governance must span all data regardless of platform
- Dimensionalize data before applying governance rules
- Privacy is the most important governance concern
  - PII protection
  - Data masking and anonymization
  - Access controls and audit
- Never choose big data technology over governance requirements
  - Compliance and governance trump architecture preferences
```
