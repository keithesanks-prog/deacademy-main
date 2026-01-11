# 🎧 WHERE vs HAVING: Examples & Syntax

**This guide matches the audio lesson script. Follow along as you listen!**

---

## 🟢 WHERE: The "Row" Filter

**Rule:** Use when asking about **raw data** in a specific row.
**Timing:** Before Grouping.

### **Example 1: Dates**
> "Show me orders from 2023."
```sql
SELECT * FROM orders
WHERE order_date >= '2023-01-01';
```

### **Example 2: Status**
> "Show me only active customers."
```sql
SELECT * FROM customers
WHERE status = 'Active';
```

### **Example 3: Text Patterns**
> "Show me names starting with A."
```sql
SELECT * FROM employees
WHERE name LIKE 'A%';
```

---

## 🔵 HAVING: The "Group" Filter

**Rule:** Use when asking about a **calculated summary** (Count, Sum, Avg).
**Timing:** After Grouping.

### **Example 1: Counts**
> "Show me customers who placed more than 5 orders."
```sql
SELECT customer_id, COUNT(*)
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;
```

### **Example 2: Sums**
> "Show me sales reps who sold more than $10,000."
```sql
SELECT rep_id, SUM(sales_amount)
FROM sales
GROUP BY rep_id
HAVING SUM(sales_amount) > 10000;
```

### **Example 3: Averages**
> "Show me products with an average rating below 3 stars."
```sql
SELECT product_id, AVG(rating)
FROM reviews
GROUP BY product_id
HAVING AVG(rating) < 3;
```

---

## 🟣 The Power Move: Using BOTH

**Scenario:** "Show me customers from the **USA** who placed **more than 5** orders."

1.  **Filter Rows (WHERE)**: Only keep USA rows.
2.  **Group (GROUP BY)**: Bundle them by customer.
3.  **Filter Groups (HAVING)**: Only keep bundles with > 5 orders.

```sql
SELECT customer_id, COUNT(*)
FROM orders
WHERE country = 'USA'        -- Step 1: Filter Rows
GROUP BY customer_id         -- Step 2: Make Groups
HAVING COUNT(*) > 5;         -- Step 3: Filter Groups
```

---

## ⚡ Cheat Sheet

| Question Type | Clause | Example |
|---------------|--------|---------|
| "Is the **date**...?" | `WHERE` | `order_date > '2023'` |
| "Is the **status**...?" | `WHERE` | `status = 'Pending'` |
| "Is the **total**...?" | `HAVING` | `SUM(total) > 100` |
| "Is the **count**...?" | `HAVING` | `COUNT(*) > 5` |
| "Is the **average**...?" | `HAVING` | `AVG(score) < 50` |
