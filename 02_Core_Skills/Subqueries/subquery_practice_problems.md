# Subquery Practice Problems

## Setup

First, run the database setup:
```sql
-- Run this file first:
.read subquery_database_setup.sql
```

---

## Level 1: Basic Subqueries

### Problem 1: Customers Above Average Spending
Find all customers whose total order amount is above the average.

**Hint:** You'll need:
- Inner query: Calculate average total spending per customer
- Outer query: Find customers above that average

**Your answer:**
```sql
-- Write your query here


```

---

### Problem 2: Products Never Ordered
Find all products that have never been ordered.

**Hint:** Use `NOT IN` with a subquery

**Your answer:**
```sql
-- Write your query here


```

---

### Problem 3: Customers with No Orders
Find all customers who haven't placed any orders yet.

**Hint:** Similar to Problem 2

**Your answer:**
```sql
-- Write your query here


```

---

## Level 2: Subqueries with Aggregates

### Problem 4: Top Spending Customer
Find the customer who has spent the most money (highest total order amount).

**Hint:** Use a subquery to find the MAX total, then find who has that total

**Your answer:**
```sql
-- Write your query here


```

---

### Problem 5: Departments Above Average Salary
Find all departments where the average salary is above the company-wide average salary.

**Hint:** 
- Inner query: Calculate company-wide average
- Outer query: GROUP BY department, HAVING avg > company avg

**Your answer:**
```sql
-- Write your query here


```

---

### Problem 6: Products More Expensive Than Category Average
Find all products that are more expensive than the average price in their category.

**Hint:** Use a correlated subquery (subquery references outer query)

**Your answer:**
```sql
-- Write your query here


```

---

## Level 3: Multiple Subqueries

### Problem 7: Customers Who Ordered Electronics
Find all customers who have ordered at least one product from the 'Electronics' category.

**Hint:** Chain subqueries through order_items → products

**Your answer:**
```sql
-- Write your query here


```

---

### Problem 8: Employees Earning More Than Their Department Average
Find all employees who earn more than the average salary in their department.

**Hint:** Correlated subquery comparing to department average

**Your answer:**
```sql
-- Write your query here


```

---

### Problem 9: Top 3 Products by Revenue
Find the top 3 products by total revenue (quantity × price across all orders).

**Hint:** 
- Calculate revenue per product in subquery
- Order and limit in outer query

**Your answer:**
```sql
-- Write your query here


```

---

## Level 4: Advanced Subqueries

### Problem 10: Customers Who Spent More in Q1 Than Q2
Find customers whose total spending in Q1 2024 (Jan-Mar) was greater than their Q2 2024 (Apr-Jun) spending.

**Hint:** Use two subqueries to calculate Q1 and Q2 totals separately

**Your answer:**
```sql
-- Write your query here


```

---

### Problem 11: Departments with All High Earners
Find departments where ALL employees earn more than $60,000.

**Hint:** Use `NOT EXISTS` to check if any employee earns <= 60000

**Your answer:**
```sql
-- Write your query here


```

---

### Problem 12: Customers Who Ordered Every Electronics Product
Find customers who have ordered at least one of EVERY product in the Electronics category.

**Hint:** Count distinct electronics products ordered = total electronics products

**Your answer:**
```sql
-- Write your query here


```

---

## Bonus Challenges

### Challenge 1: Second Highest Spender
Find the customer with the second-highest total order amount.

**Hint:** Use LIMIT and OFFSET, or a subquery with MAX excluding the top spender

**Your answer:**
```sql
-- Write your query here


```

---

### Challenge 2: Employees Earning More Than Their Manager
Find all employees who earn more than their manager.

**Hint:** Self-join or correlated subquery on manager_id

**Your answer:**
```sql
-- Write your query here


```

---

### Challenge 3: Products Ordered by All Top Spenders
Find products that have been ordered by ALL customers in the top 25% of spenders.

**Hint:** Very tricky! Requires multiple subqueries and set operations

**Your answer:**
```sql
-- Write your query here


```

---

## Tips for Success

1. **Start with the inner query** - Test it separately first
2. **Use aliases** - Make your subqueries readable with AS
3. **Check your logic** - Does the subquery return what you expect?
4. **Test incrementally** - Build complex queries step by step
5. **Use EXPLAIN** - Understand how the database executes your query

---

## Common Patterns

### Pattern 1: IN / NOT IN
```sql
SELECT * FROM table1
WHERE column IN (SELECT column FROM table2);
```

### Pattern 2: Comparison with Aggregate
```sql
SELECT * FROM table
WHERE value > (SELECT AVG(value) FROM table);
```

### Pattern 3: Correlated Subquery
```sql
SELECT * FROM outer_table o
WHERE value > (
    SELECT AVG(value) 
    FROM inner_table i 
    WHERE i.group_id = o.group_id
);
```

### Pattern 4: EXISTS / NOT EXISTS
```sql
SELECT * FROM table1 t1
WHERE EXISTS (
    SELECT 1 FROM table2 t2 
    WHERE t2.id = t1.id
);
```

---

## Next Steps

After completing these problems:
1. Check your answers against the solutions file
2. Try rewriting subqueries as JOINs (and vice versa)
3. Use EXPLAIN to compare performance
4. Create your own practice problems!
