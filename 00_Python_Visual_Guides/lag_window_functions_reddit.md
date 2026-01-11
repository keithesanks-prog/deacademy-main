# 🎯 LAG & Window Functions: Reddit Publisher Analysis

## 📋 Problem Statement

**Find the number of publishers that have at least 3 posts where every two consecutive posts are separated by at least one week (7+ days).**

### Tables:
```sql
fact_reddit
- publisher_id
- creation_date
- (other columns...)
```

### Expected Output:
```
number_of_publishers
```

---

## 🧠 Conceptual Breakdown

### What Are We Looking For?

A publisher qualifies if they have:
1. **At least 3 posts** total
2. **At least 2 gaps** of 7+ days between consecutive posts

**Visual Example:**

```
Publisher 101:
Post 1: Jan 1
Post 2: Jan 10  ← Gap: 9 days ✅
Post 3: Jan 20  ← Gap: 10 days ✅
Post 4: Jan 22  ← Gap: 2 days (doesn't matter, we already have 2 gaps)

Result: QUALIFIES ✅ (3+ posts, 2+ gaps of 7+ days)

Publisher 102:
Post 1: Jan 1
Post 2: Jan 3   ← Gap: 2 days ❌
Post 3: Jan 10  ← Gap: 7 days ✅
Post 4: Jan 12  ← Gap: 2 days ❌

Result: DOESN'T QUALIFY ❌ (3+ posts, but only 1 gap of 7+ days)
```

---

## 🔍 Step-by-Step Solution

### **Step 1: Calculate Days Between Posts (LAG)**

We use `LAG()` to look at the **previous post** for each publisher.

```sql
WITH posts_with_gaps AS (
    SELECT
        publisher_id,
        creation_date,
        LAG(creation_date) OVER (
            PARTITION BY publisher_id 
            ORDER BY creation_date
        ) AS previous_post_date,
        DATEDIFF(
            creation_date, 
            LAG(creation_date) OVER (PARTITION BY publisher_id ORDER BY creation_date)
        ) AS days_between_posts
    FROM fact_reddit
)
```

**What This Does:**
- `PARTITION BY publisher_id` - Separate window for each publisher
- `ORDER BY creation_date` - Look at posts chronologically
- `LAG(creation_date)` - Get the previous post's date
- `DATEDIFF(...)` - Calculate days between current and previous post

**Sample Output:**

| publisher_id | creation_date | previous_post_date | days_between_posts |
|--------------|---------------|--------------------|--------------------|
| 101 | 2024-01-01 | NULL | NULL (first post) |
| 101 | 2024-01-10 | 2024-01-01 | 9 |
| 101 | 2024-01-20 | 2024-01-10 | 10 |
| 102 | 2024-01-01 | NULL | NULL |
| 102 | 2024-01-03 | 2024-01-01 | 2 |

---

### **Step 2: Count Posts and Qualifying Gaps**

Now we count:
- Total posts per publisher
- How many gaps are 7+ days

```sql
publisher_gap_check AS (
    SELECT
        publisher_id,
        COUNT(*) AS total_posts,
        COUNT(CASE WHEN days_between_posts >= 7 THEN 1 END) AS gaps_of_7plus_days
    FROM posts_with_gaps
    GROUP BY publisher_id
)
```

**Key Insight:**
```sql
COUNT(CASE WHEN days_between_posts >= 7 THEN 1 END)
```

This counts **only** the rows where the gap is 7+ days. The `CASE` returns `1` for qualifying gaps, and `NULL` for others. `COUNT()` ignores NULLs!

**Sample Output:**

| publisher_id | total_posts | gaps_of_7plus_days |
|--------------|-------------|--------------------|
| 101 | 4 | 2 |
| 102 | 4 | 1 |
| 103 | 2 | 0 |

---

### **Step 3: Filter and Count**

Finally, count publishers meeting **both** criteria:

```sql
SELECT
    COUNT(*) AS number_of_publishers
FROM publisher_gap_check
WHERE total_posts >= 3
  AND gaps_of_7plus_days >= 2
```

