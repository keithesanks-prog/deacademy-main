# 📚 SQL Data Manipulation Guide
## INSERT, UPDATE, DELETE, ALTER

---

## 🎯 Overview

SQL has different types of commands:
- **SELECT** - Read data (you already know this!)
- **INSERT** - Add new rows
- **UPDATE** - Modify existing rows
- **DELETE** - Remove rows
- **ALTER** - Modify table structure

---

## ➕ INSERT - Adding New Data

### **Basic Syntax:**
```sql
INSERT INTO table_name (column1, column2, column3)
VALUES (value1, value2, value3);
```

---

### **Example 1: Insert a Single Row**

**Table: customers**
| customer_id | name | email | city |
|-------------|------|-------|------|
| 1 | Alice | alice@email.com | NYC |

**Add a new customer:**
```sql
INSERT INTO customers (customer_id, name, email, city)
VALUES (2, 'Bob', 'bob@email.com', 'LA');
```

**Result:**
| customer_id | name | email | city |
|-------------|------|-------|------|
| 1 | Alice | alice@email.com | NYC |
| 2 | Bob | bob@email.com | LA |

---

### **Example 2: Insert Multiple Rows**

```sql
INSERT INTO customers (customer_id, name, email, city)
VALUES 
    (3, 'Carol', 'carol@email.com', 'Chicago'),
    (4, 'David', 'david@email.com', 'Boston'),
    (5, 'Eve', 'eve@email.com', 'Seattle');
```

**Result:** 3 new rows added at once!

---

### **Example 3: Insert Without Specifying All Columns**

If some columns have default values or allow NULL:

```sql
INSERT INTO customers (customer_id, name, email)
VALUES (6, 'Frank', 'frank@email.com');
-- city will be NULL or default value
```

---

### **Example 4: Insert from Another Table**

```sql
INSERT INTO archived_customers (customer_id, name, email, city)
SELECT customer_id, name, email, city
FROM customers
WHERE created_at < '2020-01-01';
```

Copies old customers to archive table.

---

## ✏️ UPDATE - Modifying Existing Data

### **Basic Syntax:**
```sql
UPDATE table_name
SET column1 = value1, column2 = value2
WHERE condition;
```

⚠️ **CRITICAL:** Always use WHERE! Without it, you'll update ALL rows!

---

### **Example 1: Update a Single Row**

**Before:**
| customer_id | name | email | city |
|-------------|------|-------|------|
| 2 | Bob | bob@email.com | LA |

**Update Bob's city:**
```sql
UPDATE customers
SET city = 'San Francisco'
WHERE customer_id = 2;
```

**After:**
| customer_id | name | email | city |
|-------------|------|-------|------|
| 2 | Bob | bob@email.com | San Francisco |

---

### **Example 2: Update Multiple Columns**

```sql
UPDATE customers
SET 
    email = 'bob.new@email.com',
    city = 'San Diego'
WHERE customer_id = 2;
```

---

### **Example 3: Update Multiple Rows**

```sql
UPDATE customers
SET city = 'Remote'
WHERE city IS NULL;
```

Updates all customers with no city to 'Remote'.

---

### **Example 4: Update Based on Calculation**

```sql
UPDATE products
SET price = price * 1.10
WHERE category = 'Electronics';
```

Increases all electronics prices by 10%.

---

### **Example 5: Update with JOIN (Advanced)**

```sql
UPDATE orders o
JOIN customers c ON o.customer_id = c.customer_id
SET o.shipping_address = c.city
WHERE o.shipping_address IS NULL;
```

---

## ❌ DELETE - Removing Data

### **Basic Syntax:**
```sql
DELETE FROM table_name
WHERE condition;
```

⚠️ **CRITICAL:** Always use WHERE! Without it, you'll delete ALL rows!

---

### **Example 1: Delete a Single Row**

**Before:**
| customer_id | name | email |
|-------------|------|-------|
| 1 | Alice | alice@email.com |
| 2 | Bob | bob@email.com |
| 3 | Carol | carol@email.com |

**Delete Bob:**
```sql
DELETE FROM customers
WHERE customer_id = 2;
```

