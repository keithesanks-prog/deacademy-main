-- ============================================
-- TRIM & DELIMITER TRAINING (PostgreSQL)
-- ============================================
-- Topic: String manipulation with TRIM, POSITION, SUBSTRING
-- Use Case: Splitting delimited strings (e.g., "Brand - Model")

-- ⚠️ IMPORTANT: Run apple_phones_setup.sql FIRST to create tables!
-- Then run apple_phones_solution.sql for the complete working solution.
-- This file is for learning the concepts step-by-step.

-- ============================================
-- PART 1: UNDERSTANDING THE FUNCTIONS (PostgreSQL)
-- ============================================

-- TRIM() - Removes leading and trailing spaces
-- Example:
-- TRIM('  Hello  ') → 'Hello'
-- TRIM('  Acer - Iconia  ') → 'Acer - Iconia'

-- POSITION(substring IN string) - Finds position of substring in string
-- Example:
-- POSITION('-' IN 'Acer - Iconia') → 6 (position of the dash)
-- Returns 0 if not found

-- SUBSTRING(string FROM start FOR length) - Extracts substring
-- Example:
-- SUBSTRING('Acer - Iconia' FROM 1 FOR 4) → 'Acer'

-- LENGTH(string) - Returns length of string
-- Example:
-- LENGTH('Acer - Iconia') → 14

-- SPLIT_PART(string, delimiter, field_number) - PostgreSQL specific!
-- Example:
-- SPLIT_PART('Acer - Iconia', ' - ', 1) → 'Acer'
-- SPLIT_PART('Acer - Iconia', ' - ', 2) → 'Iconia'


-- ============================================
-- PART 2: BREAKING DOWN THE SPLITTING LOGIC
-- ============================================

-- Given: "Acer - Iconia Talk S"
-- Goal: Extract "Acer" as brand and "Iconia Talk S" as model

