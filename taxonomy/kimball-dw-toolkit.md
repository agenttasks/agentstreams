---
source: ** Ralph Kimball & Margy Ross, *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling*, 3rd Ed. (Wiley, 2013)
domain: local
crawled_at: 2026-03-31T21:40:31Z
index_hash: 7062ac996609
page_count: 26
---

# Kimball Data Warehouse Toolkit — 3rd Edition

## Pages

### complete-taxonomy

URL: https://local.taxonomy/kimball-dw-toolkit/complete-taxonomy
Hash: ad7e9b159c37

```
> **Source:** Ralph Kimball & Margy Ross, *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling*, 3rd Ed. (Wiley, 2013)
> **PDF:** `/Users/alexzh/agenttasks/agenttasks/customers/neondatabase/kimball-data-warehouse-toolkit-3e.pdf`
> **Extraction date:** 2026-03-31
> **Method:** Parallel subagent extraction, 20 pages at a time, taxonomy tree format

---
```

### book-structure

URL: https://local.taxonomy/kimball-dw-toolkit/book-structure
Hash: e16f45af6662

```
| Ch | Title | Pages | Domain |
|----|-------|-------|--------|
| 1 | DW, BI, and Dimensional Modeling Primer | 1-35 | Foundations |
| 2 | Kimball Dimensional Modeling Techniques Overview | 37-68 | Techniques Reference |
| 3 | Retail Sales | 69-109 | Case Study |
| 4 | Inventory | 111-139 | Case Study |
| 5 | Procurement | 141-165 | Case Study |
| 6 | Order Management | 167-199 | Case Study |
| 7 | Accounting | 201-227 | Case Study |
| 8 | Customer Relationship Management | 229-261 | Case Study |
| 9 | Human Resources Management | 263-279 | Case Study |
| 10 | Financial Services | 281-296 | Case Study |
| 11 | Telecommunications | 297-324 | Case Study |
| 12 | Transportation | 311-324 | Case Study |
| 13 | Education | 325-336 | Case Study |
| 14 | Healthcare | 339-352 | Case Study |
| 15 | Electronic Commerce | 353-373 | Case Study |
| 16 | Insurance | 375-401 | Case Study |
| 17 | Kimball DW/BI Lifecycle Overview | 403-427 | Methodology |
| 18 | Dimensional Modeling Process and Tasks | 429-441 | Methodology |
| 19 | ETL Subsystems and Techniques | 443-496 | ETL (34 subsystems) |
| 20 | ETL System Design and Development Process | 497-526 | ETL |
| 21 | Big Data Analytics | 527-542 | Big Data |

---



# Kimball Data Warehouse Toolkit 3e -- Taxonomy Tree (Chapters 1-2)

Source: Kimball, Ross. *The Data Warehouse Toolkit*, 3rd Edition (Wiley, 2013).

---
```

### chapter-1-data-warehousing-business-intelligence-and-dimensi

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-1-data-warehousing-business-intelligence-and-dimensi
Hash: efa808de8d12

```
Chapter 1: Data Warehousing, Business Intelligence, and Dimensional Modeling Primer
├── Different Worlds of Data Capture and Data Analysis
│   ├── Operational systems (data capture)
│   │   ├── Optimized to process transactions quickly
│   │   ├── One transaction record at a time
│   │   ├── Do not maintain history; reflect most current state
│   │   └── Systems of record
│   └── DW/BI systems (data analysis)
│       ├── Evaluate organizational performance over time
│       ├── Optimized for high-performance queries
│       ├── Require historical context preservation
│       ├── Support constantly changing questions
│       └── Fundamentally different needs, clients, structures, and rhythms
├── Goals of Data Warehousing and Business Intelligence
│   ├── Make information easily accessible
│   │   ├── Intuitive and obvious to business users
│   │   ├── Mimic business users' thought processes and vocabulary
│   │   └── Simple and fast
│   ├── Present information consistently
│   │   ├── Data must be credible and quality assured
│   │   ├── Common labels and definitions across sources
│   │   └── Same name = same meaning; different meaning = different name
│   ├── Adapt to change
│   │   ├── Handle change gracefully without invalidating existing data/apps
│   │   ├── Existing data and applications not disrupted by new questions
│   │   └── Changes transparent to users
│   ├── Present information in a timely way
│   │   ├── May need to convert raw data within hours, minutes, or seconds
│   │   └── Realistic expectations for data delivery timeliness
│   ├── Be a secure bastion that protects information assets
│   │   └── Effectively control access to confidential information
│   ├── Serve as authoritative and trustworthy foundation for decision making
│   │   ├── Right data to support decision making
│   │   ├── Decisions are the most important outputs
│   │   └── Originally called a "decision support system"
│   └── Business community must accept the DW/BI system to deem it successful
│       ├── Usage is sometimes optional (unlike operational systems)
│       └── Must be the "simple and fast" source for actionable information
├── Publishing Metaphor for DW/BI Managers
│   ├── DW/BI manager as editor-in-chief analogy
│   ├── Understand the business users
│   │   ├── Understand their job responsibilities, goals, objectives
│   │   ├── Determine decisions they want to make with DW/BI
│   │   ├── Identify "best" users who make high-impact decisions
│   │   └── Find potential new users
│   ├── Deliver high-quality, relevant, accessible information
│   │   ├── Choose most robust, actionable data
│   │   ├── Simple and template-driven interfaces
│   │   ├── Accurate, trusted, consistently labeled data
│   │   ├── Continuously monitor accuracy
│   │   └── Adapt to changing profiles, requirements, and priorities
│   ├── Sustain the DW/BI environment
│   │   ├── Take credit for business decisions enabled by DW/BI
│   │   ├── Update regularly
│   │   ├── Maintain trust
│   │   └── Keep stakeholders happy
│   └── Hybrid DBA/MBA skill set required
├── Dimensional Modeling Introduction
│   ├── Core goals
│   │   ├── Deliver data understandable to business users
│   │   └── Deliver fast query performance
│   ├── Simplicity as fundamental principle
│   │   ├── Users easily understand and navigate
│   │   └── Software navigates and delivers results efficiently
│   ├── Data cube metaphor (product, market, time)
│   │   ├── Edges = dimensions
│   │   └── Points inside = measurements (facts)
│   ├── Third Normal Form (3NF) vs. Dimensional Models
│   │   ├── 3NF: removes data redundancies, many discrete entities
│   │   ├── Entity-relationship (ER) diagrams
│   │   ├── 3NF too complicated for BI queries
│   │   ├── Dimensional model contains same information as 3NF
│   │   └── Dimensional model optimizes for understandability, performance, resilience
│   └── Star Schemas Versus OLAP Cubes
│       ├── Star schema: dimensional model in RDBMS
│       ├── OLAP cube: dimensional model in multidimensional database
│       ├── Common logical design, different physical implementation
│       └── OLAP Deployment Considerations
│           ├── Star schema is good foundation for OLAP cube
│           ├── OLAP performance advantages diminishing with hardware advances
│           ├── More sophisticated security options
│           ├── Richer analysis capabilities than SQL
│           ├── Graceful SCD type 2 support
│           ├── Graceful transaction and periodic snapshot support
│           ├── Handle accumulating snapshots less well
│           ├── Support complex ragged hierarchies natively
│           ├── May impose constraints on drill-down hierarchy structure
│           └── Some OLAP products do not support dimensional roles/aliases
├── Fact Tables for Measurements
│   ├── Stores performance measurements from business process events
│   ├── Store low-level measurement data in a single dimensional model
│   ├── Each row = one measurement event
│   ├── Grain: specific level of detail per row
│   │   ├── All rows must be at the same grain
│   │   └── Three grain categories: transaction, periodic snapshot, accumulating snapshot
│   ├── Fact = a business measure (numeric, additive)
│   ├── Additivity
│   │   ├── Fully additive: can be summed across any dimension
│   │   ├── Semi-additive: cannot be summed across time (e.g., account balances)
│   │   └── Non-additive: can never be added (e.g., unit prices, ratios)
│   ├── Continuously valued (facts) vs. discretely valued (dimension attributes)
│   ├── Textual facts are rare; usually belong in dimensions
│   ├── No rows for non-activity (no zeros for missing events)
│   ├── Fact tables are deep (many rows) and narrow (few columns)
│   ├── 90%+ of space consumed by fact tables
│   ├── Foreign keys referencing dimension table primary keys
│   ├── Referential integrity
│   └── Composite primary key (subset of foreign keys)
├── Dimension Tables for Descriptive Context
│   ├── Integral companions to fact tables
│   ├── Contain textual context: who, what, where, when, how, why
│   ├── Often 50-100 attributes per dimension table
│   ├── Wide with many text columns, fewer rows than fact tables
│   ├── Single primary key column (PK)
│   ├── Attributes = primary source of query constraints, groupings, report labels
│   │   └── Identified as the "by" words in queries
│   ├── Attributes should be real words, not cryptic codes
│   ├── Decode operational codes into separate descriptive attributes
│   ├── Analytic power proportional to quality/depth of dimension attributes
│   ├── Fact vs. attribute decision for numeric data
│   │   ├── Continuously valued numeric = almost always a fact
│   │   └── Discrete numeric from small list = almost always a dimension attribute
│   ├── Hierarchical relationships (denormalized)
│   │   ├── Products roll up to brands, then to categories
│   │   └── Store redundantly in dimension table
│   └── Snowflaking (normalizing dimensions) -- generally avoid
│       ├── Trade off dimension table space for simplicity and accessibility
│       └── Virtually no impact on overall database size
├── Facts and Dimensions Joined in a Star Schema
│   ├── Star join structure
│   │   ├── Fact table surrounded by dimension tables
│   │   └── Star-like structure / star join
│   ├── Benefits of dimensional models
│   │   ├── Simplicity and symmetry
│   │   ├── Highly recognizable to business users
│   │   ├── Reduced number of tables, less navigation
│   │   ├── Performance: fewer joins, optimizer efficiency
│   │   └── Gracefully extensible to accommodate change
│   ├── Atomic data has the most dimensionality
│   ├── Extensions without breaking existing queries
│   │   ├── Add new dimensions (new FK column)
│   │   ├── Add new facts (new measure column)
│   │   ├── Add new attributes to dimension tables
│   │   └── Use SQL ALTER TABLE
│   └── Dimensions supply report filters/labels; facts supply numeric values
├── Kimball's DW/BI Architecture
│   ├── Four components
│   │   ├── Operational Source Systems
│   │   │   ├── Systems of record capturing business transactions
│   │   │   ├── Outside the data warehouse
│   │   │   ├── Processing performance and availability as priorities
│   │   │   ├── Narrow, one-record-at-a-time queries
│   │   │   └── Maintain little historical data
│   │   ├── Extract, Transformation, and Load (ETL) System
│   │   │   ├── Extraction: reading and copying source data
│   │   │   ├── Transformation: cleansing, conforming, de-duplicating
│   │   │   │   ├── Correcting misspellings
│   │   │   │   ├── Resolving domain conflicts
│   │   │   │   ├── Dealing with missing elements
│   │   │   │   ├── Parsing into standard formats
│   │   │   │   └── Combining data from multiple sources
│   │   │   ├── Loading: physical structuring into target dimensional models
│   │   │   │   ├── Surrogate key assignments
│   │   │   │   ├── Code lookups
│   │   │   │   └── Denormalization into flattened dimensions
│   │   │   ├── Design goals: throughput, integrity, consistency
│   │   │   ├── Diagnostic metadata creation
│   │   │   └── Debate: normalized staging vs. direct dimensional loading
│   │   ├── Presentation Area to Support Business Intelligence
│   │   │   ├── Where data is organized, stored, and made available for querying
│   │   │   ├── Must be dimensional (star schemas or OLAP cubes)
│   │   │   ├── Must contain detailed, atomic data
│   │   │   ├── May also contain performance-enhancing aggregates
│   │   │   ├── Structured around business process measurement events
│   │   │   ├── Business processes cross organizational boundaries
│   │   │   └── Built using common, conformed dimensions
│   │   │       └── Enterprise data warehouse bus architecture
│   │   └── Business Intelligence Applications
│   │       ├── Range of capabilities for analytic decision making
│   │       ├── Ad hoc query tools
│   │       ├── Prebuilt parameter-driven applications and templates
│   │       ├── Data mining and modeling applications
│   │       └── Some may upload results back to source/ETL/presentation
│   └── Restaurant Metaphor for the Kimball Architecture
│       ├── ETL = Back Room Kitchen
│       │   ├── Throughput
│       │   ├── Consistency (create sauces/business rules once)
│       │   ├── Integrity
│       │   ├── Quality control of incoming data
│       │   └── Off limits to users
│       └── Presentation Area + BI = Front Dining Room
│           ├── Food (quality, taste, presentation) = data
│           ├── Decor = presentation area design for user comfort
│           ├── Service = data delivery (prompt, as ordered)
│           └── Cost = budget considerations
├── Alternative DW/BI Architectures
│   ├── Independent Data Mart Architecture
│   │   ├── Departmental analytic silos without cross-organizational integration
│   │   ├── Essentially un-architected
│   │   ├── Path of least resistance, low short-term cost
│   │   ├── Results in incompatible views, unnecessary debate
│   │   └── Strongly discouraged
│   ├── Hub-and-Spoke Corporate Information Factory (CIF) / Inmon Architecture
│   │   ├── Data extracted and processed into 3NF Enterprise Data Warehouse (EDW)
│   │   ├── Normalized, atomic, user-queryable EDW
│   │   ├── Downstream dimensional data marts (often departmental, summarized)
│   │   ├── Normalization does not equal integration
│   │   └── Pure CIF locks atomic data in difficult-to-query normalized structures
│   └── Hybrid Hub-and-Spoke and Kimball Architecture
│       ├── CIF-centric EDW (off-limits to users) feeds Kimball presentation area
│       ├── Dimensional, atomic, process-centric, conformed dimensions
│       ├── Claims best of both worlds
│       └── Higher cost due to redundant storage and multiple data movements
├── Dimensional Modeling Myths
│   ├── Myth 1: Dimensional models are only for summary data
│   │   ├── Must provide queryable access to most detailed data
│   │   ├── Summary complements granular detail, does not replace it
│   │   └── Corollary: no limit on historical data in dimensional structures
│   ├── Myth 2: Dimensional models are departmental, not enterprise
│   │   ├── Organize around business processes, not departments
│   │   └── Avoid multiple inconsistent extracts of same source data
│   ├── Myth 3: Dimensional models are not scalable
│   │   ├── Fact tables frequently have billions of rows (2 trillion reported)
│   │   ├── Same information and data relationships as normalized models
│   │   └── Both can answer exactly the same questions
│   ├── Myth 4: Dimensional models are only for predictable usage
│   │   ├── Design should center on measurement processes, not predefined reports
│   │   ├── Symmetric structure is flexible and adaptive to change
│   │   └── Build fact tables at most granular level for max flexibility
│   └── Myth 5: Dimensional models can't be integrated
│       ├── Integrate via enterprise data warehouse bus architecture
│       ├── Conformed dimensions as centralized, persistent master data
│       └── Data integration requires standardized labels, values, definitions
├── More Reasons to Think Dimensionally
│   ├── Requirements gathering: synthesize findings around business processes
│   ├── Focus on business process measurement events, not reports
│   ├── Enterprise data warehouse bus matrix as prime deliverable
│   ├── Data stewardship/governance on major dimensions
│   │   ├── Focus on central nouns: date, customer, product, employee, facility, etc.
│   │   └── Led by subject matter experts from business community
│   └── Dimensional modeling relevant throughout DW/BI lifecycle
├── Agile Considerations
│   ├── Kimball best practices align with agile tenets
│   │   ├── Focus on delivering business value
│   │   ├── Collaboration between development and business stakeholders
│   │   ├── Ongoing face-to-face communication and feedback
│   │   ├── Adapt quickly to evolving requirements
│   │   └── Iterative, incremental development
│   ├── Enterprise data warehouse bus matrix addresses agile shortcomings
│   │   ├── Provides framework and master plan
│   │   ├── Identifies reusable conformed dimensions
│   │   └── Reduces time-to-market as conformed dimensions mature
│   └── Avoid building isolated data stovepipes
└── Summary
```

### chapter-2-kimball-dimensional-modeling-techniques-overview-p

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-2-kimball-dimensional-modeling-techniques-overview-p
Hash: 08ea4248fcf2

