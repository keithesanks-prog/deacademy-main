# When Indexes Are Used - Practical Examples

## Overview

This guide shows **real-world examples** of when database indexes are used (and when they're not). Understanding these patterns will help you write faster queries and know when to create indexes.

---

## ✅ Index IS Used

### 1. Exact Match (Equality)

```sql
-- Query
SELECT * FROM users WHERE email = 'alice@test.com';

-- Index used: idx_email
-- Why: Direct lookup in B-Tree
-- Performance: O(log n) - ~3-4 disk reads
```

**Pattern:** `WHERE column = value`

---

### 2. Range Queries

```sql
-- Query
SELECT * FROM products WHERE price BETWEEN 10 AND 100;

-- Index used: idx_price
-- Why: Navigate to 10, scan leaves to 100
-- Performance: O(log n + k) where k = results
```

**Patterns:**
- `WHERE price BETWEEN 10 AND 100`
- `WHERE score > 80`
- `WHERE date < '2024-01-01'`
- `WHERE age >= 18 AND age <= 65`

---

### 3. ORDER BY (Sorting)

```sql
-- Query
SELECT * FROM players ORDER BY score DESC LIMIT 10;

-- Index used: idx_score
-- Why: Data already sorted in B-Tree leaves
-- Performance: Just read first 10 entries from index
```

**Pattern:** `ORDER BY indexed_column`

**Huge benefit:** No sorting needed!

---

### 4. Prefix Matching (LIKE)

```sql
-- Query
SELECT * FROM users WHERE email LIKE 'alice%';

-- Index used: idx_email
-- Why: Range scan from 'alice' to 'alicf' (next prefix)
-- Performance: O(log n + k)
```

**Pattern:** `WHERE column LIKE 'prefix%'`

**Important:** Wildcard must be at the END!

---

### 5. MIN/MAX Aggregates

```sql
-- Query
SELECT MIN(price), MAX(price) FROM products;

-- Index used: idx_price
-- Why: Min = leftmost leaf, Max = rightmost leaf
-- Performance: O(log n) - just navigate to edges
```

**Pattern:** `MIN(indexed_column)` or `MAX(indexed_column)`

---

### 6. JOIN Conditions

```sql
-- Query
SELECT o.*, u.name
FROM orders o
JOIN users u ON o.user_id = u.id;

-- Indexes used:
-- - idx_user_id on orders.user_id
-- - PRIMARY KEY on users.id (auto-indexed)
-- Why: Fast lookup for each join match
-- Performance: O(n * log m) instead of O(n * m)
```

**Pattern:** `JOIN table ON indexed_column = indexed_column`

---

### 7. GROUP BY

```sql
-- Query
SELECT team_id, COUNT(*) 
FROM players 
GROUP BY team_id;

-- Index used: idx_team_id
-- Why: Data already grouped in index
-- Performance: Scan index, count consecutive values
```

**Pattern:** `GROUP BY indexed_column`

---

### 8. IN Clause (Small List)

```sql
-- Query
SELECT * FROM users WHERE id IN (1, 5, 10, 42);

-- Index used: PRIMARY KEY (id)
-- Why: Multiple index lookups (one per value)
-- Performance: O(k * log n) where k = list size
```

**Pattern:** `WHERE column IN (val1, val2, val3)`

**Note:** Efficient for small lists (~10-100 values)

---

### 9. Compound Index (Leftmost Prefix)

```sql
-- Index: CREATE INDEX idx_name ON users(last_name, first_name, birth_date);

-- ✅ Uses index (leftmost: last_name)
SELECT * FROM users WHERE last_name = 'Smith';

-- ✅ Uses index (leftmost: last_name, first_name)
SELECT * FROM users 
WHERE last_name = 'Smith' AND first_name = 'John';

-- ✅ Uses index (all columns)
SELECT * FROM users 
WHERE last_name = 'Smith' 
  AND first_name = 'John' 
  AND birth_date = '1990-01-01';
```

**Pattern:** Query uses leftmost column(s) of compound index

---

### 10. Window Functions with ORDER BY

```sql
-- Query
SELECT 
    player_name,
    ROW_NUMBER() OVER (PARTITION BY team_id ORDER BY score DESC) as rank
FROM players;

-- Indexes used:
-- - idx_team_id for PARTITION BY
-- - idx_score for ORDER BY
-- Why: Avoids sorting millions of rows
-- Performance: Dramatically faster
```

**Pattern:** Window functions with indexed columns

---

## ❌ Index IS NOT Used

### 1. Wildcard at Beginning

```sql
-- Query
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- Index used: NONE
-- Why: Can't navigate B-Tree without knowing prefix
-- Performance: Full table scan - O(n)
```

**Problem:** `LIKE '%anything'` or `LIKE '%middle%'`

**Solution:** Use full-text search indexes instead

---

### 2. Function on Indexed Column

```sql
-- Query
SELECT * FROM users WHERE UPPER(email) = 'ALICE@TEST.COM';

-- Index used: NONE
-- Why: Index stores original values, not UPPER() results
-- Performance: Full table scan - O(n)
```

**Problem:** Any function wrapping the column

**Solution:** 
```sql
-- Store computed values or use functional indexes
CREATE INDEX idx_email_upper ON users(UPPER(email));
```

---

### 3. Math Operations on Indexed Column

```sql
-- Query
SELECT * FROM products WHERE price * 1.1 > 100;

-- Index used: NONE
-- Why: Index doesn't know computed values
-- Performance: Full table scan
```

**Problem:** `WHERE price * 1.1 > 100`

**Solution:** Rewrite to isolate column
```sql
-- This WILL use index
SELECT * FROM products WHERE price > 100 / 1.1;
```

---

### 4. OR with Non-Indexed Column

```sql
-- Query
SELECT * FROM users 
WHERE email = 'alice@test.com' OR phone = '555-1234';

-- Indexes: idx_email exists, but NO index on phone
-- Index used: NONE (or partial scan + merge)
-- Why: Must check both conditions for all rows
-- Performance: Often falls back to full scan
```

**Solution:** Create index on both columns or use UNION
```sql
-- Option 1: Index both
CREATE INDEX idx_phone ON users(phone);

-- Option 2: Use UNION
SELECT * FROM users WHERE email = 'alice@test.com'
UNION
SELECT * FROM users WHERE phone = '555-1234';
```

---

### 5. NOT EQUAL (!=, <>)

```sql
-- Query
SELECT * FROM users WHERE status != 'active';

-- Index used: NONE (usually)
-- Why: Might return most rows - full scan is faster
-- Performance: Full table scan
```

**Problem:** Negation often returns too many rows

**Solution:** Use positive conditions when possible
```sql
-- Better if 'inactive' is small set
SELECT * FROM users WHERE status = 'inactive';
```

---

### 6. IS NULL (Sometimes)

```sql
-- Query
SELECT * FROM users WHERE deleted_at IS NULL;

-- Index used: DEPENDS on database
-- Why: Some DBs don't index NULL values
-- Performance: May require full scan
```

**Problem:** NULL handling varies by database

**Solution:** Use partial/filtered indexes
```sql
-- PostgreSQL: Partial index
CREATE INDEX idx_active_users ON users(id) WHERE deleted_at IS NULL;
```

---

### 7. Type Mismatch

```sql
-- Query (user_id is INT)
SELECT * FROM users WHERE user_id = '123';  -- String!

-- Index used: NONE (or inefficient)
-- Why: Type conversion prevents index usage
-- Performance: May scan entire index
```

**Problem:** Comparing INT to STRING

**Solution:** Use correct types
```sql
SELECT * FROM users WHERE user_id = 123;  -- Correct!
```

---

### 8. Skipping Leftmost Column (Compound Index)

```sql
-- Index: CREATE INDEX idx_name ON users(last_name, first_name);

-- ❌ Cannot use index (skips last_name)
SELECT * FROM users WHERE first_name = 'John';

-- ❌ Cannot use index (skips last_name)
SELECT * FROM users WHERE birth_date = '1990-01-01';
```

**Problem:** Compound index requires leftmost column

**Solution:** Create separate index or reorder compound index

---

### 9. SELECT * with Low Selectivity

```sql
-- Query (assuming 90% of users are 'active')
SELECT * FROM users WHERE status = 'active';

-- Index used: MAYBE, but might ignore it
-- Why: Returning 90% of rows - full scan is faster
-- Performance: Database may choose full scan
```

**Problem:** Index overhead > scan benefit

**Database decision:** "Faster to just read the whole table"

---

### 10. Complex Expressions

```sql
-- Query
SELECT * FROM orders 
WHERE YEAR(order_date) = 2024 AND MONTH(order_date) = 1;

-- Index used: NONE
-- Why: Functions prevent index usage
-- Performance: Full table scan
```

**Solution:** Rewrite as range
```sql
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' 
  AND order_date < '2024-02-01';
-- Now idx_order_date CAN be used!
```

---

## How to Check Index Usage

### PostgreSQL
```sql
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'alice@test.com';
```

**Look for:**
- ✅ `Index Scan using idx_email` - Good!
- ❌ `Seq Scan on users` - Full table scan (bad!)

---

### MySQL
```sql
EXPLAIN
SELECT * FROM users WHERE email = 'alice@test.com';
```

**Look for:**
- ✅ `type: ref` or `type: range` - Using index
- ❌ `type: ALL` - Full table scan

---

### SQLite
```sql
EXPLAIN QUERY PLAN
SELECT * FROM users WHERE email = 'alice@test.com';
```

**Look for:**
- ✅ `SEARCH users USING INDEX idx_email` - Good!
- ❌ `SCAN users` - Full table scan

---

## Quick Decision Tree

```
Is your WHERE/JOIN/ORDER BY column indexed?
├─ NO → Index won't be used (create one!)
└─ YES → Continue...
    │
    ├─ Using functions on column? (UPPER, YEAR, etc.)
    │  └─ YES → Index NOT used ❌
    │
    ├─ Using LIKE '%prefix'? (wildcard at start)
    │  └─ YES → Index NOT used ❌
    │
    ├─ Using != or NOT?
    │  └─ YES → Index probably NOT used ❌
    │
    ├─ Compound index but skipping leftmost column?
    │  └─ YES → Index NOT used ❌
    │
    └─ None of the above?
       └─ Index WILL be used ✅
```

---

## Best Practices Summary

### ✅ Write Index-Friendly Queries

```sql
-- Good: Direct column comparison
WHERE price > 100

-- Good: Prefix matching
WHERE email LIKE 'alice%'

-- Good: Range with indexed column
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31'

-- Good: Isolated column
WHERE price > total_cost / quantity
```

### ❌ Avoid Index-Breaking Patterns

```sql
-- Bad: Function on column
WHERE YEAR(order_date) = 2024

-- Bad: Wildcard at start
WHERE email LIKE '%@gmail.com'

-- Bad: Math on column
WHERE price * 1.1 > 100

-- Bad: Type mismatch
WHERE user_id = '123'  -- user_id is INT
```

---

## Real-World Example

### Scenario: E-commerce Order Search

```sql
-- Table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    order_date DATE,
    status VARCHAR(20),
    total_amount DECIMAL(10,2)
);

-- Indexes
CREATE INDEX idx_user_id ON orders(user_id);
CREATE INDEX idx_order_date ON orders(order_date);
CREATE INDEX idx_status ON orders(status);
CREATE INDEX idx_user_status ON orders(user_id, status);
```

### Query Analysis

```sql
-- ✅ Uses idx_user_id
SELECT * FROM orders WHERE user_id = 123;

-- ✅ Uses idx_order_date
SELECT * FROM orders WHERE order_date >= '2024-01-01';

-- ✅ Uses idx_user_status (compound, leftmost prefix)
SELECT * FROM orders WHERE user_id = 123 AND status = 'shipped';

-- ✅ Uses idx_order_date for ORDER BY
SELECT * FROM orders ORDER BY order_date DESC LIMIT 10;

-- ❌ NO index used (function on column)
SELECT * FROM orders WHERE YEAR(order_date) = 2024;

-- ❌ NO index used (skips leftmost in compound)
SELECT * FROM orders WHERE status = 'shipped';  -- idx_user_status can't help

-- ✅ Uses idx_status (separate index exists)
SELECT * FROM orders WHERE status = 'shipped';
```

---

## Key Takeaways

🎯 **Index IS used when:**
- Direct column comparisons (`=`, `>`, `<`, `BETWEEN`)
- Prefix matching (`LIKE 'prefix%'`)
- ORDER BY indexed columns
- JOIN on indexed columns
- Leftmost columns of compound indexes

🎯 **Index IS NOT used when:**
- Functions wrap the column
- Wildcards at start (`LIKE '%suffix'`)
- Math operations on column
- Type mismatches
- Skipping leftmost column in compound index

🎯 **Always verify with EXPLAIN!**

---

## Related Topics

- [B-Tree Fundamentals](btree_fundamentals.md)
- [How B-Trees Power SQL Indexes](btree_sql_indexes.md)
- [Why B-Trees Dominate Databases](btree_advantages.md)
