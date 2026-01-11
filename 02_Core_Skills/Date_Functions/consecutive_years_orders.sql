-- ============================================
-- CUSTOMERS WITH CONSECUTIVE YEAR ORDERS
-- ============================================
-- Goal: Find customers who:
--   1. Placed orders in at least 2 consecutive years (e.g., 2022 AND 2023)
--   2. Had more than 1 order in at least one of those years

-- ============================================
-- TERMINOLOGY (IMPORTANT!)
-- ============================================
-- "Consecutive years" = Years that follow each other (2022 → 2023, not 2022 → 2024)
-- "More than one order in at least one year" = 2+ orders in 2022 OR 2+ orders in 2023

-- Example:
-- Alice: 2 orders in 2022, 1 order in 2023 → ✅ Qualifies (consecutive + 2 in 2022)
-- Bob: 1 order in 2022, 1 order in 2023 → ❌ Doesn't qualify (only 1 order each year)
-- Charlie: 3 orders in 2022, 0 in 2023 → ❌ Doesn't qualify (not consecutive)
-- Diana: 1 order in 2022, 2 orders in 2024 → ❌ Doesn't qualify (not consecutive)

-- ============================================
-- SETUP: Create tables and sample data
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
(2, 'Bob Smith', 35, 'Chicago'),
(3, 'Charlie Brown', 45, 'Los Angeles'),
(4, 'Diana Prince', 28, 'Seattle'),
(5, 'Eve Wilson', 32, 'Boston');

INSERT INTO orders_prc VALUES
-- Alice: 2 orders in 2022, 1 in 2023 (consecutive, 2+ in one year) ✅
(101, 1, '2022-01-15', 100),
(102, 1, '2022-06-20', 200),
(103, 1, '2023-03-10', 150),

-- Bob: 1 order in 2022, 1 in 2023 (consecutive, but only 1 each year) ❌
(104, 2, '2022-05-10', 50),
(105, 2, '2023-08-15', 75),

-- Charlie: 3 orders in 2022, none in 2023 (not consecutive) ❌
(106, 3, '2022-02-10', 500),
(107, 3, '2022-07-15', 300),
(108, 3, '2022-11-20', 400),

-- Diana: 1 in 2022, 2 in 2024 (not consecutive - gap year) ❌
(109, 4, '2022-04-05', 150),
(110, 4, '2024-01-10', 200),
(111, 4, '2024-06-15', 250),

-- Eve: 2 in 2023, 2 in 2024 (consecutive, 2+ in both years) ✅
(112, 5, '2023-02-10', 300),
(113, 5, '2023-09-20', 350),
(114, 5, '2024-03-15', 400),
(115, 5, '2024-11-25', 450);

-- Verify the data
SELECT 'Customers:' as info;
SELECT * FROM customers_prc;

SELECT 'Orders by Customer and Year:' as info;
SELECT 
    c.name,
    EXTRACT(YEAR FROM o.order_date) AS year,
    COUNT(*) AS order_count
FROM customers_prc c
JOIN orders_prc o ON c.customerid = o.customer_id
GROUP BY c.name, EXTRACT(YEAR FROM o.order_date)
ORDER BY c.name, year;


-- ============================================
-- STEP 1: Get Order Counts by Customer and Year
-- ============================================

SELECT 
    c.customerid,
    c.name,
    EXTRACT(YEAR FROM o.order_date) AS year,
    COUNT(*) AS order_count
FROM 
    customers_prc c
JOIN 
    orders_prc o ON c.customerid = o.customer_id
GROUP BY 
    c.customerid, c.name, EXTRACT(YEAR FROM o.order_date)
ORDER BY 
    c.name, year;

-- Result shows each customer's order count per year


-- ============================================
-- STEP 2: Check for Consecutive Years Using LAG
-- ============================================

WITH customer_years AS (
    SELECT 
        c.customerid,
        c.name,
        EXTRACT(YEAR FROM o.order_date) AS year,
        COUNT(*) AS order_count
    FROM 
        customers_prc c
    JOIN 
        orders_prc o ON c.customerid = o.customer_id
    GROUP BY 
        c.customerid, c.name, EXTRACT(YEAR FROM o.order_date)
)
SELECT 
    customerid,
    name,
    year,
    order_count,
    LAG(year) OVER (PARTITION BY customerid ORDER BY year) AS previous_year,
    year - LAG(year) OVER (PARTITION BY customerid ORDER BY year) AS year_gap
FROM 
    customer_years
ORDER BY 
    name, year;

-- year_gap = 1 means consecutive years
-- year_gap > 1 means there's a gap