```
Chapter 2: Kimball Dimensional Modeling Techniques Overview
├── Fundamental Concepts
│   ├── Gather Business Requirements and Data Realities
│   │   ├── Understand business needs via sessions with business representatives
│   │   ├── Key performance indicators, compelling business issues
│   │   ├── Decision-making processes and supporting analytic needs
│   │   └── Data realities: meet source system experts, do high-level data profiling
│   ├── Collaborative Dimensional Modeling Workshops
│   │   ├── Designed in collaboration with subject matter experts and data governance reps
│   │   ├── Data modeler is in charge
│   │   ├── Highly interactive workshops with business representatives
│   │   └── Models should not be designed in isolation
│   ├── Four-Step Dimensional Design Process
│   │   ├── 1. Select the business process
│   │   ├── 2. Declare the grain
│   │   ├── 3. Identify the dimensions
│   │   └── 4. Identify the facts
│   ├── Business Processes
│   │   ├── Operational activities that generate or capture performance metrics
│   │   ├── Translate into facts in a fact table
│   │   ├── Most fact tables focus on single business process
│   │   └── Each business process = one row in enterprise data warehouse bus matrix
│   ├── Grain
│   │   ├── Establishes exactly what a single fact table row represents
│   │   ├── Binding contract on the design
│   │   ├── Must be declared before choosing dimensions or facts
│   │   ├── Atomic grain = lowest level captured by business process
│   │   ├── Strongly encourage starting with atomic grain
│   │   └── Different grains must not be mixed in the same fact table
│   ├── Dimensions for Descriptive Context
│   │   ├── Provide who, what, where, when, why, and how context
│   │   ├── Contain descriptive attributes for filtering and grouping
│   │   ├── Should be single valued for a given fact row
│   │   ├── Sometimes called the "soul" of the data warehouse
│   │   └── Disproportionate effort in governance and development
│   ├── Facts for Measurements
│   │   ├── Measurements from a business process event, almost always numeric
│   │   ├── One-to-one relationship between fact table row and measurement event
│   │   ├── Only facts consistent with declared grain are allowed
│   │   └── Store manager salary is NOT a valid fact for retail sales transaction grain
│   ├── Star Schemas and OLAP Cubes
│   │   ├── Star schema: fact tables linked to dimension tables via PK/FK in RDBMS
│   │   ├── OLAP cube: dimensional structure in multidimensional database
│   │   ├── Accessed via XMLA and MDX (more analytic than SQL)
│   │   └── OLAP cube often final deployment step or aggregate structure
│   └── Graceful Extensions to Dimensional Models
│       ├── Add new facts by creating new columns (consistent with grain)
│       ├── Add new dimensions by creating new FK columns (don't alter grain)
│       ├── Add new attributes by creating new dimension columns
│       └── Make grain more atomic by adding attributes and restating fact table
├── Basic Fact Table Techniques
│   ├── Fact Table Structure
│   │   ├── Contains numeric measures from operational measurement events
│   │   ├── Foreign keys for each dimension + optional degenerate dimension keys
│   │   ├── Date/time stamps
│   │   └── Primary target of computations and dynamic aggregations
│   ├── Additive, Semi-Additive, Non-Additive Facts
│   │   ├── Fully additive: summed across any dimension
│   │   ├── Semi-additive: summed across some but not all (e.g., balances not across time)
│   │   └── Non-additive: ratios -- store components and compute in BI layer
│   ├── Nulls in Fact Tables
│   │   ├── Null-valued measurements behave gracefully (SUM, COUNT, MIN, MAX, AVG)
│   │   ├── Nulls in FK columns must be avoided (referential integrity violation)
│   │   └── Use default dimension row (surrogate key) for unknown/not applicable
│   ├── Conformed Facts
│   │   ├── Same measurement appearing in separate fact tables
│   │   ├── Technical definitions must be identical if compared/computed together
│   │   ├── Identically named if consistent; differently named if incompatible
│   │   └── Alert business users and BI applications about incompatibilities
│   ├── Transaction Fact Tables
│   │   ├── One row per measurement event at a point in space and time
│   │   ├── Most dimensional and expressive fact tables
│   │   ├── Maximum slicing and dicing
│   │   ├── May be dense or sparse
│   │   ├── Foreign key for each dimension + optional timestamps + degenerate dimension keys
│   │   └── Measured numeric facts consistent with transaction grain
│   ├── Periodic Snapshot Fact Tables
│   │   ├── Summarize many measurement events over a standard period (day, week, month)
│   │   ├── Grain = the period, not individual transaction
│   │   ├── Often contain many facts (any measurement consistent with grain)
│   │   ├── Uniformly dense in foreign keys
│   │   └── Rows inserted even if no activity (zero or null for each fact)
│   ├── Accumulating Snapshot Fact Tables
│   │   ├── Summarize measurement events across predictable pipeline/workflow steps
│   │   ├── Defined start point, intermediate steps, defined end point
│   │   ├── Date FK for each critical milestone in the process
│   │   ├── Rows are revisited and updated as pipeline progresses (unique among fact types)
│   │   ├── Initially inserted when process begins (e.g., order line created)
│   │   ├── Contain degenerate dimensions and numeric lag measurements
│   │   └── Milestone completion counters
│   ├── Factless Fact Tables
│   │   ├── Events with no associated numeric metrics
│   │   ├── Row of foreign keys recording dimensional entities at a moment in time
│   │   ├── Example: student attending a class on a given day
│   │   ├── Coverage table: all possibilities of events that might happen
│   │   ├── Activity table: events that did happen
│   │   └── Coverage minus activity = events that did not happen
│   ├── Aggregate Fact Tables or OLAP Cubes
│   │   ├── Simple numeric rollups of atomic fact table data
│   │   ├── Solely to accelerate query performance
│   │   ├── Available to BI layer alongside atomic fact tables
│   │   ├── Aggregate navigation must be open (transparent to all tools)
│   │   ├── Behave like database indexes (invisible performance boost)
│   │   ├── Contain FK to shrunken conformed dimensions
│   │   └── Aggregate OLAP cubes are accessed directly by users
│   └── Consolidated Fact Tables
│       ├── Combine facts from multiple processes into single table
│       ├── Must be expressible at the same grain
│       ├── Example: actuals consolidated with forecasts
│       ├── Add ETL burden but ease analytic burden
│       └── Consider for cross-process metrics frequently analyzed together
├── Basic Dimension Table Techniques
│   ├── Dimension Table Structure
│   │   ├── Single PK column embedded as FK in fact tables
│   │   ├── Usually wide, flat denormalized tables
│   │   ├── Many low-cardinality text attributes
│   │   ├── Operational codes treated as attributes with verbose descriptions
│   │   └── Primary target of constraints, groupings, report labels
│   ├── Dimension Surrogate Keys
│   │   ├── Anonymous integer primary keys for every dimension
│   │   ├── Cannot use operational system's natural key (multiple rows for changes)
│   │   ├── Simple integers assigned in sequence starting with 1
│   │   ├── DW/BI system claims control of all dimension primary keys
│   │   └── Date dimension exempt (can use meaningful YYYYMMDD integer)
│   ├── Natural, Durable, and Supernatural Keys
│   │   ├── Natural keys: from operational source systems, subject to business rules
│   │   ├── Durable key: persistent, does not change across employee rehire etc.
│   │   ├── Durable supernatural key: format independent of business process
│   │   └── Multiple surrogate keys may map to one durable key over time
│   ├── Drilling Down
│   │   ├── Adding a row header (dimension attribute) to GROUP BY in query
│   │   ├── Attribute can come from any dimension attached to fact table
│   │   └── Does not require predetermined hierarchies or drill-down paths
│   ├── Degenerate Dimensions
│   │   ├── Dimension with no content except its primary key
│   │   ├── Placed directly in the fact table (no associated dimension table)
│   │   ├── Example: invoice number on line item fact table
│   │   └── Most common with transaction and accumulating snapshot fact tables
│   ├── Denormalized Flattened Dimensions
│   │   ├── Resist normalization urges for dimension tables
│   │   ├── Denormalize many-to-one fixed depth hierarchies into flat rows
│   │   └── Supports simplicity and speed goals
│   ├── Multiple Hierarchies in Dimensions
│   │   ├── Many dimensions contain more than one natural hierarchy
│   │   ├── Example: calendar date has fiscal period hierarchy and day-to-year hierarchy
│   │   └── Separate hierarchies gracefully coexist in same dimension table
│   ├── Flags and Indicators as Textual Attributes
│   │   ├── Supplement cryptic abbreviations and true/false flags with full text words
│   │   ├── Operational codes with embedded meaning should be broken down
│   │   └── Each part expanded into its own separate descriptive dimension attribute
│   ├── Null Attributes in Dimensions
│   │   ├── Substitute descriptive string (Unknown, Not Applicable) for nulls
│   │   └── Avoid nulls because databases handle grouping/constraining on nulls inconsistently
│   ├── Calendar Date Dimensions
│   │   ├── Attached to virtually every fact table
│   │   ├── Navigate through familiar dates, months, fiscal periods, special days
│   │   ├── PK can be meaningful integer (YYYYMMDD) to facilitate partitioning
│   │   ├── Special row for unknown/to-be-determined dates
│   │   ├── Date/time stamp is a standalone column, not a FK to dimension
│   │   └── Separate time-of-day dimension FK if business users constrain on time parts
│   ├── Role-Playing Dimensions
│   │   ├── Single physical dimension referenced multiple times in a fact table
│   │   ├── Each reference = logically distinct role (e.g., order date, ship date, delivery date)
│   │   ├── Each FK refers to a separate view of the dimension
│   │   └── Separate dimension views (with unique column names) called "roles"
│   ├── Junk Dimensions
│   │   ├── Combine miscellaneous low-cardinality flags and indicators
│   │   ├── Frequently labeled as "transaction profile dimension"
│   │   ├── Not full Cartesian product -- only combinations that actually occur
│   │   └── Avoids creating separate dimensions for each flag/attribute
│   ├── Snowflaked Dimensions
│   │   ├── Normalized low-cardinality attributes as secondary tables by attribute key
│   │   ├── Creates characteristic multilevel "snowflake" structure
│   │   ├── Should be avoided: difficult for users, may hurt query performance
│   │   └── Flattened denormalized table contains exactly the same information
│   └── Outrigger Dimensions
│       ├── Dimension containing a reference (FK) to another dimension table
│       ├── Example: bank account dimension referencing date dimension for account open date
│       ├── Use sparingly
│       └── In most cases, demote correlations to fact table as separate FKs
├── Integration via Conformed Dimensions
│   ├── Conformed Dimensions
│   │   ├── Attributes in separate dimension tables have same column names and domain contents
│   │   ├── Information from separate fact tables combined in single report
│   │   ├── Essence of integration in enterprise DW/BI system
│   │   ├── Defined once in collaboration with business data governance representatives
│   │   ├── Reused across fact tables
│   │   └── Deliver analytic consistency and reduced development costs
│   ├── Shrunken Dimensions
│   │   ├── Conformed dimensions that are a subset of rows and/or columns
│   │   ├── Shrunken rollup dimensions for aggregate fact tables
│   │   ├── Required for business processes at higher granularity (e.g., forecast by month+brand)
│   │   └── Subsetting at same level of detail (one represents subset of rows)
│   ├── Drilling Across
│   │   ├── Separate queries against two or more fact tables
│   │   ├── Row headers = identical conformed attributes
│   │   ├── Answer sets aligned via sort-merge on common dimension attributes
│   │   └── BI tools call this stitch, multipass query
│   ├── Value Chain
│   │   ├── Natural flow of organization's primary business processes
│   │   ├── Example: purchasing -> warehousing -> retail sales
│   │   ├── Each step produces unique metrics with unique granularity
│   │   └── Each process typically spawns at least one atomic fact table
│   ├── Enterprise Data Warehouse Bus Architecture
│   │   ├── Incremental approach to building enterprise DW/BI system
│   │   ├── Decomposes into manageable pieces by business process
│   │   ├── Integration via standardized conformed dimensions reused across processes
│   │   ├── Encourages manageable agile implementations
│   │   └── Technology and database platform independent
│   ├── Enterprise Data Warehouse Bus Matrix
│   │   ├── Essential tool for designing and communicating the bus architecture
│   │   ├── Rows = business processes
│   │   ├── Columns = dimensions
│   │   ├── Shaded cells = dimension associated with business process
│   │   ├── Used to prioritize DW/BI projects with business management
│   │   └── Teams implement one row at a time
│   ├── Detailed Implementation Bus Matrix
│   │   ├── More granular: each business process row expanded to specific fact tables/OLAP cubes
│   │   └── Documents precise grain statement and list of facts
│   └── Opportunity/Stakeholder Matrix
│       ├── Replace dimension columns with business functions (marketing, sales, finance)
│       ├── Shade cells to indicate which functions are interested in which processes
│       └── Helps identify which business groups to invite to collaborative design sessions
├── Dealing with Slowly Changing Dimension (SCD) Attributes
│   ├── Type 0: Retain Original
│   │   ├── Attribute value never changes
│   │   ├── Appropriate for "original" attributes (e.g., original credit score)
│   │   └── Applies to most date dimension attributes
│   ├── Type 1: Overwrite
│   │   ├── Old value overwritten with new value
│   │   ├── Always reflects most recent assignment
│   │   ├── Destroys history
│   │   ├── Easy to implement, no additional rows
│   │   └── Must recompute affected aggregate fact tables and OLAP cubes
│   ├── Type 2: Add New Row
│   │   ├── New row with updated attribute values and new surrogate key
│   │   ├── Requires generalizing PK beyond natural/durable key
│   │   ├── New surrogate key used as FK from moment of update onward
│   │   └── Three additional columns: row effective date, row expiration date, current row indicator
│   ├── Type 3: Add New Attribute
│   │   ├── New attribute column preserves old value alongside new ("alternate reality")
│   │   ├── New value overwrites main attribute (like type 1)
│   │   ├── Business user can group/filter by current or alternate reality
│   │   └── Used relatively infrequently
│   ├── Type 4: Add Mini-Dimension
│   │   ├── Split rapidly changing attributes into a mini-dimension
│   │   ├── Also called "rapidly changing monster dimension"
│   │   ├── Mini-dimension has its own unique PK
│   │   ├── Both base dimension and mini-dimension PKs captured in fact table
│   │   └── Candidates: frequently used attributes in multimillion-row dimensions
│   ├── Type 5: Add Mini-Dimension and Type 1 Outrigger
│   │   ├── Accurately preserve historical attribute values
│   │   ├── Report historical facts according to current attribute values
│   │   ├── Builds on type 4 by embedding current type 1 reference to mini-dimension in base dimension
│   │   ├── Enables current mini-dimension attributes alongside base dimension attributes
│   │   └── ETL must overwrite type 1 reference whenever mini-dimension assignment changes
│   ├── Type 6: Add Type 1 Attributes to Type 2 Dimension
│   │   ├── Delivers both historical and current dimension attribute values
│   │   ├── Embeds current type 1 versions of same attributes in type 2 dimension row
│   │   ├── Filter/group by historical value or current value
│   │   └── Type 1 attribute systematically overwritten on all rows for a durable key
│   └── Type 7: Dual Type 1 and Type 2 Dimensions
│       ├── Support both as-was and as-is reporting
│       ├── Fact table accessed through type 1 dimension (current only) or type 2 (historical)
│       ├── Same dimension table, two perspectives
│       ├── Both durable key and surrogate key in fact table
│       ├── Type 1: join via durable key, constrain on current flag
│       ├── Type 2: join via surrogate key, no current flag constraint
│       └── Deploy as separate views to BI applications
├── Dealing with Dimension Hierarchies
│   ├── Fixed Depth Positional Hierarchies
│   │   ├── Series of many-to-one relationships (product -> brand -> category -> department)
│   │   ├── Hierarchy levels as separate positional attributes in dimension table
│   │   ├── Easiest to understand, navigate, and query
│   │   └── If levels not fixed or not named, use ragged hierarchy technique
│   ├── Slightly Ragged/Variable Depth Hierarchies
│   │   ├── Fixed number of levels but small range in depth
│   │   ├── Force-fit into fixed depth positional design
│   │   └── Populate attribute values based on business rules
│   ├── Ragged/Variable Depth Hierarchies with Hierarchy Bridge Tables
│   │   ├── Indeterminate depth, difficult to model in RDBMS
│   │   ├── Bridge table with row for every possible path in the hierarchy
│   │   ├── Enables all forms of hierarchy traversal with standard SQL
│   │   ├── Supports alternative hierarchies, shared ownership, time varying hierarchies
│   │   └── No need for special SQL language extensions
│   └── Ragged/Variable Depth Hierarchies with Pathstring Attributes
│       ├── Pathstring attribute: encoded text string of complete path from root to node
│       ├── Handled by standard SQL without language extensions
│       ├── Does not support rapid substitution of alternative or shared ownership hierarchies
│       └── Vulnerable to structure changes requiring relabeling
├── Advanced Fact Table Techniques
│   ├── Fact Table Surrogate Keys
│   │   ├── Single column surrogate FK, not associated with any dimension
│   │   ├── Assigned sequentially during ETL load
│   │   ├── Uses: 1) single column PK, 2) immediate row identifier for ETL
│   │   ├── 3) allow interrupted load to back out/resume
│   │   └── 4) decompose fact table updates into inserts + deletes
│   ├── Centipede Fact Tables
│   │   ├── Anti-pattern: separate normalized dimensions for each hierarchy level as FKs
│   │   ├── Results in dozens of hierarchically related dimensions
│   │   ├── Should be avoided -- collapse to unique lowest grains
│   │   └── Also results from embedding numerous FKs to low-cardinality tables (use junk dimension)
│   ├── Numeric Values as Attributes or Facts
│   │   ├── If used primarily for calculation -> fact table
│   │   ├── If stable and used for filtering/grouping -> dimension attribute
│   │   ├── Discrete values supplemented with value band attributes
│   │   └── Sometimes model as both fact and dimension attribute
│   ├── Lag/Duration Facts
│   │   ├── Accumulating snapshots have multiple date FKs (milestones)
│   │   ├── Store one time lag per step (measured from process start)
│   │   ├── Lag between any two steps = simple subtraction
│   │   └── Avoids forcing user queries to calculate all possible lags
│   ├── Header/Line Fact Tables
│   │   ├── Operational header row + multiple transaction lines
│   │   ├── Also called parent/child schemas
│   │   └── All header-level dimension FKs and degenerate dimensions included on line-level fact table
│   ├── Allocated Facts
│   │   ├── Header/line data with differing granularity (e.g., header freight charge)
│   │   ├── Allocate header facts to line level based on business rules
│   │   ├── Enables slicing and rolling up by all dimensions
│   │   └── Avoids separate header-level fact table unless query performance warrants it
│   ├── Profit and Loss Fact Tables Using Allocations
│   │   ├── Expose full profit equation: revenue - costs = profit
│   │   ├── Ideally at atomic revenue transaction grain
│   │   ├── Enable customer, product, promotion, channel profitability rollups
│   │   ├── Cost components must be allocated from original sources
│   │   └── Politically charged; typically not tackled in early implementation phases
│   ├── Multiple Currency Facts
│   │   ├── Pair of columns: true transaction currency + standard currency
│   │   ├── Standard currency value created in ETL via approved conversion business rule
│   │   └── Currency dimension to identify transaction's true currency
│   ├── Multiple Units of Measure Facts
│   │   ├── Facts stated in several units simultaneously (pallets, cases, scan units)
│   │   ├── Store at agreed standard unit + conversion factors to other units
│   │   └── Deploy through views to each user constituency
│   ├── Year-to-Date Facts
│   │   ├── Do not store YTD in fact table
│   │   ├── YTD requests can morph unpredictably
│   │   └── Calculate in BI applications or OLAP cube instead
│   ├── Multipass SQL to Avoid Fact-to-Fact Table Joins
│   │   ├── Never join two fact tables directly across their FK columns
│   │   ├── Impossible to control cardinality; incorrect results
│   │   ├── Use drilling across: separate queries per fact table
│   │   └── Sort-merge results on common row header attribute values
│   ├── Timespan Tracking in Fact Tables
│   │   ├── Add row effective date, expiration date, current row indicator to fact rows
│   │   ├── Analogous to type 2 SCD for dimensions
│   │   ├── Addresses slowly changing inventory balances
│   │   └── Avoids loading identical periodic snapshot rows repeatedly
│   └── Late Arriving Facts
│       ├── Most current dimensional context does not match the delayed fact row
│       ├── Search relevant dimensions for keys that were effective when event occurred
│       └── Assign appropriate historical dimension keys
├── Advanced Dimension Techniques
│   ├── Dimension-to-Dimension Table Joins
│   │   ├── Dimensions can reference other dimensions (outrigger)
│   │   ├── Risk: type 2 changes in outrigger force explosive growth in base dimension
│   │   ├── Often avoidable by placing outrigger FK in fact table instead
│   │   └── Acceptable when fact table is periodic snapshot (all dimension keys present)
│   ├── Multivalued Dimensions and Bridge Tables
│   │   ├── When dimension is legitimately multivalued for a fact row
│   │   ├── Example: patient with multiple simultaneous diagnoses
│   │   ├── Attach via group dimension key to bridge table
│   │   └── Bridge table: one row per member of each group
│   ├── Time Varying Multivalued Bridge Tables
│   │   ├── Bridge table based on type 2 slowly changing dimension
│   │   ├── Must include effective and expiration date/time stamps
│   │   ├── Requesting application constrains bridge to specific moment in time
│   │   └── Example: many-to-many between bank accounts and customers
│   ├── Behavior Tag Time Series
│   │   ├── Textual behavior tags from data mining / customer cluster analyses
│   │   ├── Identified periodically; sequence becomes time series
│   │   ├── Stored as positional attributes in customer dimension
│   │   └── Optional complete sequence text string
│   ├── Behavior Study Groups
│   │   ├── Complex customer behavior discovered via lengthy iterative analyses
│   │   ├── Study group: simple table of durable keys for qualifying members
│   │   ├── Static table used as filter on any dimensional schema
│   │   └── Multiple study groups with intersections, unions, set differences
│   ├── Aggregated Facts as Dimension Attributes
│   │   ├── Aggregated performance metrics placed in dimension as constraints/labels
│   │   ├── Example: filter on customers who spent over X dollars last year
│   │   ├── Often presented as banded ranges
│   │   └── Adds ETL burden, eases analytic burden in BI layer
│   ├── Dynamic Value Bands
│   │   ├── Report row headers defined at query time (not ETL time)
│   │   ├── Example: "Balance from 0 to $10", "$10.01 to $25"
│   │   ├── Small value banding dimension table with greater-than/less-than joins
│   │   └── Alternative: SQL CASE statement (higher performing in columnar DBs)
│   ├── Text Comments Dimension
│   │   ├── Freeform comments stored outside fact table in separate dimension
│   │   ├── Or as attributes if cardinality matches unique transactions
│   │   └── Corresponding FK in fact table
│   ├── Multiple Time Zones
│   │   ├── Dual FKs to role-playing date (and potentially time-of-day) dimension tables
│   │   └── Capture both universal standard time and local time
│   ├── Measure Type Dimensions
│   │   ├── Collapses fact table row to single generic fact identified by measure type dimension
│   │   ├── Generally not recommended (multiplies rows, complicates intra-column computations)
│   │   └── Acceptable when potential facts are extreme (hundreds) and few apply per row
│   ├── Step Dimensions
│   │   ├── For sequential processes (e.g., web page events)
│   │   ├── Shows current step number and remaining steps to complete session
│   │   └── Separate row in transaction fact table for each step
│   ├── Hot Swappable Dimensions
│   │   ├── Same fact table alternatively paired with different copies of same dimension
│   │   ├── Example: stock ticker facts exposed to multiple investors with different attributes
│   │   └── Each investor has unique and proprietary attributes for the same stocks
│   ├── Abstract Generic Dimensions
│   │   ├── Anti-pattern: single generic location/person dimension for all entity types
│   │   ├── Should be avoided in dimensional models
│   │   ├── Attribute sets differ significantly by type
│   │   ├── Negatively impacts query performance and legibility
│   │   └── Data abstraction may be appropriate in source/ETL but not presentation area
│   ├── Audit Dimensions
│   │   ├── Contains ETL processing metadata known at time of fact row creation
│   │   ├── Data quality indicators
│   │   ├── Error event schema references
│   │   ├── ETL code versions
│   │   ├── ETL process execution timestamps
│   │   └── Useful for compliance and auditing
│   └── Late Arriving Dimensions
│       ├── Facts arrive before associated dimension context
│       ├── Special dimension rows created with natural keys and generic unknown values
│       ├── Placeholder rows updated with type 1 overwrite when context arrives
│       └── Retroactive type 2 changes require new dimension row + restated fact rows
└── Special Purpose Schemas
    ├── Supertype and Subtype Schemas for Heterogeneous Products
    │   ├── For businesses with wide variety of product types (e.g., bank account types)
    │   ├── Supertype fact table: intersection of facts from all types + supertype dimension
    │   ├── Subtype fact tables: specific facts and dimensions per product type
    │   └── Also called core and custom fact tables
    ├── Real-Time Fact Tables
    │   ├── Updated more frequently than traditional nightly batch
    │   ├── Hot partition on fact table (pinned in memory, no aggregations/indexes)
    │   ├── Deferred updating supported by some DBMSs and OLAP cubes
    │   └── Allows existing queries to complete before performing updates
    └── Error Event Schemas
        ├── Comprehensive data quality screens/filters test data flowing from source to BI
        ├── Error events recorded in special dimensional schema (ETL back room only)
        ├── Error event fact table (grain = individual error event)
        └── Error event detail fact table (grain = each column participating in error)
```

### chapter-3-retail-sales-pp-69-110

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-3-retail-sales-pp-69-110
Hash: 383f2800938e

```
Chapter 3: Retail Sales
├── Four-Step Dimensional Design Process
│   ├── Step 1: Select the Business Process
│   │   ├── Business processes expressed as action verbs (taking orders, invoicing, etc.)
│   │   ├── Supported by operational systems (billing, purchasing)
│   │   ├── Generate or capture key performance metrics
│   │   ├── Triggered by input, result in output metrics
│   │   ├── Business processes vs. business initiatives (strategic plans)
│   │   ├── Processes vs. departments -- focus on processes, not org chart
│   │   └── Retail case study selects: POS retail sales transactions
│   ├── Step 2: Declare the Grain
│   │   ├── Specifies what a single fact table row represents
│   │   ├── Expressed in business terms, not as a list of dimensions
│   │   ├── Example grains:
│   │   │   ├── One row per scan of individual product on a sales transaction
│   │   │   ├── One row per line item on a bill from a doctor
│   │   │   ├── One row per individual boarding pass scanned at airport gate
│   │   │   ├── One row per daily snapshot of inventory per item per warehouse
│   │   │   └── One row per bank account each month
│   │   ├── Grain = primary key of the fact table (ultimately)
│   │   ├── Most frequent design error: not declaring grain at the beginning
│   │   ├── Atomic grain provides maximum analytic flexibility
│   │   ├── Aggregated grain limits drill-down and future dimensions
│   │   └── Retail case study grain: individual product line item on a POS transaction
│   ├── Step 3: Identify the Dimensions
│   │   ├── Answer "who, what, where, when, why, and how" of each event
│   │   ├── Common dimensions: date, product, customer, employee, facility
│   │   ├── Grain statement determines primary dimensionality
│   │   ├── Additional dimensions must take on one value per primary combination
│   │   └── Retail case study dimensions: date, product, store, promotion, cashier, payment method, POS transaction number (DD)
│   └── Step 4: Identify the Facts
│       ├── Answer "What is the process measuring?"
│       ├── Facts must be true to the declared grain
│       ├── Typical facts: numeric additive figures (quantity, dollar amount)
│       ├── Facts at different grain belong in separate fact tables
│       ├── Figure 3-1: Business Requirements + Data Realities --> Dimensional Model
│       └── Retail case study facts: sales quantity, regular/discount/net unit price, extended discount/sales/cost/gross profit dollar amounts
├── Retail Case Study
│   ├── Business context: large grocery chain, 100 stores, 5 states
│   │   ├── Departments: grocery, frozen foods, dairy, meat, produce, bakery, floral, health/beauty
│   │   ├── ~60,000 SKUs per store
│   │   └── POS system scans product barcodes at cash register
│   ├── Management concerns: ordering, stocking, selling, maximizing profit
│   ├── Promotions: temporary price reductions, newspaper inserts, displays, coupons
│   └── Figure 3-2: Sample cash register receipt (Allstar Grocery)
├── Retail Sales Star Schema (Figure 3-3)
│   ├── Retail Sales Fact table
│   │   ├── Foreign Keys: Date Key, Product Key, Store Key, Promotion Key, Cashier Key, Payment Method Key
│   │   ├── Degenerate Dimension: POS Transaction # (DD)
│   │   └── Facts (measures):
│   │       ├── Sales Quantity (additive)
│   │       ├── Regular Unit Price (non-additive)
│   │       ├── Discount Unit Price (non-additive)
│   │       ├── Net Unit Price (non-additive)
│   │       ├── Extended Discount Dollar Amount (additive)
│   │       ├── Extended Sales Dollar Amount (additive)
│   │       ├── Extended Cost Dollar Amount (additive)
│   │       └── Extended Gross Profit Dollar Amount (derived, additive)
│   ├── Dimension tables: Date, Product, Store, Promotion, Cashier, Payment Method
│   └── Four additive facts: sales quantity, extended discount, sales, and cost dollar amounts
├── Fact Types and Additivity
│   ├── Derived Facts
│   │   ├── Gross profit = extended sales - extended cost
│   │   ├── Recommend storing derived facts physically in ETL
│   │   ├── Eliminates user calculation errors
│   │   ├── Ensures consistency across users and BI tools
│   │   └── Views as alternative (but ad hoc tools may bypass views)
│   ├── Non-Additive Facts
│   │   ├── Gross margin (ratio) -- cannot be summed across any dimension
│   │   ├── Unit price -- summing is meaningless
│   │   ├── Store numerator and denominator; calculate ratio of sums, not sum of ratios
│   │   ├── Weighted average unit price = total sales amount / total quantity
│   │   ├── Temperature as a fundamentally non-additive fact
│   │   └── OLAP cubes excel at non-additive metrics
│   └── Transaction Fact Tables (characteristics)
│       ├── Grain expressed as one row per transaction or transaction line
│       ├── Sparsely populated (not every product in every cart)
│       ├── Unpredictably and sparsely populated, but can be enormous (billions/trillions of rows)
│       ├── Highly dimensional
│       ├── Metrics typically additive (extended amounts, not per-unit)
│       └── Estimate row counts: $4B revenue / $2 avg = ~2 billion rows/year
├── Dimension Table Details
│   ├── Date Dimension (Figure 3-4)
│   │   ├── Nearly guaranteed in every dimensional model
│   │   ├── Usually first dimension in partitioning scheme
│   │   ├── Built in advance (10-20 years, ~7,300 rows)
│   │   ├── Columns (partial list from Figure 3-4):
│   │   │   ├── Date Key (PK), Date, Full Date Description
│   │   │   ├── Day of Week, Day Number in Calendar/Fiscal Month/Year
│   │   │   ├── Last Day in Month Indicator
│   │   │   ├── Calendar Week Ending Date, Calendar Week Number in Year
│   │   │   ├── Calendar Month Name, Calendar Month Number in Year
│   │   │   ├── Calendar Year-Month (YYYY-MM), Calendar Quarter/Year-Quarter/Year
│   │   │   ├── Fiscal Week/Month/Quarter/Half Year/Year (and numbered variants)
│   │   │   ├── Holiday Indicator, Weekday Indicator
│   │   │   └── SQL Date Stamp
│   │   ├── Figure 3-5: Sample rows with Date Key format YYYYMMDD
│   │   ├── Explicit date dimension always needed (SQL date semantics insufficient)
│   │   │   ├── SQL functions cannot handle fiscal periods, seasons, holidays, weekends
│   │   │   └── Calendar logic belongs in dimension table, not application code
│   │   ├── Flags and Indicators as Textual Attributes
│   │   │   ├── Use meaningful values: "Holiday"/"Non-Holiday", not Y/N or 1/0
│   │   │   ├── Figure 3-6: Cryptic vs. textual indicators comparison
│   │   │   └── Decoded values stored in DB for consistency across BI tools
│   │   ├── Current and Relative Date Attributes
│   │   │   ├── IsCurrentDay, IsCurrentMonth, IsPrior60Days (updated daily)
│   │   │   ├── IsFiscalMonthEnd and other corporate calendar attributes
│   │   │   └── Lag day column (0=today, -1=yesterday, +1=tomorrow)
│   │   └── Time-of-Day as a Dimension or Fact
│   │       ├── Separate from date dimension to avoid row count explosion
│   │       ├── If grouping needed (shifts, lunch hour): time-of-day dimension (1,440 rows, one per minute)
│   │       ├── If no grouping needed: simple date/time fact in fact table
│   │       └── Time lags computed from date/time stamps
│   ├── Product Dimension (Figure 3-8)
│   │   ├── Describes every SKU; may have 300,000+ rows
│   │   ├── Sourced from operational product master file
│   │   ├── Columns (partial list from Figure 3-8):
│   │   │   ├── Product Key (PK), SKU Number (NK)
│   │   │   ├── Product Description, Brand Description
│   │   │   ├── Subcategory Description, Category Description
│   │   │   ├── Department Number, Department Description
│   │   │   ├── Package Type Description, Package Size
│   │   │   ├── Fat Content, Diet Type
│   │   │   ├── Weight, Weight Unit of Measure
│   │   │   ├── Storage Type, Shelf Life Type
│   │   │   └── Shelf Width, Shelf Height, Shelf Depth
│   │   ├── Flatten Many-to-One Hierarchies
│   │   │   ├── Merchandise hierarchy: SKU --> Brand --> Category --> Department
│   │   │   ├── Figure 3-7: Sample rows showing flattened hierarchy
│   │   │   ├── Repeated low-cardinality values are acceptable (e.g., 6,000 rows per department value)
│   │   │   └── Do NOT normalize repeated values into separate tables
│   │   ├── Multiple hierarchies common (merchandise hierarchy + package type, etc.)
│   │   ├── Attributes with Embedded Meaning
│   │   │   ├── Operational codes with meaningful sub-parts (e.g., chars 5-9 = manufacturer)
│   │   │   └── Preserve whole code AND break into separate attributes
│   │   ├── Numeric Values as Attributes or Facts
│   │   │   ├── Standard list price: numeric but changes infrequently --> dimension attribute
│   │   │   ├── If used for calculation --> fact table; if for filtering/grouping --> dimension
│   │   │   ├── Sometimes store in BOTH fact and dimension tables
│   │   │   └── Data for calculations in facts; data for constraints/groups/labels in dimensions
│   │   └── Drilling Down on Dimension Attributes
│   │       ├── Drill down = add row header from dimension; drill up = remove row header
│   │       ├── Can drill on any attribute, not just within a hierarchy
│   │       ├── Figure 3-9: Drill from Department --> Brand or Department --> Fat Content
│   │       └── 50+ descriptive attributes per product dimension is reasonable
│   ├── Store Dimension (Figure 3-10)
│   │   ├── Describes every store in the grocery chain
│   │   ├── May need to assemble from multiple operational sources
│   │   ├── Columns (partial list from Figure 3-10):
│   │   │   ├── Store Key (PK), Store Number (NK), Store Name
│   │   │   ├── Store Street Address, Store City, Store County
│   │   │   ├── Store City-State, Store State, Store Zip Code
│   │   │   ├── Store Manager, Store District, Store Region
│   │   │   ├── Floor Plan Type, Photo Processing Type, Financial Service Type
│   │   │   ├── Selling Square Footage, Total Square Footage
│   │   │   └── First Open Date, Last Remodel Date
│   │   ├── Short text descriptors (10-20 chars), not single-character codes
│   │   ├── Selling square footage: numeric but belongs in dimension (used as constraint/label, not sum)
│   │   ├── Multiple Hierarchies in Dimension Tables
│   │   │   ├── Geographic hierarchy: Store --> ZIP --> County --> State
│   │   │   ├── Organizational hierarchy: Store --> District --> Region
│   │   │   ├── City-State attribute needed (cities not unique within US)
│   │   │   └── Attribute names must be unique across hierarchies
│   │   └── Dates Within Dimension Tables
│   │       ├── First Open Date, Last Remodel Date as date type columns
│   │       ├── For calendar grouping/constraining: join to copies of date dimension via views
│   │       ├── View-based role-playing date dimension (e.g., FIRST_OPEN_DATE view)
│   │       └── Example of dimension role playing
│   ├── Promotion Dimension (Figure 3-11) -- "Causal Dimension"
│   │   ├── Describes promotion conditions under which a product is sold
│   │   ├── Promotion mechanisms: temporary price reductions, ads, displays, coupons
│   │   ├── Promotion effectiveness metrics:
│   │   │   ├── Lift (gain in sales during promotion vs. baseline)
│   │   │   ├── Time shifting (sales drop before/after promotion)
│   │   │   ├── Cannibalization (sales of nearby products decrease)
│   │   │   ├── Market growth (net gain across promoted category)
│   │   │   └── Profitability (incremental profit over baseline, net of costs)
│   │   ├── One row per unique combination of promotion conditions
│   │   ├── Columns (from Figure 3-11):
│   │   │   ├── Promotion Key (PK), Promotion Code, Promotion Name
│   │   │   ├── Price Reduction Type, Promotion Media Type
│   │   │   ├── Ad Type, Display Type, Coupon Type
│   │   │   ├── Ad Media Name, Display Provider
│   │   │   ├── Promotion Cost (for constraining/grouping only, not in transaction fact)
│   │   │   └── Promotion Begin Date, Promotion End Date
│   │   ├── Design choice: combined single dimension vs. four separate causal dimensions
│   │   │   ├── Combined: efficient browsing, smaller if mechanisms are correlated
│   │   │   └── Separate: more understandable if users think of mechanisms independently
│   │   └── Promotion cost at wrong grain for POS transaction fact; belongs in separate fact table
│   ├── Null Foreign Keys, Attributes, and Facts
│   │   ├── Non-promoted products: promotion dimension must include a "No Promotion" row (key 0 or -1)
│   │   ├── Never put null foreign keys in fact table -- violates referential integrity
│   │   ├── Null dimension attributes: substitute "Unknown" or "Not Applicable"
│   │   ├── Null values disappear from pull-down menus and cause grouping inconsistencies
│   │   ├── Null facts: leave as null for correct aggregate function behavior (SUM, AVG, COUNT)
│   │   └── Some OLAP products prohibit null attribute values
│   └── Other Retail Sales Dimensions
│       ├── Cashier dimension (small, non-private employee attributes; "No Cashier" row for self-service)
│       └── Payment method dimension (description, group: cash vs. credit)
│           └── Multiple payment methods per transaction: separate fact table at different grain
├── Degenerate Dimensions for Transaction Numbers
│   ├── POS transaction number on every line item row
│   ├── Header information already extracted into other dimensions
│   ├── Degenerate dimension (DD): dimension key with no corresponding dimension table
│   ├── Sits in fact table without joining to a dimension table
│   ├── Serves as grouping key for market basket analysis
│   ├── Enables link back to operational system
│   ├── Primary key of retail sales fact = POS transaction number + product key
│   ├── Order numbers, invoice numbers, bill-of-lading numbers are common DDs
│   └── If leftover attributes exist: create a real dimension table (no longer degenerate)
├── Retail Schema in Action
│   │   ├── Figure 3-12: Full querying schema with dimension attributes highlighted
│   │   │   (e.g., month=January, year=2013, district=Boston, category=Snacks)
│   │   └── Figure 3-13: Query results and cross-tabular "pivoted" report
├── Retail Schema Extensibility
│   ├── Adding Frequent Shopper dimension after initial rollout
│   │   ├── New FK in fact table, new dimension table
│   │   ├── Historical rows: default "Prior to Frequent Shopper Program" surrogate key
│   │   ├── Non-members: "Frequent Shopper Not Identified" row
│   │   └── Atomic grain enabled adding this dimension; summarized grain would not have
│   ├── Predictable schema extensibility patterns:
│   │   ├── New dimension attributes: add columns to existing dimension tables
│   │   ├── New dimensions: add FK column to fact table
│   │   └── New measured facts: add columns to fact table (null for old rows if needed)
│   └── Facts at different grain belong in their own fact table
├── Factless Fact Tables
│   ├── Problem: "What products were on promotion but did not sell?"
│   ├── Promotion Coverage Fact Table (Figure 3-14)
│   │   ├── Keys: Date Key (FK), Product Key (FK), Store Key (FK), Promotion Key (FK)
│   │   ├── Dummy fact: Promotion Count (=1) for counting convenience
│   │   ├── Grain: one row per product on promotion per store per day/week
│   │   └── No measurement metrics -- captures relationship between keys only
│   └── Answer via set difference: products on promotion MINUS products sold
├── Dimension and Fact Table Keys
│   ├── Dimension Table Surrogate Keys
│   │   ├── Meaningless integer primary keys assigned sequentially
│   │   ├── Aliases: artificial keys, synthetic keys, non-natural keys
│   │   ├── Column naming convention: "Key" suffix (PK or FK)
│   │   ├── Advantages of surrogate keys:
│   │   │   ├── Buffer DW from operational changes (code recycling, reassignment)
│   │   │   ├── Integrate multiple source systems (cross-reference mapping table)
│   │   │   ├── Improve performance (4-byte integer vs. bulky alphanumeric)
│   │   │   ├── Handle null/unknown conditions (special surrogate for "No Promotion", "Unknown")
│   │   │   └── Support dimension attribute change tracking (multiple profiles per natural key)
│   │   └── Cross-reference table in ETL system for surrogate key assignment
│   ├── Dimension Natural and Durable Supernatural Keys
│   │   ├── Natural keys (NK): business/production/operational keys from source systems
│   │   ├── Modeled as dimension attribute, identified by NK notation
│   │   ├── Multi-source natural keys: prepend source code (e.g., SAP|43251, CRM|6539152)
│   │   ├── Durable supernatural keys: permanent identifiers controlled by DW/BI system
│   │   │   ├── Immutable for life of system
│   │   │   ├── Simple integer, sequentially assigned
│   │   │   ├── Handled as dimension attribute, not replacement for surrogate PK
│   │   │   └── Needed when natural keys are not absolutely protected over time
│   │   └── Component parts of natural keys should be split into separate attributes
│   ├── Degenerate Dimension Surrogate Keys
│   │   ├── Not typically needed, but evaluate case by case
│   │   ├── Needed if transaction numbers are not unique across locations or get reused
│   │   ├── Needed if transaction number is bulky alphanumeric
│   │   └── If surrogate key + dimension table created: no longer degenerate
│   ├── Date Dimension Smart Keys
│   │   ├── Sequential integer (chronological) or meaningful YYYYMMDD format
│   │   ├── YYYYMMDD: benefits of surrogate + easier partition management
│   │   ├── Some optimizers prefer true date type column for partitioning intelligence
│   │   └── Reserve special date key value for "unknown date" situations
│   └── Fact Table Surrogate Keys
│       ├── Less demanded than for dimensions; mainly for back room ETL
│       ├── Simple integer assigned in sequence as rows are generated
│       ├── Benefits:
│       │   ├── Immediate unique identification of any fact row
│       │   ├── Backing out or resuming a bulk load (find max key)
│       │   ├── Replacing updates with inserts plus deletes
│       │   └── Parent key in parent/child fact table schemas
│       └── Primary key of fact table = subset of FKs and/or degenerate dimensions
├── Resisting Normalization Urges
│   ├── Snowflake Schemas with Normalized Dimensions
│   │   ├── Snowflaking: removing redundant attributes into separate normalized dimension tables
│   │   ├── Figure 3-15: Snowflaked product dimension (Brand, Category, Department, Package Type, Storage Type, Shelf Life Type dimensions)
│   │   ├── Arguments against snowflaking:
│   │   │   ├── Complex presentation; users struggle with many tables
│   │   │   ├── Database optimizers struggle with numerous joins --> slower queries
│   │   │   ├── Insignificant disk space savings (dimensions are <1% of total schema)
│   │   │   ├── Impairs cross-attribute browsing within a dimension
│   │   │   └── Defeats bitmap indexes on low-cardinality columns
│   │   ├── Fixed-depth hierarchies should be flattened in dimension tables
│   │   ├── Acceptable snowflaking situations: BI tool requirements, OLAP cube population (hidden from users)
│   │   └── Columnar databases more tolerant of centipede designs
│   ├── Outriggers
│   │   ├── Permissible dimension attached to another dimension's FK (one level removed from fact)
│   │   ├── Figure 3-16: Product dimension with Product Introduction Date Key (FK) --> Product Introduction Date Dimension (outrigger)
│   │   ├── Use only when business needs to filter/group a dimension's date by nonstandard calendar attributes
│   │   ├── Outrigger date attributes must be uniquely labeled to distinguish from primary date dimension
│   │   ├── Downsides: more joins, reduced legibility, hampers attribute browsing
│   │   └── Should be the exception rather than the rule
│   └── Centipede Fact Tables with Too Many Dimensions
│       ├── Caused by denormalizing dimension hierarchies into the fact table instead of dimension tables
│       ├── Figure 3-17: Centipede fact table with ~25 FKs (Week, Month, Quarter, Year, Fiscal Year, Fiscal Month, Brand, Category, Department, Package Type, Store County, Store State, Store District, Store Region, Store Floor Plan, Promotion Reduction Type, Promotion Media Type dimensions)
│       ├── Enormous multipart key; cannot be effectively indexed
│       ├── Most business processes represented with <20 dimensions
│       ├── 25+ dimensions: look for correlated dimensions to combine
│       └── Columnar databases reduce storage/query penalties of centipede designs
└── Summary
    ├── Four-step design process for dimensional models
    ├── Clearly state grain; load fact table with atomic data
    └── Populate dimension tables with verbose, robust descriptive attributes
```

