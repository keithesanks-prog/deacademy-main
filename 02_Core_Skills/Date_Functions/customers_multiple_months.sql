-- ============================================
-- CUSTOMERS WITH ORDERS IN MULTIPLE MONTHS
-- ============================================
-- Goal: Find customers who made orders in at least 2 different months of 2022

-- ============================================
-- TERMINOLOGY (IMPORTANT!)
-- ============================================
-- "At least two months" = 2 or more DIFFERENT months
-- NOT 2 or more orders total!

-- Example:
-- Alice: Orders on 2022-01-15, 2022-01-20, 2022-03-10
--   → Ordered in 2 different months (January, March) ✅
--
-- Bob: Orders on 2022-05-01, 2022-05-15
--   → Ordered in 1 month (May only) ❌
--
-- Charlie: Orders on 2022-02-10, 2022-06-15, 2022-12-20
--   → Ordered in 3 different months (Feb, June, Dec) ✅

-- ============================================
-- SETUP: Create tables and sample data
-- ============================================
DROP TABLE IF EXISTS orders_prc CASCADE;
DROP TABLE IF EXISTS customers_prc CASCADE;

CREATE TABLE customers_prc (
    customerid INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    city VARCHAR(100)
);

CREATE TABLE orders_prc (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    amount INT,
    FOREIGN KEY (customer_id) REFERENCES customers_prc(customerid)
);

INSERT INTO customers_prc VALUES
(1, 'Alice Johnson', 25, 'New York'),
(2, 'Bob Smith', 35, 'Chicago'),
(3, 'Charlie Brown', 45, 'Los Angeles'),
(4, 'Diana Prince', 28, 'Seattle'),
(5, 'Eve Wilson', 32, 'Boston');

INSERT INTO orders_prc VALUES
-- Alice: 3 orders in 2 different months (Jan, Mar) ✅
(101, 1, '2022-01-15', 100),
(102, 1, '2022-01-20', 200),
(103, 1, '2022-03-10', 150),
-- Bob: 2 orders in 1 month (May only) ❌
(104, 2, '2022-05-01', 50),
(105, 2, '2022-05-15', 75),
-- Charlie: 3 orders in 3 different months (Feb, June, Dec) ✅
(106, 3, '2022-02-10', 500),
(107, 3, '2022-06-15', 300),
(108, 3, '2022-12-20', 400),
-- Diana: 1 order in 1 month (April) ❌
(109, 4, '2022-04-05', 150),
-- Eve: No orders in 2022 ❌
(110, 5, '2023-01-10', 200);

-- Verify the data
SELECT 'Customers:' as info;
SELECT * FROM customers_prc;

SELECT 'Orders in 2022:' as info;
SELECT * FROM orders_prc WHERE EXTRACT(YEAR FROM order_date) = 2022 ORDER BY customer_id, order_date;


-- ============================================
-- STEP 1: See Each Customer's Order Months
-- ============================================

SELECT 
    c.customerid,
    c.name,
    TO_CHAR(o.order_date, 'YYYY-MM') AS order_month
FROM 
    customers_prc c
JOIN 
    orders_prc o ON c.customerid = o.customer_id
WHERE 
    EXTRACT(YEAR FROM o.order_date) = 2022
ORDER BY 
    c.customerid, order_month;

-- Result:
-- customerid | name           | order_month
-- -----------|----------------|------------
-- 1          | Alice Johnson  | 2022-01
-- 1          | Alice Johnson  | 2022-01  (duplicate month)
-- 1          | Alice Johnson  | 2022-03
-- 2          | Bob Smith      | 2022-05
-- 2          | Bob Smith      | 2022-05  (duplicate month)
-- 3          | Charlie Brown  | 2022-02
-- 3          | Charlie Brown  | 2022-06
-- 3          | Charlie Brown  | 2022-12
-- 4          | Diana Prince   | 2022-04


-- ============================================
-- STEP 2: Count DISTINCT Months per Customer
-- ============================================

SELECT 
    c.customerid,
    c.name,
    COUNT(DISTINCT TO_CHAR(o.order_date, 'YYYY-MM')) AS distinct_months
FROM 
    customers_prc c
