# SQL Pattern Recognition Practice Problems
## 30 Problems to Build Your Pattern Recognition Skills

---

## 📖 How to Use This Practice Set

1. **Read each problem carefully**
2. **Before looking at the solution, identify:**
   - What pattern type is this?
   - What SQL approach should I use?
   - What are the key trigger words?
3. **Write your solution**
4. **Check the answer**
5. **Track your accuracy** (see tracker file)

---

## 🎯 Level 1: Basic Pattern Recognition (Problems 1-10)

### **Problem 1**
Find the total number of employees in each department.

<details>
<summary>💡 Hint</summary>
Do you need to see individual employee rows, or just a count per department?
</details>

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Simple aggregation per group

**Approach:** GROUP BY

```sql
SELECT 
    department,
    COUNT(*) as employee_count
FROM employees_prc
GROUP BY department;
```

**Key Recognition:**
- "total number" = COUNT aggregate
- "in each department" = GROUP BY
- No individual row details needed
</details>

---

### **Problem 2**
Find the employee with the highest salary in each department.

<details>
<summary>💡 Hint</summary>
Do you need just the salary amount, or the actual employee details?
</details>

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Top 1 per group with row details

**Approach:** Window function (ROW_NUMBER)

```sql
SELECT employee_name, department, salary
FROM (
    SELECT 
        employee_name,
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM employees_prc
) ranked
WHERE rn = 1;
```

**Key Recognition:**
- "employee with highest" = need row details, not just MAX
- "in each department" = PARTITION BY department
- "highest salary" = ORDER BY salary DESC
</details>

---

### **Problem 3**
Calculate the average salary across all employees.

<details>
<summary>💡 Hint</summary>
Is there any grouping involved?
</details>

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Simple aggregate (no grouping)

**Approach:** Simple SELECT with aggregate

```sql
SELECT AVG(salary) as average_salary
FROM employees_prc;
```

**Key Recognition:**
- "across all employees" = no grouping
- Just need one number
- Simple aggregate function
</details>

---

### **Problem 4**
Show each employee's salary and the overall company average salary.

<details>
<summary>💡 Hint</summary>
Do you need individual rows AND an aggregate value on each row?
</details>

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Individual rows with overall aggregate

**Approach:** Window function (no PARTITION BY)

```sql
SELECT 
    employee_name,
    department,
    salary,
    AVG(salary) OVER () as company_avg
FROM employees_prc;
```

**Alternative (using subquery):**
```sql
SELECT 
    employee_name,
    department,
    salary,
    (SELECT AVG(salary) FROM employees_prc) as company_avg
FROM employees_prc;
```

**Key Recognition:**
- "each employee" = need individual rows
- "overall company average" = aggregate across all rows
- Window function with empty OVER() or scalar subquery
</details>

---

### **Problem 5**
Find all employees who earn more than $75,000.

<details>
<summary>💡 Hint</summary>
Is this a filtering problem or an aggregation problem?
</details>

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Simple filtering

**Approach:** WHERE clause

```sql
SELECT *
FROM employees_prc
WHERE salary > 75000;
```

**Key Recognition:**
- "employees who earn more than" = filtering condition
- No grouping or ranking needed
- Simple WHERE clause
</details>

---

### **Problem 6**
List the top 5 highest-paid employees across the entire company.

<details>
<summary>💡 Hint</summary>
Is there a "per group" or "in each" phrase? Or is it across the whole dataset?
</details>

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Top N across entire dataset

**Approach:** Window function (no PARTITION BY) or ORDER BY with LIMIT

```sql
-- Window function approach:
SELECT employee_name, department, salary
FROM (
    SELECT 
        employee_name,
        department,
        salary,
        ROW_NUMBER() OVER (ORDER BY salary DESC) as rn
    FROM employees_prc
) ranked
WHERE rn <= 5;
```

```sql
-- Simpler approach (if your SQL supports LIMIT):
SELECT employee_name, department, salary
FROM employees_prc
ORDER BY salary DESC
LIMIT 5;
```

**Key Recognition:**
- "top 5" = ranking needed
- "across entire company" = no PARTITION BY
- Need employee details = can't just use MAX
</details>

