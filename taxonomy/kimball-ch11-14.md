---
source: *The Data Warehouse Toolkit, 3rd Edition* by Ralph Kimball and Margy Ross
domain: local
crawled_at: 2026-03-31T21:40:31Z
index_hash: 5652a6473d9a
page_count: 5
---

# Kimball Data Warehouse Toolkit 3e -- Chapters 11-14 Taxonomy

## Pages

### chapter-11-telecommunications-pp-297-310

URL: https://local.taxonomy/kimball-ch11-14/chapter-11-telecommunications-pp-297-310
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

URL: https://local.taxonomy/kimball-ch11-14/chapter-12-transportation-pp-311-324
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

URL: https://local.taxonomy/kimball-ch11-14/chapter-13-education-pp-325-337
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

URL: https://local.taxonomy/kimball-ch11-14/chapter-14-healthcare-pp-339-352
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

URL: https://local.taxonomy/kimball-ch11-14/cross-chapter-pattern-index
Hash: 4b0b34684996

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
```
