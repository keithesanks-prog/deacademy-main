-- ============================================
-- QUARTERLY REVENUE ANALYSIS
-- ============================================
-- Goal: Calculate total revenue by quarter for 2022 and 2023

-- ============================================
-- SETUP: Create table and sample data
-- ============================================
DROP TABLE IF EXISTS orders_prc CASCADE;

CREATE TABLE orders_prc (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    amount INT
);

INSERT INTO orders_prc VALUES
-- 2022 Q1
(101, 1, '2022-01-15', 1000),
(102, 2, '2022-02-20', 1500),
(103, 3, '2022-03-10', 2000),
-- 2022 Q2
(104, 1, '2022-04-05', 1200),
(105, 2, '2022-05-15', 1800),
-- 2022 Q3
(106, 3, '2022-07-20', 2500),
(107, 1, '2022-08-10', 1600),
-- 2022 Q4
(108, 2, '2022-10-05', 3000),
(109, 3, '2022-11-15', 2200),
(110, 1, '2022-12-25', 2800),
-- 2023 Q1
(111, 2, '2023-01-10', 3500),
(112, 3, '2023-02-14', 4000),
-- 2023 Q2
(113, 1, '2023-04-20', 3200),
(114, 2, '2023-05-30', 3800),
-- 2023 Q3
(115, 3, '2023-07-15', 4500),
-- 2023 Q4
(116, 1, '2023-10-10', 5000),
(117, 2, '2023-11-20', 4200);

-- Verify the data
SELECT * FROM orders_prc ORDER BY order_date;


-- ============================================
-- MYSQL VERSION (Original - Won't work in PostgreSQL!)
-- ============================================
-- This is what you provided - it uses MySQL functions

-- ❌ MYSQL SYNTAX (Don't use this in PostgreSQL):
/*
SELECT
    CONCAT(YEAR(order_date), 'Q', QUARTER(order_date)) AS QuarterTotalRevenue,
    SUM(amount) AS total_revenue
FROM
    orders_prc
WHERE
    YEAR(order_date) IN (2022, 2023)
GROUP BY
    CONCAT(YEAR(order_date), 'Q', QUARTER(order_date))
ORDER BY
    QuarterTotalRevenue ASC;
*/


-- ============================================
-- POSTGRESQL VERSION (Use this!)
-- ============================================

SELECT
    -- Concatenate year, 'Q', and quarter number
    CONCAT(EXTRACT(YEAR FROM order_date), 'Q', EXTRACT(QUARTER FROM order_date)) AS QuarterTotalRevenue,
    SUM(amount) AS total_revenue
FROM
    orders_prc
WHERE
    -- Filter for 2022 and 2023
    EXTRACT(YEAR FROM order_date) IN (2022, 2023)
GROUP BY
    -- Group by the same concatenated expression
    CONCAT(EXTRACT(YEAR FROM order_date), 'Q', EXTRACT(QUARTER FROM order_date))
ORDER BY
    QuarterTotalRevenue ASC;

-- Expected Output:
-- QuarterTotalRevenue | total_revenue
-- --------------------|---------------
-- 2022Q1              | 4500
-- 2022Q2              | 3000
-- 2022Q3              | 4100
-- 2022Q4              | 8000
-- 2023Q1              | 7500
-- 2023Q2              | 7000
-- 2023Q3              | 4500
-- 2023Q4              | 9200


-- ============================================
-- ALTERNATIVE: Using TO_CHAR (Cleaner!)
-- ============================================

SELECT
    TO_CHAR(order_date, 'YYYY"Q"Q') AS quarter_label,
    SUM(amount) AS total_revenue
FROM
    orders_prc
WHERE
    EXTRACT(YEAR FROM order_date) IN (2022, 2023)
GROUP BY
    TO_CHAR(order_date, 'YYYY"Q"Q')
ORDER BY
    quarter_label ASC;

-- Same output, but using TO_CHAR instead of CONCAT


-- ============================================
-- MYSQL vs POSTGRESQL SYNTAX COMPARISON
-- ============================================

-- Function          | MySQL                  | PostgreSQL
-- ------------------|------------------------|---------------------------
-- Extract Year      | YEAR(date)             | EXTRACT(YEAR FROM date)
-- Extract Quarter   | QUARTER(date)          | EXTRACT(QUARTER FROM date)
-- Extract Month     | MONTH(date)            | EXTRACT(MONTH FROM date)
-- Concatenate       | CONCAT(a, b, c)        | CONCAT(a, b, c) ← Same!
-- Format Date       | DATE_FORMAT(date, fmt) | TO_CHAR(date, fmt)


-- ============================================
-- BONUS: Quarter-over-Quarter Growth
-- ============================================

WITH quarterly_revenue AS (
    SELECT
        CONCAT(EXTRACT(YEAR FROM order_date), 'Q', EXTRACT(QUARTER FROM order_date)) AS quarter,
        SUM(amount) AS total_revenue
    FROM
        orders_prc
    WHERE
        EXTRACT(YEAR FROM order_date) IN (2022, 2023)
    GROUP BY
        CONCAT(EXTRACT(YEAR FROM order_date), 'Q', EXTRACT(QUARTER FROM order_date))
)
SELECT
    quarter,
    total_revenue,
    LAG(total_revenue) OVER (ORDER BY quarter) AS previous_quarter_revenue,
    total_revenue - LAG(total_revenue) OVER (ORDER BY quarter) AS revenue_change,
    ROUND(
        (total_revenue - LAG(total_revenue) OVER (ORDER BY quarter))::DECIMAL 
        / LAG(total_revenue) OVER (ORDER BY quarter) * 100,
        2
    ) AS growth_percentage
FROM
    quarterly_revenue
ORDER BY
    quarter;


-- ============================================
-- PRACTICE VARIATIONS
-- ============================================

-- Practice 1: Find the quarter with the highest revenue
-- Hint: ORDER BY total_revenue DESC LIMIT 1

-- Practice 2: Calculate average revenue per quarter
-- Hint: AVG(total_revenue) from the quarterly_revenue CTE

-- Practice 3: Show only quarters with revenue > $5000
-- Hint: Add HAVING SUM(amount) > 5000

-- Practice 4: Compare 2022 vs 2023 by quarter (Q1 2022 vs Q1 2023)
-- Hint: Use CASE or PIVOT to show years side-by-side


-- ============================================
-- KEY CONCEPTS
-- ============================================
-- 1. EXTRACT(YEAR/QUARTER FROM date): PostgreSQL date extraction
-- 2. CONCAT(): Combines text (works in both MySQL and PostgreSQL)
-- 3. TO_CHAR(date, 'YYYY"Q"Q'): Alternative formatting method
-- 4. GROUP BY: Must match the SELECT expression exactly
-- 5. Quarter format: 2022Q1, 2022Q2, etc.