**After:**
| customer_id | name | email |
|-------------|------|-------|
| 1 | Alice | alice@email.com |
| 3 | Carol | carol@email.com |

---

### **Example 2: Delete Multiple Rows**

```sql
DELETE FROM customers
WHERE created_at < '2020-01-01';
```

Deletes all customers created before 2020.

---

### **Example 3: Delete Based on Condition**

```sql
DELETE FROM orders
WHERE order_status = 'Cancelled'
  AND order_date < '2021-01-01';
```

---

### **Example 4: Delete All Rows (Dangerous!)**

```sql
DELETE FROM temp_table;
```

⚠️ This deletes EVERYTHING! Use with extreme caution!

**Better alternative for clearing a table:**
```sql
TRUNCATE TABLE temp_table;
```
Faster and resets auto-increment counters.

---

## 🔧 ALTER - Modifying Table Structure

### **ALTER TABLE** changes the table itself, not the data.

---

### **Example 1: Add a New Column**

**Before:**
```
customers: customer_id, name, email
```

**Add phone column:**
```sql
ALTER TABLE customers
ADD COLUMN phone VARCHAR(20);
```

**After:**
```
customers: customer_id, name, email, phone
```

---

### **Example 2: Add Column with Default Value**

```sql
ALTER TABLE customers
ADD COLUMN status VARCHAR(20) DEFAULT 'Active';
```

All existing rows get 'Active' as status.

---

### **Example 3: Drop (Remove) a Column**

```sql
ALTER TABLE customers
DROP COLUMN phone;
```

⚠️ This permanently deletes the column and all its data!

---

### **Example 4: Rename a Column**

**MySQL:**
```sql
ALTER TABLE customers
CHANGE COLUMN email email_address VARCHAR(255);
```

**PostgreSQL:**
```sql
ALTER TABLE customers
RENAME COLUMN email TO email_address;
```

---

### **Example 5: Modify Column Data Type**

```sql
ALTER TABLE products
MODIFY COLUMN price DECIMAL(10,2);
```

Changes price column to allow 2 decimal places.

---

### **Example 6: Add a Constraint**

**Add NOT NULL:**
```sql
ALTER TABLE customers
MODIFY COLUMN email VARCHAR(255) NOT NULL;
```

**Add UNIQUE:**
```sql
ALTER TABLE customers
ADD CONSTRAINT unique_email UNIQUE (email);
```

**Add FOREIGN KEY:**
```sql
ALTER TABLE orders
ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_id) REFERENCES customers(customer_id);
```

---

### **Example 7: Rename a Table**

```sql
ALTER TABLE customers
RENAME TO clients;
```

---

## 💡 Common Patterns

### **Pattern 1: Safe Update (Check First)**

```sql
-- 1. Check what will be updated
SELECT * FROM customers WHERE city = 'LA';

-- 2. If correct, update
UPDATE customers SET city = 'Los Angeles' WHERE city = 'LA';

-- 3. Verify
SELECT * FROM customers WHERE city = 'Los Angeles';
```

---

### **Pattern 2: Safe Delete (Check First)**

```sql
-- 1. Check what will be deleted
SELECT * FROM orders WHERE order_status = 'Cancelled';

-- 2. If correct, delete
DELETE FROM orders WHERE order_status = 'Cancelled';

-- 3. Verify
SELECT COUNT(*) FROM orders WHERE order_status = 'Cancelled';
-- Should return 0
```

---

### **Pattern 3: Backup Before Deleting**

```sql
-- 1. Create backup
CREATE TABLE orders_backup AS
SELECT * FROM orders WHERE order_status = 'Cancelled';

-- 2. Delete
DELETE FROM orders WHERE order_status = 'Cancelled';

-- 3. If needed, restore
INSERT INTO orders SELECT * FROM orders_backup;
```

---

## 🎯 Real-World Examples

### **Example 1: User Registration**

```sql
INSERT INTO users (username, email, password_hash, created_at)
VALUES ('john_doe', 'john@example.com', 'hashed_password', NOW());
```

---

