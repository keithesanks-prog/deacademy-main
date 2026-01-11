-- =====================================================
-- SQL PATTERN RECOGNITION PRACTICE - DATABASE SETUP
-- =====================================================
-- Copy this entire file into an online SQL editor like:
-- - https://www.db-fiddle.com/ (PostgreSQL recommended)
-- - https://sqliteonline.com/
-- - http://sqlfiddle.com/
-- =====================================================

-- Drop table if it exists (for re-running)
DROP TABLE IF EXISTS employees_prc;

-- Create the employees table
CREATE TABLE employees_prc (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10, 2),
    hire_date DATE,
    performance_rating DECIMAL(3, 2)
);

-- Insert sample data (30 employees across 4 departments)
INSERT INTO employees_prc (employee_id, employee_name, department, salary, hire_date, performance_rating) VALUES
-- Engineering Department (10 employees)
(1, 'Alice Johnson', 'Engineering', 120000, '2020-01-15', 4.5),
(2, 'Bob Smith', 'Engineering', 115000, '2020-03-22', 4.2),
(3, 'Carol White', 'Engineering', 95000, '2021-06-10', 3.8),
(4, 'David Brown', 'Engineering', 105000, '2021-08-05', 4.0),
(5, 'Eve Davis', 'Engineering', 98000, '2022-01-20', 3.9),
(6, 'Frank Miller', 'Engineering', 110000, '2022-04-12', 4.3),
(7, 'Grace Wilson', 'Engineering', 92000, '2023-02-28', 3.7),
(8, 'Henry Moore', 'Engineering', 88000, '2023-05-15', 3.5),
(9, 'Ivy Taylor', 'Engineering', 125000, '2019-11-08', 4.7),
(10, 'Jack Anderson', 'Engineering', 102000, '2022-09-30', 4.1),

-- Sales Department (8 employees)
(11, 'Karen Thomas', 'Sales', 95000, '2020-02-10', 4.4),
(12, 'Leo Jackson', 'Sales', 88000, '2020-07-18', 4.0),
(13, 'Mia White', 'Sales', 78000, '2021-03-25', 3.6),
(14, 'Noah Harris', 'Sales', 92000, '2021-09-14', 4.2),
(15, 'Olivia Martin', 'Sales', 85000, '2022-01-05', 3.9),
(16, 'Paul Thompson', 'Sales', 90000, '2022-06-20', 4.1),
(17, 'Quinn Garcia', 'Sales', 82000, '2023-03-10', 3.8),
(18, 'Rachel Martinez', 'Sales', 96000, '2019-12-01', 4.5),

-- HR Department (7 employees)
(19, 'Sam Robinson', 'HR', 75000, '2020-04-15', 3.9),
(20, 'Tina Clark', 'HR', 72000, '2020-08-22', 3.7),
(21, 'Uma Rodriguez', 'HR', 68000, '2021-05-30', 3.5),
(22, 'Victor Lewis', 'HR', 85000, '2021-11-12', 4.2),
(23, 'Wendy Lee', 'HR', 70000, '2022-02-28', 3.6),
(24, 'Xavier Walker', 'HR', 78000, '2022-07-15', 4.0),
(25, 'Yara Hall', 'HR', 73000, '2023-01-20', 3.8),

-- Marketing Department (5 employees)
(26, 'Zoe Allen', 'Marketing', 82000, '2020-05-10', 4.1),
(27, 'Adam Young', 'Marketing', 88000, '2021-02-14', 4.3),
(28, 'Bella King', 'Marketing', 79000, '2021-10-05', 3.9),
(29, 'Chris Wright', 'Marketing', 91000, '2022-03-18', 4.4),
(30, 'Diana Scott', 'Marketing', 85000, '2023-04-22', 4.0);

-- Verify data loaded correctly
SELECT 'Data loaded successfully!' as status, COUNT(*) as total_employees FROM employees_prc;

-- Show department breakdown
SELECT 
    department,
    COUNT(*) as employee_count,
    MIN(salary) as min_salary,
    MAX(salary) as max_salary,
    ROUND(AVG(salary), 2) as avg_salary
FROM employees_prc
GROUP BY department
ORDER BY department;

-- =====================================================
-- NOW YOU'RE READY TO PRACTICE!
-- =====================================================
-- Use the problems from pattern_practice_problems.md
-- and write your queries below this line.
-- =====================================================

-- Example: Problem 1 - Find the total number of employees in each department
-- YOUR SOLUTION HERE:



-- Example: Problem 2 - Find the employee with the highest salary in each department
-- YOUR SOLUTION HERE:



-- Continue with more problems...
