# 🛒 Walmart Loyal Customers: Complete Problem Breakdown

**Learn to solve multi-criteria problems using CTEs**

---

## 📋 The Problem

**Background:**
Walmart wants to identify loyal customers who show strong engagement and high spending behavior. The marketing team plans to reward customers who:

1. Spent over $1500 in 2023
2. Left 5 or more product reviews in 2023 with an average rating of at least 4

**Question:**
Find customers who meet **both** criteria.

**Output:** customer_name, total_spent, avg_rating, review_count

---

## 🔍 Step 1: Parse the Question

### **Signal Words**

**"meet both criteria"** → Need customers in BOTH groups (use JOIN)

**Criteria 1: "Spent over $1500 in 2023"**
- "Spent" → `SUM(order_amount)`
- "over $1500" → `> 1500`
- "in 2023" → `YEAR(order_date) = 2023`

**Criteria 2: "5 or more reviews... avg rating of at least 4"**
- "5 or more reviews" → `COUNT(review_id) >= 5`
- "avg rating of at least 4" → `AVG(rating) >= 4`
- "in 2023" → `YEAR(review_date) = 2023`

---

## 🎯 Step 2: Break Into Logical Parts

**This is a perfect CTE problem because:**
- Two separate criteria
- Each needs different aggregations
- Need customers who meet BOTH

**Strategy:**
1. **CTE 1:** Find high spenders (> $1500)
2. **CTE 2:** Find active reviewers (>= 5 reviews, avg >= 4)
3. **JOIN:** Only customers in BOTH CTEs

---

## 🔨 Step 3: Build CTE 1 (Spenders)

**Goal:** Find customers who spent > $1500 in 2023

```sql
WITH Spender AS (
    SELECT
        customer_id,
        SUM(total_amount) AS total_spent
    FROM walmart_orders
    WHERE YEAR(order_date) = 2023
    GROUP BY customer_id
    HAVING SUM(total_amount) > 1500
)
```

**Breakdown:**
- `WHERE YEAR(order_date) = 2023` → Filter to 2023 orders
- `GROUP BY customer_id` → Aggregate per customer
- `SUM(total_amount)` → Calculate total spent
- `HAVING SUM(...) > 1500` → Filter to high spenders

**Sample Result:**
| customer_id | total_spent |
|-------------|-------------|
| 101 | 2500.00 |
| 102 | 1800.00 |
| 105 | 3200.00 |

---

## 🔨 Step 4: Build CTE 2 (Reviewers)

**Goal:** Find customers with >= 5 reviews and avg rating >= 4 in 2023

```sql
Reviews AS (
    SELECT
        customer_id,
        AVG(rating) AS avg_rating,
        COUNT(review_id) AS review_count
    FROM walmart_reviews
    WHERE YEAR(review_date) = 2023
    GROUP BY customer_id
    HAVING AVG(rating) >= 4
      AND COUNT(review_id) >= 5
)
```

**Breakdown:**
- `WHERE YEAR(review_date) = 2023` → Filter to 2023 reviews
- `GROUP BY customer_id` → Aggregate per customer
- `AVG(rating)` → Calculate average rating
- `COUNT(review_id)` → Count reviews
- `HAVING AVG(...) >= 4 AND COUNT(...) >= 5` → Filter to active reviewers

**Sample Result:**
| customer_id | avg_rating | review_count |
|-------------|------------|--------------|
| 101 | 4.5 | 8 |
| 103 | 4.2 | 6 |
| 105 | 4.8 | 12 |

---

## 🔗 Step 5: JOIN the CTEs

**Goal:** Get customers who are in BOTH CTEs

```sql
SELECT
    wc.customer_name,
    s.total_spent,
    r.avg_rating,
    r.review_count
FROM Spender s
JOIN Reviews r ON s.customer_id = r.customer_id
JOIN walmart_customers wc ON wc.customer_id = s.customer_id
ORDER BY s.total_spent DESC;
```

**Breakdown:**
- `FROM Spender s` → Start with high spenders
- `JOIN Reviews r` → Only keep those who are also active reviewers
- `JOIN walmart_customers wc` → Get customer names
- `ORDER BY s.total_spent DESC` → Show highest spenders first

---

## 📊 Visual Execution

