# ROW_NUMBER() Practice Problems
## Focused Practice for Mastering ROW_NUMBER() OVER (PARTITION BY ...)

---

## 🎯 ROW_NUMBER() Quick Reference

### **Basic Syntax:**
```sql
ROW_NUMBER() OVER (
    [PARTITION BY column1, column2, ...]  -- Optional: creates groups
    ORDER BY column3 [ASC|DESC]           -- Required: determines numbering order
) AS row_num
```

### **What it does:**
- Assigns a **unique sequential number** to each row
- Numbering **starts at 1** for each partition (group)
- **No ties** - even identical values get different numbers

### **Common Pattern:**
```sql
-- Step 1: Number rows within groups
-- Step 2: Filter to get top N per group
SELECT *
FROM (
    SELECT 
        columns...,
        ROW_NUMBER() OVER (PARTITION BY group_column ORDER BY rank_column DESC) as rn
    FROM table_name
) ranked
WHERE rn <= N;  -- Top N per group
```

---

## 📝 Practice Problems

### **Problem 1: Basic Numbering (No Partitioning)**
Number all employees by salary (highest to lowest).

<details>
<summary>💡 Hint</summary>
No PARTITION BY needed - just ORDER BY salary DESC
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    employee_name,
    department,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as salary_rank
FROM employees_prc
ORDER BY salary_rank;
```

**Key Points:**
- No `PARTITION BY` = numbers across entire table
- `ORDER BY salary DESC` = highest salary gets #1
- Ivy Taylor (125000) = 1, Alice Johnson (120000) = 2, etc.
</details>

---

### **Problem 2: Top 1 Per Department**
Find the highest-paid employee in each department.

<details>
<summary>💡 Hint</summary>
PARTITION BY department, ORDER BY salary DESC, then filter WHERE rn = 1
</details>

<details>
<summary>✅ Solution</summary>

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

**Result:**
```
employee_name    | department   | salary
-----------------|--------------|--------
Ivy Taylor       | Engineering  | 125000
Rachel Martinez  | Sales        | 96000
Victor Lewis     | HR           | 85000
Chris Wright     | Marketing    | 91000
```

**Key Points:**
- `PARTITION BY department` = separate numbering for each dept
- `WHERE rn = 1` = only the #1 in each group
</details>

---

### **Problem 3: Top 3 Per Department**
Find the 3 highest-paid employees in each department.

<details>
<summary>💡 Hint</summary>
Same as Problem 2, but WHERE rn <= 3
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT employee_name, department, salary, rn as dept_rank
FROM (
    SELECT 
        employee_name,
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM employees_prc
) ranked
WHERE rn <= 3
ORDER BY department, rn;
```

**Result:**
```
employee_name   | department   | salary  | dept_rank
----------------|--------------|---------|----------
Ivy Taylor      | Engineering  | 125000  | 1
Alice Johnson   | Engineering  | 120000  | 2
Bob Smith       | Engineering  | 115000  | 3
Victor Lewis    | HR           | 85000   | 1
...
```
</details>

---

### **Problem 4: Bottom 2 Per Department (Lowest Salaries)**
Find the 2 lowest-paid employees in each department.

<details>
<summary>💡 Hint</summary>
Change ORDER BY to ASC instead of DESC
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT employee_name, department, salary
FROM (
    SELECT 
        employee_name,
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary ASC) as rn
    FROM employees_prc
) ranked
WHERE rn <= 2
ORDER BY department, salary;
```

**Key Point:** `ORDER BY salary ASC` makes lowest salary = rn 1
</details>

---

### **Problem 5: Most Recently Hired Employee Per Department**
Find the most recently hired employee in each department.

<details>
<summary>💡 Hint</summary>
PARTITION BY department, ORDER BY hire_date DESC
</details>

<details>
<summary>✅ Solution</summary>

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
WHERE rn = 1;
```

**Key Point:** `ORDER BY hire_date DESC` = most recent date gets rn = 1
</details>

---

### **Problem 6: 3 Oldest Employees (By Hire Date) in Company**
Find the 3 employees who have been with the company longest.

<details>
<summary>💡 Hint</summary>
No PARTITION BY (company-wide), ORDER BY hire_date ASC
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT employee_name, department, hire_date
FROM (
    SELECT 
        employee_name,
        department,
        hire_date,
        ROW_NUMBER() OVER (ORDER BY hire_date ASC) as rn
    FROM employees_prc
) ranked
WHERE rn <= 3
ORDER BY hire_date;
```

**Result:**
```
employee_name    | department   | hire_date
-----------------|--------------|------------
Ivy Taylor       | Engineering  | 2019-11-08
Rachel Martinez  | Sales        | 2019-12-01
Alice Johnson    | Engineering  | 2020-01-15
```
</details>

---

### **Problem 7: Second Highest Salary Per Department**
Find the employee with the 2nd highest salary in each department.

<details>
<summary>💡 Hint</summary>
Same pattern, but WHERE rn = 2
</details>

<details>
<summary>✅ Solution</summary>

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
WHERE rn = 2;
```
</details>

---

### **Problem 8: Employees Ranked 4-6 by Salary in Each Department**
Show employees ranked 4th, 5th, and 6th by salary in each department.

