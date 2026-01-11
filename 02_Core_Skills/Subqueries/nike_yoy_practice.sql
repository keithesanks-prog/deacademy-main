
-- 1. Show both current and previous 
--year's sales for comparison
SELECT *
FROM sales_by_year;

-- 2. Show both current and previous 
--year's sales for comparison   
SELECT
    year,
-- Current year's sales
    sales AS current_sales,
-- Get previous year's sales using LAG window function then order by year, without this the previous year's sales will be null
    LAG(sales) OVER (ORDER BY year) AS previous_sales,
-- Calculate YoY change Sales - Previous Sales / Previous Sales * 100 the outer round is to limit decimal places to 2
    ROUND((sales - LAG(sales) OVER (ORDER BY year)) / LAG(sales) OVER (ORDER BY year) * 100, 2) AS yoy_change
FROM sales_by_year;

-- 3. Only show years with positive growth
-- IMPORTANT: Window functions can't be used in WHERE clause!
-- Must use CTE or subquery to filter window function results
WITH yoy_calculations AS (
    SELECT
-- For this query we need to calculate the YoY change, which means we need the year and sales columns from the sales_by_year table and calculate the YoY change
        year,
        sales,
-- Now that we have the year and sales columns from the sales_by_year table and calculate the YoY change, we can use the LAG window function to get the previous year's sales
-- Below is a subquery that calculates the YoY change, which means year-over-year (i.e. 2020 vs 2021) change by taking the current year's (column sales) sales and subtracting the previous year's (LAG(sales)) sales, then dividing by the previous year's sales (LAG(sales)) and multiplying by 100
-- Calculate YoY change Sales - Previous Sales / Previous Sales * 100 the outer round is to limit decimal places to 2
        ROUND((sales - LAG(sales) OVER (ORDER BY year)) / LAG(sales) OVER (ORDER BY year) * 100, 2) AS yoy_change
-- From this we get yoy_change, which is just a number nothing scary about it, it can have negative numbers as well, this tells us that the previous year's sales were higher than the current year's sales, think of this like a variable that we can use to *filter* the results, we can use this variable to filter the results to only show years with positive growth
    FROM sales_by_year
)
SELECT year, yoy_change
FROM yoy_calculations
WHERE yoy_change > 0;

-- 4. Calculate absolute dollar change as well
SELECT
    year,
    sales - LAG(sales) OVER (ORDER BY year) AS dollar_change,
    ROUND((sales - LAG(sales) OVER (ORDER BY year)) / LAG(sales) OVER (ORDER BY year) * 100, 2) AS percent_change
FROM sales_by_year;
