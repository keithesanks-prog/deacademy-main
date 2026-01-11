# Subqueries Explained Simply

## What Even IS a Subquery?

**A subquery is just a question inside another question.**

Think of it like this conversation:

> **You:** "Show me all the tall people"  
> **Friend:** "How tall is 'tall'?"  
> **You:** "Taller than average"  
> **Friend:** "What's the average?"  
> **You:** "Add up everyone's height and divide by how many people there are"

**In SQL, you can answer BOTH questions in one go:**

```sql
-- Outer question: Show me tall people
SELECT name, height
FROM people
WHERE height > (
    -- Inner question: What's average height?
    SELECT AVG(height) FROM people
);
```

---

## The Restaurant Menu Analogy

Imagine you're at a restaurant and you ask:

**"What dishes cost less than the average price?"**

### Step 1: What's the average price?

First, you'd need to calculate it:
- Burger: $12
- Pizza: $15
- Salad: $8
- Steak: $25

**Average = ($12 + $15 + $8 + $25) / 4 = $15**

### Step 2: Which dishes are below $15?

- Burger: $12 ✅ (less than $15)
- Pizza: $15 ❌ (equal, not less)
- Salad: $8 ✅ (less than $15)
- Steak: $25 ❌ (more than $15)

**Answer: Burger and Salad**

### In SQL:

```sql
SELECT dish_name, price
FROM menu
WHERE price < (
    SELECT AVG(price) FROM menu
);
```

**The subquery `(SELECT AVG(price) FROM menu)` just calculates ONE number: $15**

Then the outer query uses that number!

---

## Rule #1: Subqueries Run FIRST

**Think of subqueries like doing math in parentheses:**

```
5 + (3 × 2) = ?
```

You do `(3 × 2)` FIRST → get 6  
Then: `5 + 6 = 11`

**Same with SQL:**

```sql
SELECT * FROM customers
WHERE total > (SELECT AVG(total) FROM orders);
```

1. **Inner query runs first:** `SELECT AVG(total) FROM orders` → returns 374.16
2. **Outer query uses that:** `WHERE total > 374.16`

---

## The Three Types of Subqueries

### Type 1: Single Value (Scalar)

**Returns ONE number**

```sql
-- Question: "What's the average order amount?"
SELECT AVG(order_amount) FROM orders;
-- Answer: 374.16
```

**Used like:**
```sql
WHERE order_amount > (SELECT AVG(order_amount) FROM orders)
--                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
--                    This returns ONE number: 374.16
```

**Real-world example:**
"Show me products more expensive than the average product"

---

### Type 2: List of Values (Column)

**Returns MULTIPLE values in one column**

```sql
-- Question: "Which customer IDs have placed orders?"
SELECT DISTINCT customer_id FROM orders;
-- Answer: 1, 2, 3, 4, 5, 6, 7, 8 (a list)
```

**Used with IN:**
```sql
SELECT * FROM customers
WHERE customer_id IN (SELECT DISTINCT customer_id FROM orders);
--                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
--                    This returns a LIST: (1, 2, 3, 4, 5, 6, 7, 8)
```

**Real-world example:**
"Show me customers who have actually ordered something"

---

### Type 3: Table (Multiple Rows & Columns)

**Returns a whole temporary table**

```sql
-- Question: "What's each customer's total spending?"
SELECT customer_id, SUM(order_amount) as total
FROM orders
GROUP BY customer_id;

-- Answer: A table!
-- customer_id | total
-- ------------|-------
-- 1           | 901.25
-- 2           | 215.00
-- 3           | 700.50
```

**Used in FROM:**
```sql
SELECT AVG(total)
FROM (
    SELECT customer_id, SUM(order_amount) as total
    FROM orders
    GROUP BY customer_id
);
--   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
--   This returns a TEMPORARY TABLE
```

**Real-world example:**
"What's the average customer's total spending?"

---

## Let's Build a Subquery Step-by-Step

**Problem:** Find customers who spent more than average

### Step 1: Run the Inner Query ALONE

```sql
-- How much did each customer spend?
SELECT customer_id, SUM(order_amount) as total
FROM orders
GROUP BY customer_id;
```

**Result:**
```
customer_id | total
------------|-------
1           | 901.25
2           | 215.00
3           | 700.50
4           | 45.00
5           | 245.00
```

**Test this first!** Make sure it works.

---

### Step 2: Wrap It to Get the Average

```sql
-- What's the average of those totals?
SELECT AVG(total)
FROM (
    -- This is Step 1's query!
    SELECT customer_id, SUM(order_amount) as total
    FROM orders
    GROUP BY customer_id
);
```

**Result:**
```
AVG(total)
----------
374.16
```

**Test this second!** You should get one number.

---

### Step 3: Use That Number in the Main Query

```sql
-- Who spent more than 374.16?
SELECT c.customer_name, SUM(o.order_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(o.order_amount) > 374.16;  -- Hardcoded for now
```