### chapter-4-inventory-pp-111-139

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-4-inventory-pp-111-139
Hash: 5770ca967047

```
Chapter 4: Inventory
├── Value Chain Introduction
│   ├── Value chain = natural, logical flow of an organization's primary activities
│   ├── Retailer's value chain (Figure 4-1):
│   │   ├── Issue Purchase Order to Manufacturer
│   │   ├── Receive Warehouse Deliveries
│   │   ├── Warehouse Product Inventory
│   │   ├── Receive Store Deliveries
│   │   ├── Store Product Inventory
│   │   └── Retail Sales
│   ├── Each process produces unique metrics at unique granularity/dimensionality
│   ├── Each process spawns one or more fact tables
│   └── Products sourced directly from manufacturers bypass warehousing
├── Inventory Models (three complementary schemas)
│   ├── Inventory Periodic Snapshot
│   │   ├── Grain: daily inventory for each product in each store (date + product + store)
│   │   ├── Store Inventory Snapshot Fact (Figure 4-2, simple version):
│   │   │   ├── Date Key (FK), Product Key (FK), Store Key (FK)
│   │   │   └── Quantity on Hand (semi-additive fact)
│   │   ├── Dimensions: Date, Product (with Storage Requirement Type), Store
│   │   ├── Date/Product/Store dimensions identical or conforming to Chapter 3
│   │   ├── Product dimension enhanced: minimum reorder quantity, storage requirement
│   │   ├── Store dimension enhanced: frozen/refrigerated storage square footages
│   │   ├── Dense fact table: row for every product in every store every day
│   │   │   ├── 60,000 products x 100 stores = 6 million rows per nightly load
│   │   │   ├── Only 14 bytes per row --> ~84 MB per load
│   │   │   └── Zero out-of-stock measurements included as explicit rows
│   │   ├── Managing density: reduce snapshot frequency over time
│   │   │   ├── Last 60 days: daily snapshots
│   │   │   ├── Older data: weekly snapshots
│   │   │   └── Daily and weekly snapshots in separate fact tables (different periodicity)
│   │   ├── Semi-Additive Facts
│   │   │   ├── Quantity on hand: additive across products and stores, NOT across dates
│   │   │   ├── All inventory levels, financial account balances, and intensity measures are semi-additive
│   │   │   ├── Combine across dates by averaging (not summing)
│   │   │   ├── SQL AVG function is incorrect: averages over all rows (products x stores x dates), not just dates
│   │   │   ├── Correct approach: SUM across non-date dimensions, then divide by number of date periods
│   │   │   └── OLAP cubes can define per-dimension aggregation rules for semi-additive measures
│   │   └── Enhanced Inventory Facts (Figure 4-3)
│   │       ├── Store Inventory Snapshot Fact (enhanced):
│   │       │   ├── Date Key (FK), Product Key (FK), Store Key (FK)
│   │       │   ├── Quantity on Hand (semi-additive)
│   │       │   ├── Quantity Sold (fully additive -- rolled up to daily grain)
│   │       │   ├── Inventory Dollar Value at Cost (extended, additive)
│   │       │   └── Inventory Dollar Value at Latest Selling Price (extended, additive)
│   │       ├── Derived metrics from enhanced facts:
│   │       │   ├── Number of turns = quantity sold / quantity on hand (daily); total qty sold / daily avg qty on hand (extended period)
│   │       │   └── Days' supply = final quantity on hand / average quantity sold (over time span)
│   │       └── Optional: beginning balance, inventory change/delta, ending balance (deltas are fully additive)
│   ├── Inventory Transactions
│   │   ├── Records every transaction affecting inventory at the warehouse
│   │   ├── Example warehouse inventory transactions:
│   │   │   ├── Receive product, Place in inspection hold, Release from inspection
│   │   │   ├── Return to vendor (inspection failure), Place in bin, Pick from bin
│   │   │   ├── Package for shipment, Ship to customer
│   │   │   ├── Receive from customer (return), Return to inventory from customer return
│   │   │   └── Remove product from inventory
│   │   ├── Grain: one row per inventory transaction
│   │   ├── Warehouse Inventory Transaction Fact (Figure 4-4):
│   │   │   ├── Date Key (FK), Product Key (FK), Warehouse Key (FK)
│   │   │   ├── Inventory Transaction Type Key (FK)
│   │   │   ├── Inventory Transaction Number (DD -- degenerate dimension)
│   │   │   └── Inventory Transaction Dollar Amount
│   │   ├── Warehouse Dimension (Figure 4-4):
│   │   │   ├── Warehouse Key (PK), Warehouse Number (NK), Warehouse Name
│   │   │   ├── Warehouse Address, City, City-State, State, ZIP
│   │   │   ├── Warehouse Zone
│   │   │   └── Warehouse Total Square Footage
│   │   ├── Inventory Transaction Type Dimension:
│   │   │   ├── Inventory Transaction Type Key (PK)
│   │   │   ├── Inventory Transaction Type Description
│   │   │   └── Inventory Transaction Type Group
│   │   ├── Useful for measuring frequency/timing of specific transaction types
│   │   ├── Impractical as sole basis for inventory analysis (can't reconstruct position easily)
│   │   ├── Snapshot table complements transaction table
│   │   └── If transaction types have different dimensionality: separate fact tables per event type
│   └── Inventory Accumulating Snapshot
│       ├── For processes with definite beginning, definite end, and identifiable milestones
│       ├── One row inserted when product lot is received; updated as it moves through warehouse
│       ├── Grain: one row per product lot receipt (or per serial number/lot number)
│       ├── Inventory Receipt Accumulating Fact (Figure 4-5):
│       │   ├── Product Lot Receipt Number (DD -- degenerate dimension)
│       │   ├── Multiple date FKs (role-playing date dimensions):
│       │   │   ├── Date Received Key (FK), Date Inspected Key (FK)
│       │   │   ├── Date Bin Placement Key (FK)
│       │   │   ├── Date Initial Shipment Key (FK), Date Last Shipment Key (FK)
│       │   ├── Product Key (FK), Warehouse Key (FK), Vendor Key (FK)
│       │   ├── Quantity facts (updated over time):
│       │   │   ├── Quantity Received, Quantity Inspected
│       │   │   ├── Quantity Returned to Vendor, Quantity Placed in Bin
│       │   │   ├── Quantity Shipped to Customer, Quantity Returned by Customer
│       │   │   ├── Quantity Returned to Inventory, Quantity Damaged
│       │   └── Lag facts (elapsed time metrics):
│       │       ├── Receipt to Inspected Lag
│       │       ├── Receipt to Bin Placement Lag
│       │       ├── Receipt to Initial Shipment Lag
│       │       └── Initial to Last Shipment Lag
│       ├── Figure 4-6: Evolution of an accumulating snapshot row (lot 101)
│       │   ├── Row inserted when received (other date keys = 0, lags empty)
│       │   ├── Row updated when inspected (Date Inspected Key filled, Receipt to Inspected Lag = 2)
│       │   └── Row updated when placed in bin (Date Bin Placement Key filled, Receipt to Bin Placement Lag = 3)
│       ├── Row updated repeatedly until lot is completely depleted
│       └── Problematic for OLAP cubes (updates force cube reprocessing)
├── Fact Table Types (Figure 4-7 -- comparison table)
│   ├── Transaction Fact Tables
│   │   ├── Periodicity: discrete transaction point in time
│   │   ├── Grain: 1 row per transaction or transaction line
│   │   ├── Date dimension(s): transaction date
│   │   ├── Facts: transaction performance
│   │   ├── Sparsity: sparse or dense, depending on activity
│   │   ├── Updates: no updates, unless error correction
│   │   └── Most naturally dimensional; extreme detail; not revisited after posted
│   ├── Periodic Snapshot Fact Tables
│   │   ├── Periodicity: recurring snapshots at regular, predictable intervals
│   │   ├── Grain: 1 row per snapshot period plus other dimensions
│   │   ├── Date dimension(s): snapshot date
│   │   ├── Facts: cumulative performance for time interval
│   │   ├── Sparsity: predictably dense
│   │   ├── Updates: no updates, unless error correction
│   │   ├── Regular, predictable view of longitudinal performance trends
│   │   ├── Fewer dimensions than companion transaction table
│   │   ├── Often more facts than transaction table (any activity during period is fair game)
│   │   └── Transaction snapshots are aggregations; inventory snapshots are direct measurements
│   ├── Accumulating Snapshot Fact Tables
│   │   ├── Periodicity: indeterminate time span for evolving pipeline/workflow
│   │   ├── Grain: 1 row per pipeline occurrence
│   │   ├── Date dimension(s): multiple dates for pipeline milestones
│   │   ├── Facts: performance for pipeline occurrence
│   │   ├── Sparsity: sparse or dense, depending on pipeline occurrence
│   │   ├── Updates: updated whenever pipeline activity occurs
│   │   ├── Lags Between Milestones and Milestone Counts
│   │   │   ├── Duration/lag metrics between key milestones
│   │   │   ├── Raw difference between date/time stamps, or workday-adjusted calculations
│   │   │   └── Milestone completion counters (0 or 1)
│   │   ├── Accumulating Snapshot Updates and OLAP Cubes
│   │   │   └── Updates to facts and FK date keys force cube reprocessing
│   │   └── Foreign key to status dimension (reflects pipeline's latest status)
│   └── Complementary Fact Table Types
│       ├── Transactions and snapshots are yin and yang of dimensional designs
│       ├── Both needed for complete view; no simple way to combine in single fact table
│       ├── Data redundancy between transaction and snapshot tables is acceptable
│       └── Accumulating + periodic snapshots can work together (e.g., rolling monthly accumulator becomes periodic at month end)
├── Value Chain Integration
│   ├── Business and IT need to look across processes end-to-end
│   ├── Figure 4-8: Shared dimensions among business processes
│   │   ├── Store Dimension shared by: Retail Sales, Retail Inventory, (not Warehouse)
│   │   ├── Date Dimension shared by: all three fact tables
│   │   ├── Product Dimension shared by: all three fact tables
│   │   ├── Promotion Dimension: Retail Sales only
│   │   └── Warehouse Dimension: Warehouse Inventory only
│   └── Common dimensions (date, product, store) are the integration glue
├── Enterprise Data Warehouse Bus Architecture
│   ├── Understanding the Bus Architecture
│   │   ├── "Bus" from electrical/computer industry -- common interface standard
│   │   ├── Standard bus interface for DW/BI: conformed dimensions and facts
│   │   ├── Separate process-centric models plug together if they adhere to the standard
│   │   ├── Figure 4-9: Enterprise data warehouse bus with shared dimensions
│   │   │   └── Dimensions: Date, Product, Store, Promotion, Warehouse, Vendor, Shipper
│   │   │   └── Processes: Purchase Orders, Store Inventory, Store Sales
│   │   ├── Independent of technology and database platform
│   │   └── Relational and OLAP-based models both participate if built around conformed dimensions/facts
│   ├── Enterprise Data Warehouse Bus Matrix (Figure 4-10)
│   │   ├── Rows = business processes; Columns = common dimensions
│   │   ├── Sample retailer matrix (11 processes x 6 dimensions):
│   │   │   ├── Processes: Issue Purchase Orders, Receive Warehouse/Store Deliveries, Warehouse/Store Inventory, Retail Sales, Retail Sales Forecast, Retail Promotion Tracking, Customer Returns, Returns to Vendor, Frequent Shopper Sign-Ups
│   │   │   └── Dimensions: Date, Product, Warehouse, Store, Promotion, Customer, Employee
│   │   ├── Cells marked with "X" to indicate dimension-process relationships
│   │   ├── Typically 25-50 rows and comparable number of columns
│   │   ├── Multiple Matrix Uses:
│   │   │   ├── Architecture planning, database design
│   │   │   ├── Data governance, project estimating
│   │   │   └── Organizational communication (upward, outward, across teams)
│   │   ├── Opportunity/Stakeholder Matrix (Figure 4-11)
│   │   │   ├── Same rows (business processes), columns = business functions (Merchandising, Marketing, Store Operations, Logistics, Finance)
│   │   │   └── Identifies which groups to invite for requirements, modeling, and BI specification
│   │   └── Common Bus Matrix Mistakes
│   │       ├── Row mistakes:
│   │       │   ├── Departmental or overly encompassing rows (should not mirror org chart)
│   │       │   └── Report-centric or too narrowly defined rows (should not be laundry list of reports)
│   │       └── Column mistakes:
│   │           ├── Overly generalized columns (e.g., generic "person" or "location" spanning unrelated populations)
│   │           └── Separate columns for each level of a hierarchy (use single dimension column at most granular level)
│   └── Retrofitting Existing Models to a Bus Matrix
│       ├── Assess gap between current stovepipe models and architected goal
│       ├── If sound dimensional design: map existing dimension to standardized version via cross-reference
│       ├── If poor design: may need to shut down and rebuild in proper bus architecture
│       └── Requires senior IT and business management commitment
├── Conformed Dimensions
│   ├── Cornerstone of the enterprise bus architecture
│   │   ├── Aliases: common dimensions, master dimensions, reference dimensions, shared dimensions
│   │   ├── Built once in ETL, replicated logically or physically across DW/BI environment
│   │   └── Usage must be mandated by CIO as organizational policy
│   ├── Drilling Across Fact Tables
│   │   ├── Combine metrics from different business processes in a single report
│   │   ├── Figure 4-12: Drill-across report (Open Orders Qty, Inventory Qty, Sales Qty by Product Description)
│   │   ├── Multipass SQL: query each model separately, full outer-join on conformed dimension attributes
│   │   ├── Implementations: temporary tables, application server, report-level joins
│   │   ├── Cross-fact calculations done in BI application after separate conformed results returned
│   │   └── Never join fact tables directly to each other
│   ├── Identical Conformed Dimensions
│   │   ├── Same dimension keys, attribute column names, attribute definitions, attribute values
│   │   ├── May be same physical table or duplicated synchronously
│   │   └── Attribute column names should be uniquely labeled across dimensions
│   ├── Shrunken Rollup Conformed Dimension with Attribute Subset
│   │   ├── Subset of attributes from a more granular dimension (Figure 4-13)
│   │   ├── Example: Brand Dimension conforms to Product Dimension (Brand, Subcategory, Category, Department descriptions)
│   │   ├── Example: Month Dimension conforms to Date Dimension (Calendar Month Name/Number, YYYY-MM, Calendar Year)
│   │   ├── Required when fact table captures metrics at higher granularity than atomic base dimension
│   │   └── Primary keys of detailed and rollup dimensions are separate
│   ├── Shrunken Conformed Dimension with Row Subset
│   │   ├── Same level of detail, but one represents only a subset of rows (Figure 4-14)
│   │   ├── Example: Corporate Product Dimension vs. Appliance Products subset vs. Apparel Products subset
│   │   ├── Drilling across requires common conformed attributes
│   │   └── Referential integrity implications if user accesses full fact table with subset dimension
│   └── Shrunken Conformed Dimensions on the Bus Matrix (Figure 4-15)
│       ├── Option 1: Mark cell for atomic dimension, document rollup/subset granularity within cell
│       └── Option 2: Subdivide dimension column into granularity sub-columns (e.g., Date split into Day | Month)
├── Limited Conformity
│   ├── Not always realistic to fully conform across conglomerate subsidiaries
│   ├── Litmus test: willingness to agree on common definitions for product, customer, etc.
│   ├── If unwilling: build separate DW per subsidiary
│   └── Least-common-denominator approach: conform a handful of attributes (e.g., product description, category, line of business) even if full conformity is impractical
├── Importance of Data Governance and Stewardship
│   ├── Key challenge: enterprise consensus on dimension attribute names, contents, definitions
│   ├── Business-Driven Governance
│   │   ├── Must be led by business subject matter experts, not IT alone
│   │   ├── Governance leader characteristics:
│   │   │   ├── Organizational respect, broad operational knowledge
│   │   │   ├── Balance organizational vs. departmental needs
│   │   │   ├── Authority to challenge status quo and enforce policies
│   │   │   └── Strong communication and negotiation skills
│   │   └── IT can facilitate but lacks organizational authority to drive adoption alone
│   ├── Governance Objectives
│   │   ├── Agreement on data definitions, labels, domain values
│   │   ├── Master data management (MDM) for centralized reference data
│   │   ├── Data quality and accuracy policies
│   │   └── Data security and access controls
│   └── Cultural challenge: shifting from departmental data silos to shared enterprise information
├── Conformed Dimensions and the Agile Movement
│   ├── Conformed dimensions enable agile DW/BI development (not hinder it)
│   ├── Build and maintain dimension tables once; reuse across projects
│   ├── Time-to-market shrinks as developers reuse existing conformed dimensions
│   ├── Start with minimalist conformed attributes (even a single attribute like product category)
│   ├── Iteratively expand during architectural agile sprints
│   └── Without conformed dimensions: departmental data silos with inconsistent categorizations
├── Conformed Facts
│   ├── ~5% of the data architecture effort (95% is conformed dimensions)
│   ├── Facts appearing in multiple models must have identical definitions, equations, and units of measure
│   ├── Revenue, profit, standard prices, costs, KPIs must conform
│   ├── If definitions differ: use different names to prevent users from combining incompatible facts
│   ├── Incompatible units of measure across value chain (e.g., shipping cases at warehouse vs. scanned units at store)
│   │   ├── Incorrect solution: conversion factor buried in product dimension
│   │   └── Correct solution: carry fact in both units of measure so reports can glide down value chain
│   └── Revenue facts must be labeled uniquely if definitional differences exist
└── Summary
    ├── Three complementary inventory models: periodic snapshot, transaction, accumulating snapshot
    ├── Periodic snapshot: best for long-running, continuously replenished inventory
    ├── Accumulating snapshot: best for finite pipeline with definite beginning and end
    ├── Transaction schema: augments snapshot models for detailed analysis
    ├── Enterprise data warehouse bus architecture and matrix for incremental, integrated DW/BI
    ├── Conformed dimensions are the cornerstone of integration
    ├── Conformed facts ensure consistent metric definitions across processes
    └── Data governance is essential for achieving and maintaining conformity
```

### chapter-5-procurement-pp-141-165

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-5-procurement-pp-141-165
Hash: 1e68d0b9a25a

```
Chapter 5: Procurement
├── Procurement Case Study
│   ├── Cross-industry applicability (any org that acquires products/services)
│   ├── Upstream value chain (from retail sales/inventory toward suppliers)
│   └── Common analytic requirements
│       ├── Most frequently purchased materials/products
│       ├── Vendor pricing and consolidation opportunities
│       ├── Maverick spending detection (bypassing preferred vendors)
│       ├── Contract purchase price variance
│       └── Vendor performance (fill rate, on-time delivery, rejection rate)
├── Procurement Transactions and Bus Matrix
│   ├── Four-step dimensional design process applied to procurement
│   ├── Procurement Transaction Fact Table (Figure 5-1)
│   │   ├── Grain: one row per procurement transaction
│   │   ├── Dimensions
│   │   │   ├── Date Dimension
│   │   │   ├── Product Dimension (conformed from Retail Sales)
│   │   │   ├── Vendor Dimension (name, address, status, minority ownership, corporate parent)
│   │   │   ├── Contract Terms Dimension (description, type)
│   │   │   └── Procurement Transaction Type Dimension (description, category)
│   │   ├── Degenerate Dimensions
│   │   │   └── Contract Number (DD)
│   │   └── Facts
│   │       ├── Procurement Transaction Quantity
│   │       └── Procurement Transaction Dollar Amount
│   └── Transaction types: purchase requisitions, purchase orders, shipping notifications, receipts, payments
├── Single Versus Multiple Transaction Fact Tables
│   ├── Design decision criteria
│   │   ├── What are the users' analytic requirements?
│   │   ├── Are there really multiple unique business processes?
│   │   ├── Are multiple source systems capturing metrics with unique granularities?
│   │   └── What is the dimensionality of the facts?
│   ├── Bus Matrix with granularity and metrics columns (Figure 5-2)
│   │   ├── Purchase Requisitions: 1 row per requisition line, Requisition Quantity & Dollars
│   │   ├── Purchase Orders: 1 row per PO line, PO Quantity & Dollars
│   │   ├── Shipping Notifications: 1 row per shipping notice line, Shipped Quantity
│   │   ├── Warehouse Receipts: 1 row per receipt line, Received Quantity
│   │   ├── Vendor Invoices: 1 row per invoice line, Invoice Quantity & Dollars
│   │   └── Vendor Payments: 1 row per payment, Invoice/Discount/Net Payment Dollars
│   ├── Shared dimensions: Date, Product, Vendor, Contract Terms, Employee, Warehouse, Carrier
│   └── Multiple Fact Tables Design (Figure 5-3)
│       ├── Purchase Requisition Fact
│       ├── Purchase Order Fact
│       ├── Shipping Notices Fact
│       ├── Warehouse Receipts Fact
│       └── Vendor Payment Fact
├── Complementary Procurement Snapshot
│   ├── Accumulating Snapshot Fact Table (Figure 5-4)
│   │   ├── Grain: one row per product purchase, updated as milestones occur
│   │   ├── Multiple role-playing date dimensions
│   │   │   ├── Purchase Order Date
│   │   │   ├── Requested By Date
│   │   │   ├── Warehouse Receipt Date
│   │   │   ├── Vendor Invoice Date
│   │   │   └── Vendor Payment Date
│   │   ├── Degenerate dimensions
│   │   │   ├── Contract Number, Purchase Order Number
│   │   │   ├── Warehouse Receipt Number, Vendor Invoice Number
│   │   │   └── Payment Check Number
│   │   ├── Quantity facts at each stage
│   │   │   ├── Purchase Order Quantity, Shipped Quantity
│   │   │   └── Received Quantity
│   │   ├── Dollar amount facts
│   │   │   ├── Purchase Order Dollar Amount
│   │   │   ├── Vendor Invoice Dollar Amount
│   │   │   ├── Vendor Discount Dollar Amount
│   │   │   └── Vendor Net Payment Dollar Amount
│   │   └── Lag facts (date differences between milestones)
│   │       ├── PO to Requested By Date Lag
│   │       ├── PO to Receipt Date Lag
│   │       ├── Requested By to Receipt Date Lag
│   │       ├── Receipt to Payment Date Lag
│   │       └── Invoice to Payment Date Lag
│   └── Well-defined milestones required (not continuous flow)
├── Slowly Changing Dimension Basics
│   ├── Dimension attributes change slowly over time
│   ├── Business governance must be involved in SCD decisions
│   ├── Surrogate keys vs. natural keys (natural key demoted to attribute)
│   ├── Type 0: Retain Original
│   │   ├── Dimension attribute value never changes
│   │   ├── Facts always grouped by original value
│   │   ├── Example: customer original credit score, date dimension attributes
│   │   └── Persistent durable keys are always type 0
│   ├── Type 1: Overwrite
│   │   ├── Overwrite old attribute value with current value
│   │   ├── No history of prior values maintained
│   │   ├── Appropriate for insignificant corrections
│   │   ├── Fact table untouched but historical context lost
│   │   ├── BI reports produce different results before vs. after overwrite
│   │   ├── Preexisting aggregations must be rebuilt
│   │   └── OLAP cubes need reprocessing if hierarchical rollup attribute
│   ├── Type 2: Add New Row
│   │   ├── New dimension row inserted with new surrogate key
│   │   ├── Primary workhorse technique for tracking SCD attributes
│   │   ├── Automatically partitions history in the fact table
│   │   ├── Type 2 Effective and Expiration Dates
│   │   │   ├── Row Effective Date (when profile becomes valid)
│   │   │   ├── Row Expiration Date (set to 9999-12-31 for current)
│   │   │   ├── Current Row Indicator flag
│   │   │   └── Use BETWEEN for date range queries (avoid nulls)
│   │   ├── Surrogate key administration required
│   │   ├── Type 1 Attributes in Type 2 Dimensions
│   │   │   └── Type 1 change may require updating multiple type 2 rows
│   │   ├── No need to rebuild aggregations or reprocess OLAP cubes
│   │   └── Safest response if business rules are uncertain
│   ├── Type 3: Add New Attribute
│   │   ├── Add new column to capture attribute change (no new row)
│   │   ├── Current and prior attribute values coexist on same row
│   │   ├── Supports "alternate realities" -- both old and new views simultaneously
│   │   ├── Infrequently used; best for significant en masse changes
│   │   ├── Example: sales force reorganization, product line restructuring
│   │   ├── Multiple Type 3 Attributes
│   │   │   └── Series of annual columns (Current, 2012, 2011 department names)
│   │   └── OLAP cubes may need reprocessing for hierarchical rollup
│   ├── Type 4: Add Mini-Dimension
│   │   ├── Break off frequently changing attributes into separate mini-dimension
│   │   ├── Addresses browsing performance and change tracking for large dimensions
│   │   ├── Continuously variable attributes converted to banded ranges
│   │   ├── Example: Demographics Dimension (Age Band, Purchase Frequency Score, Income Level)
│   │   ├── Mini-dimension FK in fact table captures profile at time of event
│   │   ├── Reasonable upper limit ~100,000 rows (e.g., 5 attributes x 10 values = 10^5)
│   │   └── Factless fact table for point-in-time profiling outside business events
│   └── Hybrid Slowly Changing Dimension Techniques
│       ├── Type 5: Mini-Dimension and Type 1 Outrigger (4 + 1 = 5)
│       │   ├── Add current mini-dimension key as type 1 overwritten FK in base dimension
│       │   ├── Enables current profile counts and rollups without fact table
│       │   ├── Logical view merges base dimension and current mini-dimension
│       │   └── Outrigger when demographics key is FK in customer dimension (not fact table)
│       ├── Type 6: Add Type 1 Attributes to Type 2 Dimension (1 + 2 + 3 = 6)
│       │   ├── Historic department column (type 2, historically accurate)
│       │   ├── Current department column (type 1, overwritten on all rows)
│       │   ├── New type 2 row issued for each change
│       │   ├── All prior rows get current value overwritten
│       │   └── Supports both point-in-time and current attribute reporting
│       └── Type 7: Dual Type 1 and Type 2 Dimensions (next available number)
│           ├── Fact table has both surrogate key (type 2) and durable natural key (type 1)
│           ├── Type 2 dimension: historically accurate attributes
│           ├── Current Product Dimension view: filtered to current rows only
│           ├── Durable key joins to current-only view for current reporting
│           ├── Variation: single surrogate key with view delivering current attributes
│           ├── Type 7 for Random "As Of" Reporting
│           │   └── Filter type 2 rows by effective/expiration dates for any point-in-time
│           └── Less ETL effort than type 6 (current view derived automatically)
└── Slowly Changing Dimension Recap (Figure 5-17)
    ├── Type 0: No change -- facts with original value
    ├── Type 1: Overwrite -- facts with current value
    ├── Type 2: Add row -- facts with value in effect when fact occurred
    ├── Type 3: Add column -- facts with both current and prior values
    ├── Type 4: Mini-dimension -- facts with rapidly changing attributes at event time
    ├── Type 5: Type 4 + type 1 outrigger -- above plus current rapidly changing values
    ├── Type 6: Type 1 overwritten attrs on type 2 rows -- historical + current values
    └── Type 7: Dual FKs for type 1 and type 2 dimensions -- historical + current values
```

