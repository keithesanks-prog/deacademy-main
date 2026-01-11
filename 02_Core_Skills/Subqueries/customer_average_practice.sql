-- ============================================
-- SUBQUERY PRACTICE: CUSTOMER ORDERS
-- ============================================
-- Goal: Retrieve the customer_name of customers who have placed orders 
-- with a total amount greater than the average amount of all orders.

-- ============================================
-- OPTION 1: Customers with a SINGLE order > Average
-- ============================================
-- Logic:
-- 1. Calculate Average Order Amount (Subquery)
-- 2. Find orders > Average
-- 3. Get customer names

SELECT DISTINCT c.customer_name
FROM customers_new c
JOIN orders_new o ON c.customer_id = o.customer_id
WHERE o.amount > (
    SELECT AVG(amount) FROM orders_new
);

-- ============================================
-- OPTION 2: Customers with TOTAL SPEND > Average Order
-- ============================================
-- Logic:
-- 1. Calculate Total Spend per Customer
-- 2. Compare to Average Order Amount

SELECT c.customer_name, SUM(o.amount) as total_spend
FROM customers_new c
JOIN orders_new o ON c.customer_id = o.customer_id
GROUP BY c.customer_name
HAVING SUM(o.amount) > (
    SELECT AVG(amount) FROM orders_new
);

-- ============================================
-- OPTION 3: Customers with TOTAL SPEND > Average Customer Spend
-- ============================================
-- Logic:
-- 1. Calculate Average Spend PER CUSTOMER
-- 2. Compare each customer's total to that average

WITH customer_totals AS (
    SELECT customer_id, SUM(amount) as total_spent
    FROM orders_new
    GROUP BY customer_id
),
avg_customer_spend AS (
    SELECT AVG(total_spent) as avg_spend FROM customer_totals
)
SELECT c.customer_name, ct.total_spent
FROM customers_new c
JOIN customer_totals ct ON c.customer_id = ct.customer_id
WHERE ct.total_spent > (SELECT avg_spend FROM avg_customer_spend);
