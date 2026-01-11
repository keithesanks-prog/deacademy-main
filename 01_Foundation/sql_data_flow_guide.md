# 🌊 SQL Data Flow: The Complete Picture

**How data moves through a SQL query**

---

## 🎯 The Execution Order (Not What You Write!)

**What you write:**
```sql
SELECT column
FROM table
WHERE condition
GROUP BY column
HAVING condition
ORDER BY column
```

**What the database executes:**
```
1. FROM        → Get the raw data
2. WHERE       → Filter rows (before grouping)
3. GROUP BY    → Create groups
4. HAVING      → Filter groups (after aggregation)
5. SELECT      → Pick columns
6. ORDER BY    → Sort results
```

---

## 🔍 Visual Flow: Step-by-Step

### **Starting Data**
| customer_id | order_amount | order_date |
|-------------|--------------|------------|
| 1 | 100 | 2023-01-15 |
| 1 | 200 | 2023-02-20 |
| 2 | 50 | 2023-01-10 |
| 2 | 150 | 2023-03-05 |
| 3 | 300 | 2023-01-25 |

---

### **Step 1: FROM**
**Query:** `FROM orders`

**Action:** Load the table into memory.

**Result:** (Same as above - all 5 rows)

---

### **Step 2: WHERE**
**Query:** `WHERE order_amount > 75`

**Action:** Filter **individual rows** (no aggregation yet).

**Result:**
| customer_id | order_amount | order_date |
|-------------|--------------|------------|
| 1 | 100 | 2023-01-15 |
| 1 | 200 | 2023-02-20 |
| 2 | 150 | 2023-03-05 |
| 3 | 300 | 2023-01-25 |

**Removed:** Customer 2's $50 order (too small).

---

### **Step 3: GROUP BY**
**Query:** `GROUP BY customer_id`

**Action:** Collapse rows into groups.

**Result:**
| customer_id | orders_in_group |
|-------------|-----------------|
| 1 | [100, 200] |
| 2 | [150] |
| 3 | [300] |

**Notice:** We went from 4 rows → 3 groups.

---

### **Step 4: HAVING**
**Query:** `HAVING SUM(order_amount) > 200`

**Action:** Filter **groups** based on aggregated values.

**Calculation:**
- Customer 1: `100 + 200 = 300` ✅ (Keep)
- Customer 2: `150` ❌ (Remove)
- Customer 3: `300` ✅ (Keep)

**Result:**
| customer_id | total_amount |
|-------------|--------------|
| 1 | 300 |
| 3 | 300 |

---

### **Step 5: SELECT**
**Query:** `SELECT customer_id, SUM(order_amount) AS total`

**Action:** Pick which columns to show.

**Result:**
| customer_id | total |
|-------------|-------|
| 1 | 300 |
| 3 | 300 |

---

### **Step 6: ORDER BY**
**Query:** `ORDER BY total DESC`

**Action:** Sort the final results.

**Result:**
| customer_id | total |
|-------------|-------|
| 1 | 300 |
| 3 | 300 |

*(No change here since they're tied)*

---

## 🔗 CTEs: The Pipeline

**CTEs let you chain transformations like Unix pipes.**

```sql
WITH step1 AS (
    SELECT customer_id, SUM(order_amount) AS total
    FROM orders
    WHERE order_amount > 75
    GROUP BY customer_id
),
step2 AS (
    SELECT customer_id, total, total * 0.1 AS reward_points
    FROM step1
    WHERE total > 200
)
SELECT * FROM step2 ORDER BY reward_points DESC;
```

**Visual Flow:**
```
Raw Data (orders)
    ↓
[CTE: step1]
  FROM orders
  WHERE order_amount > 75
  GROUP BY customer_id
    ↓
Intermediate Result (customer totals)
    ↓
[CTE: step2]
  FROM step1
  WHERE total > 200
  SELECT total * 0.1 AS reward_points
    ↓
Final Result (customers with rewards)
    ↓
ORDER BY reward_points DESC
```

---

## 🎯 WHERE vs HAVING (The Key Difference)

| Clause | Filters | Timing | Can Use Aggregates? |
|--------|---------|--------|---------------------|
| **WHERE** | Individual Rows | Before GROUP BY | ❌ NO |
| **HAVING** | Groups | After GROUP BY | ✅ YES |

**Example:**
```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
WHERE order_amount > 100        -- Filter rows first
GROUP BY customer_id
HAVING COUNT(*) > 2;            -- Filter groups second
```

**Flow:**
1. **WHERE**: Keep only orders > $100
2. **GROUP BY**: Group by customer
3. **HAVING**: Keep only customers with > 2 orders

---

## 🧠 Mental Model: The Assembly Line

Think of SQL as an assembly line:

```
[Raw Materials] → [Filter Defects] → [Group by Type] → [Filter Groups] → [Package] → [Sort]
     FROM              WHERE            GROUP BY          HAVING         SELECT    ORDER BY
```

**CTEs are like multiple assembly lines:**
```
Line 1 (CTE #1) → Output
                    ↓
                Line 2 (CTE #2) → Output
                                    ↓
                                Final Product
```

---

## 🚀 Real-World Example

**Problem:** Find customers who spent > $500 total in 2023, show their reward points.

```sql
WITH customer_totals AS (
    -- Assembly Line 1: Calculate totals
    SELECT 
        customer_id,
        SUM(order_amount) AS total_spent
    FROM orders
    WHERE YEAR(order_date) = 2023    -- Filter: Only 2023
    GROUP BY customer_id
    HAVING SUM(order_amount) > 500   -- Filter: Only big spenders
),
rewards AS (
    -- Assembly Line 2: Calculate rewards
    SELECT 
        customer_id,
        total_spent,
        total_spent * 0.05 AS reward_points
    FROM customer_totals
)
SELECT * FROM rewards ORDER BY reward_points DESC;
```

**Data Flow:**
```
orders (raw)
    ↓ WHERE (2023 only)
    ↓ GROUP BY (customer)
    ↓ HAVING (> $500)
customer_totals (CTE)
    ↓ SELECT (add reward_points)
rewards (CTE)
    ↓ ORDER BY (sort)
Final Result
```
