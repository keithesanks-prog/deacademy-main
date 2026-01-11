# 🎓 SQL Logical Operators - NOT and Operator Precedence

## 🎯 What You Already Know

You're already familiar with:
- ✅ **AND** - Both conditions must be true
- ✅ **OR** - At least one condition must be true
- ✅ **WHERE** - Filtering rows

---

## 🆕 The NOT Operator

### **What is NOT?**

`NOT` **negates** (reverses) a condition. It returns TRUE when the condition is FALSE.

**Think of it as:** "Give me everything EXCEPT..."

---

## 📊 NOT Examples

### **Example 1: NOT with Equality**

**Without NOT:**
```sql
SELECT * FROM customers
WHERE country = 'USA';
```
Returns: All customers FROM the USA

**With NOT:**
```sql
SELECT * FROM customers
WHERE NOT country = 'USA';
```
Returns: All customers NOT from the USA (everyone else!)

---

### **Example 2: NOT with Comparison**

```sql
SELECT * FROM products
WHERE NOT price > 100;
```

**This is the same as:**
```sql
SELECT * FROM products
WHERE price <= 100;
```

Both return products with price 100 or less.

---

### **Example 3: NOT with IN**

**Without NOT:**
```sql
SELECT * FROM employees
WHERE department IN ('Sales', 'Marketing', 'HR');
```
Returns: Employees in Sales, Marketing, or HR

**With NOT:**
```sql
SELECT * FROM employees
WHERE department NOT IN ('Sales', 'Marketing', 'HR');
```
Returns: Employees in ALL OTHER departments (Engineering, Finance, etc.)

---

### **💡 Best Practice: NOT IN for Multiple Exclusions**

When excluding multiple values, `NOT IN` is the **cleanest and most readable** approach!

**Scenario:** Exclude employees from Marketing and IT departments

**❌ Verbose (using AND):**
```sql
WHERE department != 'Marketing' AND department != 'IT'
```

**✅ Clean (using NOT IN):**
```sql
WHERE department NOT IN ('Marketing', 'IT')
```

**Why NOT IN is better:**
- ✅ More concise
- ✅ Easier to read
- ✅ Scales better (easy to add more values)
- ✅ Industry standard

**Comparison:**

| Number of Exclusions | Using AND | Using NOT IN |
|---------------------|-----------|--------------|
| 2 values | `!= 'A' AND != 'B'` | `NOT IN ('A', 'B')` ✅ |
| 3 values | `!= 'A' AND != 'B' AND != 'C'` | `NOT IN ('A', 'B', 'C')` ✅ |
| 5 values | Very long! | `NOT IN ('A', 'B', 'C', 'D', 'E')` ✅ |

**Real Example:**
```sql
-- Exclude test and internal accounts
SELECT * FROM users
WHERE email NOT IN (
    'test@example.com',
    'admin@example.com',
    'internal@example.com'
);
```

Much cleaner than:
```sql
WHERE email != 'test@example.com' 
  AND email != 'admin@example.com' 
  AND email != 'internal@example.com'
```

---

### **Example 4: NOT with LIKE**

```sql
SELECT * FROM products
WHERE product_name NOT LIKE '%Phone%';
```

Returns: All products that DON'T have "Phone" in their name

---

### **Example 5: NOT with BETWEEN**

```sql
SELECT * FROM orders
WHERE order_amount NOT BETWEEN 100 AND 500;
```

Returns: Orders with amount < 100 OR amount > 500

---

### **Example 6: NOT with NULL**

```sql
SELECT * FROM customers
WHERE email IS NOT NULL;
```

Returns: All customers who HAVE an email address

---

## 💡 When to Use NOT

### **Use NOT when you want to exclude something:**

**Scenario 1: Exclude specific values**
```sql
-- Get all products except Electronics
SELECT * FROM products
WHERE NOT category = 'Electronics';
```

**Scenario 2: Exclude a range**
```sql
-- Get orders outside the normal range
SELECT * FROM orders
WHERE order_amount NOT BETWEEN 50 AND 1000;
```

**Scenario 3: Exclude multiple values**
```sql
-- Get employees not in these departments
SELECT * FROM employees
WHERE department NOT IN ('Sales', 'Marketing');
```

**Scenario 4: Exclude pattern matches**
```sql
-- Get products that don't contain "Pro"
SELECT * FROM products
WHERE product_name NOT LIKE '%Pro%';
```

---

## ⚖️ Operator Precedence

### **What is Operator Precedence?**

When you combine multiple logical operators, SQL evaluates them in a specific order:

**Order (highest to lowest):**
1. **NOT** (evaluated first)
2. **AND** (evaluated second)
3. **OR** (evaluated last)

---

## 🔍 Precedence Examples

### **Example 1: Without Parentheses**

```sql
SELECT * FROM products
WHERE category = 'Electronics' OR category = 'Appliances' AND price > 500;
```

**How SQL reads this:**
1. First: `category = 'Appliances' AND price > 500`
2. Then: `category = 'Electronics' OR [result from step 1]`

**Returns:**
- ALL Electronics (any price)
- Appliances with price > 500

---

