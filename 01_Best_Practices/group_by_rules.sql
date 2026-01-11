-- ============================================
-- GROUP BY RULES: The ID and Name Relationship
-- ============================================
-- Understanding what you must include in GROUP BY

-- ============================================
-- THE GOLDEN RULE
-- ============================================
-- "If you SELECT it and you don't aggregate it (SUM, COUNT, AVG, etc.),
--  you MUST include it in GROUP BY"

-- ============================================
-- SETUP: Sample Data
-- ============================================
DROP TABLE IF EXISTS campaigns CASCADE;

CREATE TABLE campaigns (
    campaign_id INT,
    campaign_name VARCHAR(100),
    clicks INT,
    impressions INT
);

INSERT INTO campaigns VALUES
(1, 'Summer Sale', 100, 1000),
(1, 'Summer Sale', 150, 1200),  -- Same campaign, different metrics
(1, 'Summer Sale', 200, 1500),
(2, 'Winter Promo', 300, 2000),
(2, 'Winter Promo', 250, 1800),
(3, 'Spring Launch', 400, 3000);

SELECT * FROM campaigns ORDER BY campaign_id;


-- ============================================
-- EXAMPLE 1: The ID and Name Relationship
-- ============================================

-- ❌ WRONG: GROUP BY name only
/*
SELECT
    campaign_id,      -- Selected but not in GROUP BY!
    campaign_name,    -- In GROUP BY ✓
    SUM(clicks) AS total_clicks
FROM campaigns
GROUP BY campaign_name;

-- ERROR: column "campaign_id" must appear in the GROUP BY clause
-- or be used in an aggregate function
*/

-- Why it fails:
-- The database doesn't ASSUME that campaign_id and campaign_name have a 1:1 relationship
-- Even though logically they do, SQL requires you to be explicit!


-- ✅ CORRECT: GROUP BY both ID and name
SELECT
    campaign_id,       -- In GROUP BY ✓
    campaign_name,     -- In GROUP BY ✓
    SUM(clicks) AS total_clicks,
    SUM(impressions) AS total_impressions
FROM campaigns
GROUP BY campaign_id, campaign_name
ORDER BY campaign_id;

-- Expected Output:
-- campaign_id | campaign_name  | total_clicks | total_impressions
-- ------------|----------------|--------------|------------------
-- 1           | Summer Sale    | 450          | 3700
-- 2           | Winter Promo   | 550          | 3800
-- 3           | Spring Launch  | 400          | 3000


-- ============================================
-- WHY THE DATABASE IS "PEDANTIC"
-- ============================================

-- Scenario 1: What if the data is inconsistent?
-- campaign_id | campaign_name
-- ------------|---------------
-- 1           | Summer Sale
-- 1           | Summer Sale 2024  ← Same ID, different name!

-- If you only GROUP BY campaign_name, which ID should it use?
-- The database can't decide, so it requires you to GROUP BY both.


-- ============================================
-- THE RULE IN ACTION
-- ============================================

-- ✅ CORRECT: Everything in SELECT is either aggregated or in GROUP BY
SELECT
    campaign_id,           -- In GROUP BY ✓
    campaign_name,         -- In GROUP BY ✓
    SUM(clicks),           -- Aggregated ✓
    AVG(impressions),      -- Aggregated ✓
    COUNT(*) AS row_count  -- Aggregated ✓
FROM campaigns
GROUP BY campaign_id, campaign_name;


-- ❌ WRONG: Missing column in GROUP BY
/*
SELECT
    campaign_id,      -- In GROUP BY ✓
    campaign_name,    -- NOT in GROUP BY ✗
    SUM(clicks)       -- Aggregated ✓
FROM campaigns
GROUP BY campaign_id;  -- Missing campaign_name!

-- ERROR!
*/


-- ============================================
-- SCAFFOLDING: Verify Your Grouping
-- ============================================

-- See which rows are being grouped together
SELECT
    campaign_id,
    campaign_name,
    clicks,
    impressions,
    -- SCAFFOLDING: Show what the SUM will be for this group
    SUM(clicks) OVER (PARTITION BY campaign_id, campaign_name) AS total_clicks_in_group,
    -- SCAFFOLDING: Show how many rows in this group
    COUNT(*) OVER (PARTITION BY campaign_id, campaign_name) AS rows_in_group
