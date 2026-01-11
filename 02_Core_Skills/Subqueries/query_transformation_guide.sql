-- ============================================
-- QUERY TRANSFORMATION GUIDE
-- ============================================
-- Understanding how standalone queries become subqueries
-- to answer different questions with the same data

-- ============================================
-- SCENARIO 1: From Simple to Subquery
-- ============================================

-- STEP 1: Start with a simple query
-- Question: "What are all the phones and their prices?"

SELECT 
  phone_id,
  phone_names,
  price_usd
FROM dim_phones_apple
ORDER BY price_usd DESC;

-- Result:
-- phone_id | phone_names              | price_usd
-- jkl012   | Apple - iPhone 13        | 999.99
-- ghi789   | Samsung - Galaxy S21     | 799.99
-- 2695bb9  | Acer - Iconia Talk S     | 759.91


-- STEP 2: Transform into a subquery
-- NEW Question: "What phones are more expensive than the average price?"

-- First, let's see what the average is:
SELECT AVG(price_usd) AS avg_price
FROM dim_phones_apple;
-- Result: avg_price = 687.13 (example)

-- Now use the original query as a filter:
SELECT 
  phone_id,
  phone_names,
  price_usd
FROM dim_phones_apple
WHERE price_usd > (
  -- This is our SUBQUERY - it runs first and returns one value
  SELECT AVG(price_usd)
  FROM dim_phones_apple
)
ORDER BY price_usd DESC;

-- How it works:
-- 1. Subquery runs: SELECT AVG(price_usd) → returns 687.13
-- 2. Main query uses that value: WHERE price_usd > 687.13
-- 3. Returns only phones above average price


-- ============================================
-- SCENARIO 2: From JOIN to Subquery
-- ============================================

-- STEP 1: Start with a JOIN query
-- Question: "Show me all orders with phone details"

SELECT 
  o.order_id,
  o.customer_id,
  p.phone_names,
  p.price_usd
FROM dim_phoneOrders_apple o
JOIN dim_phones_apple p ON o.phone_id = p.phone_id
ORDER BY o.order_time;

-- Result:
-- order_id | customer_id | phone_names           | price_usd
-- 7dd8597  | 009c4e      | Acer - Iconia Talk S  | 759.91
-- ord001   | cust01      | Samsung - Galaxy S21  | 799.99


-- STEP 2: Transform to answer a different question
-- NEW Question: "Which customers ordered phones over $700?"

-- Method A: Using the JOIN (what we know)
SELECT DISTINCT
  o.customer_id
FROM dim_phoneOrders_apple o
JOIN dim_phones_apple p ON o.phone_id = p.phone_id
WHERE p.price_usd > 700;

-- Method B: Using a SUBQUERY (same result, different approach)
SELECT DISTINCT
  customer_id
FROM dim_phoneOrders_apple
WHERE phone_id IN (
  -- This subquery finds all expensive phone IDs
  SELECT phone_id
  FROM dim_phones_apple
  WHERE price_usd > 700
);

-- How it works:
-- 1. Subquery runs: SELECT phone_id WHERE price_usd > 700 
--    → returns ('2695bb9', 'ghi789', 'jkl012')
-- 2. Main query: WHERE phone_id IN ('2695bb9', 'ghi789', 'jkl012')
-- 3. Returns customers who ordered those phones


-- ============================================
-- SCENARIO 3: From Aggregation to Subquery
-- ============================================

-- STEP 1: Start with an aggregation
-- Question: "How many orders does each phone have?"

SELECT 
  phone_id,
  COUNT(*) AS order_count
FROM dim_phoneOrders_apple
GROUP BY phone_id;

-- Result:
-- phone_id | order_count
-- 2695bb9  | 1
-- ghi789   | 2
-- jkl012   | 1


-- STEP 2: Transform to find specific information
-- NEW Question: "Which phones have more than 1 order?"

-- Method A: Using HAVING (simple)
SELECT 
  phone_id,
  COUNT(*) AS order_count
FROM dim_phoneOrders_apple
GROUP BY phone_id
HAVING COUNT(*) > 1;

-- Method B: Using subquery to get phone details
SELECT 
  p.phone_names,
  p.price_usd,
  order_counts.order_count
FROM dim_phones_apple p
JOIN (
  -- This subquery becomes a temporary table
  SELECT 
    phone_id,
    COUNT(*) AS order_count
  FROM dim_phoneOrders_apple
  GROUP BY phone_id
  HAVING COUNT(*) > 1
) AS order_counts ON p.phone_id = order_counts.phone_id;

