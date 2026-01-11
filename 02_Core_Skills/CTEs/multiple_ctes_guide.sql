-- ============================================
-- MULTIPLE CTEs: CROSS-REFERENCING & CHAINING
-- ============================================
-- Goal: Understand how to use multiple CTEs together and reference them

-- ============================================
-- WHAT ARE CTEs?
-- ============================================
-- CTE = Common Table Expression
-- Think of each CTE as a "temporary table" that exists only for this query
-- You can reference earlier CTEs in later CTEs (like building blocks!)

-- ============================================
-- SETUP: Sample Data
-- ============================================
DROP TABLE IF EXISTS sales CASCADE;

CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(50),
    sale_date DATE,
    amount DECIMAL(10,2)
);

INSERT INTO sales VALUES
(1, 'Laptop', 'Electronics', '2024-01-15', 1200),
(2, 'Mouse', 'Electronics', '2024-01-20', 25),
(3, 'Desk', 'Furniture', '2024-02-10', 350),
(4, 'Chair', 'Furniture', '2024-02-15', 200),
(5, 'Monitor', 'Electronics', '2024-03-05', 450),
(6, 'Keyboard', 'Electronics', '2024-03-10', 75),
(7, 'Lamp', 'Furniture', '2024-04-12', 45),
(8, 'Phone', 'Electronics', '2024-04-20', 800);

SELECT * FROM sales ORDER BY sale_date;


-- ============================================
-- EXAMPLE 1: SINGLE CTE (Review)
-- ============================================
-- Just one temporary table

WITH category_totals AS (
    SELECT 
        category,
        SUM(amount) AS total_sales
    FROM sales
    GROUP BY category
)
SELECT * FROM category_totals;

-- Result:
-- category    | total_sales
-- ------------|------------
-- Electronics | 2550
-- Furniture   | 595


-- ============================================
-- EXAMPLE 2: MULTIPLE CTEs (Chaining)
-- ============================================
-- CTE #2 can reference CTE #1!

WITH category_totals AS (
    -- CTE #1: Calculate totals by category
    SELECT 
        category,
        SUM(amount) AS total_sales
    FROM sales
    GROUP BY category
),
ranked_categories AS (
    -- CTE #2: Rank the categories (references CTE #1!)
    SELECT 
        category,
        total_sales,
        RANK() OVER (ORDER BY total_sales DESC) AS rank
    FROM category_totals  -- ← Referencing the first CTE!
)
-- Final SELECT: Use the last CTE
SELECT * FROM ranked_categories;

-- Result:
-- category    | total_sales | rank
-- ------------|-------------|-----
-- Electronics | 2550        | 1
-- Furniture   | 595         | 2


-- ============================================
-- VISUAL: How CTEs Chain Together
-- ============================================

/*
┌─────────────────────────────────────────────────────────┐
│ WITH category_totals AS (...)                          │
│   ↓                                                     │
│   Creates temporary table:                             │
│   ┌──────────────┬─────────────┐                      │
│   │ category     │ total_sales │                      │
│   ├──────────────┼─────────────┤                      │
│   │ Electronics  │ 2550        │                      │
│   │ Furniture    │ 595         │                      │
│   └──────────────┴─────────────┘                      │
└─────────────────────────────────────────────────────────┘
                    ↓ (passed to next CTE)
┌─────────────────────────────────────────────────────────┐
│ ranked_categories AS (                                  │
│   SELECT ... FROM category_totals ← Uses previous CTE! │
│   ↓                                                     │
│   Creates new temporary table:                         │
│   ┌──────────────┬─────────────┬──────┐              │
│   │ category     │ total_sales │ rank │              │
│   ├──────────────┼─────────────┼──────┤              │
│   │ Electronics  │ 2550        │ 1    │              │
│   │ Furniture    │ 595         │ 2    │              │
│   └──────────────┴─────────────┴──────┘              │
└─────────────────────────────────────────────────────────┘
                    ↓ (used in final SELECT)
┌─────────────────────────────────────────────────────────┐
│ SELECT * FROM ranked_categories                         │
└─────────────────────────────────────────────────────────┘
*/


