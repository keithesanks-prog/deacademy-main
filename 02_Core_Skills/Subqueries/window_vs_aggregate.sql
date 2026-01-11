-- ============================================
-- WINDOW FUNCTIONS vs AGGREGATE FUNCTIONS
-- Quick Reference Guide
-- ============================================

-- ============================================
-- SETUP
-- ============================================
DROP TABLE IF EXISTS sales_data;

CREATE TABLE sales_data (
    sale_id INTEGER PRIMARY KEY,
    salesperson TEXT,
    region TEXT,
    amount DECIMAL(10,2)
);

INSERT INTO sales_data VALUES
(1, 'Alice', 'East', 1000),
(2, 'Bob', 'East', 1500),
(3, 'Carol', 'West', 2000),
(4, 'David', 'West', 1200),
(5, 'Eve', 'East', 1800);

-- ============================================
-- COMPARISON 1: Aggregate vs Window Function
-- ============================================

-- AGGREGATE FUNCTION (GROUP BY):
-- Collapses rows into groups - REDUCES row count
SELECT 
    region,
    SUM(amount) AS total_sales
FROM sales_data
GROUP BY region;

-- RESULT: Only 2 rows (one per region)
-- East  | 4300
-- West  | 3200

-- WINDOW FUNCTION:
-- Keeps all rows - PRESERVES row count
SELECT 
    salesperson,
    region,
    amount,
    -- Calculate sum for each region, but keep all rows
    SUM(amount) OVER (PARTITION BY region) AS region_total
FROM sales_data;

-- RESULT: Still 5 rows (all original rows preserved)
-- Alice | East | 1000 | 4300
-- Bob   | East | 1500 | 4300
-- Eve   | East | 1800 | 4300
-- Carol | West | 2000 | 3200
-- David | West | 1200 | 3200

-- ============================================
-- KEY DIFFERENCE SUMMARY
-- ============================================
-- GROUP BY + Aggregate: Collapses rows → fewer rows in result
-- Window Function:      Keeps all rows → same row count in result

-- ============================================
-- WHEN TO USE EACH
-- ============================================

-- Use GROUP BY when you want:
-- ✓ Summary statistics only (total sales per region)
-- ✓ Fewer rows in output
-- ✓ To collapse detail into groups

-- Use Window Functions when you want:
-- ✓ Row-level detail PLUS aggregate info
-- ✓ To compare each row to its group
-- ✓ To rank or order within groups
-- ✓ To access previous/next rows

-- ============================================
-- PRACTICAL EXAMPLE: Sales Performance Report
-- ============================================

-- Goal: Show each salesperson with their individual sale,
--       their region's total, and their % of region total

SELECT 
    salesperson,
    region,
    amount AS individual_sale,
    -- Window function: calculate region total without collapsing rows
    SUM(amount) OVER (PARTITION BY region) AS region_total,
    -- Calculate percentage of region total
    ROUND(amount * 100.0 / SUM(amount) OVER (PARTITION BY region), 2) AS pct_of_region
FROM sales_data
ORDER BY region, amount DESC;

-- RESULT:
-- Eve   | East | 1800 | 4300 | 41.86%
-- Bob   | East | 1500 | 4300 | 34.88%
-- Alice | East | 1000 | 4300 | 23.26%
-- Carol | West | 2000 | 3200 | 62.50%
-- David | West | 1200 | 3200 | 37.50%

-- This would be IMPOSSIBLE with just GROUP BY because we need:
-- 1. Individual salesperson rows (can't collapse)
-- 2. Region totals (need aggregation)
-- Window functions give us both!
