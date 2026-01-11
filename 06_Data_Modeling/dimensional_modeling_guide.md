# 🌟 Dimensional Modeling - Fact & Dimension Tables

**Star Schema & Data Warehousing Guide**

---

## 🎯 What is Dimensional Modeling?

**Dimensional modeling** is a design technique for data warehouses that organizes data into:
- **Fact Tables** - Measurements, metrics, transactions
- **Dimension Tables** - Context, descriptive attributes

**ANALOGY: Think of a Receipt**
- **Fact Table** = The receipt itself (what was bought, how much, when)
- **Dimension Tables** = Details about the receipt (who bought it, what product, which store, what date)

---

## 📊 Fact Tables vs Dimension Tables

### **Fact Tables** (The Numbers)
- Store **measurements** and **metrics**
- Contain **foreign keys** to dimension tables
- Usually have **many rows** (millions/billions)
- Examples: sales, orders, clicks, views

**Think:** The actual event/transaction

### **Dimension Tables** (The Context)
- Store **descriptive attributes**
- Provide **context** for facts
- Usually have **fewer rows** than facts
- Examples: customers, products, dates, locations

**Think:** The "who, what, when, where, why"

---

## 🌟 Star Schema

**Visual Representation:**
```
        dim_date
            |
            |
        dim_product ---- fact_sales ---- dim_customer
            |
            |
        dim_store
```

**Why "Star"?** The fact table is in the center, dimension tables radiate out like star points!

---

## 🛒 Real-World Example: Walmart Sales

### **Fact Table: fact_sales**

```sql
CREATE TABLE fact_sales (
    -- Surrogate Key (optional)
    sale_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    -- Foreign Keys to Dimensions (THE STAR POINTS!)
    date_key INT NOT NULL,              -- → dim_date
    product_key INT NOT NULL,           -- → dim_product
    store_key INT NOT NULL,             -- → dim_store
    customer_key INT NOT NULL,          -- → dim_customer
    
    -- Facts/Metrics (THE MEASUREMENTS!)
    quantity_sold SMALLINT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    cost_amount DECIMAL(10,2) NOT NULL,  -- For profit calculation
    profit_amount DECIMAL(10,2) NOT NULL, -- total - cost
    
    -- Degenerate Dimension (stored in fact table)
    transaction_id VARCHAR(50) NOT NULL,
    
    -- Indexes
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    
    INDEX idx_date (date_key),
    INDEX idx_product (product_key),
    INDEX idx_store (store_key),
    INDEX idx_customer (customer_key)
);
```

**💡 Key Points:**
- Mostly **foreign keys** + **numeric measurements**
- **BIGINT** for sale_id (millions of transactions)
- **DECIMAL** for money (never FLOAT!)
- Indexed on all foreign keys for fast JOINs

---

### **Dimension Table: dim_product**

