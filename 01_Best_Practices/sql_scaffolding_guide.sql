-- ============================================
-- SQL SCAFFOLDING: Building Queries Step-by-Step
-- ============================================
-- The Professional Approach to Complex SQL Development

-- ============================================
-- WHAT IS SCAFFOLDING?
-- ============================================
-- Scaffolding = Temporarily adding columns to verify your logic works
-- De-Scaffolding = Removing those columns for the final, clean output

-- Think of it like building a house:
-- 1. Put up scaffolding to work safely
-- 2. Build the structure
-- 3. Remove the scaffolding when done
-- Result: A clean, finished product

-- ============================================
-- SETUP: Sample Data
-- ============================================
DROP TABLE IF EXISTS employee_performance CASCADE;

CREATE TABLE employee_performance (
    employee_id INT,
    employee_name VARCHAR(100),
    department VARCHAR(50),
    year INT,
    projects_completed INT,
    hours_worked INT,
    revenue_generated DECIMAL(10,2)
);

INSERT INTO employee_performance VALUES
(1, 'Alice Johnson', 'Engineering', 2022, 5, 160, 50000),
(1, 'Alice Johnson', 'Engineering', 2023, 7, 180, 70000),
(1, 'Alice Johnson', 'Engineering', 2024, 6, 170, 65000),
(2, 'Bob Smith', 'Sales', 2022, 3, 120, 30000),
(2, 'Bob Smith', 'Sales', 2024, 4, 140, 40000),  -- Gap year!
(3, 'Charlie Brown', 'Engineering', 2023, 8, 200, 80000),
(3, 'Charlie Brown', 'Engineering', 2024, 9, 210, 90000);

SELECT * FROM employee_performance ORDER BY employee_name, year;


-- ============================================
-- PROBLEM: Find employees with consecutive years
-- who worked 150+ hours in at least one year
-- ============================================

-- ❌ BAD APPROACH: Jump straight to the final query
-- You'll spend hours debugging because you can't see what's wrong!

-- ✅ GOOD APPROACH: Use scaffolding to build and verify step-by-step


-- ============================================
-- STEP 1: SCAFFOLDING - Add ALL verification columns
-- ============================================
-- Include EVERYTHING you need to verify the logic

WITH employee_years AS (
    SELECT 
        employee_id,
        employee_name,
        year,
        hours_worked,
        -- SCAFFOLDING: Add previous year to verify LAG works
        LAG(year) OVER (PARTITION BY employee_id ORDER BY year) AS prev_year,
        -- SCAFFOLDING: Calculate the gap to verify consecutive logic
        year - LAG(year) OVER (PARTITION BY employee_id ORDER BY year) AS year_gap,
        -- SCAFFOLDING: Add previous hours to verify the condition
        LAG(hours_worked) OVER (PARTITION BY employee_id ORDER BY year) AS prev_hours
    FROM 
        employee_performance
)
SELECT 
    employee_name,
    year,
    hours_worked,
    prev_year,        -- ← SCAFFOLDING: Verify LAG pulled correct year
    year_gap,         -- ← SCAFFOLDING: Verify gap = 1 for consecutive
    prev_hours,       -- ← SCAFFOLDING: Verify hours comparison
    -- SCAFFOLDING: Show which condition passed
    CASE 
        WHEN year_gap = 1 THEN 'Consecutive ✓' 
        ELSE 'Not Consecutive ✗' 
    END AS consecutive_check,
    CASE 
        WHEN hours_worked >= 150 OR prev_hours >= 150 THEN '150+ Hours ✓'
        ELSE 'Under 150 ✗'
    END AS hours_check
FROM 
    employee_years
ORDER BY 
    employee_name, year;

-- Run this first! Verify:
-- ✓ Does LAG pull the correct previous year?
-- ✓ Is year_gap = 1 for consecutive years?
-- ✓ Are the hours comparisons correct?


-- ============================================
-- STEP 2: VERIFY THE LOGIC
-- ============================================
-- Look at the scaffolding output:

-- employee_name   | year | hours | prev_year | year_gap | prev_hours | consecutive | hours_check
-- ----------------|------|-------|-----------|----------|------------|-------------|-------------
-- Alice Johnson   | 2022 | 160   | NULL      | NULL     | NULL       | Not Consec  | 150+ Hours ✓
-- Alice Johnson   | 2023 | 180   | 2022      | 1        | 160        | Consecutive ✓| 150+ Hours ✓
-- Alice Johnson   | 2024 | 170   | 2023      | 1        | 180        | Consecutive ✓| 150+ Hours ✓
-- Bob Smith       | 2022 | 120   | NULL      | NULL     | NULL       | Not Consec  | Under 150 ✗
-- Bob Smith       | 2024 | 140   | 2022      | 2        | 120        | Not Consec ✗| Under 150 ✗
-- Charlie Brown   | 2023 | 200   | NULL      | NULL     | NULL       | Not Consec  | 150+ Hours ✓
-- Charlie Brown   | 2024 | 210   | 2023      | 1        | 200        | Consecutive ✓| 150+ Hours ✓

-- ✓ Alice: 2023 row shows consecutive (gap=1) and 150+ hours → Should qualify
-- ✓ Bob: 2024 row shows gap=2 (not consecutive) → Should NOT qualify
-- ✓ Charlie: 2024 row shows consecutive and 150+ hours → Should qualify