---

### **Problem 7**
Find the minimum and maximum salary in each department.

<details>
<summary>💡 Hint</summary>
Do you need individual employee rows or just the min/max values?
</details>

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Multiple aggregates per group

**Approach:** GROUP BY

```sql
SELECT 
    department,
    MIN(salary) as min_salary,
    MAX(salary) as max_salary
FROM employees_prc
GROUP BY department;
```

**Key Recognition:**
- "minimum and maximum" = aggregate functions
- "in each department" = GROUP BY
- No individual row details needed
</details>

---

### **Problem 8**
Show each employee and indicate whether their salary is above or below their department's average.

<details>
<summary>💡 Hint</summary>
Do you need to see each employee AND compare them to a group aggregate?
</details>

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Row-level comparison to group aggregate

**Approach:** Window function

```sql
SELECT 
    employee_name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    CASE 
        WHEN salary > AVG(salary) OVER (PARTITION BY department) 
        THEN 'Above Average'
        ELSE 'Below Average'
    END as salary_category
FROM employees_prc;
```

**Key Recognition:**
- "each employee" = need individual rows
- "their department's average" = group aggregate
- Need both on same row = window function
</details>

---

### **Problem 9**
Count how many departments have more than 10 employees.

<details>
<summary>💡 Hint</summary>
This is a two-step problem: first group, then filter groups.
</details>

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Filtering groups based on aggregate

**Approach:** GROUP BY with HAVING, then count

```sql
SELECT COUNT(*) as dept_count
FROM (
    SELECT department
    FROM employees_prc
    GROUP BY department
    HAVING COUNT(*) > 10
) departments_with_many_employees;
```

**Alternative (simpler):**
```sql
SELECT COUNT(DISTINCT department) as dept_count
FROM employees_prc
GROUP BY department
HAVING COUNT(*) > 10;
```

**Key Recognition:**
- "departments have more than 10" = filter groups with HAVING
- "count how many" = COUNT of filtered results
</details>

---

### **Problem 10**
Find the second-highest salary in the company.

<details>
<summary>💡 Hint</summary>
Is this across the whole company or per department?
</details>

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Nth highest value (no grouping)

**Approach:** Window function or subquery with OFFSET

```sql
-- Window function approach:
SELECT DISTINCT salary
FROM (
    SELECT 
        salary,
        DENSE_RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees_prc
) ranked
WHERE rank = 2;
```

```sql
-- Alternative (using LIMIT/OFFSET):
SELECT salary
FROM employees_prc
ORDER BY salary DESC
LIMIT 1 OFFSET 1;
```

**Key Recognition:**
- "second-highest" = ranking needed
- "in the company" = no grouping
- Use DENSE_RANK to handle ties properly
</details>

---

## 🎯 Level 2: Intermediate Patterns (Problems 11-20)

### **Problem 11**
For each department, show the salary difference between the highest and lowest paid employees.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Aggregate calculation per group

**Approach:** GROUP BY

```sql
SELECT 
    department,
    MAX(salary) - MIN(salary) as salary_range
FROM employees_prc
GROUP BY department;
```

**Key Recognition:**
- "for each department" = GROUP BY
- "difference between highest and lowest" = MAX - MIN
- No individual row details needed
</details>

---

### **Problem 12**
Rank all employees by salary within their department, showing ties with the same rank.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Ranking with ties

**Approach:** Window function (RANK or DENSE_RANK)

```sql
SELECT 
    employee_name,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank
FROM employees_prc;
```

**Key Recognition:**
- "rank employees" = RANK function
- "within their department" = PARTITION BY department
- "showing ties" = use RANK (not ROW_NUMBER)
</details>

---

### **Problem 13**
Find all employees whose salary is above the company-wide average.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Filtering based on overall aggregate

**Approach:** Subquery in WHERE or window function

```sql
-- Subquery approach:
SELECT *
FROM employees_prc
WHERE salary > (SELECT AVG(salary) FROM employees_prc);
```

