---
source: Kimball & Ross, *The Data Warehouse Toolkit*, 3rd Edition (2013)
domain: local
crawled_at: 2026-03-31T21:40:31Z
index_hash: 34d0853c3e1f
page_count: 4
---

# Kimball Data Warehouse Toolkit 3e -- Taxonomy: Chapters 5-7

## Pages

### chapter-5-procurement-pp-141-165

URL: https://local.taxonomy/kimball-ch05-07/chapter-5-procurement-pp-141-165
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

URL: https://local.taxonomy/kimball-ch05-07/chapter-6-order-management-pp-167-199
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

URL: https://local.taxonomy/kimball-ch05-07/chapter-7-accounting-pp-201-227
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

URL: https://local.taxonomy/kimball-ch05-07/cross-chapter-design-pattern-summary
Hash: 8e4280605b7e

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
```