-- How it works:
-- 1. Subquery runs first: finds phones with >1 order
-- 2. Result becomes a temporary table called "order_counts"
-- 3. Main query joins it with phone details
-- 4. Returns full information about popular phones


-- ============================================
-- SCENARIO 4: CTE Transformation
-- ============================================

-- STEP 1: Original query with string splitting
-- Question: "What are the brands and models?"

SELECT 
  phone_id,
  TRIM(SPLIT_PART(phone_names, ' - ', 1)) AS brand,
  TRIM(SPLIT_PART(phone_names, ' - ', 2)) AS model_name
FROM dim_phones_apple;

-- Result:
-- phone_id | brand   | model_name
-- 2695bb9  | Acer    | Iconia Talk S
-- 76397    | Acer    | Liquid Z6 Plus


-- STEP 2: Transform using CTE (Common Table Expression)
-- NEW Question: "Which brands have phones without orders?"

WITH split_phones AS (
  -- This CTE is like a temporary view of our split data
  SELECT 
    phone_id,
    TRIM(SPLIT_PART(phone_names, ' - ', 1)) AS brand,
    TRIM(SPLIT_PART(phone_names, ' - ', 2)) AS model_name
  FROM dim_phones_apple
)
SELECT DISTINCT
  sp.brand,
  sp.model_name
FROM split_phones sp  -- Now we can use the CTE like a table
LEFT JOIN dim_phoneOrders_apple po ON sp.phone_id = po.phone_id
WHERE po.order_id IS NULL
ORDER BY sp.brand, sp.model_name;

-- How it works:
-- 1. CTE runs first: creates temporary "split_phones" table
-- 2. Main query uses split_phones just like a regular table
-- 3. Performs LEFT JOIN to find phones without orders
-- 4. Returns brand/model combinations with no sales


-- ============================================
-- SCENARIO 5: Nested Subqueries
-- ============================================

-- STEP 1: Find the most expensive phone
SELECT MAX(price_usd) AS max_price
FROM dim_phones_apple;
-- Result: 999.99

-- STEP 2: Find which phone has that price
SELECT phone_names
FROM dim_phones_apple
WHERE price_usd = (
  SELECT MAX(price_usd)
  FROM dim_phones_apple
);
-- Result: Apple - iPhone 13

-- STEP 3: Find all orders for the most expensive phone
SELECT 
  o.order_id,
  o.customer_id,
  o.order_status
FROM dim_phoneOrders_apple o
WHERE o.phone_id = (
  -- Nested subquery level 1: Find the phone_id
  SELECT phone_id
  FROM dim_phones_apple
  WHERE price_usd = (
    -- Nested subquery level 2: Find the max price
    SELECT MAX(price_usd)
    FROM dim_phones_apple
  )
);

-- How it works (inside-out):
-- 1. Innermost: SELECT MAX(price_usd) → 999.99
-- 2. Middle: SELECT phone_id WHERE price_usd = 999.99 → 'jkl012'
-- 3. Outer: SELECT orders WHERE phone_id = 'jkl012'


-- ============================================
-- TRANSFORMATION PATTERNS SUMMARY
-- ============================================

-- Pattern 1: SCALAR SUBQUERY (returns one value)
-- Before: SELECT AVG(price_usd) FROM phones;
-- After:  WHERE price_usd > (SELECT AVG(price_usd) FROM phones)

-- Pattern 2: IN SUBQUERY (returns multiple values)
-- Before: SELECT phone_id FROM phones WHERE price_usd > 700;
-- After:  WHERE phone_id IN (SELECT phone_id FROM phones WHERE price_usd > 700)

-- Pattern 3: FROM SUBQUERY (creates temporary table)
-- Before: SELECT phone_id, COUNT(*) FROM orders GROUP BY phone_id;
-- After:  FROM (SELECT phone_id, COUNT(*) FROM orders GROUP BY phone_id) AS counts

-- Pattern 4: CTE (named temporary table)
-- Before: SELECT phone_id, SPLIT_PART(...) FROM phones;
-- After:  WITH split AS (SELECT phone_id, SPLIT_PART(...) FROM phones)
--         SELECT * FROM split WHERE ...

-- Pattern 5: EXISTS SUBQUERY (checks for existence)
-- Before: SELECT phone_id FROM orders WHERE phone_id = 'abc';
-- After:  WHERE EXISTS (SELECT 1 FROM orders WHERE phone_id = phones.phone_id)
