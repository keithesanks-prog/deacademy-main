# Walmart Loyal Customers - Subqueries Explained Simply

## What's This Query Really Doing?

**The Question in Plain English:**
"Find customers who BOTH spent a lot AND left good reviews"

Think of it like finding people who are:
- Rich (spent > $1500) **AND**
- Popular (left 5+ reviews with 4+ stars)

---

## The Two Groups

### Group 1: Big Spenders

**Question:** "Who spent more than $1500 in 2023?"

```sql
SELECT customer_id, SUM(total_amount) AS total_spent
FROM walmart_orders
WHERE YEAR(order_date) = 2023
GROUP BY customer_id
HAVING SUM(total_amount) > 1500;
```

**Result:**
```
customer_id | total_spent
------------|------------
101         | 2500
102         | 1800
105         | 3200
```

**In plain English:** "Alice spent $2500, Bob spent $1800, Emma spent $3200"

---

### Group 2: Active Reviewers

**Question:** "Who left 5+ reviews with 4+ star average in 2023?"

```sql
SELECT customer_id, AVG(rating) AS avg_rating, COUNT(review_id) AS review_count
FROM walmart_reviews
WHERE YEAR(review_date) = 2023
GROUP BY customer_id
HAVING AVG(rating) >= 4 AND COUNT(review_id) >= 5;
```

**Result:**
```
customer_id | avg_rating | review_count
------------|------------|-------------
101         | 4.5        | 8
103         | 4.2        | 6
105         | 4.8        | 12
```

**In plain English:** "Alice left 8 reviews (4.5 stars), Carol left 6 reviews (4.2 stars), Emma left 12 reviews (4.8 stars)"

---

## Finding People in BOTH Groups

**Now the key question:** "Who is in BOTH lists?"

Looking at our results:
- **Group 1 (Big Spenders):** Alice (101), Bob (102), Emma (105)
- **Group 2 (Active Reviewers):** Alice (101), Carol (103), Emma (105)

**Who's in BOTH?**
- Alice (101) ✅ - In both lists!
- Bob (102) ❌ - Only in Group 1
- Carol (103) ❌ - Only in Group 2
- Emma (105) ✅ - In both lists!

**Answer: Alice and Emma**

---

## The CTE Way (What the Guide Shows)

**CTE = Common Table Expression = Fancy name for "temporary named result"**

Think of CTEs like **giving your subqueries names** so you can reuse them:

```sql
WITH Spenders AS (
    -- This is just Group 1's query with a name!
    SELECT customer_id, SUM(total_amount) AS total_spent
    FROM walmart_orders
    WHERE YEAR(order_date) = 2023
    GROUP BY customer_id
    HAVING SUM(total_amount) > 1500
),
Reviewers AS (
    -- This is just Group 2's query with a name!
    SELECT customer_id, AVG(rating) AS avg_rating, COUNT(review_id) AS review_count
    FROM walmart_reviews
    WHERE YEAR(review_date) = 2023
    GROUP BY customer_id
    HAVING AVG(rating) >= 4 AND COUNT(review_id) >= 5
)
-- Now use those names!
SELECT 
    wc.customer_name,
    s.total_spent,
    r.avg_rating,
    r.review_count
FROM Spenders s
JOIN Reviewers r ON s.customer_id = r.customer_id
JOIN walmart_customers wc ON wc.customer_id = s.customer_id;
```

---

## Breaking Down the CTE

### Part 1: Create "Spenders" Table

```sql
WITH Spenders AS (
    SELECT customer_id, SUM(total_amount) AS total_spent
    FROM walmart_orders
    WHERE YEAR(order_date) = 2023
    GROUP BY customer_id
    HAVING SUM(total_amount) > 1500
)
```

**What this does:** Creates a temporary table called `Spenders` with high-spending customers

**Think of it like:**
```
Spenders = [Alice, Bob, Emma]
```

---

### Part 2: Create "Reviewers" Table

```sql
Reviewers AS (
    SELECT customer_id, AVG(rating) AS avg_rating, COUNT(review_id) AS review_count
    FROM walmart_reviews
    WHERE YEAR(review_date) = 2023
    GROUP BY customer_id
    HAVING AVG(rating) >= 4 AND COUNT(review_id) >= 5
)
```

**What this does:** Creates a temporary table called `Reviewers` with active reviewers

**Think of it like:**
```
Reviewers = [Alice, Carol, Emma]
```

---

### Part 3: Find the Overlap (JOIN)

```sql
SELECT ...
FROM Spenders s
JOIN Reviewers r ON s.customer_id = r.customer_id
```

**What this does:** Only keeps customers who are in BOTH tables

**Visual:**
```
Spenders:  [Alice, Bob, Emma]
              ↓      ↓     ↓
Reviewers: [Alice, Carol, Emma]
              ↓             ↓
              ↓             ↓
Result:    [Alice,       Emma]  ← Only these two are in BOTH!
```

