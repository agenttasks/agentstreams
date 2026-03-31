---
source: *The Data Warehouse Toolkit, Third Edition* by Ralph Kimball and Margy Ross
domain: local
crawled_at: 2026-03-31T21:40:31Z
index_hash: 03b6e8f5d313
page_count: 2
---

# Kimball Data Warehouse Toolkit 3e -- Chapters 17-18 Taxonomy

## Pages

### chapter-17-kimball-dw-bi-lifecycle-overview-pp-403-427

URL: https://local.taxonomy/kimball-ch17-18/chapter-17-kimball-dw-bi-lifecycle-overview-pp-403-427
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

URL: https://local.taxonomy/kimball-ch17-18/chapter-18-dimensional-modeling-process-and-tasks-pp-429-441
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