```sql
-- Window function approach:
SELECT employee_name, department, salary
FROM (
    SELECT 
        employee_name,
        department,
        salary,
        AVG(salary) OVER () as company_avg
    FROM employees_prc
) with_avg
WHERE salary > company_avg;
```

**Key Recognition:**
- "above the company-wide average" = compare to overall aggregate
- Need to filter rows = WHERE clause with subquery
</details>

---

### **Problem 14**
Show each employee's hire date and the hire date of the next employee hired in their department.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Sequential comparison (next row)

**Approach:** Window function (LEAD)

```sql
SELECT 
    employee_name,
    department,
    hire_date,
    LEAD(hire_date) OVER (PARTITION BY department ORDER BY hire_date) as next_hire_date
FROM employees_prc;
```

**Key Recognition:**
- "next employee hired" = LEAD function
- "in their department" = PARTITION BY department
- Sequential/temporal comparison
</details>

---

### **Problem 15**
Calculate the running total of salaries when employees are ordered by hire date.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Cumulative calculation

**Approach:** Window function (SUM with ORDER BY)

```sql
SELECT 
    employee_name,
    hire_date,
    salary,
    SUM(salary) OVER (ORDER BY hire_date) as running_total
FROM employees_prc
ORDER BY hire_date;
```

**Key Recognition:**
- "running total" = cumulative sum
- "ordered by hire date" = ORDER BY in window function
- No PARTITION BY = running total across all rows
</details>

---

### **Problem 16**
Find departments where the average salary exceeds $90,000.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Filtering groups based on aggregate

**Approach:** GROUP BY with HAVING

```sql
SELECT 
    department,
    AVG(salary) as avg_salary
FROM employees_prc
GROUP BY department
HAVING AVG(salary) > 90000;
```

**Key Recognition:**
- "departments where" = filtering groups
- "average salary exceeds" = HAVING clause
- GROUP BY with aggregate filter
</details>

---

### **Problem 17**
For each employee, show their salary percentile within their department.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Percentile calculation within groups

**Approach:** Window function (PERCENT_RANK)

```sql
SELECT 
    employee_name,
    department,
    salary,
    PERCENT_RANK() OVER (PARTITION BY department ORDER BY salary) as salary_percentile
FROM employees_prc;
```

**Key Recognition:**
- "percentile within their department" = PARTITION BY department
- "percentile" = PERCENT_RANK or CUME_DIST function
- Need individual rows with ranking
</details>

---

### **Problem 18**
Find the 3 most recently hired employees in each department.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Top N per group (temporal)

**Approach:** Window function (ROW_NUMBER)

```sql
SELECT employee_name, department, hire_date
FROM (
    SELECT 
        employee_name,
        department,
        hire_date,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY hire_date DESC) as rn
    FROM employees_prc
) ranked
WHERE rn <= 3;
```

**Key Recognition:**
- "3 most recently hired" = top 3 by date
- "in each department" = PARTITION BY department
- Need employee details = window function
</details>

---

### **Problem 19**
Show each employee's salary and the percentage it represents of their department's total salary budget.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Row value as percentage of group total

**Approach:** Window function

```sql
SELECT 
    employee_name,
    department,
    salary,
    SUM(salary) OVER (PARTITION BY department) as dept_total,
    ROUND(100.0 * salary / SUM(salary) OVER (PARTITION BY department), 2) as pct_of_dept_budget
FROM employees_prc;
```

**Key Recognition:**
- "each employee" = need individual rows
- "percentage of department's total" = individual value / group aggregate
- Window function for group aggregate on each row
</details>

---

### **Problem 20**
Find employees who were hired in the same month and year as at least one other employee.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Finding duplicates/groups with multiple members

**Approach:** GROUP BY with HAVING, then JOIN back

```sql
SELECT e.*
FROM employees_prc e
INNER JOIN (
    SELECT 
        DATE_TRUNC('month', hire_date) as hire_month,
        COUNT(*) as hire_count
    FROM employees_prc
    GROUP BY DATE_TRUNC('month', hire_date)
    HAVING COUNT(*) > 1
) months_with_multiple
ON DATE_TRUNC('month', e.hire_date) = months_with_multiple.hire_month;
```

