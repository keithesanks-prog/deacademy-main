-- ============================================
-- REVENUE GROWTH: APRIL TO MAY 2023
-- ============================================
-- Goal: Calculate total revenue growth from April to May 2023

-- ============================================
-- TERMINOLOGY (IMPORTANT!)
-- ============================================
-- "Growth" = DIFFERENTIAL (the change/difference between two values)
-- NOT the total revenue itself!

-- Example with our data:
-- April Revenue (TOTAL):     $1,400
-- May Revenue (TOTAL):       $2,400
-- Revenue Growth (DIFFERENTIAL): $2,400 - $1,400 = $1,000
-- Growth Rate (PERCENTAGE):  ($1,000 / $1,400) × 100 = 71.43%

-- Key Terms:
-- • TOTAL/SUM: The actual amount (e.g., "May had $2,400 in revenue")
-- • GROWTH/CHANGE/DIFFERENTIAL: The difference between periods (e.g., "Revenue grew by $1,000")
-- • GROWTH RATE: The percentage change (e.g., "Revenue grew by 71.43%")

-- Think of it like temperature:
-- • Monday: 70°F (TOTAL/ACTUAL)
-- • Tuesday: 85°F (TOTAL/ACTUAL)
-- • Temperature Change: +15°F (DIFFERENTIAL/GROWTH)
-- • Percentage Change: +21.4% (GROWTH RATE)

-- Goal: Calculate total revenue growth from April to May 2023

-- ============================================
-- SETUP: Create table and sample data
-- ============================================
DROP TABLE IF EXISTS orders_prc CASCADE;

CREATE TABLE orders_prc (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    amount INT
);

INSERT INTO orders_prc VALUES
-- March 2023 (for context)
(101, 1, '2023-03-10', 100),
(102, 2, '2023-03-15', 200),
(103, 3, '2023-03-20', 150),
-- April 2023
(104, 1, '2023-04-05', 300),
(105, 2, '2023-04-10', 400),
(106, 3, '2023-04-15', 500),
(107, 4, '2023-04-20', 200),  -- April Total: 1400
-- May 2023
(108, 1, '2023-05-05', 600),
(109, 2, '2023-05-10', 700),
(110, 3, '2023-05-15', 800),
(111, 4, '2023-05-20', 300),  -- May Total: 2400
-- June 2023 (for context)
(112, 1, '2023-06-05', 500);

-- Verify the data
SELECT * FROM orders_prc ORDER BY order_date;


-- ============================================
-- STEP 1: View Monthly Revenue
-- ============================================
-- First, let's see the revenue for each month

-- PostgreSQL version (use TO_CHAR)
SELECT 
    TO_CHAR(order_date, 'YYYY-MM') AS month,
    SUM(amount) AS total_revenue
FROM 
    orders_prc
WHERE 
    order_date >= '2023-04-01' AND order_date < '2023-06-01'
GROUP BY 
    TO_CHAR(order_date, 'YYYY-MM')
ORDER BY 
    month;

-- Expected Output:
-- month   | total_revenue
-- --------|-------------
-- 2023-04 | 1400
-- 2023-05 | 2400


-- ============================================
-- SOLUTION 1: Using LAG() for Growth Calculation
-- ============================================
-- This is the cleanest approach using window functions

WITH monthly_revenue AS (
    SELECT 
        TO_CHAR(order_date, 'YYYY-MM') AS month,
        SUM(amount) AS total_revenue
    FROM 
        orders_prc
    WHERE 
        EXTRACT(YEAR FROM order_date) = 2023
    GROUP BY 
        TO_CHAR(order_date, 'YYYY-MM')
)
SELECT 
    month,
    total_revenue,
    LAG(total_revenue) OVER (ORDER BY month) AS previous_month_revenue,
    total_revenue - LAG(total_revenue) OVER (ORDER BY month) AS revenue_growth,
    ROUND(
        (total_revenue - LAG(total_revenue) OVER (ORDER BY month)) 
        / LAG(total_revenue) OVER (ORDER BY month)::DECIMAL * 100, 
        2
    ) AS growth_percentage
FROM 
    monthly_revenue
WHERE 
    month IN ('2023-04', '2023-05')
ORDER BY 
    month;

-- Expected Output:
-- month   | total_revenue | previous_month_revenue | revenue_growth | growth_percentage
-- --------|---------------|------------------------|----------------|------------------
-- 2023-04 | 1400          | NULL                   | NULL           | NULL
-- 2023-05 | 2400          | 1400                   | 1000           | 71.43


-- ============================================
-- SOLUTION 2: EXACT FORMAT (Single Number)
-- ============================================
-- This matches the expected output format exactly

SELECT 
    (SELECT SUM(amount) FROM orders_prc 
     WHERE order_date >= '2023-05-01' AND order_date < '2023-06-01') 
    -
    (SELECT SUM(amount) FROM orders_prc 
     WHERE order_date >= '2023-04-01' AND order_date < '2023-05-01')
    AS RevenueGrowth;