**Spender CTE:**
```
┌─────────────┬─────────────┐
│ customer_id │ total_spent │
├─────────────┼─────────────┤
│ 101         │ 2500        │
│ 102         │ 1800        │
│ 105         │ 3200        │
└─────────────┴─────────────┘
```

**Reviews CTE:**
```
┌─────────────┬────────────┬──────────────┐
│ customer_id │ avg_rating │ review_count │
├─────────────┼────────────┼──────────────┤
│ 101         │ 4.5        │ 8            │
│ 103         │ 4.2        │ 6            │
│ 105         │ 4.8        │ 12           │
└─────────────┴────────────┴──────────────┘
```

**After JOIN (only customers in BOTH):**
```
┌─────────────┬─────────────┬────────────┬──────────────┐
│ customer_id │ total_spent │ avg_rating │ review_count │
├─────────────┼─────────────┼────────────┼──────────────┤
│ 101         │ 2500        │ 4.5        │ 8            │
│ 105         │ 3200        │ 4.8        │ 12           │
└─────────────┴─────────────┴────────────┴──────────────┘
```

**Notice:** Customer 102 (only in Spender) and 103 (only in Reviews) are excluded!

---

## ✅ Complete Query

```sql
WITH Spender AS (
    SELECT
        customer_id,
        SUM(total_amount) AS total_spent
    FROM walmart_orders
    WHERE YEAR(order_date) = 2023
    GROUP BY customer_id
    HAVING SUM(total_amount) > 1500
),
Reviews AS (
    SELECT
        customer_id,
        AVG(rating) AS avg_rating,
        COUNT(review_id) AS review_count
    FROM walmart_reviews
    WHERE YEAR(review_date) = 2023
    GROUP BY customer_id
    HAVING AVG(rating) >= 4
      AND COUNT(review_id) >= 5
)
SELECT
    wc.customer_name,
    s.total_spent,
    r.avg_rating,
    r.review_count
FROM Spender s
JOIN Reviews r ON s.customer_id = r.customer_id
JOIN walmart_customers wc ON wc.customer_id = s.customer_id
ORDER BY s.total_spent DESC;
```

---

## 💡 Why Use CTEs for This?

### **Advantages:**
1. ✅ **Readable** - Each CTE has a clear purpose
2. ✅ **Testable** - Run each CTE separately to debug
3. ✅ **Maintainable** - Easy to modify criteria
4. ✅ **Logical** - Mirrors the problem structure

### **Alternative (One Big Query):**
```sql
-- ❌ Harder to read
SELECT ...
FROM walmart_customers c
JOIN walmart_orders o ON ...
JOIN walmart_reviews r ON ...
WHERE YEAR(o.order_date) = 2023 AND YEAR(r.review_date) = 2023
GROUP BY ...
HAVING SUM(...) > 1500 AND AVG(...) >= 4 AND COUNT(...) >= 5
```

**Problem:** Mixes orders and reviews in one GROUP BY (can cause issues!)

---

## 🎯 Key Takeaways

1. **"meet both criteria"** → Use CTEs + JOIN
2. **Each CTE handles one criterion** independently
3. **JOIN ensures** customers are in BOTH groups
4. **HAVING filters aggregates** (SUM, AVG, COUNT)
5. **Test each CTE separately** before joining

---

## 🚀 Practice Problem

**Problem:** Find products that:
1. Sold more than 100 units in 2023
2. Have at least 10 reviews with avg rating >= 4.5

**Tables:** products, sales, product_reviews

<details>
<summary>Click for solution</summary>

```sql
WITH HighSales AS (
    SELECT
        product_id,
        SUM(quantity) AS total_sold
    FROM sales
    WHERE YEAR(sale_date) = 2023
    GROUP BY product_id
    HAVING SUM(quantity) > 100
),
HighRated AS (
    SELECT
        product_id,
        AVG(rating) AS avg_rating,
        COUNT(review_id) AS review_count
    FROM product_reviews
    GROUP BY product_id
    HAVING AVG(rating) >= 4.5
      AND COUNT(review_id) >= 10
)
SELECT
    p.product_name,
    hs.total_sold,
    hr.avg_rating,
    hr.review_count
FROM HighSales hs
JOIN HighRated hr ON hs.product_id = hr.product_id
JOIN products p ON p.product_id = hs.product_id
ORDER BY hs.total_sold DESC;
```

</details>
