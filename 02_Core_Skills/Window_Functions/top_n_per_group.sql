-- ============================================
-- TOP N PER GROUP: Finding Best Performers by Category
-- ============================================
-- Goal: Find the top spender in EACH city (not overall)
-- This uses PARTITION BY to rank within groups

-- ============================================
-- THE PATTERN
-- ============================================
-- 1. Aggregate data (SUM, COUNT, etc.)
-- 2. Use ROW_NUMBER() or RANK() with PARTITION BY
-- 3. Filter to top N per group

-- ============================================
-- SETUP: Sample Data
-- ============================================
DROP TABLE IF EXISTS orders_prc CASCADE;
DROP TABLE IF EXISTS customers_prc CASCADE;

CREATE TABLE customers_prc (
    customerid INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    city VARCHAR(100)
);

CREATE TABLE orders_prc (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    amount INT,
    FOREIGN KEY (customer_id) REFERENCES customers_prc(customerid)
);

INSERT INTO customers_prc VALUES
(1, 'Alice Johnson', 25, 'New York'),
(2, 'Bob Smith', 35, 'New York'),
(3, 'Charlie Brown', 45, 'Chicago'),
(4, 'Diana Prince', 28, 'Chicago'),
(5, 'Eve Wilson', 32, 'Chicago');

INSERT INTO orders_prc VALUES
-- New York customers
(101, 1, '2025-01-10', 100),
(102, 1, '2025-01-15', 200),  -- Alice total: 300
(103, 2, '2025-01-12', 500),
(104, 2, '2025-01-18', 600),  -- Bob total: 1100 (top in NY!)
-- Chicago customers
(105, 3, '2025-01-14', 300),
(106, 3, '2025-01-20', 400),  -- Charlie total: 700 (top in Chicago!)
(107, 4, '2025-01-16', 200),  -- Diana total: 200
(108, 5, '2025-01-19', 150);  -- Eve total: 150

SELECT * FROM customers_prc ORDER BY city, name;
SELECT * FROM orders_prc ORDER BY customer_id;


-- ============================================
-- SOLUTION: Top Spender Per City
-- ============================================

WITH CustomerSpending AS (
    -- CTE 1: Calculate total spending for every customer
    SELECT
        c.city,
        c.name,
        SUM(o.amount) AS TotalSpending,
        c.customerid  -- Needed for grouping
    FROM
        customers_prc c
    JOIN
        orders_prc o ON c.customerid = o.customer_id
    GROUP BY
        c.customerid, c.city, c.name  -- Group by customer to get their total
),
RankedSpending AS (
    -- CTE 2: Rank customers WITHIN their city based on spending
    SELECT
        city,
        name,
        TotalSpending,
        -- PARTITION BY city: Rank resets for each city!
        ROW_NUMBER() OVER (PARTITION BY city ORDER BY TotalSpending DESC) AS rank_in_city
    FROM
        CustomerSpending
)
-- Final Select: Filter for only the customer with Rank 1 in each city
SELECT
    city,
    name,
    TotalSpending
FROM
    RankedSpending
WHERE
    rank_in_city = 1
ORDER BY
    city DESC;

-- Expected Output:
-- city     | name          | TotalSpending
-- ---------|---------------|---------------
-- New York | Bob Smith     | 1100
-- Chicago  | Charlie Brown | 700


-- ============================================
-- UNDERSTANDING PARTITION BY
-- ============================================

-- WITHOUT PARTITION BY (ranks across ALL customers):
-- name          | city     | spending | rank
-- --------------|----------|----------|-----
-- Bob Smith     | New York | 1100     | 1  ← Overall #1
-- Charlie Brown | Chicago  | 700      | 2
-- Alice Johnson | New York | 300      | 3
-- Diana Prince  | Chicago  | 200      | 4
-- Eve Wilson    | Chicago  | 150      | 5

-- WITH PARTITION BY city (ranks WITHIN each city):
-- name          | city     | spending | rank_in_city
-- --------------|----------|----------|-------------
-- Bob Smith     | New York | 1100     | 1  ← #1 in NY
-- Alice Johnson | New York | 300      | 2  ← #2 in NY
-- Charlie Brown | Chicago  | 700      | 1  ← #1 in Chicago
-- Diana Prince  | Chicago  | 200      | 2  ← #2 in Chicago
-- Eve Wilson    | Chicago  | 150      | 3  ← #3 in Chicago


-- ============================================
-- SCAFFOLDING: See ALL ranks
-- ============================================
-- Remove the WHERE clause to see everyone's rank