FROM campaigns
ORDER BY campaign_id, clicks;

-- This shows you EACH ROW and what group it belongs to


-- ============================================
-- COMMON SCENARIOS
-- ============================================

-- Scenario 1: ID only (if name isn't needed)
SELECT
    campaign_id,
    SUM(clicks) AS total_clicks
FROM campaigns
GROUP BY campaign_id;  -- Only need ID


-- Scenario 2: ID and Name (most common)
SELECT
    campaign_id,
    campaign_name,
    SUM(clicks) AS total_clicks
FROM campaigns
GROUP BY campaign_id, campaign_name;  -- Need both


-- Scenario 3: Multiple descriptive columns
SELECT
    campaign_id,
    campaign_name,
    campaign_type,      -- Another descriptive column
    campaign_region,    -- Another descriptive column
    SUM(clicks) AS total_clicks
FROM campaigns
GROUP BY 
    campaign_id,
    campaign_name,
    campaign_type,
    campaign_region;    -- ALL non-aggregated columns!


-- ============================================
-- POSTGRESQL SHORTCUT (Functional Dependency)
-- ============================================
-- If campaign_id is the PRIMARY KEY, PostgreSQL is smart enough
-- to know that all other columns are functionally dependent on it

DROP TABLE IF EXISTS campaigns_pk CASCADE;

CREATE TABLE campaigns_pk (
    campaign_id INT PRIMARY KEY,  -- ← PRIMARY KEY!
    campaign_name VARCHAR(100),
    campaign_type VARCHAR(50)
);

INSERT INTO campaigns_pk VALUES
(1, 'Summer Sale', 'Seasonal'),
(2, 'Winter Promo', 'Seasonal'),
(3, 'Spring Launch', 'Product');

-- In PostgreSQL, this works because campaign_id is the PRIMARY KEY:
SELECT
    campaign_id,       -- PRIMARY KEY, in GROUP BY ✓
    campaign_name,     -- Functionally dependent on campaign_id ✓
    campaign_type      -- Functionally dependent on campaign_id ✓
FROM campaigns_pk
GROUP BY campaign_id;  -- Only need to group by PRIMARY KEY!

-- But this is PostgreSQL-specific! In MySQL, you'd still need all columns.


-- ============================================
-- DECISION TREE: What to Include in GROUP BY
-- ============================================

/*
For each column in SELECT:
├─ Is it aggregated (SUM, COUNT, AVG, etc.)?
│  └─ YES → Don't include in GROUP BY
│  └─ NO → Continue to next question
│
├─ Is it in the GROUP BY clause?
│  └─ YES → ✓ Correct
│  └─ NO → ✗ ERROR! Add it to GROUP BY
*/


-- ============================================
-- PRACTICE EXERCISES
-- ============================================

-- Practice 1: Fix this query
/*
SELECT
    campaign_id,
    campaign_name,
    SUM(clicks)
FROM campaigns
GROUP BY campaign_id;  -- What's missing?
*/

-- Practice 2: What needs to be in GROUP BY?
/*
SELECT
    campaign_id,
    campaign_name,
    campaign_type,
    AVG(clicks),
    MAX(impressions)
FROM campaigns
GROUP BY ???;  -- Fill in the blanks
*/

-- Practice 3: Identify the error
/*
SELECT
    campaign_name,
    clicks,  -- ← This is the problem!
    SUM(impressions)
FROM campaigns
GROUP BY campaign_name;
*/


-- ============================================
-- KEY TAKEAWAYS
-- ============================================
-- 1. If you SELECT it and don't aggregate it, you MUST GROUP BY it
-- 2. The database doesn't assume ID and Name have a 1:1 relationship
-- 3. Include ALL non-aggregated columns in GROUP BY
-- 4. PostgreSQL allows grouping by PRIMARY KEY only (functional dependency)
-- 5. When in doubt, include it in GROUP BY!
