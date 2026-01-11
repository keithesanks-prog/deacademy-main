-- ============================================
-- FINDING MISSING DATA: Months with No Orders
-- ============================================
-- Goal: Identify months in 2023 that had zero orders

-- ============================================
-- THE STRATEGY
-- ============================================
-- 1. Generate a list of ALL months (1-12)
-- 2. Count actual orders per month
-- 3. LEFT JOIN to find months with no orders
-- 4. Filter for NULL (no matches = no orders)

-- ============================================
-- SETUP: Sample Data
-- ============================================
DROP TABLE IF EXISTS orders_prc CASCADE;

CREATE TABLE orders_prc (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    amount INT
);

INSERT INTO orders_prc VALUES
-- January: 2 orders
(101, 1, '2023-01-15', 100),
(102, 2, '2023-01-20', 200),
-- February: 0 orders (MISSING!)
-- March: 1 order
(103, 3, '2023-03-10', 150),
-- April: 0 orders (MISSING!)
-- May: 2 orders
(104, 1, '2023-05-05', 300),
(105, 2, '2023-05-15', 250),
-- June-December: 0 orders (MISSING!)
-- Some 2022 orders (should be excluded)
(106, 3, '2022-12-25', 500);

SELECT * FROM orders_prc ORDER BY order_date;


