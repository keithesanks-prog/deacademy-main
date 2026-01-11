-- ============================================
-- CASE vs GROUP BY: When to Use Each
-- ============================================
-- Understanding the difference between row-level logic and aggregation

-- ============================================
-- THE KEY DIFFERENCE
-- ============================================
-- CASE: Tests a condition for EACH ROW, returns a single value per row
-- GROUP BY + AVG(): Aggregates MULTIPLE ROWS into one result per group

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
-- January 2022
(101, 1, '2022-01-10', 100),
(102, 2, '2022-01-15', 200),
(103, 3, '2022-01-20', 150),  -- Jan avg: (100+200+150)/3 = 150
-- February 2022
(104, 1, '2022-02-05', 300),
(105, 2, '2022-02-10', 400),  -- Feb avg: (300+400)/2 = 350
-- March 2022
(106, 3, '2022-03-12', 250),  -- Mar avg: 250/1 = 250
-- Some 2023 orders (should be excluded)
(107, 1, '2023-01-15', 500);

SELECT * FROM orders_prc ORDER BY order_date;


-- ============================================
-- WRONG APPROACH: Using CASE (Doesn't work!)
-- ============================================
-- ❌ This is what you might try, but it's WRONG

/*
SELECT
    order_date,
    amount,
    CASE 
        WHEN EXTRACT(MONTH FROM order_date) = 1 THEN AVG(amount)  -- ERROR!
        WHEN EXTRACT(MONTH FROM order_date) = 2 THEN AVG(amount)  -- ERROR!
        ...
    END AS monthly_average
FROM orders_prc
WHERE EXTRACT(YEAR FROM order_date) = 2022;
*/

-- Why it's wrong:
-- 1. CASE operates on EACH ROW individually
-- 2. AVG() needs multiple rows to calculate an average
-- 3. You can't use AVG() inside CASE without GROUP BY


-- ============================================
-- CORRECT APPROACH: Using GROUP BY + AVG()
-- ============================================

-- MYSQL VERSION (Original):
/*
SELECT
    YEAR(order_date) AS order_year,
    MONTH(order_date) AS order_month_num,
    AVG(amount) AS average_order_amount
FROM orders_prc
WHERE YEAR(order_date) = 2022
GROUP BY order_year, order_month_num
ORDER BY order_month_num ASC;
*/

-- POSTGRESQL VERSION (Use this!):
SELECT
    -- 1. Extract the year (for filtering)
    EXTRACT(YEAR FROM order_date) AS order_year,
    
    -- 2. Extract the month number (for grouping)
    EXTRACT(MONTH FROM order_date) AS order_month_num,
    
    -- 3. Calculate the average amount for all orders in that group (month)
    AVG(amount) AS average_order_amount
FROM
    orders_prc
WHERE
    EXTRACT(YEAR FROM order_date) = 2022  -- Filters to only 2022
GROUP BY
    order_year,
    order_month_num  -- Groups all orders into monthly buckets
ORDER BY
    order_month_num ASC;  -- Lists results in chronological order

-- Expected Output:
-- order_year | order_month_num | average_order_amount
-- -----------|-----------------|---------------------
-- 2022       | 1               | 150.00
-- 2022       | 2               | 350.00
-- 2022       | 3               | 250.00


-- ============================================
-- HOW GROUP BY WORKS: Step-by-Step
-- ============================================

-- Step 1: Filter to 2022 only
-- order_id | order_date  | amount | month
-- ---------|-------------|--------|------
-- 101      | 2022-01-10  | 100    | 1
-- 102      | 2022-01-15  | 200    | 1
-- 103      | 2022-01-20  | 150    | 1
-- 104      | 2022-02-05  | 300    | 2
-- 105      | 2022-02-10  | 400    | 2
-- 106      | 2022-03-12  | 250    | 3

-- Step 2: GROUP BY month (creates buckets)
-- Month 1 bucket: [100, 200, 150]
-- Month 2 bucket: [300, 400]
-- Month 3 bucket: [250]

-- Step 3: AVG() calculates average for each bucket
-- Month 1: (100 + 200 + 150) / 3 = 150
-- Month 2: (300 + 400) / 2 = 350
-- Month 3: 250 / 1 = 250


-- ============================================
-- WHEN TO USE CASE vs GROUP BY
-- ============================================

-- Use CASE when:
-- ✓ You want to categorize INDIVIDUAL ROWS
-- ✓ You want to create a new column based on row values
-- ✓ You want conditional logic per row

-- Example: Categorize each order as "High" or "Low"
SELECT
    order_id,
    amount,
    CASE 
        WHEN amount >= 200 THEN 'High Value'
        ELSE 'Low Value'
    END AS order_category
FROM orders_prc;

-- Use GROUP BY + Aggregate when:
-- ✓ You want to COMBINE multiple rows into one result
-- ✓ You want to calculate totals, averages, counts, etc.
-- ✓ You want summary statistics per group

-- Example: Calculate average per month (this problem!)


-- ============================================
-- SCAFFOLDING: Verify the Grouping
-- ============================================
-- See which orders are in each group

SELECT
    EXTRACT(MONTH FROM order_date) AS month_num,
    order_id,
    amount,
    -- SCAFFOLDING: Show the average for this month
    AVG(amount) OVER (PARTITION BY EXTRACT(MONTH FROM order_date)) AS monthly_avg,
    -- SCAFFOLDING: Show how many orders in this month
    COUNT(*) OVER (PARTITION BY EXTRACT(MONTH FROM order_date)) AS orders_in_month
FROM orders_prc
WHERE EXTRACT(YEAR FROM order_date) = 2022
ORDER BY month_num, order_id;

-- Result shows EACH ORDER with its month's average:
-- month_num | order_id | amount | monthly_avg | orders_in_month
-- ----------|----------|--------|-------------|----------------
-- 1         | 101      | 100    | 150.00      | 3
-- 1         | 102      | 200    | 150.00      | 3
-- 1         | 103      | 150    | 150.00      | 3
-- 2         | 104      | 300    | 350.00      | 2
-- 2         | 105      | 400    | 350.00      | 2
-- 3         | 106      | 250    | 250.00      | 1


-- ============================================
-- BONUS: Add Month Names
-- ============================================

SELECT
    EXTRACT(YEAR FROM order_date) AS order_year,
    EXTRACT(MONTH FROM order_date) AS order_month_num,
    TO_CHAR(order_date, 'Month') AS month_name,
    AVG(amount) AS average_order_amount,
    COUNT(*) AS order_count  -- How many orders in this month
FROM orders_prc
WHERE EXTRACT(YEAR FROM order_date) = 2022
GROUP BY 
    EXTRACT(YEAR FROM order_date),
    EXTRACT(MONTH FROM order_date),
    TO_CHAR(order_date, 'Month')
ORDER BY order_month_num;

-- Result:
-- order_year | order_month_num | month_name | average_order_amount | order_count
-- -----------|-----------------|------------|----------------------|------------
-- 2022       | 1               | January    | 150.00               | 3
-- 2022       | 2               | February   | 350.00               | 2
-- 2022       | 3               | March      | 250.00               | 1


-- ============================================
-- COMMON MISTAKE: Mixing CASE and Aggregation
-- ============================================

-- ❌ WRONG: Trying to use AVG inside CASE without GROUP BY
/*
SELECT
    CASE 
        WHEN EXTRACT(MONTH FROM order_date) = 1 THEN AVG(amount)
    END
FROM orders_prc;
-- ERROR: AVG needs GROUP BY!
*/

-- ✅ CORRECT: Use GROUP BY to create groups, then AVG
SELECT
    EXTRACT(MONTH FROM order_date) AS month,
    AVG(amount) AS avg_amount
FROM orders_prc
GROUP BY EXTRACT(MONTH FROM order_date);


-- ============================================
-- PRACTICE VARIATIONS
-- ============================================

-- Practice 1: Calculate total (SUM) instead of average per month
-- Hint: Replace AVG(amount) with SUM(amount)

-- Practice 2: Find the month with the highest average
-- Hint: Add ORDER BY average_order_amount DESC LIMIT 1

-- Practice 3: Show only months with average > 200
-- Hint: Add HAVING AVG(amount) > 200

-- Practice 4: Calculate average per customer (not per month)
-- Hint: GROUP BY customer_id instead


-- ============================================
-- KEY TAKEAWAYS
-- ============================================
-- 1. CASE: Row-level logic (one row in, one value out)
-- 2. GROUP BY + AVG(): Multi-row aggregation (many rows in, one result per group)
-- 3. You CANNOT use AVG() inside CASE without GROUP BY
-- 4. For "average per month/category/etc.", use GROUP BY
-- 5. EXTRACT(MONTH FROM date) in PostgreSQL, MONTH(date) in MySQL
