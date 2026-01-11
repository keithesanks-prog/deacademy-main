# 📚 SQL IN and HAVING Guide

## 🎯 The IN Operator

### **What is IN?**

`IN` checks if a value matches **any** value in a list.

**Syntax:**
```sql
WHERE column IN (value1, value2, value3)
```

---

## 📊 IN Examples

### **Example 1: Multiple Values**

**Without IN (verbose):**
```sql
WHERE department = 'Sales' OR department = 'Marketing' OR department = 'HR'
```

**With IN (clean):**
```sql
WHERE department IN ('Sales', 'Marketing', 'HR')
```

---

### **Example 2: Numeric Values**

```sql
SELECT * FROM products
WHERE customer_satisfaction IN (4, 5);
```

**Same as:**
```sql
WHERE customer_satisfaction = 4 OR customer_satisfaction = 5
```

---

### **Example 3: Exclude Multiple Values (NOT IN)**

```sql
SELECT * FROM employees
WHERE department NOT IN ('Sales', 'Marketing', 'IT');
```

Returns employees NOT in those three departments.

---

### **Example 4: IN with Subquery**

```sql
SELECT * FROM orders
WHERE customer_id IN (
    SELECT customer_id 
    FROM customers 
    WHERE country = 'USA'
);
```

Returns orders from US customers.

---

## 💡 When to Use IN

### **✅ Use IN when:**
- Checking against multiple specific values
- More than 2 values to check
- Values are known/fixed

### **❌ Don't use IN when:**
- Only checking one value (use `=`)
- Checking a range (use `BETWEEN`)
- Only two values and OR is clearer

---

## 🎯 The HAVING Clause

### **What is HAVING?**

`HAVING` filters **after** grouping, used with aggregate functions.

**Key Difference:**
- **WHERE** filters BEFORE grouping
- **HAVING** filters AFTER grouping

---

## 📊 WHERE vs HAVING

### **WHERE - Filters Individual Rows**

```sql
SELECT department, AVG(salary)
FROM employees
WHERE salary > 50000  -- Filter individual employees
GROUP BY department;
```

**Process:**
1. Filter employees with salary > 50000
2. Group by department
3. Calculate average

---

### **HAVING - Filters Grouped Results**

```sql
SELECT department, AVG(salary)
FROM employees
GROUP BY department
HAVING AVG(salary) > 80000;  -- Filter departments
```

**Process:**
1. Group by department
2. Calculate average per department
3. Filter departments with avg > 80000

---

## 📊 HAVING Examples

### **Example 1: Filter by Count**

```sql
SELECT product_id, COUNT(*) AS review_count
FROM reviews
GROUP BY product_id
HAVING COUNT(*) >= 5;
```

Returns products with at least 5 reviews.

---

### **Example 2: Filter by Average**

```sql
SELECT content_id, AVG(rating) AS avg_rating
FROM reviews
GROUP BY content_id
HAVING AVG(rating) >= 4;
```

Returns content with average rating 4 or higher.

---

### **Example 3: Multiple HAVING Conditions**

```sql
SELECT 
    product_id,
    AVG(rating) AS avg_rating,
    COUNT(*) AS review_count
FROM reviews
GROUP BY product_id
HAVING AVG(rating) >= 4
   AND COUNT(*) >= 5;
```

Returns products with:
- Average rating ≥ 4 **AND**
- At least 5 reviews

---

### **Example 4: HAVING with WHERE**

```sql
SELECT 
    category,
    AVG(price) AS avg_price
FROM products
WHERE is_active = TRUE  -- Filter individual products first
GROUP BY category
HAVING AVG(price) > 100;  -- Then filter categories
```

**Process:**
1. WHERE: Keep only active products
2. GROUP BY: Group by category
3. HAVING: Keep categories with avg price > 100

---

## 🎯 Combining IN and HAVING

### **Example: High-Rated Hardware Products**

