# SQL Pattern Recognition Guide
## How to Identify When to Use Window Functions vs GROUP BY vs Subqueries

---

## 🚦 The 3-Second Decision Framework

When you read a SQL problem, ask these questions **in order**:

```
┌─────────────────────────────────────────────────────────────┐
│ QUESTION 1: Do I need to see INDIVIDUAL ROWS in the output? │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
               YES                     NO
                │                       │
                ▼                       ▼
    ┌─────────────────────┐   ┌──────────────────┐
    │ Go to QUESTION 2    │   │ Use GROUP BY     │
    └─────────────────────┘   │ or simple WHERE  │
                │              └──────────────────┘
                ▼
┌──────────────────────────────────────────────────────────────┐
│ QUESTION 2: Do I need to compare each row to OTHER ROWS     │
│             in the SAME GROUP?                               │
└──────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
               YES                     NO
                │                       │
                ▼                       ▼
    ┌─────────────────────┐   ┌──────────────────────┐
    │ WINDOW FUNCTION     │   │ Use JOIN or          │
    │ (PARTITION BY)      │   │ Correlated Subquery  │
    └─────────────────────┘   └──────────────────────┘
```

---

## 📋 Quick Reference: Trigger Phrases

### 🔴 **WINDOW FUNCTION Signals**

| Phrase | Example | Solution |
|--------|---------|----------|
| **"top N per/in each"** | "Top 3 salaries per department" | `ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC)` |
| **"highest/lowest in each"** | "Highest salary in each department" | `ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC)` |
| **"first/last per group"** | "First order for each customer" | `ROW_NUMBER() OVER (PARTITION BY customer ORDER BY date)` |
| **"rank within"** | "Rank employees within department" | `RANK() OVER (PARTITION BY dept ORDER BY performance)` |
| **"running total"** | "Running total of sales by date" | `SUM(amount) OVER (ORDER BY date)` |
| **"moving average"** | "7-day moving average" | `AVG(value) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` |
| **"previous/next"** | "Compare to previous month" | `LAG(value) OVER (ORDER BY month)` |
| **"difference from average"** | "Salary vs department average" | `salary - AVG(salary) OVER (PARTITION BY dept)` |

### 🟡 **GROUP BY Signals**

| Phrase | Example | Solution |
|--------|---------|----------|
| **"total per"** | "Total sales per region" | `SELECT region, SUM(sales) FROM ... GROUP BY region` |
| **"count of each"** | "Count of employees per department" | `SELECT dept, COUNT(*) FROM ... GROUP BY dept` |
| **"average by"** | "Average salary by department" | `SELECT dept, AVG(salary) FROM ... GROUP BY dept` |
| **"summarize by"** | "Summarize revenue by quarter" | `SELECT quarter, SUM(revenue) FROM ... GROUP BY quarter` |

### 🟢 **SUBQUERY Signals**

| Phrase | Example | Solution |
|--------|---------|----------|
| **"employees who earn more than average"** | Filter based on aggregate | `WHERE salary > (SELECT AVG(salary) FROM ...)` |
| **"departments with more than X employees"** | Filter groups | `HAVING COUNT(*) > X` |
| **"customers who never ordered"** | NOT EXISTS pattern | `WHERE NOT EXISTS (SELECT 1 FROM orders WHERE ...)` |

---

## 🎯 Pattern Recognition Practice

### **Problem Type 1: "Top N in Each Group"**

**Problem:** *"Find the 3 highest-paid employees in each department"*

**Recognition Checklist:**
- ✅ "3 highest" = ranking/ordering needed
- ✅ "in each department" = grouping needed
- ✅ Need to see employee names = individual rows needed

**Solution Pattern:**
```sql
SELECT *
FROM (
    SELECT 
        employee_name,
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM employees_prc
) ranked
WHERE rn <= 3;
```

**Key Components:**
- `PARTITION BY department` ← "in each department"
- `ORDER BY salary DESC` ← "highest-paid"
- `WHERE rn <= 3` ← "top 3"

---

### **Problem Type 2: "Aggregate Per Group"**

**Problem:** *"What is the total salary budget for each department?"*

**Recognition Checklist:**
- ❌ Don't need individual employee rows
- ✅ Just need one number per department
- ✅ "total" = SUM aggregate

**Solution Pattern:**
```sql
SELECT 
    department,
    SUM(salary) as total_budget
FROM employees_prc
GROUP BY department;
```

**Why NOT a window function?**
- Output is ONE ROW per department
- No need to compare individual employees

---

### **Problem Type 3: "Row Comparison Within Group"**

**Problem:** *"Show each employee's salary and how it compares to their department average"*

**Recognition Checklist:**
- ✅ "each employee" = need individual rows
- ✅ "department average" = need aggregate calculation
- ✅ Need BOTH on same row = window function

**Solution Pattern:**
```sql
SELECT 
    employee_name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) as diff_from_avg
FROM employees_prc;
```

**Key Insight:**
- Can't use GROUP BY (would lose individual rows)
- Window function lets you see row-level AND group-level data together

---

### **Problem Type 4: "Sequential/Temporal Comparison"**

**Problem:** *"Show each month's sales and the change from the previous month"*

**Recognition Checklist:**
- ✅ "each month" = need individual rows
- ✅ "previous month" = need to access another row
- ✅ Sequential comparison = LAG/LEAD

**Solution Pattern:**
```sql
SELECT 
    month,
    sales,
    LAG(sales) OVER (ORDER BY month) as prev_month_sales,
    sales - LAG(sales) OVER (ORDER BY month) as month_over_month_change
FROM monthly_sales;
```

