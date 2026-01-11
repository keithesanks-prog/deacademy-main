-- ============================================
-- AND/OR LOGIC & PARENTHESES IN WHERE CLAUSES
-- ============================================
-- Understanding operator precedence and grouping conditions

-- ============================================
-- THE PROBLEM: OR Without Parentheses
-- ============================================
-- Without parentheses, OR can cause unexpected results!

-- ============================================
-- SETUP: Sample Data
-- ============================================
DROP TABLE IF EXISTS qualificationandskills CASCADE;
DROP TABLE IF EXISTS employee_dimension CASCADE;

CREATE TABLE employee_dimension (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    role VARCHAR(50),
    department VARCHAR(50)
);

CREATE TABLE qualificationandskills (
    skill_id INT PRIMARY KEY,
    employee_id INT,
    technical_skills VARCHAR(200),
    FOREIGN KEY (employee_id) REFERENCES employee_dimension(employee_id)
);

INSERT INTO employee_dimension VALUES
(1, 'Alice Johnson', 'Data Analyst', 'Analytics'),
(2, 'Bob Smith', 'Data Analyst', 'Analytics'),
(3, 'Charlie Brown', 'Software Engineer', 'Engineering'),
(4, 'Diana Prince', 'Data Analyst', 'Analytics'),
(5, 'Eve Wilson', 'Project Manager', 'Operations');

INSERT INTO qualificationandskills VALUES
(1, 1, 'SQL, Python, Tableau'),
(2, 2, 'Excel, PowerBI'),
(3, 3, 'Python, Java, C++'),
(4, 4, 'SQL, R'),
(5, 5, 'Excel, Project Management');

SELECT * FROM employee_dimension ORDER BY employee_id;
SELECT * FROM qualificationandskills ORDER BY employee_id;


-- ============================================
-- EXAMPLE 1: WITHOUT Parentheses (WRONG!)
-- ============================================
-- Goal: Find Data Analysts who know SQL OR Python

-- ❌ WRONG: OR without parentheses
SELECT
    e.employee_id,
    e.employee_name,
    e.role,
    q.technical_skills
FROM employee_dimension e
JOIN qualificationandskills q ON q.employee_id = e.employee_id
WHERE e.role = 'Data Analyst'
    AND q.technical_skills LIKE '%SQL%'
    OR q.technical_skills LIKE '%Python%';  -- ← DANGER!

-- UNEXPECTED RESULT:
-- employee_id | employee_name  | role              | technical_skills
-- ------------|----------------|-------------------|------------------
-- 1           | Alice Johnson  | Data Analyst      | SQL, Python, Tableau  ✓ Correct
-- 3           | Charlie Brown  | Software Engineer | Python, Java, C++     ✗ WRONG ROLE!
-- 4           | Diana Prince   | Data Analyst      | SQL, R                ✓ Correct

-- Charlie is included even though he's NOT a Data Analyst!


-- ============================================
-- WHY IT'S WRONG: Operator Precedence
-- ============================================
-- SQL evaluates the query like this:
-- (e.role = 'Data Analyst' AND q.technical_skills LIKE '%SQL%')
-- OR
-- (q.technical_skills LIKE '%Python%')

-- Translation:
-- "Give me employees who are:
--   (Data Analysts with SQL) OR (Anyone with Python)"

-- That's why Charlie (Software Engineer with Python) appears!


-- ============================================
-- EXAMPLE 2: WITH Parentheses (CORRECT!)
-- ============================================

-- ✅ CORRECT: Use parentheses to group OR conditions
SELECT
    e.employee_id,
    e.employee_name,
    e.role,
    q.technical_skills
FROM employee_dimension e
JOIN qualificationandskills q ON q.employee_id = e.employee_id
WHERE e.role = 'Data Analyst'
    AND (
        q.technical_skills LIKE '%SQL%'      -- Check for SQL
        OR q.technical_skills LIKE '%Python%' -- Check for Python
    );

-- CORRECT RESULT:
-- employee_id | employee_name  | role         | technical_skills
-- ------------|----------------|--------------|------------------
-- 1           | Alice Johnson  | Data Analyst | SQL, Python, Tableau  ✓
-- 4           | Diana Prince   | Data Analyst | SQL, R                ✓

-- Charlie is excluded because he's not a Data Analyst!


-- ============================================
-- HOW PARENTHESES CHANGE THE LOGIC
-- ============================================

-- WITH parentheses:
-- e.role = 'Data Analyst' AND (skill LIKE '%SQL%' OR skill LIKE '%Python%')
-- Translation: "Data Analysts who know SQL OR Python"

-- WITHOUT parentheses:
-- e.role = 'Data Analyst' AND skill LIKE '%SQL%' OR skill LIKE '%Python%'
-- Translation: "(Data Analysts with SQL) OR (Anyone with Python)"


-- ============================================
-- VISUAL BREAKDOWN
-- ============================================

-- WITHOUT Parentheses:
-- ┌─────────────────────────────────────┐
-- │ Condition 1: Data Analyst + SQL     │ ← Alice, Diana
-- └─────────────────────────────────────┘
--              OR
-- ┌─────────────────────────────────────┐
-- │ Condition 2: Anyone with Python     │ ← Alice, Charlie
-- └─────────────────────────────────────┘
-- Result: Alice, Diana, Charlie (WRONG!)

