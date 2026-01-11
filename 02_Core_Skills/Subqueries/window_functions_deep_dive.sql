-- ============================================
-- YoY Calculation with Nike Product Data
-- ============================================
-- Goal: Calculate year-over-year percent change in Nike product sales

WITH sales AS (
    -- STEP 1: Aggregate sales by year
    -- We need to sum up all the prices for each year
    -- PostgreSQL uses EXTRACT(YEAR FROM date) instead of YEAR(date)
    SELECT
        EXTRACT(YEAR FROM order_date) AS order_year,
        SUM(price) AS total_sales
    FROM
        dim_product_nike
    GROUP BY
        EXTRACT(YEAR FROM order_date)
),
-- Note the comma here! Multiple CTEs are separated by commas, not semicolons
sales_change AS (
    -- STEP 2: Calculate YoY percent change
    SELECT
        order_year,
        total_sales,
        -- LAG gets the previous year's sales (the row before this one when ordered by year)
        LAG(total_sales) OVER (ORDER BY order_year) AS previous_year_sales,
        -- COALESCE handles NULL values (first year has no previous year)
        -- ROUND limits to 2 decimal places
        COALESCE(
            ROUND(
                -- Formula: (Current - Previous) / Previous * 100
                (total_sales - LAG(total_sales) OVER (ORDER BY order_year)) 
                / LAG(total_sales) OVER (ORDER BY order_year) * 100,
                2
            ),
            NULL  -- Keep NULL for first year to show "no previous year to compare"
        ) AS percent_change
    FROM
        sales
)
-- STEP 3: Select the final results
-- IMPORTANT: We're selecting FROM sales_change (the CTE name), NOT from order_date (which is a column)
SELECT
    order_year,
    total_sales,
    previous_year_sales,
    percent_change
FROM
    sales_change  -- This is the CTE name we defined above
ORDER BY
    order_year;

-- ============================================
-- KEY FIXES FROM YOUR ORIGINAL CODE:
-- ============================================
-- 1. ❌ "COALESCEC" → ✅ "COALESCE" (typo)
-- 2. ❌ "ROUNDO" → ✅ "ROUND" (typo)
-- 3. ❌ "AG(total_sales)" → ✅ "LAG(total_sales)" (missing L)
-- 4. ❌ Missing comma between CTEs → ✅ Added comma after first CTE
-- 5. ❌ Incorrect parentheses placement → ✅ Fixed nesting
-- 6. ❌ "sales_change as" → ✅ "sales_change AS (" (missing opening paren)
-- 7. ❌ "YEAR(order_date)" → ✅ "EXTRACT(YEAR FROM order_date)" (PostgreSQL syntax)

-- ============================================
-- DATABASE-SPECIFIC SYNTAX:
-- ============================================
-- MySQL/SQL Server:  YEAR(order_date)
-- PostgreSQL:        EXTRACT(YEAR FROM order_date)
-- SQLite:            strftime('%Y', order_date)
--
-- Since you're using PostgreSQL, we use EXTRACT()

-- ============================================
-- UNDERSTANDING THE ERROR YOU GOT:
-- ============================================
-- ERROR: column "order_date" does not exist
--
-- This can happen for two reasons:
-- 1. The table dim_product_nike hasn't been created yet
--    → Run the setup file first: sql_practice_setup.sql
-- 2. Wrong database syntax (YEAR() doesn't exist in PostgreSQL)
--    → Use EXTRACT(YEAR FROM order_date) instead

-- ============================================
-- HOW MULTIPLE CTEs WORK:
-- ============================================
-- WITH cte1 AS (
--     SELECT ...
-- ),          ← Comma here!
-- cte2 AS (
--     SELECT ... FROM cte1  ← Can reference cte1
-- ),          ← Comma here!
-- cte3 AS (
--     SELECT ... FROM cte2  ← Can reference cte1 or cte2
-- )           ← NO comma on the last one!
-- SELECT ... FROM cte3;