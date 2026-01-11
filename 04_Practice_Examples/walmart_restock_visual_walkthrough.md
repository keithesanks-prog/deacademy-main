# 🏪 Walmart Restock Query: Visual Step-by-Step

**Building the query incrementally with data transformations**

---

## 📋 The Problem

> "Find products that had stock replenished (quantity > 0) at least once between January and June 2023."

**Output:** `product_id, product_name, restock_count`

---

## 📊 Starting Tables

### **walmart_products**
| product_id | product_name | category | price | stock_count |
|------------|--------------|----------|-------|-------------|
| 101 | Laptop | Electronics | 899.99 | 15 |
| 102 | Mouse | Electronics | 29.99 | 50 |
| 103 | Keyboard | Electronics | 79.99 | 30 |
| 104 | Monitor | Electronics | 299.99 | 10 |

### **walmart_inventory_updates**
| update_id | product_id | update_date | quantity_added |
|-----------|------------|-------------|----------------|
| 1 | 101 | 2023-02-15 | 50 |
| 2 | 101 | 2023-05-20 | 30 |
| 3 | 102 | 2023-01-10 | 100 |
| 4 | 103 | 2023-08-05 | 20 |
| 5 | 104 | 2023-03-12 | -10 |

---

## 🔨 Step 1: JOIN the Tables

**Query:**
```sql
SELECT 
    p.product_id,
    p.product_name,
    u.update_date,
    u.quantity_added
FROM walmart_products p
JOIN walmart_inventory_updates u 
    ON p.product_id = u.product_id;
```

**Result:**
| product_id | product_name | update_date | quantity_added |
|------------|--------------|-------------|----------------|
| 101 | Laptop | 2023-02-15 | 50 |
| 101 | Laptop | 2023-05-20 | 30 |
| 102 | Mouse | 2023-01-10 | 100 |
| 103 | Keyboard | 2023-08-05 | 20 |
| 104 | Monitor | 2023-03-12 | -10 |

**What changed:** Combined product names with their restock events.

---

## 🔨 Step 2: Filter by Quantity (quantity > 0)

**Query:**
```sql
SELECT 
    p.product_id,
    p.product_name,
    u.update_date,
    u.quantity_added
FROM walmart_products p
JOIN walmart_inventory_updates u 
    ON p.product_id = u.product_id
WHERE u.quantity_added > 0;
```

**Result:**
| product_id | product_name | update_date | quantity_added |
|------------|--------------|-------------|----------------|
| 101 | Laptop | 2023-02-15 | 50 |
| 101 | Laptop | 2023-05-20 | 30 |
| 102 | Mouse | 2023-01-10 | 100 |
| 103 | Keyboard | 2023-08-05 | 20 |

**What changed:** Removed Monitor (quantity_added = -10).

---

## 🔨 Step 3: Filter by Date (Jan-Jun 2023)

**Query:**
```sql
SELECT 
    p.product_id,
    p.product_name,
    u.update_date,
    u.quantity_added
FROM walmart_products p
JOIN walmart_inventory_updates u 
    ON p.product_id = u.product_id
WHERE u.quantity_added > 0
  AND u.update_date BETWEEN '2023-01-01' AND '2023-06-30';
```

**Result:**
| product_id | product_name | update_date | quantity_added |
|------------|--------------|-------------|----------------|
| 101 | Laptop | 2023-02-15 | 50 |
| 101 | Laptop | 2023-05-20 | 30 |
| 102 | Mouse | 2023-01-10 | 100 |

**What changed:** Removed Keyboard (August 2023, outside the range).

---

## 🔨 Step 4: GROUP BY and COUNT

**Query:**
```sql
SELECT 
    p.product_id,
    p.product_name,
    COUNT(*) AS restock_count
FROM walmart_products p
JOIN walmart_inventory_updates u 
    ON p.product_id = u.product_id
WHERE u.quantity_added > 0
  AND u.update_date BETWEEN '2023-01-01' AND '2023-06-30'
GROUP BY p.product_id, p.product_name;
```

**Result:**
| product_id | product_name | restock_count |
|------------|--------------|---------------|
| 101 | Laptop | 2 |
| 102 | Mouse | 1 |

**What changed:** Collapsed rows by product, counting restock events.

---

## 📊 Visual Data Flow