### chapter-6-order-management-pp-167-199

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-6-order-management-pp-167-199
Hash: 3e0e5022f472

```
Chapter 6: Order Management
├── Order Management Bus Matrix (Figure 6-1)
│   ├── Business processes (rows)
│   │   ├── Quoting
│   │   ├── Ordering
│   │   ├── Shipping to Customer
│   │   ├── Shipment Invoicing
│   │   ├── Receiving Payments
│   │   └── Customer Returns
│   └── Conformed dimensions (columns): Date, Customer, Product, Sales Rep, Deal, Warehouse, Shipper
├── Order Transactions
│   ├── Order Line Transaction Fact Table (Figure 6-2)
│   │   ├── Grain: one row per order line item
│   │   ├── Dimensions
│   │   │   ├── Order Date Dimension
│   │   │   ├── Requested Ship Date Dimension
│   │   │   ├── Customer Dimension
│   │   │   ├── Product Dimension
│   │   │   ├── Sales Rep Dimension
│   │   │   └── Deal Dimension
│   │   ├── Degenerate Dimensions
│   │   │   ├── Order Number (DD)
│   │   │   └── Order Line Number (DD)
│   │   └── Facts
│   │       ├── Order Line Quantity
│   │       ├── Extended Order Line Gross Dollar Amount
│   │       ├── Extended Order Line Discount Dollar Amount
│   │       └── Extended Order Line Net Dollar Amount
│   └── Fact Normalization
│       ├── Anti-pattern: single generic fact with measurement type dimension
│       ├── Multiplies rows by number of fact types (e.g., 10M -> 40M rows)
│       ├── Makes inter-fact arithmetic (ratios, differences) difficult in SQL
│       └── Only appropriate for extremely sparse, unrelated facts
├── Dimension Role Playing
│   ├── Single physical date dimension, multiple logical views/aliases (Figure 6-3)
│   │   ├── Order Date Dimension (view of Date)
│   │   └── Requested Ship Date Dimension (view of Date)
│   ├── SQL views with uniquely labeled columns (e.g., order_month vs. req_ship_month)
│   ├── Role Playing and the Bus Matrix (Figure 6-4)
│   │   └── Multiple date roles documented within a single cell or subcolumns
│   └── OLAP considerations: some products require separate physical dimensions per role
├── Product Dimension Revisited
│   ├── Characteristics
│   │   ├── Numerous verbose, descriptive columns (100+ for manufacturers)
│   │   ├── One or more attribute hierarchies plus non-hierarchical attributes
│   │   └── Flattened denormalized table (resist snowflaking)
│   └── ETL transformations
│       ├── Remap operational product code to surrogate key
│       ├── Add descriptive attribute values (replace cryptic codes)
│       ├── Quality check attribute values (spelling, completeness)
│       └── Document attribute definitions and metadata
├── Customer Dimension (Figure 6-5)
│   ├── Grain: one row per discrete ship-to location
│   ├── Attributes: Name, Ship To (Address/City/County/State/ZIP/Region), Bill To, Organization, Corporate Parent, Credit Rating
│   ├── Multiple independent hierarchies
│   │   ├── Geographic hierarchy (city -> county -> state -> country)
│   │   ├── ZIP code hierarchy (ZIP -> ZIP Region -> Sectional Center)
│   │   └── Organizational hierarchy (ship-to -> bill-to -> corporate parent)
│   ├── Ship-to / Bill-to considerations
│   │   ├── Many-to-one: embed bill-to in customer dimension
│   │   ├── Many-to-many: separate ship-to and bill-to dimensions
│   │   └── Grain adjustment: each unique ship-to/bill-to combination
│   └── Single Versus Multiple Dimension Tables
│       ├── Decision factors for combining sales rep with customer
│       │   ├── Is the relationship truly one-to-one or many-to-many?
│       │   ├── Does relationship vary over time or by another dimension?
│       │   ├── Is the customer dimension extremely large?
│       │   ├── Do dimensions participate independently in other fact tables?
│       │   └── Does the business think of them as separate things?
│       └── Factless Fact Table for Customer/Rep Assignments (Figure 6-6)
│           ├── Tracks historical sales rep assignments to customers
│           ├── Dual date keys (effective and expiration dates)
│           ├── Customer Assignment Counter (=1) fact
│           └── Enables comparison with order activity via set operations
├── Deal Dimension (Figure 6-7)
│   ├── Similar to promotion dimension (terms, allowances, incentives)
│   ├── Attributes: Deal Description, Terms, Allowance, Special Incentive, Local Budget Indicator
│   └── Single vs. split: correlated factors -> single; uncorrelated -> multiple dimensions
├── Degenerate Dimension for Order Number
│   ├── Order number as degenerate dimension (no join to dimension table)
│   ├── Groups line items on an order; links to operational system
│   ├── Order line number as second degenerate dimension
│   ├── May be part of fact table primary key
│   └── Resist dumping order header info into an order dimension
├── Junk Dimensions
│   ├── Grouping of low-cardinality flags and indicators
│   ├── Also called "transaction indicator" or "transaction profile dimension"
│   ├── Options for handling miscellaneous flags
│   │   ├── Ignore them
│   │   ├── Leave on fact row (undesirable: cryptic codes or bulky text)
│   │   ├── Each flag as its own dimension (only if FK count stays < ~20)
│   │   └── Store in order header dimension (ill-advised)
│   ├── Order Indicator Junk Dimension example (Figure 6-8)
│   │   └── Payment Type Description, Payment Type Group, Order Type, Commission Credit Indicator
│   ├── Cartesian product of combinations: 10 two-value flags -> max 1,024 rows
│   └── Build beforehand vs. on encounter (depends on expected combination count)
├── Header/Line Pattern to Avoid
│   ├── Anti-pattern 1: Transaction header as dimension (Figure 6-9)
│   │   ├── Order Header Dimension grows at nearly the same rate as fact table
│   │   ├── Dimension nearly as large as fact table (1:5 ratio)
│   │   └── All interesting header attributes belong in proper analytic dimensions
│   ├── Anti-pattern 2: Header as separate fact table (Figure 6-13)
│   │   ├── Line facts not inheriting header dimensionality
│   │   └── Requires joining two large fact tables for any header-based analysis
│   └── Proper approach: push header attributes into line-level dimensions
├── Multiple Currencies (Figures 6-10, 6-11)
│   ├── Dual sets of facts: local currency + standard corporate currency
│   ├── Local Currency Dimension (FK in fact table)
│   ├── Conversion rate applied during ETL (behind the scenes in views)
│   ├── Standard currency metrics fully additive; local only within single currency
│   ├── Currency Conversion Fact Table (Figure 6-11)
│   │   ├── Conversion Date Key, Source/Destination Currency Key
│   │   └── Bidirectional exchange rates
│   └── Supports end-of-month/quarter close rates
├── Transaction Facts at Different Granularity
│   ├── Allocating header-level facts to line items (Figure 6-12)
│   │   ├── Example: shipping charges allocated to line items
│   │   ├── Allocation enables slicing by all dimensions including product
│   │   └── Activity-based costing measures as allocation mechanism
│   ├── Alternative (undesirable) techniques
│   │   ├── Repeat unallocated header fact on every line (overcounting risk)
│   │   ├── Store on first or last line only (disappears with product filter)
│   │   └── Special product key for header facts (decoder ring complexity)
│   └── WARNING: Never mix fact granularities in a single fact table
├── Invoice Transactions (Figure 6-14)
│   ├── Shipment Invoice Line Transaction Fact
│   │   ├── Grain: one row per invoice line item
│   │   ├── Date Dimension (views for 3 roles: Invoice, Requested Ship, Actual Ship)
│   │   ├── Dimensions: Product, Customer, Sales Rep, Deal, Warehouse, Shipper, Service Level
│   │   ├── Degenerate: Invoice Number, Invoice Line Number
│   │   ├── Revenue facts
│   │   │   ├── Extended Invoice Line Gross Dollar Amount
│   │   │   ├── Extended Invoice Line Allowance Dollar Amount
│   │   │   ├── Extended Invoice Line Discount Dollar Amount
│   │   │   └── Extended Invoice Line Net Dollar Amount
│   │   ├── Cost facts
│   │   │   ├── Extended Invoice Line Fixed Mfg Cost Dollar Amount
│   │   │   ├── Extended Invoice Line Variable Mfg Cost Dollar Amount
│   │   │   ├── Extended Invoice Line Storage Cost Dollar Amount
│   │   │   └── Extended Invoice Line Distribution Cost Dollar Amount
│   │   ├── Extended Invoice Line Contribution Dollar Amount
│   │   └── Service level metrics
│   │       ├── Shipment On-Time Counter (additive 0/1)
│   │       └── Requested to Actual Ship Lag
│   └── Most powerful fact table: combines customers, products, revenues, costs, profitability
├── Service Level Performance as Facts, Dimensions, or Both
│   ├── Quantitative: on-time counter, lag metrics (days between dates)
│   ├── Qualitative: Service Level Dimension (Figure 6-15)
│   │   └── Service Level Description (On-time, 1 day early, 2 days late...) + Service Level Group
│   └── Both perspectives complement each other
├── Profit and Loss Facts
│   ├── P&L statement structure in invoice fact table
│   │   ├── Quantity shipped
│   │   ├── Extended gross amount (list price x quantity)
│   │   ├── Extended allowance amount (off-invoice allowance)
│   │   ├── Extended discount amount (volume/payment term discounts)
│   │   ├── Extended net amount (gross - allowances - discounts)
│   │   ├── Extended fixed manufacturing cost
│   │   ├── Extended variable manufacturing cost
│   │   ├── Extended storage cost
│   │   ├── Extended distribution cost
│   │   └── Contribution amount (net - all costs; a.k.a. margin)
│   ├── All dollar values are "extended amounts" (unit rate x quantity)
│   ├── Profitability Words of Warning
│   │   ├── Cost facts often hardest to capture at atomic level
│   │   └── Activity-based costing may require parallel extraction programs
│   └── Sliceable P&L by any dimension (customer, product, deal profitability)
├── Audit Dimension (Figure 6-16)
│   ├── Exposes ETL metadata context to business users
│   ├── Attributes: Quality Indicator, Out of Bounds Indicator, Amount Adjusted Flag
│   ├── Cost Allocation Version, Foreign Currency Version
│   ├── Enables "instrumented reports" (Figure 6-17)
│   └── Modest design recommended (limit ETL complexity and row count)
├── Accumulating Snapshot for Order Fulfillment Pipeline
│   ├── Pipeline stages (Figure 6-18): Orders -> Backlog -> Release to Manufacturing -> Finished Goods Inventory -> Shipment -> Invoicing
│   ├── Order Fulfillment Accumulating Fact Table (Figure 6-19)
│   │   ├── Grain: one row per order line item (revisited/updated as milestones occur)
│   │   ├── Date Dimension (views for 9 roles)
│   │   │   ├── Order Date, Backlog Date, Release to Manufacturing Date
│   │   │   ├── Finished Inventory Placement Date
│   │   │   ├── Requested Ship Date, Scheduled Ship Date, Actual Ship Date
│   │   │   ├── Arrival Date, Invoice Date
│   │   │   └── Unknown/TBD date row for unfilled milestones
│   │   ├── Dimensions: Product, Customer, Sales Rep, Deal, Manufacturing Facility, Warehouse, Shipper
│   │   ├── Degenerate: Order Number, Order Line Number, Invoice Number
│   │   ├── Quantity facts at each pipeline stage
│   │   │   ├── Order Quantity, Release to Manufacturing Quantity
│   │   │   ├── Manufacturing Pass/Fail Inspection Quantity
│   │   │   ├── Finished Goods Inventory Quantity, Authorized to Sell Quantity
│   │   │   ├── Shipment Quantity, Shipment Damage Quantity
│   │   │   ├── Customer Return Quantity, Invoice Quantity
│   │   │   └── Extended Order/Invoice Dollar Amounts
│   │   └── Lag facts
│   │       ├── Order to Manufacturing Release Lag
│   │       ├── Manufacturing Release to Inventory Lag
│   │       ├── Inventory to Shipment Lag
│   │       └── Order to Shipment Lag
│   ├── Accumulating Snapshots and Type 2 Dimensions
│   │   └── Update to most current surrogate key for active pipelines
│   └── Complements transaction fact tables (pipeline velocity vs. event volumes)
├── Lag Calculations
│   ├── Numerical difference between any two milestone dates
│   ├── Usefully averaged over all dimensions
│   ├── Workday lags (exclude weekends/holidays)
│   ├── Sub-day granularity (hours/minutes) for short-lived processes
│   └── Calculated by ETL or delivered via views
├── Multiple Units of Measure (Figure 6-20)
│   ├── Base quantity facts + unit-of-measure conversion factors in fact table
│   ├── Example: 10 quantity facts + 4 conversion factors = 14 columns (vs. 50 physical columns)
│   ├── Conversion factors: Pallet, Retail Cases, Scan Units, Equivalized Consumer Units
│   ├── Delivered through views (intra-row multiplication is negligible cost)
│   └── Reduces pressure on product dimension for SCD type 2 changes
├── Beyond the Rearview Mirror
│   ├── Historical "rearview mirror" metrics vs. forward-looking "leading indicators"
│   ├── Prospecting, quoting activity as early pipeline stages
│   └── Leading indicators are additional bus matrix rows sharing conformed dimensions
└── Summary
    ├── Multiples: role-playing dimensions, multiple currencies, multiple units of measure
    ├── Header/line challenges: granularity, junk dimensions, anti-patterns
    ├── Invoice facts: rich P&L with dimensional profitability
    └── Accumulating snapshot: pipeline velocity and bottleneck identification
```

### chapter-7-accounting-pp-201-227

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-7-accounting-pp-201-227
Hash: 69005f2d9749

```
Chapter 7: Accounting
├── Accounting Case Study and Bus Matrix (Figure 7-1)
│   ├── Focus: general ledger (G/L), subledgers, budgeting
│   ├── Bus matrix rows
│   │   ├── General Ledger Transactions
│   │   ├── General Ledger Snapshot
│   │   ├── Budget
│   │   ├── Commitment
│   │   ├── Payments
│   │   └── Actual-Budget Variance
│   └── Dimensions: Date, Ledger, Account, Organization, Budget Line, Commitment Profile, Payment Profile
├── General Ledger Data
│   ├── Core foundation: ties together purchasing, payables, receivables
│   └── Complementary schemas needed: periodic snapshot + journal transactions
├── General Ledger Periodic Snapshot (Figure 7-2)
│   ├── Grain: one row per accounting period per most granular account level
│   ├── Dimensions
│   │   ├── Accounting Period Dimension (Period Number, Description, Fiscal Year)
│   │   ├── Ledger Dimension (Ledger Book Name)
│   │   ├── Account Dimension (Account Name, Category, Type)
│   │   └── Organization Dimension (Cost Center Name/Number, Department, Division, Business Unit, Company)
│   ├── Facts
│   │   ├── Period End Balance Amount (semi-additive -- cannot sum across time)
│   │   ├── Period Debit Amount
│   │   ├── Period Credit Amount
│   │   └── Period Net Change Amount
│   └── WARNING: Every query must constrain Ledger Dimension to single value (avoid double counting)
├── Chart of Accounts
│   ├── Intelligent key structure (account type encoded in number ranges)
│   ├── Account types: asset, liability, equity, income, expense
│   ├── Decomposes into Account dimension + Organization dimension
│   ├── Organization rollup: cost center -> department -> division -> business unit -> company
│   ├── Uniform chart of accounts (conformed across organizations)
│   └── Multiple sets of books/subledgers as separate Ledger dimension
├── Period Close
│   ├── End-of-period reconciliation and finalization
│   ├── DW/BI for analyzing closed results and pre-close anomaly detection
│   └── Trial balances loaded for haystack analysis before period ends
├── Year-to-Date Facts
│   ├── Anti-pattern: storing YTD/QTD totals in fact tables
│   ├── Violates grain; produces overstated results when summarized
│   ├── Should be calculated in BI reporting application, not stored
│   └── OLAP cubes handle to-date metrics more gracefully
├── Multiple Currencies Revisited
│   ├── Dual fact sets: local currency + standardized corporate currency
│   ├── Currency dimension FK for local currency type
│   └── Same technique as Chapter 6 Order Management
├── General Ledger Journal Transactions (Figure 7-3)
│   ├── Grain: one row per journal entry line (debit or credit)
│   ├── Dimensions
│   │   ├── Post Date Dimension
│   │   ├── Ledger Dimension
│   │   ├── Account Dimension
│   │   ├── Organization Dimension
│   │   └── Debit-Credit Indicator Dimension (two values only)
│   ├── Degenerate Dimensions
│   │   └── Journal Entry Number (DD)
│   ├── Facts
│   │   ├── Journal Entry Effective Date/Time
│   │   └── Journal Entry Amount
│   ├── Journal entry transaction profile dimension (type, description) if available
│   └── Complements periodic snapshot for drill-down into anomalies
├── Multiple Fiscal Accounting Calendars
│   ├── Fiscal periods often misalign with Gregorian calendar months
│   ├── Example: 13 four-week periods vs. 12 calendar months
│   ├── Single fiscal calendar: hierarchical attributes on daily date dimension
│   ├── Few unique calendars: uniquely labeled fiscal attributes on single date dimension
│   ├── Many subsidiary calendars: options
│   │   ├── Date dimension outrigger with multipart key (date + subsidiary)
│   │   ├── Separate physical date dimensions per subsidiary calendar
│   │   └── Subsidiary fiscal period dimension FK in fact table
│   └── 5-4-4 fiscal periods (5-week + two 4-week spans)
├── Drilling Down Through a Multilevel Hierarchy (Figure 7-4)
│   ├── Multiple ledgers: department -> division -> enterprise
│   ├── Parent Snapshot Surrogate Key in fact table (self-referencing FK)
│   ├── Enables drill-down from consolidated to detailed ledger entries
│   └── SQL example: SELECT * FROM GL_Fact WHERE Parent_Snapshot_key = (subquery)
├── Financial Statements
│   ├── Balance sheet and income statement from operational system
│   ├── DW/BI creates complementary aggregated data
│   ├── Financial statement line number/label tagging
│   └── Performance indicators and financial ratios at same detail level
├── Budgeting Process
│   ├── Budgeting Chain of Fact Tables (Figure 7-5)
│   │   ├── Budget Fact -> Commitment Fact -> Payment Fact
│   │   └── Dimensions expand as you move from budget to payments
│   ├── Budget Fact Table (Figure 7-6)
│   │   ├── Grain: net change of budget line item per organization cost center per month
│   │   ├── Dimensions
│   │   │   ├── Effective Date Dimension (Budget Effective Date Month/Year)
│   │   │   ├── Budget Line Item Dimension (Name, Version, Description, Year, Subcategory, Category)
│   │   │   ├── Account Dimension (reused from G/L)
│   │   │   └── Organization Dimension (reused from G/L)
│   │   ├── Fact: Budget Amount (fully additive, net change grain)
│   │   ├── Budget adjustments: additional rows with net change amounts
│   │   └── Annual vs. monthly budgets (add spending month role-playing dimension if needed)
│   ├── Commitment Fact Table
│   │   ├── Same dimensions as Budget + Commitment Dimension (Description, Party)
│   │   └── Fact: Commitment Amount
│   ├── Payment Fact Table
│   │   ├── Same dimensions as Commitment + Payment Dimension (Description, Party)
│   │   └── Fact: Payment Amount
│   └── Drill-across analysis
│       ├── Compare current budget vs. commitments vs. payments
│       ├── Sum amounts from beginning of time to current date
│       └── Multipass SQL to combine answer sets on common row headers
├── Dimension Attribute Hierarchies
│   ├── At least four hierarchy types: calendar, account, geographic, organization
│   ├── Fixed Depth Positional Hierarchies
│   │   ├── Fixed set of named levels as rollups
│   │   ├── Calendar: day -> fiscal period -> year; or day -> month -> year
│   │   ├── Account: manager level -> director level -> executive level
│   │   ├── 5-4-4 fiscal periods: parallel hierarchy sets in date dimension
│   │   ├── Each level must have a specific, meaningful name
│   │   └── WARNING: Avoid abstract names (Level-1, Level-2) -- hides ragged hierarchy
│   ├── Slightly Ragged Variable Depth Hierarchies (Figure 7-7)
│   │   ├── Geographic hierarchy: address -> city -> [district] -> [zone] -> state -> country
│   │   ├── Simple, medium, complex location variants
│   │   ├── Compromise: single dimension with max levels, propagate values down/up for missing levels
│   │   └── Works only for narrow range of hierarchy depths (e.g., 4-6 levels)
│   └── Ragged Variable Depth Hierarchies
│       ├── Organization hierarchy of indeterminate depth (Figure 7-8: 13-node tree)
│       ├── Classic parent/child recursive pointers (Figure 7-10)
│       │   ├── Organization Parent Key in dimension table
│       │   ├── Oracle CONNECT BY, SQL Server recursive CTEs
│       │   └── Problems: hierarchy locked in dimension, impractical for SCD type 2
│       ├── Bridge Table (Hierarchy Map Table) approach (Figures 7-11, 7-12)
│       │   ├── Organization Map Bridge table
│       │   │   ├── Parent Organization Key (FK)
│       │   │   ├── Child Organization Key (FK)
│       │   │   ├── Depth from Parent
│       │   │   ├── Highest Parent Flag
│       │   │   └── Lowest Child Flag
│       │   ├── One row per path from each parent to each descendant (including self)
│       │   ├── 13-node tree -> 43 rows in bridge table
│       │   ├── Constrain to single parent node -> fetches entire subtree
│       │   ├── Constrain Lowest Child Flag -> fetches only leaf nodes
│       │   └── Join: Organization Dimension -> Map Bridge -> Fact Table
│       ├── Shared Ownership in a Ragged Hierarchy (Figure 7-13)
│       │   ├── Percent Ownership column added to bridge table
│       │   ├── Example: node 10 is 50% owned by node 6, 50% by node 11
│       │   ├── Weighting applied to all path rows ending in shared node
│       │   └── Facts flow upward with fractional weights
│       ├── Time Varying Ragged Hierarchies (Figure 7-14)
│       │   ├── Begin Effective Date/Time and End Effective Date/Time on bridge table
│       │   ├── Query must constrain to single date/time to freeze hierarchy view
│       │   └── Old relationships expired, new paths inserted with begin date
│       ├── Modifying Ragged Hierarchies (Figure 7-15)
│       │   ├── Static case: delete old paths, insert new paths (simple SQL)
│       │   ├── Time-varying case: update end dates on old paths, insert new paths with begin dates
│       │   └── Only affected paths are modified; rest of tree untouched
│       └── Alternative Ragged Hierarchy Modeling Approaches
│           ├── Pathstring attribute approach (Figure 7-16)
│           │   ├── Each node labeled with concatenated path from root (e.g., AAB+, ABBA+)
│           │   ├── Wildcard navigation (A* = whole tree, *. = leaf nodes)
│           │   └── Vulnerable to relabeling ripples on insertion
│           ├── Modified preordered tree traversal (Figure 7-17)
│           │   ├── Left/Right numbering pairs identify subtrees
│           │   ├── Even more vulnerable to relabeling (entire tree to the right)
│           │   └── Any tree change causes cascading renumber
│           └── Advantages of Bridge Table Approach
│               ├── Alternative rollup structures selectable at query time
│               ├── Shared ownership rollups
│               ├── Time varying ragged hierarchies
│               ├── Limited impact for SCD type 2 changes
│               └── Limited impact when tree structure changes
├── Consolidated Fact Tables (Figure 7-19)
│   ├── Combine metrics from multiple business processes at common granularity
│   ├── Actual vs. Budget Variance Fact Table
│   │   ├── Dimensions: Accounting Period, Account, Organization
│   │   ├── Facts: Actual Amount, Budget Amount, Variance (calculated difference)
│   │   └── Multiple currency representations (local, corporate effective rate, corporate planned rate)
│   ├── "Least common denominator" of dimensionality
│   ├── Risk: designing only at consolidated grain, losing ability to drill into atomic data
│   └── WARNING: Do not create artificial facts/dimensions to force-fit different granularities
├── Role of OLAP and Packaged Analytic Solutions
│   ├── OLAP well suited for financial analysis
│   │   ├── Handles complex organizational rollups
│   │   ├── Inter-row calculations (net present value, compound growth)
│   │   ├── Proper debit/credit treatment by account type
│   │   ├── Financial consolidation functions
│   │   └── Complex security models (summary vs. detail access)
│   ├── Packaged analytic solutions
│   │   ├── Vendor cumulative experience reduces cost and risk
│   │   ├── Tools for extraction, staging, analysis, and interpretation
│   │   └── WARNING: Avoid stovepipe applications -- must conform dimensions across packages
│   └── Build vs. buy vs. integrate: most organizations use combination
└── Summary
    ├── General ledger: periodic snapshots + journal entry transactions
    ├── Common G/L challenges: multiple currencies, fiscal calendars, YTD totals
    ├── Ragged hierarchies: bridge table approach preferred over recursive pointers or pathstrings
    ├── Budgeting chain: budget -> commitment -> payment (net change grain)
    ├── Consolidated fact tables: actual vs. budget variance at common grain
    └── OLAP and packaged solutions: natural fit for financial analysis, must conform dimensions
```

