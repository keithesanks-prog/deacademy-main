-- ============================================
-- STEP 3: CALCULATING THE PERCENTAGE (FINAL STEP)
-- ============================================
-- We have the dollar change. Now let's turn it into a %.
-- Formula: (Change / Previous) * 100

SELECT 
    year, 
    sales,
    LAG(sales) OVER (ORDER BY year) as previous_sales,
    sales - LAG(sales) OVER (ORDER BY year) as dollar_change,
    
    -- NEW PART: Divide by previous to get %
    (sales - LAG(sales) OVER (ORDER BY year)) 
    / LAG(sales) OVER (ORDER BY year) * 100 as percent_change
    
FROM 
    sales_by_year;

-- Expected Result for 2021:
-- Change: 250,000
-- Previous: 1,000,000
-- % Change: 250,000 / 1,000,000 = 0.25 = 25%
