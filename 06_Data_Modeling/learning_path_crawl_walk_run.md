# Data Engineering Learning Path: Crawl, Walk, Run 🎯

## How to Use This Guide

This guide is structured in three progressive levels:
- **🐛 CRAWL**: Foundational concepts - understand the basics
- **🚶 WALK**: Intermediate application - connect the dots
- **🏃 RUN**: Advanced mastery - speak confidently in interviews

Each level has:
1. **Learning objectives**
2. **Key concepts to master**
3. **Practice questions** (alternating difficulty)
4. **Interview talking points**

---

## 🐛 LEVEL 1: CRAWL (Foundations)

### Learning Objectives
- [ ] Understand what each component is
- [ ] Know the basic differences between systems
- [ ] Recognize common terminology

### Key Concepts

#### 1. Database vs Data Warehouse vs Data Lake

**Database (OLTP)**
- **What:** Stores data for applications to run
- **Example:** MySQL storing customer orders for an e-commerce site
- **Key phrase:** "Optimized for transactions - INSERT, UPDATE, DELETE"

**Data Warehouse (OLAP)**
- **What:** Stores data for analysis and reporting
- **Example:** Snowflake storing historical sales data for business intelligence
- **Key phrase:** "Optimized for analytics - SELECT, aggregate, JOIN"

**Data Lake**
- **What:** Stores ALL data in raw format
- **Example:** AWS S3 storing images, logs, CSV files, everything
- **Key phrase:** "Store now, decide how to use later"

#### 2. ETL vs ELT

**ETL (Traditional)**
- Extract → Transform → Load
- "Clean the data BEFORE putting it in the warehouse"

**ELT (Modern)**
- Extract → Load → Transform
- "Put raw data in the warehouse, THEN clean it"

---

### 🎯 CRAWL Practice Questions (Alternating)

**Question 1 (Easy):** What does OLTP stand for?
<details>
<summary>Answer</summary>
Online Transaction Processing - handles day-to-day transactions in applications
</details>

**Question 2 (Medium):** Why would you choose a data lake over a data warehouse?
<details>
<summary>Answer</summary>
Data lake when you:
- Have unstructured data (images, videos, logs)
- Don't know how you'll use the data yet
- Need low-cost storage
- Want flexibility
</details>

**Question 3 (Easy):** In ETL, when does transformation happen?
<details>
<summary>Answer</summary>
BEFORE loading into the warehouse (Extract → Transform → Load)
</details>

**Question 4 (Medium):** What's the main advantage of ELT over ETL?
<details>
<summary>Answer</summary>
Flexibility - you can re-transform data without re-extracting from sources. Also leverages the warehouse's compute power.
</details>

**Question 5 (Easy):** What type of data does a relational database store?
<details>
<summary>Answer</summary>
Structured data in tables with rows and columns
</details>

---

### 🗣️ CRAWL Interview Talking Points

**When asked "What's the difference between a database and a data warehouse?"**

> "A database, specifically an OLTP database, is optimized for running applications - it handles lots of INSERT, UPDATE, and DELETE operations quickly. Think of it like the engine that powers a website. 
>
> A data warehouse, on the other hand, is optimized for analytics - it's designed for complex SELECT queries and aggregations. It's where you store historical data from multiple sources to answer business questions like 'What were our sales last quarter?'"

---

## 🚶 LEVEL 2: WALK (Intermediate)

### Learning Objectives
- [ ] Understand how components work together
- [ ] Explain the data flow through a pipeline
- [ ] Know when to use each technology

### Key Concepts

#### 1. Data Warehouse Layers (Bronze, Silver, Gold)

**Bronze (Staging/Raw)**
- Exact copy from source
- No transformations
- Example: `staging.raw_orders`

**Silver (Integration/Cleaned)**
- Deduplicated
- Standardized formats
- Data quality checks
- Example: `integration.orders_cleaned`

**Gold (Presentation/Business-Ready)**
- Star schema (fact + dimensions)
- Pre-aggregated metrics
- Business-friendly names
- Example: `presentation.fact_sales`, `presentation.dim_customer`

#### 2. Star Schema Components

**Fact Table**
- Contains measurements (sales amount, quantity, profit)
- Has foreign keys to dimensions
- Example: `fact_sales(sale_id, customer_key, product_key, date_key, amount)`

**Dimension Tables**
- Contains context (who, what, when, where)
- Has descriptive attributes
- Example: `dim_customer(customer_key, name, city, segment)`

#### 3. Common Metrics

