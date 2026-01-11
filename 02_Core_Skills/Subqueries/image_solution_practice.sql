-- ============================================
-- THE "WHERE IN" SUBQUERY APPROACH
-- ============================================
-- This matches the solution from your image!

-- LOGIC FLOW:
-- 1. Inner Subquery: Calculate the Global Average Order Amount
-- 2. Middle Subquery: Find customer_ids where SUM(amount) > Global Average
-- 3. Outer Query: Get the names for those specific IDs

SELECT customer_name
FROM customers_new
-- This means where customer_id is IN the list of customer_ids that are in the orders_new table
WHERE customer_id IN (
    --This is a subquery that gets the customer_id from the orders_new table
    -- "Find the list of customers who..."
    SELECT customer_id
    FROM orders_new
    GROUP BY customer_id
    -- "...have a total spend greater than..."
    HAVING SUM(amount) > (
        -- "...the average of all orders"
        SELECT AVG(amount)
        FROM orders_new
    )
);

-- ============================================
-- WHY THIS IS A GOOD APPROACH
-- ============================================
-- 1. Readable: It reads like English logic.
--    "Select names where ID is in (list of high spenders)"
--
-- 2. Safe: It avoids duplicate rows.
--    If you used a JOIN, you might get the customer name multiple times
--    if you didn't group correctly. The "IN" clause handles that naturally.
--
-- 3. Modular: You can easily test just the inner part first.

-- ============================================
-- LET'S TEST THE INNER PARTS SEPARATELY
-- ============================================

-- Step 1: What is the average order?
-- SELECT AVG(amount) FROM orders_new; 
-- Result: 200.00

-- Step 2: Who spent more than 200?
-- SELECT customer_id, SUM(amount) 
-- FROM orders_new 
-- GROUP BY customer_id 
-- HAVING SUM(amount) > 200;
-- Result: ID 1 (300 total), ID 3 (500 total)

-- Step 3: What are their names?
-- Alice Smith (ID 1), Charlie Brown (ID 3)
