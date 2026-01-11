# 🎧 SQL Subqueries - Audio Lesson Companion

**This guide matches the audio lesson script. Follow along as you listen!**

---

## 🧩 What is a Subquery?

A **query nested inside another query**.
Think of it like a Russian nesting doll 🪆.

**Common Uses:**
- "Who earns more than average?"
- "Which products have never been ordered?"

---

## 1️⃣ Type 1: Single Row Subquery

**Returns:** One single value (e.g., `50.00`).
**Operators:** `=`, `>`, `<`, `>=`, `<=`

**Example:** Find products cheaper than the average price.

```sql
SELECT product_name, price 
FROM products 
WHERE price < (
    SELECT AVG(price) FROM products  -- Returns one value (e.g., 50)
);
```

---

## 2️⃣ Type 2: Multiple Row Subquery

**Returns:** A list of values (e.g., `101, 102, 105`).
**Operators:** `IN`, `NOT IN`

**Example:** Find orders from customers in the USA.

```sql
SELECT order_id 
FROM orders 
WHERE customer_id IN (
    SELECT customer_id 
    FROM customers 
    WHERE country = 'USA'  -- Returns a list of IDs
);
```

---

## 3️⃣ Type 3: Correlated Subquery (The Tricky One!)

**Key Feature:** The inner query **depends** on the outer query.
**Execution:** Runs once for **every single row** (can be slow!).

**Example:** Find employees who earn more than the average **for their department**.

```sql
SELECT employee_name, salary 
FROM employees E  -- Outer Table Alias
WHERE salary > (
    SELECT AVG(salary) 
    FROM employees 
    WHERE department_id = E.department_id  -- Links to Outer Table
);
```

---

## 4️⃣ Type 4: Subqueries with EXISTS

**Returns:** `TRUE` or `FALSE`.
**Purpose:** Checks if a record exists.

**Example:** Find products that have at least one order.

```sql
SELECT product_name 
FROM products P
WHERE EXISTS (
    SELECT 1 
    FROM orders O 
    WHERE O.product_id = P.product_id
);
```

---

## 💡 Key Takeaways

1.  **Parentheses**: Subqueries always go inside `( )`.
2.  **Single Row**: Use standard comparison (`=`, `>`, `<`).
3.  **Multiple Row**: Use `IN`.
4.  **Correlated**: Links inner & outer queries (runs repeatedly).

---

## 🚀 Visual Summary

| Type | Returns | Operator | Example |
|------|---------|----------|---------|
| **Single Row** | One Value | `=`, `>` | Price > Avg Price |
| **Multi Row** | List of Values | `IN` | Customer IN (USA List) |
| **Correlated** | Value per Row | Any | Salary > Dept Avg |
| **EXISTS** | True/False | `EXISTS` | Has Orders? |
