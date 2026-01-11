# 📚 SQL LIMIT Guide

## 🎯 What is LIMIT?

`LIMIT` controls how many rows are returned by a query.

**Basic Syntax:**
```sql
SELECT columns FROM table LIMIT number;
```

---

## 📊 Basic Examples

### **Example 1: Get First 5 Rows**
```sql
SELECT * FROM products LIMIT 5;
```
Returns the first 5 products.

---

### **Example 2: Top 3 Most Expensive Products**
```sql
SELECT product_name, price
FROM products
ORDER BY price DESC
LIMIT 3;
```
Returns the 3 most expensive products.

---

### **Example 3: Top 10 Recent Orders**
```sql
SELECT * FROM orders
ORDER BY order_date DESC
LIMIT 10;
```
Returns the 10 most recent orders.

---

## 🔢 LIMIT with OFFSET

`OFFSET` skips a certain number of rows before returning results.

**Syntax:**
```sql
SELECT columns FROM table LIMIT number OFFSET skip;
```

---

### **Example 4: Skip First 10, Get Next 5**
```sql
SELECT * FROM customers
LIMIT 5 OFFSET 10;
```

**What this does:**
- Skip rows 1-10
- Return rows 11-15

**Use case:** Pagination (page 3 of results)

---

### **Example 5: Get 2nd Highest Salary**
```sql
SELECT first_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;
```

**How it works:**
1. Sort by salary (highest first)
2. Skip 1st row (highest salary)
3. Return next 1 row (2nd highest)

---

### **Example 6: Get 3rd Highest Salary**
```sql
SELECT first_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 2;
```

**Pattern for Nth highest:**
- 1st highest: `LIMIT 1 OFFSET 0`
- 2nd highest: `LIMIT 1 OFFSET 1`
- 3rd highest: `LIMIT 1 OFFSET 2`
- Nth highest: `LIMIT 1 OFFSET (N-1)`

---

## 📄 Pagination Pattern

**Page 1 (rows 1-10):**
```sql
SELECT * FROM products LIMIT 10 OFFSET 0;
```

**Page 2 (rows 11-20):**
```sql
SELECT * FROM products LIMIT 10 OFFSET 10;
```

**Page 3 (rows 21-30):**
```sql
SELECT * FROM products LIMIT 10 OFFSET 20;
```

**Formula:**
```sql
LIMIT page_size OFFSET (page_number - 1) * page_size
```

---

## 🎯 Common Patterns

### **Pattern 1: Top N Results**
```sql
SELECT * FROM table
ORDER BY column DESC
LIMIT N;
```

### **Pattern 2: Nth Item**
```sql
SELECT * FROM table
ORDER BY column DESC
LIMIT 1 OFFSET (N-1);
```

### **Pattern 3: Pagination**
```sql
SELECT * FROM table
LIMIT page_size OFFSET (page - 1) * page_size;
```

### **Pattern 4: Sample Data**
```sql
SELECT * FROM large_table LIMIT 100;
```
Quick preview of data.

---

## 💡 Important Notes

### **1. LIMIT Comes Last**
```sql
SELECT columns
FROM table
WHERE condition
GROUP BY column
HAVING condition
ORDER BY column
LIMIT number;  ← Always at the end
```

### **2. Always Use ORDER BY**
Without `ORDER BY`, results are unpredictable!

**❌ Bad:**
```sql
SELECT * FROM products LIMIT 5;
-- Which 5? Random!
```

**✅ Good:**
```sql
SELECT * FROM products
ORDER BY product_id
LIMIT 5;
-- First 5 by ID
```

### **3. Different Databases**

**MySQL/PostgreSQL/SQLite:**
```sql
LIMIT 10 OFFSET 5
```

**SQL Server:**
```sql
OFFSET 5 ROWS FETCH NEXT 10 ROWS ONLY
```

**Oracle:**
```sql
FETCH FIRST 10 ROWS ONLY
```

---

## ✅ Practice Exercises

### **Exercise 1:**
Get the top 5 highest-paid employees.

<details>
<summary>Solution</summary>

```sql
SELECT first_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 5;
```
</details>

---

### **Exercise 2:**
Get the 10th highest salary.

<details>
<summary>Solution</summary>

```sql
SELECT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 9;
```
</details>

---

### **Exercise 3:**
Get page 3 of products (10 per page).

<details>
<summary>Solution</summary>

```sql
SELECT * FROM products
ORDER BY product_id
LIMIT 10 OFFSET 20;
-- Page 3: skip first 20 (pages 1-2), get next 10
```
</details>

---

## 📊 Quick Reference

| Task | Query |
|------|-------|
| First 10 rows | `LIMIT 10` |
| Top 5 by price | `ORDER BY price DESC LIMIT 5` |
| 2nd highest | `ORDER BY col DESC LIMIT 1 OFFSET 1` |
| 3rd highest | `ORDER BY col DESC LIMIT 1 OFFSET 2` |
| Page 2 (10/page) | `LIMIT 10 OFFSET 10` |
| Skip 5, get 10 | `LIMIT 10 OFFSET 5` |

---

## 🚀 Summary

- **LIMIT** - Controls how many rows to return
- **OFFSET** - Skips rows before returning results
- **Always use ORDER BY** for predictable results
- **Pattern for Nth item:** `LIMIT 1 OFFSET (N-1)`
- **Pagination:** `LIMIT page_size OFFSET (page-1)*page_size`

Happy querying! 🎓