-- ============================================
-- EXAMPLE 3: CROSS-REFERENCING (Joining CTEs)
-- ============================================
-- You can JOIN two CTEs together!

WITH monthly_sales AS (
    -- CTE #1: Sales by month
    SELECT 
        TO_CHAR(sale_date, 'YYYY-MM') AS month,
        SUM(amount) AS monthly_total
    FROM sales
    GROUP BY TO_CHAR(sale_date, 'YYYY-MM')
),
category_sales AS (
    -- CTE #2: Sales by category (independent of CTE #1)
    SELECT 
        category,
        SUM(amount) AS category_total
    FROM sales
    GROUP BY category
),
overall_stats AS (
    -- CTE #3: Overall statistics
    SELECT 
        SUM(amount) AS grand_total,
        AVG(amount) AS avg_sale
    FROM sales
)
-- Final SELECT: Reference ALL three CTEs!
SELECT 
    'Monthly Sales' AS report_type,
    month AS detail,
    monthly_total AS amount
FROM monthly_sales

UNION ALL

SELECT 
    'Category Sales' AS report_type,
    category AS detail,
    category_total AS amount
FROM category_sales

UNION ALL

SELECT 
    'Overall Stats' AS report_type,
    'Grand Total' AS detail,
    grand_total AS amount
FROM overall_stats;


-- ============================================
-- EXAMPLE 4: COMPLEX CHAINING (3+ CTEs)
-- ============================================

WITH step1_raw_data AS (
    -- Step 1: Get the raw data
    SELECT 
        category,
        EXTRACT(MONTH FROM sale_date) AS month,
        amount
    FROM sales
),
step2_monthly_category AS (
    -- Step 2: Aggregate by category and month (uses step1)
    SELECT 
        category,
        month,
        SUM(amount) AS monthly_category_total
    FROM step1_raw_data
    GROUP BY category, month
),
step3_add_rank AS (
    -- Step 3: Add rankings (uses step2)
    SELECT 
        category,
        month,
        monthly_category_total,
        RANK() OVER (PARTITION BY category ORDER BY monthly_category_total DESC) AS rank_in_category
    FROM step2_monthly_category
),
step4_filter AS (
    -- Step 4: Filter to top month per category (uses step3)
    SELECT 
        category,
        month,
        monthly_category_total
    FROM step3_add_rank
    WHERE rank_in_category = 1
)
-- Final: Show the best month for each category
SELECT * FROM step4_filter
ORDER BY category;


-- ============================================
-- KEY RULES FOR MULTIPLE CTEs
-- ============================================

-- ✅ CORRECT Syntax:
/*
WITH cte1 AS (
    SELECT ...
),              ← Comma here!
cte2 AS (
    SELECT ... FROM cte1  ← Can reference cte1
),              ← Comma here!
cte3 AS (
    SELECT ... FROM cte1  ← Can reference cte1
    JOIN cte2 ...         ← Can reference cte2
)               ← NO comma on the last one!
SELECT ... FROM cte3;
*/

-- ❌ WRONG: Missing commas
/*
WITH cte1 AS (...)
cte2 AS (...)  ← ERROR: Missing comma after cte1!
*/

-- ❌ WRONG: Comma after last CTE
/*
WITH cte1 AS (...),
cte2 AS (...),  ← ERROR: No comma here!
SELECT ...
*/

-- ❌ WRONG: Referencing a CTE that comes AFTER
/*
WITH cte1 AS (
    SELECT ... FROM cte2  ← ERROR: cte2 doesn't exist yet!
),
cte2 AS (...)
*/


-- ============================================
-- WHEN TO USE MULTIPLE CTEs
-- ============================================

-- Use Case 1: Breaking down complex logic into steps
-- Instead of one giant nested query, use CTEs like:
-- Step 1: Filter data
-- Step 2: Aggregate
-- Step 3: Calculate metrics
-- Step 4: Rank results

-- Use Case 2: Reusing the same calculation
-- Calculate something once in CTE #1, use it in CTE #2 and CTE #3

-- Use Case 3: Comparing different aggregations
-- CTE #1: Monthly totals
-- CTE #2: Category totals
-- Final: Compare them side-by-side


