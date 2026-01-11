# Subquery Practice Solutions

## Level 1: Basic Subqueries

### Problem 1: Customers Above Average Spending

**Solution:**
```sql
SELECT c.customer_name, SUM(o.order_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(o.order_amount) > (
    SELECT AVG(total_per_customer)
    FROM (
        SELECT SUM(order_amount) as total_per_customer
        FROM orders
        GROUP BY customer_id
    )
);
```

**Explanation:**
- Inner subquery: Calculate total spending per customer
- Middle subquery: Find average of those totals
- Outer query: Find customers above that average

**Alternative (simpler but different logic):**
```sql
SELECT c.customer_name, SUM(o.order_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(o.order_amount) > (SELECT AVG(order_amount) FROM orders);
```

---

### Problem 2: Products Never Ordered

**Solution:**
```sql
SELECT product_id, product_name, category
FROM products
WHERE product_id NOT IN (
    SELECT DISTINCT product_id 
    FROM order_items
);
```

**Explanation:**
- Subquery: Get all product_ids that have been ordered
- Outer query: Find products NOT in that list

**Alternative using NOT EXISTS:**
```sql
SELECT p.product_id, p.product_name, p.category
FROM products p
WHERE NOT EXISTS (
    SELECT 1 
    FROM order_items oi 
    WHERE oi.product_id = p.product_id
);
```

---

### Problem 3: Customers with No Orders

**Solution:**
```sql
SELECT customer_id, customer_name, email
FROM customers
WHERE customer_id NOT IN (
    SELECT DISTINCT customer_id 
    FROM orders
);
```

**Explanation:**
- Subquery: Get all customer_ids who have placed orders
- Outer query: Find customers NOT in that list