**Additive:** Can sum across all dimensions (Revenue, Quantity)
**Semi-Additive:** Can sum across some dimensions (Account balance - NOT across time)
**Non-Additive:** Cannot sum (Averages, Ratios, Percentages)

---

### 🎯 WALK Practice Questions (Alternating)

**Question 1 (Medium):** Explain the data flow from source to BI tool.
<details>
<summary>Answer</summary>
Source Database → ETL/ELT Pipeline → Data Lake (optional) → Data Warehouse (Bronze → Silver → Gold) → Data Mart (optional) → BI Tool (Tableau, Power BI)
</details>

**Question 2 (Hard):** Why do we need three layers (Bronze, Silver, Gold) in a data warehouse?
<details>
<summary>Answer</summary>
- **Bronze:** Preserves raw data for auditing and reprocessing
- **Silver:** Provides clean, standardized data for multiple use cases
- **Gold:** Optimized for specific business questions (star schema)

This separation allows you to fix data quality issues in Silver without re-extracting from sources, and create multiple Gold layers for different departments.
</details>

**Question 3 (Medium):** What's the difference between a fact table and a dimension table?
<details>
<summary>Answer</summary>
- **Fact table:** Contains MEASUREMENTS (numbers you want to analyze) - sales amount, quantity, profit
- **Dimension table:** Contains CONTEXT (who, what, when, where) - customer name, product category, date

Fact tables have foreign keys pointing to dimension tables.
</details>

**Question 4 (Hard):** When would you use a data mart instead of giving users direct access to the data warehouse?
<details>
<summary>Answer</summary>
Use a data mart when:
- Department needs faster queries (smaller, optimized dataset)
- Need to control what data a department can see (security)
- Want to pre-aggregate common metrics
- Department has specific business logic that doesn't apply company-wide

Example: Sales team only needs sales data, not HR data.
</details>

**Question 5 (Medium):** What's the grain of a fact table?
<details>
<summary>Answer</summary>
The grain is the level of detail - what one row represents.

Example: "One row = one product sold per transaction" (line-item grain)
vs "One row = one entire order" (order grain)

The grain determines what questions you can answer.
</details>

---

### 🗣️ WALK Interview Talking Points

**When asked "Walk me through how you'd design a data pipeline for sales data"**

> "I'd start by understanding the business questions we need to answer. Then I'd design a pipeline like this:
>
> 1. **Source:** Extract from the OLTP database (MySQL) where orders are stored
> 2. **Ingestion:** Use an ELT tool like Fivetran to load raw data into our data warehouse
> 3. **Bronze Layer:** Land the raw data exactly as-is for auditing
> 4. **Silver Layer:** Clean the data - remove duplicates, standardize formats, handle nulls
> 5. **Gold Layer:** Transform into a star schema with:
>    - `fact_sales` (sale_id, customer_key, product_key, date_key, amount, quantity)
>    - `dim_customer`, `dim_product`, `dim_date`
> 6. **Serving:** Connect Tableau to the Gold layer for dashboards
>
> This approach gives us flexibility to re-transform if business logic changes, and the star schema makes queries fast and easy for analysts."

---

## 🏃 LEVEL 3: RUN (Advanced Mastery)

### Learning Objectives
- [ ] Explain trade-offs between different approaches
- [ ] Design systems for specific use cases
- [ ] Speak confidently about best practices

### Key Concepts

#### 1. When to Use What

**Use OLTP Database when:**
- Running an application (website, mobile app)
- Need ACID transactions
- Frequent writes (INSERT, UPDATE, DELETE)

**Use Data Warehouse when:**
- Need to analyze historical data
- Combine data from multiple sources
- Run complex analytical queries
- Generate reports and dashboards

**Use Data Lake when:**
- Have unstructured data (images, videos, logs)
- Don't know how you'll use the data yet
- Need to store massive amounts of data cheaply
- Data science/ML use cases

**Use NoSQL when:**
- Schema changes frequently
- Need horizontal scaling
- High-speed reads/writes
- Specific use cases (graphs, documents, key-value)

#### 2. Design Decisions

**ETL vs ELT:**
- **ETL:** Limited warehouse compute, data privacy concerns, on-premise
- **ELT:** Cloud warehouse (Snowflake, BigQuery), need flexibility, modern approach

**Batch vs Streaming:**
- **Batch:** Daily/hourly updates acceptable, large volumes, cost-effective
- **Streaming:** Real-time requirements, fraud detection, live dashboards

**Star Schema vs Snowflake Schema:**
- **Star:** Denormalized, faster queries, more storage
- **Snowflake:** Normalized dimensions, less storage, more complex queries

#### 3. Best Practices