-- WITH Parentheses:
-- ┌─────────────────────────────────────────────────────┐
-- │ Data Analyst AND (SQL OR Python)                    │
-- │   ├─ Alice: Data Analyst + SQL ✓                    │
-- │   ├─ Alice: Data Analyst + Python ✓                 │
-- │   ├─ Diana: Data Analyst + SQL ✓                    │
-- │   └─ Charlie: Software Engineer + Python ✗          │
-- └─────────────────────────────────────────────────────┘
-- Result: Alice, Diana (CORRECT!)


-- ============================================
-- EXAMPLE 3: Multiple AND/OR Conditions
-- ============================================

-- Find Data Analysts OR Software Engineers who know SQL OR Python

-- ❌ WRONG: Without proper grouping
SELECT e.employee_name, e.role, q.technical_skills
FROM employee_dimension e
JOIN qualificationandskills q ON q.employee_id = e.employee_id
WHERE e.role = 'Data Analyst'
    OR e.role = 'Software Engineer'
    AND q.technical_skills LIKE '%SQL%'
    OR q.technical_skills LIKE '%Python%';
-- This evaluates as:
-- (Data Analyst) OR (Software Engineer AND SQL) OR (Anyone with Python)

-- ✅ CORRECT: With proper grouping
SELECT e.employee_name, e.role, q.technical_skills
FROM employee_dimension e
JOIN qualificationandskills q ON q.employee_id = e.employee_id
WHERE (e.role = 'Data Analyst' OR e.role = 'Software Engineer')
    AND (q.technical_skills LIKE '%SQL%' OR q.technical_skills LIKE '%Python%');
-- This evaluates as:
-- (Data Analyst OR Software Engineer) AND (SQL OR Python)


-- ============================================
-- SCAFFOLDING: Verify Your Logic
-- ============================================
-- Use CASE statements to see which conditions match!

SELECT
    e.employee_id,
    e.employee_name,
    e.role,
    q.technical_skills,
    -- SCAFFOLDING: Show which conditions pass
    CASE WHEN e.role = 'Data Analyst' THEN '✓ Data Analyst' ELSE '✗ Not DA' END AS role_check,
    CASE WHEN q.technical_skills LIKE '%SQL%' THEN '✓ Has SQL' ELSE '✗ No SQL' END AS sql_check,
    CASE WHEN q.technical_skills LIKE '%Python%' THEN '✓ Has Python' ELSE '✗ No Python' END AS python_check,
    -- SCAFFOLDING: Final qualification
    CASE 
        WHEN e.role = 'Data Analyst' 
            AND (q.technical_skills LIKE '%SQL%' OR q.technical_skills LIKE '%Python%')
        THEN '✓ QUALIFIES'
        ELSE '✗ Does Not Qualify'
    END AS final_result
FROM employee_dimension e
JOIN qualificationandskills q ON q.employee_id = e.employee_id
ORDER BY e.employee_id;

-- This shows you EXACTLY why each row does or doesn't qualify!


-- ============================================
-- OPERATOR PRECEDENCE RULES
-- ============================================

-- SQL evaluates conditions in this order:
-- 1. Parentheses ( )
-- 2. NOT
-- 3. AND
-- 4. OR

-- Example:
-- A OR B AND C
-- Evaluates as: A OR (B AND C)
-- NOT as: (A OR B) AND C

-- Always use parentheses to make your intent clear!


-- ============================================
-- COMMON PATTERNS
-- ============================================

-- Pattern 1: One required condition + multiple optional conditions
WHERE required_condition = TRUE
    AND (optional1 = TRUE OR optional2 = TRUE OR optional3 = TRUE)

-- Pattern 2: Multiple required conditions + one optional condition
WHERE required1 = TRUE
    AND required2 = TRUE
    AND (optional1 = TRUE OR optional2 = TRUE)

-- Pattern 3: Multiple groups of OR conditions
WHERE (condition1 = TRUE OR condition2 = TRUE)
    AND (condition3 = TRUE OR condition4 = TRUE)


-- ============================================
-- PRACTICE EXERCISES
-- ============================================

-- Practice 1: Find employees who are:
-- - Data Analysts OR Software Engineers
-- - AND know SQL
-- Hint: Group the role conditions with parentheses

-- Practice 2: Find employees who are:
-- - Data Analysts with (SQL OR Python)
-- - OR Software Engineers with Python
-- Hint: You'll need two sets of parentheses

-- Practice 3: Rewrite this query with proper parentheses:
-- WHERE role = 'Manager' OR role = 'Director' AND salary > 100000
-- What does it currently mean? What should it mean?


-- ============================================
-- KEY TAKEAWAYS
-- ============================================
-- 1. AND has higher precedence than OR
-- 2. Always use parentheses to group OR conditions
-- 3. Without parentheses, OR can "leak" and include unwanted rows
-- 4. Use scaffolding to verify your logic
-- 5. When in doubt, add parentheses for clarity!
