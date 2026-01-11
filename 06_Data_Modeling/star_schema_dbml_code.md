# 🌟 Star Schema DBML Code

**Complete DBML syntax for the star schema visualization**

Copy this code to [dbdiagram.io](https://dbdiagram.io) to see the visual diagram!

---

## 📝 Complete Star Schema in DBML

```dbml
// ============================================
// FACT TABLE (CENTER OF STAR)
// ============================================
Table fact_sales {
  sale_id bigint [pk, increment]
  
  // Foreign Keys (connections to dimensions)
  date_key int [not null, note: 'Links to dim_date']
  product_key int [not null, note: 'Links to dim_product']
  customer_key int [not null, note: 'Links to dim_customer']
  store_key int [not null, note: 'Links to dim_store']
  
  // Metrics/Facts
  quantity_sold smallint [not null]
  unit_price decimal(10,2) [not null]
  discount_amount decimal(10,2) [default: 0]
  tax_amount decimal(10,2) [not null]
  total_amount decimal(10,2) [not null]
  cost_amount decimal(10,2) [not null]
  profit_amount decimal(10,2) [not null]
  
  // Degenerate Dimension
  transaction_id varchar(50) [not null]
  
  // Indexes for performance
  Indexes {
    date_key [name: 'idx_date']
    product_key [name: 'idx_product']
    customer_key [name: 'idx_customer']
    store_key [name: 'idx_store']
    (date_key, product_key) [name: 'idx_date_product']
  }
  
  Note: 'Fact table - stores sales transactions with measurements'
}

// ============================================
// DIMENSION: DATE (WHEN)
// ============================================
Table dim_date {
  date_key int [pk, note: 'Format: YYYYMMDD (20241211)']
  
  // Date attributes
  full_date date [unique, not null]
  
  // Day attributes
  day_of_week tinyint [note: '1-7']
  day_name varchar(10) [note: 'Monday, Tuesday, etc.']
  day_of_month tinyint [note: '1-31']
  day_of_year smallint [note: '1-365']
  
  // Week attributes
  week_of_year tinyint [note: '1-52']
  week_of_month tinyint [note: '1-5']
  
  // Month attributes
  month_number tinyint [note: '1-12']
  month_name varchar(10) [note: 'January, February, etc.']
  month_abbr char(3) [note: 'Jan, Feb, etc.']
  
  // Quarter attributes
  quarter tinyint [note: '1-4']
  quarter_name varchar(10) [note: 'Q1, Q2, Q3, Q4']
  
  // Year attributes
  year smallint [note: '2024']
  
  // Fiscal period
  fiscal_month tinyint
  fiscal_quarter tinyint
  fiscal_year smallint
  
  // Flags
  is_weekend boolean [default: false]
  is_holiday boolean [default: false]
  holiday_name varchar(100)
  
  Note: 'Date dimension - pre-populated with all dates'
}

// ============================================
// DIMENSION: PRODUCT (WHAT)
// ============================================
Table dim_product {
  product_key int [pk, increment, note: 'Surrogate key']
  
  // Natural key
  product_id varchar(50) [unique, not null, note: 'From source system']
  
  // Product info
  product_name varchar(255) [not null]
  brand varchar(100)
  category varchar(100)
  subcategory varchar(100)
  department varchar(100)
  
  // Product details
  size varchar(50)
  color varchar(50)
  weight_lbs decimal(8,2)
  
  // Slowly Changing Dimension (SCD) fields
  effective_date date [not null]
  expiration_date date
  is_current boolean [default: true]
  
  // Metadata
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  
  Indexes {
    product_id [unique]
    (category, subcategory) [name: 'idx_category']
    is_current [name: 'idx_current']
  }
  
  Note: 'Product dimension - what was sold'
}

// ============================================
// DIMENSION: CUSTOMER (WHO)
// ============================================
Table dim_customer {
  customer_key int [pk, increment, note: 'Surrogate key']
  
  // Natural key
  customer_id varchar(50) [unique, not null, note: 'From source system']
  
  // Customer info
  first_name varchar(100)
  last_name varchar(100)
  email varchar(255)
  phone varchar(20)
  
  // Demographics
  age_group varchar(20) [note: '18-24, 25-34, 35-44, etc.']
  gender varchar(10)
  
  // Location
  city varchar(100)
  state char(2)
  zip_code char(5)
  country char(2) [default: 'US']
  region varchar(50) [note: 'Northeast, Southwest, etc.']
  
  // Customer segmentation
  customer_segment varchar(50) [note: 'VIP, Regular, New']
  loyalty_tier varchar(20) [note: 'Gold, Silver, Bronze']
  
  // SCD fields
  effective_date date [not null]
  expiration_date date
  is_current boolean [default: true]
  
  // Metadata
  created_at timestamp [default: `now()`]
  
  Indexes {
    customer_id [unique]
    email [name: 'idx_email']
    (city, state) [name: 'idx_location']
    is_current [name: 'idx_current']
  }
  
  Note: 'Customer dimension - who made the purchase'
}

// ============================================
// DIMENSION: STORE (WHERE)
// ============================================
Table dim_store {
  store_key int [pk, increment, note: 'Surrogate key']
  
  // Natural key
  store_id varchar(50) [unique, not null, note: 'From source system']
  
  // Store info
  store_name varchar(255) [not null]
  store_number varchar(20)
  
  // Location
  street_address varchar(255)
  city varchar(100)
  state char(2)
  zip_code char(5)
  country char(2) [default: 'US']
  region varchar(50) [note: 'Northeast, Southwest, etc.']
  
  // Store attributes
  store_type varchar(50) [note: 'Supercenter, Neighborhood Market']
  store_size_sqft int
  manager_name varchar(100)
  
  // Dates
  opening_date date
  
  // SCD fields
  effective_date date [not null]
  expiration_date date
  is_current boolean [default: true]
  
  Indexes {
    store_id [unique]
    (city, state) [name: 'idx_location']
    store_type [name: 'idx_type']
    is_current [name: 'idx_current']
  }
  
  Note: 'Store dimension - where the sale occurred'
}

// ============================================
// RELATIONSHIPS (THE STAR!)
// ============================================

// Fact → Date
Ref: fact_sales.date_key > dim_date.date_key

// Fact → Product
Ref: fact_sales.product_key > dim_product.product_key

// Fact → Customer
Ref: fact_sales.customer_key > dim_customer.customer_key

// Fact → Store
Ref: fact_sales.store_key > dim_store.store_key
```

---

## 🎯 Key Syntax Elements

### **1. Table Definition**
```dbml
Table table_name {
  column_name data_type [attributes]
}
```

### **2. Primary Key**
```dbml
product_key int [pk, increment]
// pk = primary key
// increment = auto-increment
```

### **3. Foreign Key (in table)**
```dbml
customer_key int [not null, note: 'Links to dim_customer']
```

### **4. Relationship (outside table)**
```dbml
Ref: fact_sales.customer_key > dim_customer.customer_key
// Read as: "fact_sales.customer_key references dim_customer.customer_key"
// > means one-to-many
```

### **5. Indexes**
```dbml
Indexes {
  column_name [name: 'idx_name']
  (col1, col2) [name: 'idx_composite']
}
```

### **6. Attributes**
```dbml
[pk]              // Primary key
[increment]       // Auto-increment
[not null]        // Required
[unique]          // Must be unique
[default: value]  // Default value
[note: 'text']    // Add note/comment
```

---

## 📊 SQL Version (for comparison)

```sql
-- FACT TABLE
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    -- Foreign Keys
    date_key INT NOT NULL,
    product_key INT NOT NULL,
    customer_key INT NOT NULL,
    store_key INT NOT NULL,
    
    -- Metrics
    quantity_sold SMALLINT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    profit_amount DECIMAL(10,2) NOT NULL,
    
    -- Foreign Key Constraints
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    
    -- Indexes
    INDEX idx_date (date_key),
    INDEX idx_product (product_key),
    INDEX idx_customer (customer_key),
    INDEX idx_store (store_key)
);

-- DIMENSION: DATE
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    day_name VARCHAR(10),
    month_name VARCHAR(10),
    quarter TINYINT,
    year SMALLINT,
    is_weekend BOOLEAN DEFAULT FALSE,
    is_holiday BOOLEAN DEFAULT FALSE
);

-- DIMENSION: PRODUCT
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY AUTO_INCREMENT,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    brand VARCHAR(100),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    is_current BOOLEAN DEFAULT TRUE,
    
    INDEX idx_product_id (product_id),
    INDEX idx_category (category, subcategory)
);

-- DIMENSION: CUSTOMER
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY AUTO_INCREMENT,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    age_group VARCHAR(20),
    city VARCHAR(100),
    state CHAR(2),
    customer_segment VARCHAR(50),
    is_current BOOLEAN DEFAULT TRUE
);

-- DIMENSION: STORE
CREATE TABLE dim_store (
    store_key INT PRIMARY KEY AUTO_INCREMENT,
    store_id VARCHAR(50) UNIQUE NOT NULL,
    store_name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    state CHAR(2),
    store_type VARCHAR(50),
    is_current BOOLEAN DEFAULT TRUE
);
```

---

## 💡 Quick Comparison

| Aspect | DBML | SQL |
|--------|------|-----|
| **Purpose** | Design/documentation | Implementation |
| **Readability** | Very easy | More verbose |
| **Visual** | Auto-generates diagrams | No visuals |
| **Foreign Keys** | `Ref:` outside table | `FOREIGN KEY` inside table |
| **Syntax** | `[pk]`, `[not null]` | `PRIMARY KEY`, `NOT NULL` |

---

## 🚀 Try It Yourself!

1. Go to **[dbdiagram.io](https://dbdiagram.io)**
2. Paste the DBML code above
3. See the star schema diagram automatically!
4. Export to SQL, PDF, or PNG

---

**Remember:** DBML is for **planning**, SQL is for **building**!
