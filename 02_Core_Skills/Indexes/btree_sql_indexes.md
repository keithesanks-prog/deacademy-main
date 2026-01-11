# How B-Trees Power SQL Indexes

## Creating an Index

```sql
CREATE INDEX idx_email ON users(email);
```

This single command tells the database: *"Build me a B-Tree index on the email column"*

**Most databases use B-Trees by default for indexes:**
- PostgreSQL ✅
- MySQL ✅
- SQLite ✅
- SQL Server ✅
- Oracle ✅

---

## What Happens Behind the Scenes

When you create an index, the database:

1. **Extracts** all email values from the `users` table
2. **Sorts** them alphabetically
3. **Builds** a B-Tree structure with sorted values
4. **Stores pointers** in leaf nodes pointing to actual table rows
5. **Persists** the tree structure to disk pages

---

## Index Lookup Flow

### Query Example
```sql
SELECT * FROM users WHERE email = 'alice@test.com';
```

### Lookup Process
```
Root → Internal → Internal → Leaf → Row pointer → Fetch data
```

**Step-by-step:**
1. **Root**: "alice@test.com starts with 'a', go left"
2. **Internal**: "'alice' comes before 'bob', go left"
3. **Internal**: "'alice@test' is here, go to leaf"
4. **Leaf**: "Found it! Row is at disk page #4729"
5. **Fetch**: Jump directly to page #4729, grab the row

**Total: 3-4 disk reads, ~30-40ms**

---

## Performance Impact

### Without Index (Full Table Scan)
```sql
SELECT * FROM players WHERE player_id = 42;
```

1. Read row 1: `player_id = 1`? Nope.
2. Read row 2: `player_id = 2`? Nope.
3. Read row 3: `player_id = 3`? Nope.
4. ...
5. Read row 847,293: `player_id = 42`? YES!

**Time: ~10 seconds** 😱

### With B-Tree Index
```sql
SELECT * FROM players WHERE player_id = 42;
```

1. Check root: "42 < 50, go left"
2. Check node: "42 > 40, go right"  
3. Check leaf: "42 is here! Row 847,293"
4. Jump directly to row 847,293

**Time: ~0.003 seconds** ⚡

---

## Primary Keys Get Indexes Automatically

When you create a table:
```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    email VARCHAR(255),
    name VARCHAR(255)
);
```

The database **automatically** creates a B-Tree index on `id`.

This is why:
```sql
SELECT * FROM users WHERE id = 12345;
```
...is **blazing fast** even with millions of users.

---

## Sorted Data Benefits

B-Trees store keys in sorted order, enabling:

### Range Queries
```sql
SELECT * FROM users 
WHERE email BETWEEN 'a%' AND 'c%' 
ORDER BY email;
```

- Navigate to 'a', scan leaf nodes left-to-right until 'c'
- **Already sorted**, no extra work needed!

### ORDER BY Optimization
```sql
SELECT * FROM products ORDER BY price DESC;
```

If there's an index on `price`:
- Data is already sorted in the B-Tree
- Database just reads leaf nodes in order
- **No sorting required!**

---

## Connection to Window Functions

Window functions benefit massively from B-Tree indexes:

```sql
SELECT 
    player_name,
    score,
    ROW_NUMBER() OVER (PARTITION BY team ORDER BY score DESC) as rank
FROM players;
```

**With B-Tree index on `score`:**
- `ORDER BY score DESC` uses the index
- Database doesn't sort millions of rows
- Query runs **100x faster**

**Without index:**
- Full table scan required
- Sort everything in memory (or disk if too big)
- SLOW and memory-intensive

---

## When to Create Indexes

### ✅ Good Candidates
- Columns you frequently search: `WHERE email = ...`
- Columns you sort by: `ORDER BY score`
- Columns you join on: `JOIN ON user_id`
- Foreign keys (often auto-indexed)

### ❌ Poor Candidates
- Columns you never query
- Tables with very few rows (<1,000)
- Columns that change constantly (index maintenance overhead)
- Columns with very low cardinality (e.g., boolean fields)

---

## Compound Indexes

Index multiple columns together:

```sql
CREATE INDEX idx_name ON users(last_name, first_name, birth_date);
```

### Leftmost Prefix Rule

This single index efficiently handles:

```sql
-- ✅ Uses index (leftmost prefix)
WHERE last_name = 'Smith'

-- ✅ Uses index (leftmost prefix)
WHERE last_name = 'Smith' AND first_name = 'John'

-- ✅ Uses index (full match)
WHERE last_name = 'Smith' AND first_name = 'John' AND birth_date = '1990-01-01'

-- ❌ Cannot use index (skips leftmost column)
WHERE first_name = 'John'
```

**Benefits:**
- One index serves multiple query patterns
- Saves disk space
- Reduces maintenance overhead

---

## Index Maintenance

B-Trees automatically maintain themselves:

### On INSERT
- Find correct leaf node
- Insert new key in sorted position
- If node is full, split it and rebalance

### On DELETE
- Find and remove key
- If node becomes too empty, merge with sibling and rebalance

### On UPDATE
- If indexed column changes: DELETE old + INSERT new
- If indexed column unchanged: no index update needed

**All automatic. You never manually rebuild indexes.**

---

## Checking Index Usage

### PostgreSQL
```sql
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'alice@test.com';
```

Look for: `Index Scan using idx_email`

### MySQL
```sql
EXPLAIN
SELECT * FROM users WHERE email = 'alice@test.com';
```

Look for: `type: ref` or `type: range` (good!)  
Avoid: `type: ALL` (full table scan - bad!)

---

## Key Takeaways

✅ `CREATE INDEX` builds a B-Tree by default  
✅ Indexes turn O(n) scans into O(log n) lookups  
✅ Primary keys get indexes automatically  
✅ Sorted data enables fast range queries and ORDER BY  
✅ Compound indexes support multiple query patterns  
✅ Self-balancing means no manual maintenance  
✅ Always verify index usage with EXPLAIN  

**B-Trees are the secret sauce that make databases fast!**

---

## Related Topics

- [B-Tree Search Operations](btree_search_operations.md)
- [Why B-Trees Dominate Databases](btree_advantages.md)
- [B-Tree Fundamentals](btree_fundamentals.md)
