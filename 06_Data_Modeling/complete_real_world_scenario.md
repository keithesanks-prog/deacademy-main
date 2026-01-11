# Follow Luke: A Data Engineer's Journey 👨‍💻

## Meet Luke

**Luke Martinez** is a data engineer at ShopCo, a growing e-commerce company. His task is to **build a complete analytics platform** that will transform how the business makes decisions.

Follow along as Luke takes on **the Analytics Platform Project** and develops **a self-service data warehouse** using **AWS S3, Snowflake, Fivetran, dbt, and Tableau** to engineer **real-time business insights** and deliver **actionable dashboards to business stakeholders**.

---

## 📅 Day 1: Understanding the Problem

Luke walks into a meeting with Sarah, the VP of Sales, and the executive team.

**Sarah (VP Sales):** "Luke, we have a problem. I need to know our revenue for last month, but it takes my team 2 days to pull data from different systems and combine it in Excel. By the time we have the numbers, they're already outdated."

**Mike (VP Marketing):** "Same issue here. I can't get customer segmentation data quickly enough to run targeted campaigns."

**Emma (Product Manager):** "I need to know which products are selling, but the data is scattered everywhere."

### Luke's Clarifying Questions

Luke pulls out his notebook and starts asking questions:

**Luke:** "Let me make sure I understand the requirements. Can I ask a few questions?"

**Question 1: Business Requirements**
**Luke:** "What business questions do you need to answer most frequently?"

**Sarah:** "Revenue by month, by customer segment, by product category."
**Mike:** "Customer lifetime value, churn rate, campaign ROI."
**Emma:** "Top-selling products, inventory turnover, product profitability."

**Luke notes:** *Need to support aggregations across time, customer, and product dimensions.*

**Question 2: Latency Requirements**
**Luke:** "How fresh does the data need to be? Real-time, hourly, daily?"

**Sarah:** "Daily is fine for most reports. But I'd love to see yesterday's numbers first thing in the morning."
**Mike:** "Real-time would be nice for campaign tracking, but hourly is acceptable."

**Luke notes:** *Daily batch processing is sufficient. No need for expensive real-time streaming yet.*

**Question 3: Historical Data**
**Luke:** "How far back do you need historical data?"

**Sarah:** "At least 3 years for trend analysis."
**Emma:** "5 years would be ideal for seasonality patterns."

**Luke notes:** *Need to store and query years of historical data efficiently.*

**Question 4: User Access**
**Luke:** "Who needs access to this data? Just analysts or business users too?"

**Sarah:** "I want my entire sales team to create their own reports without waiting for IT."
**Mike:** "Same for marketing. Self-service is critical."

**Luke notes:** *Need user-friendly BI tool. Tableau or Power BI.*

**Question 5: Current Pain Points**
**Luke:** "What's the biggest pain point right now?"

**Sarah:** "Manual data collection. My analyst spends 2 days per month just pulling data from different systems."
**Mike:** "Data inconsistency. Sales numbers don't match between systems."
**Emma:** "Can't trust the data. Too many errors from manual Excel work."

**Luke notes:** *Need automated pipelines and single source of truth.*

### Luke Maps the Current State

Luke spends the afternoon documenting existing systems:

**System 1: MySQL (Orders Database)**
- **Type:** OLTP (Transactional)
- **Volume:** 10,000 orders/day
- **Update frequency:** Real-time
- **Schema:** Normalized (3NF)
- **Pain point:** Slow for analytics queries

**System 2: Salesforce (Customer CRM)**
- **Type:** SaaS API
- **Volume:** 100,000 customers
- **Update frequency:** Real-time
- **Access:** API only (rate limited)
- **Pain point:** Can't join with order data easily

**System 3: MongoDB (Product Catalog)**
- **Type:** NoSQL Document Store
- **Volume:** 5,000 products
- **Schema:** Flexible (changes frequently)
- **Pain point:** Different structure than relational data

**System 4: S3 Logs (Website Clickstream)**
- **Type:** Log files
- **Volume:** 1 million events/day
- **Format:** Unstructured text
- **Pain point:** No way to query without custom scripts

### Luke Identifies the Root Causes

**Luke's analysis:**

**Root Cause 1: Data Silos**
- Data scattered across 4 different systems
- No way to join data across systems
- Each system optimized for different use case

**Root Cause 2: OLTP vs OLAP Mismatch**
- MySQL optimized for transactions (INSERT/UPDATE)
- Business needs analytics (SELECT/JOIN/GROUP BY)
- Analytical queries slow down production database

**Root Cause 3: Manual Processes**
- Analysts manually export from each system
- Manual data cleaning in Excel
- High error rate, time-consuming

**Root Cause 4: No Single Source of Truth**
- Different systems have different numbers
- No data quality checks
- Trust issues with data

**Luke's thought:** *"This is a classic case for a data warehouse. We need to centralize, clean, and optimize for analytics."*

---

## 📅 Week 1: Designing the Architecture (Decision Week)

Luke sits down with his whiteboard to design the solution. But first, he needs to make several critical decisions.

### Decision 1: Data Lake vs No Data Lake?

**Luke's thought:** *"Do we even need a Data Lake, or can we load directly to the warehouse?"*

