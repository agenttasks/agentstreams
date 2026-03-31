---
source: Kimball, Ross. *The Data Warehouse Toolkit*, 3rd Edition (Wiley, 2013).
domain: local
crawled_at: 2026-03-31T21:40:31Z
index_hash: c81780859341
page_count: 2
---

# Kimball Data Warehouse Toolkit 3e -- Taxonomy Tree (Chapters 1-2)

## Pages

### chapter-1-data-warehousing-business-intelligence-and-dimensi

URL: https://local.taxonomy/kimball-ch01-02/chapter-1-data-warehousing-business-intelligence-and-dimensi
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

URL: https://local.taxonomy/kimball-ch01-02/chapter-2-kimball-dimensional-modeling-techniques-overview-p
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
