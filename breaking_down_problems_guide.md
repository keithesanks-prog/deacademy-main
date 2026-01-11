# 🎧 Breaking Down SQL Problems - Audio Lesson Companion

**This guide matches the audio lesson script. Follow along as you listen!**

---

## 🗣️ The Question

> "Retrieve the **customer_name** of customers who have placed orders with a **total amount** greater than the **average amount of all orders**."

---

## 🚦 Identifying Signal Words

| Phrase | Signal | SQL Translation |
|--------|--------|-----------------|
| "Total amount" | Aggregation | `SUM(order_amount)` |
| "Greater than" | Comparison | `>` |
| "Average amount of ALL" | Global Aggregation | `(SELECT AVG(...) FROM ...)` |
| "By Customer" (Implied) | Grouping | `GROUP BY customer_id` |

---

## 🏗️ The Structure Breakdown

We need 3 layers to solve this:

### **Layer 1: The Benchmark (Subquery)**
First, we need the "Global Average" to compare against.
```sql
(SELECT AVG(order_amount) FROM orders)
-- Result: e.g., 500.00
```

### **Layer 2: The Groups (Main Query)**
We need to calculate the total for **each** customer.
```sql
SELECT customer_name, SUM(order_amount)
FROM customers
JOIN orders ...
GROUP BY customer_name
```

### **Layer 3: The Filter (HAVING)**
We filter the **Groups** based on the **Benchmark**.
```sql
HAVING SUM(order_amount) > (Benchmark)
```

---

## 🔨 Building the Query

```sql
SELECT 
    c.customer_name
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(o.order_amount) > (
    -- The Subquery
    SELECT AVG(order_amount) 
    FROM orders
);
```

---

## 🧠 Mental Model

1.  **Calculate Global Avg**: Imagine a single number floating in the air (e.g., 500).
2.  **Group Customers**: Stack all orders for "John", all orders for "Jane".
3.  **Sum Each Stack**: John's Total = 400. Jane's Total = 600.
4.  **Compare**:
    -   Is John (400) > Global (500)? **NO** ❌
    -   Is Jane (600) > Global (500)? **YES** ✅ -> **Keep Jane**

---

## ⚠️ Common Pitfalls

### **❌ Mistake 1: Using WHERE**
```sql
-- WRONG!
WHERE SUM(order_amount) > ...
```
**Why?** `WHERE` filters rows *before* grouping. `SUM` doesn't exist yet! You must use `HAVING`.

### **❌ Mistake 2: Forgetting the Subquery**
```sql
-- WRONG!
HAVING SUM(order_amount) > AVG(order_amount)
```
**Why?** `AVG(order_amount)` here would mean "Average of *this customer's* orders", not "Average of *all* orders". You need the subquery to go outside the group.