**Option A: Direct to Warehouse (No Lake)**
```
Sources → Data Warehouse (Snowflake)
```
**Pros:**
- Simpler architecture
- Fewer components to maintain
- Lower cost

**Cons:**
- Can't store unstructured data (logs, images)
- Lose raw data if warehouse corrupted
- More expensive storage in warehouse

**Option B: Data Lake + Warehouse**
```
Sources → Data Lake (S3) → Data Warehouse (Snowflake)
```
**Pros:**
- Cheap storage for raw data ($0.023/GB vs $23/TB in Snowflake)
- Can store any data type (structured, logs, images)
- Disaster recovery (can rebuild warehouse from lake)
- Future-proof (can use for ML, data science)

**Cons:**
- More complex
- Additional component to manage

**Luke's Decision:** ✅ **Use Data Lake**

**Reasoning:**
1. We have unstructured clickstream logs
2. Storage cost savings: $50/month (lake) vs $500/month (warehouse only)
3. Disaster recovery is critical for business
4. Future ML use cases likely

**Luke documents:** *"Data Lake provides cheap, durable storage for all data types. Worth the added complexity."*

---

### Decision 2: Which Cloud Data Warehouse?

**Luke needs clarification from Finance:**

**Luke:** "What's our cloud budget for this project?"
**CFO:** "We can allocate $3,000/month for the data platform."

**Luke evaluates options:**

**Option A: Snowflake**
- **Pros:** Separate storage/compute, auto-scaling, easy to use
- **Cons:** Can get expensive with heavy usage
- **Cost:** ~$2,000/month (estimated)

**Option B: BigQuery (Google)**
- **Pros:** Pay-per-query, serverless, integrates with Google tools
- **Cons:** Vendor lock-in, less control over costs
- **Cost:** ~$1,500/month (estimated)

**Option C: Redshift (AWS)**
- **Pros:** Already using AWS (S3), good for large datasets
- **Cons:** More complex to manage, less flexible scaling
- **Cost:** ~$2,500/month (estimated)

**Luke's Decision:** ✅ **Snowflake**

**Reasoning:**
1. Separation of storage/compute = cost control
2. Auto-scaling handles variable workloads
3. Easy for business users to learn SQL
4. Within budget ($2,000 < $3,000)
5. Team has Snowflake experience

**Luke documents:** *"Snowflake offers best balance of cost, performance, and ease of use."*

---

### Decision 3: ETL vs ELT?

**Luke's thought:** *"Should we transform before or after loading to the warehouse?"*

**Option A: ETL (Transform before loading)**
```
Sources → ETL Tool (Transform) → Warehouse
```
**Pros:**
- Only load clean data
- Reduce warehouse storage
- Data privacy (can scrub PII before loading)

**Cons:**
- Need separate ETL server (more cost)
- If transformation fails, must re-extract from sources
- Less flexible (hard to change transformations)

**Option B: ELT (Load then transform)**
```
Sources → Warehouse (Load raw) → Transform in warehouse
```
**Pros:**
- Leverage warehouse's compute power
- Keep raw data (can re-transform anytime)
- More flexible (change logic without re-extracting)
- Modern best practice

**Cons:**
- Store more data in warehouse (higher cost)
- Raw data visible in warehouse

**Luke's Decision:** ✅ **ELT**

**Reasoning:**
1. Snowflake has powerful compute (faster than separate ETL server)
2. Flexibility to re-transform is valuable (business logic changes often)
3. Raw data preservation important for auditing
4. No PII concerns (internal data only)
5. Industry best practice for cloud warehouses

**Luke documents:** *"ELT leverages Snowflake's compute and provides flexibility for future changes."*

---

### Decision 4: Bronze-Silver-Gold vs Single Layer?

**Luke's thought:** *"Do we need three layers, or is that over-engineering?"*

**Option A: Single Layer (Just load and transform)**
```
Sources → Warehouse → Star Schema
```
**Pros:**
- Simpler
- Fewer tables to maintain
- Faster initial development

**Cons:**
- Lose raw data if transformation has bugs
- Can't reprocess if business logic changes
- No separation of concerns

**Option B: Two Layers (Raw + Business)**
```
Sources → Warehouse → Raw → Star Schema
```
**Pros:**
- Preserve raw data
- Can reprocess
- Simpler than three layers

**Cons:**
- No intermediate cleaned layer
- Cleaning logic mixed with business logic

**Option C: Three Layers (Bronze-Silver-Gold)**
```
Sources → Warehouse → Bronze (Raw) → Silver (Cleaned) → Gold (Star Schema)
```
**Pros:**
- Separation of concerns (raw, clean, business)
- Can reprocess any layer independently
- Clean data reusable for multiple use cases
- Industry best practice

**Cons:**
- More complex
- More storage needed
- Longer development time

**Luke's Decision:** ✅ **Three Layers (Bronze-Silver-Gold)**

**Reasoning:**
1. Bronze preserves raw data for auditing
2. Silver provides clean data for multiple use cases (not just star schema)
3. Gold optimized for specific business questions
4. Worth the complexity for long-term maintainability
5. Standard pattern in industry

**Luke documents:** *"Three-layer architecture provides flexibility and maintainability. Bronze = audit trail, Silver = clean foundation, Gold = business-optimized."*

