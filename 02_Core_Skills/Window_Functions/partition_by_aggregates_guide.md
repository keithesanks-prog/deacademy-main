# 🎯 PARTITION BY with Aggregate Functions

**Calculate per-group aggregates while keeping all rows**

---

## 🤔 What Does PARTITION BY Do with Aggregates?

**PARTITION BY** with aggregate functions lets you calculate **group-level statistics** (like averages, sums, counts) while **keeping every row** in your result.

**The Magic:** You get both individual row data AND group statistics in the same query!

---

## 💡 The Key Difference

### **GROUP BY (Collapses Rows)**
```sql
SELECT 
    department,
    AVG(salary) AS avg_salary
FROM employees
GROUP BY department;
```

**Result (2 rows):**
| department | avg_salary |
|------------|------------|
| Sales      | 55000      |
| IT         | 75000      |

**Lost:** All individual employee data!

---

### **PARTITION BY (Keeps All Rows)**
```sql
SELECT 
    first_name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS avg_salary
FROM employees;
```

**Result (4 rows):**
| first_name | department | salary | avg_salary |
|------------|------------|--------|------------|
| Alice      | Sales      | 60000  | 55000      |
| Bob        | Sales      | 50000  | 55000      |
| Charlie    | IT         | 80000  | 75000      |
| Dave       | IT         | 70000  | 75000      |

**Kept:** All employee data + department average!

---

## 📊 Example: Salary Difference from Department Average

### **The Problem**
> "Show each employee's salary difference from their department's average salary."

### **The Query**
```sql
SELECT
    first_name,
    last_name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS avg_department_salary,
    salary - AVG(salary) OVER (PARTITION BY department) AS salary_difference
FROM employees;
```

---

### **Step-by-Step Execution**

**Sample Data:**
| first_name | last_name | department | salary |
|------------|-----------|------------|--------|
| Alice      | Smith     | Sales      | 60000  |
| Bob        | Jones     | Sales      | 50000  |
| Charlie    | Lee       | IT         | 80000  |
| Dave       | Kim       | IT         | 70000  |

**Step 1: PARTITION BY department**

**Original Table (All Employees):**
```
┌─────────────┬────────────┬────────┐
│ first_name  │ department │ salary │
├─────────────┼────────────┼────────┤
│ Alice       │ Sales      │ 60000  │
│ Bob         │ Sales      │ 50000  │
│ Charlie     │ IT         │ 80000  │
│ Dave        │ IT         │ 70000  │
└─────────────┴────────────┴────────┘
```

**After PARTITION BY department (Creates 2 Windows):**
```
Window 1: Sales                Window 2: IT
┌─────────────┬────────┐      ┌─────────────┬────────┐
│ first_name  │ salary │      │ first_name  │ salary │
├─────────────┼────────┤      ├─────────────┼────────┤
│ Alice       │ 60000  │      │ Charlie     │ 80000  │
│ Bob         │ 50000  │      │ Dave        │ 70000  │
└─────────────┴────────┘      └─────────────┴────────┘
   AVG: 55000                     AVG: 75000
```

**Key Point:** Each partition calculates its own average independently!

**Step 2: Calculate AVG(salary) per partition**
```sql
AVG(salary) OVER (PARTITION BY department)
```

**Result (Averages Added to Each Row):**
```
┌─────────────┬────────────┬────────┬───────────────────────┐
│ first_name  │ department │ salary │ avg_department_salary │
├─────────────┼────────────┼────────┼───────────────────────┤
│ Alice       │ Sales      │ 60000  │ 55000 ← Sales avg     │
│ Bob         │ Sales      │ 50000  │ 55000 ← Sales avg     │
│ Charlie     │ IT         │ 80000  │ 75000 ← IT avg        │
│ Dave        │ IT         │ 70000  │ 75000 ← IT avg        │
└─────────────┴────────────┴────────┴───────────────────────┘
```

**Notice:** All rows kept, but each row gets its department's average!

**Step 3: Calculate difference**
```sql
salary - AVG(salary) OVER (PARTITION BY department)
```

| first_name | department | salary | avg_department_salary |
|------------|------------|--------|-----------------------|
| Alice      | Sales      | 60000  | 55000 ← (60000+50000)/2 |
| Bob        | Sales      | 50000  | 55000 ← Same average |
| Charlie    | IT         | 80000  | 75000 ← (80000+70000)/2 |
| Dave       | IT         | 70000  | 75000 ← Same average |

