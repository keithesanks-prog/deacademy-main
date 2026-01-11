-- ============================================
-- RANK() and ROW_NUMBER() with PARTITION BY
-- ============================================
-- Hands-on practice for mastering ranking within groups

-- ============================================
-- SETUP: Employee Sales Data
-- ============================================
DROP TABLE IF EXISTS employee_sales CASCADE;

CREATE TABLE employee_sales (
    employee_id INT,
    employee_name VARCHAR(100),
    department VARCHAR(50),
    region VARCHAR(50),
    sales_amount DECIMAL(10,2)
);

INSERT INTO employee_sales VALUES
-- Sales Department
(1, 'Alice', 'Sales', 'East', 5000),
(2, 'Bob', 'Sales', 'East', 7000),
(3, 'Charlie', 'Sales', 'East', 7000),  -- Tie with Bob!
(4, 'Diana', 'Sales', 'West', 9000),
(5, 'Eve', 'Sales', 'West', 6000),
-- Engineering Department
(6, 'Frank', 'Engineering', 'East', 8000),
(7, 'Grace', 'Engineering', 'East', 8000),  -- Tie with Frank!
(8, 'Henry', 'Engineering', 'West', 10000),
(9, 'Iris', 'Engineering', 'West', 5500);

SELECT * FROM employee_sales ORDER BY department, region, sales_amount DESC;


-- ============================================
-- PART 1: ROW_NUMBER() - Always Unique
-- ============================================
-- ROW_NUMBER() assigns a unique sequential number to each row
-- Even if values are tied, each row gets a different number

SELECT
    employee_name,
    department,
    region,
    sales_amount,
    -- ROW_NUMBER without PARTITION BY: Ranks across ALL rows
    ROW_NUMBER() OVER (ORDER BY sales_amount DESC) AS overall_row_num,
    -- ROW_NUMBER with PARTITION BY department: Ranks within each department
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY sales_amount DESC) AS dept_row_num,
    -- ROW_NUMBER with PARTITION BY region: Ranks within each region
    ROW_NUMBER() OVER (PARTITION BY region ORDER BY sales_amount DESC) AS region_row_num
FROM employee_sales
ORDER BY department, region, sales_amount DESC;

-- Key Observation:
-- Bob and Charlie both have $7000, but ROW_NUMBER gives them different numbers (2, 3)
-- The order between ties is arbitrary (depends on physical row order)


-- ============================================
-- PART 2: RANK() - Handles Ties, Skips Numbers
-- ============================================
-- RANK() gives the same rank to tied values
-- After a tie, it SKIPS numbers (1, 2, 2, 4, 5...)

SELECT
    employee_name,
    department,
    sales_amount,
    -- RANK without PARTITION BY: Ranks across ALL rows
    RANK() OVER (ORDER BY sales_amount DESC) AS overall_rank,
    -- RANK with PARTITION BY department: Ranks within each department
    RANK() OVER (PARTITION BY department ORDER BY sales_amount DESC) AS dept_rank
FROM employee_sales
ORDER BY department, sales_amount DESC;

-- Key Observation:
-- Bob and Charlie both get rank 2 (tied at $7000)
-- The next person (Alice) gets rank 4 (skips 3!)


-- ============================================
-- PART 3: Side-by-Side Comparison
-- ============================================

SELECT
    employee_name,
    department,
    sales_amount,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY sales_amount DESC) AS row_num,
    RANK() OVER (PARTITION BY department ORDER BY sales_amount DESC) AS rank,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY sales_amount DESC) AS dense_rank
FROM employee_sales
ORDER BY department, sales_amount DESC;

-- Expected Output for Sales Department:
-- employee_name | dept  | sales | row_num | rank | dense_rank
-- --------------|-------|-------|---------|------|------------
-- Diana         | Sales | 9000  | 1       | 1    | 1
-- Bob           | Sales | 7000  | 2       | 2    | 2
-- Charlie       | Sales | 7000  | 3       | 2    | 2  ← Same rank!
-- Eve           | Sales | 6000  | 4       | 4    | 3  ← RANK skips 3
-- Alice         | Sales | 5000  | 5       | 5    | 4


-- ============================================
-- PART 4: PARTITION BY Multiple Columns
-- ============================================
-- You can partition by MORE than one column!

SELECT
    employee_name,
    department,
    region,
    sales_amount,
    -- Rank within each department AND region combination
    RANK() OVER (PARTITION BY department, region ORDER BY sales_amount DESC) AS dept_region_rank
FROM employee_sales
ORDER BY department, region, sales_amount DESC;