---

### Decision 5: Data Marts - Yes or No?

**Luke asks Sarah:**

**Luke:** "How many people on your sales team will be querying the data?"
**Sarah:** "About 20 people, multiple times per day."

**Luke's thought:** *"20 users running the same queries repeatedly. Data marts could help."*

**Option A: No Data Marts (Query Gold directly)**
**Pros:**
- Simpler
- Single source of truth
- No data duplication

**Cons:**
- Slower queries (must JOIN fact + dimensions every time)
- Higher compute costs (20 users × many queries/day)

**Option B: Department-Specific Data Marts**
**Pros:**
- Pre-aggregated = faster queries
- Lower compute costs (aggregate once, query many times)
- Department-specific security

**Cons:**
- Data duplication
- More tables to maintain
- Potential for inconsistency

**Luke's Decision:** ✅ **Create Data Marts for Sales and Marketing**

**Reasoning:**
1. 20+ users querying frequently = high compute cost without marts
2. Pre-aggregation reduces query time from 0.8s to 0.1s (8x faster)
3. Department-specific marts provide better security
4. Cost savings justify maintenance overhead

**Luke documents:** *"Data marts for high-frequency use cases. Sales and Marketing teams query daily metrics repeatedly."*

---

### Decision 6: Which BI Tool?

**Luke asks the team:**

**Luke:** "Does anyone have experience with BI tools?"
**Sarah:** "We used Tableau at my previous company. I loved it."
**Mike:** "I've used Power BI. It's cheaper."

**Option A: Tableau**
- **Pros:** Powerful, user-friendly, great visualizations
- **Cons:** Expensive ($70/user/month)
- **Cost:** $70 × 30 users = $2,100/month

**Option B: Power BI**
- **Pros:** Cheaper ($10/user/month), integrates with Microsoft
- **Cons:** Less powerful, steeper learning curve
- **Cost:** $10 × 30 users = $300/month

**Option C: Looker**
- **Pros:** Code-based (LookML), version control
- **Cons:** Expensive, requires technical skills
- **Cost:** ~$3,000/month

**Luke's Decision:** ✅ **Tableau**

**Reasoning:**
1. Sarah (key stakeholder) has experience
2. User-friendly = faster adoption
3. Within budget ($2,100 < $3,000 total budget)
4. Best visualizations for executive presentations

**Luke documents:** *"Tableau for ease of use and stakeholder buy-in. Cost justified by productivity gains."*

---

### Final Architecture

Luke presents his final design to the team:

```
Sources (MySQL, Salesforce, MongoDB, S3 Logs)
    ↓
Ingestion (Fivetran - ELT tool)
    ↓
Data Lake (AWS S3 - Raw storage)
    ↓
Data Warehouse (Snowflake)
    ├─ Bronze Layer (Raw, exact copy)
    ├─ Silver Layer (Cleaned, standardized)
    └─ Gold Layer (Star Schema, business-ready)
        ↓
Data Marts (Sales, Marketing - pre-aggregated)
    ↓
BI Tool (Tableau - self-service dashboards)
```

**Total Monthly Cost Estimate:**
- Data Lake (S3): $50
- Fivetran: $500
- Snowflake: $2,000
- Tableau: $2,100
- dbt: $100
- **Total: $4,750/month**

**Luke to CFO:** "We're $1,750 over budget. Can we get approval?"
**CFO:** "What's the ROI?"
**Luke:** "We'll eliminate 2 analyst positions ($150K/year) and enable faster decisions (estimated $500K/year revenue impact). ROI is 1,300%."
**CFO:** "Approved."

**Manager:** "Great work, Luke. What's the timeline?"

**Luke:** "9 weeks to production. Week 1 is done - we have our architecture. Let's build it."

---

## 📅 Week 2: Setting Up Data Sources

Luke starts connecting to the source systems.

### Challenge 1: MySQL Orders Database

```sql
-- Luke examines the orders table
SELECT * FROM orders LIMIT 5;

order_id | customer_id | product_id | order_date          | amount | status
---------|-------------|------------|---------------------|--------|----------
1001     | 5001        | PROD123    | 2024-12-11 10:30:00 | 29.99  | completed
1002     | 5002        | PROD456    | 2024-12-11 10:35:00 | 49.99  | pending
```

**Luke's thought:** *"This is OLTP - optimized for transactions, not analytics. We need to move this to a warehouse."*

### Challenge 2: Salesforce API

Luke writes a Python script to test the Salesforce API:

```python
import requests

response = requests.get(
    'https://api.salesforce.com/customers',
    headers={'Authorization': f'Bearer {api_key}'}
)

customers = response.json()
print(f"Found {len(customers)} customers")
# Output: Found 100000 customers
```

**Luke's thought:** *"Good, the API works. Fivetran can handle this automatically."*

### Challenge 3: MongoDB Products

```javascript
// Luke queries MongoDB
db.products.findOne()

{
  "product_id": "PROD123",
  "name": "Wireless Mouse",
  "category": "Electronics",
  "price": 29.99,
  "attributes": {
    "color": "Black",
    "wireless": true
  }
}
```

**Luke's thought:** *"Flexible schema. Good for product catalog, but we'll need to flatten this for analytics."*

---

