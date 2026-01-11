-- ============================================
-- SQL TRAINING: Amazon Repeat Buyers Analysis
-- ============================================

/*
PROBLEM STATEMENT:
Find customers who:
1. Purchased the same product at least 3 times
2. Identify their MOST purchased product
3. Show customer_name, product_name, and times_purchased

OUTPUT COLUMNS: customer_name, product_name, times_purchased
*/

-- ============================================
-- STEP 1: Understanding the Data Model
-- ============================================

/*
Table Relationships:
customers_amz (customer_id) 
↓ 1:M
orders_amz (order_id, customer_id)
↓ 1:M
orderdetails (order_id, product_id)
↓ M:1
products_amz (product_id)

Key Insight: One customer can have multiple orders, and each order can have multiple products.
We need to COUNT how many times each customer bought each product.
*/

-- ============================================
-- STEP 2: Count Purchases Per Customer-Product
-- ============================================

-- First, let's see how many times each customer bought each product
SELECT c.customer_id, c.customer_name, p.product_id, p.product_name, COUNT(*) AS times_purchased
FROM
    customers_amz c
    JOIN orders_amz o ON c.customer_id = o.customer_id
    JOIN orderdetails od ON o.order_id = od.order_id
    JOIN products_amz p ON od.product_id = p.product_id
GROUP BY
    c.customer_id,
    c.customer_name,
    p.product_id,
    p.product_name
ORDER BY c.customer_name, times_purchased DESC;

/*
This gives us:
Alice Johnson | Coffee Beans  | 5
Alice Johnson | Wireless Mouse| 2
Bob Smith     | Wireless Mouse| 4
Bob Smith     | USB-C Cable   | 2
...
*/

-- ============================================
-- STEP 3: Filter to 3+ Purchases (HAVING Clause)
-- ============================================

-- Now filter to only show products bought 3+ times
SELECT c.customer_id, c.customer_name, p.product_id, p.product_name, COUNT(*) AS times_purchased
FROM
    customers_amz c
    JOIN orders_amz o ON c.customer_id = o.customer_id
    JOIN orderdetails od ON o.order_id = od.order_id
    JOIN products_amz p ON od.product_id = p.product_id
GROUP BY
    c.customer_id,
    c.customer_name,
    p.product_id,
    p.product_name
HAVING
    COUNT(*) >= 3
ORDER BY c.customer_name, times_purchased DESC;

/*
This gives us:
Alice Johnson | Coffee Beans  | 5
Bob Smith     | Wireless Mouse| 4
Carol White   | USB-C Cable   | 3
Emma Davis    | Water Bottle  | 3

But wait! Alice also bought Wireless Mouse 2 times (doesn't show).
We need the MOST purchased product per customer.
*/

-- ============================================
-- STEP 4: Find the MOST Purchased Product (ROW_NUMBER)
-- ============================================

-- Use ROW_NUMBER() to rank products by purchase count per customer
WITH
    customer_product_counts AS (
        SELECT c.customer_id, c.customer_name, p.product_id, p.product_name, COUNT(*) AS times_purchased
        FROM
            customers_amz c
            JOIN orders_amz o ON c.customer_id = o.customer_id
            JOIN orderdetails od ON o.order_id = od.order_id
            JOIN products_amz p ON od.product_id = p.product_id
        GROUP BY
            c.customer_id,
            c.customer_name,
            p.product_id,
            p.product_name
        HAVING
            COUNT(*) >= 3 -- Only products bought 3+ times
    ),
    ranked_products AS (
        SELECT
            customer_id,
            customer_name,
            product_id,
            product_name,
            times_purchased,
            ROW_NUMBER() OVER (
                PARTITION BY
                    customer_id
                ORDER BY times_purchased DESC
            ) AS rn
        FROM customer_product_counts
    )
SELECT
    customer_name,
    product_name,
    times_purchased
FROM ranked_products
WHERE
    rn = 1 -- Only the top product per customer
ORDER BY customer_name;

-- ============================================
-- ALTERNATIVE SOLUTION (Using MAX and Subquery)
-- ============================================