JOIN 
    orders_prc o ON c.customerid = o.customer_id
WHERE 
    EXTRACT(YEAR FROM o.order_date) = 2022
GROUP BY 
    c.customerid, c.name
ORDER BY 
    distinct_months DESC;

-- Result:
-- customerid | name           | distinct_months
-- -----------|----------------|----------------
-- 3          | Charlie Brown  | 3
-- 1          | Alice Johnson  | 2
-- 2          | Bob Smith      | 1
-- 4          | Diana Prince   | 1


-- ============================================
-- STEP 3: DETAILED BREAKDOWN - How COUNT(DISTINCT) Works
-- ============================================
-- Let's trace through EXACTLY what happens for Alice Johnson

-- Alice's Orders in 2022:
-- order_id | order_date  | amount
-- ---------|-------------|-------
-- 101      | 2022-01-15  | 100
-- 102      | 2022-01-20  | 200
-- 103      | 2022-03-10  | 150

-- STEP 3A: Extract the Month (TO_CHAR(order_date, 'YYYY-MM'))
-- The TO_CHAR function runs FIRST. It extracts the year-month from each date:

-- order_id | order_date  | TO_CHAR(order_date, 'YYYY-MM')
-- ---------|-------------|-------------------------------
-- 101      | 2022-01-15  | '2022-01'
-- 102      | 2022-01-20  | '2022-01'  ← Same month as 101!
-- 103      | 2022-03-10  | '2022-03'

-- STEP 3B: Find the Unique Months (DISTINCT)
-- The DISTINCT keyword looks at this list and removes duplicates:

-- List of Months: ('2022-01', '2022-01', '2022-03')
-- Unique Months (DISTINCT): ('2022-01', '2022-03')

-- STEP 3C: Count the Unique Months (COUNT(DISTINCT ...))
-- Finally, COUNT() counts how many items are in the unique list:

-- Final Count: 2

-- STEP 3D: Apply the Filter (HAVING ... >= 2)
-- Since Alice's count is 2, and 2 >= 2, she PASSES the filter!
-- She is included in the final result.

-- ============================================
-- VISUAL COMPARISON: Alice vs Bob
-- ============================================

-- ALICE (Passes - 2 distinct months):
-- Jan 15 → '2022-01' ┐
-- Jan 20 → '2022-01' ├─ DISTINCT → ('2022-01', '2022-03') → COUNT = 2 ✅
-- Mar 10 → '2022-03' ┘

-- BOB (Fails - 1 distinct month):
-- May 1  → '2022-05' ┐
-- May 15 → '2022-05' ┘─ DISTINCT → ('2022-05') → COUNT = 1 ❌

-- ============================================
-- WHY COUNT(DISTINCT) IS ESSENTIAL
-- ============================================

-- ❌ Without DISTINCT:
-- Alice: COUNT('2022-01', '2022-01', '2022-03') = 3 orders
-- Bob:   COUNT('2022-05', '2022-05') = 2 orders
-- Result: Both would pass the >= 2 filter! WRONG!

-- ✅ With DISTINCT:
-- Alice: COUNT(DISTINCT '2022-01', '2022-03') = 2 months
-- Bob:   COUNT(DISTINCT '2022-05') = 1 month
-- Result: Only Alice passes! CORRECT!


-- ============================================
-- SOLUTION 1: Using HAVING (Simplest)
-- ============================================

SELECT 
    c.name
FROM 
    customers_prc c
JOIN 
    orders_prc o ON c.customerid = o.customer_id
WHERE 
    EXTRACT(YEAR FROM o.order_date) = 2022
GROUP BY 
    c.customerid, c.name
HAVING 
    COUNT(DISTINCT TO_CHAR(o.order_date, 'YYYY-MM')) >= 2;

-- Expected Output:
-- name
-- ---------------
-- Alice Johnson
-- Charlie Brown


-- ============================================
-- SOLUTION 2: Using CTE (More Readable)
-- ============================================