```
Step 1: JOIN
┌────────────┬──────────────┬─────────────┬────────────────┐
│ product_id │ product_name │ update_date │ quantity_added │
├────────────┼──────────────┼─────────────┼────────────────┤
│ 101        │ Laptop       │ 2023-02-15  │ 50             │
│ 101        │ Laptop       │ 2023-05-20  │ 30             │
│ 102        │ Mouse        │ 2023-01-10  │ 100            │
│ 103        │ Keyboard     │ 2023-08-05  │ 20             │
│ 104        │ Monitor      │ 2023-03-12  │ -10            │
└────────────┴──────────────┴─────────────┴────────────────┘
                    ↓
        WHERE quantity_added > 0
                    ↓
┌────────────┬──────────────┬─────────────┬────────────────┐
│ product_id │ product_name │ update_date │ quantity_added │
├────────────┼──────────────┼─────────────┼────────────────┤
│ 101        │ Laptop       │ 2023-02-15  │ 50             │
│ 101        │ Laptop       │ 2023-05-20  │ 30             │
│ 102        │ Mouse        │ 2023-01-10  │ 100            │
│ 103        │ Keyboard     │ 2023-08-05  │ 20             │
└────────────┴──────────────┴─────────────┴────────────────┘
                    ↓
    WHERE update_date BETWEEN '2023-01-01' AND '2023-06-30'
                    ↓
┌────────────┬──────────────┬─────────────┬────────────────┐
│ product_id │ product_name │ update_date │ quantity_added │
├────────────┼──────────────┼─────────────┼────────────────┤
│ 101        │ Laptop       │ 2023-02-15  │ 50             │
│ 101        │ Laptop       │ 2023-05-20  │ 30             │
│ 102        │ Mouse        │ 2023-01-10  │ 100            │
└────────────┴──────────────┴─────────────┴────────────────┘
                    ↓
        GROUP BY product_id, product_name
                    ↓
┌────────────┬──────────────┬───────────────┐
│ product_id │ product_name │ restock_count │
├────────────┼──────────────┼───────────────┤
│ 101        │ Laptop       │ 2             │
│ 102        │ Mouse        │ 1             │
└────────────┴──────────────┴───────────────┘
```

---

## 🎯 The 3-Step Method Applied

### **Step 1: Entity (The Row)**
**Question:** "What does one row represent?"  
**Answer:** A Product  
**SQL:** `GROUP BY product_id, product_name`

### **Step 2: Filters (The Trash)**
**Question:** "Which rows to throw away?"  
**Answer:** 
- Negative quantities (removals, not restocks)
- Dates outside Jan-Jun 2023

**SQL:** 
```sql
WHERE quantity_added > 0 
  AND update_date BETWEEN '2023-01-01' AND '2023-06-30'
```

### **Step 3: Aggregates (The Math)**
**Question:** "Am I counting/summing/averaging?"  
**Answer:** Counting restock events  
**SQL:** `COUNT(*) AS restock_count`

---

## 🔄 Alternative: Using HAVING Instead of Subquery

**If the question was:** "Find products with **more than 2** restocks"

### **Method 1: HAVING Clause (Simpler)**
```sql
SELECT 
    p.product_id,
    p.product_name,
    COUNT(*) AS restock_count
FROM walmart_products p
JOIN walmart_inventory_updates u 
    ON p.product_id = u.product_id
WHERE u.quantity_added > 0
  AND u.update_date BETWEEN '2023-01-01' AND '2023-06-30'
GROUP BY p.product_id, p.product_name
HAVING COUNT(*) > 2;  -- Filter on the aggregated count
```

### **Method 2: Subquery (More Complex)**
```sql
SELECT 
    t.product_id,
    t.product_name,
    t.restock_count
FROM (
    SELECT 
        p.product_id,
        p.product_name,
        COUNT(*) AS restock_count
    FROM walmart_products p
    JOIN walmart_inventory_updates u 
        ON p.product_id = u.product_id
    WHERE u.quantity_added > 0
      AND u.update_date BETWEEN '2023-01-01' AND '2023-06-30'
    GROUP BY p.product_id, p.product_name
) t
WHERE t.restock_count > 2;  -- Filter on the calculated column
```

### **Visual Comparison:**

**HAVING Approach:**
```
FROM → WHERE → GROUP BY → HAVING → SELECT
                           ↑
                    Filter on COUNT(*)
```

**Subquery Approach:**
```
Inner: FROM → WHERE → GROUP BY → SELECT (with COUNT)
                                    ↓
Outer: FROM (subquery) → WHERE (filter on COUNT)
```

---

## 🎯 When to Use Each

| Scenario | Use HAVING | Use Subquery |
|----------|------------|--------------|
| Filter on COUNT/SUM/AVG | ✅ **Simpler** | ⚠️ Works but verbose |
| Need to use the aggregated value in calculations | ❌ Can't do math on it | ✅ **Better** |
| Multiple filters on aggregates | ✅ **Cleaner** | ⚠️ Gets messy |

**Example where subquery is better:**
```sql
-- Calculate reward points (10% of total restocks)
SELECT 
    product_id,
    restock_count,
    restock_count * 0.1 AS reward_points  -- Math on the COUNT
FROM (
    SELECT product_id, COUNT(*) AS restock_count
    FROM walmart_inventory_updates
    GROUP BY product_id
) t;
```

**You can't do:** `SELECT COUNT(*) * 0.1` directly in the same query with GROUP BY.

---

## 💡 Key Takeaways

1. **Build incrementally** - Don't write the full query at once
2. **Test each step** - Run `SELECT *` after each addition
3. **Filter before grouping** - WHERE comes before GROUP BY
4. **GROUP BY all non-aggregated columns** - Both `product_id` and `product_name`
5. **Use HAVING for simple aggregate filters** - Cleaner than subqueries
6. **Use subqueries when you need to do math on aggregates** - More flexible
