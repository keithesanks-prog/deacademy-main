# 🔗 SQL Correlated Subqueries: Complete Guide

**Subqueries that reference the outer query**

---

## 🤔 What is a Correlated Subquery?

A **correlated subquery** is a subquery that **references columns from the outer query**. It runs **once for each row** in the outer query.

**Think of it like a loop:**
```
For each product:
    Calculate the average price for THIS product's category
    Compare THIS product's price to that average
```

---

## 💡 Regular Subquery vs Correlated Subquery

### **Regular Subquery (Runs Once)**
```sql
SELECT *
FROM products
WHERE unit_price > (SELECT AVG(unit_price) FROM products);
                    ↑ Runs once, returns one value
```

**Execution:**
1. Calculate global average: `$150`
2. Find all products > `$150`

---

### **Correlated Subquery (Runs for Each Row)**
```sql
SELECT *
FROM products p
WHERE p.unit_price > 
(
    SELECT AVG(unit_price)
    FROM products
    WHERE category = p.category  -- ← References outer query!
);
```

**Execution:**
1. For **each product**, calculate average for **its category**
2. Compare that product's price to **its category's average**

---

## 📊 Visual Example

**Sample Data:**
| product_id | product_name | unit_price | category |
|------------|--------------|------------|----------|
| 1 | Laptop | 1200 | Electronics |
| 2 | Mouse | 25 | Electronics |
| 3 | Desk | 300 | Furniture |
| 4 | Chair | 150 | Furniture |

**Category Averages:**
- Electronics: `(1200 + 25) / 2 = 612.50`
- Furniture: `(300 + 150) / 2 = 225.00`

---

## 🔍 Step-by-Step Execution

**Query:**
```sql
SELECT p.product_id, p.product_name, p.unit_price, p.category
FROM products p
WHERE p.unit_price > 
(
    SELECT AVG(unit_price)
    FROM products
    WHERE category = p.category
);
```

**Row 1: Laptop (Electronics, $1200)**
```
Subquery: SELECT AVG(unit_price) FROM products WHERE category = 'Electronics'
Result: 612.50
Compare: 1200 > 612.50? ✅ YES → Include Laptop
```

**Row 2: Mouse (Electronics, $25)**
```
Subquery: SELECT AVG(unit_price) FROM products WHERE category = 'Electronics'
Result: 612.50
Compare: 25 > 612.50? ❌ NO → Exclude Mouse
```

**Row 3: Desk (Furniture, $300)**
```
Subquery: SELECT AVG(unit_price) FROM products WHERE category = 'Furniture'
Result: 225.00
Compare: 300 > 225.00? ✅ YES → Include Desk
```

**Row 4: Chair (Furniture, $150)**
```
Subquery: SELECT AVG(unit_price) FROM products WHERE category = 'Furniture'
Result: 225.00
Compare: 150 > 225.00? ❌ NO → Exclude Chair
```

**Final Result:**
| product_id | product_name | unit_price | category |
|------------|--------------|------------|----------|
| 1 | Laptop | 1200 | Electronics |
| 3 | Desk | 300 | Furniture |

---

## 🎯 Common Use Cases

### **Use Case 1: Above-Average Products per Category**
```sql
SELECT *
FROM products p
WHERE p.unit_price > 
(
    SELECT AVG(unit_price)
    FROM products
    WHERE category = p.category
);
```

---

### **Use Case 2: Employees Earning More Than Their Department Average**
```sql
SELECT *
FROM employees e
WHERE e.salary > 
(
    SELECT AVG(salary)
    FROM employees
    WHERE department = e.department
);
```

---

### **Use Case 3: Customers Who Spent More Than Their Country's Average**
```sql
SELECT *
FROM customers c
WHERE c.total_spent > 
(
    SELECT AVG(total_spent)
    FROM customers
    WHERE country = c.country
);
```

---

## ⚠️ Performance Warning

**Correlated subqueries can be SLOW** because they run once for each row!

**Example:**
- 1,000 products → Subquery runs 1,000 times

**Better Alternative: Use a JOIN with a CTE**
```sql
WITH category_averages AS (
    SELECT 
        category,
        AVG(unit_price) AS avg_price
    FROM products
    GROUP BY category
)
SELECT p.*
FROM products p
JOIN category_averages ca ON p.category = ca.category
WHERE p.unit_price > ca.avg_price;
```

**This is faster** because the average is calculated once per category, not once per product!

---

## 🔍 How to Identify a Correlated Subquery

**Look for these signs:**

1. **Alias in outer query** (`p` in `FROM products p`)
2. **Reference to outer alias in subquery** (`WHERE category = p.category`)

**Example:**
```sql
SELECT *
FROM products p  -- ← Alias 'p'
WHERE p.unit_price > 
(
    SELECT AVG(unit_price)
    FROM products
    WHERE category = p.category  -- ← References 'p' from outer query
);
```

---

## 💡 Correlated vs Non-Correlated

| Type | Runs | References Outer Query | Speed |
|------|------|------------------------|-------|
| **Non-Correlated** | Once | ❌ No | ⚡ Fast |
| **Correlated** | Once per row | ✅ Yes | 🐌 Slower |

---

## 🎯 Practice Problem

**Problem:** Find employees who earn more than the average salary in their department.

**Sample Data:**
| employee_id | name | department | salary |
|-------------|------|------------|--------|
| 1 | Alice | Sales | 60000 |
| 2 | Bob | Sales | 50000 |
| 3 | Charlie | IT | 80000 |
| 4 | Dave | IT | 70000 |

**Department Averages:**
- Sales: `(60000 + 50000) / 2 = 55000`
- IT: `(80000 + 70000) / 2 = 75000`

<details>
<summary>Click for solution</summary>

```sql
SELECT e.employee_id, e.name, e.department, e.salary
FROM employees e
WHERE e.salary > 
(
    SELECT AVG(salary)
    FROM employees
    WHERE department = e.department
);
```

**Result:**
| employee_id | name | department | salary |
|-------------|------|------------|--------|
| 1 | Alice | Sales | 60000 |
| 3 | Charlie | IT | 80000 |

</details>

---

## 🚀 Key Takeaways

1. **Correlated subqueries reference the outer query**
2. **They run once for each row** (can be slow)
3. **Use for row-by-row comparisons** (e.g., above category average)
4. **Consider CTEs + JOINs for better performance**
5. **Look for outer query aliases in the subquery** to identify them
