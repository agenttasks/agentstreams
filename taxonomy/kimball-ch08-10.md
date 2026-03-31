---
source: Kimball & Ross, *The Data Warehouse Toolkit*, 3rd Edition, pp. 229-296
domain: local
crawled_at: 2026-03-31T21:40:31Z
index_hash: b15d2530813c
page_count: 4
---

# Kimball Data Warehouse Toolkit 3e -- Taxonomy Tree: Chapters 8-10

## Pages

### chapter-8-customer-relationship-management-pp-229-262

URL: https://local.taxonomy/kimball-ch08-10/chapter-8-customer-relationship-management-pp-229-262
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

URL: https://local.taxonomy/kimball-ch08-10/chapter-9-human-resources-management-pp-263-279
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

URL: https://local.taxonomy/kimball-ch08-10/chapter-10-financial-services-pp-281-296
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

URL: https://local.taxonomy/kimball-ch08-10/cross-chapter-concept-index
Hash: ed0e094bac33

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
```
