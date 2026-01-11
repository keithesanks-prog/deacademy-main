-- ============================================
-- FINDING TOP CUSTOMERS BY ORDER COUNT
-- ============================================
-- Goal: Find customer(s) with the MOST orders
-- This uses nested subqueries with HAVING clause

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
    amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers_prc(customerid)
);

INSERT INTO customers_prc VALUES
(1, 'Alice Johnson', 25, 'New York'),
(2, 'Bob Smith', 35, 'Chicago'),
(3, 'Charlie Brown', 45, 'Los Angeles'),
(4, 'Diana Prince', 28, 'Seattle'),
(5, 'Eve Wilson', 32, 'Boston');

INSERT INTO orders_prc VALUES
(101, 1, '2025-01-10', 100.00),
(102, 1, '2025-01-15', 200.00),
(103, 1, '2025-01-20', 150.00),  -- Alice: 3 orders
(104, 2, '2025-01-12', 50.00),
(105, 2, '2025-01-18', 75.00),   -- Bob: 2 orders
(106, 3, '2025-01-14', 500.00),
(107, 3, '2025-01-22', 300.00),
(108, 3, '2025-01-25', 400.00),  -- Charlie: 3 orders (tied for most!)
(109, 4, '2025-01-16', 150.00),  -- Diana: 1 order
(110, 5, '2025-01-19', 200.00);  -- Eve: 1 order

-- Verify the data
SELECT 'Customers:' as info;
SELECT * FROM customers_prc;

SELECT 'Orders:' as info;
SELECT * FROM orders_prc ORDER BY customer_id;

-- ============================================
-- SOLUTION 1: The Original (Nested Subqueries)
-- ============================================

SELECT
    c.name,
    COUNT(o.order_id) AS total_orders
FROM
    customers_prc c
JOIN
    orders_prc o ON c.customerid = o.customer_id
GROUP BY
    c.name
HAVING
    COUNT(o.order_id) = (
        -- Inner Query: Finds the single, highest number of orders
        SELECT MAX(order_count)
        FROM (
            -- Innermost Query: Calculates order count for every customer
            SELECT COUNT(order_id) AS order_count 
            FROM orders_prc 
            GROUP BY customer_id
        ) AS customer_orders
    );

-- Expected Output:
-- name           | total_orders
-- ---------------|-------------
-- Alice Johnson  | 3
-- Charlie Brown  | 3


-- ============================================
-- UNDERSTANDING THE NESTED SUBQUERIES
-- ============================================

-- Step 1: Let's see what the INNERMOST query does
SELECT COUNT(order_id) AS order_count 
FROM orders_prc 
GROUP BY customer_id;

-- Result:
-- order_count
-- -----------
-- 3  (Alice)
-- 2  (Bob)
-- 3  (Charlie)
-- 1  (Diana)
-- 1  (Eve)

-- Step 2: Now let's see what the MIDDLE query does (wraps Step 1)
SELECT MAX(order_count)
FROM (
    SELECT COUNT(order_id) AS order_count 
    FROM orders_prc 
    GROUP BY customer_id
) AS customer_orders;

-- Result:
-- max
-- ---
-- 3

-- Step 3: The OUTER query uses this max value (3) to filter
-- It keeps only customers where COUNT(orders) = 3


-- ============================================
-- SOLUTION 2: Using a CTE (Much Clearer!)
-- ============================================

WITH customer_order_counts AS (
    -- Step 1: Count orders for each customer
    SELECT 
        c.customerid,
        c.name,
        COUNT(o.order_id) AS total_orders
    FROM customers_prc c
    JOIN orders_prc o ON c.customerid = o.customer_id
    GROUP BY c.customerid, c.name
),
max_orders AS (
    -- Step 2: Find the maximum order count
    SELECT MAX(total_orders) AS max_count
    FROM customer_order_counts
)
-- Step 3: Filter to keep only customers with max orders
SELECT 
    name,
    total_orders
FROM 
    customer_order_counts
WHERE 
    total_orders = (SELECT max_count FROM max_orders);


-- ============================================
-- SOLUTION 3: Using RANK() Window Function
-- ============================================
-- This is often the cleanest approach for "top N" problems

WITH customer_order_counts AS (
    SELECT 
        c.name,
        COUNT(o.order_id) AS total_orders,
        RANK() OVER (ORDER BY COUNT(o.order_id) DESC) as rank
    FROM customers_prc c
    JOIN orders_prc o ON c.customerid = o.customer_id
    GROUP BY c.name
)
SELECT 
    name,
    total_orders
FROM 
    customer_order_counts
WHERE 
    rank = 1;  -- Get only the top-ranked customers


-- ============================================
-- COMPARISON: When to Use Each Approach
-- ============================================

-- Nested Subqueries (Solution 1):
-- ✅ Works in all SQL databases
-- ❌ Hard to read and debug
-- ❌ Can be slow on large datasets

-- CTE (Solution 2):
-- ✅ Very readable and maintainable
-- ✅ Easy to debug (run each CTE separately)
-- ✅ Good performance
-- ❌ Not supported in very old SQL versions

-- Window Functions (Solution 3):
-- ✅ Most concise
-- ✅ Best performance
-- ✅ Easy to extend (e.g., "top 3 customers")
-- ❌ Requires understanding of window functions


-- ============================================
-- PRACTICE VARIATIONS
-- ============================================

-- Practice 1: Find customers with the LEAST orders
-- Hint: Change MAX to MIN

-- Practice 2: Find the top 3 customers by order count
-- Hint: Use RANK() and WHERE rank <= 3

-- Practice 3: Show ALL customers with their order counts AND rank
-- Hint: Remove the WHERE clause from Solution 3

-- Practice 4: Find customers who spent the MOST money (not most orders)
-- Hint: Use SUM(amount) instead of COUNT(order_id)


-- ============================================
-- KEY CONCEPTS
-- ============================================
-- 1. HAVING: Filters groups (after GROUP BY)
-- 2. Nested Subqueries: Query inside a query
-- 3. MAX/MIN with GROUP BY: Find extreme values
-- 4. CTEs: Break complex queries into readable steps
-- 5. RANK(): Assign rankings to rows