-- ============================================
-- CROSS JOIN: Combining Every Row with Every Row
-- ============================================
-- CROSS JOIN creates a "Cartesian Product" - every row from CTE #1 
-- is paired with every row from CTE #2

-- Example: If CTE #1 has 3 rows and CTE #2 has 2 rows,
-- the result will have 3 × 2 = 6 rows

WITH categories AS (
    SELECT DISTINCT category FROM sales
),
months AS (
    SELECT DISTINCT TO_CHAR(sale_date, 'YYYY-MM') AS month FROM sales
)
-- CROSS JOIN: Every category paired with every month
SELECT 
    c.category,
    m.month
FROM 
    categories c
CROSS JOIN 
    months m
ORDER BY 
    c.category, m.month;

-- Result: All possible category-month combinations
-- category    | month
-- ------------|--------
-- Electronics | 2024-01
-- Electronics | 2024-02
-- Electronics | 2024-03
-- Electronics | 2024-04
-- Furniture   | 2024-01
-- Furniture   | 2024-02
-- Furniture   | 2024-03
-- Furniture   | 2024-04


-- ============================================
-- CROSS JOIN USE CASE: Filling in Missing Data
-- ============================================
-- Problem: Not every category has sales in every month
-- Solution: Use CROSS JOIN to create all combinations, then LEFT JOIN actual sales

WITH categories AS (
    SELECT DISTINCT category FROM sales
),
months AS (
    SELECT DISTINCT TO_CHAR(sale_date, 'YYYY-MM') AS month FROM sales
),
all_combinations AS (
    -- CROSS JOIN: Every category × every month
    SELECT 
        c.category,
        m.month
    FROM categories c
    CROSS JOIN months m
),
actual_sales AS (
    -- Actual sales by category and month
    SELECT 
        category,
        TO_CHAR(sale_date, 'YYYY-MM') AS month,
        SUM(amount) AS total_sales
    FROM sales
    GROUP BY category, TO_CHAR(sale_date, 'YYYY-MM')
)
-- LEFT JOIN to show $0 for months with no sales
SELECT 
    ac.category,
    ac.month,
    COALESCE(s.total_sales, 0) AS total_sales
FROM 
    all_combinations ac
LEFT JOIN 
    actual_sales s 
    ON ac.category = s.category 
    AND ac.month = s.month
ORDER BY 
    ac.category, ac.month;

-- This shows EVERY month for EVERY category, even if there were no sales!


-- ============================================
-- CROSS JOIN vs Other JOINs
-- ============================================

-- INNER JOIN: Only matching rows
-- LEFT JOIN: All rows from left table, matches from right
-- CROSS JOIN: EVERY row from left × EVERY row from right (no ON condition!)

-- Example:
-- Table A: 3 rows
-- Table B: 2 rows
--
-- CROSS JOIN result: 3 × 2 = 6 rows
-- INNER JOIN result: 0-6 rows (depends on matches)
-- LEFT JOIN result: 3 rows minimum


-- ============================================
-- PRACTICE EXERCISES
-- ============================================

-- Practice 1: Create 3 CTEs
-- CTE #1: Get all Electronics sales
-- CTE #2: Calculate average Electronics sale
-- CTE #3: Find Electronics sales above average
-- Hint: Each CTE references the previous one

-- Practice 2: Cross-reference two independent CTEs
-- CTE #1: Best-selling category
-- CTE #2: Most recent sale date
-- Final: JOIN them together

-- Practice 3: Build a 4-step analysis
-- Step 1: Extract year and category
-- Step 2: Sum by year and category
-- Step 3: Calculate year-over-year growth
-- Step 4: Filter to positive growth only


-- ============================================
-- KEY TAKEAWAYS
-- ============================================
-- 1. Each CTE is like a temporary table
-- 2. Later CTEs can reference earlier CTEs
-- 3. You CANNOT reference a CTE that comes after
-- 4. Separate CTEs with commas (except the last one)
-- 5. The final SELECT can reference ANY of the CTEs
-- 6. CTEs make complex queries readable and debuggable
