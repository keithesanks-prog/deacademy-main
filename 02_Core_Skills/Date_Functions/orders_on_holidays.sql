-- ============================================
-- FINDING ORDERS ON U.S. FEDERAL HOLIDAYS
-- ============================================
-- Goal: Find orders placed on U.S. federal holidays

-- ============================================
-- TERMINOLOGY (IMPORTANT!)
-- ============================================
-- U.S. Federal Holidays are SPECIFIC DATES that change each year
-- Some are fixed (July 4th), others are floating (Memorial Day = last Monday of May)
--
-- We can't use a simple formula - we need a LIST of the actual dates!

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
-- Regular days
(101, 1, '2024-01-10', 100),
(102, 2, '2024-03-15', 200),
-- Holiday orders
(103, 3, '2024-01-01', 150),  -- New Year's Day
(104, 4, '2024-07-04', 250),  -- Independence Day
(105, 5, '2024-12-25', 300),  -- Christmas
(106, 1, '2024-11-28', 175),  -- Thanksgiving
-- More regular days
(107, 2, '2024-06-20', 125),
(108, 3, '2024-09-15', 180);

-- Verify the data
SELECT * FROM orders_prc ORDER BY order_date;


-- ============================================
-- SOLUTION 1: Using CTE (Recommended)
-- ============================================
-- This creates a temporary list of 2024 federal holidays

WITH federal_holidays AS (
    -- Define U.S. Federal Holidays for 2024
    SELECT DATE '2024-01-01' AS holiday_date, 'New Year''s Day' AS holiday_name UNION ALL
    SELECT DATE '2024-01-15', 'MLK Jr. Day' UNION ALL
    SELECT DATE '2024-02-19', 'Washington''s Birthday' UNION ALL
    SELECT DATE '2024-05-27', 'Memorial Day' UNION ALL
    SELECT DATE '2024-06-19', 'Juneteenth' UNION ALL
    SELECT DATE '2024-07-04', 'Independence Day' UNION ALL
    SELECT DATE '2024-09-02', 'Labor Day' UNION ALL
    SELECT DATE '2024-10-14', 'Columbus Day' UNION ALL
    SELECT DATE '2024-11-11', 'Veterans Day' UNION ALL
    SELECT DATE '2024-11-28', 'Thanksgiving Day' UNION ALL
    SELECT DATE '2024-12-25', 'Christmas Day'
)
SELECT
    o.order_id,
    o.order_date,
    h.holiday_name,
    o.amount
FROM
    orders_prc o
JOIN
    federal_holidays h ON o.order_date = h.holiday_date
ORDER BY
    o.order_date;

-- Expected Output:
-- order_id | order_date  | holiday_name       | amount
-- ---------|-------------|--------------------|---------
-- 103      | 2024-01-01  | New Year's Day     | 150
-- 104      | 2024-07-04  | Independence Day   | 250
-- 106      | 2024-11-28  | Thanksgiving Day   | 175
-- 105      | 2024-12-25  | Christmas Day      | 300


-- ============================================
-- SOLUTION 2: Using IN with Subquery
-- ============================================
-- If you only need the order info (not the holiday name)

SELECT
    order_id,
    order_date,
    amount
FROM
    orders_prc
WHERE
    order_date IN (
        SELECT DATE '2024-01-01' UNION ALL
        SELECT DATE '2024-01-15' UNION ALL
        SELECT DATE '2024-02-19' UNION ALL
        SELECT DATE '2024-05-27' UNION ALL
        SELECT DATE '2024-06-19' UNION ALL
        SELECT DATE '2024-07-04' UNION ALL
        SELECT DATE '2024-09-02' UNION ALL
        SELECT DATE '2024-10-14' UNION ALL
        SELECT DATE '2024-11-11' UNION ALL
        SELECT DATE '2024-11-28' UNION ALL
        SELECT DATE '2024-12-25'
    )
ORDER BY
    order_date;


-- ============================================
-- SOLUTION 3: Creating a Permanent Holiday Table
-- ============================================
-- For production use, create a real table

DROP TABLE IF EXISTS federal_holidays CASCADE;

CREATE TABLE federal_holidays (
    holiday_date DATE PRIMARY KEY,
    holiday_name VARCHAR(100),
    year INT
);

