-- ============================================
-- AGE RANGE COUNTING PRACTICE
-- ============================================
-- Goal: Count customers in three age ranges:
--   - Under 30
--   - 30 to 40
--   - Over 40

-- ============================================
-- SETUP: Create the table and sample data
-- ============================================
DROP TABLE IF EXISTS customers_prc CASCADE;

CREATE TABLE customers_prc (
    customerid INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    city VARCHAR(100)
);

INSERT INTO customers_prc VALUES
(1, 'Alice Johnson', 25, 'New York'),
(2, 'Bob Smith', 35, 'Chicago'),
(3, 'Charlie Brown', 45, 'Los Angeles'),
(4, 'Diana Prince', 28, 'Seattle'),
(5, 'Eve Wilson', 32, 'Boston'),
(6, 'Frank Moore', 50, 'Miami'),
(7, 'Grace Lee', 22, 'Portland'),
(8, 'Henry Davis', 38, 'Denver'),
(9, 'Iris Chen', 55, 'Austin'),
(10, 'Jack Taylor', 29, 'Phoenix');

-- Verify the data
SELECT * FROM customers_prc ORDER BY age;

-- ============================================
-- SOLUTION 1: Using CASE Statement
-- ============================================
-- This is the most common and readable approach

SELECT
    -- CASE creates categories based on conditions
    CASE
        WHEN age < 30 THEN 'Under 30'
        WHEN age BETWEEN 30 AND 40 THEN '30 to 40'
        WHEN age > 40 THEN 'Over 40'
    END AS age_range,
    COUNT(*) AS customer_count
FROM
    customers_prc
GROUP BY
    -- We group by the same CASE expression
    CASE
        WHEN age < 30 THEN 'Under 30'
        WHEN age BETWEEN 30 AND 40 THEN '30 to 40'
        WHEN age > 40 THEN 'Over 40'
    END
ORDER BY
    age_range;

-- Expected Result:
-- age_range  | customer_count
-- -----------|---------------
-- 30 to 40   | 3
-- Over 40    | 3
-- Under 30   | 4


-- ============================================
-- SOLUTION 2: Using a CTE (Cleaner!)
-- ============================================
-- This avoids repeating the CASE statement

WITH categorized_customers AS (
    SELECT
        customerid,
        name,
        age,
        CASE
            WHEN age < 30 THEN 'Under 30'
            WHEN age BETWEEN 30 AND 40 THEN '30 to 40'
            WHEN age > 40 THEN 'Over 40'
        END AS age_range
    FROM
        customers_prc
)
SELECT
    age_range,
    COUNT(*) AS customer_count
FROM
    categorized_customers
GROUP BY
    age_range
ORDER BY
    age_range;


-- ============================================
-- SOLUTION 3: PIVOTED OUTPUT (Side-by-Side Columns)
-- ============================================
-- This shows counts in columns instead of rows

SELECT
    COUNT(CASE WHEN age < 30 THEN 1 END) AS Under30,
    COUNT(CASE WHEN age BETWEEN 30 AND 40 THEN 1 END) AS Between30And40,
    COUNT(CASE WHEN age > 40 THEN 1 END) AS Over40
FROM
    customers_prc;

-- Expected Output:
-- Under30 | Between30And40 | Over40
-- --------|----------------|-------
--    4    |       3        |   3

-- HOW IT WORKS:
-- COUNT(CASE WHEN condition THEN 1 END) counts only rows where condition is true
-- Each CASE creates a separate column


-- ============================================
-- SOLUTION 4: Showing Individual Customers
-- ============================================
-- If you want to see WHO is in each category

WITH categorized_customers AS (
    SELECT
        customerid,
        name,
        age,
        CASE
            WHEN age < 30 THEN 'Under 30'
            WHEN age BETWEEN 30 AND 40 THEN '30 to 40'
            WHEN age > 40 THEN 'Over 40'
        END AS age_range
    FROM
        customers_prc
)
SELECT
    age_range,
    COUNT(*) AS customer_count,
    STRING_AGG(name, ', ' ORDER BY name) AS customer_names
FROM
    categorized_customers
GROUP BY
    age_range
ORDER BY
    age_range;


-- ============================================
-- PRACTICE VARIATIONS
-- ============================================

-- Practice 1: Count customers by city
-- Hint: GROUP BY city

-- Practice 2: Find the average age in each age range
-- Hint: Add AVG(age) to the SELECT

-- Practice 3: Count customers in different age ranges:
--   - Under 25
--   - 25 to 35
--   - 35 to 50
--   - Over 50

-- Practice 4: Show age ranges with percentage of total
-- Hint: Use a window function or calculate total separately


-- ============================================
-- KEY CONCEPTS
-- ============================================
-- 1. CASE Statement: Creates categories based on conditions
-- 2. GROUP BY: Groups rows by the category
-- 3. COUNT(*): Counts rows in each group
-- 4. CTE: Makes the query cleaner by avoiding repetition