**Why `gaps_of_7plus_days >= 2`?**
- If you have 3 posts, there are 2 gaps between them
- Both gaps must be 7+ days
- So we need at least 2 qualifying gaps

---

## 🎯 Complete Solution

```sql
WITH posts_with_gaps AS (
    SELECT
        publisher_id,
        creation_date,
        DATEDIFF(
            creation_date, 
            LAG(creation_date) OVER (PARTITION BY publisher_id ORDER BY creation_date)
        ) AS days_between_posts
    FROM fact_reddit
),
publisher_gap_check AS (
    SELECT
        publisher_id,
        COUNT(*) AS total_posts,
        COUNT(CASE WHEN days_between_posts >= 7 THEN 1 END) AS gaps_of_7plus_days
    FROM posts_with_gaps
    GROUP BY publisher_id
)
SELECT
    COUNT(*) AS number_of_publishers
FROM publisher_gap_check
WHERE total_posts >= 3
  AND gaps_of_7plus_days >= 2;
```

---

## 🧪 Test Data Example

Let's trace through with sample data:

### Sample Posts:
```
Publisher 1:
- 2024-01-01
- 2024-01-10 (9 days later)
- 2024-01-20 (10 days later)

Publisher 2:
- 2024-01-01
- 2024-01-03 (2 days later)
- 2024-01-10 (7 days later)
- 2024-01-12 (2 days later)

Publisher 3:
- 2024-01-01
- 2024-01-02 (1 day later)
```

### After CTE 1 (posts_with_gaps):
```
pub_id | creation_date | days_between_posts
1      | 2024-01-01   | NULL
1      | 2024-01-10   | 9
1      | 2024-01-20   | 10
2      | 2024-01-01   | NULL
2      | 2024-01-03   | 2
2      | 2024-01-10   | 7
2      | 2024-01-12   | 2
3      | 2024-01-01   | NULL
3      | 2024-01-02   | 1
```

### After CTE 2 (publisher_gap_check):
```
pub_id | total_posts | gaps_of_7plus_days
1      | 3           | 2  ✅
2      | 4           | 1  ❌
3      | 2           | 0  ❌
```

### Final Result:
```
number_of_publishers
1
```

Only Publisher 1 qualifies!

---

## 💡 Key Concepts Explained

### **1. LAG() Window Function**

```sql
LAG(column) OVER (PARTITION BY ... ORDER BY ...)
```

- **What it does**: Looks at the **previous row** in the window
- **Returns**: The value from the previous row, or NULL for the first row
- **Alternative**: `LEAD()` looks at the **next row**

### **2. PARTITION BY**

```sql
PARTITION BY publisher_id
```

- Creates **separate windows** for each publisher
- LAG() only looks at posts from the **same publisher**
- Without it, you'd compare posts across different publishers!

### **3. Conditional Counting**

```sql
COUNT(CASE WHEN condition THEN 1 END)
```

- Counts **only** rows meeting the condition
- Returns `1` for matches, `NULL` for non-matches
- `COUNT()` ignores NULLs, so only matches are counted

### **4. Why >= 2 Gaps for 3 Posts?**

```
Post 1 → [Gap 1] → Post 2 → [Gap 2] → Post 3

3 posts = 2 gaps
4 posts = 3 gaps
n posts = n-1 gaps
```

---

## 🎨 Visual Diagram

```
Timeline View:

Publisher 1 (QUALIFIES ✅):
|-------|---------|---------|
Post1   Post2     Post3     Post4
  ↓       ↓         ↓         ↓
Jan 1   Jan 10    Jan 20    Jan 22
        [9 days]  [10 days] [2 days]
           ✅         ✅        -

Total: 4 posts, 2 qualifying gaps → PASS


Publisher 2 (DOESN'T QUALIFY ❌):
|--|-------|--|
P1  P2      P3 P4
 ↓   ↓       ↓  ↓
J1  J3     J10 J12
   [2d]    [7d] [2d]
    ❌      ✅   ❌

Total: 4 posts, 1 qualifying gap → FAIL
```