**Data Modeling:**
- Always use surrogate keys (not natural keys)
- Define grain explicitly
- Use Type 2 SCD for important historical changes
- Pre-calculate common metrics in fact tables

**Performance:**
- Index all foreign keys
- Partition large tables by date
- Use materialized views for complex aggregations
- Monitor query performance

---

### 🎯 RUN Practice Questions (Alternating)

**Question 1 (Hard):** A company has 10 TB of customer clickstream data. They want real-time fraud detection AND historical analysis. Design the architecture.
<details>
<summary>Answer</summary>

**Architecture:**
1. **Streaming Ingestion:** Kafka captures clickstream events in real-time
2. **Dual Path:**
   - **Real-time:** Kafka → Streaming processor (Flink/Spark Streaming) → Fraud detection model → Alert system
   - **Batch:** Kafka → Data Lake (S3) → Nightly ETL → Data Warehouse (Snowflake)
3. **Data Warehouse Layers:**
   - Bronze: Raw clickstream data
   - Silver: Cleaned, sessionized data
   - Gold: Star schema with fact_clicks, dim_user, dim_page
4. **Serving:**
   - Real-time dashboard (fraud alerts)
   - Historical analysis (Tableau connected to Gold layer)

**Why this design:**
- Kafka handles high-volume streaming
- Data Lake stores raw data cheaply
- Streaming path for real-time needs
- Batch path for historical analysis
- Separation of concerns
</details>

**Question 2 (Expert):** You're seeing slow query performance on a 1 billion row fact table. Walk through your debugging process.
<details>
<summary>Answer</summary>

**Debugging Process:**

1. **Check Query Plan:**
   - Look for full table scans
   - Identify missing indexes
   - Check JOIN order

2. **Verify Indexes:**
   - All foreign keys indexed?
   - Commonly filtered columns indexed?
   - Consider composite indexes for common query patterns

3. **Check Partitioning:**
   - Is table partitioned by date?
   - Are queries using partition pruning?

4. **Review Data Model:**
   - Is grain too detailed? (Can we pre-aggregate?)
   - Are we JOINing too many dimensions?
   - Should we denormalize some dimensions?

5. **Consider Materialized Views:**
   - For common aggregations
   - Pre-compute expensive calculations

6. **Warehouse-Specific Optimizations:**
   - Snowflake: Clustering keys
   - BigQuery: Partitioning and clustering
   - Redshift: Distribution and sort keys

7. **Query Optimization:**
   - Push down filters
   - Reduce columns selected
   - Use CTEs for readability and optimization
</details>

**Question 3 (Hard):** Explain the trade-offs between Type 1, Type 2, and Type 3 Slowly Changing Dimensions.
<details>
<summary>Answer</summary>

**Type 1 (Overwrite):**
- **Pros:** Simple, no extra storage
- **Cons:** Lose history
- **Use when:** Correcting errors, unimportant changes

**Type 2 (Add Row):**
- **Pros:** Full history, accurate reporting
- **Cons:** More storage, more complex queries
- **Use when:** Need to track changes over time (price changes, customer segments)
- **Best practice:** Use this by default for important attributes

**Type 3 (Add Column):**
- **Pros:** Simple queries, one row per entity
- **Cons:** Limited history (only 1 previous value), inflexible
- **Use when:** Rarely - Type 2 is almost always better
- **Avoid:** Hard to extend, loses history after 2 changes

**Recommendation:** Default to Type 2 for any attribute that changes and you care about history. Use Type 1 only for corrections.
</details>

**Question 4 (Expert):** A startup is choosing between building on Snowflake vs building a data lake on S3 + Spark. What factors should they consider?
<details>
<summary>Answer</summary>

**Snowflake (Data Warehouse):**
- **Pros:**
  - Managed service (less ops overhead)
  - SQL interface (easier for analysts)
  - Auto-scaling
  - Great for structured data
- **Cons:**
  - Higher cost
  - Less flexible for ML/data science
  - Vendor lock-in
- **Choose when:** Team is SQL-focused, need BI/reporting, want managed service

**S3 + Spark (Data Lake):**
- **Pros:**
  - Lower storage cost
  - Flexible (all data types)
  - Great for ML/data science
  - Open-source ecosystem
- **Cons:**
  - More ops overhead
  - Need Spark expertise
  - Slower for ad-hoc SQL queries
- **Choose when:** Heavy ML use cases, unstructured data, have engineering resources

**Best of Both Worlds:**
- Use Data Lake (S3) for raw storage
- Use Snowflake for curated analytics
- This is the modern "Data Lakehouse" pattern
</details>