WITH customer_month_counts AS (
    SELECT 
        c.customerid,
        c.name,
        COUNT(DISTINCT TO_CHAR(o.order_date, 'YYYY-MM')) AS distinct_months
    FROM 
        customers_prc c
    JOIN 
        orders_prc o ON c.customerid = o.customer_id
    WHERE 
        EXTRACT(YEAR FROM o.order_date) = 2022
    GROUP BY 
        c.customerid, c.name
)
SELECT 
    name
FROM 
    customer_month_counts
WHERE 
    distinct_months >= 2;


-- ============================================
-- SOLUTION 3: Alternative Date Extraction
-- ============================================
-- Using EXTRACT for both year and month

SELECT 
    c.name
FROM 
    customers_prc c
JOIN 
    orders_prc o ON c.customerid = o.customer_id
WHERE 
    EXTRACT(YEAR FROM o.order_date) = 2022
GROUP BY 
    c.customerid, c.name
HAVING 
    COUNT(DISTINCT EXTRACT(MONTH FROM o.order_date)) >= 2;


-- ============================================
-- SOLUTION 4: Showing the Month Count
-- ============================================
-- If you want to see HOW MANY months each customer ordered in

SELECT 
    c.name,
    COUNT(DISTINCT TO_CHAR(o.order_date, 'YYYY-MM')) AS months_ordered
FROM 
    customers_prc c
JOIN 
    orders_prc o ON c.customerid = o.customer_id
WHERE 
    EXTRACT(YEAR FROM o.order_date) = 2022
GROUP BY 
    c.customerid, c.name
HAVING 
    COUNT(DISTINCT TO_CHAR(o.order_date, 'YYYY-MM')) >= 2
ORDER BY 
    months_ordered DESC;

-- Expected Output:
-- name           | months_ordered
-- ---------------|---------------
-- Charlie Brown  | 3
-- Alice Johnson  | 2


-- ============================================
-- KEY INSIGHT: COUNT(DISTINCT ...)
-- ============================================

-- ❌ WRONG: COUNT without DISTINCT
SELECT c.name
FROM customers_prc c
JOIN orders_prc o ON c.customerid = o.customer_id
WHERE EXTRACT(YEAR FROM o.order_date) = 2022
GROUP BY c.name
HAVING COUNT(TO_CHAR(o.order_date, 'YYYY-MM')) >= 2;
-- This counts TOTAL orders, not distinct months!
-- Alice has 3 orders, so she'd be included even though 2 are in the same month.

-- ✅ CORRECT: COUNT(DISTINCT ...)
-- This counts only UNIQUE months


-- ============================================
-- COMMON MISTAKES TO AVOID
-- ============================================

-- ❌ WRONG: Forgetting the year filter
SELECT c.name
FROM customers_prc c
JOIN orders_prc o ON c.customerid = o.customer_id
GROUP BY c.name
HAVING COUNT(DISTINCT TO_CHAR(o.order_date, 'YYYY-MM')) >= 2;
-- This would include Eve if she had orders in 2023 and 2024!

-- ❌ WRONG: Using >= 2 on order count instead of month count
SELECT c.name
FROM customers_prc c
JOIN orders_prc o ON c.customerid = o.customer_id
WHERE EXTRACT(YEAR FROM o.order_date) = 2022
GROUP BY c.name
HAVING COUNT(o.order_id) >= 2;
-- This counts orders, not months! Bob has 2 orders but only 1 month.


-- ============================================
-- PRACTICE VARIATIONS
-- ============================================

-- Practice 1: Find customers who ordered in EXACTLY 2 months
-- Hint: Change >= 2 to = 2

-- Practice 2: Find customers who ordered in at least 3 months
-- Hint: Change >= 2 to >= 3

-- Practice 3: Find customers who ordered in ALL 12 months of 2022
-- Hint: HAVING COUNT(DISTINCT ...) = 12

-- Practice 4: Show which specific months each customer ordered in
-- Hint: Use STRING_AGG or array_agg with DISTINCT months


-- ============================================
-- KEY CONCEPTS
-- ============================================
-- 1. COUNT(DISTINCT ...): Counts unique values only
-- 2. TO_CHAR(date, 'YYYY-MM'): Extracts year-month as text
-- 3. HAVING: Filters groups after GROUP BY
-- 4. "At least 2 months" = >= 2 distinct months, not >= 2 orders