**Alternative using LEFT JOIN:**
```sql
SELECT c.customer_id, c.customer_name, c.email
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

---

## Level 2: Subqueries with Aggregates

### Problem 4: Top Spending Customer

**Solution:**
```sql
SELECT c.customer_name, SUM(o.order_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(o.order_amount) = (
    SELECT MAX(total)
    FROM (
        SELECT SUM(order_amount) as total
        FROM orders
        GROUP BY customer_id
    )
);
```

**Explanation:**
- Inner subquery: Calculate total per customer
- Middle subquery: Find MAX of those totals
- Outer query: Find customer(s) with that max total

**Alternative using ORDER BY LIMIT:**
```sql
SELECT c.customer_name, SUM(o.order_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC
LIMIT 1;
```

---

### Problem 5: Departments Above Average Salary

**Solution:**
```sql
SELECT d.department_name, AVG(e.salary) as avg_salary
FROM departments d
JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name
HAVING AVG(e.salary) > (
    SELECT AVG(salary) 
    FROM employees
);
```

**Explanation:**
- Subquery: Calculate company-wide average salary
- Outer query: Group by department, filter to those above company average

---

### Problem 6: Products More Expensive Than Category Average

**Solution:**
```sql
SELECT p1.product_name, p1.category, p1.price,
       (SELECT AVG(price) FROM products p2 WHERE p2.category = p1.category) as category_avg
FROM products p1
WHERE p1.price > (
    SELECT AVG(p2.price)
    FROM products p2
    WHERE p2.category = p1.category
);
```

**Explanation:**
- This is a **correlated subquery** - it runs for each row in outer query
- For each product, calculate average price in its category
- Keep only products above their category average

---

## Level 3: Multiple Subqueries

### Problem 7: Customers Who Ordered Electronics

**Solution:**
```sql
SELECT DISTINCT c.customer_name, c.email
FROM customers c
WHERE c.customer_id IN (
    SELECT o.customer_id
    FROM orders o
    WHERE o.order_id IN (
        SELECT oi.order_id
        FROM order_items oi
        WHERE oi.product_id IN (
            SELECT p.product_id
            FROM products p
            WHERE p.category = 'Electronics'
        )
    )
);
```

**Explanation:**
- Innermost: Find Electronics product IDs
- Middle: Find order_ids containing those products
- Next: Find customer_ids with those orders
- Outer: Get customer details

**Alternative using JOINs (more efficient):**
```sql
SELECT DISTINCT c.customer_name, c.email
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE p.category = 'Electronics';
```

---

### Problem 8: Employees Earning More Than Their Department Average

**Solution:**
```sql
SELECT e1.employee_name, e1.salary, d.department_name,
       (SELECT AVG(e2.salary) 
        FROM employees e2 
        WHERE e2.department_id = e1.department_id) as dept_avg
FROM employees e1
JOIN departments d ON e1.department_id = d.department_id
WHERE e1.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department_id = e1.department_id
);
```

**Explanation:**
- Correlated subquery calculates average for each employee's department
- Compare employee's salary to their department average

---

### Problem 9: Top 3 Products by Revenue

**Solution:**
```sql
SELECT p.product_name, revenue
FROM (
    SELECT oi.product_id, SUM(oi.quantity * oi.item_price) as revenue
    FROM order_items oi
    GROUP BY oi.product_id
    ORDER BY revenue DESC
    LIMIT 3
) top_products
JOIN products p ON top_products.product_id = p.product_id
ORDER BY revenue DESC;
```

**Explanation:**
- Subquery: Calculate total revenue per product
- Order by revenue and limit to top 3
- Join with products table to get product names

---

## Level 4: Advanced Subqueries

### Problem 10: Customers Who Spent More in Q1 Than Q2

**Solution:**
```sql
SELECT c.customer_name,
       q1.total as q1_spending,
       COALESCE(q2.total, 0) as q2_spending
FROM customers c
LEFT JOIN (
    SELECT customer_id, SUM(order_amount) as total
    FROM orders
    WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31'
    GROUP BY customer_id
) q1 ON c.customer_id = q1.customer_id
LEFT JOIN (
    SELECT customer_id, SUM(order_amount) as total
    FROM orders
    WHERE order_date BETWEEN '2024-04-01' AND '2024-06-30'
    GROUP BY customer_id
) q2 ON c.customer_id = q2.customer_id
WHERE q1.total > COALESCE(q2.total, 0);
```

**Explanation:**
- First subquery: Calculate Q1 totals
- Second subquery: Calculate Q2 totals
- Compare Q1 > Q2 (use COALESCE for customers with no Q2 orders)

---

### Problem 11: Departments with All High Earners

**Solution:**
```sql
SELECT d.department_name
FROM departments d
WHERE NOT EXISTS (
    SELECT 1
    FROM employees e
    WHERE e.department_id = d.department_id
    AND e.salary <= 60000
);
```

**Explanation:**
- Use NOT EXISTS to check if ANY employee earns <= 60000
- If no such employee exists, ALL employees earn > 60000

---

### Problem 12: Customers Who Ordered Every Electronics Product

**Solution:**
```sql
SELECT c.customer_name
FROM customers c
WHERE (
    SELECT COUNT(DISTINCT oi.product_id)
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.customer_id = c.customer_id
    AND p.category = 'Electronics'
) = (
    SELECT COUNT(*)
    FROM products
    WHERE category = 'Electronics'
);
```

**Explanation:**
- First subquery: Count distinct Electronics products this customer ordered
- Second subquery: Count total Electronics products
- Keep customers where these counts match

---

## Bonus Challenges

### Challenge 1: Second Highest Spender

**Solution:**
```sql
SELECT c.customer_name, SUM(o.order_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC
LIMIT 1 OFFSET 1;
```

**Alternative using subquery:**
```sql
SELECT c.customer_name, SUM(o.order_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(o.order_amount) = (
    SELECT MAX(total)
    FROM (
        SELECT SUM(order_amount) as total
        FROM orders
        GROUP BY customer_id
        ORDER BY total DESC
        LIMIT 1 OFFSET 1
    )
);
```

---

### Challenge 2: Employees Earning More Than Their Manager

**Solution:**
```sql
SELECT e1.employee_name, e1.salary as employee_salary,
       e2.employee_name as manager_name, e2.salary as manager_salary
FROM employees e1
JOIN employees e2 ON e1.manager_id = e2.employee_id
WHERE e1.salary > e2.salary;
```

**Using subquery:**
```sql
SELECT e1.employee_name, e1.salary
FROM employees e1
WHERE e1.salary > (
    SELECT e2.salary
    FROM employees e2
    WHERE e2.employee_id = e1.manager_id
);
```

---

### Challenge 3: Products Ordered by All Top Spenders

**Solution:**
```sql
SELECT p.product_name
FROM products p
WHERE (
    -- Count how many top spenders ordered this product
    SELECT COUNT(DISTINCT o.customer_id)
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE oi.product_id = p.product_id
    AND o.customer_id IN (
        -- Top 25% of spenders
        SELECT customer_id
        FROM (
            SELECT customer_id, SUM(order_amount) as total
            FROM orders
            GROUP BY customer_id
            ORDER BY total DESC
            LIMIT (SELECT COUNT(DISTINCT customer_id) / 4 FROM orders)
        )
    )
) = (
    -- Total count of top spenders
    SELECT COUNT(DISTINCT customer_id)
    FROM (
        SELECT customer_id, SUM(order_amount) as total
        FROM orders
        GROUP BY customer_id
        ORDER BY total DESC
        LIMIT (SELECT COUNT(DISTINCT customer_id) / 4 FROM orders)
    )
);
```

**Explanation:**
- Very complex! Multiple nested subqueries
- Find top 25% spenders
- For each product, count how many top spenders ordered it
- Keep products where count = total top spenders

---

## Key Takeaways

1. **Test subqueries independently** before nesting
2. **Correlated subqueries** run for each outer row (can be slow)
3. **JOINs are often faster** than subqueries for large datasets
4. **Use EXISTS** instead of IN for better performance
5. **EXPLAIN your queries** to understand execution plans

---

## Performance Comparison

### Subquery vs JOIN

**Subquery (can be slower):**
```sql
SELECT * FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders);
```

**JOIN (usually faster):**
```sql
SELECT DISTINCT c.*
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;
```

**EXISTS (often fastest):**
```sql
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```

---

Great job working through these! 🎉