-- ============================================
-- SOLUTION: Complete Query
-- ============================================

WITH customer_years AS (
    -- Step 1: Count orders per customer per year
    SELECT 
        c.customerid,
        c.name,
        EXTRACT(YEAR FROM o.order_date) AS year,
        COUNT(*) AS order_count
    FROM 
        customers_prc c
    JOIN 
        orders_prc o ON c.customerid = o.customer_id
    GROUP BY 
        c.customerid, c.name, EXTRACT(YEAR FROM o.order_date)
),
consecutive_years AS (
    -- Step 2: Check for consecutive years
    SELECT 
        customerid,
        name,
        year,
        order_count,
        LAG(year) OVER (PARTITION BY customerid ORDER BY year) AS previous_year,
        LAG(order_count) OVER (PARTITION BY customerid ORDER BY year) AS previous_year_count
    FROM 
        customer_years
),
qualified_customers AS (
    -- Step 3: Filter for consecutive years with 2+ orders in at least one year
    SELECT DISTINCT
        customerid,
        name
    FROM 
        consecutive_years
    WHERE 
        -- Consecutive years (current year = previous year + 1)
        year - previous_year = 1
        AND
        -- At least one of the two years has 2+ orders
        (order_count > 1 OR previous_year_count > 1)
)
SELECT 
    name
FROM 
    qualified_customers
ORDER BY 
    name;

-- Expected Output:
-- name
-- ---------------
-- Alice Johnson
-- Eve Wilson


-- ============================================
-- DETAILED BREAKDOWN: How It Works
-- ============================================

-- For Alice:
-- Year | Order Count | Previous Year | Year Gap | Previous Count
-- -----|-------------|---------------|----------|---------------
-- 2022 | 2           | NULL          | NULL     | NULL
-- 2023 | 1           | 2022          | 1        | 2
--
-- Check: year_gap = 1 ✅ (consecutive)
--        order_count (1) > 1? No, but previous_count (2) > 1? Yes ✅
-- Result: QUALIFIES

-- For Bob:
-- Year | Order Count | Previous Year | Year Gap | Previous Count
-- -----|-------------|---------------|----------|---------------
-- 2022 | 1           | NULL          | NULL     | NULL
-- 2023 | 1           | 2022          | 1        | 1
--
-- Check: year_gap = 1 ✅ (consecutive)
--        order_count (1) > 1? No, previous_count (1) > 1? No ❌
-- Result: DOESN'T QUALIFY

-- For Diana:
-- Year | Order Count | Previous Year | Year Gap | Previous Count
-- -----|-------------|---------------|----------|---------------
-- 2022 | 1           | NULL          | NULL     | NULL
-- 2024 | 2           | 2022          | 2        | 1
--
-- Check: year_gap = 2 ❌ (NOT consecutive - gap year 2023)
-- Result: DOESN'T QUALIFY


-- ============================================
-- ALTERNATIVE: Using SELF JOIN
-- ============================================

WITH customer_years AS (
    SELECT 
        c.customerid,
        c.name,
        EXTRACT(YEAR FROM o.order_date) AS year,
        COUNT(*) AS order_count
    FROM 
        customers_prc c
    JOIN 
        orders_prc o ON c.customerid = o.customer_id
    GROUP BY 
        c.customerid, c.name, EXTRACT(YEAR FROM o.order_date)
)
SELECT DISTINCT
    cy1.name
FROM 
    customer_years cy1
JOIN 
    customer_years cy2 
    ON cy1.customerid = cy2.customerid 
    AND cy2.year = cy1.year + 1  -- Consecutive year
WHERE 
    cy1.order_count > 1 OR cy2.order_count > 1  -- At least one year has 2+ orders
ORDER BY 
    cy1.name;


-- ============================================
-- PRACTICE VARIATIONS
-- ============================================

-- Practice 1: Find customers with 3+ consecutive years
-- Hint: Check for year - LAG(year) = 1 AND year - LAG(year, 2) = 2

-- Practice 2: Find customers with 2+ orders in BOTH consecutive years
-- Hint: Change OR to AND in the filter

-- Practice 3: Show which specific years were consecutive for each customer
-- Hint: SELECT year, previous_year in the final output

-- Practice 4: Find customers with the longest streak of consecutive years
-- Hint: Use a running count with CASE statements


-- ============================================
-- KEY CONCEPTS
-- ============================================
-- 1. LAG(): Gets the previous row's value (previous year)
-- 2. PARTITION BY: Resets LAG for each customer
-- 3. Consecutive check: year - previous_year = 1
-- 4. "At least one": Use OR condition
-- 5. DISTINCT: Removes duplicate customer names