---

## 🚀 Practice Variations

### **Variation 1: Show Publisher Details**
```sql
-- Instead of just counting, show which publishers qualify
SELECT
    publisher_id,
    total_posts,
    gaps_of_7plus_days
FROM publisher_gap_check
WHERE total_posts >= 3
  AND gaps_of_7plus_days >= 2
ORDER BY gaps_of_7plus_days DESC;
```

### **Variation 2: Different Time Threshold**
```sql
-- Find publishers with 4+ posts, all gaps >= 14 days
WHERE total_posts >= 4
  AND gaps_of_7plus_days >= 3  -- n posts = n-1 gaps
  AND gaps_of_7plus_days = total_posts - 1  -- ALL gaps must be 7+ days
```

### **Variation 3: Show the Actual Gaps**
```sql
-- See the gaps for a specific publisher
SELECT
    publisher_id,
    creation_date,
    days_between_posts,
    CASE 
        WHEN days_between_posts >= 7 THEN 'Qualifies ✅'
        WHEN days_between_posts IS NULL THEN 'First Post'
        ELSE 'Too Soon ❌'
    END AS gap_status
FROM posts_with_gaps
WHERE publisher_id = 101
ORDER BY creation_date;
```

---

## ✅ Common Mistakes to Avoid

### ❌ Mistake 1: Forgetting PARTITION BY
```sql
-- WRONG:
LAG(creation_date) OVER (ORDER BY creation_date)
-- This compares across ALL publishers!
```

### ❌ Mistake 2: Wrong Gap Count Logic
```sql
-- WRONG:
WHERE total_posts >= 3 AND gaps_of_7plus_days >= 3
-- 3 posts only have 2 gaps!
```

### ❌ Mistake 3: Using SUM Instead of COUNT
```sql
-- WRONG:
SUM(CASE WHEN days_between_posts >= 7 THEN 1 ELSE 0 END)
-- This works, but COUNT is cleaner and ignores NULLs automatically
```

### ❌ Mistake 4: Not Handling NULL
```sql
-- The first post always has NULL for days_between_posts
-- COUNT(CASE WHEN ...) automatically ignores it ✅
```

---

## 🎓 Learning Objectives

After mastering this problem, you should understand:

1. ✅ How `LAG()` compares current row to previous row
2. ✅ Why `PARTITION BY` is crucial for grouping
3. ✅ How to count conditionally with `CASE`
4. ✅ The relationship between posts and gaps (n posts = n-1 gaps)
5. ✅ How to chain CTEs for complex logic
6. ✅ Date difference calculations with `DATEDIFF()`

---

## 🔗 Related Concepts

- **LAG/LEAD**: Time series analysis, growth calculations
- **PARTITION BY**: Group-wise operations
- **CTEs**: Breaking complex queries into steps
- **Conditional Aggregation**: Flexible counting/summing
- **Window Functions**: Running totals, rankings, comparisons

---

## 📝 Practice Exercise

**Try this variation:**

Find publishers who have **exactly 5 posts** where **all consecutive gaps** are at least 7 days.

<details>
<summary>Click to see solution</summary>

```sql
WITH posts_with_gaps AS (
    SELECT
        publisher_id,
        creation_date,
        DATEDIFF(
            creation_date, 
            LAG(creation_date) OVER (PARTITION BY publisher_id ORDER BY creation_date)
        ) AS days_between_posts
    FROM fact_reddit
),
publisher_gap_check AS (
    SELECT
        publisher_id,
        COUNT(*) AS total_posts,
        COUNT(CASE WHEN days_between_posts >= 7 THEN 1 END) AS gaps_of_7plus_days
    FROM posts_with_gaps
    GROUP BY publisher_id
)
SELECT
    COUNT(*) AS number_of_publishers
FROM publisher_gap_check
WHERE total_posts = 5  -- Exactly 5 posts
  AND gaps_of_7plus_days = 4;  -- All 4 gaps must be 7+ days
```

</details>

---

Now you have a complete understanding of this powerful pattern! 🚀