### cross-chapter-design-pattern-summary

URL: https://local.taxonomy/kimball-dw-toolkit/cross-chapter-design-pattern-summary
Hash: 66c11e22978f

```
| Pattern | Ch 5 | Ch 6 | Ch 7 |
|---------|------|------|------|
| Bus matrix with granularity/metrics | Fig 5-2 | Fig 6-1 | Fig 7-1 |
| Transaction fact table | Procurement transactions | Order line items, Invoice line items | GL journal entries |
| Periodic snapshot | -- | -- | GL periodic snapshot |
| Accumulating snapshot | Procurement pipeline (Fig 5-4) | Order fulfillment pipeline (Fig 6-19) | -- |
| Role-playing dimensions | 5 date roles in pipeline | 2-9 date roles | Post date + effective date |
| Degenerate dimensions | Contract#, PO#, Receipt#, Check# | Order#, Line#, Invoice# | Journal Entry# |
| Junk dimensions | -- | Order indicator (Fig 6-8) | Debit-Credit indicator |
| Conformed dimensions | Date, Product, Vendor | Date, Product, Customer, Sales Rep | Date, Account, Organization, Ledger |
| SCD types 0-7 | Full taxonomy | Referenced (type 5 for sales rep) | Type 2 in bridge tables |
| Mini-dimensions (type 4) | Demographics example | -- | -- |
| Bridge tables | -- | -- | Organization map (ragged hierarchy) |
| Consolidated fact tables | -- | -- | Actual vs. Budget variance |
| Multiple currencies | -- | Dual facts + conversion table | Dual facts (local + corporate) |
| Factless fact tables | -- | Sales rep coverage (Fig 6-6) | -- |
| Allocation of header facts | -- | Shipping charges to line items | Budget line to G/L accounts |
| Audit dimension | -- | Fig 6-16 | -- |
| P&L / profitability facts | -- | Invoice contribution (Fig 6-14) | -- |


# Kimball Data Warehouse Toolkit 3e -- Taxonomy Tree: Chapters 8-10

Source: Kimball & Ross, *The Data Warehouse Toolkit*, 3rd Edition, pp. 229-296

---
```

### chapter-8-customer-relationship-management-pp-229-262

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-8-customer-relationship-management-pp-229-262
Hash: 15028da23163

```
Customer Relationship Management
|
+-- CRM Overview
|   +-- Operational CRM
|   |   +-- Synchronization of customer-facing processes
|   |   +-- Touch point data collection (sales, marketing, operations, service)
|   |   +-- Quote generation, purchase, fulfillment, payment, service
|   +-- Analytic CRM
|   |   +-- Closed-loop analytic CRM (Figure 8-1)
|   |   |   +-- Collect (Operational Source System)
|   |   |   +-- Integrate (ETL)
|   |   |   +-- Store (Data Presentation)
|   |   |   +-- Analyze and Report (BI Applications)
|   |   |   +-- Model (BI Applications) --> feeds back to Collect
|   |   +-- 360-degree customer view
|   |   +-- Up-sell / cross-sell identification
|   |   +-- Churn prediction, demand generation, retention
|   +-- Real-time / low latency CRM
|       +-- Hot response cache
|       +-- Intraday hybrid approach (real-time + nightly batch correction)
|
+-- Customer Dimension Attributes
|   +-- Name and Address Parsing
|   |   +-- Problem: overly general columns (Name, Address 1-6)
|   |   +-- Solution: parsed elemental attributes (Figure 8-3)
|   |       +-- Salutation, Informal Greeting Name, Formal Greeting Name
|   |       +-- First and Middle Names, Surname, Suffix
|   |       +-- Ethnicity, Title
|   |       +-- Street Number, Street Name, Street Type, Street Direction
|   |       +-- City, District, Second District, State, Region, Country, Continent
|   |       +-- Primary Postal Code, Secondary Postal Code, Postal Code Type
|   |       +-- Office Telephone (Country Code, Area Code, Number, Extension)
|   |       +-- Mobile Telephone (Country Code, Area Code, Number)
|   |       +-- E-mail, Web Site
|   |       +-- Public Key Authentication, Certificate Authority
|   |       +-- Unique Individual Identifier
|   +-- International Name and Address Considerations
|   |   +-- Unicode / character set support (ASCII vs. Unicode 6.2.0)
|   |   +-- International DW/BI Goals
|   |   |   +-- Universal and consistent (single root language, then translate)
|   |   |   +-- Sorting sequence differences across languages
|   |   |   +-- Attribute cardinality preservation across languages
|   |   |   +-- Localization of BI tool messages and prompts
|   |   +-- End-to-end data quality and downstream compatibility
|   |   +-- Cultural correctness (name ordering, salutations)
|   |   +-- Real-time customer response (5-second greeting window)
|   |   +-- Other kinds of addresses (electronic, security tokens, internet)
|   |   +-- Full address block attribute (postally-valid assembled address)
|   |   +-- International telephone dialing sequences
|   +-- Customer-Centric Dates
|   |   +-- Date of first purchase, date of last purchase, date of birth
|   |   +-- Foreign keys to date dimension (role-playing views)
|   |   +-- Date dimension outrigger (Figure 8-4)
|   |       +-- Date of 1st Purchase Dimension --> Customer Dimension --> Fact Table
|   +-- Aggregated Facts as Dimension Attributes
|   |   +-- Spending totals stored as dimension attributes for constraining/labeling
|   |   +-- Descriptive value bands (e.g., "High Spender") instead of raw numbers
|   |   +-- ETL burden: must be accurate, up-to-date, consistent with fact rows
|   +-- Segmentation Attributes and Scores
|   |   +-- Classification attributes
|   |   |   +-- Gender, Ethnicity
|   |   |   +-- Age / life stage classifications
|   |   |   +-- Income / lifestyle classifications
|   |   |   +-- Status (new, active, inactive, closed)
|   |   |   +-- Referring source
|   |   |   +-- Business-specific market segment
|   |   +-- Statistical segmentation scores
|   |   |   +-- Purchase behavior, payment behavior
|   |   |   +-- Propensity to churn, probability to default
|   |   +-- Behavior Tag Time Series
|   |       +-- RFI / RFM measures (Recency, Frequency, Intensity/Monetary)
|   |       +-- RFI cube (Figure 8-5) -- quintile axes (1-5)
|   |       +-- Data mining cluster labels (A through H behavior tags)
|   |       |   +-- A: High volume repeat, good credit, few returns
|   |       |   +-- B: High volume repeat, good credit, many returns
|   |       |   +-- C: Recent new customer, no established credit
|   |       |   +-- D: Occasional customer, good credit
|   |       |   +-- E: Occasional customer, poor credit
|   |       |   +-- F: Former good customer, not seen recently
|   |       |   +-- G: Frequent window shopper, mostly unproductive
|   |       |   +-- H: Other
|   |       +-- Positional time series in customer dimension
|   |       +-- Concatenated behavior tag string for wildcard searches
|   |       +-- Mini-dimension for contemporary behavior tag value
|   +-- Relationship Between Data Mining and DW/BI System
|   |   +-- Decision tree analysis on customer observations
|   |   +-- Seven-way drill across (census, demographic, credit, purchases, etc.)
|   |   +-- Answer sets written to files for neural networks / case-based reasoning
|   +-- Counts with Type 2 Dimension Changes
|       +-- COUNT DISTINCT on durable natural key
|       +-- Current Row Indicator for most up-to-date values
|       +-- Historical point-in-time counts via effective/expiration date constraints
|
+-- Outrigger for Low Cardinality Attribute Set
|   +-- Exception to the no-snowflake rule
|   +-- County Demographics Outrigger Dimension (Figure 8-6)
|   |   +-- Total Population, population by age bands (under 5, under 18, 65+)
|   |   +-- Female/Male Population and percentages
|   |   +-- Number of High School Graduates, College Graduates
|   |   +-- Number of Housing Units, Home Ownership Rate
|   +-- Justification: different grain, different update frequency, space savings
|   +-- WARNING: outriggers should be exception, not the rule
|
+-- Customer Hierarchy Considerations
|   +-- Commercial customer organizational hierarchies
|   +-- Fixed depth hierarchy (3 levels: corporate parent, business unit HQ, regional HQ)
|   +-- Slightly variable hierarchy (duplicate lower-level values upward)
|   +-- Ragged hierarchy of indeterminate depth
|       +-- Avoid generic Level-1, Level-2 naming
|
+-- Bridge Tables for Multivalued Dimensions
|   +-- Common multivalued dimension examples
|   |   +-- Demographic descriptors from multiple sources
|   |   +-- Contact addresses for commercial customers
|   |   +-- Professional skills, hobbies, diagnoses/symptoms
|   |   +-- Optional features, joint account holders, tenants
|   +-- Two design choices
|   |   +-- Positional design (named columns, scalable to ~100)
|   |   |   +-- Bitmapped indexes, easy BI tool integration
|   |   |   +-- Columnar databases well-suited
|   |   +-- Bridge table design (open-ended, scalable)
|   |       +-- Removes scalability/null value problems
|   |       +-- Requires complex SQL hidden from business users
|   +-- Bridge Table for Sparse Attributes (Figure 8-8)
|   |   +-- Loan Application Fact --> Application Disclosure Bridge --> Disclosure Item Dimension
|   |   +-- Name-value pair data (numeric, textual, file pointer, URL, recursive)
|   |   +-- Disclosure Item Dimension: Item Name, Item Value Type, Item Value Text String
|   +-- Bridge Table for Multiple Customer Contacts (Figure 8-9)
|       +-- Customer Dimension --> Contact Group Dimension --> Contact Group Bridge --> Contact Dimension
|       +-- Contact Group Bridge: Contact Group Key (FK), Contact Key (FK), Contact Role
|
+-- Complex Customer Behavior
|   +-- Behavior Study Groups for Cohorts
|   |   +-- Customer Behavior Study Group Dimension (Figure 8-10)
|   |   |   +-- Single column: Customer ID (Durable Key)
|   |   |   +-- Joined to Customer Dimension via durable key equijoin
|   |   +-- Impervious to type 2 changes (uses durable keys)
|   |   +-- Set operations: union, intersection, set difference
|   |   +-- Optional occurrence date column for panel studies
|   |   +-- Requires UI for capturing, creating, administering study groups
|   +-- Step Dimension for Sequential Behavior (Figure 8-11)
|   |   +-- Step Dimension (3 Roles): Step Key (PK), Total Number Steps, This Step Number, Steps Until End
|   |   +-- Pre-built for sessions up to 100 steps
|   |   +-- Three roles: overall session, successful purchase subsession, abandoned shopping cart
|   |   +-- Transaction Fact: Session Key (FK), Session Step Key (FK), Purchase Step Key (FK), Abandon Step Key (FK)
|   |   +-- Alternative: product code sequence in wide text column (wildcard search)
|   +-- Timespan Fact Tables (Figure 8-12)
|   |   +-- Customer Transaction Fact with twin date/time stamps
|   |   |   +-- Begin Effective Date/Time
|   |   |   +-- End Effective Date/Time (= begin of next transaction)
|   |   +-- Dimensions: Date, Demographics, Customer, Status
|   |   +-- Enables point-in-time status queries and duration calculations
|   |   +-- Back Room Administration: two-step process for maintaining date/time pairs
|   |   +-- Use far-future date instead of NULL for current end effective date/time
|   +-- Tagging Fact Tables with Satisfaction Indicators
|   |   +-- Satisfaction Dimension (positional design) (Figure 8-13)
|   |   |   +-- Delayed Arrival Indicator
|   |   |   +-- Diversion to Other Airport Indicator
|   |   |   +-- Lost Luggage Indicator
|   |   |   +-- Failure to Get Upgrade Indicator
|   |   |   +-- Middle Seat Indicator
|   |   |   +-- Personnel Problem Indicator
|   |   +-- Numeric satisfaction: product returns, support calls, social media metrics
|   +-- Tagging Fact Tables with Abnormal Scenario Indicators
|       +-- Standard scenario pipeline (order created, shipped, delivered, paid, returned)
|       +-- Delivery status dimension for unusual departures
|       +-- Companion transaction fact table (every step of the weird story)
|
+-- Customer Data Integration Approaches
|   +-- Master Data Management Creating a Single Customer Dimension
|   |   +-- "Best of breed" from multiple sources
|   |   +-- Enterprise MDM (centralized, feeds all operational apps + EDW)
|   |   +-- Downstream MDM (data warehouse builds MDM from operational extracts) (Figure 8-14)
|   |   +-- National Change of Address (NCOA) integration
|   |   +-- Customer matching: fuzzy logic, address parsing, postal code lookup
|   |   +-- Householding capabilities (linking by name/address)
|   +-- Partial Conformity of Multiple Customer Dimensions
|       +-- Lighter-weight conformed dimensions
|       +-- Shared specially administered conformed attributes (not full identity)
|       +-- Incremental approach: start with customer category, add geographic attributes
|       +-- Agile, incremental development
|
+-- Avoiding Fact-to-Fact Table Joins
|   +-- WARNING: simultaneous join of one dimension to two fact tables returns wrong answer
|   +-- Many-to-one-to-many cardinality mismatch (Figure 8-15)
|   |   +-- Customer Solicitation Fact <-- Customer Dimension --> Customer Response Fact
|   +-- Solution: drill-across technique (separate queries, outer join answer sets)
|   +-- Alternative: consolidated fact table combining data from multiple processes
|
+-- Low Latency Reality Check
    +-- Trade-offs: data quality degrades as latency decreases
    +-- Intraday: incomplete transaction sets, credit checks pending
    +-- Instantaneous: transaction fragments only, no data quality checks
    +-- Hybrid: intraday delivery + nightly batch correction
```

### chapter-9-human-resources-management-pp-263-279

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-9-human-resources-management-pp-263-279
Hash: a399ec1ae989

```
Human Resources Management
|
+-- Employee Profile Tracking
|   +-- Initial Draft Schema (Figure 9-1)
|   |   +-- Employee Transaction Fact (factless, 1 row per profile transaction)
|   |   |   +-- Transaction Date Key (FK)
|   |   |   +-- Transaction Date/Time
|   |   |   +-- Employee Key (FK)
|   |   |   +-- Employee Transaction Type Key (FK)
|   |   +-- Dimensions: Employee, Transaction Date, Employee Transaction Type
|   +-- Simplified Design: Embellished Employee Dimension (Figure 9-2)
|   |   +-- Employee Dimension absorbs the transaction event fact table
|   |   +-- Employee Key (PK), Employee ID (NK)
|   |   +-- Employee Name, Employee Address
|   |   +-- Job Grade, Salary, Education
|   |   +-- Original Hire Date (FK), Last Review Date (FK)
|   |   +-- Appraisal Rating
|   |   +-- Health Insurance Plan, Vacation Plan
|   |   +-- Change Reason Code, Change Reason Description
|   |   +-- Row Effective Date/Time, Row Expiration Date/Time
|   |   +-- Current Row Indicator
|   +-- Precise Effective and Expiration Timespans
|   |   +-- Date/time stamps (not just dates) for sub-daily precision
|   |   +-- Expiration set to "just before" new row's effective stamp
|   |   +-- Never modify earlier profile row's expiration date retroactively
|   |   +-- Current Row Indicator for fast retrieval of latest profile
|   +-- Dimension Change Reason Tracking
|   |   +-- ETL-centric metadata embedded with actual data
|   |   +-- Two-character abbreviation or legible description (e.g., "Last Name")
|   |   +-- Multiple concurrent changes: "|Last Name|ZIP|" text string or bridge table
|   |   +-- LIKE operator with wildcards for querying (WHERE ChangeReason LIKE '%ZIP%')
|   +-- Micro-transactions from source systems
|       +-- Encapsulate as "super transactions" (e.g., promotion = multiple attribute changes)
|       +-- Single type 2 row reflects all relevant changed attributes in one step
|
+-- Profile Changes as Type 2 Attributes or Fact Events
|   +-- Type 2 slowly changing dimension approach
|   |   +-- Associates accurate employee profile with each business process fact
|   |   +-- Can result in millions of rows for large organizations
|   +-- Separate fact tables for HR events (preferred for many events)
|   |   +-- Review events, benefit participation, professional development
|   |   +-- Each involves other dimensions (event date, organization, reviewer, approver)
|   |   +-- Factless fact tables: enable counting/trending by time and other dimensions
|   +-- Avoid overloading employee dimension
|       +-- Do not include lots of FK outriggers (reviewer, benefit, separation reason)
|       +-- These belong as dimensions on process-specific fact tables
|
+-- Headcount Periodic Snapshot
|   +-- Employee Headcount Snapshot Fact (Figure 9-3)
|   |   +-- Grain: 1 row per employee per month
|   |   +-- Dimensions: Month, Organization, Employee
|   |   +-- Facts (additive unless noted):
|   |       +-- Employee Count
|   |       +-- New Hire Count, Transfer Count, Promotion Count
|   |       +-- Salary Paid, Overtime Paid
|   |       +-- Retirement Fund Paid, Retirement Fund Employee Contribution
|   |       +-- Vacation Days Accrued, Vacation Days Taken
|   |       +-- Vacation Days Balance (SEMI-ADDITIVE -- average across months)
|   +-- Employee key corresponds to month-end profile row
|   +-- Organization dimension: description of org at close of relevant month
|
+-- Bus Matrix for HR Processes (Figure 9-4)
|   +-- Dimensions: Date, Position, Employee (or Empl Mgr), Organization, Benefit
|   +-- Hiring Processes
|   |   +-- Employee Position Snapshot (Periodic)
|   |   +-- Employee Requisition Pipeline (Accumulating)
|   |   +-- Employee Hiring (Transaction)
|   |   +-- Employee "On Board" Pipeline (Accumulating)
|   +-- Benefits Processes
|   |   +-- Employee Benefits Eligibility (Periodic)
|   |   +-- Employee Benefits Application (Accumulating)
|   |   +-- Employee Benefit Participation (Periodic)
|   +-- Employee Management Processes
|       +-- Employee Headcount Snapshot (Periodic)
|       +-- Employee Compensation (Transaction)
|       +-- Employee Benefit Accruals (Transaction)
|       +-- Employee Performance Review Pipeline (Accumulating)
|       +-- Employee Performance Review (Transaction)
|       +-- Employee Prof Dev Completed Courses (Transaction)
|       +-- Employee Disciplinary Action Pipeline (Accumulating)
|       +-- Employee Separations (Transaction)
|
+-- Packaged Analytic Solutions and Data Models
|   +-- Vendor-provided standard models / prebuilt data loaders
|   +-- Pros: rapid implementation, common process identification
|   +-- Cons:
|   |   +-- Party table abstractions vs. meaningful business labels
|   |   +-- Generic attribute column names
|   |   +-- Difficult to conform with internally available master data
|   |   +-- May not exhibit dimensional modeling best practices
|   +-- Recommendation: spend weeks with business users instead
|
+-- Recursive Employee Hierarchies
|   +-- Embedded Manager Attribute
|   |   +-- Manager name as flat attribute in employee dimension
|   +-- Dual Role-Playing Dimensions (Figure 9-5)
|   |   +-- Employee Dimension + Manager Dimension (role-play of same table)
|   |   +-- Manager Key (FK) in fact table joins to Manager Dimension
|   |   +-- Employee Separation Fact: Employee Key, Manager Key, Organization Key, Separation Profile Key
|   +-- Manager as Outrigger (Figure 9-6)
|   |   +-- Manager Key (FK) as attribute on Employee Dimension row
|   |   +-- Manager Key joins to Manager Dimension (role-play outrigger)
|   |   +-- Manager Dimension: Manager Key (PK), Manager Employee ID (NK), Manager Employee Attributes, Row Effective/Expiration Date, Current Row Indicator
|   +-- Change Tracking on Embedded Manager Key
|   |   +-- Type 2 on manager FK: new employee row per manager change
|   |   +-- Ripple effect risk: CEO profile change cascades to all employees
|   |   +-- Alternatives: type 1 (current only), or durable natural key (limited role-play)
|   +-- Drilling Up and Down Management Hierarchies
|   |   +-- Fixed depth: simple attribute or FK on employee dimension
|   |   +-- Variable depth recursive: OLAP parent/child structures
|   |   +-- Relational: CONNECT BY (Oracle) or CTE -- impractical for business users
|   +-- Management Hierarchy Bridge Table (Figure 9-7)
|       +-- Manager Dimension --> Management Hierarchy Bridge --> Employee Separation Fact
|       +-- Bridge columns: Manager Key (FK), Employee Key (FK), # Levels from Top, Bottom Flag, Top Flag
|       +-- One row per manager-employee pair (direct + indirect reports + self)
|       +-- Durable keys reduce ripple propagation vs. surrogate keys
|       +-- Optional effective/expiration dates on bridge rows for historical rollups
|       +-- Pathstring attribute as alternative (from Chapter 7)
|
+-- Multivalued Skill Keyword Attributes
|   +-- Positional Dimension Attributes
|   |   +-- Individual named columns (e.g., Linux: "Linux Skills" / "No Linux Skills")
|   |   +-- Works well for finite, stable set of skills
|   |   +-- Falls apart as number of skills expands
|   +-- Skill Keyword Bridge (Figure 9-8)
|   |   +-- Employee Dimension --> Employee Skill Group Bridge --> Skills Dimension
|   |   +-- Employee Skill Group Bridge: Employee Skill Group Key (FK), Employee Skill Key (FK)
|   |   +-- Skills Dimension: Employee Skill Key (PK), Employee Skill Description, Employee Skill Category
|   |   +-- Employee Skill Group Key (FK) embedded in Employee Dimension
|   |   +-- AND/OR Query Dilemma
|   |       +-- OR queries: simple constraint on skill description
|   |       +-- AND queries: require UNION/INTERSECTION of separate SELECTs
|   +-- Skill Keyword Text String (Figure 9-9)
|       +-- Delimited skills list string on Employee Dimension (e.g., "|Unix|C++|")
|       +-- UCase() for case-insensitive matching
|       +-- OR: UCase(skill_list) LIKE '%|UNIX|%' OR ... LIKE '%|LINUX|%'
|       +-- AND: UCase(skill_list) LIKE '%|UNIX|%' AND ... LIKE '%|LINUX|%'
|       +-- Works in any relational database, standard SQL
|       +-- Limitation: does not support count-by-skill-keyword queries
|
+-- Survey Questionnaire Data (Figure 9-10)
|   +-- Employee Evaluation Survey Fact
|   |   +-- Grain: 1 row per question per respondent's survey
|   |   +-- Survey Sent Date Key (FK), Survey Received Date Key (FK)
|   |   +-- Survey Key (FK)
|   |   +-- Responding Employee Key (FK), Reviewed Employee Key (FK) -- dual role-playing
|   |   +-- Question Key (FK), Response Category Key (FK)
|   |   +-- Survey Number (DD), Response
|   +-- Survey Dimension: Survey Title, Survey Type, Survey Objective, Review Year
|   +-- Question Dimension: Question Label, Question Category, Question Objective
|   +-- Response Category Dimension: Response Category Description (e.g., favorable, hostile)
|   +-- Date Dimension (2 views for roles: sent date, received date)
|   +-- Employee Dimension (2 views for roles: responding, reviewed)
|
+-- Text Comments
    +-- Not degenerate dimensions (too bulky for fact table)
    +-- Options:
    |   +-- Separate comments dimension (FK in fact table)
    |   +-- Attribute on transaction-grained dimension table
    +-- If cardinality < number of transactions --> comments dimension
    +-- If unique per event --> transaction dimension attribute
    +-- Query performance: heavy dimension joined only after significant filtering
```

### chapter-10-financial-services-pp-281-296

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-10-financial-services-pp-281-296
Hash: a20424a8bab9