## 📅 Week 3: Ingestion with Fivetran

Luke sets up Fivetran connectors.

**Luke's setup:**

```yaml
# Fivetran configuration
connectors:
  - mysql_orders:
      sync_frequency: "1 hour"
      destination: "s3://shopco-datalake/raw/orders/"
  
  - salesforce_customers:
      sync_frequency: "15 minutes"
      destination: "s3://shopco-datalake/raw/customers/"
  
  - mongodb_products:
      sync_frequency: "1 hour"
      destination: "s3://shopco-datalake/raw/products/"
```

Luke clicks "Start Sync" and watches the data flow:

```
[10:00 AM] Extracting from MySQL... 10,000 rows
[10:05 AM] Loading to S3... Complete
[10:10 AM] Extracting from Salesforce... 100,000 rows
[10:15 AM] Loading to S3... Complete
```

**Luke's thought:** *"Beautiful. Data is flowing to the lake. Now let's get it into Snowflake."*

---

## 📅 Week 4: Building the Bronze Layer

Luke opens Snowflake and creates the Bronze schema.

```sql
-- Luke creates the Bronze layer
CREATE SCHEMA bronze;

-- Load from S3 to Snowflake
CREATE TABLE bronze.raw_orders AS
SELECT * FROM @s3_stage/raw/orders/;

-- Check the data
SELECT COUNT(*) FROM bronze.raw_orders;
-- Result: 10,000 rows
```

Luke notices something:

```sql
SELECT order_id, COUNT(*) as count
FROM bronze.raw_orders
GROUP BY order_id
HAVING count > 1;

-- Result: 50 duplicate orders!
```

**Luke's thought:** *"Duplicates. That's why we need the Silver layer to clean this up."*

---

## 📅 Week 5: Cleaning Data in Silver Layer

Luke uses dbt to create transformation models.

```sql
-- models/silver/orders_cleaned.sql
-- Luke writes his first transformation

WITH deduplicated AS (
    -- Remove duplicates
    SELECT DISTINCT *
    FROM {{ ref('raw_orders') }}
),
cleaned AS (
    SELECT
        order_id,
        customer_id,
        product_id,
        order_date,
        amount,
        UPPER(status) as status,  -- Standardize to uppercase
        CURRENT_TIMESTAMP() as loaded_at
    FROM deduplicated
    WHERE amount > 0  -- Remove invalid orders
      AND customer_id IS NOT NULL
      AND product_id IS NOT NULL
)
SELECT * FROM cleaned;
```

Luke runs the transformation:

```bash
$ dbt run --models silver.orders_cleaned

Running with dbt=1.5.0
Found 1 model
Compiling model silver.orders_cleaned
Starting execution
Completed successfully in 12.3s
```

Luke checks the results:

```sql
SELECT COUNT(*) FROM silver.orders_cleaned;
-- Result: 9,950 rows (50 duplicates removed)
```

**Luke's thought:** *"Perfect. Clean data. Now we can build the star schema."*

---

## 📅 Week 5.5: Designing the Data Model (Critical Design Phase)

Before Luke can build the Gold layer, he needs to design the star schema. This is where **business requirements directly drive technical decisions**.

### Luke's Data Modeling Process

**Luke's thought:** *"The data model is the foundation. If I get this wrong, everything built on top will be wrong. I need to design based on business questions, not just available data."*

---

### Step 1: Identify Business Questions (Requirements Gathering)

Luke schedules meetings with each stakeholder to understand their specific needs.

**Meeting with Sarah (Sales VP):**

**Luke:** "What are the top 5 questions you need to answer with data?"

**Sarah's Requirements:**
1. "What's our revenue by month, quarter, year?"
2. "Which customer segments are most profitable?"
3. "What's the average order value by customer segment?"
4. "How many repeat customers do we have?"
5. "Which products sell best to which customer segments?"

**Luke notes:** *Revenue, customer segment, time period, product category are key dimensions.*

**Meeting with Mike (Marketing VP):**

**Mike's Requirements:**
1. "What's the customer lifetime value by segment?"
2. "How has customer segmentation changed over time?" ← **Important!**
3. "Which products have the highest conversion rates?"
4. "What's the revenue impact of our campaigns?"

**Luke notes:** *Need to track customer segment changes over time. This means Type 2 SCD!*

**Meeting with Emma (Product Manager):**

**Emma's Requirements:**
1. "Which product categories are growing month-over-month?"
2. "What's the revenue by product brand?"
3. "Which products are frequently bought together?"
4. "What's the profit margin by product?"

**Luke notes:** *Product category, brand, and profitability are important. May need product hierarchy.*

---

### Step 2: Design Decision - What's the Grain?

**Luke's thought:** *"The grain is the most important decision. It determines what questions I can answer."*

**Option 1: Order-level grain**
```
One row = one order
Columns: order_id, customer_id, total_amount, order_date
```
**Pros:** Simple, matches source data
**Cons:** Can't analyze individual products, can't answer "which products sell together"

**Option 2: Order line-item grain**
```
One row = one product per order
Columns: order_id, line_item_id, customer_id, product_id, quantity, amount
```
**Pros:** Can analyze products, can see product combinations
**Cons:** More rows, slightly more complex

**Luke asks Emma:** "Do you need to see individual products per order, or just order totals?"