```sql
SELECT 
    p.product_id,
    p.product_name,
    AVG(r.rating) AS avg_rating,
    COUNT(r.review_id) AS review_count
FROM products p
JOIN reviews r ON p.product_id = r.product_id
WHERE p.category IN ('Hardware', 'Electronics')  -- IN for multiple categories
GROUP BY p.product_id, p.product_name
HAVING AVG(r.rating) >= 4  -- HAVING for aggregated rating
   AND COUNT(r.review_id) >= 5;  -- HAVING for aggregated count
```

---

## 💡 Key Rules

### **WHERE vs HAVING:**

| Aspect | WHERE | HAVING |
|--------|-------|--------|
| **When** | Before GROUP BY | After GROUP BY |
| **Filters** | Individual rows | Grouped results |
| **Can use aggregates?** | ❌ No | ✅ Yes |
| **Example** | `WHERE price > 100` | `HAVING AVG(price) > 100` |

---

### **IN Best Practices:**

1. ✅ Use for 3+ values
2. ✅ Use NOT IN for exclusions
3. ✅ Can use with subqueries
4. ⚠️ Watch for NULL values with NOT IN

---

### **HAVING Best Practices:**

1. ✅ Always use with GROUP BY
2. ✅ Use for filtering aggregated data
3. ✅ Can combine multiple conditions with AND/OR
4. ✅ Use WHERE first to filter before grouping (more efficient)

---

## ✅ Practice Exercises

### **Exercise 1: IN**
Get employees from Sales, Marketing, or HR departments.

<details>
<summary>Solution</summary>

```sql
SELECT * FROM employees
WHERE department IN ('Sales', 'Marketing', 'HR');
```
</details>

---

### **Exercise 2: NOT IN**
Get products NOT in Electronics or Appliances categories.

<details>
<summary>Solution</summary>

```sql
SELECT * FROM products
WHERE category NOT IN ('Electronics', 'Appliances');
```
</details>

---

### **Exercise 3: HAVING with Count**
Get departments with more than 10 employees.

<details>
<summary>Solution</summary>

```sql
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 10;
```
</details>

---

### **Exercise 4: HAVING with Average**
Get products with average rating above 4 and at least 5 reviews.

<details>
<summary>Solution</summary>

```sql
SELECT 
    product_id,
    AVG(rating) AS avg_rating,
    COUNT(*) AS review_count
FROM reviews
GROUP BY product_id
HAVING AVG(rating) > 4
   AND COUNT(*) >= 5;
```
</details>

---

### **Exercise 5: WHERE + IN + HAVING**
Get active products in Hardware or Electronics with avg rating ≥ 4.

<details>
<summary>Solution</summary>

```sql
SELECT 
    p.product_id,
    p.category,
    AVG(r.rating) AS avg_rating
FROM products p
JOIN reviews r ON p.product_id = r.product_id
WHERE p.is_active = TRUE
  AND p.category IN ('Hardware', 'Electronics')
GROUP BY p.product_id, p.category
HAVING AVG(r.rating) >= 4;
```
</details>

---

## 📊 Quick Reference

### **IN Operator:**
```sql
-- Check multiple values
WHERE column IN (value1, value2, value3)

-- Exclude multiple values
WHERE column NOT IN (value1, value2, value3)

-- With subquery
WHERE column IN (SELECT column FROM table WHERE condition)
```

### **HAVING Clause:**
```sql
-- Filter by count
HAVING COUNT(*) > 10

-- Filter by average
HAVING AVG(column) >= 4

-- Multiple conditions
HAVING AVG(column) >= 4 AND COUNT(*) >= 5
```

---

## 🚀 Summary

**IN Operator:**
- ✅ Cleaner than multiple OR conditions
- ✅ Works with values or subqueries
- ✅ Use NOT IN for exclusions

**HAVING Clause:**
- ✅ Filters after GROUP BY
- ✅ Works with aggregate functions
- ✅ Use WHERE first, then HAVING

**Remember:** WHERE filters rows, HAVING filters groups! 🎓
