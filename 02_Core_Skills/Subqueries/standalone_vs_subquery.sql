-- ============================================
-- SIDE-BY-SIDE QUERY COMPARISON
-- ============================================
-- Seeing the SAME query standalone vs. as a subquery
-- with clear annotations showing where subquery data appears

-- ============================================
-- EXAMPLE 1: Average Price Comparison
-- ============================================

-- STANDALONE QUERY A: Get the average price
-- Run this first to see what value we get
SELECT AVG(price_usd) AS average_price
FROM dim_phones_apple;

-- Result: 687.13
-- ↑ This single number will be used in the subquery version


-- STANDALONE QUERY B: Get all phones with their prices
SELECT 
  phone_names,
  price_usd
FROM dim_phones_apple
ORDER BY price_usd DESC;

-- Result:
-- phone_names              | price_usd
-- Apple - iPhone 13        | 999.99
-- Acer - Iconia Talk S     | 759.91
-- Samsung - Galaxy S21     | 799.99
-- Google - Pixel 6         | 599.99


-- COMBINED WITH SUBQUERY: Same query but filtered by average
-- The subquery replaces the hardcoded number with a calculated value
SELECT 
  phone_names,
  price_usd,
  (SELECT AVG(price_usd) FROM dim_phones_apple) AS avg_price  -- ← SUBQUERY DATA appears here
FROM dim_phones_apple
WHERE price_usd > (SELECT AVG(price_usd) FROM dim_phones_apple)  -- ← SUBQUERY used as filter
ORDER BY price_usd DESC;

-- Result with subquery data shown:
-- phone_names              | price_usd | avg_price (from subquery)
-- Apple - iPhone 13        | 999.99    | 687.13  ← This 687.13 came from the subquery
-- Samsung - Galaxy S21     | 799.99    | 687.13  ← Same value for every row
-- Acer - Iconia Talk S     | 759.91    | 687.13  ← Subquery ran once, used everywhere


-- ============================================
-- EXAMPLE 2: Finding Expensive Phone IDs
-- ============================================

-- STANDALONE QUERY A: Get IDs of expensive phones
SELECT phone_id
FROM dim_phones_apple
WHERE price_usd > 700;

-- Result:
-- phone_id
-- 2695bb9
-- ghi789
-- jkl012
-- ↑ These 3 IDs will be used in the subquery version


-- STANDALONE QUERY B: Get all orders
SELECT 
  order_id,
  customer_id,
  phone_id
FROM dim_phoneOrders_apple;

-- Result:
-- order_id | customer_id | phone_id
-- 7dd8597  | 009c4e      | 2695bb9
-- ord001   | cust01      | ghi789
-- ord002   | cust02      | jkl012
-- ord003   | cust03      | mno345


-- COMBINED WITH SUBQUERY: Filter orders by expensive phones
SELECT 
  order_id,
  customer_id,
  phone_id,
  '← This phone_id matches subquery list' AS note
FROM dim_phoneOrders_apple
WHERE phone_id IN (
  SELECT phone_id              -- ← SUBQUERY returns: 2695bb9, ghi789, jkl012
  FROM dim_phones_apple
  WHERE price_usd > 700
);

-- Result showing which rows matched the subquery:
-- order_id | customer_id | phone_id | note
-- 7dd8597  | 009c4e      | 2695bb9  | ← This phone_id matches subquery list (2695bb9 ✓)
-- ord001   | cust01      | ghi789   | ← This phone_id matches subquery list (ghi789 ✓)
-- ord002   | cust02      | jkl012   | ← This phone_id matches subquery list (jkl012 ✓)
-- (ord003 with mno345 was filtered out because mno345 not in subquery results)


-- ============================================
-- EXAMPLE 3: Order Counts
-- ============================================

-- STANDALONE QUERY A: Count orders per phone
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
-- mno345   | 1
-- ↑ This entire table becomes available in the subquery version


-- STANDALONE QUERY B: Get phone details
SELECT 
  phone_id,
  phone_names,
  price_usd
FROM dim_phones_apple;

-- Result:
-- phone_id | phone_names              | price_usd
-- 2695bb9  | Acer - Iconia Talk S     | 759.91
-- ghi789   | Samsung - Galaxy S21     | 799.99


-- COMBINED WITH SUBQUERY: Join phone details with order counts
SELECT 
  p.phone_names,
  p.price_usd,
  counts.order_count,  -- ← SUBQUERY DATA: This column comes from the subquery
  counts.phone_id      -- ← SUBQUERY DATA: This is how we joined
FROM dim_phones_apple p
JOIN (
  -- This entire result set becomes the "counts" table
  SELECT 
    phone_id,
    COUNT(*) AS order_count
  FROM dim_phoneOrders_apple
  GROUP BY phone_id
) AS counts ON p.phone_id = counts.phone_id;

