# How to Read EXPLAIN ANALYZE Output

## What is EXPLAIN ANALYZE?

`EXPLAIN ANALYZE` shows you:
- **How** PostgreSQL executes your query
- **Whether** it uses indexes
- **How long** it takes (actual execution time)

---

## Example Output

When you run:
```sql
EXPLAIN ANALYZE
SELECT * FROM orders 
WHERE order_date BETWEEN '2025-11-20' AND '2025-11-30';
```

You'll see output like this:

### **Scenario 1: Index is USED** ✅
```
Index Scan using idx_orders_date on orders  (cost=0.15..8.17 rows=1 width=48) (actual time=0.012..0.015 rows=4 loops=1)
  Index Cond: ((order_date >= '2025-11-20'::date) AND (order_date <= '2025-11-30'::date))
Planning Time: 0.123 ms
Execution Time: 0.045 ms
```

**Key indicators:**
- ✅ **"Index Scan using idx_orders_date"** - Your index is being used!
- ✅ **"Index Cond"** - Shows the condition used with the index

### **Scenario 2: Index is NOT USED** ⚠️
```
Seq Scan on orders  (cost=0.00..1.10 rows=4 width=48) (actual time=0.008..0.010 rows=4 loops=1)
  Filter: ((order_date >= '2025-11-20'::date) AND (order_date <= '2025-11-30'::date))
Planning Time: 0.089 ms
Execution Time: 0.025 ms
```

**Key indicators:**
- ⚠️ **"Seq Scan"** - Sequential scan (reads entire table, no index)
- ⚠️ **"Filter"** - Applies filter AFTER reading all rows

---

## Breaking Down the Output

### **Scan Type** (First word tells you everything!)

| Scan Type | Meaning | Index Used? |
|-----------|---------|-------------|
| **Index Scan** | Uses index to find rows | ✅ Yes |
| **Index Only Scan** | Gets data entirely from index (fastest!) | ✅ Yes |
| **Bitmap Index Scan** | Uses index for multiple conditions | ✅ Yes |
| **Seq Scan** | Reads entire table row-by-row | ❌ No |

### **Cost Numbers**
```
(cost=0.15..8.17 rows=1 width=48)
```
- `cost=0.15..8.17` - Estimated cost (startup..total)
- `rows=1` - Estimated rows returned
- `width=48` - Average row size in bytes

### **Actual Performance**
```
(actual time=0.012..0.015 rows=4 loops=1)
```
- `actual time=0.012..0.015` - Real time in milliseconds
- `rows=4` - Actual rows returned
- `loops=1` - How many times this step ran

---

## Why Might PostgreSQL NOT Use Your Index?

Even with an index, PostgreSQL might choose `Seq Scan` if:

1. **Table is tiny** (< 100 rows) - Faster to just read everything
2. **Query returns most rows** - If you're getting 80%+ of rows, index is slower
3. **Statistics are outdated** - Run `ANALYZE orders;` to update
4. **Index isn't selective enough** - Too many matching rows

---

## Quick Reference: What to Look For

### ✅ **Index is being used:**
```
Index Scan using idx_orders_date
```

### ❌ **Index is NOT being used:**
```
Seq Scan on orders
```

---

## Practice Exercise

1. **Run this query:**
   ```sql
   EXPLAIN ANALYZE
   SELECT * FROM orders WHERE order_date > '2025-11-20';
   ```

2. **Look at the first line** - Does it say "Index Scan" or "Seq Scan"?

3. **Try a different query:**
   ```sql
   EXPLAIN ANALYZE
   SELECT * FROM orders WHERE customer_id = 1;
   ```
   This should use `idx_orders_customer_id`!

4. **Compare with a query that can't use an index:**
   ```sql
   EXPLAIN ANALYZE
   SELECT * FROM orders WHERE amount > 1000;
   ```
   This will be a Seq Scan (no index on `amount`)

---

## Pro Tip: EXPLAIN vs EXPLAIN ANALYZE

- **`EXPLAIN`** - Shows the plan WITHOUT running the query (fast, estimates only)
- **`EXPLAIN ANALYZE`** - Actually runs the query and shows real performance (slower, but accurate)

For learning, use `EXPLAIN ANALYZE` to see real results!