**Emma:** "I need to see which products are in each order. That's critical for product analysis."

**Luke's Decision:** ✅ **Order line-item grain**

**Reasoning:**
1. Emma needs product-level analysis
2. Can always aggregate up to order level
3. Can't disaggregate from order level down to products
4. Standard e-commerce pattern

**Luke documents:** *"Grain: One row = one product per order (order line item). This enables product-level analysis while still supporting order-level aggregations."*

---

### Step 3: Design Decision - Which Dimensions?

**Luke's thought:** *"Dimensions answer WHO, WHAT, WHEN, WHERE. Let me map business questions to dimensions."*

**Business Question → Dimension Mapping:**

| Business Question | Dimension Needed |
|-------------------|------------------|
| "Revenue by month?" | dim_date |
| "Revenue by customer segment?" | dim_customer |
| "Revenue by product category?" | dim_product |
| "Revenue by order status?" | dim_order_status |

**Luke identifies required dimensions:**

**Dimension 1: dim_customer**
- **Why:** All stakeholders need customer segmentation
- **Attributes:** customer_id, name, email, segment, signup_date
- **Key decision:** Type 1 or Type 2 SCD?

**Luke asks Mike:** "When a customer changes from 'Regular' to 'VIP', do you need to know what segment they were in when they made past purchases?"

**Mike:** "Absolutely! I need to see if VIP customers were profitable BEFORE becoming VIP."

**Luke's Decision:** ✅ **Type 2 SCD for customer segment**

**Reasoning:**
1. Mike needs historical segment tracking
2. Enables "segment migration" analysis
3. Standard practice for important attributes

**Dimension 2: dim_product**
- **Why:** Emma needs product analysis
- **Attributes:** product_id, name, category, brand, price
- **Key decision:** Product hierarchy?

**Luke asks Emma:** "Do you analyze by category, brand, or both?"

**Emma:** "Both. I need to see 'Electronics > Logitech' and also 'All Logitech products across categories'."

**Luke's Decision:** ✅ **Include both category and brand as separate attributes**

**Reasoning:**
1. Enables analysis by either dimension
2. Simpler than hierarchy table
3. Category and brand are independent

**Dimension 3: dim_date**
- **Why:** All time-based analysis
- **Attributes:** date, day_of_week, month, quarter, year, is_weekend
- **Key decision:** Granularity?

**Luke's Decision:** ✅ **Daily granularity**

**Reasoning:**
1. Can aggregate up to month/quarter/year
2. Can't disaggregate from month down to day
3. Standard practice

**Dimension 4: dim_order_status**
- **Why:** Track order lifecycle
- **Attributes:** status (pending, completed, cancelled, refunded)
- **Key decision:** Type 1 or Type 2 SCD?

**Luke's thought:** *"Orders change status over time. Do we need to track this?"*

**Luke asks Sarah:** "Do you need to see when orders changed from 'pending' to 'completed'?"

**Sarah:** "Not really. I just care about the final status."

**Luke's Decision:** ✅ **Type 1 SCD (overwrite)**

**Reasoning:**
1. Only current status matters for analysis
2. Saves storage
3. Simpler queries

---

### Step 4: Design Decision - Fact Table Measures

**Luke's thought:** *"What do we want to MEASURE? These become fact table columns."*

**Business Questions → Measures:**

| Business Question | Measure Needed | Type |
|-------------------|----------------|------|
| "What's our revenue?" | total_amount | Additive |
| "How many items sold?" | quantity | Additive |
| "What's the unit price?" | unit_price | Non-additive |
| "What's the discount?" | discount_amount | Additive |
| "What's the profit?" | profit_amount | Additive |

**Luke asks Emma:** "Do you have cost data to calculate profit?"

**Emma:** "Not yet, but we're getting it next quarter."

**Luke's Decision:** ✅ **Include profit_amount column, populate with NULL for now**

**Reasoning:**
1. Future-proof the model
2. Easier to populate later than to alter schema
3. Minimal cost (NULL values compress well)

---

### Step 5: Design Decision - Slowly Changing Dimensions Strategy

**Luke reviews which dimensions need SCD:**

**dim_customer:**
- **Attributes that change:** segment (Regular → VIP)
- **Business need:** Track historical segments
- **Decision:** ✅ Type 2 SCD

**Implementation:**
```sql
CREATE TABLE gold.dim_customer (
    customer_key INT PRIMARY KEY,  -- Surrogate key
    customer_id VARCHAR(50),        -- Natural key
    name VARCHAR(100),
    email VARCHAR(100),
    segment VARCHAR(50),            -- Can change (VIP, Regular)
    signup_date DATE,
    valid_from DATE,                -- SCD Type 2 fields
    valid_to DATE,                  -- SCD Type 2 fields
    is_current BOOLEAN              -- SCD Type 2 fields
);
```

**dim_product:**
- **Attributes that change:** price
- **Business need:** Track price changes? Luke asks Emma.

**Luke:** "When product prices change, do you need to see historical prices?"

**Emma:** "No, I just care about current price. Historical pricing is in the order data anyway."

**Decision:** ✅ Type 1 SCD (overwrite price)