WITH CustomerSpending AS (
    SELECT
        c.city,
        c.name,
        SUM(o.amount) AS TotalSpending,
        c.customerid
    FROM customers_prc c
    JOIN orders_prc o ON c.customerid = o.customer_id
    GROUP BY c.customerid, c.city, c.name
),
RankedSpending AS (
    SELECT
        city,
        name,
        TotalSpending,
        ROW_NUMBER() OVER (PARTITION BY city ORDER BY TotalSpending DESC) AS rank_in_city,
        -- SCAFFOLDING: Show overall rank too
        ROW_NUMBER() OVER (ORDER BY TotalSpending DESC) AS overall_rank
    FROM CustomerSpending
)
SELECT
    city,
    name,
    TotalSpending,
    rank_in_city,
    overall_rank,
    CASE WHEN rank_in_city = 1 THEN '✓ Top in City' ELSE '' END AS top_spender
FROM RankedSpending
ORDER BY city, rank_in_city;


-- ============================================
-- ROW_NUMBER vs RANK vs DENSE_RANK
-- ============================================

WITH CustomerSpending AS (
    SELECT
        c.city,
        c.name,
        SUM(o.amount) AS TotalSpending
    FROM customers_prc c
    JOIN orders_prc o ON c.customerid = o.customer_id
    GROUP BY c.city, c.name
)
SELECT
    city,
    name,
    TotalSpending,
    ROW_NUMBER() OVER (PARTITION BY city ORDER BY TotalSpending DESC) AS row_num,
    RANK() OVER (PARTITION BY city ORDER BY TotalSpending DESC) AS rank,
    DENSE_RANK() OVER (PARTITION BY city ORDER BY TotalSpending DESC) AS dense_rank
FROM CustomerSpending
ORDER BY city, TotalSpending DESC;

-- Difference:
-- ROW_NUMBER(): Always unique (1, 2, 3, 4, 5...)
-- RANK(): Ties get same rank, skips next (1, 2, 2, 4, 5...)
-- DENSE_RANK(): Ties get same rank, no skip (1, 2, 2, 3, 4...)


-- ============================================
-- EXAMPLE 2: Top 3 Products Per Category
-- ============================================

DROP TABLE IF EXISTS products CASCADE;

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    sales_amount INT
);

INSERT INTO products VALUES
(1, 'Laptop Pro', 'Electronics', 1200),
(2, 'Mouse', 'Electronics', 25),
(3, 'Keyboard', 'Electronics', 75),
(4, 'Monitor', 'Electronics', 450),
(5, 'Desk', 'Furniture', 350),
(6, 'Chair', 'Furniture', 200),
(7, 'Lamp', 'Furniture', 45);

-- Find top 2 products per category
WITH RankedProducts AS (
    SELECT
        category,
        product_name,
        sales_amount,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales_amount DESC) AS rank_in_category
    FROM products
)
SELECT
    category,
    product_name,
    sales_amount
FROM RankedProducts
WHERE rank_in_category <= 2  -- Top 2 per category
ORDER BY category, rank_in_category;


-- ============================================
-- COMMON PATTERNS
-- ============================================

-- Pattern 1: Top 1 per group
WHERE rank_in_group = 1

-- Pattern 2: Top N per group
WHERE rank_in_group <= N

-- Pattern 3: Bottom N per group
-- Use ORDER BY ... ASC instead of DESC

-- Pattern 4: Top 10% per group
WHERE rank_in_group <= (COUNT(*) OVER (PARTITION BY group_column) * 0.1)


-- ============================================
-- PRACTICE VARIATIONS
-- ============================================

-- Practice 1: Find the LOWEST spender in each city
-- Hint: Change ORDER BY TotalSpending DESC to ASC

-- Practice 2: Find the top 2 spenders in each city
-- Hint: Change WHERE rank_in_city = 1 to <= 2

-- Practice 3: Find customers who are in the top 3 overall but NOT top in their city
-- Hint: Use both overall_rank and rank_in_city

-- Practice 4: Find cities where the top spender spent more than $500
-- Hint: Add AND TotalSpending > 500 to the WHERE clause


-- ============================================
-- KEY CONCEPTS
-- ============================================
-- 1. PARTITION BY: Resets the ranking for each group
-- 2. ROW_NUMBER(): Assigns unique sequential numbers
-- 3. RANK(): Handles ties, skips numbers
-- 4. DENSE_RANK(): Handles ties, no gaps
-- 5. "Top N per group" = PARTITION BY + filter on rank