WITH
    customer_product_counts AS (
        SELECT c.customer_id, c.customer_name, p.product_id, p.product_name, COUNT(*) AS times_purchased
        FROM
            customers_amz c
            JOIN orders_amz o ON c.customer_id = o.customer_id
            JOIN orderdetails od ON o.order_id = od.order_id
            JOIN products_amz p ON od.product_id = p.product_id
        GROUP BY
            c.customer_id,
            c.customer_name,
            p.product_id,
            p.product_name
        HAVING
            COUNT(*) >= 3
    ),
    max_purchases AS (
        SELECT customer_id, MAX(times_purchased) AS max_count
        FROM customer_product_counts
        GROUP BY
            customer_id
    )
SELECT cpc.customer_name, cpc.product_name, cpc.times_purchased
FROM
    customer_product_counts cpc
    JOIN max_purchases mp ON cpc.customer_id = mp.customer_id
    AND cpc.times_purchased = mp.max_count
ORDER BY cpc.customer_name;

-- ============================================
-- COMPACT SOLUTION (One CTE)
-- ============================================

WITH
    purchase_counts AS (
        SELECT c.customer_name, p.product_name, COUNT(*) AS times_purchased, ROW_NUMBER() OVER (
                PARTITION BY
                    c.customer_id
                ORDER BY COUNT(*) DESC
            ) AS rank
        FROM
            customers_amz c
            JOIN orders_amz o ON c.customer_id = o.customer_id
            JOIN orderdetails od ON o.order_id = od.order_id
            JOIN products_amz p ON od.product_id = p.product_id
        GROUP BY
            c.customer_id,
            c.customer_name,
            p.product_id,
            p.product_name
        HAVING
            COUNT(*) >= 3
    )
SELECT
    customer_name,
    product_name,
    times_purchased
FROM purchase_counts
WHERE
    rank = 1
ORDER BY customer_name;

-- ============================================
-- KEY CONCEPTS EXPLAINED
-- ============================================

/*
1. GROUP BY with Multiple Joins:
- We join 4 tables to connect customers → orders → order details → products
- GROUP BY customer and product to count purchases

2. HAVING vs WHERE:
- WHERE filters BEFORE grouping (filters rows)
- HAVING filters AFTER grouping (filters groups)
- We use HAVING COUNT(*) >= 3 to filter aggregated results

3. ROW_NUMBER() Window Function:
- PARTITION BY customer_id: Restart numbering for each customer
- ORDER BY times_purchased DESC: Rank by most purchased first
- This gives us rank 1 = most purchased product per customer

4. Alternative: MAX with Self-Join:
- Find the maximum count per customer
- Join back to get the product with that count
- Works but less efficient than ROW_NUMBER()
*/

-- ============================================
-- EXPECTED OUTPUT
-- ============================================

/*
customer_name    | product_name      | times_purchased
-----------------+-------------------+----------------
Alice Johnson    | Coffee Beans 1lb  | 5
Bob Smith        | Wireless Mouse    | 4
Carol White      | USB-C Cable       | 3
Emma Davis       | Water Bottle      | 3

Note: David Brown doesn't appear because he only bought Yoga Mat 2 times (< 3)
*/

-- ============================================
-- COMMON MISTAKES TO AVOID
-- ============================================

/*
❌ MISTAKE 1: Forgetting HAVING
SELECT customer_name, product_name, COUNT(*) 
FROM ... 
WHERE COUNT(*) >= 3  -- ERROR! Can't use aggregate in WHERE

✅ CORRECT:
HAVING COUNT(*) >= 3

❌ MISTAKE 2: Not handling ties
If a customer bought 2 products the same number of times (both 5x),
ROW_NUMBER() picks one arbitrarily. Use RANK() if you want both.

❌ MISTAKE 3: Wrong GROUP BY
GROUP BY customer_name, product_name  -- Missing customer_id!
This can cause issues if two customers have the same name.

✅ CORRECT:
GROUP BY c.customer_id, c.customer_name, p.product_id, p.product_name
*/