-- ============================================
-- APPLE PHONES PRACTICE - SOLUTION (PostgreSQL)
-- ============================================
-- Run apple_phones_setup.sql FIRST to create tables!

-- ============================================
-- SOLUTION: Find brands/models without orders
-- ============================================

-- METHOD 1: Using SPLIT_PART (Easiest for PostgreSQL!)
WITH split_phones AS (
  SELECT 
    phone_id,
    phone_names,
    price_usd,
    TRIM(SPLIT_PART(phone_names, ' - ', 1)) AS brand,
    TRIM(SPLIT_PART(phone_names, ' - ', 2)) AS model_name
  FROM dim_phones_apple
)

-- Find phones that have NO orders using LEFT JOIN
SELECT DISTINCT
  sp.brand,
  sp.model_name
FROM split_phones sp
LEFT JOIN dim_phoneOrders_apple po ON sp.phone_id = po.phone_id
WHERE po.order_id IS NULL  -- No matching orders found
ORDER BY sp.brand, sp.model_name;


-- ============================================
-- METHOD 2: Using POSITION and SUBSTRING
-- ============================================

WITH cte AS (
  SELECT 
    phone_id,
    phone_names,
    price_usd,
    CASE 
      WHEN POSITION(' - ' IN phone_names) > 0 THEN ' - '
      WHEN POSITION('-' IN phone_names) > 0 THEN '-'
      ELSE ' - '
    END AS delimiter_used
  FROM dim_phones_apple
),

split_phones AS (
  SELECT 
    phone_id,
    phone_names,
    price_usd,
    delimiter_used,
    TRIM(SUBSTRING(phone_names FROM 1 FOR POSITION(delimiter_used IN phone_names) - 1)) AS brand,
    TRIM(SUBSTRING(phone_names FROM POSITION(delimiter_used IN phone_names) + LENGTH(delimiter_used))) AS model_name
  FROM cte
)

SELECT DISTINCT
  sp.brand,
  sp.model_name
FROM split_phones sp
LEFT JOIN dim_phoneOrders_apple po ON sp.phone_id = po.phone_id
WHERE po.order_id IS NULL
ORDER BY sp.brand, sp.model_name;


-- ============================================
-- METHOD 3: Using NOT EXISTS
-- ============================================

WITH split_phones AS (
  SELECT 
    phone_id,
    phone_names,
    price_usd,
    TRIM(SPLIT_PART(phone_names, ' - ', 1)) AS brand,
    TRIM(SPLIT_PART(phone_names, ' - ', 2)) AS model_name
  FROM dim_phones_apple
)

SELECT DISTINCT
  sp.brand,
  sp.model_name
FROM split_phones sp
WHERE NOT EXISTS (
  SELECT 1 
  FROM dim_phoneOrders_apple po 
  WHERE po.phone_id = sp.phone_id
)
ORDER BY sp.brand, sp.model_name;


-- ============================================
-- BONUS: See the full breakdown
-- ============================================

WITH split_phones AS (
  SELECT 
    phone_id,
    phone_names,
    price_usd,
    TRIM(SPLIT_PART(phone_names, ' - ', 1)) AS brand,
    TRIM(SPLIT_PART(phone_names, ' - ', 2)) AS model_name
  FROM dim_phones_apple
)

SELECT 
  sp.phone_id,
  sp.brand,
  sp.model_name,
  sp.price_usd,
  CASE 
    WHEN po.order_id IS NOT NULL THEN 'Has Orders ✓'
    ELSE 'No Orders ✗'
  END AS order_status,
  COUNT(po.order_id) AS order_count
FROM split_phones sp
LEFT JOIN dim_phoneOrders_apple po ON sp.phone_id = po.phone_id
GROUP BY sp.phone_id, sp.brand, sp.model_name, sp.price_usd, po.order_id
ORDER BY sp.brand, sp.model_name;


-- ============================================
-- COMPARISON: All three methods side by side
-- ============================================

-- All three methods produce the same result!
-- Choose based on:
-- - SPLIT_PART: Simplest, best for consistent delimiters
-- - POSITION/SUBSTRING: More flexible for complex parsing
-- - NOT EXISTS: Often faster for large datasets
