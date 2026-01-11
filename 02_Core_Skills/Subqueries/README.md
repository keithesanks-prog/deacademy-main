# Subqueries Training Module

## Overview

Learn how to use subqueries (queries within queries) to solve complex SQL problems. Subqueries let you break down complicated questions into smaller, manageable pieces.

---

## What Are Subqueries?

**A subquery is a query nested inside another query.**

Think of it like asking a question that depends on the answer to another question:
- "Show me customers who spent more than average" → First find the average, then find who's above it
- "Find products never ordered" → First find all ordered products, then find what's NOT in that list

---

## Quick Start

### 1. Setup Database
```bash
# In your SQL editor, run:
.read subquery_database_setup.sql
```

This creates 6 tables with sample data:
- **customers** - 10 customers
- **orders** - 17 orders
- **products** - 12 products
- **order_items** - Order details
- **employees** - 18 employees
- **departments** - 5 departments

### 2. Start Practicing
Open `subquery_practice_problems.md` and work through the problems!

---

## Learning Path

### Level 1: Basic Subqueries
- Using `IN` and `NOT IN`
- Simple comparisons with subqueries
- Finding items that don't exist

### Level 2: Subqueries with Aggregates
- Comparing to `AVG()`, `MAX()`, `MIN()`
- Using `GROUP BY` with `HAVING`
- Finding top performers

### Level 3: Multiple Subqueries
- Chaining subqueries
- Correlated subqueries
- Complex filtering

### Level 4: Advanced
- Multiple conditions
- Set operations
- Performance optimization

---

## Key Concepts

### Types of Subqueries

| Type | Returns | Example Use |
|------|---------|-------------|
| **Scalar** | Single value | `WHERE price > (SELECT AVG(price)...)` |
| **Row** | Single row | `WHERE (col1, col2) = (SELECT...)` |
| **Column** | List of values | `WHERE id IN (SELECT id...)` |
| **Table** | Multiple rows/cols | `FROM (SELECT...) AS subquery` |

### Subquery Locations

```sql
-- In SELECT clause
SELECT name, (SELECT COUNT(*) FROM orders WHERE...) AS order_count
FROM customers;

-- In FROM clause
SELECT * 
FROM (SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id) AS totals;

-- In WHERE clause
SELECT * FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders);

-- In HAVING clause
SELECT department, AVG(salary)
FROM employees
GROUP BY department
HAVING AVG(salary) > (SELECT AVG(salary) FROM employees);
```

---

## Common Patterns

### Pattern 1: Above Average
```sql
-- Find items above average
SELECT * FROM table
WHERE value > (SELECT AVG(value) FROM table);
```

### Pattern 2: Not Exists
```sql
-- Find items with no related records
SELECT * FROM table1
WHERE NOT EXISTS (
    SELECT 1 FROM table2 
    WHERE table2.id = table1.id
);
```

### Pattern 3: Top N
```sql
-- Find top performers
SELECT * FROM (
    SELECT *, RANK() OVER (ORDER BY value DESC) as rnk
    FROM table
)
WHERE rnk <= 3;
```

### Pattern 4: Correlated Subquery
```sql
-- Compare to group average
SELECT * FROM employees e1
WHERE salary > (
    SELECT AVG(salary) 
    FROM employees e2 
    WHERE e2.department_id = e1.department_id
);
```

---

## Subqueries vs Window Functions

You've learned `ROW_NUMBER()` - here's how it compares:

| Task | Window Function | Subquery |
|------|----------------|----------|
| **Top 3 per group** | `ROW_NUMBER() OVER (PARTITION BY...)` | Subquery with GROUP BY |
| **Above average** | Can't do easily | `WHERE > (SELECT AVG...)` |
| **Ranking** | ✅ Better choice | Possible but complex |
| **Filtering** | ❌ Can't filter directly | ✅ Better choice |

**Use window functions for:** Ranking, running totals, row numbering  
**Use subqueries for:** Filtering, comparisons, existence checks

---

## Performance Tips

### ✅ Good Practices
- Use `EXISTS` instead of `IN` for large datasets
- Index columns used in subquery joins
- Test subquery independently first
- Use `EXPLAIN` to check query plan

### ❌ Avoid
- Correlated subqueries in SELECT (runs for each row!)
- Subqueries that return huge result sets
- Multiple levels of nesting (hard to read)

---

## Files in This Module

| File | Purpose |
|------|---------|
| `README.md` | This file - overview and guide |
| `subquery_database_setup.sql` | Creates sample database |
| `subquery_practice_problems.md` | 15 practice problems |
| `subquery_solutions.md` | Solutions with explanations |
| `subquery_vs_joins.md` | When to use each |

---

## Practice Workflow

1. **Run setup** - Load the sample database
2. **Read the problem** - Understand what's being asked
3. **Plan your approach** - What data do you need first?
4. **Write inner query** - Test it separately
5. **Wrap in outer query** - Combine the pieces
6. **Verify results** - Does it make sense?
7. **Check solution** - Compare with provided answer

---

## Example Walkthrough

**Problem:** Find customers who spent more than average

**Step 1: What's the average?**
```sql
SELECT AVG(order_amount) FROM orders;
-- Result: 175.50
```

**Step 2: Who's above that?**
```sql
SELECT customer_id, SUM(order_amount) as total
FROM orders
GROUP BY customer_id
HAVING SUM(order_amount) > 175.50;
```

**Step 3: Combine (replace hardcoded value with subquery)**
```sql
SELECT customer_id, SUM(order_amount) as total
FROM orders
GROUP BY customer_id
HAVING SUM(order_amount) > (SELECT AVG(order_amount) FROM orders);
```

**Step 4: Add customer names**
```sql
SELECT c.customer_name, SUM(o.order_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(o.order_amount) > (SELECT AVG(order_amount) FROM orders);
```

---

## Connection to Other Topics

### Builds On
- Basic SELECT queries
- Aggregate functions (SUM, AVG, COUNT)
- GROUP BY and HAVING
- JOINs

### Prepares You For
- Complex data analysis
- Reporting queries
- Data warehouse queries
- Advanced SQL optimization

---

## Next Steps

1. Complete all Level 1 problems
2. Move to Level 2 when comfortable
3. Try rewriting subqueries as JOINs
4. Compare performance with EXPLAIN
5. Create your own practice problems

**Ready to start? Open `subquery_practice_problems.md`!** 🚀
