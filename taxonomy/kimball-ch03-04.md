---
source: Kimball & Ross, *The Data Warehouse Toolkit*, 3rd Edition, pp. 69-139
domain: local
crawled_at: 2026-03-31T21:40:31Z
index_hash: 504f64a4559a
page_count: 2
---

# Kimball Data Warehouse Toolkit 3e -- Taxonomy: Chapters 3-4

## Pages

### chapter-3-retail-sales-pp-69-110

URL: https://local.taxonomy/kimball-ch03-04/chapter-3-retail-sales-pp-69-110
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

URL: https://local.taxonomy/kimball-ch03-04/chapter-4-inventory-pp-111-139
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
