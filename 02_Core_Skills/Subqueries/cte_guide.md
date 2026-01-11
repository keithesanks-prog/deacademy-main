# 📦 SQL CTEs (Common Table Expressions): Complete Guide

**Temporary result sets that make complex queries readable**

---

## 🤔 What is a CTE?

A **CTE (Common Table Expression)** is a temporary named result set that exists only during the execution of a query. Think of it as a **temporary table** that disappears after the query runs.

**In Plain English:** "Give this subquery a name so I can reference it later."

---

## 📝 Basic Syntax

```sql
WITH cte_name AS (
    SELECT ...
    FROM ...
)
SELECT *
FROM cte_name;
```

**Key parts:**
1. `WITH` keyword
2. CTE name
3. `AS (...)` with the query
4. Main query that uses the CTE

---

## ⚠️ THE COMMA RULE (CRITICAL!)

### **One CTE: NO comma**
```sql
WITH cte_name AS (
    SELECT ...
)  -- ← NO COMMA!
SELECT * FROM cte_name;
```

### **Multiple CTEs: Comma BETWEEN them**
```sql
WITH cte1 AS (
    SELECT ...
),  -- ← COMMA HERE!
cte2 AS (
    SELECT ...
)  -- ← NO COMMA after last CTE!
SELECT * FROM cte1
JOIN cte2 ON ...;
```

---

## 🎯 Visual: When to Use Commas

```
WITH cte1 AS (...)  ← Start
    ,               ← Comma BETWEEN CTEs
cte2 AS (...)       ← Middle CTE
    ,               ← Comma BETWEEN CTEs
cte3 AS (...)       ← Last CTE (NO comma after!)

SELECT ...          ← Main query
```

---

## 📊 Problem-Solving with CTEs

### **Example Problem:**
> "Retrieve department names, the total number of employees in each department, and the average salary, but include only those departments where the average salary exceeds the overall average salary across all employees."

---

## 🧠 Step-by-Step Breakdown

### **Step 1: Identify What You Need**

**Question breakdown:**
- "department names" → `department`
- "total number of employees" → `COUNT(employee_id)`
- "average salary" → `AVG(salary)`
- "per department" → `GROUP BY department`
- "exceeds overall average" → Compare to global average

---

### **Step 2: Break Into Logical Steps**

**Step A:** Calculate department stats (count, average)  
**Step B:** Calculate global average  
**Step C:** Filter departments where dept avg > global avg

---

### **Step 3: Build the CTE**

```sql
WITH department_stats AS (
    SELECT 
        department,
        COUNT(employee_id) AS employee_count,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
)
SELECT *
FROM department_stats
WHERE avg_salary > (SELECT AVG(salary) FROM employees);
```

---

## 🔍 How It Executes

**Sample Data:**
| employee_id | department | salary |
|-------------|------------|--------|
| 1 | Sales | 50000 |
| 2 | Sales | 60000 |
| 3 | IT | 80000 |
| 4 | IT | 90000 |
| 5 | HR | 45000 |

**Step 1: CTE calculates department stats**
```sql
WITH department_stats AS (
    SELECT 
        department,
        COUNT(employee_id) AS employee_count,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
)
```

**CTE Result:**
| department | employee_count | avg_salary |
|------------|----------------|------------|
| Sales | 2 | 55000 |
| IT | 2 | 85000 |
| HR | 1 | 45000 |

**Step 2: Calculate global average**
```sql
SELECT AVG(salary) FROM employees
-- Result: 65000
```

**Step 3: Filter departments**
```sql
WHERE avg_salary > 65000
```

**Final Result:**
| department | employee_count | avg_salary |
|------------|----------------|------------|
| IT | 2 | 85000 |

---

## 💡 Multiple CTEs Example

**Problem:** Find employees earning more than their department average, and show department stats.

```sql
WITH department_averages AS (
    SELECT 
        department,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
),
high_earners AS (
    SELECT 
        e.employee_id,
        e.name,
        e.department,
        e.salary
    FROM employees e
    JOIN department_averages da ON e.department = da.department
    WHERE e.salary > da.avg_salary
)
SELECT 
    he.department,
    COUNT(*) AS high_earner_count,
    AVG(he.salary) AS avg_high_earner_salary
FROM high_earners he
GROUP BY he.department;
```

**Notice:**
- Comma AFTER `department_averages`
- NO comma AFTER `high_earners`

---

## 🎯 CTE vs Subquery

### **Subquery (Hard to Read)**
```sql
SELECT *
FROM (
    SELECT 
        department,
        COUNT(employee_id) AS employee_count,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
) AS dept_stats
WHERE avg_salary > (SELECT AVG(salary) FROM employees);
```

### **CTE (Easy to Read)**
```sql
WITH dept_stats AS (
    SELECT 
        department,
        COUNT(employee_id) AS employee_count,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
)
SELECT *
FROM dept_stats
WHERE avg_salary > (SELECT AVG(salary) FROM employees);
```

**Same result, but CTE is clearer!**

---

## ⚠️ Common Mistakes

### **Mistake 1: Comma after single CTE**
```sql
-- ❌ Wrong
WITH cte AS (...),
SELECT * FROM cte;

-- ✅ Correct
WITH cte AS (...)
SELECT * FROM cte;
```

### **Mistake 2: Missing comma between CTEs**
```sql
-- ❌ Wrong
WITH cte1 AS (...)
cte2 AS (...)

-- ✅ Correct
WITH cte1 AS (...),
cte2 AS (...)
```

### **Mistake 3: Comma after last CTE**
```sql
-- ❌ Wrong
WITH cte1 AS (...),
cte2 AS (...),
SELECT * FROM cte1;

-- ✅ Correct
WITH cte1 AS (...),
cte2 AS (...)
SELECT * FROM cte1;
```

---

## 🎯 When to Use CTEs

**Use CTEs when:**
- ✅ You need to reference the same subquery multiple times
- ✅ You want to make complex queries more readable
- ✅ You're building multi-step transformations
- ✅ You need to break down a complex problem

**Don't use CTEs when:**
- ❌ A simple subquery is clearer
- ❌ Performance is critical (CTEs can be slower in some databases)

---

## 🚀 Practice Problem

**Problem:** Find departments where the average salary is above $60,000 and show the count of employees.

<details>
<summary>Click for solution</summary>

```sql
WITH dept_stats AS (
    SELECT 
        department,
        COUNT(employee_id) AS employee_count,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
)
SELECT 
    department,
    employee_count,
    avg_salary
FROM dept_stats
WHERE avg_salary > 60000;
```

</details>

---

## 💡 Key Takeaways

1. **CTEs make complex queries readable**
2. **One CTE = NO comma after**
3. **Multiple CTEs = Comma BETWEEN, not after last**
4. **CTEs are temporary** (exist only during query execution)
5. **Use CTEs to break down complex problems** into logical steps