### **Example 2: With Parentheses (Explicit Control)**

```sql
SELECT * FROM products
WHERE (category = 'Electronics' OR category = 'Appliances') AND price > 500;
```

**How SQL reads this:**
1. First: `category = 'Electronics' OR category = 'Appliances'`
2. Then: `[result from step 1] AND price > 500`

**Returns:**
- Electronics with price > 500
- Appliances with price > 500

**Different result!**

---

### **Example 3: NOT with AND/OR**

```sql
SELECT * FROM employees
WHERE NOT department = 'Sales' AND salary > 50000;
```

**How SQL reads this:**
1. First: `NOT department = 'Sales'` → (department != 'Sales')
2. Then: `[result from step 1] AND salary > 50000`

**Returns:** Employees NOT in Sales who earn > 50000

---

### **Example 4: Complex Precedence**

```sql
SELECT * FROM orders
WHERE NOT order_status = 'Cancelled' AND order_amount > 1000 OR order_status = 'Processing';
```

**Evaluation order:**
1. `NOT order_status = 'Cancelled'` → (status != 'Cancelled')
2. `[step 1] AND order_amount > 1000`
3. `[step 2] OR order_status = 'Processing'`

**Returns:**
- Orders that are NOT cancelled AND amount > 1000
- OR orders that are Processing (any amount)

---

### **Example 5: Using Parentheses for Clarity**

**Better version of Example 4:**
```sql
SELECT * FROM orders
WHERE (NOT order_status = 'Cancelled' AND order_amount > 1000) 
   OR order_status = 'Processing';
```

Same result, but much clearer to read!

---

## 🎯 Best Practices

### **1. Use Parentheses for Clarity**

**❌ Confusing:**
```sql
WHERE a = 1 OR b = 2 AND c = 3
```

**✅ Clear:**
```sql
WHERE a = 1 OR (b = 2 AND c = 3)
```

---

### **2. NOT vs Comparison Operators**

**Both work, choose what's clearer:**

```sql
-- Using NOT
WHERE NOT price > 100

-- Using comparison
WHERE price <= 100
```

**For IN, use NOT IN:**
```sql
-- ✅ Clear
WHERE department NOT IN ('Sales', 'HR')

-- ❌ Awkward
WHERE NOT (department = 'Sales' OR department = 'HR')
```

---

### **3. NOT with NULL**

**Always use IS NOT NULL:**

```sql
-- ✅ Correct
WHERE email IS NOT NULL

-- ❌ Wrong (won't work!)
WHERE email NOT = NULL
```

---

## 📊 Real-World Examples

### **Example 1: Find Active Users Not from USA**

```sql
SELECT name, country, status
FROM users
WHERE status = 'Active' 
  AND NOT country = 'USA';
```

---

### **Example 2: Products Outside Normal Price Range**

```sql
SELECT product_name, price
FROM products
WHERE price NOT BETWEEN 10 AND 100
  AND category = 'Electronics';
```

Returns expensive or very cheap electronics.

---

### **Example 3: Orders Needing Attention**

```sql
SELECT order_id, order_status, order_amount
FROM orders
WHERE (order_status = 'Pending' AND order_amount > 1000)
   OR (NOT order_status IN ('Completed', 'Cancelled'));
```

Returns:
- High-value pending orders
- OR any orders not completed/cancelled

---

### **Example 4: Exclude Test Accounts**

```sql
SELECT user_id, email, created_at
FROM users
WHERE email NOT LIKE '%@test.com'
  AND email NOT LIKE '%@example.com'
  AND status = 'Active';
```

---

## ✅ Practice Exercises

### **Exercise 1:**
Get all customers NOT from USA, Canada, or Mexico.

<details>
<summary>Solution</summary>

```sql
SELECT * FROM customers
WHERE country NOT IN ('USA', 'Canada', 'Mexico');
```
</details>

---

### **Exercise 2:**
Get products that are NOT in the 'Electronics' category AND cost more than $50.

<details>
<summary>Solution</summary>

```sql
SELECT * FROM products
WHERE NOT category = 'Electronics'
  AND price > 50;
```
</details>

---

### **Exercise 3:**
Get orders that are either:
- High value (> $1000) and NOT cancelled
- OR in Processing status

<details>
<summary>Solution</summary>

```sql
SELECT * FROM orders
WHERE (order_amount > 1000 AND NOT order_status = 'Cancelled')
   OR order_status = 'Processing';
```
</details>

---

## 🎓 Summary

### **NOT Operator:**
- Negates a condition
- Use for "everything except..."
- Works with =, IN, LIKE, BETWEEN, NULL

### **Operator Precedence:**
1. NOT (first)
2. AND (second)
3. OR (last)

### **Best Practice:**
- Use parentheses for clarity
- Test your logic with small datasets first

---

## 📚 Quick Reference

| Operator | Precedence | Example |
|----------|------------|---------|
| NOT | 1 (highest) | `NOT country = 'USA'` |
| AND | 2 | `a = 1 AND b = 2` |
| OR | 3 (lowest) | `a = 1 OR b = 2` |

**Remember:** When in doubt, use parentheses! 🚀
