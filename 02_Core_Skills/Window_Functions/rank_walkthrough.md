# Step-by-Step Walkthrough: RANK() and ROW_NUMBER() with Two CTEs

## Problem: Find the Top 2 Salespeople in Each Department

This walkthrough explains **why** we use each step, not just **what** the code does.

---

## The Complete Query

```sql
WITH ranked_employees AS (
    SELECT
        employee_name,
        department,
        sales_amount,
        RANK() OVER (PARTITION BY department ORDER BY sales_amount DESC) AS dept_rank
    FROM employee_sales
)
SELECT
    department,
    employee_name,
    sales_amount,
    dept_rank
FROM ranked_employees
WHERE dept_rank <= 2
ORDER BY department, dept_rank;
```

---

## Step-by-Step Breakdown

### **Step 1: Understanding the Problem**

**Question:** "Find the top 2 salespeople in each department"

**Key words:**
- **"top 2"** → We need ranking
- **"in each department"** → We need separate rankings per department (PARTITION BY)

**Why we can't do this in one query:**
- We need to calculate the rank FIRST
- Then filter based on that rank
- SQL doesn't let you filter on a window function in the WHERE clause directly

---

### **Step 2: CTE #1 - Calculate Rankings**

```sql
WITH ranked_employees AS (
    SELECT
        employee_name,
        department,
        sales_amount,
        RANK() OVER (PARTITION BY department ORDER BY sales_amount DESC) AS dept_rank
    FROM employee_sales
)
```

**Purpose:** Create a temporary table with rankings added

**Why this step?**
- We need to ADD a new column (`dept_rank`) to our data
- This column doesn't exist in the original table
- We'll use this rank to filter in the next step

**Breaking down the RANK() function:**

```sql
RANK() OVER (
    PARTITION BY department    -- ← Separate rankings for each department
    ORDER BY sales_amount DESC -- ← Highest sales = rank 1
)
```

**What PARTITION BY does:**
- Creates separate "buckets" for each department
- Ranking resets to 1 for each new department
- Without it, we'd get one overall ranking across all departments

**What this CTE produces:**

| employee_name | department | sales_amount | dept_rank |
|---------------|------------|--------------|-----------|
| Diana | Sales | 9000 | 1 |
| Bob | Sales | 7000 | 2 |
| Charlie | Sales | 7000 | 2 |
| Eve | Sales | 6000 | 4 |
| Alice | Sales | 5000 | 5 |
| Henry | Engineering | 10000 | 1 |
| Frank | Engineering | 8000 | 2 |
| Grace | Engineering | 8000 | 2 |
| Iris | Engineering | 5500 | 4 |

**Key observation:** Notice how the rank resets to 1 for Engineering!

---

### **Step 3: Final SELECT - Filter to Top 2**

```sql
SELECT
    department,
    employee_name,
    sales_amount,
    dept_rank
FROM ranked_employees
WHERE dept_rank <= 2
ORDER BY department, dept_rank;
```

**Purpose:** Filter to keep only ranks 1 and 2 from each department

**Why we need a separate step:**
- We can't use `WHERE RANK() OVER (...) <= 2` directly
- SQL evaluates WHERE before window functions
- So we calculate the rank in CTE #1, then filter in the final SELECT

**What the WHERE clause does:**
- `dept_rank <= 2` keeps only rows where rank is 1 or 2
- This happens AFTER the ranking is calculated
- We get the top 2 from EACH department (because PARTITION BY created separate rankings)

**Final Result:**

| department | employee_name | sales_amount | dept_rank |
|------------|---------------|--------------|-----------|
| Engineering | Henry | 10000 | 1 |
| Engineering | Frank | 8000 | 2 |
| Engineering | Grace | 8000 | 2 |
| Sales | Diana | 9000 | 1 |
| Sales | Bob | 7000 | 2 |
| Sales | Charlie | 7000 | 2 |

---

## Why We Use a CTE Instead of a Subquery

**Option 1: CTE (What we used)**
```sql
WITH ranked_employees AS (...)
SELECT ... FROM ranked_employees WHERE dept_rank <= 2;
```
✅ **Readable** - Clear separation of steps
✅ **Debuggable** - Can run `SELECT * FROM ranked_employees` to verify
✅ **Maintainable** - Easy to modify

**Option 2: Subquery (Alternative)**
```sql
SELECT ... FROM (
    SELECT ..., RANK() OVER (...) AS dept_rank
    FROM employee_sales
) AS ranked_employees
WHERE dept_rank <= 2;
```
❌ **Harder to read** - Everything nested
❌ **Harder to debug** - Can't easily test the inner query
✅ **Works the same** - Functionally identical

---

## Common Questions

### Q: Why can't we just use WHERE in the CTE?

**Wrong:**
```sql
WITH ranked_employees AS (
    SELECT ..., RANK() OVER (...) AS dept_rank
    FROM employee_sales
    WHERE dept_rank <= 2  -- ❌ ERROR!
)
```

**Answer:** The WHERE clause runs BEFORE the SELECT, so `dept_rank` doesn't exist yet!

**Order of execution:**
1. FROM
2. WHERE ← Happens here
3. GROUP BY
4. SELECT ← dept_rank is created here
5. Window functions (RANK)

---

### Q: Why use RANK() instead of ROW_NUMBER()?

**RANK():**
- Bob and Charlie both have $7000 → Both get rank 2
- Result: We get 3 people (Diana, Bob, Charlie)

**ROW_NUMBER():**
- Bob gets 2, Charlie gets 3 (arbitrary order)
- Result: We get exactly 2 people (Diana, Bob)

**Use RANK() when:** You want to honor ties
**Use ROW_NUMBER() when:** You want exactly N results

---

## Practice: Modify the Query

### Exercise 1: Find the top 1 in each department
**Change:** `WHERE dept_rank <= 2` → `WHERE dept_rank = 1`

### Exercise 2: Find the bottom 2 in each department
**Change:** `ORDER BY sales_amount DESC` → `ORDER BY sales_amount ASC`

### Exercise 3: Use ROW_NUMBER() to get exactly 2 per department
**Change:** `RANK()` → `ROW_NUMBER()`

---

## Key Takeaways

1. **PARTITION BY** creates separate groups for ranking
2. **CTE** lets us calculate the rank first, then filter on it
3. **RANK()** honors ties, **ROW_NUMBER()** doesn't
4. **Window functions** can't be used directly in WHERE
5. **Two-step process:** Calculate rank → Filter by rank