### **Example 2: Update User Profile**

```sql
UPDATE users
SET 
    city = 'New York',
    last_updated = NOW()
WHERE user_id = 123;
```

---

### **Example 3: Deactivate Account**

```sql
UPDATE users
SET 
    status = 'Inactive',
    deactivated_at = NOW()
WHERE user_id = 456;
```

---

### **Example 4: Delete Old Logs**

```sql
DELETE FROM activity_logs
WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
```

Deletes logs older than 90 days.

---

### **Example 5: Add Timestamp Columns**

```sql
ALTER TABLE products
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
```

---

## ⚠️ Important Safety Rules

### **1. Always Use WHERE with UPDATE/DELETE**
```sql
-- ❌ DANGEROUS - Updates ALL rows
UPDATE customers SET city = 'NYC';

-- ✅ SAFE - Updates specific rows
UPDATE customers SET city = 'NYC' WHERE customer_id = 1;
```

---

### **2. Test with SELECT First**
```sql
-- 1. Test what will be affected
SELECT * FROM customers WHERE created_at < '2020-01-01';

-- 2. If correct, then delete
DELETE FROM customers WHERE created_at < '2020-01-01';
```

---

### **3. Use Transactions for Critical Changes**
```sql
START TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;

-- Check if everything looks good
SELECT * FROM accounts WHERE account_id IN (1, 2);

-- If good, commit. If not, rollback.
COMMIT;
-- or
ROLLBACK;
```

---

### **4. Backup Before Major Changes**
```sql
-- Create backup
CREATE TABLE customers_backup AS SELECT * FROM customers;

-- Make changes
ALTER TABLE customers DROP COLUMN old_column;

-- If something goes wrong, restore
DROP TABLE customers;
ALTER TABLE customers_backup RENAME TO customers;
```

---

## 📊 Quick Reference Table

| Command | Purpose | Example |
|---------|---------|---------|
| **INSERT** | Add new rows | `INSERT INTO table VALUES (...)` |
| **UPDATE** | Modify existing rows | `UPDATE table SET col = val WHERE ...` |
| **DELETE** | Remove rows | `DELETE FROM table WHERE ...` |
| **ALTER ADD** | Add column | `ALTER TABLE table ADD COLUMN col TYPE` |
| **ALTER DROP** | Remove column | `ALTER TABLE table DROP COLUMN col` |
| **ALTER MODIFY** | Change column type | `ALTER TABLE table MODIFY COLUMN col TYPE` |
| **ALTER RENAME** | Rename column/table | `ALTER TABLE table RENAME TO new_name` |

---

## ✅ Practice Exercises

### **Exercise 1: INSERT**
Add a new product to the products table:
- product_id: 101
- name: 'Laptop'
- price: 999.99
- category: 'Electronics'

<details>
<summary>Solution</summary>

```sql
INSERT INTO products (product_id, name, price, category)
VALUES (101, 'Laptop', 999.99, 'Electronics');
```
</details>

---

### **Exercise 2: UPDATE**
Increase all product prices in 'Electronics' category by 5%.

<details>
<summary>Solution</summary>

```sql
UPDATE products
SET price = price * 1.05
WHERE category = 'Electronics';
```
</details>

---

### **Exercise 3: DELETE**
Delete all orders with status 'Cancelled' from before 2021.

<details>
<summary>Solution</summary>

```sql
DELETE FROM orders
WHERE order_status = 'Cancelled'
  AND order_date < '2021-01-01';
```
</details>

---

### **Exercise 4: ALTER**
Add a 'phone' column to the customers table (VARCHAR(20)).

<details>
<summary>Solution</summary>

```sql
ALTER TABLE customers
ADD COLUMN phone VARCHAR(20);
```
</details>

---

## 🚀 Summary

- **INSERT** - Add new data
- **UPDATE** - Change existing data (always use WHERE!)
- **DELETE** - Remove data (always use WHERE!)
- **ALTER** - Modify table structure

**Remember:** 
- Test with SELECT first
- Use WHERE clauses
- Backup before major changes
- Use transactions for critical operations

Happy querying! 🎓