-- METHOD 1: Using SPLIT_PART (PostgreSQL's easiest way!)
-- SPLIT_PART('Acer - Iconia Talk S', ' - ', 1) → 'Acer'
-- SPLIT_PART('Acer - Iconia Talk S', ' - ', 2) → 'Iconia Talk S'

-- METHOD 2: Using POSITION and SUBSTRING (more manual)
-- Step-by-step breakdown:
-- 1. Find delimiter position: POSITION(' - ' IN 'Acer - Iconia Talk S') = 5
-- 2. Extract brand (everything BEFORE delimiter):
--    SUBSTRING('Acer - Iconia Talk S' FROM 1 FOR 4) = 'Acer'
-- 
-- 3. Extract model (everything AFTER delimiter):
--    SUBSTRING('Acer - Iconia Talk S' FROM 8) = 'Iconia Talk S'


-- ============================================
-- PART 3: VISUAL EXAMPLE WITH POSITIONS
-- ============================================

-- String: "Acer - Iconia Talk S"
-- Position: 123456789...
--           A c e r   -   I c o n i a   T a l k   S
--           1 2 3 4 5 6 7 8 9 ...

-- POSITION(' - ' IN 'Acer - Iconia Talk S') returns 5
-- SUBSTRING needs to start at 1 and take 4 characters to get "Acer"
-- SUBSTRING needs to start at 8 to skip " - " and get "Iconia Talk S"


-- ============================================
-- PART 4: HANDLING DIFFERENT DELIMITERS
-- ============================================

-- Sometimes data has inconsistent delimiters:
-- "Acer - Iconia"  (has dash with spaces)
-- "Acer-Iconia"    (has dash without spaces)
-- "Acer | Iconia"  (has pipe)

-- Solution: Detect which delimiter is used first
-- This is what the CTE approach does:

-- WITH cte AS (
--   SELECT 
--     phone_id,
--     phone_names,
--     CASE 
--       WHEN POSITION(' - ' IN phone_names) > 0 THEN ' - '
--       WHEN POSITION('-' IN phone_names) > 0 THEN '-'
--       WHEN POSITION('|' IN phone_names) > 0 THEN '|'
--       ELSE ' - '  -- default
--     END AS delimiter_used
--   FROM dim_phones_apple
-- )


-- ============================================
-- PART 5: COMPLETE SOLUTION TEMPLATE
-- ============================================

-- METHOD 1: Using SPLIT_PART (Easiest for PostgreSQL!)
SELECT 
  phone_id,
  phone_names,
  TRIM(SPLIT_PART(phone_names, ' - ', 1)) AS brand,
  TRIM(SPLIT_PART(phone_names, ' - ', 2)) AS model_name
FROM dim_phones_apple
ORDER BY brand, model_name;


-- METHOD 2: Using POSITION and SUBSTRING (More flexible)
WITH cte AS (
  SELECT 
    phone_id,
    phone_names,
    price_usd,
    CASE 
      WHEN POSITION(' - ' IN phone_names) > 0 THEN ' - '
      ELSE '-'
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

SELECT 
  phone_id,
  phone_names,
  brand,
  model_name
FROM split_phones
ORDER BY brand, model_name;


-- ============================================
-- PART 6: FINDING BRANDS/MODELS WITHOUT ORDERS
-- ============================================

-- Problem: Which brand/model combinations have NO orders?
-- Approach: LEFT JOIN phones with orders, then filter for NULL order_ids

WITH split_phones AS (
  SELECT 
    phone_id,
    phone_names,
    price_usd,
    TRIM(SPLIT_PART(phone_names, ' - ', 1)) AS brand,
    TRIM(SPLIT_PART(phone_names, ' - ', 2)) AS model_name
  FROM dim_phones_apple
)

-- Find phones that don't appear in orders table
SELECT DISTINCT
  sp.brand,
  sp.model_name
FROM split_phones sp
LEFT JOIN dim_phoneOrders_apple po ON sp.phone_id = po.phone_id
WHERE po.order_id IS NULL  -- No matching orders
ORDER BY sp.brand, sp.model_name;


-- ============================================
-- ALTERNATIVE APPROACH: USING NOT EXISTS
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

-- Find phones that don't appear in orders table using NOT EXISTS
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
-- PART 7: PRACTICE EXERCISES
-- ============================================

-- Exercise 1: Extract just the brands (no duplicates)
-- Hint: Use DISTINCT on the brand column
SELECT DISTINCT TRIM(SPLIT_PART(phone_names, ' - ', 1)) AS brand
FROM dim_phones_apple
ORDER BY brand;


-- Exercise 2: Count how many models each brand has
-- Hint: GROUP BY brand and COUNT(DISTINCT model_name)
SELECT 
  TRIM(SPLIT_PART(phone_names, ' - ', 1)) AS brand,
  COUNT(*) AS model_count
FROM dim_phones_apple
GROUP BY brand
ORDER BY brand;


-- Exercise 3: Find brands that have at least one model with orders
-- Hint: Use INNER JOIN instead of LEFT JOIN
WITH split_phones AS (
  SELECT 
    phone_id,
    TRIM(SPLIT_PART(phone_names, ' - ', 1)) AS brand,
    TRIM(SPLIT_PART(phone_names, ' - ', 2)) AS model_name
  FROM dim_phones_apple
)

SELECT DISTINCT sp.brand
FROM split_phones sp
INNER JOIN dim_phoneOrders_apple po ON sp.phone_id = po.phone_id
ORDER BY sp.brand;


-- Exercise 4: Find the most expensive phone for each brand
-- Hint: Use window functions or GROUP BY with MAX(price_usd)
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
  brand,
  model_name,
  price_usd
FROM (
  SELECT 
    brand,
    model_name,
    price_usd,
    RANK() OVER (PARTITION BY brand ORDER BY price_usd DESC) as price_rank
  FROM split_phones
) ranked
WHERE price_rank = 1
ORDER BY brand;


-- ============================================
-- DEBUGGING TIPS
-- ============================================

-- 1. Always check what POSITION returns:
SELECT 
  phone_names, 
  POSITION(' - ' IN phone_names) AS delimiter_position
FROM dim_phones_apple;

-- 2. Test SPLIT_PART on sample data:
SELECT 
  phone_names,
  SPLIT_PART(phone_names, ' - ', 1) AS brand_part,
  SPLIT_PART(phone_names, ' - ', 2) AS model_part
FROM dim_phones_apple;

-- 3. Test with a single row first:
SELECT * FROM dim_phones_apple WHERE phone_id = '2695bb9';