---

## Why Use CTEs Instead of Subqueries?

### Without CTEs (Messy Subquery Version):

```sql
SELECT 
    wc.customer_name,
    spenders.total_spent,
    reviewers.avg_rating,
    reviewers.review_count
FROM (
    -- Subquery 1: Spenders
    SELECT customer_id, SUM(total_amount) AS total_spent
    FROM walmart_orders
    WHERE YEAR(order_date) = 2023
    GROUP BY customer_id
    HAVING SUM(total_amount) > 1500
) AS spenders
JOIN (
    -- Subquery 2: Reviewers
    SELECT customer_id, AVG(rating) AS avg_rating, COUNT(review_id) AS review_count
    FROM walmart_reviews
    WHERE YEAR(review_date) = 2023
    GROUP BY customer_id
    HAVING AVG(rating) >= 4 AND COUNT(review_id) >= 5
) AS reviewers ON spenders.customer_id = reviewers.customer_id
JOIN walmart_customers wc ON wc.customer_id = spenders.customer_id;
```

**Problem:** Hard to read! Everything is nested and jumbled.

---

### With CTEs (Clean Version):

```sql
WITH Spenders AS (...),
     Reviewers AS (...)
SELECT ...
FROM Spenders s
JOIN Reviewers r ON s.customer_id = r.customer_id
```

**Benefit:** Each piece has a clear name and purpose!

---

## Step-by-Step: How to Build This

### Step 1: Test Group 1 Alone

```sql
SELECT customer_id, SUM(total_amount) AS total_spent
FROM walmart_orders
WHERE YEAR(order_date) = 2023
GROUP BY customer_id
HAVING SUM(total_amount) > 1500;
```

**Run this first!** Make sure it returns the right customers.

---

### Step 2: Test Group 2 Alone

```sql
SELECT customer_id, AVG(rating) AS avg_rating, COUNT(review_id) AS review_count
FROM walmart_reviews
WHERE YEAR(review_date) = 2023
GROUP BY customer_id
HAVING AVG(rating) >= 4 AND COUNT(review_id) >= 5;
```

**Run this second!** Make sure it returns the right customers.

---

### Step 3: Wrap Them in CTEs

```sql
WITH Spenders AS (
    -- Copy Step 1's query here
),
Reviewers AS (
    -- Copy Step 2's query here
)
SELECT * FROM Spenders;  -- Test that CTE works
```

---

### Step 4: JOIN Them

```sql
WITH Spenders AS (...),
     Reviewers AS (...)
SELECT 
    s.customer_id,
    s.total_spent,
    r.avg_rating,
    r.review_count
FROM Spenders s
JOIN Reviewers r ON s.customer_id = r.customer_id;
```

---

### Step 5: Add Customer Names

```sql
WITH Spenders AS (...),
     Reviewers AS (...)
SELECT 
    wc.customer_name,  -- Add names
    s.total_spent,
    r.avg_rating,
    r.review_count
FROM Spenders s
JOIN Reviewers r ON s.customer_id = r.customer_id
JOIN walmart_customers wc ON wc.customer_id = s.customer_id;  -- Join for names
```

---

## Key Concepts

### WHERE vs HAVING

```sql
-- ❌ WRONG: Can't use SUM in WHERE
WHERE SUM(total_amount) > 1500

-- ✅ CORRECT: Use HAVING for aggregates
GROUP BY customer_id
HAVING SUM(total_amount) > 1500
```

**Rule:**
- `WHERE` filters rows BEFORE grouping
- `HAVING` filters groups AFTER aggregating

---

### GROUP BY Requirement

```sql
-- ❌ WRONG: Using SUM without GROUP BY
SELECT customer_id, SUM(total_amount)
FROM walmart_orders;

-- ✅ CORRECT: GROUP BY when using aggregates
SELECT customer_id, SUM(total_amount)
FROM walmart_orders
GROUP BY customer_id;
```

**Rule:** If you use `SUM()`, `AVG()`, `COUNT()`, you need `GROUP BY`

---

### YEAR() Function

```sql
WHERE YEAR(order_date) = 2023
```

**What it does:** Extracts the year from a date

**Example:**
- `YEAR('2023-05-15')` → 2023
- `YEAR('2022-12-31')` → 2022

---

## The Bottom Line

**CTEs are just named subqueries that make your code easier to read!**

**Instead of:**
```sql
SELECT ... FROM (big messy subquery) AS temp
```

**You write:**
```sql
WITH temp AS (big messy subquery)
SELECT ... FROM temp
```

**Same thing, cleaner code!**

---

## Practice: Break It Down

When you see a CTE query:

1. **Run each CTE separately** - Test them one at a time
2. **Check the results** - Do they make sense?
3. **Understand the JOIN** - How are they connected?
4. **Read the final SELECT** - What's the output?

**You've got this!** CTEs are just a cleaner way to write what you already know. 🚀
