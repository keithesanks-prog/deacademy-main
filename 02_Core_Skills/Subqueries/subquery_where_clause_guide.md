# 🔍 Subqueries with WHERE: Complete Guide

**Understanding when to filter INSIDE vs OUTSIDE the subquery**

---

## 🤔 The Confusion

**Question:** "Find the highest paid employee in the Analytics department."

**Your first instinct might be:**
```sql
SELECT *
FROM employees
WHERE department = 'Analytics'
  AND salary = (SELECT MAX(salary) FROM employees);  -- ❌ Wrong!
```

**But this is incorrect!** Let me show you why.

---

## 📊 The Problem: Wrong Subquery Scope

**Sample Data:**
| employee_id | name | department | salary |
|-------------|------|------------|--------|
| 1 | Alice | Analytics | 80000 |
| 2 | Bob | Analytics | 90000 |
| 3 | Charlie | Sales | 95000 |
| 4 | Dave | Sales | 70000 |

**Your query:**
```sql
SELECT *
FROM employees
WHERE department = 'Analytics'
  AND salary = (SELECT MAX(salary) FROM employees);
```

**What happens:**

**Step 1: Subquery runs**
```sql
SELECT MAX(salary) FROM employees
-- Result: 95000 (Charlie from Sales!)
```

**Step 2: Outer query filters**
```sql
WHERE department = 'Analytics' AND salary = 95000
```

**Step 3: No results!**
```
No Analytics employee has salary = 95000
Result: Empty set
```

---

## ✅ The Solution: Filter Inside the Subquery

```sql
SELECT *
FROM employees
WHERE department = 'Analytics'
  AND salary = (
      SELECT MAX(salary) 
      FROM employees 
      WHERE department = 'Analytics'  -- ← Add filter here!
  );
```

**What happens:**

**Step 1: Subquery runs**
```sql
SELECT MAX(salary) FROM employees WHERE department = 'Analytics'
-- Result: 90000 (Bob from Analytics!)
```

**Step 2: Outer query filters**
```sql
WHERE department = 'Analytics' AND salary = 90000
```

**Step 3: Correct result!**
| employee_id | name | department | salary |
|-------------|------|------------|--------|
| 2 | Bob | Analytics | 90000 |

---

## 🎯 The Rule: Match Your Filters

**If you filter the outer query, filter the subquery the same way!**

```sql
SELECT *
FROM employees
WHERE department = 'Analytics'  -- ← Filter here
  AND salary = (
      SELECT MAX(salary) 
      FROM employees 
      WHERE department = 'Analytics'  -- ← Must filter here too!
  );
```

---

## 📊 Visual Comparison

### **❌ Wrong: No Filter in Subquery**

```
┌─────────────────────────────────────┐
│ Subquery (ALL departments)          │
│ SELECT MAX(salary) FROM employees   │
│ Result: 95000 (from Sales)          │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Outer Query (Analytics only)        │
│ WHERE department = 'Analytics'      │
│   AND salary = 95000                │
│ Result: No match! ❌                │
└─────────────────────────────────────┘
```

### **✅ Correct: Filter in Both**

```
┌─────────────────────────────────────┐
│ Subquery (Analytics only)           │
│ SELECT MAX(salary) FROM employees   │
│ WHERE department = 'Analytics'      │
│ Result: 90000 (from Analytics)      │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Outer Query (Analytics only)        │
│ WHERE department = 'Analytics'      │
│   AND salary = 90000                │
│ Result: Bob ✅                      │
└─────────────────────────────────────┘
```

---

## 💡 More Examples

### **Example 1: Highest Salary Per Department**

**❌ Wrong:**
```sql
SELECT *
FROM employees
WHERE department = 'Sales'
  AND salary = (SELECT MAX(salary) FROM employees);  -- All departments!
```

**✅ Correct:**
```sql
SELECT *
FROM employees
WHERE department = 'Sales'
  AND salary = (SELECT MAX(salary) FROM employees WHERE department = 'Sales');
```

