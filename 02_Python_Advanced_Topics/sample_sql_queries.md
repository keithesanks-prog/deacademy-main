# Sample SQL Queries for SQL Lineage Parser Testing

## Table Schemas

### 1. E-Commerce Database

```sql
-- customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    signup_date DATE
);

-- orders table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status VARCHAR(20)
);

-- order_items table
CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2)
);

-- products table
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock_quantity INT
);
```

---

## Sample SQL Queries to Test

### Query 1: Simple SELECT with Transformations
**Purpose**: Test basic column lineage with calculations

```sql
SELECT 
    first_name || ' ' || last_name AS full_name,
    email,
    UPPER(city) AS city_upper,
    signup_date
FROM customers
WHERE state = 'CA'
```

**Expected Lineage**:
- `customers.first_name` → `full_name` (transformation: concatenation)
- `customers.last_name` → `full_name` (transformation: concatenation)
- `customers.email` → `email` (direct mapping)
- `customers.city` → `city_upper` (transformation: UPPER())
- `customers.signup_date` → `signup_date` (direct mapping)

---

### Query 2: JOIN with Aggregations
**Purpose**: Test multi-table lineage

```sql
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS lifetime_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
```

**Expected Lineage**:
- `customers.customer_id` → `customer_id`
- `customers.first_name` → `first_name`
- `customers.last_name` → `last_name`
- `orders.order_id` → `total_orders` (transformation: COUNT())
- `orders.total_amount` → `lifetime_value` (transformation: SUM())

---

### Query 3: Subquery Example
**Purpose**: Test subquery lineage tracking

```sql
SELECT 
    customer_id,
    full_name,
    total_spent
FROM (
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name AS full_name,
        SUM(o.total_amount) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
) customer_summary
WHERE total_spent > 1000
```

**Expected Lineage**:
- `customers.customer_id` → `customer_summary.customer_id` → `customer_id`
- `customers.first_name` → `customer_summary.full_name` → `full_name`
- `customers.last_name` → `customer_summary.full_name` → `full_name`
- `orders.total_amount` → `customer_summary.total_spent` → `total_spent`

---

### Query 4: Complex Calculations
**Purpose**: Test complex transformations

```sql
SELECT 
    p.product_name,
    p.category,
    p.price AS original_price,
    p.price * 0.9 AS sale_price,
    p.price * 0.9 * oi.quantity AS line_total,
    oi.quantity
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
WHERE p.category = 'Electronics'
```

**Expected Lineage**:
- `products.product_name` → `product_name`
- `products.category` → `category`
- `products.price` → `original_price`
- `products.price` → `sale_price` (transformation: * 0.9)
- `products.price` → `line_total` (transformation: * 0.9 * quantity)
- `order_items.quantity` → `line_total` (transformation: price * 0.9 * quantity)
- `order_items.quantity` → `quantity`

---

### Query 5: CASE Statement
**Purpose**: Test conditional logic lineage

```sql
SELECT 
    customer_id,
    first_name,
    last_name,
    CASE 
        WHEN state IN ('CA', 'NY', 'TX') THEN 'Major Market'
        WHEN state IN ('FL', 'IL', 'PA') THEN 'Secondary Market'
        ELSE 'Other'
    END AS market_segment
FROM customers
```

**Expected Lineage**:
- `customers.customer_id` → `customer_id`
- `customers.first_name` → `first_name`
- `customers.last_name` → `last_name`
- `customers.state` → `market_segment` (transformation: CASE statement)

---

### Query 6: Window Functions
**Purpose**: Test window function lineage

```sql
SELECT 
    customer_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS order_rank
FROM orders
```

**Expected Lineage**:
- `orders.customer_id` → `customer_id`
- `orders.order_date` → `order_date`
- `orders.total_amount` → `total_amount`
- `orders.total_amount` → `running_total` (transformation: SUM() OVER)
- `orders.customer_id` → `running_total` (used in PARTITION BY)
- `orders.order_date` → `running_total` (used in ORDER BY)
- `orders.order_date` → `order_rank` (transformation: ROW_NUMBER() OVER)

---

## Quick Test Queries (Copy & Paste)

### Beginner Level
```sql
SELECT first_name, last_name, email FROM customers
```

### Intermediate Level
```sql
SELECT 
    c.first_name,
    COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.first_name
```

### Advanced Level
```sql
SELECT 
    product_name,
    category,
    price,
    AVG(price) OVER (PARTITION BY category) AS avg_category_price,
    price - AVG(price) OVER (PARTITION BY category) AS price_vs_avg
FROM products
```

---

## How to Use These Samples

1. **Copy a SQL query** from above
2. **Paste it into the SQL Lineage Parser** text area
3. **Click "Parse SQL"** button
4. **Review the lineage results** in the table below

The parser will show you:
- Which source tables and columns are used
- What transformations are applied
- What the output column names are

---

## Testing Checklist

- [ ] Test Query 1: Simple SELECT
- [ ] Test Query 2: JOIN with aggregations
- [ ] Test Query 3: Subquery
- [ ] Test Query 4: Complex calculations
- [ ] Test Query 5: CASE statement
- [ ] Test Query 6: Window functions

---

## Expected Output Format

When you parse a query, you should see results like:

| From Schema | From Table | From Column | To Schema | To Table | To Column | Transformation |
|-------------|------------|-------------|-----------|----------|-----------|----------------|
| None | customers | first_name | None | None | full_name | first_name \|\| ' ' \|\| last_name |
| None | customers | last_name | None | None | full_name | first_name \|\| ' ' \|\| last_name |
| None | customers | email | None | None | email | email |

---

## Troubleshooting

**If you don't see results:**
- Check that the SQL is valid
- Ensure you clicked the "Parse SQL" button
- Look for error messages in the console

**If lineage looks incomplete:**
- Some complex SQL features may not be fully supported
- Try simplifying the query to test specific features
