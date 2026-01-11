# 🎧 The 3-Step Problem Parsing Method

**A repeatable framework to beat SQL anxiety.**

---

## 🧠 The Psychology

When you see a long, complex question, your brain tries to solve it all at once. **That causes anxiety.**
Instead, we will break it into **3 small, manageable steps**.

---

## 🛠️ The 3 Steps

### **Step 1: Identify the "Entity" (The Row)**
**Question to ask:** "What does ONE row in my final output represent?"
**SQL Action:** This determines your `GROUP BY`.

| If the row is... | Then GROUP BY... |
|------------------|------------------|
| A Customer | `customer_id` |
| A Product | `product_id` |
| A Month | `month(date)` |
| A Department | `department_id` |

---

### **Step 2: Identify the "Filters" (The Trash)**
**Question to ask:** "Which rows do I want to throw away immediately?"
**SQL Action:** This determines your `WHERE` clause.

**Trigger Words:**
- "Active customers" -> `status = 'Active'`
- "In 2023" -> `year = 2023`
- "From USA" -> `country = 'USA'`

---

### **Step 3: Identify the "Aggregates" (The Math)**
**Question to ask:** "Am I counting, summing, or averaging?"
**SQL Action:** This determines your `SELECT` math and `HAVING` clause.

**Trigger Words:**
- "Total Sales" -> `SUM(sales)`
- "Number of Orders" -> `COUNT(orders)`
- "Average Price" -> `AVG(price)`
- "More than 5 orders" -> `HAVING COUNT(*) > 5`

---

## 🎓 Example Walkthrough

**The Scary Question:**
> "Find the **average order value** for all **VIP customers** in **2023** who placed **more than 5 orders**."

### **Apply the Steps:**

1.  **Entity**: "For all VIP **Customers**"
    -   ✅ **Action**: `GROUP BY customer_id`

2.  **Filters**: "**VIP**" and "**In 2023**"
    -   ✅ **Action**: `WHERE status = 'VIP' AND year = 2023`

3.  **Aggregates**: "**Average order value**" and "**More than 5**"
    -   ✅ **Action**: `SELECT AVG(value)` and `HAVING COUNT(*) > 5`

### **The Resulting Query:**

```sql
SELECT customer_id, AVG(order_value)
FROM orders
WHERE status = 'VIP' AND year = 2023  -- Step 2 (Filters)
GROUP BY customer_id                  -- Step 1 (Entity)
HAVING COUNT(*) > 5;                  -- Step 3 (Aggregates)
```

---

## 🧘 Mental Checklist

Next time you see a question, take a deep breath and find:
1.  **The Entity** (Group By)
2.  **The Filters** (Where)
3.  **The Aggregates** (Select/Having)