-- ============================================
-- MYSQL VERSION (Original - Won't work in PostgreSQL!)
-- ============================================
/*
-- ❌ MYSQL SYNTAX:
WITH AllMonths AS (
    SELECT 1 AS month_num UNION ALL SELECT 2 UNION ALL SELECT 3 ...
),
MonthlyOrders AS (
    SELECT
        MONTH(order_date) AS month_num,  -- MySQL function
        COUNT(order_id) AS order_count
    FROM orders_prc
    WHERE YEAR(order_date) = 2023       -- MySQL function
    GROUP BY MONTH(order_date)
)
SELECT
    CONCAT('2023', '-', LPAD(am.month_num, 2, '0')) AS order_month_year_formatted
FROM AllMonths am
LEFT JOIN MonthlyOrders mo ON am.month_num = mo.month_num
WHERE mo.order_count IS NULL;
*/


-- ============================================
-- POSTGRESQL VERSION (Use this!)
-- ============================================

WITH AllMonths AS (
    -- Generate all 12 months
    SELECT 1 AS month_num UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL
    SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL
    SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL
    SELECT 12
),
MonthlyOrders AS (
    -- Count actual orders per month
    SELECT
        EXTRACT(MONTH FROM order_date) AS month_num,
        COUNT(order_id) AS order_count
    FROM orders_prc
    WHERE EXTRACT(YEAR FROM order_date) = 2023
    GROUP BY EXTRACT(MONTH FROM order_date)
)
SELECT
    -- Format as '2023-01', '2023-02', etc.
    CONCAT('2023-', LPAD(am.month_num::TEXT, 2, '0')) AS order_month_year_formatted
FROM AllMonths am
LEFT JOIN MonthlyOrders mo ON am.month_num = mo.month_num
WHERE mo.order_count IS NULL  -- Only months with NO orders
ORDER BY am.month_num;

-- Expected Output:
-- order_month_year_formatted
-- --------------------------
-- 2023-02
-- 2023-04
-- 2023-06
-- 2023-07
-- 2023-08
-- 2023-09
-- 2023-10
-- 2023-11
-- 2023-12


-- ============================================
-- ALTERNATIVE: Using generate_series (PostgreSQL)
-- ============================================
-- PostgreSQL has a built-in function to generate sequences!

WITH AllMonths AS (
    -- Generate 1-12 using generate_series
    SELECT generate_series(1, 12) AS month_num
),
MonthlyOrders AS (
    SELECT
        EXTRACT(MONTH FROM order_date) AS month_num,
        COUNT(order_id) AS order_count
    FROM orders_prc
    WHERE EXTRACT(YEAR FROM order_date) = 2023
    GROUP BY EXTRACT(MONTH FROM order_date)
)
SELECT
    CONCAT('2023-', LPAD(am.month_num::TEXT, 2, '0')) AS order_month_year_formatted
FROM AllMonths am
LEFT JOIN MonthlyOrders mo ON am.month_num = mo.month_num
WHERE mo.order_count IS NULL
ORDER BY am.month_num;


-- ============================================
-- SCAFFOLDING: See ALL months with counts
-- ============================================
-- Remove the WHERE clause to see ALL months (including those with orders)

WITH AllMonths AS (
    SELECT generate_series(1, 12) AS month_num
),
MonthlyOrders AS (
    SELECT
        EXTRACT(MONTH FROM order_date) AS month_num,
        COUNT(order_id) AS order_count
    FROM orders_prc
    WHERE EXTRACT(YEAR FROM order_date) = 2023
    GROUP BY EXTRACT(MONTH FROM order_date)
)
SELECT
    CONCAT('2023-', LPAD(am.month_num::TEXT, 2, '0')) AS month_formatted,
    COALESCE(mo.order_count, 0) AS order_count,  -- Show 0 for missing months
    CASE 
        WHEN mo.order_count IS NULL THEN 'No Orders ✗'
        ELSE 'Has Orders ✓'
    END AS status
FROM AllMonths am
LEFT JOIN MonthlyOrders mo ON am.month_num = mo.month_num
ORDER BY am.month_num;

-- Result shows ALL months:
-- month_formatted | order_count | status
-- ----------------|-------------|-------------
-- 2023-01         | 2           | Has Orders ✓
-- 2023-02         | 0           | No Orders ✗
-- 2023-03         | 1           | Has Orders ✓
-- 2023-04         | 0           | No Orders ✗
-- 2023-05         | 2           | Has Orders ✓
-- ...


-- ============================================
-- HOW LEFT JOIN FINDS MISSING DATA
-- ============================================

-- Step 1: AllMonths CTE creates:
-- month_num
-- ---------
-- 1
-- 2
-- 3
-- ...
-- 12

-- Step 2: MonthlyOrders CTE creates (only months with orders):
-- month_num | order_count
-- ----------|------------
-- 1         | 2
-- 3         | 1
-- 5         | 2

-- Step 3: LEFT JOIN keeps ALL rows from AllMonths:
-- am.month_num | mo.month_num | mo.order_count
-- -------------|--------------|---------------
-- 1            | 1            | 2              ← Match found
-- 2            | NULL         | NULL           ← No match (missing!)
-- 3            | 3            | 1              ← Match found
-- 4            | NULL         | NULL           ← No match (missing!)
-- 5            | 5            | 2              ← Match found
-- ...

-- Step 4: WHERE mo.order_count IS NULL filters to only missing months


-- ============================================
-- BONUS: Show Month Names Instead of Numbers
-- ============================================

WITH AllMonths AS (
    SELECT generate_series(1, 12) AS month_num
),
MonthlyOrders AS (
    SELECT
        EXTRACT(MONTH FROM order_date) AS month_num,
        COUNT(order_id) AS order_count
    FROM orders_prc
    WHERE EXTRACT(YEAR FROM order_date) = 2023
    GROUP BY EXTRACT(MONTH FROM order_date)
)
SELECT
    TO_CHAR(TO_DATE(am.month_num::TEXT, 'MM'), 'Month') AS month_name,
    CONCAT('2023-', LPAD(am.month_num::TEXT, 2, '0')) AS month_formatted
FROM AllMonths am
LEFT JOIN MonthlyOrders mo ON am.month_num = mo.month_num
WHERE mo.order_count IS NULL
ORDER BY am.month_num;

-- Result:
-- month_name | month_formatted
-- -----------|----------------
-- February   | 2023-02
-- April      | 2023-04
-- June       | 2023-06
-- ...


-- ============================================
-- COMMON USE CASES FOR THIS PATTERN
-- ============================================

-- 1. Find missing months (this example)
-- 2. Find missing days in a date range
-- 3. Find missing categories (e.g., products with no sales)
-- 4. Find missing employees (e.g., who didn't submit timesheets)
-- 5. Fill gaps in time series data for charts


-- ============================================
-- PRACTICE VARIATIONS
-- ============================================

-- Practice 1: Find months with FEWER than 5 orders
-- Hint: Change WHERE mo.order_count IS NULL to WHERE COALESCE(mo.order_count, 0) < 5

-- Practice 2: Find missing days in January 2023
-- Hint: Use generate_series('2023-01-01'::date, '2023-01-31'::date, '1 day')

-- Practice 3: Show ALL months with their order counts (0 for missing)
-- Hint: Remove the WHERE clause, use COALESCE(mo.order_count, 0)

-- Practice 4: Find which customers placed NO orders in 2023
-- Hint: Generate list of all customers, LEFT JOIN to orders


-- ============================================
-- KEY CONCEPTS
-- ============================================
-- 1. Generate a complete list (all months, all days, etc.)
-- 2. LEFT JOIN to actual data
-- 3. WHERE ... IS NULL finds missing data
-- 4. COALESCE(..., 0) shows 0 for missing values
-- 5. This pattern works for any "find what's missing" problem