-- Result showing subquery data:
-- phone_names              | price_usd | order_count (from subquery) | phone_id (from subquery)
-- Acer - Iconia Talk S     | 759.91    | 1 ← came from subquery      | 2695bb9 ← came from subquery
-- Samsung - Galaxy S21     | 799.99    | 2 ← came from subquery      | ghi789 ← came from subquery


-- ============================================
-- EXAMPLE 4: String Splitting with CTE
-- ============================================

-- STANDALONE QUERY A: Split phone names
SELECT 
  phone_id,
  TRIM(SPLIT_PART(phone_names, ' - ', 1)) AS brand,
  TRIM(SPLIT_PART(phone_names, ' - ', 2)) AS model_name
FROM dim_phones_apple;

-- Result:
-- phone_id | brand   | model_name
-- 2695bb9  | Acer    | Iconia Talk S
-- 76397    | Acer    | Liquid Z6 Plus
-- abc123   | Acer    | Iconia Tab 10 A3-A40
-- ↑ This entire result set becomes available as "split_phones"


-- STANDALONE QUERY B: Find phones without orders
SELECT phone_id
FROM dim_phones_apple p
WHERE NOT EXISTS (
  SELECT 1 FROM dim_phoneOrders_apple o WHERE o.phone_id = p.phone_id
);

-- Result:
-- phone_id
-- 76397
-- abc123
-- def456


-- COMBINED WITH CTE: Use split data to show brand/model without orders
WITH split_phones AS (
  -- This CTE makes the split data available as a table
  SELECT 
    phone_id,
    TRIM(SPLIT_PART(phone_names, ' - ', 1)) AS brand,
    TRIM(SPLIT_PART(phone_names, ' - ', 2)) AS model_name
  FROM dim_phones_apple
)
SELECT 
  sp.brand,        -- ← CTE DATA: brand column from split_phones
  sp.model_name,   -- ← CTE DATA: model_name column from split_phones
  sp.phone_id      -- ← CTE DATA: phone_id from split_phones
FROM split_phones sp  -- ← Using the CTE as if it's a real table
LEFT JOIN dim_phoneOrders_apple po ON sp.phone_id = po.phone_id
WHERE po.order_id IS NULL;

-- Result showing CTE data:
-- brand (from CTE) | model_name (from CTE)      | phone_id (from CTE)
-- Acer             | Liquid Z6 Plus             | 76397
-- Acer             | Iconia Tab 10 A3-A40       | abc123
-- Acer             | Liquid X2                  | def456
-- ↑ All these columns came from the split_phones CTE


-- ============================================
-- EXAMPLE 5: Nested Subqueries with Annotations
-- ============================================

-- STANDALONE QUERY A: Find max price
SELECT MAX(price_usd) AS max_price
FROM dim_phones_apple;

-- Result: 999.99
-- ↑ This value goes into subquery level 2


-- STANDALONE QUERY B: Find phone with max price
SELECT phone_id
FROM dim_phones_apple
WHERE price_usd = 999.99;  -- We know this from query A

-- Result: jkl012
-- ↑ This value goes into subquery level 1


-- STANDALONE QUERY C: Find orders for a specific phone
SELECT 
  order_id,
  customer_id,
  order_status
FROM dim_phoneOrders_apple
WHERE phone_id = 'jkl012';  -- We know this from query B

-- Result:
-- order_id | customer_id | order_status
-- ord002   | cust02      | Completed


-- COMBINED WITH NESTED SUBQUERIES: All in one query
SELECT 
  order_id,
  customer_id,
  order_status,
  (SELECT MAX(price_usd) FROM dim_phones_apple) AS max_price,  -- ← Shows 999.99
  (SELECT phone_id FROM dim_phones_apple 
   WHERE price_usd = (SELECT MAX(price_usd) FROM dim_phones_apple)) AS expensive_phone_id  -- ← Shows jkl012
FROM dim_phoneOrders_apple
WHERE phone_id = (
  -- SUBQUERY LEVEL 1: Find the phone_id
  SELECT phone_id
  FROM dim_phones_apple
  WHERE price_usd = (
    -- SUBQUERY LEVEL 2: Find the max price (999.99)
    SELECT MAX(price_usd)
    FROM dim_phones_apple
  )
);

-- Result with all subquery data visible:
-- order_id | customer_id | order_status | max_price (subquery) | expensive_phone_id (subquery)
-- ord002   | cust02      | Completed    | 999.99 ← from subquery | jkl012 ← from nested subquery


-- ============================================
-- VISUAL SUMMARY
-- ============================================

-- Pattern: STANDALONE → SUBQUERY transformation

-- 1. Run standalone query, note the result
-- 2. Use that result in WHERE, SELECT, or FROM clause
-- 3. The subquery data appears in:
--    - WHERE clause: as a filter value
--    - SELECT clause: as a new column
--    - FROM clause: as a temporary table
--    - IN clause: as a list to check against

-- Key insight: Every subquery could be run standalone first
-- to see what data it produces, then that data is used
-- by the outer query!