**Alternative (using window function):**
```sql
SELECT employee_name, department, hire_date
FROM (
    SELECT 
        employee_name,
        department,
        hire_date,
        COUNT(*) OVER (PARTITION BY DATE_TRUNC('month', hire_date)) as same_month_count
    FROM employees_prc
) with_counts
WHERE same_month_count > 1;
```

**Key Recognition:**
- "same month as at least one other" = groups with COUNT > 1
- Can use GROUP BY + HAVING or window function
</details>

---

## 🎯 Level 3: Advanced Patterns (Problems 21-30)

### **Problem 21**
For each employee, calculate the number of days between their hire date and the previous employee's hire date in their department.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Sequential comparison with calculation

**Approach:** Window function (LAG)

```sql
SELECT 
    employee_name,
    department,
    hire_date,
    LAG(hire_date) OVER (PARTITION BY department ORDER BY hire_date) as prev_hire_date,
    hire_date - LAG(hire_date) OVER (PARTITION BY department ORDER BY hire_date) as days_since_last_hire
FROM employees_prc;
```

**Key Recognition:**
- "previous employee" = LAG function
- "in their department" = PARTITION BY department
- "days between" = date arithmetic
</details>

---

### **Problem 22**
Find departments where the salary gap between highest and lowest paid employees exceeds $50,000.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Filtering groups based on calculated aggregate

**Approach:** GROUP BY with HAVING

```sql
SELECT 
    department,
    MAX(salary) as highest_salary,
    MIN(salary) as lowest_salary,
    MAX(salary) - MIN(salary) as salary_gap
FROM employees_prc
GROUP BY department
HAVING MAX(salary) - MIN(salary) > 50000;
```

**Key Recognition:**
- "departments where" = filtering groups
- "salary gap exceeds" = HAVING with calculation
- GROUP BY with aggregate comparison
</details>

---

### **Problem 23**
Show a running count of employees hired, ordered by hire date.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Cumulative count

**Approach:** Window function (COUNT or ROW_NUMBER)

```sql
SELECT 
    employee_name,
    hire_date,
    ROW_NUMBER() OVER (ORDER BY hire_date) as employee_number
FROM employees_prc
ORDER BY hire_date;
```

**Alternative:**
```sql
SELECT 
    employee_name,
    hire_date,
    COUNT(*) OVER (ORDER BY hire_date) as cumulative_headcount
FROM employees_prc
ORDER BY hire_date;
```

**Key Recognition:**
- "running count" = cumulative calculation
- "ordered by hire date" = ORDER BY in window function
</details>

---

### **Problem 24**
Find employees whose salary is within 10% of their department's average salary.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Filtering based on group aggregate with tolerance

**Approach:** Window function with WHERE clause

```sql
SELECT employee_name, department, salary
FROM (
    SELECT 
        employee_name,
        department,
        salary,
        AVG(salary) OVER (PARTITION BY department) as dept_avg
    FROM employees_prc
) with_avg
WHERE ABS(salary - dept_avg) <= dept_avg * 0.10;
```

**Key Recognition:**
- "within 10% of department's average" = compare to group aggregate with tolerance
- Need individual rows = window function
- "within X%" = use ABS for distance calculation
</details>

---

### **Problem 25**
Calculate a 3-employee moving average of salaries when ordered by hire date within each department.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Moving average with frame

**Approach:** Window function with ROWS BETWEEN

```sql
SELECT 
    employee_name,
    department,
    hire_date,
    salary,
    AVG(salary) OVER (
        PARTITION BY department 
        ORDER BY hire_date 
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ) as moving_avg_3
FROM employees_prc;
```

**Key Recognition:**
- "moving average" = window function with frame
- "3-employee" = current + 1 before + 1 after
- "within each department" = PARTITION BY department
</details>

---

### **Problem 26**
Find the longest gap (in days) between consecutive hires in each department.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Maximum of calculated differences within groups

**Approach:** Window function (LAG) + GROUP BY