-- ============================================
-- STEP 3: DE-SCAFFOLDING - Remove verification columns
-- ============================================
-- Now that we've verified the logic works, clean it up!

WITH employee_years AS (
    SELECT 
        employee_id,
        employee_name,
        year,
        hours_worked,
        LAG(year) OVER (PARTITION BY employee_id ORDER BY year) AS prev_year,
        LAG(hours_worked) OVER (PARTITION BY employee_id ORDER BY year) AS prev_hours
    FROM 
        employee_performance
)
SELECT DISTINCT
    employee_name
FROM 
    employee_years
WHERE 
    year - prev_year = 1  -- Consecutive years
    AND
    (hours_worked >= 150 OR prev_hours >= 150)  -- 150+ hours in at least one year
ORDER BY 
    employee_name;

-- Expected Output (Clean!):
-- employee_name
-- ---------------
-- Alice Johnson
-- Charlie Brown


-- ============================================
-- SCAFFOLDING BEST PRACTICES
-- ============================================

-- ✅ DO: Add scaffolding columns during development
-- - LAG/LEAD results
-- - Calculated differences
-- - Boolean checks (CASE WHEN ... THEN 'Pass' ELSE 'Fail')
-- - Row numbers, ranks
-- - Intermediate calculations

-- ✅ DO: Run queries with scaffolding first
-- - Verify each piece of logic works
-- - Check edge cases (NULL values, gaps, etc.)
-- - Ensure filters are correct

-- ✅ DO: Remove scaffolding for final query
-- - Keep only required output columns
-- - Add comments explaining complex logic
-- - Test the final query produces same results

-- ❌ DON'T: Skip scaffolding for complex queries
-- - You'll waste time debugging
-- - You won't understand why it's wrong
-- - You might miss edge cases


-- ============================================
-- EXAMPLE 2: Scaffolding with Aggregations
-- ============================================

-- Problem: Find departments with average revenue > $60,000

-- STEP 1: WITH SCAFFOLDING
SELECT 
    department,
    COUNT(*) AS employee_count,           -- ← SCAFFOLDING: Verify count
    SUM(revenue_generated) AS total_rev,  -- ← SCAFFOLDING: Verify sum
    AVG(revenue_generated) AS avg_rev,    -- ← SCAFFOLDING: Verify average
    CASE 
        WHEN AVG(revenue_generated) > 60000 THEN 'Qualifies ✓'
        ELSE 'Does Not Qualify ✗'
    END AS qualification_check            -- ← SCAFFOLDING: Verify filter
FROM 
    employee_performance
GROUP BY 
    department
ORDER BY 
    avg_rev DESC;

-- Verify the calculations look correct!

-- STEP 2: DE-SCAFFOLDED (Final)
SELECT 
    department
FROM 
    employee_performance
GROUP BY 
    department
HAVING 
    AVG(revenue_generated) > 60000
ORDER BY 
    department;


-- ============================================
-- EXAMPLE 3: Scaffolding with Window Functions
-- ============================================

-- Problem: Find top 2 performers per department by revenue

-- STEP 1: WITH SCAFFOLDING
SELECT 
    employee_name,
    department,
    revenue_generated,
    RANK() OVER (PARTITION BY department ORDER BY revenue_generated DESC) AS rank_num,  -- ← SCAFFOLDING
    CASE 
        WHEN RANK() OVER (PARTITION BY department ORDER BY revenue_generated DESC) <= 2 
        THEN 'Top 2 ✓' 
        ELSE 'Not Top 2 ✗' 
    END AS rank_check  -- ← SCAFFOLDING
FROM 
    employee_performance
ORDER BY 
    department, rank_num;

-- Verify the ranking is correct!

-- STEP 2: DE-SCAFFOLDED (Final)
WITH ranked_employees AS (
    SELECT 
        employee_name,
        department,
        revenue_generated,
        RANK() OVER (PARTITION BY department ORDER BY revenue_generated DESC) AS rank_num
    FROM 
        employee_performance
)
SELECT 
    employee_name,
    department,
    revenue_generated
FROM 
    ranked_employees
WHERE 
    rank_num <= 2
ORDER BY 
    department, revenue_generated DESC;


-- ============================================
-- THE SCAFFOLDING WORKFLOW
-- ============================================

/*
1. BUILD (Scaffolding Phase)
   ├─ Add ALL verification columns
   ├─ Add CASE statements to show pass/fail
   ├─ Include intermediate calculations
   └─ Run and review the output

2. VERIFY (Testing Phase)
   ├─ Check each scaffolding column
   ├─ Verify edge cases (NULLs, gaps, etc.)
   ├─ Confirm filters work correctly
   └─ Test with different data

3. CLEAN (De-Scaffolding Phase)
   ├─ Remove verification columns
   ├─ Keep only required output
   ├─ Add comments for complex logic
   └─ Final test to ensure same results
*/


-- ============================================
-- KEY TAKEAWAYS
-- ============================================
-- 1. Scaffolding = Professional SQL development
-- 2. Always verify complex logic before finalizing
-- 3. Temporary columns are your debugging tools
-- 4. Clean queries = Remove scaffolding for final output
-- 5. This approach saves time and prevents errors
