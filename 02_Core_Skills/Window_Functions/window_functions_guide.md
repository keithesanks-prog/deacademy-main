# 🎓 SQL Window Functions: Complete Training Guide

**Master RANK(), ROW_NUMBER(), and PARTITION BY**

---

## 📚 What Are Window Functions?

**Window Functions** let you perform calculations **across a set of rows** related to the current row, without collapsing the rows (like GROUP BY does).

**Key Difference from GROUP BY:**
- **GROUP BY**: Collapses rows into groups (many rows → one row per group)
- **Window Functions**: Keeps all rows, but adds calculated columns

---

## 🎯 The Core Concept: PARTITION BY

**PARTITION BY** splits your data into "windows" (groups), and the function operates within each window.

**Example Data:**

| category  | youtuber  | video_views |
|---------- |---------- |-------------|
| Gaming    | Alice     | 50000       |
| Gaming    | Bob       | 30000       |
| Music     | Eve       | 40000       |
| Music     | Frank     | 25000       |

**Query:**
```sql
SELECT 
    category,
    youtuber,
    video_views,
    RANK() OVER (PARTITION BY category ORDER BY video_views DESC) AS rnk
FROM youtubers;
```

**What happens:**
1. **PARTITION BY category** → Creates 2 windows (Gaming, Music)
2. **ORDER BY video_views DESC** → Sorts each window by views
3. **RANK()** → Assigns ranks within each window

**Result:**

| category  | youtuber  | video_views | rnk   |
|---------- |---------- |-------------|-----  |
| Gaming    | Alice     | 50000       | **1** |
| Gaming    | Bob       | 30000       | **2** |
| Music     | Eve       | 40000       | **1** |
| Music     | Frank     | 25000       | **2** |

**Notice:** Each category has its own ranking (1, 2...).

---

## 🔢 The Three Main Ranking Functions

### **1. ROW_NUMBER()**

**Assigns a unique number to each row** (no ties).

```sql
ROW_NUMBER() OVER (PARTITION BY category ORDER BY video_views DESC)
```

**Example:**

| category  | youtuber  | views     | row_num |
|---------- |---------- |-----------|---------|
| Gaming    | Alice     | 50000     | 1       |
| Gaming    | Bob       | 50000     | 2 ← Different from Alice! |
| Gaming    | Charlie   | 30000     | 3       |

**Use Case:** "Get the 2nd highest value" (no ties allowed).

---

### **2. RANK()**

**Assigns ranks, but skips numbers after ties.**

```sql
RANK() OVER (PARTITION BY category ORDER BY video_views DESC)
```

**Example:**

| category  | youtuber  | views     | rank  |
|---------- |---------- |-----------|-------|
| Gaming    | Alice     | 50000     | 1     |
| Gaming    | Bob       | 50000     | 1 ← Tied! |
| Gaming    | Charlie   | 30000     | **3** ← Skipped 2! |

**Use Case:** "Top 3 winners" (ties share the same rank).

---

### **3. DENSE_RANK()**

**Assigns ranks, but does NOT skip numbers after ties.**

```sql
DENSE_RANK() OVER (PARTITION BY category ORDER BY video_views DESC)
```

**Example:**

| category  | youtuber  | views     | dense_rank |
|---------- |---------- |-----------|------------|
| Gaming    | Alice     | 50000     | 1          |
| Gaming    | Bob       | 50000     | 1 ← Tied!  |
| Gaming    | Charlie   | 30000     | **2** ← No skip! |

**Use Case:** "Top 3 distinct values" (no gaps in ranking).

---

## 🧩 The Anatomy of a Window Function

```sql
RANK() OVER (PARTITION BY category ORDER BY video_views DESC)
  ↑        ↑         ↑                    ↑
Function  Keyword  Group By          Sort Within Group
```

**Breakdown:**
1. **RANK()** → The function (ROW_NUMBER, RANK, DENSE_RANK, etc.)
2. **OVER** → Signals this is a window function
3. **PARTITION BY** → Defines the groups (optional)
4. **ORDER BY** → Defines the sort order within each group

---

## 🚀 Common Use Cases

### **Use Case 1: Top N per Group**

