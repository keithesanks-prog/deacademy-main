-- ============================================
-- RUNNING TOTALS: Cumulative Calculations
-- ============================================
-- Goal: Calculate cumulative sums using SUM() OVER (ORDER BY ...)

-- ============================================
-- WHAT IS A RUNNING TOTAL?
-- ============================================
-- A running total (cumulative sum) adds up values as you go through rows
-- Example: Daily sales → Cumulative sales for the year

-- Day 1: $100 → Running total: $100
-- Day 2: $150 → Running total: $250 ($100 + $150)
-- Day 3: $200 → Running total: $450 ($100 + $150 + $200)

-- ============================================
-- SETUP: Sample Data
-- ============================================
DROP TABLE IF EXISTS daily_sales CASCADE;

CREATE TABLE daily_sales (
    sale_date DATE,
    product VARCHAR(50),
    amount DECIMAL(10,2)
);

INSERT INTO daily_sales VALUES
('2024-01-01', 'Laptop', 1200),
('2024-01-02', 'Mouse', 25),
('2024-01-03', 'Keyboard', 75),
('2024-01-04', 'Monitor', 450),
('2024-01-05', 'Desk', 350),
('2024-01-06', 'Chair', 200);

SELECT * FROM daily_sales ORDER BY sale_date;


-- ============================================
-- BASIC RUNNING TOTAL
-- ============================================

SELECT
    sale_date,
    product,
    amount,
    -- Running total: Sum of all amounts up to and including this row
    SUM(amount) OVER (ORDER BY sale_date) AS running_total
FROM daily_sales
ORDER BY sale_date;

-- Expected Output:
-- sale_date  | product  | amount | running_total
-- -----------|----------|--------|---------------
-- 2024-01-01 | Laptop   | 1200   | 1200
-- 2024-01-02 | Mouse    | 25     | 1225  (1200 + 25)
-- 2024-01-03 | Keyboard | 75     | 1300  (1200 + 25 + 75)
-- 2024-01-04 | Monitor  | 450    | 1750  (1200 + 25 + 75 + 450)
-- 2024-01-05 | Desk     | 350    | 2100
-- 2024-01-06 | Chair    | 200    | 2300


-- ============================================
-- HOW IT WORKS: Frame Specification
-- ============================================

-- SUM(amount) OVER (ORDER BY sale_date)
-- Is shorthand for:
-- SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- Translation:
-- "Sum all rows from the beginning (UNBOUNDED PRECEDING) 
--  up to and including the current row (CURRENT ROW)"


-- ============================================
-- RUNNING TOTAL PER CATEGORY
-- ============================================

DROP TABLE IF EXISTS sales_by_category CASCADE;

CREATE TABLE sales_by_category (
    sale_date DATE,
    category VARCHAR(50),
    amount DECIMAL(10,2)
);

INSERT INTO sales_by_category VALUES
('2024-01-01', 'Electronics', 1200),
('2024-01-02', 'Electronics', 450),
('2024-01-03', 'Furniture', 350),
('2024-01-04', 'Electronics', 75),
('2024-01-05', 'Furniture', 200),
('2024-01-06', 'Furniture', 150);

-- Running total PER CATEGORY
SELECT
    sale_date,
    category,
    amount,
    -- Overall running total
    SUM(amount) OVER (ORDER BY sale_date) AS overall_running_total,
    -- Running total PER CATEGORY (resets for each category)
    SUM(amount) OVER (PARTITION BY category ORDER BY sale_date) AS category_running_total
FROM sales_by_category
ORDER BY sale_date;

-- Expected Output:
-- sale_date  | category    | amount | overall_rt | category_rt
-- -----------|-------------|--------|------------|------------
-- 2024-01-01 | Electronics | 1200   | 1200       | 1200
-- 2024-01-02 | Electronics | 450    | 1650       | 1650  (1200+450)
-- 2024-01-03 | Furniture   | 350    | 2000       | 350   (resets!)
-- 2024-01-04 | Electronics | 75     | 2075       | 1725  (1200+450+75)
-- 2024-01-05 | Furniture   | 200    | 2275       | 550   (350+200)
-- 2024-01-06 | Furniture   | 150    | 2425       | 700   (350+200+150)


