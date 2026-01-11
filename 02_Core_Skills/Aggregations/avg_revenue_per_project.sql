-- ============================================
-- AVERAGE REVENUE PER PROJECT
-- ============================================
-- Goal: Calculate the average revenue generated per project in January 2023

-- ============================================
-- TERMINOLOGY (IMPORTANT!)
-- ============================================
-- "Average revenue PER PROJECT" means:
-- Total Revenue ÷ Total Projects = Revenue per Project

-- Example:
-- If 3 employees completed projects in January:
--   Employee A: 5 projects, $10,000 revenue
--   Employee B: 3 projects, $6,000 revenue
--   Employee C: 2 projects, $4,000 revenue
--
-- Total Projects: 5 + 3 + 2 = 10
-- Total Revenue: $10,000 + $6,000 + $4,000 = $20,000
-- Average Revenue PER PROJECT: $20,000 ÷ 10 = $2,000

-- This is NOT:
-- ❌ Average revenue per employee ($20,000 ÷ 3 = $6,667)
-- ❌ Total revenue ($20,000)
-- ✅ Average revenue per project ($20,000 ÷ 10 = $2,000)

-- ============================================
-- SETUP: Create table and sample data
-- ============================================
DROP TABLE IF EXISTS employee_performance_fact CASCADE;

CREATE TABLE employee_performance_fact (
    employee_id INT,
    month VARCHAR(20),
    year INT,
    projects_completed INT,
    hours_worked INT,
    revenue_generated INT
);

INSERT INTO employee_performance_fact VALUES
-- January 2023
(1, 'January', 2023, 5, 160, 10000),
(2, 'January', 2023, 3, 120, 6000),
(3, 'January', 2023, 2, 80, 4000),
-- February 2023 (for context)
(1, 'February', 2023, 4, 150, 8000),
(2, 'February', 2023, 6, 180, 12000),
-- January 2022 (different year)
(1, 'January', 2022, 3, 100, 5000);

-- Verify the data
SELECT * FROM employee_performance_fact ORDER BY year, month, employee_id;


-- ============================================
-- STEP 1: View January 2023 Data
-- ============================================
-- First, let's see what we're working with

SELECT 
    employee_id,
    projects_completed,
    revenue_generated
FROM 
    employee_performance_fact
WHERE 
    month = 'January' AND year = 2023;

-- Result:
-- employee_id | projects_completed | revenue_generated
-- ------------|--------------------|-----------------
-- 1           | 5                  | 10000
-- 2           | 3                  | 6000
-- 3           | 2                  | 4000


-- ============================================
-- STEP 2: Calculate Totals
-- ============================================
-- Sum up projects and revenue

SELECT 
    SUM(projects_completed) AS total_projects,
    SUM(revenue_generated) AS total_revenue
FROM 
    employee_performance_fact
WHERE 
    month = 'January' AND year = 2023;

-- Result:
-- total_projects | total_revenue
-- ---------------|-------------
-- 10             | 20000


-- ============================================
-- SOLUTION 1: Direct Division (Simplest)
-- ============================================

SELECT 
    SUM(revenue_generated) / SUM(projects_completed) AS avg_revenue_per_project
FROM 
    employee_performance_fact
WHERE 
    month = 'January' AND year = 2023;

-- Expected Output:
-- avg_revenue_per_project
-- -----------------------
-- 2000


-- ============================================
-- SOLUTION 2: Using CAST for Decimal Precision
-- ============================================
-- If you want decimal places (e.g., $2,000.50)

SELECT 
    ROUND(
        SUM(revenue_generated)::DECIMAL / SUM(projects_completed),
        2
    ) AS avg_revenue_per_project
FROM 
    employee_performance_fact
WHERE 
    month = 'January' AND year = 2023;


-- ============================================
-- SOLUTION 3: Showing the Breakdown
-- ============================================
-- Show both totals and the average

SELECT 
    SUM(projects_completed) AS total_projects,
    SUM(revenue_generated) AS total_revenue,
    SUM(revenue_generated) / SUM(projects_completed) AS avg_revenue_per_project
FROM 
    employee_performance_fact
WHERE 
    month = 'January' AND year = 2023;

-- Result:
-- total_projects | total_revenue | avg_revenue_per_project
-- ---------------|---------------|------------------------
-- 10             | 20000         | 2000


-- ============================================
-- SOLUTION 4: With Column Alias (Exact Format)
-- ============================================
-- If the problem wants a specific column name

SELECT 
    SUM(revenue_generated) / SUM(projects_completed) AS AvgRevenuePerProject
FROM 
    employee_performance_fact
WHERE 
    month = 'January' AND year = 2023;

-- Expected Output:
-- AvgRevenuePerProject
-- --------------------
-- 2000


-- ============================================
-- COMMON MISTAKES TO AVOID
-- ============================================

-- ❌ WRONG: Average of revenue (ignores project count)
SELECT AVG(revenue_generated) 
FROM employee_performance_fact 
WHERE month = 'January' AND year = 2023;
-- This gives: (10000 + 6000 + 4000) / 3 = 6667 (average per EMPLOYEE, not per PROJECT!)

-- ❌ WRONG: Dividing averages
SELECT AVG(revenue_generated) / AVG(projects_completed)
FROM employee_performance_fact 
WHERE month = 'January' AND year = 2023;
-- This gives: 6667 / 3.33 = 2000 (happens to be right here, but wrong approach!)

-- ✅ CORRECT: Sum of revenue divided by sum of projects
SELECT SUM(revenue_generated) / SUM(projects_completed)
FROM employee_performance_fact 
WHERE month = 'January' AND year = 2023;
-- This gives: 20000 / 10 = 2000 (correct!)


-- ============================================
-- WHY SUM/SUM IS CORRECT
-- ============================================
-- Think of it this way:
-- 
-- You want to know: "On average, how much revenue did each project generate?"
-- 
-- Total revenue from ALL projects: $20,000
-- Total number of projects: 10
-- Revenue per project: $20,000 ÷ 10 = $2,000
--
-- You're NOT asking: "What's the average revenue per employee?"
-- That would be: AVG(revenue_generated) = $6,667


-- ============================================
-- PRACTICE VARIATIONS
-- ============================================

-- Practice 1: Calculate average hours worked per project in January 2023
-- Hint: SUM(hours_worked) / SUM(projects_completed)

-- Practice 2: Calculate average revenue per project for ALL of 2023
-- Hint: Remove the month filter, keep only year = 2023

-- Practice 3: Compare average revenue per project for Jan 2022 vs Jan 2023
-- Hint: Use CASE or separate queries

-- Practice 4: Find which month in 2023 had the highest avg revenue per project
-- Hint: GROUP BY month, then use ORDER BY ... DESC LIMIT 1


-- ============================================
-- KEY CONCEPTS
-- ============================================
-- 1. "Per Project" = Divide by total projects, not by number of employees
-- 2. Use SUM/SUM, not AVG
-- 3. Filter correctly: month = 'January' AND year = 2023
-- 4. CAST to DECIMAL if you need precision