<details>
<summary>💡 Hint</summary>
WHERE rn BETWEEN 4 AND 6 or WHERE rn >= 4 AND rn <= 6
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT employee_name, department, salary, rn as salary_rank
FROM (
    SELECT 
        employee_name,
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM employees_prc
) ranked
WHERE rn BETWEEN 4 AND 6
ORDER BY department, rn;
```

**Note:** Some departments might not have 6 employees, so they won't appear in results.
</details>

---

### **Problem 9: Number Employees by Hire Date Within Department**
Assign each employee a number based on when they were hired in their department (1 = first hired).

<details>
<summary>💡 Hint</summary>
PARTITION BY department, ORDER BY hire_date ASC, but don't filter - show all rows
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    employee_name,
    department,
    hire_date,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY hire_date ASC) as hire_order
FROM employees_prc
ORDER BY department, hire_order;
```

**Key Point:** No WHERE clause - we want to see ALL employees with their number
</details>

---

### **Problem 10: Alternating Pattern - Odd Ranked Employees Only**
Show only employees with odd-numbered salary ranks (1st, 3rd, 5th, etc.) in each department.

<details>
<summary>💡 Hint</summary>
Use MOD function: WHERE MOD(rn, 2) = 1 or WHERE rn % 2 = 1
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT employee_name, department, salary, rn as salary_rank
FROM (
    SELECT 
        employee_name,
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM employees_prc
) ranked
WHERE MOD(rn, 2) = 1  -- or: WHERE rn % 2 = 1
ORDER BY department, rn;
```

**Key Point:** `MOD(rn, 2) = 1` filters to odd numbers only
</details>

---

## 🎓 Advanced Challenges

### **Challenge 1: Multiple Partitions**
Number employees by salary within each department, but also show their overall company rank.

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    employee_name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as company_rank
FROM employees_prc
ORDER BY company_rank;
```

**Key Point:** You can have multiple `ROW_NUMBER()` functions in the same query!
</details>

---

### **Challenge 2: Exclude Top and Bottom**
Show employees ranked 2-4 by salary in each department (exclude highest and lowest extremes).

<details>
<summary>✅ Solution</summary>

```sql
SELECT employee_name, department, salary, rn as salary_rank
FROM (
    SELECT 
        employee_name,
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn,
        COUNT(*) OVER (PARTITION BY department) as dept_size
    FROM employees_prc
) ranked
WHERE rn >= 2 AND rn <= dept_size - 1 AND rn <= 4
ORDER BY department, rn;
```

**Key Point:** Combines multiple window functions and complex filtering
</details>

---

### **Challenge 3: First and Last Hired Per Department**
Show only the first and last employee hired in each department.

<details>
<summary>✅ Solution</summary>

```sql
SELECT employee_name, department, hire_date, 
       CASE WHEN rn = 1 THEN 'First Hired' ELSE 'Most Recent' END as hire_status
FROM (
    SELECT 
        employee_name,
        department,
        hire_date,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY hire_date ASC) as rn,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY hire_date DESC) as rn_desc
    FROM employees_prc
) ranked
WHERE rn = 1 OR rn_desc = 1
ORDER BY department, hire_date;
```

**Key Point:** Uses two different `ROW_NUMBER()` calculations with opposite ordering
</details>

---

## 🧠 Common Mistakes to Avoid

### **Mistake 1: Forgetting to include columns in subquery**
```sql
-- ❌ WRONG - department not in subquery SELECT
SELECT employee_name, department, salary
FROM (
    SELECT employee_name, salary,
           ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM employees_prc
) ranked
WHERE rn = 1;

-- ✅ CORRECT
SELECT employee_name, department, salary
FROM (
    SELECT employee_name, department, salary,  -- ← Include department!
           ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM employees_prc
) ranked
WHERE rn = 1;
```

---

### **Mistake 2: Forgetting ORDER BY in ROW_NUMBER()**
```sql
-- ❌ WRONG - ROW_NUMBER requires ORDER BY
ROW_NUMBER() OVER (PARTITION BY department)  -- ERROR!

-- ✅ CORRECT
ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)
```

---

### **Mistake 3: Filtering in wrong place**
```sql
-- ❌ WRONG - Can't filter on window function in same query level
SELECT employee_name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) as rn
FROM employees_prc
WHERE rn = 1;  -- ERROR: rn doesn't exist yet!

-- ✅ CORRECT - Use subquery
SELECT employee_name, salary
FROM (
    SELECT employee_name, salary,
           ROW_NUMBER() OVER (ORDER BY salary DESC) as rn
    FROM employees_prc
) ranked
WHERE rn = 1;
```

---

## 🎯 Practice Routine

**Daily drill (10 minutes):**
1. Pick 3 random problems from above
2. Write the query from memory (don't look at solution)
3. Test in [DB Fiddle](https://www.db-fiddle.com/)
4. Check solution and understand any differences

**Goal:** After 1 week, you should be able to write `ROW_NUMBER()` queries confidently without reference!

---

## 📚 Next Steps

Once you're comfortable with `ROW_NUMBER()`, learn:
- **RANK()** - allows ties (1, 2, 2, 4)
- **DENSE_RANK()** - allows ties without gaps (1, 2, 2, 3)
- **NTILE()** - divides into equal groups

But master `ROW_NUMBER()` first - it's the foundation! 💪
