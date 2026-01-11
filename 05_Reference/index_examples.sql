-- ============================================
-- INDEX EXAMPLES FOR PRACTICE TABLES
-- ============================================
-- This file shows useful indexes for your practice tables
-- and explains WHEN and WHY to create them

-- ============================================
-- WHAT IS AN INDEX?
-- ============================================
-- An index is like a book's index - it helps find data faster
-- WITHOUT index: Database scans EVERY row (slow for large tables)
-- WITH index: Database jumps directly to matching rows (fast!)
--
-- Trade-offs:
-- ✅ Faster SELECT queries (especially with WHERE, JOIN, ORDER BY)
-- ❌ Slower INSERT/UPDATE/DELETE (index needs updating too)
-- ❌ Takes up disk space

-- ============================================
-- INDEXES YOU ALREADY HAVE (Automatic)
-- ============================================
-- PRIMARY KEY columns automatically get indexes:
-- - customers.customer_id
-- - orders.order_id
-- - products.product_id
-- - employees.employee_id
-- - dim_product_nike.entry_id
-- - dim_category_nike.category_id
-- - sales_by_year.year

-- ============================================
-- RECOMMENDED INDEXES FOR YOUR TABLES
-- ============================================

-- 1. ORDERS TABLE - Foreign Key Index
-- WHY: You'll often JOIN orders with customers
-- QUERY: SELECT * FROM orders o JOIN customers c ON o.customer_id = c.customer_id
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- 2. ORDERS TABLE - Date Range Queries
-- WHY: Common to filter by date ranges
-- QUERY: SELECT * FROM orders WHERE order_date BETWEEN '2025-11-01' AND '2025-11-30'
CREATE INDEX idx_orders_date ON orders(order_date);

-- 3. ORDERS TABLE - Status Filtering
-- WHY: Often filter by order status
-- QUERY: SELECT * FROM orders WHERE status = 'Pending'
CREATE INDEX idx_orders_status ON orders(status);

-- 4. CUSTOMERS TABLE - Country Grouping
-- WHY: Grouping or filtering by country
-- QUERY: SELECT country, COUNT(*) FROM customers GROUP BY country
CREATE INDEX idx_customers_country ON customers(country);

-- 5. PRODUCTS TABLE - Category Filtering
-- WHY: Filter products by category
-- QUERY: SELECT * FROM products WHERE category = 'Electronics'
CREATE INDEX idx_products_category ON products(category);

-- 6. EMPLOYEES TABLE - Department Queries
-- WHY: Common to filter or group by department
-- QUERY: SELECT * FROM employees WHERE department = 'Engineering'
CREATE INDEX idx_employees_department ON employees(department);

-- 7. DIM_PRODUCT_NIKE - Category Foreign Key
-- WHY: JOIN with dim_category_nike
-- QUERY: SELECT * FROM dim_product_nike p JOIN dim_category_nike c ON p.category_id = c.category_id
CREATE INDEX idx_nike_product_category ON dim_product_nike(category_id);

-- 8. DIM_PRODUCT_NIKE - Date for YoY Calculations
-- WHY: Extract year from order_date for aggregations
-- QUERY: SELECT EXTRACT(YEAR FROM order_date), SUM(price) FROM dim_product_nike GROUP BY EXTRACT(YEAR FROM order_date)
CREATE INDEX idx_nike_product_order_date ON dim_product_nike(order_date);

-- 9. DIM_PRODUCT_NIKE - Gender Filtering
-- WHY: Filter products by gender
-- QUERY: SELECT * FROM dim_product_nike WHERE gender = 'Female'
CREATE INDEX idx_nike_product_gender ON dim_product_nike(gender);

-- ============================================
-- COMPOSITE INDEXES (Multiple Columns)
-- ============================================
-- Use when you frequently filter by MULTIPLE columns together

-- Example 1: Orders by customer AND date
-- QUERY: SELECT * FROM orders WHERE customer_id = 1 AND order_date > '2025-11-01'
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Example 2: Employees by department AND salary
-- QUERY: SELECT * FROM employees WHERE department = 'Engineering' AND salary > 90000
CREATE INDEX idx_employees_dept_salary ON employees(department, salary);

-- ============================================
-- WHEN NOT TO CREATE INDEXES
-- ============================================
-- ❌ Small tables (< 1000 rows) - Full table scan is fast enough
-- ❌ Columns with very few unique values (e.g., gender with only 2 values)
-- ❌ Columns that are rarely used in WHERE/JOIN/ORDER BY
-- ❌ Tables with frequent INSERT/UPDATE/DELETE operations

-- ============================================
-- HOW TO CHECK IF AN INDEX IS BEING USED
-- ============================================
-- Use EXPLAIN ANALYZE to see query execution plan:

-- Without index (Seq Scan = Sequential Scan = slow):
EXPLAIN ANALYZE
SELECT * FROM orders WHERE status = 'Pending';

-- With index (Index Scan = fast):
-- After creating idx_orders_status, run the same query

-- ============================================
-- HOW TO DROP AN INDEX
-- ============================================
-- If you want to remove an index:
-- DROP INDEX idx_orders_customer_id;

-- ============================================
-- PRACTICE EXERCISE
-- ============================================
-- 1. Create the idx_orders_customer_id index
-- 2. Run this query WITHOUT the index:
--    EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 1;
-- 3. Create the index
-- 4. Run the same query again and compare the execution plan
-- 5. Look for "Seq Scan" vs "Index Scan" in the output

-- ============================================
-- SUMMARY: INDEXES FOR YOUR PRACTICE TABLES
-- ============================================
-- For learning purposes, these are the MOST USEFUL indexes:
--
-- 1. orders(customer_id)     - For JOINs with customers
-- 2. orders(order_date)      - For date range queries
-- 3. employees(department)   - For department grouping
-- 4. products(category)      - For category filtering
-- 5. dim_product_nike(order_date) - For YoY calculations
--
-- Start with these 5 and add more as you encounter slow queries!