**Step 3: Calculate difference**
```sql
salary - AVG(salary) OVER (PARTITION BY department)
```

**Final Result:**
| first_name | last_name | department | salary | avg_department_salary | salary_difference |
|------------|-----------|------------|--------|-----------------------|-------------------|
| Alice      | Smith     | Sales      | 60000  | 55000                 | **+5000** ✅      |
| Bob        | Jones     | Sales      | 50000  | 55000                 | **-5000** ❌      |
| Charlie    | Lee       | IT         | 80000  | 75000                 | **+5000** ✅      |
| Dave       | Kim       | IT         | 70000  | 75000                 | **-5000** ❌      |

**Interpretation:**
- Alice earns $5,000 **above** Sales average
- Bob earns $5,000 **below** Sales average
- Charlie earns $5,000 **above** IT average
- Dave earns $5,000 **below** IT average

---

## 🎯 Other Aggregate Functions with PARTITION BY

### **1. SUM (Running Total per Department)**
```sql
SELECT 
    department,
    employee,
    salary,
    SUM(salary) OVER (PARTITION BY department ORDER BY hire_date) AS running_total
FROM employees;
```

**Example:**
| department | employee | salary | running_total |
|------------|----------|--------|---------------|
| Sales      | Alice    | 60000  | 60000         |
| Sales      | Bob      | 50000  | 110000        |
| IT         | Charlie  | 80000  | 80000         |
| IT         | Dave     | 70000  | 150000        |

---

### **2. COUNT (Employee Count per Department)**
```sql
SELECT 
    employee,
    department,
    COUNT(*) OVER (PARTITION BY department) AS dept_employee_count
FROM employees;
```

**Example:**
| employee | department | dept_employee_count |
|----------|------------|---------------------|
| Alice    | Sales      | 2                   |
| Bob      | Sales      | 2                   |
| Charlie  | IT         | 2                   |
| Dave     | IT         | 2                   |

---

### **3. MAX/MIN (Highest/Lowest in Department)**
```sql
SELECT 
    employee,
    department,
    salary,
    MAX(salary) OVER (PARTITION BY department) AS highest_in_dept,
    MIN(salary) OVER (PARTITION BY department) AS lowest_in_dept,
    salary - MIN(salary) OVER (PARTITION BY department) AS above_minimum
FROM employees;
```

**Example:**
| employee | department | salary | highest_in_dept | lowest_in_dept | above_minimum |
|----------|------------|--------|-----------------|----------------|---------------|
| Alice    | Sales      | 60000  | 60000           | 50000          | 10000         |
| Bob      | Sales      | 50000  | 60000           | 50000          | 0             |
| Charlie  | IT         | 80000  | 80000           | 70000          | 10000         |
| Dave     | IT         | 70000  | 80000           | 70000          | 0             |

---

## ⚠️ Common Mistakes

### **Mistake 1: Forgetting PARTITION BY**
```sql
-- ❌ Wrong (global average, not per department)
AVG(salary) OVER () AS avg_salary

-- ✅ Correct (department average)
AVG(salary) OVER (PARTITION BY department) AS avg_salary
```

### **Mistake 2: Using GROUP BY instead**
```sql
-- ❌ Wrong (loses individual rows)
SELECT department, AVG(salary)
FROM employees
GROUP BY department;

-- ✅ Correct (keeps all rows)
SELECT *, AVG(salary) OVER (PARTITION BY department)
FROM employees;
```

---

## 🎯 When to Use PARTITION BY with Aggregates

**Use when you need:**
- ✅ Individual row data + group statistics
- ✅ Comparisons to group averages/totals
- ✅ Percentage of group total
- ✅ Difference from group average

**Don't use when:**
- ❌ You only need group totals (use GROUP BY)
- ❌ You don't need individual rows

---

## 💡 Practice Problem

**Problem:** Show each product's price and how much it differs from the average price in its category.

<details>
<summary>Click for solution</summary>

```sql
SELECT 
    product_name,
    category,
    price,
    AVG(price) OVER (PARTITION BY category) AS avg_category_price,
    price - AVG(price) OVER (PARTITION BY category) AS price_difference
FROM products;
```

</details>

---

## 🚀 Key Takeaways

1. **PARTITION BY + aggregates = Keep all rows + add group stats**
2. **GROUP BY = Collapse to group totals only**
3. **Use PARTITION BY when you need both individual and group data**
4. **Common pattern:** `value - AVG(value) OVER (PARTITION BY group)`
