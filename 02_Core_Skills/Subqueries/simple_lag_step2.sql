-- ============================================
-- STEP 2: CALCULATING THE DIFFERENCE
-- ============================================
-- Now that we have "sales" and "previous_sales" side-by-side,
-- we can do simple math with them.

SELECT 
    year, 
    sales,
    LAG(sales) OVER (ORDER BY year) as previous_sales,
    
    -- NEW PART: Just subtract them!
    sales - LAG(sales) OVER (ORDER BY year) as dollar_change
    
FROM 
    sales_by_year;

-- Expected Result:
-- 2020: 1000000 | NULL    | NULL
-- 2021: 1250000 | 1000000 | 250000  (Grew by $250k)
-- 2022: 1500000 | 1250000 | 250000  (Grew by $250k)