**dim_date:**
- **Attributes that change:** None (dates don't change!)
- **Decision:** ✅ No SCD needed

**dim_order_status:**
- **Decision:** ✅ Type 1 SCD (already decided above)

---

### Step 6: Design Decision - Star Schema vs Snowflake Schema?

**Luke's thought:** *"Should I normalize dimensions or keep them denormalized?"*

**Option A: Star Schema (Denormalized)**
```
fact_orders → dim_customer (includes segment)
fact_orders → dim_product (includes category, brand)
```
**Pros:**
- Simpler queries (fewer JOINs)
- Faster performance
- Easier for business users to understand

**Cons:**
- Some data duplication
- Larger dimension tables

**Option B: Snowflake Schema (Normalized)**
```
fact_orders → dim_customer → dim_segment
fact_orders → dim_product → dim_category
                          → dim_brand
```
**Pros:**
- Less data duplication
- Smaller dimension tables

**Cons:**
- More complex queries (more JOINs)
- Slower performance
- Harder for business users

**Luke's Decision:** ✅ **Star Schema (Denormalized)**

**Reasoning:**
1. Query performance is critical (20+ users)
2. Business users need simple queries
3. Storage is cheap (data duplication not a concern)
4. Industry best practice for BI

---

### Step 7: Final Star Schema Design

Luke draws the final design on the whiteboard:

```
                dim_customer                    dim_product
          ┌─────────────────────┐         ┌─────────────────────┐
          │ customer_key (PK)   │         │ product_key (PK)    │
          │ customer_id         │         │ product_id          │
          │ name                │         │ name                │
          │ email               │         │ category            │
          │ segment             │         │ brand               │
          │ signup_date         │         │ price               │
          │ valid_from (SCD)    │         └──────────┬──────────┘
          │ valid_to (SCD)      │                    │
          │ is_current (SCD)    │                    │
          └──────────┬──────────┘                    │
                     │                               │
                     │      ┌────────────────────────┴──────────┐
                     │      │     fact_orders                   │
                     └─────→│───────────────────────────────────│
                            │ order_id                          │
                     ┌─────→│ line_item_id                      │
                     │      │ customer_key (FK)                 │
                     │      │ product_key (FK)                  │
                     │      │ date_key (FK)                     │
                     │      │ status_key (FK)                   │
                     │      │ quantity (measure)                │
                     │      │ unit_price (measure)              │
                     │      │ discount_amount (measure)         │
                     │      │ total_amount (measure)            │
                     │      │ profit_amount (measure - future)  │
                     │      └────────────┬──────────────────────┘
                     │                   │
          ┌──────────┴──────────┐       │
          │ dim_date            │       │
          │─────────────────────│       │
          │ date_key (PK)       │←──────┘
          │ date                │
          │ day_of_week         │
          │ month               │
          │ quarter             │
          │ year                │
          │ is_weekend          │
          └─────────────────────┘
                                        ┌─────────────────────┐
                                        │ dim_order_status    │
                                        │─────────────────────│
                                        │ status_key (PK)     │
                                        │ status              │
                                        │ status_category     │
                                        └──────────┬──────────┘
                                                   │
                                                   └─────────────┘
```

---

### Step 8: Validate Design Against Business Questions

Luke goes back to each stakeholder to validate the design.

**Validation with Sarah:**

**Luke:** "With this model, you can answer 'Revenue by customer segment' like this:"
```sql
SELECT 
    c.segment,
    SUM(f.total_amount) as revenue
FROM fact_orders f
JOIN dim_customer c ON f.customer_key = c.customer_key
WHERE c.is_current = TRUE
GROUP BY c.segment;
```

**Sarah:** "Perfect! And I can filter by month?"

**Luke:** "Yes:"
```sql
SELECT 
    d.month,
    c.segment,
    SUM(f.total_amount) as revenue
FROM fact_orders f
JOIN dim_customer c ON f.customer_key = c.customer_key
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2024
GROUP BY d.month, c.segment;
```

**Sarah:** "Love it! ✅"

---

**Validation with Mike:**

**Luke:** "You wanted to track segment changes over time. Here's how:"
```sql
-- Which customers moved from Regular to VIP?
SELECT 
    customer_id,
    name,
    valid_from as became_vip_date
FROM dim_customer
WHERE segment = 'VIP' 
  AND is_current = TRUE
  AND customer_id IN (
      SELECT customer_id 
      FROM dim_customer 
      WHERE segment = 'Regular'
  );
```

**Mike:** "Exactly what I need! ✅"

---

**Validation with Emma:**

**Luke:** "You wanted product category growth:"
```sql
SELECT 
    d.month,
    p.category,
    SUM(f.total_amount) as revenue,
    LAG(SUM(f.total_amount)) OVER (
        PARTITION BY p.category 
        ORDER BY d.month
    ) as prev_month_revenue,
    (SUM(f.total_amount) - LAG(SUM(f.total_amount)) OVER (...)) / 
    LAG(SUM(f.total_amount)) OVER (...) * 100 as growth_pct
FROM fact_orders f
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.month, p.category;
```

**Emma:** "Perfect! ✅"

---

### Key Takeaways from Luke's Design Process

**1. Business Questions Drive Design**
- Luke didn't design based on source data structure
- He designed based on what questions needed answering
- Every dimension and measure has a business justification

**2. Grain is Critical**
- Order line-item grain enables product analysis
- Can aggregate up, can't disaggregate down
- Grain decision affects all downstream analysis

**3. SCD Types Based on Business Need**
- Type 2 for customer segment (need history)
- Type 1 for order status (only current matters)
- Not all dimensions need SCD!

**4. Star Schema for Performance**
- Denormalized for query speed
- Simple for business users
- Industry best practice

**5. Validate Early**
- Luke validated design with stakeholders BEFORE building
- Showed example queries
- Got buy-in before coding

**Luke's thought:** *"The data model is the contract between the data and the business. Get it right, and everything else is easy. Get it wrong, and you'll be refactoring forever."*

---

## 📅 Week 6-7: Building the Gold Layer - Star Schema

Now that Luke has designed the model, he can build it.

Luke opens Snowflake and starts creating tables:

```

         dim_customer          dim_product
              ↓                     ↓
         fact_orders  ←  dim_date
              ↓
         dim_order_status
```

### Day 1: Create Date Dimension

```sql
-- Luke creates the date dimension
CREATE TABLE gold.dim_date AS
SELECT
    TO_NUMBER(TO_CHAR(date, 'YYYYMMDD')) as date_key,
    date,
    DAYNAME(date) as day_of_week,
    MONTHNAME(date) as month,
    QUARTER(date) as quarter,
    YEAR(date) as year
FROM (
    SELECT DATEADD(day, SEQ4(), '2020-01-01') as date
    FROM TABLE(GENERATOR(ROWCOUNT => 3650))
);

-- Luke checks it
SELECT * FROM gold.dim_date WHERE date = '2024-12-11';

date_key  | date       | day_of_week | month    | quarter | year
----------|------------|-------------|----------|---------|-----
20241211  | 2024-12-11 | Wednesday   | December | 4       | 2024
```

**Luke's thought:** *"Date dimension is the backbone of time-based analysis."*

### Day 2: Create Customer Dimension (Type 2 SCD)

```sql
-- Luke implements Type 2 SCD for customer changes
CREATE TABLE gold.dim_customer AS
SELECT
    ROW_NUMBER() OVER (ORDER BY customer_id, signup_date) as customer_key,
    customer_id,
    name,
    email,
    segment,
    signup_date,
    '9999-12-31'::DATE as valid_to,
    TRUE as is_current
FROM silver.customers_cleaned;
```

Luke's colleague asks: "Why Type 2 SCD?"

**Luke explains:** 
> "If a customer changes from 'Regular' to 'VIP' segment, we want to track that history. Type 2 SCD adds a new row with the new segment, so we can see what segment they were in when they made each purchase."

### Day 3: Create Product Dimension

```sql
CREATE TABLE gold.dim_product AS
SELECT
    ROW_NUMBER() OVER (ORDER BY product_id) as product_key,
    product_id,
    name,
    category,
    brand,
    price
FROM silver.products_cleaned;
```

### Day 4: Create Fact Table

```sql
-- Luke creates the fact table - the heart of the star schema
CREATE TABLE gold.fact_orders AS
SELECT
    o.order_id,
    c.customer_key,
    p.product_key,
    d.date_key,
    s.status_key,
    1 as quantity,
    o.amount as unit_price,
    0 as discount,
    o.amount as total_amount
FROM silver.orders_cleaned o
JOIN gold.dim_customer c 
    ON o.customer_id = c.customer_id 
    AND c.is_current = TRUE
JOIN gold.dim_product p 
    ON o.product_id = p.product_id
JOIN gold.dim_date d 
    ON TO_NUMBER(TO_CHAR(o.order_date, 'YYYYMMDD')) = d.date_key
JOIN gold.dim_order_status s 
    ON o.status = s.status;
```

Luke tests a query:

```sql
-- Revenue by month
SELECT
    d.month,
    d.year,
    SUM(f.total_amount) as revenue
FROM gold.fact_orders f
JOIN gold.dim_date d ON f.date_key = d.date_key
WHERE d.year = 2024
GROUP BY d.month, d.year
ORDER BY d.year, d.month;

-- Query time: 0.8 seconds for 10,000 rows
```

**Luke's thought:** *"Fast! Star schema makes queries simple and performant."*

---

## 📅 Week 8: Creating Data Marts

Sarah from Sales asks Luke: "Can you make queries even faster for my team?"

**Luke:** "Absolutely. I'll create a Sales Data Mart with pre-aggregated metrics."

```sql
CREATE SCHEMA sales_mart;

-- Pre-aggregate daily sales
CREATE TABLE sales_mart.daily_sales AS
SELECT
    d.date,
    d.month,
    c.segment,
    p.category,
    COUNT(DISTINCT f.order_id) as order_count,
    SUM(f.total_amount) as revenue,
    AVG(f.total_amount) as avg_order_value
FROM gold.fact_orders f
JOIN gold.dim_date d ON f.date_key = d.date_key
JOIN gold.dim_customer c ON f.customer_key = c.customer_key
JOIN gold.dim_product p ON f.product_key = p.product_key
GROUP BY d.date, d.month, c.segment, p.category;
```

Luke tests the performance:

```sql
-- Query the data mart
SELECT month, SUM(revenue) as total_revenue
FROM sales_mart.daily_sales
WHERE month = 'December'
GROUP BY month;

-- Query time: 0.1 seconds (8x faster than querying fact table!)
```

**Luke's thought:** *"Data marts are perfect for department-specific, fast queries."*

---

## 📅 Week 9: Connecting Tableau

Luke sets up Tableau for the business users.

**Connection settings:**
```
Server: shopco.snowflakecomputing.com
Database: SHOPCO_DW
Schema: sales_mart
Authentication: OAuth
```

Luke creates the first dashboard for Sarah:

**Dashboard: Monthly Revenue**
- Line chart showing revenue trend
- Filter by customer segment
- Filter by product category

Sarah opens Tableau and drags "Month" and "Revenue" to the chart.

**Behind the scenes:**
```sql
-- Tableau automatically generates this query
SELECT month, SUM(revenue) as total_revenue
FROM sales_mart.daily_sales
GROUP BY month
ORDER BY month;

-- Snowflake executes in cloud: 0.1 seconds
-- Returns 12 rows to Tableau
-- Sarah sees the chart instantly
```

**Sarah:** "Luke, this is amazing! I can see our revenue in real-time. No more waiting 2 days for Excel reports!"

---

## 📅 Day 60: Real-World Usage

### Scenario 1: Morning Standup

**Sarah (Sales VP):** "What was our revenue yesterday?"

Sarah opens Tableau, clicks "Yesterday" filter.

**Query sent to Snowflake:**
```sql
SELECT SUM(revenue) 
FROM sales_mart.daily_sales 
WHERE date = CURRENT_DATE - 1;
```

**Result:** $45,000

**Time:** 2 seconds (vs 2 days before!)

---

### Scenario 2: Marketing Campaign

**Mike (Marketing Manager):** "I need a list of VIP customers who haven't ordered in 30 days."

Mike writes a simple SQL query:

```sql
SELECT customer_id, name, email
FROM sales_mart.top_customers
WHERE segment = 'VIP'
  AND last_order_date < CURRENT_DATE - 30;
```

**Result:** 150 customers exported to CSV

Mike uploads to email marketing tool and sends targeted campaign.

**Time:** 5 minutes (vs hours of manual work!)

---

### Scenario 3: Product Decision

**Emma (Product Manager):** "Which product categories are growing?"

Emma uses Tableau to create a chart:
- X-axis: Month
- Y-axis: Revenue
- Color: Product Category

**Query Tableau sends:**
```sql
SELECT 
    d.month,
    p.category,
    SUM(f.total_amount) as revenue
FROM gold.fact_orders f
JOIN gold.dim_date d ON f.date_key = d.date_key
JOIN gold.dim_product p ON f.product_key = p.product_key
WHERE d.year = 2024
GROUP BY d.month, p.category;
```

**Insight:** Electronics growing 40% month-over-month!

**Emma's decision:** "Let's invest more in electronics inventory."

---

## 📅 Day 90: The Results

Luke presents the results to the executive team:

**Before Luke's Platform:**
- ❌ Manual Excel reports: 2 days
- ❌ Data scattered across 4 systems
- ❌ No self-service analytics
- ❌ Decisions based on outdated data

**After Luke's Platform:**
- ✅ Real-time dashboards: 2 seconds
- ✅ Single source of truth in Snowflake
- ✅ Self-service analytics for all teams
- ✅ Data-driven decisions daily

**Business Impact:**
- 💰 Saved $150,000/year (eliminated 2 analyst positions)
- 📈 Revenue increased 15% (faster, better decisions)
- ⚡ 99.9% faster reporting (2 days → 2 seconds)
- 😊 100% user satisfaction

**CEO:** "Luke, this is transformational. Great work!"

---

## 🎓 What Luke Learned

### Technical Skills:
1. **Data Lake (S3):** Store raw data cheaply
2. **ELT (Fivetran):** Extract and load, transform later
3. **Bronze/Silver/Gold:** Three-layer architecture
4. **Star Schema:** Fact + Dimensions = Fast analytics
5. **Type 2 SCD:** Track historical changes
6. **Data Marts:** Pre-aggregate for speed
7. **Cloud Warehouse (Snowflake):** Queries run remotely

### Design Principles:
1. **Preserve raw data** (Bronze layer)
2. **Clean once, use many times** (Silver layer)
3. **Optimize for business questions** (Gold layer)
4. **Pre-aggregate for speed** (Data Marts)
5. **Enable self-service** (Tableau)

### Career Growth:
- Promoted to Senior Data Engineer
- Leading a team of 3 engineers
- Building data platforms for other departments

---

## 🎯 Your Turn

Now you understand how all the pieces fit together because you followed Luke's journey!

**You learned:**
- ✅ Why we need Data Lakes, Warehouses, and Marts
- ✅ How Bronze/Silver/Gold layers work
- ✅ Why star schema is powerful
- ✅ Where queries actually run (cloud, not local)
- ✅ How ETL/ELT fits into the pipeline
- ✅ Real-world business impact

**Next steps:**
1. Review Luke's architecture diagram
2. Practice explaining each layer's purpose
3. Use the HTML guide to dive deeper into each concept
4. Take the quiz to test your understanding

You're ready to be the next Luke! 🚀
