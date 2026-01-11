-- ============================================
-- THE SIMPLEST LAG() EXAMPLE
-- ============================================
-- No CTEs. No complex math. Just looking at the previous row.

-- 1. View the raw data first
SELECT * FROM sales_by_year;

-- 2. Use LAG() to see previous year's sales next to current year
SELECT 
    year, 
    sales,
    -- LAG(column) OVER (ORDER BY column)
    LAG(sales) OVER (ORDER BY year) as previous_sales
FROM 
    sales_by_year;

-- ============================================
-- THAT'S IT!
-- ============================================
-- Everything else (calculating %, rounding, handling NULLs) 
-- is just standard math on top of these two columns.
--
-- Formula for % Change:
-- (sales - previous_sales) / previous_sales