---

## 🧪 Self-Test: Can You Identify the Pattern?

For each problem below, identify:
1. What type of problem is it?
2. What SQL approach should you use?
3. What are the key components?

### **Test Problem 1**
*"Find all employees who earn more than the average salary in their department"*

<details>
<summary>Click for answer</summary>

**Type:** Filtering based on group aggregate

**Approach:** Window function OR correlated subquery

**Window Function Solution:**
```sql
SELECT *
FROM (
    SELECT 
        employee_name,
        department,
        salary,
        AVG(salary) OVER (PARTITION BY department) as dept_avg
    FROM employees_prc
) with_avg
WHERE salary > dept_avg;
```

**Subquery Solution:**
```sql
SELECT *
FROM employees_prc e1
WHERE salary > (
    SELECT AVG(salary)
    FROM employees_prc e2
    WHERE e2.department = e1.department
);
```

**Key Recognition:**
- "more than average" = comparison to aggregate
- "in their department" = grouped comparison
- Need individual employee rows = window function or correlated subquery
</details>

---

### **Test Problem 2**
*"List all departments with their employee count"*

<details>
<summary>Click for answer</summary>

**Type:** Simple aggregation per group

**Approach:** GROUP BY

**Solution:**
```sql
SELECT 
    department,
    COUNT(*) as employee_count
FROM employees_prc
GROUP BY department;
```

**Key Recognition:**
- Just need count per department
- No individual row details needed
- Simple GROUP BY is sufficient
</details>

---

### **Test Problem 3**
*"Show the hire date of the most recently hired employee in each department"*

<details>
<summary>Click for answer</summary>

**Type:** Aggregate per group (if you only need the date)

**Approach:** GROUP BY

**Solution:**
```sql
SELECT 
    department,
    MAX(hire_date) as most_recent_hire
FROM employees_prc
GROUP BY department;
```

**Key Recognition:**
- "most recently hired" = MAX(hire_date)
- "in each department" = GROUP BY department
- Only need the date, not employee details

**Alternative:** If you need the employee's NAME too, then use window function:
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
</details>

---

### **Test Problem 4**
*"Calculate a running total of sales by date"*

<details>
<summary>Click for answer</summary>

**Type:** Cumulative calculation

**Approach:** Window function with ORDER BY

**Solution:**
```sql
SELECT 
    sale_date,
    amount,
    SUM(amount) OVER (ORDER BY sale_date) as running_total
FROM sales
ORDER BY sale_date;
```

**Key Recognition:**
- "running total" = cumulative sum
- Need to see each row + accumulated value
- Window function with ORDER BY (no PARTITION needed if calculating across all rows)
</details>

---

### **Test Problem 5**
*"Find departments where the average salary is above $80,000"*

<details>
<summary>Click for answer</summary>

**Type:** Filtering groups based on aggregate

**Approach:** GROUP BY with HAVING

**Solution:**
```sql
SELECT 
    department,
    AVG(salary) as avg_salary
FROM employees_prc
GROUP BY department
HAVING AVG(salary) > 80000;
```

**Key Recognition:**
- "departments where" = filtering groups
- "average salary" = aggregate calculation
- HAVING clause filters after grouping
</details>

---

## 🎓 Advanced Pattern: When You Need BOTH Individual Rows AND Group Info

**Problem:** *"Show all employees, their salary, their department's average salary, and mark if they're above average"*

**This is a classic window function use case:**

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
    END as performance_category
FROM employees_prc;
```

**Why window function?**
- Need every employee row (can't use GROUP BY)
- Need department average on each row
- Window function provides both

---

## 📊 Common Mistakes to Avoid

### ❌ **Mistake 1: Using GROUP BY when you need individual rows**

**Problem:** "Show each employee and their department's average salary"

**Wrong:**
```sql
SELECT department, AVG(salary)
FROM employees_prc
GROUP BY department;
-- This only shows departments, not individual employees!
```

**Right:**
```sql
SELECT 
    employee_name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg
FROM employees_prc;
```

---

### ❌ **Mistake 2: Using window function when GROUP BY is simpler**

**Problem:** "What is the total salary per department?"

**Overcomplicated:**
```sql
SELECT DISTINCT
    department,
    SUM(salary) OVER (PARTITION BY department) as total
FROM employees_prc;
-- Works, but unnecessarily complex
```

**Better:**
```sql
SELECT 
    department,
    SUM(salary) as total
FROM employees_prc
GROUP BY department;
```

---

## 🔄 Practice Routine

To build pattern recognition:

1. **Daily Practice (10 minutes):**
   - Read 5 SQL problem statements
   - Before solving, identify the pattern type
   - Check your answer

2. **Weekly Review:**
   - Solve 10 problems
   - Track which patterns you miss
   - Focus extra practice on weak areas

3. **Pattern Journal:**
   - When you encounter a new pattern, document it
   - Write down the trigger phrases
   - Add to your personal cheat sheet

---

## 🎯 Your Next Steps

1. **Print/bookmark this guide** for quick reference
2. **Complete the practice problem set** (see `pattern_practice_problems.md`)
3. **Track your progress** (see `pattern_recognition_tracker.md`)
4. **Review trigger phrases** before each practice session

---

## 💡 Remember

**Pattern recognition is a SKILL, not a talent.**

You're not "bad at this" - you just haven't practiced enough yet. Every expert was once a beginner who struggled with the same patterns.

**Your goal:** After 2 weeks of daily practice, you should be able to identify the correct approach 80% of the time just from reading the problem statement.

You've got this! 💪