```sql
SELECT 
    department,
    MAX(days_between_hires) as longest_gap
FROM (
    SELECT 
        department,
        hire_date - LAG(hire_date) OVER (PARTITION BY department ORDER BY hire_date) as days_between_hires
    FROM employees_prc
) with_gaps
WHERE days_between_hires IS NOT NULL
GROUP BY department;
```

**Key Recognition:**
- "longest gap between consecutive" = MAX of LAG differences
- "in each department" = PARTITION BY + GROUP BY
- Multi-step: calculate gaps, then find max
</details>

---

### **Problem 27**
Show each employee and how many employees in their department earn more than them.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Counting rows that meet a condition within groups

**Approach:** Window function (COUNT with CASE) or self-join

```sql
-- Window function approach:
SELECT 
    employee_name,
    department,
    salary,
    COUNT(CASE WHEN salary > e.salary THEN 1 END) OVER (PARTITION BY department) as employees_earning_more
FROM employees_prc e;
```

**Alternative (correlated subquery):**
```sql
SELECT 
    e1.employee_name,
    e1.department,
    e1.salary,
    (SELECT COUNT(*) 
     FROM employees_prc e2 
     WHERE e2.department = e1.department 
     AND e2.salary > e1.salary) as employees_earning_more
FROM employees_prc e1;
```

**Key Recognition:**
- "how many employees earn more" = conditional count
- "in their department" = PARTITION BY department
- Need count on each row = window function or correlated subquery
</details>

---

### **Problem 28**
Find departments that have hired at least one employee in each of the last 3 years.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Groups meeting temporal criteria

**Approach:** GROUP BY with HAVING and date functions

```sql
SELECT department
FROM employees_prc
WHERE hire_date >= CURRENT_DATE - INTERVAL '3 years'
GROUP BY department
HAVING COUNT(DISTINCT EXTRACT(YEAR FROM hire_date)) = 3;
```

**Key Recognition:**
- "departments that have" = filtering groups
- "in each of the last 3 years" = DISTINCT year count
- GROUP BY with temporal HAVING condition
</details>

---

### **Problem 29**
Show each employee's salary, their department's median salary, and the difference.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Row comparison to group percentile

**Approach:** Window function (PERCENTILE_CONT)

```sql
SELECT 
    employee_name,
    department,
    salary,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) OVER (PARTITION BY department) as dept_median,
    salary - PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) OVER (PARTITION BY department) as diff_from_median
FROM employees_prc;
```

**Key Recognition:**
- "each employee" = need individual rows
- "department's median" = group percentile calculation
- Window function for percentile on each row
</details>

---

### **Problem 30**
Find the top 2 highest-paid employees in each department, but only for departments with more than 5 employees.

<details>
<summary>✅ Solution</summary>

**Pattern Type:** Top N per group with group filtering

**Approach:** Window function + filtering

```sql
SELECT employee_name, department, salary
FROM (
    SELECT 
        employee_name,
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn,
        COUNT(*) OVER (PARTITION BY department) as dept_size
    FROM employees_prc
) ranked
WHERE rn <= 2 
  AND dept_size > 5;
```

**Key Recognition:**
- "top 2 in each department" = ROW_NUMBER with PARTITION BY
- "only for departments with more than 5" = additional filter on group size
- Multiple window functions in same query
</details>

---

## 📊 Progress Tracking

After completing these problems, track your results:

- **Level 1 (1-10):** ___/10 correct on first try
- **Level 2 (11-20):** ___/10 correct on first try
- **Level 3 (21-30):** ___/10 correct on first try

**Goal:** 80% accuracy (24/30) before moving to real interview problems

---

## 🎯 What to Do Next

1. **If you scored < 70%:** Review the pattern recognition guide and retry missed problems
2. **If you scored 70-85%:** Focus on the problem types you missed, then do 10 more practice problems
3. **If you scored > 85%:** You're ready for LeetCode/HackerRank SQL problems!

---

## 💡 Study Tips

- **Don't just memorize solutions** - understand WHY each approach works
- **Look for trigger phrases** before writing any SQL
- **Practice identifying patterns** before solving
- **Time yourself** - aim to identify the pattern in < 30 seconds

Good luck! 🚀