-- ============================================
-- RUNNING AVERAGE
-- ============================================

SELECT
    sale_date,
    amount,
    -- Running total
    SUM(amount) OVER (ORDER BY sale_date) AS running_total,
    -- Running average
    AVG(amount) OVER (ORDER BY sale_date) AS running_average,
    -- Running count
    COUNT(*) OVER (ORDER BY sale_date) AS running_count
FROM daily_sales
ORDER BY sale_date;


-- ============================================
-- MOVING AVERAGE (Last 3 Days)
-- ============================================

SELECT
    sale_date,
    amount,
    -- Average of current row and 2 preceding rows
    AVG(amount) OVER (
        ORDER BY sale_date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3day
FROM daily_sales
ORDER BY sale_date;

-- Expected Output:
-- sale_date  | amount | moving_avg_3day
-- -----------|--------|----------------
-- 2024-01-01 | 1200   | 1200.00  (only 1 row)
-- 2024-01-02 | 25     | 612.50   (1200+25)/2
-- 2024-01-03 | 75     | 433.33   (1200+25+75)/3
-- 2024-01-04 | 450    | 183.33   (25+75+450)/3
-- 2024-01-05 | 350    | 291.67   (75+450+350)/3
-- 2024-01-06 | 200    | 333.33   (450+350+200)/3


-- ============================================
-- PERCENTAGE OF TOTAL
-- ============================================

SELECT
    sale_date,
    product,
    amount,
    -- Running total
    SUM(amount) OVER (ORDER BY sale_date) AS running_total,
    -- Total (same for all rows)
    SUM(amount) OVER () AS grand_total,
    -- Percentage of total so far
    ROUND(
        SUM(amount) OVER (ORDER BY sale_date) * 100.0 / SUM(amount) OVER (),
        2
    ) AS percent_of_total
FROM daily_sales
ORDER BY sale_date;


-- ============================================
-- SCAFFOLDING: Verify the Calculation
-- ============================================

SELECT
    sale_date,
    amount,
    -- SCAFFOLDING: Show individual amounts being summed
    STRING_AGG(amount::TEXT, ' + ' ORDER BY sale_date) 
        OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS calculation,
    -- The actual running total
    SUM(amount) OVER (ORDER BY sale_date) AS running_total
FROM daily_sales
ORDER BY sale_date;

-- Shows: "1200", "1200 + 25", "1200 + 25 + 75", etc.


-- ============================================
-- COMMON FRAME SPECIFICATIONS
-- ============================================

-- 1. Running total (all previous rows + current)
SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

-- 2. Moving average (last 3 rows including current)
AVG(amount) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)

-- 3. Moving average (last 7 days)
AVG(amount) OVER (ORDER BY date RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW)

-- 4. Total of current and next row
SUM(amount) OVER (ORDER BY date ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING)

-- 5. Total of all rows (grand total)
SUM(amount) OVER ()


-- ============================================
-- PRACTICE VARIATIONS
-- ============================================

-- Practice 1: Calculate running total of sales by month
-- Hint: GROUP BY month first, then apply running total

-- Practice 2: Calculate percentage growth from running total
-- Hint: Use LAG() on the running_total column

-- Practice 3: Find when cumulative sales exceeded $1000
-- Hint: Use CASE or WHERE on running_total

-- Practice 4: Calculate moving average for last 7 days
-- Hint: Use RANGE BETWEEN INTERVAL '6 days' PRECEDING


-- ============================================
-- KEY CONCEPTS
-- ============================================
-- 1. SUM() OVER (ORDER BY ...): Running total
-- 2. PARTITION BY: Resets running total per group
-- 3. ROWS BETWEEN: Defines which rows to include
-- 4. UNBOUNDED PRECEDING: From the start
-- 5. CURRENT ROW: Up to and including this row
-- 6. N PRECEDING: N rows before current
-- 7. N FOLLOWING: N rows after current