**Problem:** Find the top 3 YouTubers in each category.

```sql
SELECT *
FROM (
    SELECT 
        category,
        youtuber,
        video_views,
        RANK() OVER (PARTITION BY category ORDER BY video_views DESC) AS rnk
    FROM youtubers
) a
WHERE a.rnk <= 3;
```

---

### **Use Case 2: Nth Highest Value**

**Problem:** Find the 2nd highest salary in each department.

```sql
SELECT *
FROM (
    SELECT 
        department,
        employee,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
    FROM employees
) a
WHERE a.rn = 2;
```

---

---

### **Use Case 3: Ranking Aggregated Data (RANK + GROUP BY)**

**Problem:** Rank customers by their total order amount (highest to lowest).

**Key Insight:** You need to **aggregate first** (GROUP BY), **then rank** the aggregated values.

```sql
SELECT
    c.customer_id,
    c.customer_name,
    SUM(o.order_amount) AS total_order_amount,
    RANK() OVER (ORDER BY SUM(o.order_amount) DESC) AS rank
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;
```

**Step-by-Step:**

**Sample Data:**
| customer_id | customer_name | order_amount |
|-------------|---------------|--------------|
| 1           | Alice         | 100          |
| 1           | Alice         | 200          |
| 2           | Bob           | 500          |
| 3           | Charlie       | 150          |

**Step 1: GROUP BY to get totals**
```sql
GROUP BY c.customer_id, c.customer_name
```

| customer_id | customer_name | total_order_amount |
|-------------|---------------|--------------------|
| 1           | Alice         | 300                |
| 2           | Bob           | 500                |
| 3           | Charlie       | 150                |

**Step 2: RANK the totals**
```sql
RANK() OVER (ORDER BY SUM(o.order_amount) DESC)
```

| customer_id | customer_name | total_order_amount | rank |
|-------------|---------------|--------------------|------|
| 2           | Bob           | 500                | 1    |
| 1           | Alice         | 300                | 2    |
| 3           | Charlie       | 150                | 3    |

**Important:** You must `GROUP BY` all non-aggregated columns (customer_id, customer_name).

---

### **Use Case 4: Running Totals**

**Problem:** Calculate cumulative sales per month.

```sql
SELECT 
    month,
    sales,
    SUM(sales) OVER (ORDER BY month) AS running_total
FROM monthly_sales;
```

---

## ⚠️ Common Mistakes

### **Mistake 1: Using Window Functions in WHERE**

**Wrong:**
```sql
SELECT *
FROM youtubers
WHERE RANK() OVER (PARTITION BY category ORDER BY views DESC) <= 3;
-- ERROR!
```

**Right:**
```sql
SELECT *
FROM (
    SELECT *, RANK() OVER (...) AS rnk
    FROM youtubers
) a
WHERE a.rnk <= 3;
```

**Why?** Window functions are calculated AFTER the WHERE clause.

---

### **Mistake 2: Forgetting ORDER BY**

**Wrong:**
```sql
RANK() OVER (PARTITION BY category)  -- Missing ORDER BY!
```

**Right:**
```sql
RANK() OVER (PARTITION BY category ORDER BY video_views DESC)
```

**Why?** Without ORDER BY, the ranking is arbitrary.

---

## 🎯 Quick Reference

| Function         | Handles Ties?       | Skips Numbers?  | Use Case             |
|----------------- |---------------------|-----------------|----------------------|
| **ROW_NUMBER()** | No (assigns unique) | N/A             | Nth value (no ties)  |
| **RANK()**       | Yes (same rank)     | Yes             | Top N (with ties)    |
| **DENSE_RANK()** | Yes (same rank)     | No              | Top N distinct values|

---

## 💡 Mental Model

**Think of PARTITION BY as creating mini-tables:**

```
Original Table:
Gaming: Alice, Bob, Charlie
Music: Eve, Frank, Grace

PARTITION BY category creates:

Mini-Table 1 (Gaming):
  Alice   → Rank 1
  Bob     → Rank 2
  Charlie → Rank 3

Mini-Table 2 (Music):
  Eve   → Rank 1
  Frank → Rank 2
  Grace → Rank 3
```

Then the results are combined back into one table.