-- Expected Output:
-- RevenueGrowth
-- -------------
-- 1000


-- ============================================
-- SOLUTION 3: Alternative Using CASE
-- ============================================
-- Same result, different approach

SELECT 
    SUM(CASE WHEN order_date >= '2023-05-01' AND order_date < '2023-06-01' 
             THEN amount ELSE 0 END)
    -
    SUM(CASE WHEN order_date >= '2023-04-01' AND order_date < '2023-05-01' 
             THEN amount ELSE 0 END)
    AS RevenueGrowth
FROM 
    orders_prc;


-- ============================================
-- SOLUTION 4: Direct Calculation (Simpler)
-- ============================================
-- Calculate growth between two specific months

SELECT 
    (SELECT SUM(amount) FROM orders_prc 
     WHERE order_date >= '2023-05-01' AND order_date < '2023-06-01') 
    -
    (SELECT SUM(amount) FROM orders_prc 
     WHERE order_date >= '2023-04-01' AND order_date < '2023-05-01')
    AS revenue_growth;

-- Expected Output:
-- revenue_growth
-- --------------
-- 1000


-- ============================================
-- SOLUTION 3: Using FILTER (PostgreSQL Specific)
-- ============================================
-- This is a very clean PostgreSQL feature

SELECT 
    SUM(amount) FILTER (WHERE order_date >= '2023-05-01' AND order_date < '2023-06-01') AS may_revenue,
    SUM(amount) FILTER (WHERE order_date >= '2023-04-01' AND order_date < '2023-05-01') AS april_revenue,
    SUM(amount) FILTER (WHERE order_date >= '2023-05-01' AND order_date < '2023-06-01')
    -
    SUM(amount) FILTER (WHERE order_date >= '2023-04-01' AND order_date < '2023-05-01') AS revenue_growth
FROM 
    orders_prc;

-- Expected Output:
-- may_revenue | april_revenue | revenue_growth
-- ------------|---------------|---------------
-- 2400        | 1400          | 1000


-- ============================================
-- SOLUTION 4: Using CASE (Works Everywhere)
-- ============================================
-- Most portable solution across all SQL databases

SELECT 
    SUM(CASE WHEN order_date >= '2023-05-01' AND order_date < '2023-06-01' 
             THEN amount ELSE 0 END) AS may_revenue,
    SUM(CASE WHEN order_date >= '2023-04-01' AND order_date < '2023-05-01' 
             THEN amount ELSE 0 END) AS april_revenue,
    SUM(CASE WHEN order_date >= '2023-05-01' AND order_date < '2023-06-01' 
             THEN amount ELSE 0 END)
    -
    SUM(CASE WHEN order_date >= '2023-04-01' AND order_date < '2023-05-01' 
             THEN amount ELSE 0 END) AS revenue_growth
FROM 
    orders_prc;


-- ============================================
-- BONUS: Growth Percentage Calculation
-- ============================================

WITH monthly_totals AS (
    SELECT 
        SUM(CASE WHEN order_date >= '2023-04-01' AND order_date < '2023-05-01' 
                 THEN amount ELSE 0 END) AS april_revenue,
        SUM(CASE WHEN order_date >= '2023-05-01' AND order_date < '2023-06-01' 
                 THEN amount ELSE 0 END) AS may_revenue
    FROM orders_prc
)
SELECT 
    april_revenue,
    may_revenue,
    may_revenue - april_revenue AS revenue_growth,
    ROUND(
        (may_revenue - april_revenue)::DECIMAL / april_revenue * 100, 
        2
    ) AS growth_percentage
FROM 
    monthly_totals;

-- Expected Output:
-- april_revenue | may_revenue | revenue_growth | growth_percentage
-- --------------|-------------|----------------|------------------
-- 1400          | 2400        | 1000           | 71.43


-- ============================================
-- PRACTICE VARIATIONS
-- ============================================

-- Practice 1: Calculate growth from May to June 2023
-- Hint: Change the date ranges

-- Practice 2: Show growth for ALL consecutive months in 2023
-- Hint: Use LAG() without filtering specific months

-- Practice 3: Find which month had the highest growth
-- Hint: Use RANK() or MAX on the growth column

-- Practice 4: Calculate average monthly growth for 2023
-- Hint: Use AVG() on the growth values


-- ============================================
-- KEY CONCEPTS
-- ============================================
-- 1. Date Formatting: TO_CHAR(date, 'YYYY-MM') in PostgreSQL
-- 2. Date Filtering: Use >= and < for month ranges
-- 3. LAG(): Compare current row to previous row
-- 4. FILTER: PostgreSQL-specific conditional aggregation
-- 5. CASE: Portable conditional aggregation
-- 6. Growth Formula: (New - Old) / Old * 100