**Result:**
```
customer_name | total_spent
--------------|------------
Alice Johnson | 901.25
Carol White   | 700.50
Frank Miller  | 585.50
```

**Test this third!** Make sure the logic works.

---

### Step 4: Replace Hardcoded Number with Subquery

```sql
-- Final query: Replace 374.16 with Step 2's query
SELECT c.customer_name, SUM(o.order_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(o.order_amount) > (
    -- This is Step 2's query!
    SELECT AVG(total)
    FROM (
        SELECT customer_id, SUM(order_amount) as total
        FROM orders
        GROUP BY customer_id
    )
);
```

**That's it!** You just replaced `374.16` with the query that calculates it.

---

## The Key Insight

**Subqueries are just placeholders for values!**

```sql
-- These are THE SAME:
WHERE price > 15
WHERE price > (SELECT AVG(price) FROM menu)
--            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
--            This just calculates 15 for you!
```

**Think of it like variables in math:**

```
x = 5
y = x + 3

-- Is the same as:
y = (5) + 3
```

The `(5)` is like a subquery - it's just the value of `x`!

---

## Common Subquery Patterns

### Pattern 1: Above/Below Average

```sql
-- Find products more expensive than average
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

**What the subquery does:** Calculates one number (the average)

---

### Pattern 2: In a List

```sql
-- Find customers who have ordered
SELECT customer_name
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id FROM orders
);
```

**What the subquery does:** Returns a list of IDs

---

### Pattern 3: Doesn't Exist

```sql
-- Find products never ordered
SELECT product_name
FROM products
WHERE product_id NOT IN (
    SELECT DISTINCT product_id FROM order_items
);
```

**What the subquery does:** Returns a list of product IDs that WERE ordered  
**NOT IN:** Finds products NOT in that list

---

### Pattern 4: Comparing to Group Average

```sql
-- Find employees earning more than their department average
SELECT e1.employee_name, e1.salary
FROM employees e1
WHERE e1.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department_id = e1.department_id
);
```

**What the subquery does:** For EACH employee, calculates their department's average  
**This is called a CORRELATED subquery** (runs once per row)

---

## How to Read Complex Subqueries

**Start from the INSIDE and work OUT:**

```sql
SELECT c.customer_name, SUM(o.order_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(o.order_amount) > (
    SELECT AVG(total)              -- ← Read this SECOND
    FROM (
        SELECT SUM(order_amount) as total  -- ← Read this FIRST
        FROM orders
        GROUP BY customer_id
    )
);
```

**Reading order:**
1. **Innermost:** Sum orders per customer → Creates `total` column
2. **Middle:** Average those totals → Returns one number
3. **Outer:** Keep customers above that number

---

## Practice: Break It Down

When you see a confusing subquery, **run each piece separately:**

### Original (Confusing):
```sql
SELECT name FROM customers
WHERE id IN (
    SELECT customer_id FROM orders
    WHERE order_date > '2024-01-01'
);
```

### Break It Down:

**Step 1: Run the subquery alone**
```sql
SELECT customer_id FROM orders
WHERE order_date > '2024-01-01';
-- Result: 1, 3, 5, 7
```

**Step 2: Use that result**
```sql
SELECT name FROM customers
WHERE id IN (1, 3, 5, 7);  -- Same as the subquery!
```

**See? The subquery just gives you a list!**

---

## Common Mistakes

### Mistake 1: Using Aggregate in WHERE

```sql
-- ❌ WRONG
SELECT customer_name
FROM customers
WHERE SUM(order_amount) > 100;  -- Can't use SUM in WHERE!

-- ✅ CORRECT
SELECT customer_name
FROM customers
GROUP BY customer_name
HAVING SUM(order_amount) > 100;  -- Use HAVING for aggregates
```

---

### Mistake 2: Forgetting GROUP BY

```sql
-- ❌ WRONG
SELECT customer_name, SUM(order_amount)
FROM orders;  -- Error! Need GROUP BY

-- ✅ CORRECT
SELECT customer_name, SUM(order_amount)
FROM orders
GROUP BY customer_name;
```

---

### Mistake 3: Subquery Returns Multiple Values

```sql
-- ❌ WRONG
WHERE price > (SELECT price FROM products);  -- Returns MANY prices!

-- ✅ CORRECT (use IN for multiple values)
WHERE price IN (SELECT price FROM products);

-- ✅ CORRECT (use aggregate for one value)
WHERE price > (SELECT AVG(price) FROM products);
```

---

## The Bottom Line

**Subqueries are just questions that answer other questions.**

1. **Test the inner query first** - Make sure it works alone
2. **See what it returns** - One value? A list? A table?
3. **Use it appropriately** - `>` for one value, `IN` for a list, `FROM` for a table
4. **Read inside-out** - Start with the innermost query

**You already know how to write queries. Subqueries are just putting one query inside another!**

---

## Next Steps

1. Run the step-by-step examples in this guide
2. Practice breaking down complex subqueries
3. Try the practice problems one at a time
4. When stuck, run each piece separately!

**You've got this!** 🚀