**Question 5 (Hard):** How would you explain the value of a data warehouse to a non-technical executive?
<details>
<summary>Answer</summary>

> "Right now, your data is scattered across multiple systems - your sales data is in one database, customer data in another, marketing data in a third system. When you want to answer a question like 'Which customers are most profitable?' you have to manually pull data from all these systems and combine it in Excel.
>
> A data warehouse solves this by bringing all your data together in one place, already cleaned and organized. It's like having a single source of truth for your business.
>
> The benefits:
> 1. **Faster decisions:** Instead of waiting days for a report, analysts can answer questions in minutes
> 2. **Better insights:** We can see patterns across all your data, not just one system
> 3. **Historical analysis:** We keep years of data so you can see trends over time
> 4. **Self-service:** Business users can create their own reports without IT help
>
> Think of it as the difference between having files scattered across your desk vs having them organized in a filing cabinet where anyone can find what they need."
</details>

---

### 🗣️ RUN Interview Talking Points

**When asked "Tell me about a data pipeline you've designed"**

> "I designed an end-to-end pipeline for [company] to analyze customer behavior across web and mobile.
>
> **Challenge:** Data was in 3 different systems - web clicks in MySQL, mobile events in MongoDB, and customer data in Salesforce.
>
> **Solution:**
> - Used Fivetran to extract data from all three sources
> - Landed raw data in our Data Lake (S3) for archival
> - Built a 3-layer data warehouse in Snowflake:
>   - Bronze: Raw data as-is
>   - Silver: Cleaned, deduplicated, standardized timestamps
>   - Gold: Star schema with fact_events and dimensions for users, pages, and devices
> - Created a Marketing data mart with pre-aggregated metrics
> - Connected Tableau for dashboards
>
> **Impact:**
> - Reduced report generation time from 2 days to 5 minutes
> - Marketing team could self-serve analytics
> - Discovered that mobile users had 30% higher conversion - led to mobile-first strategy
>
> **Technical decisions:**
> - Chose ELT over ETL because Snowflake could handle transformations faster
> - Used Type 2 SCD for user segments to track changes over time
> - Partitioned fact table by date for query performance
> - Implemented dbt for transformation logic with version control"

---

## 📚 Study Plan

### Week 1: CRAWL
- Day 1-2: Read all CRAWL concepts
- Day 3-4: Answer all CRAWL questions
- Day 5: Practice explaining concepts out loud
- Day 6-7: Review and repeat

### Week 2: WALK
- Day 1-3: Read all WALK concepts
- Day 4-5: Answer all WALK questions
- Day 6: Draw diagrams of data flows
- Day 7: Practice interview talking points

### Week 3: RUN
- Day 1-3: Read all RUN concepts
- Day 4-5: Answer all RUN questions
- Day 6: Design your own architecture for a use case
- Day 7: Mock interview practice

---

## 🎯 Interview Readiness Checklist

### Can you explain...
- [ ] The difference between OLTP and OLAP?
- [ ] When to use ETL vs ELT?
- [ ] What a star schema is and why it's useful?
- [ ] The Bronze-Silver-Gold pattern?
- [ ] The difference between a data lake and data warehouse?
- [ ] How metrics are calculated from fact tables?
- [ ] What a data mart is and when to use one?
- [ ] The different types of NoSQL databases?
- [ ] Slowly Changing Dimensions (Types 1, 2, 3)?
- [ ] The complete data pipeline from source to BI tool?

### Can you design...
- [ ] A star schema for a given business scenario?
- [ ] An end-to-end data pipeline?
- [ ] A solution for real-time + historical analytics?
- [ ] A data warehouse layer architecture?

### Can you discuss trade-offs between...
- [ ] Different database types?
- [ ] Batch vs streaming ingestion?
- [ ] Star schema vs snowflake schema?
- [ ] Building on cloud warehouse vs data lake?

---

## 💡 Final Tips

1. **Use analogies:** "A data warehouse is like a library - organized and easy to find things. A data lake is like a storage unit - everything's there but you need to dig."

2. **Be specific:** Don't just say "I used Snowflake" - say "I chose Snowflake over Redshift because of its separation of storage and compute, which gave us better cost control."

3. **Show impact:** Always tie technical decisions to business outcomes - "This reduced query time by 80%, enabling real-time dashboards."

4. **Ask clarifying questions:** In interviews, ask about scale, latency requirements, team skills - shows you think about trade-offs.

5. **Practice out loud:** Explaining concepts verbally is different from reading them. Practice with a friend or record yourself.

Good luck! 🚀
