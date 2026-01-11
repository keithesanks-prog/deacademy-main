# SQL Indexes & B-Trees Training

## Overview

This module covers database indexes with a focus on B-Trees - the data structure that powers most database indexes and makes SQL queries fast.

---

## Learning Path

### 1. Start Here: Fundamentals
**[B-Tree Fundamentals](btree_fundamentals.md)**
- What is a B-Tree?
- Key properties and structure
- Why B-Trees vs other data structures
- The library analogy (layman's explanation)

### 2. SQL Integration
**[How B-Trees Power SQL Indexes](btree_sql_indexes.md)**
- Creating indexes with `CREATE INDEX`
- What happens behind the scenes
- Index lookup flow
- Primary keys and auto-indexing
- When to create indexes
- Compound indexes and leftmost prefix rule

### 3. Deep Dive: Operations
**[B-Tree Search Operations](btree_search_operations.md)**
- Step-by-step search walkthrough
- Performance comparisons (O(n) vs O(log n))
- Disk I/O optimization
- Caching benefits
- Search patterns (point, range, prefix)

### 4. Advanced: Why They Dominate
**[Why B-Trees Dominate Databases](btree_advantages.md)**
- Six pillars of B-Tree dominance
- Range query excellence
- Self-balancing magic
- Disk I/O optimization details
- Multi-operation support
- Battle-tested reliability
- Compound index strategies

### 5. Practical: When Indexes Are Used
**[Index Usage Examples](index_usage_examples.md)**
- Real-world query examples
- When indexes ARE used (10 patterns)
- When indexes ARE NOT used (10 anti-patterns)
- How to check index usage with EXPLAIN
- Decision tree for index-friendly queries
- Best practices and common pitfalls

---

## Quick Reference

### Key Concepts

| Concept       | Description |
|-------------|-------------|
| **B-Tree**     | Balanced tree optimized for disk I/O |
| **Order m**    | Max children per node |
| **O(log n)**   | Time complexity - scales beautifully |
| **Self-balancing** | Automatic maintenance on insert/delete |
| **Leaf nodes** | Store actual data pointers |
| **Internal nodes** | Store keys for navigation |

### Performance Numbers

| Rows        | Full Scan  | B-Tree  | Speedup |
|-------------|---------   |-------- |---------|
| 1,000       | ~1,000 ops | ~10 ops | 100x    |
| 1,000,000   | ~1M ops    | ~20 ops | 50,000x |
| 1 billion   | ~1B ops    | ~30 ops | 33M x   |

### Common SQL Patterns

```sql
-- Create index (builds B-Tree)
CREATE INDEX idx_email ON users(email);

-- Compound index
CREATE INDEX idx_name ON users(last_name, first_name);

-- Check index usage
EXPLAIN SELECT * FROM users WHERE email = 'test@test.com';

-- Range query (B-Tree optimized)
SELECT * FROM products WHERE price BETWEEN 10 AND 100;

-- Sorted results (B-Tree optimized)
SELECT * FROM players ORDER BY score DESC;
```

---

## Why This Matters

### For Your SQL Queries

B-Trees make these operations **fast**:
- ✅ `WHERE` clauses with indexed columns
- ✅ `ORDER BY` on indexed columns
- ✅ `JOIN` on indexed foreign keys
- ✅ `MIN/MAX` aggregates
- ✅ `BETWEEN` range queries
- ✅ Window functions with `ORDER BY`

### Real-World Impact

**Without indexes:**
```sql
SELECT * FROM users WHERE email = 'alice@test.com';
-- Time: ~10 seconds (full table scan)
```

**With B-Tree index:**
```sql
SELECT * FROM users WHERE email = 'alice@test.com';
-- Time: ~0.003 seconds (index lookup)
```

**3,000x faster!**

---

## Connection to Window Functions

Your window function training benefits from understanding B-Trees:

```sql
SELECT 
    player_name,
    score,
    ROW_NUMBER() OVER (PARTITION BY team ORDER BY score DESC) as rank
FROM players;
```

**With indexes on `team` and `score`:**
- `PARTITION BY team` → Uses index for grouping
- `ORDER BY score` → Uses index for sorting
- **Query runs in milliseconds**

**Without indexes:**
- Full table scan required
- In-memory sorting needed
- **Query runs in seconds**

---

## Best Practices

### ✅ Do Create Indexes On

- Primary keys (auto-indexed)
- Foreign keys
- Columns in `WHERE` clauses
- Columns in `JOIN` conditions
- Columns in `ORDER BY` clauses
- Columns in `GROUP BY` clauses

### ❌ Don't Create Indexes On

- Tables with < 1,000 rows
- Columns never queried
- Columns with very low cardinality (e.g., boolean)
- Columns that change constantly
- Every column "just in case"

### 🎯 Compound Index Strategy

**Order matters!** Put most selective columns first:

```sql
-- Good: user_id is highly selective
CREATE INDEX idx_logs ON logs(user_id, action, timestamp);

-- Bad: timestamp is not selective
CREATE INDEX idx_logs ON logs(timestamp, action, user_id);
```

---

## Tools & Commands

### Check Index Usage (PostgreSQL)
```sql
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'test@test.com';
```

Look for: `Index Scan using idx_email`

### Check Index Usage (MySQL)
```sql
EXPLAIN
SELECT * FROM users WHERE email = 'test@test.com';
```

Look for: `type: ref` or `type: range` (good!)  
Avoid: `type: ALL` (full scan - bad!)

### List Indexes
```sql
-- PostgreSQL
\di

-- MySQL
SHOW INDEXES FROM users;

-- SQLite
.indexes users
```

---

## Key Takeaways

🎯 **B-Trees are the default index type** in most databases  
🎯 **O(log n) complexity** makes them scale beautifully  
🎯 **Self-balancing** means no maintenance required  
🎯 **Disk-optimized** design minimizes I/O operations  
🎯 **One index** supports many operations  
🎯 **50+ years** of battle-testing  
🎯 **Proper indexing** is the #1 SQL performance optimization  

---

## Next Steps

1. Read through the fundamentals
2. Practice creating indexes on your training databases
3. Use `EXPLAIN` to verify index usage
4. Apply to your window function queries
5. Experiment with compound indexes

**Understanding B-Trees will make you a better SQL developer!** 🚀