-- This creates separate rankings for:
-- - Sales + East
-- - Sales + West
-- - Engineering + East
-- - Engineering + West


-- ============================================
-- PART 5: Finding Top N Per Group
-- ============================================
-- Most common use case: Find top performers in each group

-- Find the top 2 salespeople in each department
WITH ranked_employees AS (
    SELECT
        employee_name,
        department,
        sales_amount,
        RANK() OVER (PARTITION BY department ORDER BY sales_amount DESC) AS dept_rank
    FROM employee_sales
)
SELECT
    department,
    employee_name,
    sales_amount,
    dept_rank
FROM ranked_employees
WHERE dept_rank <= 2  -- Top 2 per department
ORDER BY department, dept_rank;


-- ============================================
-- PRACTICE PROBLEM 1: Top Seller Per Region
-- ============================================
-- Find the employee with the highest sales in EACH region

-- Step 1: Add ranking (SCAFFOLDING)
SELECT
    employee_name,
    region,
    sales_amount,
    RANK() OVER (PARTITION BY region ORDER BY sales_amount DESC) AS region_rank
FROM employee_sales
ORDER BY region, region_rank;

-- Step 2: Filter to rank 1 only (DE-SCAFFOLDING)
WITH ranked AS (
    SELECT
        employee_name,
        region,
        sales_amount,
        RANK() OVER (PARTITION BY region ORDER BY sales_amount DESC) AS region_rank
    FROM employee_sales
)
SELECT region, employee_name, sales_amount
FROM ranked
WHERE region_rank = 1
ORDER BY region;


-- ============================================
-- PRACTICE PROBLEM 2: Bottom Performer Per Department
-- ============================================
-- Find the employee with the LOWEST sales in each department

-- Hint: Change ORDER BY sales_amount DESC to ASC

WITH ranked AS (
    SELECT
        employee_name,
        department,
        sales_amount,
        RANK() OVER (PARTITION BY department ORDER BY sales_amount ASC) AS dept_rank
    FROM employee_sales
)
SELECT department, employee_name, sales_amount
FROM ranked
WHERE dept_rank = 1
ORDER BY department;


-- ============================================
-- PRACTICE PROBLEM 3: Exclude Ties
-- ============================================
-- What if you want ONLY ONE winner per department, even if there's a tie?
-- Use ROW_NUMBER() instead of RANK()!

WITH ranked AS (
    SELECT
        employee_name,
        department,
        sales_amount,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY sales_amount DESC) AS dept_row
    FROM employee_sales
)
SELECT department, employee_name, sales_amount
FROM ranked
WHERE dept_row = 1
ORDER BY department;

-- This guarantees exactly 1 result per department


-- ============================================
-- WHEN TO USE WHICH FUNCTION
-- ============================================

-- Use ROW_NUMBER() when:
-- ✓ You need exactly N results per group (no ties)
-- ✓ You want unique sequential numbers
-- ✓ Tie-breaking doesn't matter

-- Use RANK() when:
-- ✓ You want to honor ties (both get same rank)
-- ✓ You're okay with skipping numbers after ties
-- ✓ You want "true" rankings (like sports standings)

-- Use DENSE_RANK() when:
-- ✓ You want to honor ties
-- ✓ You DON'T want to skip numbers
-- ✓ You want consecutive rankings (1, 2, 2, 3, 4...)


-- ============================================
-- YOUR TURN: Practice Exercises
-- ============================================

-- Exercise 1: Find the top 3 employees overall (across all departments)
-- Hint: Don't use PARTITION BY, just ORDER BY

-- Exercise 2: Find employees who are ranked #1 in their department
-- Hint: Use PARTITION BY department

-- Exercise 3: Find employees who are in the top 2 in BOTH their department AND region
-- Hint: You'll need two separate RANK() columns

-- Exercise 4: Count how many employees are tied for each rank in Sales
-- Hint: Use GROUP BY on the rank column


-- ============================================
-- KEY TAKEAWAYS
-- ============================================
-- 1. PARTITION BY: Creates separate groups for ranking
-- 2. ORDER BY: Determines the ranking order within each partition
-- 3. ROW_NUMBER(): Always unique (1, 2, 3, 4, 5...)
-- 4. RANK(): Honors ties, skips numbers (1, 2, 2, 4, 5...)
-- 5. DENSE_RANK(): Honors ties, no gaps (1, 2, 2, 3, 4...)
-- 6. Without PARTITION BY: Ranks across ALL rows
-- 7. With PARTITION BY: Ranks reset for each group