```sql
CREATE TABLE dim_product (
    -- Surrogate Key
    product_key INT PRIMARY KEY AUTO_INCREMENT,
    
    -- Natural Key (from source system)
    product_id VARCHAR(50) UNIQUE NOT NULL,
    
    -- Descriptive Attributes
    product_name VARCHAR(255) NOT NULL,
    brand VARCHAR(100),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    department VARCHAR(100),
    
    -- Product Details
    size VARCHAR(50),
    color VARCHAR(50),
    weight_lbs DECIMAL(8,2),
    
    -- Slowly Changing Dimension (SCD) fields
    effective_date DATE NOT NULL,
    expiration_date DATE,
    is_current TINYINT(1) DEFAULT 1,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**💡 Key Points:**
- **Surrogate key** (product_key) - internal ID
- **Natural key** (product_id) - from source system
- **Descriptive attributes** - what you filter/group by
- **SCD fields** - track changes over time

---

### **Dimension Table: dim_date**

```sql
CREATE TABLE dim_date (
    -- Surrogate Key
    date_key INT PRIMARY KEY,           -- Format: 20241211 (YYYYMMDD)
    
    -- Date Attributes
    full_date DATE UNIQUE NOT NULL,
    
    -- Day Attributes
    day_of_week TINYINT,                -- 1-7
    day_name VARCHAR(10),               -- 'Monday', 'Tuesday'
    day_of_month TINYINT,               -- 1-31
    day_of_year SMALLINT,               -- 1-365
    
    -- Week Attributes
    week_of_year TINYINT,               -- 1-52
    week_of_month TINYINT,              -- 1-5
    
    -- Month Attributes
    month_number TINYINT,               -- 1-12
    month_name VARCHAR(10),             -- 'January', 'February'
    month_abbr CHAR(3),                 -- 'Jan', 'Feb'
    
    -- Quarter Attributes
    quarter TINYINT,                    -- 1-4
    quarter_name VARCHAR(10),           -- 'Q1', 'Q2'
    
    -- Year Attributes
    year SMALLINT,                      -- 2024
    
    -- Fiscal Period (if different from calendar)
    fiscal_month TINYINT,
    fiscal_quarter TINYINT,
    fiscal_year SMALLINT,
    
    -- Flags
    is_weekend TINYINT(1),
    is_holiday TINYINT(1),
    holiday_name VARCHAR(100)
);
```

**💡 Key Points:**
- **Pre-populated** with all dates (e.g., 2020-2030)
- **date_key** as integer (20241211) for performance
- **Rich attributes** for easy filtering/grouping
- No foreign keys (it's a dimension!)

---

### **Dimension Table: dim_customer**

```sql
CREATE TABLE dim_customer (
    -- Surrogate Key
    customer_key INT PRIMARY KEY AUTO_INCREMENT,
    
    -- Natural Key
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    
    -- Customer Info
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    
    -- Demographics
    age_group VARCHAR(20),              -- '18-24', '25-34', '35-44'
    gender VARCHAR(10),
    
    -- Location
    city VARCHAR(100),
    state CHAR(2),
    zip_code CHAR(5),
    country CHAR(2) DEFAULT 'US',
    region VARCHAR(50),                 -- 'Northeast', 'Southwest'
    
    -- Customer Segmentation
    customer_segment VARCHAR(50),       -- 'VIP', 'Regular', 'New'
    loyalty_tier VARCHAR(20),           -- 'Gold', 'Silver', 'Bronze'
    
    -- SCD Fields
    effective_date DATE NOT NULL,
    expiration_date DATE,
    is_current TINYINT(1) DEFAULT 1,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### **Dimension Table: dim_store**

```sql
CREATE TABLE dim_store (
    -- Surrogate Key
    store_key INT PRIMARY KEY AUTO_INCREMENT,
    
    -- Natural Key
    store_id VARCHAR(50) UNIQUE NOT NULL,
    
    -- Store Info
    store_name VARCHAR(255) NOT NULL,
    store_number VARCHAR(20),
    
    -- Location
    street_address VARCHAR(255),
    city VARCHAR(100),
    state CHAR(2),
    zip_code CHAR(5),
    country CHAR(2) DEFAULT 'US',
    region VARCHAR(50),
    
    -- Store Attributes
    store_type VARCHAR(50),             -- 'Supercenter', 'Neighborhood Market'
    store_size_sqft INT,
    manager_name VARCHAR(100),
    
    -- Dates
    opening_date DATE,
    
    -- SCD Fields
    effective_date DATE NOT NULL,
    expiration_date DATE,
    is_current TINYINT(1) DEFAULT 1
);
```

---

## 📊 DBML Version (Star Schema)

```dbml
// FACT TABLE (CENTER OF THE STAR)
Table fact_sales {
  sale_id bigint [pk, increment]
  
  // Foreign Keys (Star Points!)
  date_key int [not null]
  product_key int [not null]
  store_key int [not null]
  customer_key int [not null]
  
  // Metrics
  quantity_sold smallint [not null]
  unit_price decimal(10,2) [not null]
  total_amount decimal(10,2) [not null]
  profit_amount decimal(10,2) [not null]
  
  Indexes {
    date_key
    product_key
    store_key
    customer_key
  }
}

// DIMENSION TABLES (STAR POINTS)
Table dim_product {
  product_key int [pk, increment]
  product_id varchar(50) [unique, not null]
  product_name varchar(255) [not null]
  brand varchar(100)
  category varchar(100)
  subcategory varchar(100)
  is_current boolean [default: true]
}

Table dim_date {
  date_key int [pk]                    // 20241211
  full_date date [unique, not null]
  day_name varchar(10)
  month_name varchar(10)
  quarter int
  year smallint
  is_weekend boolean
  is_holiday boolean
}

Table dim_customer {
  customer_key int [pk, increment]
  customer_id varchar(50) [unique, not null]
  first_name varchar(100)
  last_name varchar(100)
  age_group varchar(20)
  city varchar(100)
  state char(2)
  customer_segment varchar(50)
  is_current boolean [default: true]
}

Table dim_store {
  store_key int [pk, increment]
  store_id varchar(50) [unique, not null]
  store_name varchar(255) [not null]
  city varchar(100)
  state char(2)
  store_type varchar(50)
  is_current boolean [default: true]
}

// RELATIONSHIPS (THE STAR!)
Ref: fact_sales.date_key > dim_date.date_key
Ref: fact_sales.product_key > dim_product.product_key
Ref: fact_sales.store_key > dim_store.store_key
Ref: fact_sales.customer_key > dim_customer.customer_key
```

---

## 🎯 Example Queries

### **Query 1: Total Sales by Product Category**
```sql
SELECT 
    p.category,
    SUM(f.total_amount) AS total_sales,
    SUM(f.quantity_sold) AS total_quantity
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
WHERE p.is_current = 1
GROUP BY p.category
ORDER BY total_sales DESC;
```

### **Query 2: Monthly Sales Trend**
```sql
SELECT 
    d.year,
    d.month_name,
    SUM(f.total_amount) AS monthly_sales,
    SUM(f.profit_amount) AS monthly_profit
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month_number, d.month_name
ORDER BY d.year, d.month_number;
```

### **Query 3: Top Customers by Region**
```sql
SELECT 
    c.region,
    c.customer_segment,
    COUNT(DISTINCT f.customer_key) AS customer_count,
    SUM(f.total_amount) AS total_spent
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
WHERE c.is_current = 1
GROUP BY c.region, c.customer_segment
ORDER BY total_spent DESC;
```

---

## 🎓 Best Practices

### **1. Surrogate Keys**
```sql
-- ✅ GOOD: Use surrogate keys in dimensions
product_key INT PRIMARY KEY AUTO_INCREMENT

-- Why? Protects against source system changes
```

### **2. Slowly Changing Dimensions (SCD)**
```sql
-- Track changes over time
effective_date DATE NOT NULL
expiration_date DATE
is_current TINYINT(1) DEFAULT 1

-- Example: Product price changes
-- Old record: is_current = 0, expiration_date = '2024-12-10'
-- New record: is_current = 1, effective_date = '2024-12-11'
```

### **3. Date Dimension is Pre-Populated**
```sql
-- Generate all dates from 2020-2030
-- Never insert dates on-the-fly!
INSERT INTO dim_date VALUES
(20241211, '2024-12-11', 3, 'Wednesday', 12, 'December', 4, 2024, 0, 0, NULL),
(20241212, '2024-12-12', 4, 'Thursday', 12, 'December', 4, 2024, 0, 0, NULL);
```

### **4. Grain of Fact Table**
```sql
-- Define the grain clearly!
-- Example: "One row per product sold per transaction"

-- ✅ GOOD: Clear grain
fact_sales: One row per line item

-- ❌ BAD: Mixed grain
fact_sales: Sometimes line item, sometimes order total
```

### **5. Additive vs Non-Additive Facts**
```sql
-- Additive (can sum across all dimensions)
quantity_sold INT        -- ✅ Can sum
total_amount DECIMAL     -- ✅ Can sum

-- Semi-Additive (can sum across some dimensions)
inventory_level INT      -- ⚠️ Can't sum across time

-- Non-Additive (can't sum)
unit_price DECIMAL       -- ❌ Don't sum prices!
profit_margin DECIMAL    -- ❌ Calculate from other facts
```

---

## 🌟 Star Schema vs Snowflake Schema

### **Star Schema** (Recommended for most cases)
```
Fact Table → Dimension Tables (denormalized)
```
**Pros:**
- ✅ Simpler queries
- ✅ Faster performance
- ✅ Easier to understand

**Cons:**
- ❌ Some data duplication in dimensions

### **Snowflake Schema**
```
Fact Table → Dimension Tables → Sub-Dimension Tables (normalized)
```
**Pros:**
- ✅ Less data duplication
- ✅ Smaller storage

**Cons:**
- ❌ More complex queries
- ❌ Slower (more JOINs)

**Recommendation:** Use **Star Schema** unless you have a specific reason not to!

---

## 💡 Key Takeaways

1. **Fact Tables** = Measurements (sales, clicks, views)
2. **Dimension Tables** = Context (who, what, when, where)
3. **Star Schema** = Fact in center, dimensions radiate out
4. **Surrogate Keys** = Use in dimensions for stability
5. **Date Dimension** = Pre-populate with all dates
6. **SCD** = Track changes over time
7. **Grain** = Define clearly (one row = what?)

---

**Use this for:** Data warehouses, analytics, reporting, BI dashboards!