```
Financial Services (Retail Banking Focus)
|
+-- Banking Case Study and Bus Matrix (Figure 10-1)
|   +-- Dimensions: Date, Prospect, Customer, Account, Product, Household, Branch
|   +-- Business Processes
|       +-- New Business Solicitation (Date, Prospect, Product)
|       +-- Lead Tracking (Date, Prospect, Product, Branch)
|       +-- Account Application Pipeline (Date, Prospect, Customer, Account, Product, Branch)
|       +-- Account Initiation (Date, Prospect, Customer, Account, Product, Household, Branch)
|       +-- Account Transactions (Date, Customer, Account, Product, Household, Branch)
|       +-- Account Monthly Snapshot (Date, Customer, Account, Product, Household, Branch)
|       +-- Account Servicing Activities (Date, Customer, Account, Product, Household, Branch)
|
+-- Dimension Triage to Avoid Too Few Dimensions
|   +-- Anti-pattern: "Too few dimensions" (Figure 10-2)
|   |   +-- Month Dimension + Account Dimension only
|   |   +-- Account Dimension bloated with: Account, Customer, Product, Household, Branch, Status attributes
|   +-- Recommended dimension supplements to consider:
|   |   +-- Causal dimensions (promotion, contract, deal, store condition, weather)
|   |   +-- Multiple date dimensions (for accumulating snapshots)
|   |   +-- Degenerate dimensions (order number, invoice, ticket)
|   |   +-- Role-playing dimensions (multiple business entities per transaction)
|   |   +-- Status dimensions (account status at month end)
|   |   +-- Audit dimension (data lineage and quality)
|   |   +-- Junk dimensions (correlated indicators and flags)
|   +-- Rule of thumb: 5-20 dimensions per fact table
|   +-- Supertype Snapshot Fact Table (Figure 10-3)
|       +-- Monthly Account Snapshot Fact
|       |   +-- Month End Date Key (FK), Branch Key (FK), Account Key (FK)
|       |   +-- Primary Customer Key (FK), Product Key (FK)
|       |   +-- Account Status Key (FK), Household Key (FK)
|       |   +-- Primary Month Ending Balance (semi-additive)
|       |   +-- Average Daily Balance (semi-additive)
|       |   +-- Number of Transactions, Interest Paid, Fees Charged
|       +-- Dimensions:
|           +-- Month Dimension: Month End Date Key (PK), Month Attributes
|           +-- Account Dimension: Account Key (PK), Account Number (NK), Address Attributes, Account Open Date
|           +-- Branch Dimension: Branch Key (PK), Branch Number (NK), Address Attributes, Rollup Attributes
|           +-- Product Dimension: Product Key (PK), Product Code (NK), Product Description
|           +-- Account Status Dimension: Account Status Key (PK), Account Status Description, Account Status Group
|           +-- Primary Customer Dimension: Primary Customer Key (PK), Name, Date of Birth
|           +-- Household Dimension: Household Key (PK), Household ID (NK), Address, Income, Homeownership Indicator, Presence of Children
|
+-- Household Dimension
|   +-- Economic unit comprising multiple accounts and account holders
|   +-- Demographic attributes: income, homeownership, retiree status, children
|   +-- Householding process: business rules + algorithms + specialized products/services
|   +-- Volatile: changes with marital status and life stage
|   +-- Separate dimension from Account (different grain, different volatility)
|   +-- Relationship captured in fact table FK (not embedded in account dimension)
|       to avoid type 2 explosion on 10-million-row account dimension
|
+-- Multivalued Dimensions and Weighting Factors
|   +-- Account-to-Customer Bridge Table (Figure 10-4)
|   |   +-- Account-to-Customer Bridge: Account Key (FK), Customer Key (FK), Weighting Factor
|   |   +-- Weighting factors sum to 1.00 per account
|   |   +-- Allocates additive facts across individual account holders
|   |   +-- Correctly weighted report vs. impact report (no weighting, with overcounting caveat)
|   +-- SQL view combining fact table + bridge table
|   |   +-- Two views: one with weighting factors, one without
|   +-- Time-stamped bridge rows for time-variant relationships
|   +-- Credit card scenario: account + customer both as FK in transaction fact (no bridge needed)
|       +-- Bridge still needed for account-level metrics (e.g., billing data)
|
+-- Mini-Dimensions Revisited (Figure 10-5)
|   +-- Problem: rapidly changing demographics/status on large customer dimension
|   +-- Solution: type 4 mini-dimensions broken off from main dimension
|   +-- Customer Dimension: relatively constant attributes
|   +-- Customer Demographics Dimension (mini-dimension)
|   |   +-- Customer Demographics Key (PK)
|   |   +-- Customer Age Band, Customer Income Band, Customer Marital Status
|   +-- Customer Risk Profile Dimension (mini-dimension)
|   |   +-- Customer Risk Profile Key (PK)
|   |   +-- Customer Risk Cluster, Customer Delinquency Cluster
|   +-- Mini-dimension design rules:
|   |   +-- Correlated clumps of attributes (not one attribute per mini-dimension)
|   |   +-- Band attribute values to maintain reasonable row counts
|   |   +-- May also store discrete numeric values as facts for data mining
|   |   +-- Current profitability range: type 1 overwrite in main dimension
|   +-- Adding a Mini-Dimension to a Bridge Table (Figure 10-6)
|       +-- Account-to-Customer Bridge: Account Key (FK), Customer Key (FK), Demographics Key (FK)
|       +-- Bridge key = (Account Key, Customer Key, Demographics Key)
|       +-- Demographics Dimension: Demographics Key (PK), Age Band, Income Band, Marital Status
|       +-- Bridge table growth limited to month-end changes (matching fact table grain)
|
+-- Dynamic Value Banding of Facts
|   +-- Problem: SQL has no GROUP BY for arbitrary value ranges
|   +-- Report example: balance ranges with unequal sizes and textual names (Figure 10-7)
|   +-- Band Definition Table (Figure 10-8)
|   |   +-- Band Group Key (PK), Band Group Sort Order (PK)
|   |   +-- Band Group Name, Band Range Name
|   |   +-- Band Lower Value, Band Upper Value
|   |   +-- Joined to fact using >= and < (non-equijoin)
|   +-- Multiple band group definitions in single table
|   +-- Performance considerations: may need index on balance fact column
|   +-- Columnar DBMSs: efficient sort and compress of fact-like balance values
|
+-- Supertype and Subtype Schemas for Heterogeneous Products
|   +-- The Dilemma
|   |   +-- Each product type has unique facts and attributes
|   |   +-- Checking: minimum balances, overdraft limits, ATM transactions, online transactions
|   |   +-- Time deposits: maturity dates, compounding frequencies, current interest rate
|   |   +-- Cannot put all product-specific facts in one supertype table (Swiss cheese)
|   +-- Two Business Perspectives
|   |   +-- Global view: single supertype fact table, common facts only, cross-product analysis
|   |   +-- Line-of-business view: subtype fact table with product-specific facts and attributes
|   +-- Subtype Schema Example: Checking (Figure 10-9)
|   |   +-- Checking Account Fact (subtype)
|   |   |   +-- Month Key (FK), Account Key (FK), Primary Customer Key (FK)
|   |   |   +-- Branch Key (FK), Household Key (FK), Product Key (FK)
|   |   |   +-- Balance, Change in Balance
|   |   |   +-- Total Deposits, Total Withdrawals
|   |   |   +-- Number Transactions, Max Backup Reserve
|   |   |   +-- Number Overdraws, Total Overdraw Penalties
|   |   |   +-- Count Local ATM Transactions, Count Foreign ATM Transactions
|   |   |   +-- Count Online Transactions, Days Below Minimum
|   |   |   +-- + 10 more facts
|   |   +-- Checking Account Dimension (subtype)
|   |   |   +-- Account Key (PK), Account Number (NK), Address Attributes, Account Open Date
|   |   +-- Checking Product Dimension (subtype)
|   |       +-- Product Key (PK), Product Code (NK), Product Description
|   |       +-- Premium Flag, Checking Type, Interest Payment Type, Overdraft Policy
|   |       +-- + 12 more attributes
|   +-- Subtype keys = same surrogate keys as supertype (shared key space)
|   +-- Subtype dimension = shrunken conformed dimension (subset of supertype rows)
|   +-- Subtype fact includes all supertype facts + product-specific facts (no join needed)
|   +-- Supertype and Subtype Products with Common Facts
|   |   +-- When facts do not vary by line of business: single supertype fact table suffices
|   |   +-- Still use subtype account/product dimension tables for product-specific attributes
|   +-- Applicability: any business with heterogeneous products (technology: HW, SW, services)
|
+-- Hot Swappable Dimensions
    +-- Scenario: brokerage house, multiple clients, same stock price fact table
    +-- Each client has confidential/customized stock dimension attributes
    +-- Separate copy of stock dimension per client
    +-- Joined to single fact table at query time
    +-- Implementation: disable referential integrity constraints, switch dimension per query
```

### cross-chapter-concept-index

URL: https://local.taxonomy/kimball-dw-toolkit/cross-chapter-concept-index
Hash: 889a131efc3d

```
| Concept | Ch 8 | Ch 9 | Ch 10 |
|---------|------|------|-------|
| Bridge tables (multivalued dimensions) | Sparse attributes, customer contacts | Skill keyword bridge, management hierarchy | Account-to-customer with weighting factors |
| Mini-dimensions | Behavior tags, demographics | -- | Customer demographics, risk profile; mini-dim on bridge table |
| Outrigger dimensions | Date outrigger, county demographics | Manager role-play outrigger | -- |
| Type 2 slowly changing dimensions | Customer dimension with effective/expiration dates | Employee dimension with precise date/time stamps | Account dimension (caution: explosion risk) |
| Recursive / ragged hierarchies | Commercial customer org hierarchies | Employee-manager hierarchies (bridge table) | -- |
| Role-playing dimensions | Date dimension views (first purchase, etc.) | Employee/Manager, Responding/Reviewed Employee | Multiple date roles, primary customer |
| Supertype / subtype schemas | -- | -- | Supertype fact (all accounts) + subtype fact/dim per product line |
| Behavior study groups / cohorts | Study group dimension (durable key table) | -- | -- |
| Positional design vs. bridge | Trade-offs for sparse attributes | Skill keywords: positional vs. bridge vs. text string | -- |
| Fact table types | Timespan facts, satisfaction/abnormal tagging | Factless (profile events), periodic snapshot (headcount) | Periodic snapshot (monthly account), accumulating (pipeline) |
| Weighting factors on bridge | -- | -- | Account-to-customer bridge, sum to 1.00 |
| Dynamic value banding | -- | -- | Band definition table joined via non-equijoin |
| Hot swappable dimensions | -- | -- | Per-client dimension copies, disabled RI constraints |
| Conformed dimensions | Partial conformity of multiple customer dims | Conformed employee dimension across HR processes | Conformed account/product dims across supertype/subtype |
| Master data management | Enterprise MDM vs. Downstream MDM | -- | Householding as MDM variant |
| Survey / questionnaire schema | -- | Survey fact with role-playing employee + question + response dims | -- |
| Text comments handling | -- | Separate dimension or transaction-dim attribute | -- |
| Packaged solutions critique | -- | Party table abstractions, generic column names | -- |


# Kimball Data Warehouse Toolkit 3e -- Chapters 11-14 Taxonomy

Source: *The Data Warehouse Toolkit, 3rd Edition* by Ralph Kimball and Margy Ross

---
```

### chapter-11-telecommunications-pp-297-310

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-11-telecommunications-pp-297-310
Hash: 096672c1849c

```
### 11.1 Case Study and Bus Matrix
- **Industry**: Wireless telecommunications company
- **Focus**: Customer billing process (first warehouse iteration)
- **Bus Matrix Rows (Business Processes)**
  - Purchasing
  - Internal Inventory
  - Channel Inventory
  - Service Activation
  - Product Sales
  - Promotion Participation
  - Call Detail Traffic
  - Customer Billing
  - Customer Support Calls
  - Repair Work Orders
- **Bus Matrix Columns (Conformed Dimensions)**
  - Date
  - Product
  - Customer
  - Rate Plan
  - Sales Organization
  - Service Line #
  - Switch
  - Employee
  - Support Call Profile

### 11.2 Draft Schema (Pre-Review) -- Figure 11-2
- **Billing Fact** (grain: one row per bill per month -- flawed)
  - Bill # (FK)
  - Customer ID (FK)
  - Sales Org Number (FK)
  - Sales Channel ID (FK)
  - Rate Plan Code (FK)
  - Rate Plan Type Code (textual fact -- flaw)
  - Call Count
  - Total Minute Count
  - Night-Weekend Minute Count
  - Roam Minute Count
  - Message Count
  - Data MB Used
  - Month Service Charge
  - Prior Month Service Charge
  - Year-to-Date Service Charge (non-additive aggregate -- flaw)
  - Message Charge
  - Data Charge
  - Roaming Charge
  - Taxes
  - Regulatory Charges
- **Customer Dimension**: Customer ID (PK and NK), Name, Address, City, State, Zip, Orig Authorization Credit Score
- **Bill Dimension**: Bill #, Service Line Number, Bill Date
- **Service Line Dimension**: Service Line Number (PK), Area Code, Activation Date
- **Rate Plan Dimension**: Rate Plan Code (PK and NK), Abbreviation, Plan Minutes Allowed, Plan Messages Allowed, Plan Data MB Allowed, Night-Weekend Minute Ind
- **Sales Org Dimension**: Sales Org Number (PK and NK), Sales Channel ID
- **Sales Channel Dimension**: Sales Channel ID (PK and NK), Sales Channel Name (snowflake -- flaw)

### 11.3 General Design Review Considerations (Checklist of Common Mistakes)
1. **Balance Business Requirements and Source Realities**
   - Models must blend business needs with source system data realities
   - Requirements-only models include unsourceable elements
   - Source-only models omit business-critical analytics
2. **Focus on Business Processes**
   - Design models around business process events, not specific reports
   - Process-centric models are more resilient to change
   - Complementary schemas: summary aggregations, accumulating snapshots, consolidated fact tables, subset fact tables
3. **Granularity**
   - First question: "What is the grain of the fact table?"
   - Build at lowest level of granularity possible
   - Implement most granular data for the business process, not just the enterprise
4. **Single Granularity for Facts**
   - All additive facts must be consistent with the grain declaration
   - Avoid aggregated facts (e.g., year-to-date totals) -- they are not perfectly additive
   - Prohibit text fields, cryptic indicators, and flags from the fact table
   - Move textual values to dimension tables with descriptive rollup attributes
5. **Dimension Granularity and Hierarchies**
   - Each dimension attribute should take on a single value per dimension row
   - Collapse/denormalize hierarchies within a single dimension
   - Avoid "centipede" fact tables with 20+ foreign keys -- combine or collapse dimensions
   - Avoid snowflaking hierarchical relationships into separate dimension tables
   - Outriggers are permissible but should be the exception
   - Avoid mixing atomic and summary rows in the same dimension table (telltale "level" attribute)
6. **Date Dimension**
   - Every fact table needs at least one explicit date dimension
   - Avoid generic unnamed date dimensions
   - **Anti-pattern: Fixed Time Series Buckets** -- repeating monthly metric columns on a single row is inflexible, loses date dimension filtering, creates nulls
7. **Degenerate Dimensions**
   - Transaction numbers (invoice, order) belong as degenerate dimensions in the fact table, not as separate dimension tables
   - Warning sign: dimension table with nearly as many rows as the fact table
8. **Surrogate Keys**
   - Use surrogate keys for all dimension table primary keys (except date dimension)
   - Reference surrogate keys as fact table foreign keys
9. **Dimension Decodes and Descriptions**
   - All identifiers and codes must be accompanied by descriptive decodes
   - Store decodes as data elements in the database, not in BI tool semantic layers
10. **Conformity Commitment**
    - Shared conformed dimensions across process-centric models are critical
    - Conformed dimensions ensure consistency and integration across the organization

### 11.4 Design Review Guidelines
- **Preparation**
  - Invite the right players (modelers, BI developers, business-knowledgeable people)
  - Designate a facilitator
  - Agree on scope in advance
  - Block time on calendars (focused two-day effort)
  - Reserve the right space (large white board)
  - Assign homework (top 5 concerns/improvements)
- **During Review**
  - Check attitudes at the door
  - Ban technology unless needed
  - Exhibit strong facilitation skills
  - Ensure common understanding of the current model
  - Designate a scribe
  - Start with the big picture (bus matrix, granularity, then dimensions)
  - Remind everyone business acceptance is critical
  - Sketch out sample rows with data values
  - Close with a recap (assignments, due dates, follow-up)
- **After Review**
  - Assign responsibility for remaining open issues
  - Evaluate cost/benefit for improvements
  - Anticipate future reviews (every 12-24 months)

### 11.5 Draft Design Exercise Discussion (Post-Review Fixes)
- **Grain correction**: one row per service line per bill (not per bill)
- **Bill dimension eliminated**: bill number becomes degenerate dimension (DD); bill date moves to a proper date dimension FK
- **Sales channel snowflake collapsed**: sales channel attributes folded into Sales Organization Dimension
- **Rate plan type code**: moved from textual fact to rollup attribute in Rate Plan Dimension
- **Customer, sales org, rate plan as mini-dimensions**: kept as separate entities (not collapsed into service line) due to service line dimension size
- **Surrogate keys**: implemented consistently across all dimension PKs
- **Descriptive names**: operational codes replaced with descriptive names
- **Year-to-date metric removed**: users calculate YTD via date dimension constraints

### 11.6 Revised Schema (Post-Review) -- Figure 11-3
- **Billing Fact** (grain: one row per service line per bill per month)
  - Bill Date Key (FK)
  - Customer Key (FK)
  - Service Line Key (FK)
  - Sales Organization Key (FK)
  - Rate Plan Key (FK)
  - Bill Number (DD -- degenerate dimension)
  - Call Count
  - Total Minute Count
  - Night-Weekend Minute Count
  - Roam Minute Count
  - Message Count
  - Data MB Used
  - Month Service Charge
  - Message Charge
  - Data Charge
  - Roaming Charge
  - Taxes
  - Regulatory Charges
- **Bill Date Dimension**: standard date dimension
- **Customer Dimension**: Customer Key (PK), Customer ID (NK), Name, Address, City, State, Zip, Orig Authorization Credit Score
- **Service Line Dimension**: Service Line Key (PK), Service Line Number (NK), Area Code, Activation Date
- **Sales Organization Dimension**: Sales Organization Key (PK), Sales Organization Number, Sales Organization Name, Sales Channel ID, Sales Channel Name
- **Rate Plan Dimension**: Rate Plan Key (PK), Rate Plan Code, Rate Plan Name, Rate Plan Abbreviation, Rate Plan Type Code, Rate Plan Type Description, Plan Minutes Allowed, Plan Messages Allowed, Plan Data MB Allowed, Night-Weekend Minute Ind

### 11.7 Remodeling Existing Data Structures
- Adding a new type 1 attribute is nearly pain-free
- Adding a new type 2 attribute requires backfilling historical rows and recasting fact rows
- Converting to conformed dimensions requires reprocessing fact table rows
- Use views to buffer BI applications from physical data structure changes
- Evaluate cost/benefit: sometimes decommission and rebuild from scratch
- Best time to remodel: source system conversion or BI tool migration

### 11.8 Geographic Location Dimension
- Telecom and utilities have strong notion of physical location
- Location attributes: street, city, state, ZIP code, latitude, longitude
- Latitude/longitude enable geospatial analysis and map-centric visualization
- **Anti-pattern: Single master location dimension** as outrigger to all entities
  - Consolidating all addresses into one dimension hurts performance
  - Geographic info naturally handled as attributes within multiple dimensions
  - Typically little overlap between geographic locations across different dimensions
- **Anti-pattern: Generalized abstract location dimension** in presentation area
  - Abstract dimensions negatively impact ease-of-use and query performance
  - Acceptable behind the scenes in the ETL back room

---
```

### chapter-12-transportation-pp-311-324

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-12-transportation-pp-311-324
Hash: b81a8216675c

```
### 12.1 Airline Case Study and Bus Matrix
- **Industry**: Airline / travel / shipping
- **Applicability**: Airlines, cargo shippers, package delivery, car rental, hotel chains, telecommunications network routing
- **Bus Matrix Rows (Business Processes)** -- Figure 12-1
  - Reservations (DD: Conf #)
  - Issued Tickets (DD: Conf #, Ticket #)
  - Unearned Revenue & Availability
  - Flight Activity (DD: Conf #, Ticket #)
  - Frequent Flyer Account Credits (DD: Conf #, Ticket #)
  - Customer Care Interactions (DD: Case #, Ticket #)
  - Frequent Flyer Communications
  - Maintenance Work Orders (DD: Work Order #)
  - Crew Scheduling
- **Bus Matrix Columns (Conformed Dimensions)**
  - Date
  - Time
  - Airport
  - Passenger
  - Booking Channel
  - Class of Service
  - Fare Basis
  - Aircraft
  - Communication Profile
  - Transaction ID #

### 12.2 Multiple Fact Table Granularities
- **Leg level**: most granular; aircraft takeoff to landing with no intermediate stops
  - Metrics: number of seats, load factors, flight duration, minutes late at departure/arrival
  - On-time arrival dimension possible
- **Segment level**: single flight number flown by single aircraft (one or more legs)
  - Represents line item on ticket coupon
  - Passenger revenue and mileage credit determined here
  - Chosen as initial grain (boarding pass collected from passengers)
- **Trip level**: origin-to-destination (may span multiple segments with aircraft changes)
  - Determined by stops of more than 4 hours (stopover definition)
  - Trip origin and trip destination as role-playing airport dimensions
  - Caution: some segment-level dimensions (fare basis, class of service) don't apply at trip level
- **Itinerary level**: entire airline ticket or reservation confirmation number

### 12.3 Segment-Level Flight Activity Schema -- Figure 12-2
- **Segment-Level Flight Activity Fact**
  - Scheduled Departure Date Key (FK) -- Date Dimension (views for 2 roles)
  - Scheduled Departure Time Key (FK) -- Time-of-Day Dimension (views for 2 roles)
  - Actual Departure Date Key (FK)
  - Actual Departure Time Key (FK)
  - Passenger Key (FK) -- Passenger Dimension
  - Passenger Profile Key (FK) -- Passenger Profile Dimension (mini-dimension)
  - Segment Origin Airport Key (FK) -- Airport Dimension (views for 2 roles)
  - Segment Destination Airport Key (FK)
  - Aircraft Key (FK) -- Aircraft Dimension
  - Class of Service Flown Key (FK) -- Class of Service Flown Dimension
  - Fare Basis Key (FK) -- Fare Basis Dimension
  - Booking Channel Key (FK) -- Booking Channel Dimension
  - Confirmation Number (DD)
  - Ticket Number (DD)
  - Segment Sequence Number (DD)
  - Flight Number (DD)
  - Base Fare Revenue
  - Passenger Facility Charges
  - Airport Tax
  - Government Tax
  - Baggage Charges
  - Upgrade Fees
  - Transaction Fees
  - Segment Miles Flown
  - Segment Miles Earned
- **Role-Playing Dimensions**
  - Date Dimension: Scheduled Departure Date, Actual Departure Date (2 views)
  - Time-of-Day Dimension: Scheduled Departure Time, Actual Departure Time (2 views)
  - Airport Dimension: Segment Origin Airport, Segment Destination Airport (2 views)

### 12.4 Passenger Mini-Dimension (Type 4) -- Figure 12-3
- **Passenger Profile Dimension** (mini-dimension, separate from main Passenger Dimension)
  - Passenger Profile Key (PK)
  - Frequent Flyer Tier (Basic, MidTier, WarriorTier)
  - Home Airport (ATL, BOS, etc.)
  - Club Membership Status (Non-Member, Club Member)
  - Lifetime Mileage Tier (Under 100,000 miles ... 2,000,000-2,999,999 miles)
- Chosen over SCD type 2 due to millions of passenger dimension rows
- Each unique combination of tier/airport/club/mileage = one row
- Marketing analysts frequently use this mini-dimension independently

### 12.5 Linking Segments into Trips
- Segment grain masks true trip origin/destination
- Solution: add two more role-playing airport dimensions (Trip Origin, Trip Destination)
- Determined during ETL by looking at stops > 4 hours
- Exercise caution summarizing by trip (some dimensions like fare basis don't apply)
- Optional aggregate fact table at trip level with trip total metrics and segment count

### 12.6 Related Fact Tables
- **Leg-level flight activity fact table**: actual/blocked flight durations, departure/arrival delays, fuel weights
- **Reservations fact table**: booking activity
- **Issued tickets fact table**: ticketing activity
- **Revenue and availability snapshot**: cumulative unearned revenue and remaining availability per class of service for 90 days prior to departure
  - "Days prior to departure" dimension for milestone comparisons (e.g., 60 days out)

### 12.7 Extensions to Other Industries

#### 12.7.1 Cargo Shipper -- Figure 12-4
- **Shipping Transport Fact** (grain: container on a particular leg of its trip)
  - Voyage Departure Date Key (FK) -- Date Dimension (views for 2 roles)
  - Leg Departure Date Key (FK)
  - Voyage Origin Port Key (FK) -- Port Dimension (views for 4 roles)
  - Voyage Destination Port Key (FK)
  - Leg Origin Port Key (FK)
  - Leg Destination Port Key (FK)
  - Ship Mode Key (FK) -- Ship Mode Dimension
  - Container Key (FK) -- Container Dimension (size, electrical power, refrigeration)
  - Commodity Key (FK) -- Commodity Dimension (harmonized commodity codes)
  - Consignor Key (FK) -- Business Entity Dimension (views for 7 roles)
  - Foreign Transporter Key (FK)
  - Foreign Consolidator Key (FK)
  - Shipper Key (FK)
  - Domestic Consolidator Key (FK)
  - Domestic Transporter Key (FK)
  - Consignee Key (FK)
  - Bill-of-Lading Number (DD)
  - Leg Fee
  - Leg Tariffs
  - Leg Miles

#### 12.7.2 Travel Services Hotel Stay -- Figure 12-5
- **Travel Services Hotel Stay Fact** (grain: entire hotel stay)
  - Reservation Date Key (FK) -- Date Dimension (views for 3 roles)
  - Arrival Date Key (FK)
  - Departure Date Key (FK)
  - Customer Key (FK) -- Customer Dimension
  - Hotel Property Key (FK) -- Hotel Property Dimension
  - Sales Channel Key (FK) -- Sales Channel Dimension
  - Confirmation Number (DD)
  - Ticket Number (DD)
  - Number of Nights
  - Extended Room Charge
  - Tax Charge

### 12.8 Combining Correlated Dimensions

#### 12.8.1 Class of Service (Combined Dimension) -- Figure 12-6
- Combines Class Purchased and Class Flown into one dimension
- Adds Class Change Indicator (Upgrade, Downgrade, No Class Change)
- Adds Purchased-Flown Group concatenation (e.g., "Economy-Business")
- Cartesian product: 4 x 4 = 16 rows (small enough to combine)
- Acts as a type of junk dimension
- Other airline fact tables (inventory, ticket purchases) reference conformed 4-row class dimension

#### 12.8.2 Origin and Destination
- Separate role-playing airport dimensions preferred when data volumes are significant
- Additional attributes depend on the combination (distance, route type)
- **City-Pair Route Dimension** -- Figure 12-7
  - City-Pair Route Key (PK)
  - Directional Route Name (e.g., BOS-JFK)
  - Non-Directional Route Name (e.g., BOS-JFK)
  - Route Distance in Miles
  - Route Distance Band
  - Dom-Intl Ind (Domestic / International)
  - Transoceanic Ind (Non-Oceanic / Transatlantic / Transpacific)
- Two options: add route dimension to fact table, or combine origin+destination+route into single dimension
- Bridge table NOT recommended here -- relationship can be represented in the fact table directly

### 12.9 More Date and Time Considerations

#### 12.9.1 Country-Specific Calendars as Outriggers -- Figure 12-8
- Primary date dimension: generic calendar attributes (Gregorian, Hebrew, Islamic, Chinese if multinational)
- **Country-Specific Date Outrigger** supplements primary date table
  - Composite key: Date Key (FK) + Country Key (FK)
  - Country Name
  - Civil Holiday Flag / Name
  - Religious Holiday Flag / Name
  - Weekday Indicator
  - Season Name
- Can join to main calendar as outrigger or directly to fact table
- Similar to handling multiple fiscal accounting calendars (Chapter 7)

#### 12.9.2 Date and Time in Multiple Time Zones -- Figure 12-9
- Capture both local time and a standard time (GMT/UTC/Zulu time)
- UTC offset cannot reside in a time or airport dimension (depends on both location AND date)
- **Recommended approach**: separate date and time-of-day dimension pairs for local and equivalized dates
  - Departure Date Key (FK) + GMT Departure Date Key (FK)
  - Departure Time-of-Day Key (FK) + GMT Departure Time-of-Day Key (FK)
- Time-of-day dimensions support time period groupings (shift numbers, rush period, time block designations)
- More than 24 time zones globally (India +5.5h, Nepal +5.75h, Australia has 3 zones, daylight saving complications)

### 12.10 Localization Recap
- Multi-currency reporting (Chapter 6)
- Multi-language support (Chapter 8)
- International time zones and calendars
- UI text translation in BI tools
- Text expansion issues (English to European languages)
- Right-to-left languages (Arabic)
- Standard: aviation uses English and feet globally

---
```

### chapter-13-education-pp-325-337

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-13-education-pp-325-337
Hash: 7becb4e98d3f