---

### **Example 2: Products Above Category Average**

**❌ Wrong:**
```sql
SELECT *
FROM products
WHERE category = 'Electronics'
  AND price > (SELECT AVG(price) FROM products);  -- All categories!
```

**✅ Correct:**
```sql
SELECT *
FROM products
WHERE category = 'Electronics'
  AND price > (SELECT AVG(price) FROM products WHERE category = 'Electronics');
```

---

### **Example 3: Orders Above Customer's Average**

**❌ Wrong:**
```sql
SELECT *
FROM orders
WHERE customer_id = 123
  AND order_amount > (SELECT AVG(order_amount) FROM orders);  -- All customers!
```

**✅ Correct:**
```sql
SELECT *
FROM orders
WHERE customer_id = 123
  AND order_amount > (SELECT AVG(order_amount) FROM orders WHERE customer_id = 123);
```

---

## 🔍 When You DON'T Need to Match Filters

**Sometimes you want the global max/avg:**

**Example: Find Analytics employees earning more than company average**
```sql
SELECT *
FROM employees
WHERE department = 'Analytics'
  AND salary > (SELECT AVG(salary) FROM employees);  -- ✅ Correct! (global avg)
```

**This is correct because you're comparing to the COMPANY average, not the department average.**

---

## ⚠️ Common Mistakes

### **Mistake 1: Forgetting to filter subquery**
```sql
-- ❌ Wrong
WHERE department = 'Analytics'
  AND salary = (SELECT MAX(salary) FROM employees)

-- ✅ Correct
WHERE department = 'Analytics'
  AND salary = (SELECT MAX(salary) FROM employees WHERE department = 'Analytics')
```

### **Mistake 2: Filtering subquery differently**
```sql
-- ❌ Wrong (different filters)
WHERE department = 'Analytics'
  AND salary = (SELECT MAX(salary) FROM employees WHERE department = 'Sales')

-- ✅ Correct (same filter)
WHERE department = 'Analytics'
  AND salary = (SELECT MAX(salary) FROM employees WHERE department = 'Analytics')
```

---

## 🎯 Quick Decision Guide

**Ask yourself:**

1. **"What am I filtering in the outer query?"**
   - Department = 'Analytics'

2. **"Should the subquery use the same filter?"**
   - If you want max/avg **within that group** → YES
   - If you want max/avg **across all groups** → NO

3. **"What's the question asking?"**
   - "Highest in Analytics" → Filter subquery to Analytics
   - "Above company average" → Don't filter subquery

---

## 📝 Practice Problems

### **Problem 1:**
Find the product with the highest price in the 'Electronics' category.

<details>
<summary>Click for solution</summary>

```sql
SELECT *
FROM products
WHERE category = 'Electronics'
  AND price = (SELECT MAX(price) FROM products WHERE category = 'Electronics');
```

</details>

---

### **Problem 2:**
Find orders that are above the average order amount for customer 123.

<details>
<summary>Click for solution</summary>

```sql
SELECT *
FROM orders
WHERE customer_id = 123
  AND order_amount > (SELECT AVG(order_amount) FROM orders WHERE customer_id = 123);
```

</details>

---

### **Problem 3:**
Find Analytics employees earning more than the company-wide average.

<details>
<summary>Click for solution</summary>

```sql
SELECT *
FROM employees
WHERE department = 'Analytics'
  AND salary > (SELECT AVG(salary) FROM employees);  -- No department filter!
```

</details>

---

## 🚀 Key Takeaways

1. **Match your filters** - If outer query filters by department, subquery should too
2. **Think about scope** - Do you want max/avg within the group or globally?
3. **Read the question carefully** - "highest in Analytics" vs "above company average"
4. **Test your subquery separately** - Make sure it returns the right value
5. **When in doubt, filter the subquery** - It's usually safer
