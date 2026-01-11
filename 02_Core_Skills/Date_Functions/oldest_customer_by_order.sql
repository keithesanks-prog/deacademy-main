-- ============================================
-- FIND OLDEST CUSTOMER BY ORDER DATE
-- ============================================
-- Goal: Find the customer with the EARLIEST first order date

-- ============================================
-- TERMINOLOGY (IMPORTANT!)
-- ============================================
-- "Oldest customer by order date" = Customer who placed their first order EARLIEST
-- NOT the customer with the highest age!

-- Example:
-- Alice (age 25): First order on 2020-01-15
-- Bob (age 60): First order on 2023-05-10
-- 
-- "Oldest by order date" = Alice (2020 is earlier than 2023)
-- "Oldest by age" = Bob (60 > 25)

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
(2, 'Bob Smith', 60, 'Chicago'),
(3, 'Charlie Brown', 45, 'Los Angeles'),
(4, 'Diana Prince', 28, 'Seattle');

INSERT INTO orders_prc VALUES
-- Alice's orders (first order: 2020-01-15) - OLDEST!
(101, 1, '2020-01-15', 100),
(102, 1, '2023-03-20', 200),
-- Bob's orders (first order: 2023-05-10)
(103, 2, '2023-05-10', 50),
(104, 2, '2023-06-15', 75),
-- Charlie's orders (first order: 2022-08-01)
(105, 3, '2022-08-01', 500),
-- Diana's orders (first order: 2021-12-25)
(106, 4, '2021-12-25', 150);

-- Verify the data
SELECT 'Customers:' as info;
SELECT * FROM customers_prc;

SELECT 'Orders:' as info;
SELECT * FROM orders_prc ORDER BY order_date;


-- ============================================
-- STEP 1: Find Each Customer's First Order Date
-- ============================================

SELECT 
    c.customerid,
    c.name,
    MIN(o.order_date) AS first_order_date
FROM 
    customers_prc c
JOIN 
    orders_prc o ON c.customerid = o.customer_id
GROUP BY 
    c.customerid, c.name
ORDER BY 
    first_order_date;

-- Result:
-- customerid | name           | first_order_date
-- -----------|----------------|------------------
-- 1          | Alice Johnson  | 2020-01-15  ← EARLIEST!
-- 4          | Diana Prince   | 2021-12-25
-- 3          | Charlie Brown  | 2022-08-01
-- 2          | Bob Smith      | 2023-05-10


-- ============================================
-- SOLUTION 1: Using LIMIT (Simplest)
-- ============================================

SELECT 
    c.name,
    MIN(o.order_date) AS first_order_date
FROM 
    customers_prc c
JOIN 
    orders_prc o ON c.customerid = o.customer_id
GROUP BY 
    c.customerid, c.name
ORDER BY 
    first_order_date
LIMIT 1;

-- Expected Output:
-- name           | first_order_date
-- ---------------|------------------
-- Alice Johnson  | 2020-01-15


-- ============================================
-- SOLUTION 2: Using Subquery with MIN
-- ============================================

SELECT 
    c.name,
    MIN(o.order_date) AS first_order_date
FROM 
    customers_prc c
JOIN 
    orders_prc o ON c.customerid = o.customer_id
GROUP BY 
    c.customerid, c.name
HAVING 
    MIN(o.order_date) = (
        SELECT MIN(order_date) FROM orders_prc
    );

-- This finds the absolute earliest order date first,
-- then filters to customers whose first order matches that date


-- ============================================
-- SOLUTION 3: Using CTE (Most Readable)
-- ============================================

WITH customer_first_orders AS (
    SELECT 
        c.customerid,
        c.name,
        MIN(o.order_date) AS first_order_date
    FROM 
        customers_prc c
    JOIN 
        orders_prc o ON c.customerid = o.customer_id
    GROUP BY 
        c.customerid, c.name
)
SELECT 
    name,
    first_order_date
FROM 
    customer_first_orders
ORDER BY 
    first_order_date
LIMIT 1;


-- ============================================
-- SOLUTION 4: Using RANK() Window Function
-- ============================================

WITH customer_first_orders AS (
    SELECT 
        c.customerid,
        c.name,
        MIN(o.order_date) AS first_order_date
    FROM 
        customers_prc c
    JOIN 
        orders_prc o ON c.customerid = o.customer_id
    GROUP BY 
        c.customerid, c.name
),
ranked_customers AS (
    SELECT 
        name,
        first_order_date,
        RANK() OVER (ORDER BY first_order_date) AS rank
    FROM 
        customer_first_orders
)
SELECT 
    name,
    first_order_date
FROM 
    ranked_customers
WHERE 
    rank = 1;


-- ============================================
-- UNDERSTANDING THE LOGIC
-- ============================================

-- Step 1: For each customer, find their earliest order
-- MIN(o.order_date) grouped by customer

-- Step 2: Find which customer has the overall earliest date
-- ORDER BY first_order_date LIMIT 1
-- OR compare to the global MIN(order_date)

-- Step 3: Return that customer's name and date


-- ============================================
-- COMMON MISTAKES TO AVOID
-- ============================================

-- ❌ WRONG: Forgetting to group by customer
SELECT c.name, MIN(o.order_date)
FROM customers_prc c
JOIN orders_prc o ON c.customerid = o.customer_id;
-- This gives you the earliest order date across ALL customers,
-- but doesn't tell you WHICH customer it belongs to!

-- ❌ WRONG: Using MAX instead of MIN
SELECT c.name, MAX(o.order_date)  -- This finds the LATEST order!
FROM customers_prc c
JOIN orders_prc o ON c.customerid = o.customer_id
GROUP BY c.name;

-- ❌ WRONG: Ordering by age instead of order_date
SELECT c.name, MIN(o.order_date)
FROM customers_prc c
JOIN orders_prc o ON c.customerid = o.customer_id
GROUP BY c.name
ORDER BY c.age DESC;  -- This sorts by age, not order date!


-- ============================================
-- PRACTICE VARIATIONS
-- ============================================

-- Practice 1: Find the NEWEST customer (most recent first order)
-- Hint: ORDER BY first_order_date DESC LIMIT 1

-- Practice 2: Find the top 3 oldest customers by order date
-- Hint: LIMIT 3

-- Practice 3: Show ALL customers with their first order date, ranked
-- Hint: Remove the LIMIT, add RANK()

-- Practice 4: Find customers whose first order was in 2020
-- Hint: Add WHERE EXTRACT(YEAR FROM first_order_date) = 2020


-- ============================================
-- KEY CONCEPTS
-- ============================================
-- 1. MIN(order_date): Finds the earliest date
-- 2. GROUP BY customer: Gets the earliest date PER customer
-- 3. ORDER BY ... LIMIT 1: Gets the single earliest overall
-- 4. "Oldest by order date" ≠ "Oldest by age"