```
### 13.1 University Case Study and Bus Matrix
- **Industry**: Higher education (university, college)
- Universities operate like small villages: real estate, restaurants, retail, events, police, fundraising, financial services, investment, job placement, construction, medical services
- **Bus Matrix (Figure 13-1) -- Conformed Dimensions**
  - Date/Term
  - Applicant-Student-Alum
  - Employee (Faculty, Staff)
  - Course
  - Department
  - Facility
  - Account

#### Student Lifecycle Processes
| Process | Date/Term | Applicant-Student-Alum | Employee | Course | Department | Facility | Account |
|---|---|---|---|---|---|---|---|
| Admission Events | X | X | X | | | | |
| Applicant Pipeline | X | X | X | | X | | |
| Financial Aid Awards | X | X | X | | X | | |
| Student Enrollment/Profile Snapshot | X | X | X | | X | X | |
| Student Residential Housing | X | X | | | X | X | |
| Student Course Registration & Outcomes | X | X | X | X | X | X | |
| Student Course Instructor Evaluations | X | X | X | X | X | X | |
| Student Activities | X | X | | | X | | |
| Career Placement Activities | X | X | | | X | | |
| Advancement Contacts | X | X | X | | | | |
| Advancement Pledges & Gifts | X | X | X | | | | X |

#### Financial Processes
| Process | Date/Term | Employee | Department | Account |
|---|---|---|---|---|
| Budgeting | X | | X | X |
| Endowment Tracking | X | | X | X |
| GL Transactions | X | | X | X |
| Payroll | X | X | X | X |
| Procurement | X | X | X | X |

#### Employee Management Processes
| Process | Date/Term | Employee | Department | Facility |
|---|---|---|---|---|
| Employee Headcount Snapshot | X | | X | X |
| Employee Hiring & Separations | X | X | X | |
| Employee Benefits & Compensation | X | X | X | |
| Staff Performance Management | X | X | X | |
| Faculty Appointment Management | X | X | X | |
| Research Proposal Pipeline | X | X | X | |
| Research Expenditures | X | X | X | X |
| Faculty Publications | X | X | X | |

#### Administrative Processes
| Process | Date/Term | Department | Facility |
|---|---|---|---|
| Facilities Utilization | X | X | X |
| Energy Consumption & Waste Management | X | X | X |
| Work Orders | X (+ Employee, Account) | X | X |

### 13.2 Accumulating Snapshot Fact Tables
- **Characteristics**
  - Single row represents complete history of a workflow/pipeline instance
  - Multiple dates represent standard pipeline milestone events
  - Facts include metrics for each milestone, status counts, elapsed durations
  - Rows are revisited and updated (destructive updates) whenever the pipeline instance changes
  - Both foreign keys and measured facts may be changed during updates

#### 13.2.1 Applicant Pipeline -- Figure 13-2
- **Applicant Pipeline Fact** (grain: one row per prospective student)
  - **Milestone Date Keys (6 role-playing date dimensions)**
    - Initial Inquiry Date Key (FK)
    - Campus Visit Date Key (FK)
    - Application Submitted Date Key (FK)
    - Application File Completed Date Key (FK)
    - Admission Decision Notification Date Key (FK)
    - Applicant Enroll/Withdraw Date Key (FK)
  - Applicant Key (FK)
  - Application Status Key (FK)
  - Application ID (DD)
  - **Status Count Facts**
    - Inquiry Count
    - Campus Visit Count
    - Application Submitted Count
    - Application Completed Count
    - Admit Early Decision Count
    - Admit Regular Decision Count
    - Waitlist Count
    - Defer to Regular Decision Count
    - Deny Count
    - Enroll Early Decision Count
    - Enroll Regular Decision Count
    - Admit Withdraw Count
- **Date Dimension** (views for 6 roles)
  - Date Key (PK), Term, Academic Year-Term, Academic Year
  - Default surrogate key for unknown/TBD dates (new/in-process rows)
- **Applicant Dimension**
  - Applicant Key (PK), Name, Address Attributes, High School, High School GPA, High School Type, SAT Math/Verbal/Writing Score, ACT Composite Score, Number of AP Credits, Gender, Date of Birth, Ethnicity, Full-time/Part-time Indicator, Application Source, Intended Major, ...
- **Application Status Dimension**
  - Application Status Key, Application Status Code, Application Status Description, Application Status Category

#### 13.2.2 Alternative Applicant Pipeline Schemas
- Retain snapshots at critical points in the admissions calendar (e.g., early decision notification date)
- Admission transaction fact table: one row per applicant per transaction for counting and period-to-period comparisons

#### 13.2.3 Research Grant Proposal Pipeline
- Another accumulating snapshot example
- Track lifecycle: preliminary proposal to grant approval to award receipt
- Analysis: outstanding proposals by faculty, department, topic area, funding source
- Success rates by various attributes

### 13.3 Factless Fact Tables
- Fact tables with NO measured numeric facts
- Contain only a series of dimension foreign keys
- Record the collision of dimensions at a point in time/space
- Two types: **event tracking** and **coverage**

#### 13.3.1 Admissions Events (Event Tracking) -- Figure 13-3
- **Admissions Event Attendance Fact** (factless)
  - Admissions Event Date Key (FK) -- Admissions Event Date Dimension
  - Planned Enroll Term Key (FK) -- Planned Enroll Term Dimension
  - Applicant Key (FK) -- Applicant Dimension
  - Applicant Status Key (FK) -- Application Status Dimension
  - Admissions Officer Key (FK) -- Admissions Officer Dimension
  - Admission Event Key (FK) -- Admission Event Dimension
  - Admissions Event Attendance Count (=1) -- artificial count metric
- Events tracked: high school visit, college fair, alumni interview, campus overnight

#### 13.3.2 Course Registrations (Event Tracking) -- Figure 13-4
- **Course Registration Event Fact** (factless)
  - Term Key (FK) -- Term Dimension (Term, Academic Year-Term, Academic Year)
  - Student Key (FK) -- Student Dimension (expanded applicant dim with on-campus info)
  - Course Key (FK) -- Course Dimension (Name, Department, Format, Credit Hours)
  - Instructor Key (FK) -- Instructor Dimension (Employee ID, Name, Address, Type, Tenure Indicator, Hire Date, Years of Service)
  - Course Registration Count (=1) -- artificial count metric
- **Term Dimension** conforms to calendar date dimension (same column labels and values)
- **Student Dimension**: expanded applicant dimension with part-time/full-time status, residence, athletic involvement, declared major, class level status
  - Consider type 4 mini-dimension for declared major, class level, graduation attainment
  - Or SCD type 7 with dual student dimension keys for historical and current profiles
- **Artificial Count Metric**: always-1 count fact makes SQL more readable (SUM vs COUNT), required for aggregate tables and OLAP cubes
- Can add measurable facts later (tuition revenue, earned credit hours, grade scores) -- then no longer factless

#### 13.3.3 Multiple Course Instructors
- Options for co-taught courses:
  1. Alter grain to one row per instructor per course registration per student per term (unnatural, prone to overstated counts)
  2. Bridge table with instructor group key (preferred -- with weighting factor for workload allocation)
  3. Concatenate instructor names into a single course dimension attribute (labeling only)
  4. Single primary instructor FK in fact table, prefaced attributes in dimension

#### 13.3.4 Course Registration Periodic Snapshots
- Grain: one row per student's registered courses per term per snapshot date
- Snapshot dates: preregistration, start of term, course drop/add deadline, end of term

#### 13.3.5 Facility Utilization (Coverage Factless Fact Table) -- Figure 13-5
- **Facility Utilization Fact** (factless, coverage type)
  - Term Key (FK) -- Term Dimension
  - Day of Week Key (FK) -- Day of Week Dimension
  - Time-of-Day Hour Key (FK) -- Time-of-Day Hour Dimension (Hour, Day Part Indicator)
  - Facility Key (FK) -- Facility Dimension
  - Owner Department Key (FK) -- Department Dimension (2 views for roles)
  - Assigned Department Key (FK)
  - Utilization Status Key (FK) -- Utilization Status Dimension (Available / Utilized)
  - Facility Count (=1)
- **Facility Dimension**: Building Name-Room, Building Name, Address, Type (classroom, lab, office), Floor, Square Footage, Capacity, Projector Indicator, Vent Indicator, ...
- One row per facility per hourly time block per day of week per term
- Inserted regardless of whether facility is being used (coverage)
- Supports: occupancy rates, utilization by time of day, Friday drop-off analysis

### 13.4 Student Attendance -- Figure 13-6
- **Student Attendance Fact**
  - Date Key (FK) -- Date Dimension
  - Student Key (FK) -- Student Dimension
  - Course Key (FK) -- Course Dimension
  - Instructor Key (FK) -- Instructor Dimension
  - Facility Key (FK) -- Facility Dimension
  - Attendance Count
- Grain: one row per student per course per day (calendar date, not term)
- Shares dimensions with course registration schema

#### 13.4.1 Explicit Rows for What Didn't Happen
- Add rows for attendance events that didn't occur (no-shows)
- Attendance metric = 1 or 0
- Viable because non-attendance events share same dimensionality and won't grow at alarming rates
- NOT viable in all scenarios (e.g., adding rows for promoted products that weren't purchased)

#### 13.4.2 What Didn't Happen with Multidimensional OLAP
- OLAP cubes handle sparsity well, minimizing overhead of storing explicit zeroes
- For non-sparse fact cubes, event and non-event analysis available while reducing relational star schema complexities

### 13.5 More Educational Analytic Opportunities
- **Research grant analysis**: variation of financial analysis (Chapter 7), subledger grain; dimensions include funding source, research topic, grant duration, faculty investigator
- **Alumni relationship management**: similar to CRM (Chapter 8); attributes include geographic, demographic, employment, interests, behavioral info, student-era data (affiliations, housing, school, major, honors)
- Robust CRM operational system should track all alumni touch points

---
```

### chapter-14-healthcare-pp-339-352

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-14-healthcare-pp-339-352
Hash: 2dbd05936ea1

```
### 14.1 Healthcare Case Study and Bus Matrix
- **Industry**: Healthcare consortium (physicians, clinics, hospitals, pharmacies, laboratories)
- **Challenges**: integrate clinical and administrative data, improve patient outcomes, manage costs
- **Data categories**: administrative (claims billing) and clinical (medical records)
- **Bus Matrix (Figure 14-1) -- Conformed Dimensions**
  - Date
  - Patient
  - Physician
  - Employee
  - Facility
  - Diagnosis
  - Procedure
  - Payer

#### Clinical Events
| Process | Date | Patient | Physician | Employee | Facility | Diagnosis | Procedure | Payer |
|---|---|---|---|---|---|---|---|---|
| Patient Encounter Workflow | X | X | X | X | X | X | | |
| Procedures | X | X | X | X | X | X | X | |
| Physician Orders | X | X | X | | X | X | | |
| Medications | X | X | X | | | X | | |
| Lab Test Results | X | X | X | X | X | X | X | |
| Disease/Case Management Participation | X | X | X | X | X | X | | |
| Patient Reported Outcomes | X | X | X | | X | X | X | |
| Patient Satisfaction Surveys | X | X | X | | X | X | | |

#### Billing/Revenue Events
| Process | Date | Patient | Physician | Facility | Diagnosis | Procedure | Payer |
|---|---|---|---|---|---|---|---|
| Inpatient Facility Charges | X | X | X | X | X | X | |
| Outpatient Professional Charges | X | X | X | X | X | X | |
| Claims Billing | X | X | X | X | X | X | X |
| Claims Payments | X | X | X | X | X | X | X |
| Collections and Write-Offs | X | X | X | X | X | X | X |

#### Operational Events
| Process | Date | Patient | Physician | Employee | Facility | Diagnosis | Procedure |
|---|---|---|---|---|---|---|---|
| Bed Inventory Utilization | X | X | X | X | X | | |
| Facilities Utilization | X | X | X | X | X | | |
| Supply Procurement | X | | | | X | X | |
| Supply Utilization | X | X | X | X | X | X | |
| Workforce Scheduling | X | | | | X | X | |

### 14.2 Conformed Dimensions in Healthcare
- **Patient**: most important conformed dimension; 360-degree view critical
  - EMR and EHR systems focus on this
  - Historically challenging due to lack of reliable national ID across facilities
  - HIPAA privacy and security requirements
- **Other conformed dimensions**:
  - Date
  - Responsible party
  - Employer
  - Health plan
  - Payer (primary and secondary)
  - Physician
  - Procedure
  - Equipment
  - Lab test
  - Medication
  - Diagnosis
  - Facility (office, clinic, outpatient facility, hospital)
- **Diagnosis dimension**: structured via ICD (International Classification of Diseases) standard
- **Procedure dimension**: structured via HCPCS (Healthcare Common Procedure Coding System) based on AMA's CPT (Current Procedural Terminology)
- **Dental**: CDT (Current Dental Terminology) code set

### 14.3 Claims Billing and Payments

#### 14.3.1 Grain Choices
- **Transaction grain**: every billing transaction + every claim payment transaction
- **Periodic snapshot grain**: long-running time series (bank accounts, insurance policies) -- not ideal for short-lived claims
- **Accumulating snapshot grain**: chosen for claims billing and payment workflow

#### 14.3.2 Accumulating Snapshot -- Figure 14-2
- **Claims Billing and Payment Workflow Fact** (grain: one line item on a medical claim)
  - **8 Role-Playing Date Dimension Keys**
    - Treatment Date Key (FK)
    - Primary Insurance Billing Date Key (FK)
    - Secondary Insurance Billing Date Key (FK)
    - Responsible Party Billing Date Key (FK)
    - Last Primary Insurance Payment Date Key (FK)
    - Last Secondary Insurance Payment Date Key (FK)
    - Last Responsible Party Payment Date Key (FK)
    - Zero Balance Date Key (FK)
  - Patient Key (FK) -- Patient Dimension
  - Physician Key (FK) -- Physician Dimension
  - Physician Organization Key (FK) -- Physician Organization Dimension
  - Procedure Key (FK) -- Procedure Dimension
  - Facility Key (FK) -- Facility Dimension
  - Primary Diagnosis Key (FK) -- Primary Diagnosis Dimension
  - Primary Insurance Organization Key (FK) -- Insurance Organization Dimension (views for 2 roles)
  - Secondary Insurance Organization Key (FK)
  - Responsible Party Key (FK) -- Responsible Party Dimension
  - Employer Key (FK) -- Employer Dimension
  - Master Bill ID (DD)
  - **Monetary Facts**
    - Billed Amount
    - Primary Insurance Paid Amount
    - Secondary Insurance Paid Amount
    - Responsible Party Paid Amount
    - Total Paid Amount (calculated)
    - Sent to Collections Amount
    - Written Off Amount
    - Unpaid Balance Amount (calculated)
  - **Duration/Lag Facts**
    - Length of Stay
    - Bill to Initial Primary Insurance Payment Lag
    - Bill to Initial Secondary Insurance Payment Lag
    - Bill to Initial Responsible Party Payment Lag
    - Bill to Zero Balance Lag
- Row initially created when charges are received; last 7 dates initially point to "To Be Determined" date dimension row
- Rows are destructively updated as payments received and bills sent
- Companion transaction schemas needed for messy payment scenarios (multiple payments per line, single payment across claims)
- Partitioning on treatment date key preserves physical clustering

### 14.4 Date Dimension Role Playing
- 8 date FKs should NOT join to a single instance of the date dimension
- Create 8 views on the single underlying date dimension table
- View definitions cosmetically relabel column names for business user understanding
- Other dimensions also role-play: payer dimension (primary/secondary insurance), physician dimension (referring, attending, consulting, assisting)

### 14.5 Multivalued Diagnoses
- Diagnosis dimension is naturally multivalued (patients have multiple simultaneous diagnoses)
- EMR applications facilitate capturing many diagnoses (not just minimal coding for reimbursement)
- Elderly hospitalized patients may have 20+ simultaneous diagnoses
- Diagnoses don't fit into well-defined roles (unlike origin/destination airports)
- **Anti-pattern**: multiple diagnosis foreign keys in fact table -- inefficient BI queries, can't constrain to a specific slot

#### 14.5.1 Bridge Table Approach -- Figure 14-3
- **Diagnosis Group Bridge**
  - Diagnosis Group Key (FK)
  - Diagnosis Key (FK)
- **Diagnosis Dimension**
  - Diagnosis Key (PK)
  - Diagnosis Code (NK)
  - Diagnosis Description
  - Diagnosis Section Code / Description
  - Diagnosis Category Code / Description
- Fact table references Diagnosis Group Key instead of individual Diagnosis Key
- Many-to-many join between fact table and diagnosis dimension via bridge
- Weighting factors generally NOT used for diagnoses (impossible to weight impact of each diagnosis beyond "primary" designation)
- Analysis focuses on "impact questions" (e.g., total billed amount for procedures involving congestive heart failure) -- analysts understand this may over-count

#### 14.5.2 Diagnosis Group Dimension for Primary Key Relationships -- Figure 14-4
- Insert a Diagnosis Group Dimension between fact table and bridge
  - Diagnosis Group Key (PK) in group dimension
  - Both fact table and bridge have conventional many-to-one joins
- Portfolio of diagnosis groups that are repeatedly used (lookup existing, create new during ETL)
- For inpatient stays: diagnosis group may be unique per patient, may evolve over time
  - Supplement bridge table with begin and end date stamps for change tracking

### 14.6 Supertypes and Subtypes for Charges
- Healthcare charges follow supertype/subtype pattern (Chapter 10)
- **Inpatient facility charges** differ from **outpatient professional charges**
- **Inpatient Hospital Claim Billing and Payment Workflow Fact** -- Figure 14-5
  - All fields from Figure 14-2 plus:
  - **Admitting Physician Key (FK)** -- role-playing physician
  - **Admitting Physician Organization Key (FK)**
  - **Attending Physician Key (FK)** -- role-playing physician
  - **Attending Physician Organization Key (FK)**
  - **Admitting Diagnosis Group Key (FK)** -- determined at beginning of hospital stay, same for all treatment rows in same stay
  - **Discharge Diagnosis Group Key (FK)** -- not known until patient discharged
- Physician role-playing: admitting physician vs. attending physician (plus physician organizations for each)
- Complex surgical events: primary responsible physician FK in fact table + multivalued bridge table for team of specialists and assistants

### 14.7 Electronic Medical Records
- Extreme variability and potentially extreme volumes
- Data forms: numeric, freeform text comments, images, photographs
- EMR/EHR is a classic use case for big data (Chapter 21)

### 14.8 Measure Type Dimension for Sparse Facts -- Figure 14-6
- **Lab Test Result Facts**
  - Order Date Key (FK)
  - Test Date Key (FK)
  - Patient Key (FK)
  - Physician Key (FK)
  - Lab Test Key (FK)
  - Lab Test Measurement Type Key (FK) -- Lab Test Measurement Type Dimension
  - Observed Test Result Value
- **Lab Test Measurement Type Dimension**
  - Lab Test Measurement Type Key (PK)
  - Lab Test Measurement Type Description
  - Lab Test Measurement Type Unit of Measure
- Grain shifts from "one row per event" to "one row per measurement per event"
- Superbly flexible: add new measurement types via dimension rows, not schema changes
- Eliminates nulls from sparse positional fact tables
- **Trade-offs**:
  - May generate many more fact table rows (10 measurements = 10 rows vs. 1)
  - Complicates BI access: combining two numbers from a single event requires fetching two rows
  - SQL arithmetic works within rows, not across rows
  - Mixing incompatible amounts in a single column
  - OLAP cubes more tolerant of measurement type approach
- Best for extremely sparse data (clinical lab, manufacturing test environments)
- Return to classic fixed-column design when fact density grows

### 14.9 Freeform Text Comments
- NOT stored directly in the fact table (waste space, clutter, hurt query performance)
- NOT treated as degenerate dimensions (those are for short operational transaction numbers)
- **Two storage options**:
  1. **Transaction event dimension**: if nearly every fact row has a unique comment, store text as attribute in a transaction dimension
  2. **Separate comments dimension**: if unique comments are much fewer than fact rows (many "No Comment"), store in a comments dimension with FK from fact table
- Either way, queries joining text comments and fact metrics will perform poorly (two voluminous table joins)
- Business users typically drill into text comments after applying highly selective fact table filters

### 14.10 Images
- Medical record data may include images (e.g., X-rays, photos)
- **Two options**:
  1. JPEG filename in the fact table (other programs can freely access)
  2. Image as BLOB directly in the database
- JPEG filename approach: advantage of interoperability; disadvantage of maintaining synchrony between file system and fact table

### 14.11 Facility/Equipment Inventory Utilization
- Healthcare organizations track utilization of patient beds, surgical operating theatres, equipment
- **Bed utilization periodic snapshot**: factless fact table with every bed's status at regular intervals (midnight, start of shift, more frequently)
  - Foreign keys: snapshot date, time-of-day, patient, attending physician, assigned nurse
- **Bed inventory transaction fact table**: one row per movement into/out of a hospital bed
  - Transaction date and time dimension FKs
  - Movement type dimension (filled, vacated)
- **Operating room utilization**: statuses like pre-operation, post-operation, downtime; with time durations
- **Timespan fact table** (Chapter 8): for non-volatile inventory like rehabilitation/eldercare beds; row effective and expiration dates/times represent bed states over time

### 14.12 Dealing with Retroactive Changes
- Healthcare has frequent late-arriving data (weeks or months late)
- Patient procedures reported weeks late; patient profile updates back-dated months
- More delayed = more challenging ETL processing
- Late-arriving fact and dimension scenarios discussed further in Chapter 19
- May be the dominant mode of processing (not a specialized exception) in healthcare
- Goal: improve source capture systems to reduce frequency of late-arriving data anomalies

---
```

### cross-chapter-pattern-index

URL: https://local.taxonomy/kimball-dw-toolkit/cross-chapter-pattern-index
Hash: f0749a735d36

```
### Dimensional Modeling Patterns Referenced Across Chapters 11-14

| Pattern | Ch 11 | Ch 12 | Ch 13 | Ch 14 |
|---|---|---|---|---|
| Bus Matrix | x | x | x | x |
| Design Review / Checklist | x | | | |
| Degenerate Dimensions | x | x | | |
| Surrogate Keys | x | x | x | x |
| Role-Playing Dimensions | | x (date, time, airport) | x (date) | x (date x8, physician, payer, insurance org, diagnosis group) |
| Mini-Dimensions (Type 4) | | x (passenger profile) | x (student attributes) | |
| Conformed Dimensions | x | x | x | x |
| Snowflake (anti-pattern) | x (sales channel) | | | |
| Junk Dimensions | | x (combined class of service) | | |
| Outriggers | x (geographic location) | x (country-specific calendar) | | |
| Accumulating Snapshots | | x (revenue/availability) | x (applicant pipeline, research grant) | x (claims billing/payment) |
| Factless Fact Tables (Event) | | | x (admissions events, course registration, student attendance) | |
| Factless Fact Tables (Coverage) | | | x (facility utilization) | x (bed utilization periodic snapshot) |
| Bridge Tables | | | x (multiple instructors) | x (diagnosis group bridge) |
| Multivalued Dimensions | | | x (multiple instructors) | x (multiple diagnoses, physician teams) |
| Supertype/Subtype | | | | x (inpatient vs. outpatient charges) |
| Measurement Type Dimension | | | | x (lab test results) |
| Multiple Granularities | | x (leg, segment, trip, itinerary) | | x (transaction, periodic snapshot, accumulating snapshot) |
| Geographic Dimensions | x (location dimension) | x (airport, port) | | x (facility) |
| Date/Time Zones | | x (local + GMT date/time pairs) | | |
| Country-Specific Calendars | | x (outrigger with holidays, seasons) | | |
| Text Comments Handling | | | | x (separate dimension or transaction event dimension) |
| Image Handling | | | | x (JPEG filename or BLOB) |
| Retroactive/Late-Arriving Data | | | | x |
| Remodeling Existing Structures | x | | | |
| What Didn't Happen (Non-Events) | | | x (student attendance no-shows, OLAP sparsity) | |


# Kimball Data Warehouse Toolkit 3e -- Chapters 15-16 Taxonomy

Source: Kimball & Ross, *The Data Warehouse Toolkit*, 3rd Edition, pp. 353-401.

---
```

### chapter-15-electronic-commerce-pp-353-373

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-15-electronic-commerce-pp-353-373
Hash: 355faf5a7f84

```
### 1. Clickstream Source Data
- Distributed collection across multiple physical servers
- Log file synchronization challenges (clock drift at sub-second level)
- Data origins
  - Own server log files
  - Referring partner logs
  - ISP logs
  - Search engine referral specifications
  - ISP-provided direct customer access (captive clickstream)
- Basic form: stateless, isolated page retrieval events
- Core problem: anonymity of visitors and sessions

### 2. Clickstream Data Challenges

#### 2.1 Identifying the Visitor Origin
- Browser home page (default)
- Portal/search engine referral (Yahoo!, Google)
  - Paid placement fee vs. organic index
  - Word/content search
- Browser bookmark
- Clickthrough (deliberate link click)
  - Paid-for referral (banner ad)
  - Free referral (cooperating site)
  - Referring site identifiable in web event record

#### 2.2 Identifying the Session
- Session = unique visitor session (visit), analogous to supermarket receipt
- Session ID: generated by operational application, not web server
- HTTP is stateless -- no built-in session concept
- Five methods of session tracking:
  1. **IP address collation** -- time-contiguous log entries from same host; breaks down with dynamic IPs, firewalls
  2. **Session-level cookie** -- browser places transient cookie; lasts while browser open; cannot identify return visits
  3. **SSL session tracking** -- login via encryption keys; high overhead, security pop-ups
  4. **Hidden field / URL query string** -- session ID embedded in dynamic pages; fragile, breaks with non-cooperating vendors
  5. **Persistent cookie** -- survives browser close; most reliable; can be refused/deleted; enables "super session" across cooperating sites
- Best practice: persistent cookie > session cookie + IP collation

#### 2.3 Identifying the Visitor
- Visitors may want anonymity
- Identity may be inaccurate even when requested
- Cannot distinguish family members on shared computer
- Cookie identifies computer, not individual (office vs. home vs. mobile)

### 3. Clickstream Dimensional Models

#### 3.1 Dimension Portfolio for Web Retailer
- **Standard dimensions** (reused from other business processes):
  - Date
  - Time of day
  - Part
  - Vendor
  - Status
  - Carrier
  - Facilities location
  - Product
  - Customer
  - Media
  - Promotion
  - Internal organization
  - Employee
- **Clickstream-unique dimensions** (new):
  - Page
  - Event
  - Session
  - Referrer

#### 3.2 Page Dimension (Figure 15-1)
- Grain: one row per interesting distinguishable page type
- Attributes:
  - Page Key (surrogate, 1..N)
  - Page Source (Static, Dynamic, Unknown, Corrupted, Inapplicable)
  - Page Function (Portal, Search, Product description, Corporate information)
  - Page Template (Sparse, Dense)
  - Item Type (Product SKU, Book ISBN, Telco rate type)
  - Graphics Type (GIF, JPG, Progressive disclosure, Size pre-declared)
  - Animation Type
  - Sound Type
  - Page File Name
- Static pages: own row each
- Dynamic pages: grouped by similar function and type
- Change handling: Type 1 overwrite or SCD technique

#### 3.3 Event Dimension (Figure 15-2)
- Grain: what happened on a page at a point in time
- Attributes:
  - Event Key (surrogate, 1..N)
  - Event Type (Open page, Refresh page, Click link, Unknown, Inapplicable)
  - Event Content (application-dependent, XML-tag driven)
- Sub-page granularity possible (graphical elements, links, game gestures)
  - Can generate hundreds of rows per page view
  - 10+ TB/day at extreme granularity

#### 3.4 Session Dimension (Figure 15-3)
- Provides diagnosis of the visitor's session as a whole
- Attributes:
  - Session Key (surrogate, 1..N)
  - Session Type (Classified, Unclassified, Corrupted, Inapplicable)
  - Local Context (page-derived, e.g., "Requesting Product Information")
  - Session Context (trajectory-derived, e.g., "Ordering a Product")
  - Action Sequence (summary label for overall sequence of actions)
  - Success Status (whether overall session mission was accomplished)
  - Customer Status (New customer, High value, About to cancel, In default)
- Analytical questions enabled:
  - How many consulted product info before ordering?
  - How many looked but never ordered?
  - How many did not finish ordering? Where did they stop?

#### 3.5 Referrer Dimension (Figure 15-4)
- How the customer arrived at the current page
- Attributes:
  - Referral Key (surrogate, 1..N)
  - Referral Type (Intra site, Remote site, Search engine, Corrupted, Inapplicable)
  - Referring URL (full URL)
  - Referring Site (domain)
  - Referring Domain
  - Search Type (Simple text match, Complex logical match)
  - Specification (actual search spec, simplified/cleaned)
  - Target (Meta tags, Body text, Title)

### 4. Clickstream Fact Tables

#### 4.1 Clickstream Session Fact Table (Figure 15-5)
- **Grain:** one row per completed customer session
- **Dimensions:**
  - Date Dimension (2 views for roles: universal date, local date)
  - Entry Page Dimension
  - Customer Dimension
  - Session Dimension
  - Referrer Dimension
- **Foreign keys and stamps:**
  - Universal Date Key (FK)
  - Universal Date/Time
  - Local Date Key (FK)
  - Local Date/Time
  - Customer Key (FK)
  - Entry Page Key (FK)
  - Session Key (FK)
  - Referrer Key (FK)
  - Session ID (DD -- degenerate dimension)
- **Facts (measures):**
  - Session Seconds
  - Pages Visited
  - Orders Placed
  - Order Quantity
  - Order Dollar Amount
- Design notes:
  - Two role-playing calendar date dimensions (universal synchronized time vs. local wall clock time)
  - Date/time stamps instead of time-of-day dimension (avoids ridiculously large dimension)
  - Entry page = the page the session started with (how customer arrived)
  - Causal dimension inappropriate at session grain (multivalued across products)

#### 4.2 Clickstream Page Event Fact Table (Figure 15-6)
- **Grain:** individual page event per customer session (micro events like JPGs/GIFs excluded)
- **Dimensions:**
  - Date Dimension (2 views for roles)
  - Page Dimension
  - Customer Dimension
  - Event Dimension
  - Session Dimension
  - Step Dimension (3 views for roles)
  - Product Dimension
  - Promotion Dimension
  - Referrer Dimension
- **Foreign keys:**
  - Universal Date Key (FK)
  - Universal Date/Time
  - Local Date Key (FK)
  - Local Date/Time
  - Customer Key (FK)
  - Page Key (FK)
  - Event Key (FK)
  - Session Key (FK)
  - Session ID (DD)
  - Session Step Key (FK)
  - Purchase Step Key (FK)
  - Abandonment Step Key (FK)
  - Product Key (FK)
  - Referrer Key (FK)
  - Promotion Key (FK)
- **Facts:**
  - Page Seconds (time before next page event; conformed with session seconds)
  - Order Quantity (zero/null for non-order events)
  - Order Dollar Amount (zero/null for non-order events)
- Design notes:
  - Page dimension now refers to individual page (vs. entry page in session fact)
  - Session ID is degenerate dimension (parent key linking to session fact)
  - Session dimension describes classes/categories, not individual sessions

#### 4.3 Step Dimension (from CRM, Chapter 8)
- Provides position of page event within the overall session
- Attributes:
  - Step Key (PK)
  - Step Number
  - Steps Until End
- Three role-playing views on the same physical table:
  1. **Session Step** -- position within overall session
  2. **Purchase Step** -- position within purchase subsession (ends in successful purchase)
  3. **Abandonment Step** -- position within abandonment subsession (fails to complete purchase)
- Powerful for analyzing sequential processes
- Constraining purchase step to step 1 returns starting pages for successful purchases
- Constraining abandonment step to 0 steps remaining returns last unfulfilling pages

#### 4.4 Aggregate Clickstream Fact Table -- Session Aggregate (Figure 15-7)
- **Grain:** grouped by month, demographic type, entry page, session outcome
- **Dimensions:**
  - Month Dimension (conformed subset of calendar date)
  - Entry Page Dimension
  - Demographic Dimension (conformed subset of customer)
  - Session Outcome Dimension
- **Facts:**
  - Number of Sessions
  - Session Seconds
  - Pages Visited
  - Orders Placed
  - Order Quantity
  - Order Dollar Amount
- Performance: ~100x faster than session-grained table; <1% of original size

### 5. Google Analytics
- External data warehouse delivering website usage insights
- GA Tracking Code (GATC) embedded in HTML `<head>`
- JavaScript-dependent; collects all clickstream info except PII
- Combines with AdWord service for ad campaign and conversion tracking
- Data elements described as dimensions and measures (Kimball-aligned)
- Used by 50%+ of popular websites

### 6. Integrating Clickstream into Web Retailer's Bus Matrix (Figure 15-8)
- Enterprise bus matrix for web-based computer retailer
- Business process groups:
  - **Supply Chain Management:** Supplier Purchase Orders, Supplier Deliveries, Part Inventories, Product Assembly Bill of Materials, Product Assembly to Order
  - **Customer Relationship Management:** Product Promotions, Advertising, Customer Communications, Customer Inquiries, **Web Visitor Clickstream**, Product Orders, Service Policy Orders, Product Shipments, Customer Billing, Customer Payments, Product Returns, Product Support, Service Policy Responses
  - **Operations:** Employee Labor, Human Resources, Facilities Operations, Web Site Operations
- Web Visitor Clickstream shares conformed dimensions with other processes:
  - Date/Time, Product, Customer, Media, Promotion
  - Plus 4 unique clickstream dimensions (Page, Event, Session, Referrer)
- Matrix serves as communication vehicle for conforming dimensions and facts

### 7. Profitability Across Channels Including Web (Figure 15-9)
- Extends sales transaction process to include web profitability
- **Grain:** individual line item sold on a sales ticket (any channel)
- **Profitability Fact Table dimensions:**
  - Date Dimension (2 views for roles)
  - Time of Day Dimension (2 views for roles)
  - Customer Dimension
  - Product Dimension
  - Channel Dimension
  - Promotion Dimension
- **Degenerate dimension:** Ticket Number (DD)
- **P&L-structured facts (top to bottom):**
  - Units Sold
  - Gross Revenue
  - Manufacturing Allowance
  - Marketing Promotion
  - Sales Markdown
  - **Net Revenue** (calculated: Gross Revenue - allowances/promos/markdowns)
  - Manufacturing Cost
  - Storage Cost
  - **Gross Profit** (calculated: Net Revenue - Mfg Cost - Storage Cost)
  - Freight Cost
  - Special Deal Cost
  - Other Overhead Cost
  - **Net Profit** (calculated: Gross Profit - all additional costs)
- Cost allocation approaches:
  - National average ratios
  - Calendar quarter / geographic region breakdowns
  - Activity-based costing (ABC) -- most granular and realistic
- Website cost allocation schemes:
  - By number of pages devoted to each product
  - By pages visited
  - By actual web-based purchases
- Analytical questions enabled:
  - Profitability by channel (web, telesales, store)
  - Profitability by customer segment, product line, promotion, time period
  - Cross-dimensional: profitable customers per channel, web-effective promotions

---
```