-- Insert 2024 holidays
INSERT INTO federal_holidays VALUES
('2024-01-01', 'New Year''s Day', 2024),
('2024-01-15', 'MLK Jr. Day', 2024),
('2024-02-19', 'Washington''s Birthday', 2024),
('2024-05-27', 'Memorial Day', 2024),
('2024-06-19', 'Juneteenth', 2024),
('2024-07-04', 'Independence Day', 2024),
('2024-09-02', 'Labor Day', 2024),
('2024-10-14', 'Columbus Day', 2024),
('2024-11-11', 'Veterans Day', 2024),
('2024-11-28', 'Thanksgiving Day', 2024),
('2024-12-25', 'Christmas Day', 2024);

-- Now you can use it in any query
SELECT
    o.order_id,
    o.order_date,
    h.holiday_name,
    o.amount
FROM
    orders_prc o
JOIN
    federal_holidays h ON o.order_date = h.holiday_date
ORDER BY
    o.order_date;


-- ============================================
-- UNDERSTANDING THE CTE APPROACH
-- ============================================

-- Step 1: The CTE creates a temporary "table" of holidays
-- federal_holidays:
-- holiday_date | holiday_name
-- -------------|------------------
-- 2024-01-01   | New Year's Day
-- 2024-01-15   | MLK Jr. Day
-- ...

-- Step 2: The JOIN matches order dates to holiday dates
-- For each order, check: "Is this date in the holiday list?"

-- Step 3: Only matching rows are returned
-- order_date = 2024-01-01 → Matches New Year's Day ✅
-- order_date = 2024-01-10 → No match ❌


-- ============================================
-- WHY WE NEED A LIST (Not a Formula)
-- ============================================

-- ❌ You CANNOT use a simple formula like:
-- WHERE EXTRACT(MONTH FROM order_date) = 12 AND EXTRACT(DAY FROM order_date) = 25
-- Because:
-- 1. Some holidays are floating (Memorial Day = last Monday of May)
-- 2. When holidays fall on weekends, they're observed on different days
-- 3. Holiday dates change each year

-- ✅ You MUST use a list of specific dates


-- ============================================
-- BONUS: Count Orders by Holiday
-- ============================================

WITH federal_holidays AS (
    SELECT DATE '2024-01-01' AS holiday_date, 'New Year''s Day' AS holiday_name UNION ALL
    SELECT DATE '2024-01-15', 'MLK Jr. Day' UNION ALL
    SELECT DATE '2024-02-19', 'Washington''s Birthday' UNION ALL
    SELECT DATE '2024-05-27', 'Memorial Day' UNION ALL
    SELECT DATE '2024-06-19', 'Juneteenth' UNION ALL
    SELECT DATE '2024-07-04', 'Independence Day' UNION ALL
    SELECT DATE '2024-09-02', 'Labor Day' UNION ALL
    SELECT DATE '2024-10-14', 'Columbus Day' UNION ALL
    SELECT DATE '2024-11-11', 'Veterans Day' UNION ALL
    SELECT DATE '2024-11-28', 'Thanksgiving Day' UNION ALL
    SELECT DATE '2024-12-25', 'Christmas Day'
)
SELECT
    h.holiday_name,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.amount), 0) AS total_revenue
FROM
    federal_holidays h
LEFT JOIN
    orders_prc o ON h.holiday_date = o.order_date
GROUP BY
    h.holiday_name, h.holiday_date
ORDER BY
    h.holiday_date;

-- This shows ALL holidays, even if there were no orders


-- ============================================
-- PRACTICE VARIATIONS
-- ============================================

-- Practice 1: Find orders NOT on holidays
-- Hint: Use LEFT JOIN and WHERE h.holiday_date IS NULL

-- Practice 2: Count how many orders were on weekends vs holidays
-- Hint: Use EXTRACT(DOW FROM order_date) for day of week

-- Practice 3: Add 2025 holidays to the permanent table
-- Hint: Look up the 2025 dates and INSERT them

-- Practice 4: Find the holiday with the most orders
-- Hint: Use GROUP BY and ORDER BY COUNT(*) DESC LIMIT 1


-- ============================================
-- KEY CONCEPTS
-- ============================================
-- 1. CTE: Creates a temporary list of holidays
-- 2. UNION ALL: Combines multiple SELECT statements into one list
-- 3. JOIN: Matches order dates to holiday dates
-- 4. DATE 'YYYY-MM-DD': PostgreSQL date literal syntax
-- 5. You need a LIST of dates, not a formula