### chapter-16-insurance-pp-375-401

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-16-insurance-pp-375-401
Hash: bf2496f9555d

```
### 1. Insurance Case Study Context
- Property and casualty insurer: automobile, homeowner, personal property
- Interview-driven requirements: claims, field operations, underwriting, finance, marketing
- Industry challenges: globalization, deregulation, demutualization, alternative channels
- Core data problem: multiple disparate legacy systems per line of business (auto, home, personal property)
  - Same policyholder identified separately in each system
  - Isolated data islands; no cross-selling integration
  - Multiple redundant analytic repositories with inconsistent results

### 2. Insurance Value Chain
- Core processes (seemingly simple):
  1. **Issue policies**
  2. **Collect premium payments**
  3. **Process claims**
- Users want to analyze:
  - Detailed transactions for policy formulation
  - Transactions from claims processing
  - Performance over time by coverage, covered item, policyholder, sales channel
  - Enterprise-wide and line-of-business perspectives
- External processes: investment of premiums, agent compensation, HR, finance, purchasing
- Policy transactions: single fact table or separate tables (quoting, rating, underwriting)
- Premium revenue complexity:
  - Pay-in-advance model (like magazine subscriptions, extended warranties)
  - Premium spread across multiple periods as revenue is earned
  - Transaction view vs. snapshot view always required together
  - Premium snapshot is NOT merely a summarization of transactions -- sourced separately

### 3. Draft Bus Matrix (Figure 16-1)
- Two initial business process rows:
  1. **Policy Transactions** -- dimensions: Date, Policyholder, Covered Item, Coverage, Employee, Policy
  2. **Premium Snapshot** -- dimensions: Date (Month), Policyholder, Covered Item, Coverage, Employee (Agent), Policy

### 4. Policy Transactions

#### 4.1 Transaction Types
- Create policy, alter policy, cancel policy (with reason)
- Create coverage on covered item, alter coverage, cancel coverage (with reason)
- Rate coverage or decline to rate coverage (with reason)
- Underwrite policy or decline to underwrite policy (with reason)

#### 4.2 Policy Transaction Fact Table Grain
- One row per individual atomic policy transaction
- Almost entirely keys; single numeric fact (Policy Transaction Dollar Amount)
- Fact interpretation depends on transaction type dimension

#### 4.3 Dimension Role Playing
- Two date roles on single physical date table:
  1. **Policy Transaction Date** -- when entered into operational system
  2. **Policy Effective Date** -- when transaction legally takes effect
- Presented through views with unique column names

#### 4.4 Slowly Changing Dimensions (applied to Policyholder)
- **Type 1 (overwrite):** corrections, e.g., date of birth changes
- **Type 2 (add row):** tracking changes, e.g., ZIP code changes (key input to pricing/risk)
  - New surrogate key + updated geographic attributes
  - Historical fact rows retain old surrogate key
  - Most common SCD technique
  - Row count grows with each change (1M+ rows possible)
  - May use mini-dimension for ZIP code tracking instead
- **Type 3 (add column):** segment reclassification
  - "Historical" column retains old classification alongside new
  - Useful for en masse reclassification (e.g., nonresidential -> large multinational / middle market / small business / nonprofit / government)
  - Becomes complex with multiple attributes or versions

#### 4.5 Mini-Dimensions for Large or Rapidly Changing Dimensions
- Policyholder dimension: 1M+ rows
- Split closely monitored, rapidly changing attributes into mini-dimensions
- Mini-dimension linked to fact table with separate surrogate key
- All possible attribute value combinations pre-created
- Change = different key in fact table row from that point forward
- Also applicable to Covered Item dimension (house, car, etc.)
  - Variable textual descriptions belong in dimensions, not facts

#### 4.6 Multivalued Dimension Attributes
- Commercial customers associated with multiple SIC/NAICS industry codes
- Bridge table ties all industry classification codes within a group
  - Joins to fact table or customer dimension as outrigger
  - Includes weighting factor (e.g., 50% agricultural services, 30% dairy, 20% oil/gas)
  - Special "Unknown" bridge row for customers with no valid industry code

#### 4.7 Numeric Attributes as Facts or Dimensions
- Appraised value of covered item: continuously valued numeric -> treat as fact
- Descriptive value range (e.g., "$250,000 to $299,999 Appraised Value"): dimension attribute for grouping/filtering
- Coverage limit: standardized values (e.g., "Replacement Value or Up to $250,000") -> dimension attribute

#### 4.8 Degenerate Dimension
- Policy number: degenerate dimension after all header info extracted to other dimensions
- Avoid overloaded policy dimension with policyholder, dates, coverages
- Exception: if attributes like risk grade belong solely to policy, create a real policy dimension

#### 4.9 Low Cardinality Dimension Tables
- Policy Transaction Type dimension: <50 rows
- Contains transaction types + reason descriptions
- Even small/narrow tables should be proper dimensions if used for filtering/labeling

#### 4.10 Audit Dimension
- Links fact rows to ETL process metadata
- Describes data lineage: extract time, source table, extract software version

#### 4.11 Policy Transaction Fact Table Schema (Figure 16-2)
- **Dimensions:**
  - Date Dimension (2 views for roles)
  - Policyholder Dimension
  - Coverage Dimension
  - Policy Transaction Type Dimension
  - Employee Dimension
  - Covered Item Dimension
  - Policy Transaction Audit Dimension
- **Keys and degenerate dimensions:**
  - Policy Transaction Date Key (FK)
  - Policy Effective Date Key (FK)
  - Policyholder Key (FK)
  - Employee Key (FK)
  - Coverage Key (FK)
  - Covered Item Key (FK)
  - Policy Transaction Type Key (FK)
  - Policy Transaction Audit Key (FK)
  - Policy Number (DD)
  - Policy Transaction Number (DD)
- **Fact:**
  - Policy Transaction Dollar Amount

#### 4.12 Heterogeneous Supertype and Subtype Products (Figure 16-3)
- Enterprise-wide perspective vs. line-of-business specifics
- Different coverage parameters per line (homeowners vs. auto vs. personal property)
- Generalize with supertype/subtype technique:
  - Supertype fact table shared across all lines
  - Subtype dimension tables per line of business (coverage type)
  - No separate line-of-business fact tables needed (metrics don't vary)
  - Views on supertype fact table filter to specific subtype rows
- Example -- Automobile subtype dimensions:
  - **Automobile Coverage Dimension:** Coverage Key, Coverage Description, Line of Business Description, Limit, Deductible, Rental Car Coverage, Windshield Coverage
  - **Automobile Coverage Item Dimension:** Covered Item Key, Covered Item Description, Vehicle Manufacturer, Vehicle Make, Vehicle Year, Vehicle Classification, Vehicle Engine Size, Vehicle Appraised Value Range

#### 4.13 Complementary Policy Accumulating Snapshot
- Grain: one row per coverage and covered item on a policy
- Captures cumulative lifespan of policy/coverage/covered item
- Policy-centric milestone dates: quoted, rated, underwritten, effective, renewed, expired
- Multiple employee roles: agent, underwriter
- Most policy transaction dimensions reusable (except transaction type)
- Expanded fact set vs. transaction table

### 5. Premium Periodic Snapshot

#### 5.1 Schema Design (Figure 16-4)
- Companion fact table to policy transactions
- **Grain:** one row per coverage and covered item on a policy, per month
- **Dimensions:**
  - Month End Dimension (conformed month, replaces daily date)
  - Policyholder Dimension (conformed, identical)
  - Coverage Dimension (conformed, identical)
  - Covered Item Dimension (conformed, identical)
  - Agent Dimension (replaces generic Employee; subset)
  - Policy Status Dimension (new; e.g., new policies, cancellations)
- **Degenerate dimension:** Policy Number (DD)
- **Facts:**
  - Written Premium Revenue Amount
  - Earned Premium Revenue Amount
- Written vs. earned example:
  - Annual policy, $600, written Jan 1: Written = $600 (Jan), Earned = $50/month
  - Feb: Written = $0, Earned = $50
  - Canceled Mar 31: Written = -$450 (Mar), Earned = $50 (Mar); earned revenue halts

#### 5.2 Conformed Dimensions
- Reuse as many dimensions as possible from policy transaction table
- Policyholder, covered item, coverage: identical across both fact tables
- Daily date replaced by conformed month dimension
- Employee replaced by Agent (field operations focus)
- Transaction type not applicable; replaced by Policy Status dimension

#### 5.3 Conformed Facts
- Facts appearing in multiple fact tables must have consistent definitions and labels
- If not identical, give them different names

#### 5.4 Pay-in-Advance Facts
- Written premium vs. earned premium distinction critical
- Revenue recognition rules complex (mid-month upgrades/downgrades)
- Sourced from separate operational revenue recognition system
- Transaction + snapshot fact tables both needed; neither can replace the other

#### 5.5 Heterogeneous Supertypes/Subtypes Revisited
- Custom facts per line of business are incompatible with each other
- Separate monthly snapshot physically by line of business:
  - Single supertype monthly snapshot schema
  - Subtype snapshots per line (auto, home, etc.)
  - Each subtype is a copy of supertype segment for that coverage type
  - Supertype facts included in subtype for convenience

#### 5.6 Multivalued Dimensions Revisited (Figure 16-5)
- Automobile insurance: multiple insured drivers per policy
- Bridge table: Policy-Insured Driver Bridge
  - Policy Key (FK)
  - Insured Driver Key (FK)
  - Weighting Factor (driver's share of total premium cost)
- Insured Driver Dimension: name, address, date of birth, risk segment
- Effective and expiration dates on bridge table -> factless fact table capturing evolving relationships

### 6. Claims Processing Background
- After policy in effect, claims made against specific coverage and covered item
- Claimant: policyholder or new party
- Claim lifecycle:
  1. Claim opened -> reserve established (preliminary liability estimate)
  2. Reserve adjusted as information develops
  3. Investigative phase: adjuster inspects, interviews claimant/policyholder
  4. Payments issued to third parties (doctors, lawyers, body shops) and/or claimant
  5. Salvage: insurer takes possession of replaced item; salvage payments credit claim
  6. Claim completed and closed
  7. Possible reopening (further payments or lawsuits)

### 7. Updated Insurance Bus Matrix (Figure 16-6)
- Three business process rows:
  1. **Policy Transactions** -- Date, Policyholder, Covered Item, Coverage, Employee, Policy
  2. **Premium Snapshot** -- Date (Month), Policyholder, Covered Item, Coverage, Employee (Agent), Policy
  3. **Claim Transactions** -- Date, Policyholder, Covered Item, Coverage, Employee, Policy, Claim, Claimant, 3rd Party Payee

### 8. Claim Transactions

#### 8.1 Transaction Task Types
- Open claim, reopen claim, close claim
- Set reserve, reset reserve, close reserve
- Set salvage estimate, receive salvage payment
- Adjuster inspection, adjuster interview
- Open lawsuit, close lawsuit
- Make payment, receive payment
- Subrogate claim

#### 8.2 Claim Transaction Fact Table (Figure 16-8)
- **Dimensions:**
  - Date Dimension (2 views for roles: claim transaction date, claim effective date)
  - Policyholder Dimension
  - Coverage Dimension
  - Claimant Dimension (typically individual; dirty dimension -- hard to match across claims)
  - Claim Transaction Type Dimension
  - Claim Dimension
  - Employee Dimension (2 views for roles)
  - Covered Item Dimension
  - 3rd Party Payee Dimension (individual or commercial entity; dirty dimension)
  - Claim Profile Dimension
- **Keys:**
  - Claim Transaction Date Key (FK)
  - Claim Transaction Effective Date Key (FK)
  - Policyholder Key (FK)
  - Claim Transaction Employee Key (FK)
  - Agent Key (FK)
  - Coverage Key (FK)
  - Covered Item Key (FK)
  - Claimant Key (FK)
  - 3rd Party Payee Key (FK)
  - Claim Transaction Type Key (FK)
  - Claim Profile Key (FK)
  - Claim Key (FK)
- **Degenerate dimensions:**
  - Policy Number (DD)
  - Claim Transaction Number (DD)
- **Fact:**
  - Claim Transaction Dollar Amount

#### 8.3 Transaction vs. Profile Junk Dimensions
- Many low-cardinality indicators/descriptions related to claims
- High-cardinality descriptors (loss address, narrative) -> claim dimension
- Low-cardinality codified data (loss reporting method, catastrophic event indicator) -> **Claim Profile Dimension** (junk dimension)
  - One row per unique combination of profile attributes
  - Faster grouping/filtering than embedding in claim dimension

### 9. Claim Accumulating Snapshot (Figure 16-9)

#### 9.1 Schema
- **Grain:** one row per claim; created when claim opened, updated throughout life until closed
- **Dimensions:**
  - Date Dimension (7 views for roles)
  - Policyholder Dimension
  - Coverage Dimension
  - Claimant Dimension
  - Claim Profile Dimension
  - Employee Dimension (2 views for roles: Claim Supervisor, Agent)
  - Covered Item Dimension
  - Claim Status Dimension (open, closed, reopened)
  - Claim Dimension
- **Date foreign keys (7 role-playing dates):**
  - Claim Open Date Key (FK)
  - Claim Loss Date Key (FK)
  - Claim Estimate Date Key (FK)
  - Claim 1st Payment Date Key (FK)
  - Claim Most Recent Payment Date Key (FK)
  - Claim Subrogation Date Key (FK)
  - Claim Close Date Key (FK)
- **Degenerate dimension:** Policy Number (DD)
- **Accumulating dollar facts:**
  - Original Reserve Dollar Amount
  - Estimate Dollar Amount
  - Current Reserve to Date Dollar Amount
  - Claim Paid to Date Dollar Amount
  - Salvage Collected to Date Dollar Amount
  - Subro Payment Collected to Date Dollar Amount
- **Lag metrics (duration between milestones):**
  - Claim Loss to Open Lag
  - Claim Open to Estimate Lag
  - Claim Open to 1st Payment Lag
  - Claim Open to Subrogation Lag
  - Claim Open to Closed Lag
- **Count:**
  - Number of Claim Transactions

#### 9.2 Accumulating Snapshot for Complex Workflows
- Standard accumulating snapshots: 5-10 well-established milestone dates
- Complex/unpredictable workflows: definite start/end, but numerous and unstable intermediate milestones
- Approach: identify key dates linking to role-playing date dimensions (start, end, commonly occurring critical milestones)
- Lag optimization: with N milestones, N*(N-1)/2 possible lags; store only N-1 lags from anchor milestone A; derive others by subtraction (e.g., B-to-C = A-to-C minus A-to-B)
- Null handling: if one milestone event never occurred, derived lag is null

#### 9.3 Timespan Accumulating Snapshot
- Standard accumulating snapshot obliterates intermediate state history
- Claims move through states: opened, denied, closed, disputed, reopened, closed again
- Solution: add effective/expiration dates + current flag to accumulating snapshot
  - Instead of destructive update, insert new row preserving prior state for a time span
  - Additional columns: Snapshot start date, Snapshot end date, Snapshot current flag
- View filtering on current flag satisfies most users
- Minority can filter on arbitrary historical date using start/end dates
- More complex to maintain but preserves full state evolution history

#### 9.4 Periodic Instead of Accumulating Snapshot
- For long-lived claims (long-term disability, bodily injury with multiyear lifespan)
- **Grain:** one row per active claim per regular interval (e.g., monthly)
- **Facts:** additive numeric measures for the period
  - Amount claimed
  - Amount paid
  - Change in reserve

### 10. Policy/Claim Consolidated Periodic Snapshot (Figure 16-10)
- Brings premium revenue and claim loss metrics together in single fact table
- **Grain:** lowest common granularity across both processes
- **Dimensions:**
  - Month End Date Dimension
  - Policyholder Dimension
  - Coverage Dimension
  - Covered Item Dimension
  - Agent Dimension
  - Policy Status Dimension
  - Claim Status Dimension
- **Degenerate dimension:** Policy Number (DD)
- **Facts:**
  - Written Premium Revenue Dollar Amount
  - Earned Premium Revenue Dollar Amount
  - Claim Paid Dollar Amount
  - Claim Collected Dollar Amount
- Consolidated fact table: combines data from multiple business processes
- Best developed after separate atomic dimensional models are delivered

### 11. Factless Accident Events (Figure 16-11)
- Factless fact table for automobile accident involvements
- Records many-to-many correlations between loss parties and loss items (people and vehicles)
- **Dimensions:**
  - Claim Loss Date Dimension
  - Policyholder Dimension
  - Coverage Dimension
  - Covered Item Dimension
  - Claimant Dimension
  - Loss Party Dimension (individuals involved: passengers, witnesses, legal representation)
  - Loss Party Role Dimension
  - Claim Profile Dimension
- **Degenerate dimensions:**
  - Claim Number (DD)
  - Policy Number (DD)
- **Fact:**
  - Accident Involvement Count (always = 1, for counting/aggregation)
- Alternative: use claimant group and loss party group bridge tables as multivalued dimensions (preserves one-record-per-accident-claim grain)

### 12. Detailed Implementation Bus Matrix (Figure 16-7)
- Expands high-level bus matrix to fact table / OLAP cube level
- Three groups with granularity, facts, and dimension columns:

#### 12.1 Policy Transactions
| Fact Table | Granularity | Facts |
|---|---|---|
| Corporate Policy Transactions | 1 row per policy transaction | Policy Transaction Amount |
| Auto Policy Transactions | 1 row per auto policy transaction | Policy Transaction Amount |
| Home Policy Transactions | 1 row per home policy transaction | Policy Transaction Amount |

#### 12.2 Policy Premium Snapshot
| Fact Table | Granularity | Facts |
|---|---|---|
| Corporate Policy Premiums | 1 row per policy, covered item, coverage per month | Written + Earned Premium Revenue |
| Auto Policy Premiums | 1 row per auto policy, covered item, coverage per month | Written + Earned Premium Revenue |
| Home Policy Premiums | 1 row per home policy, covered item, coverage per month | Written + Earned Premium Revenue |

#### 12.3 Claim Events
| Fact Table | Granularity | Facts |
|---|---|---|
| Claim Transactions | 1 row per claim task transaction | Claim Transaction Amount |
| Claim Workflow (accumulating snapshot) | 1 row per claim | Original Reserve, Estimate, Current Reserve, Claim Paid, Salvage Collected, Subro Collected; Lags (Loss to Open, Open to Estimate, Open to 1st Payment, Open to Subro, Open to Closed); # of Transactions |
| Accident Involvements | 1 row per loss party and affiliation on an auto claim | Accident Involvement Count |

### 13. Common Dimensional Modeling Mistakes to Avoid (Ranked 10 to 1)

#### Mistake 10: Place Text Attributes in a Fact Table
- Numeric measurements -> fact table
- Descriptive textual attributes -> dimension tables
- Pseudo-numeric items: place in fact table if used in calculations, dimension table if used for filtering/labeling
- Comment fields must move to dimensions

#### Mistake 9: Limit Verbose Descriptors to Save Space
- Dimension tables are geometrically smaller than fact tables
- 100 MB dimension is insignificant next to fact table 100-1000x larger
- Supply maximum descriptive context in every dimension
- Textual attributes provide browsing, constraining, filtering, row/column headers

#### Mistake 8: Split Hierarchies into Multiple Dimensions
- Fixed-depth hierarchy belongs in a single flat dimension table
- Products -> brands -> categories: all in product dimension row
- Resist snowflaking into progressively smaller subdimension tables
- Multiple rollups can coexist in same dimension if at lowest grain and uniquely labeled

#### Mistake 7: Ignore the Need to Track Dimension Changes
- Business users want to understand impact of attribute changes
- Don't rely on Type 1 exclusively
- Use Type 2 for accurate change tracking
- Split rapidly changing attributes into mini-dimensions

#### Mistake 6: Solve All Performance Problems with More Hardware
- Aggregates/derived summary tables are cost-effective for query performance
- Balanced approach: aggregates, partitioning, indices, query-efficient DBMS, memory, CPU, parallelism

#### Mistake 5: Use Operational Keys to Join Dimensions and Facts
- Dimension keys should be simple integer surrogate keys (1..N)
- Never use operational/intelligent keys or composite keys (operational key + effective date)
- Date dimension is the sole exception

#### Mistake 4: Neglect to Declare and Comply with the Fact Grain
- Begin with business process, then declare exact granularity
- Build at most atomic, granular level
- Surround with dimensions true to that grain
- Never add summary/total rows to a fact table (causes overcounting across dimensions)
- Each different measurement grain demands its own fact table

#### Mistake 3: Use a Report to Design the Dimensional Model
- Dimensional model is a model of a measurement process, not a report
- Numeric measurements form basis of fact tables
- Dimensions are context/circumstances of measurement
- Don't build hundreds of report-centric fact tables (same data extracted many times)
- Focus on atomic measurement processes with performance-enhancing aggregations

#### Mistake 2: Expect Users to Query Normalized Atomic Data
- Lowest level data is most dimensional and should be foundation
- Don't build with aggregated data and expect drill-down to 3NF
- Normalized models belong in ETL kitchen, not in front of business users

#### Mistake 1: Fail to Conform Facts and Dimensions
- Two mistakes combined (most dangerous):
  - **Conforming facts:** If same metric (e.g., "revenue") appears in multiple fact tables from different sources, technical definitions must exactly match; otherwise use different names
  - **Conforming dimensions:** If two+ fact tables share a dimension, those dimensions must be identical or carefully chosen subsets; enables drill-across queries; constraints and row headers match at data level
- Conformed dimensions are "the secret sauce" for:
  - Building distributed DW/BI environments
  - Adding unexpected new data sources
  - Making incompatible technologies work together
  - Faster delivery of value to business community


# Kimball Data Warehouse Toolkit 3e -- Chapters 17-18 Taxonomy

Source: *The Data Warehouse Toolkit, Third Edition* by Ralph Kimball and Margy Ross

---
```

### chapter-17-kimball-dw-bi-lifecycle-overview-pp-403-427

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-17-kimball-dw-bi-lifecycle-overview-pp-403-427
Hash: 12e73f871213

```
Program/Project Planning
        |
        v (two-way arrow)
Business Requirements Definition
        |
        +-------------------------------+-------------------------------+
        |                               |                               |
        v                               v                               v
  [TECHNOLOGY TRACK]            [DATA TRACK]                [BI APPLICATIONS TRACK]
        |                               |                               |
  Technical Architecture       Dimensional Modeling             BI Application
       Design                          |                          Design
        |                               |                               |
        v                               v                               v
  Product Selection            Physical Design                BI Application
   & Installation                      |                        Development
        |                               |                               |
        +--------->  ETL Design & Development  <--------+               |
                            |                                           |
                            +-------------------------------------------+
                            |
                            v
                        Deployment -----> Maintenance
                            |                  |
                            v                  v
                          Growth          (loops back to
                                         Program/Project Planning)

    [========= Program/Project Management (spans entire lifecycle) =========]
```

### chapter-18-dimensional-modeling-process-and-tasks-pp-429-441

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-18-dimensional-modeling-process-and-tasks-pp-429-441
Hash: 66248dfa5861

```
+----------------------------+
  |        Preparation         |
  +----------------------------+
              |
              v
  +----------------------------+
  | High Level Dimensional     |
  |         Model              |
  +----------------------------+
              |
              v
  +----------------------------+
  | Detailed Dimensional       |  <---+
  |   Model Development        |      |  Iterate
  +----------------------------+      |  and
              |                       |  Test
              +--->-------------------+
              |
              v
  +----------------------------+
  | Model Review and           |
  |      Validation            |
  +----------------------------+
              |
              v
  +----------------------------+
  | Final Design               |
  |    Documentation           |
  +----------------------------+
```

### chapter-19-etl-subsystems-and-techniques-pp-443-496

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-19-etl-subsystems-and-techniques-pp-443-496
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

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-20-etl-system-design-and-development-process-pp-497-
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

URL: https://local.taxonomy/kimball-dw-toolkit/chapter-21-big-data-analytics-pp-527-542
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
