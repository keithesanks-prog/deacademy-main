# B-Tree Fundamentals for SQL

## What is a B-Tree?

**B-Tree = Balanced Tree**

A self-balancing search tree optimized for systems that read and write large blocks of data - like databases and file systems.

**Invented 1970** by Rudolf Bayer & Ed McCreight at Boeing

---

## Key Properties

| Property | Description |
|----------|-------------|
| **Multiple keys per node** | Unlike binary trees (max 2 children), B-Tree nodes can store many keys |
| **All leaves at same depth** | Guarantees balanced performance - no operation degrades to O(n) |
| **Automatically sorted** | Data stays sorted as you insert/delete |
| **Disk I/O optimized** | Node size matches disk pages (4-16KB), minimizing expensive disk seeks |

---

## The Library Analogy

Imagine finding a book in a library with **1 million books**:

### Without Index (Full Scan)
Walk down every aisle, checking every book until you find it.
- **Time**: Hours
- **This is what databases do WITHOUT indexes**

### With B-Tree Index
Use the card catalog:
1. Open drawer labeled "M-P" (first decision)
2. Find section "Ma-Me" (second decision)  
3. Find exact card "Matrix, The" (third decision)
4. Card tells you: "Aisle 42, Shelf 7"

**3 lookups instead of 1 million!**

---

## B-Tree Structure

### Simplified Example

```
Root: [50]
       ├─ Internal: [20|35]
       │    ├─ Leaf: [10|15]
       │    ├─ Leaf: [25|30]
       │    └─ Leaf: [40|45]
       └─ Internal: [70|85]
            ├─ Leaf: [60|65]
            ├─ Leaf: [75|80]
            └─ Leaf: [90|95]
```

- **Root → Internal Nodes → Leaf Nodes** (where actual data lives)
- Values < 50 go left, values ≥ 50 go right
- All values remain sorted throughout the tree

---

## Anatomy of a B-Tree Node

Each node contains alternating **keys** and **pointers**:

```
[ptr | K1 | ptr | K2 | ptr | K3 | ptr]
```

### Keys (Sorted Values)
- Values from your indexed column
- Used to navigate the tree
- Example: Compare search value against K1, K2, K3 to determine path

### Pointers (References)
- In **internal nodes**: Point to child nodes
- In **leaf nodes**: Point to actual table data (row IDs)
- Always **one more pointer than keys** (n keys = n+1 pointers)

---

## Order of a B-Tree

The **"order m"** defines tree capacity:

| Rule | Meaning |
|------|---------|
| Each node has at most **m children** | Maximum branching factor |
| Each node has at most **m-1 keys** | Maximum keys per node |
| Non-root nodes have at least **⌈m/2⌉ children** | Minimum occupancy (keeps balanced) |

**Example**: B-Tree of order 5:
- Max 5 children per node
- Max 4 keys per node
- Min 3 children for non-root nodes

---

## Performance Characteristics

### Time Complexity: O(log n)

| Rows | Steps Needed |
|------|--------------|
| 1,000 | ~3 |
| 1,000,000 | ~4 |
| 1,000,000,000 | ~5 |

**As data doubles, you only add ONE more step!**

### Disk I/O Efficiency

**3-4 disk reads** for millions of rows:
- Each disk read = ~10ms
- **Total time: ~30-40ms**

Compare to full table scan:
- 1,000,000 comparisons
- **~10 seconds**

---

## Why B-Trees vs Other Structures?

### Why not a sorted list?
Still requires ~500,000 comparisons on average for 1M records.

### Why not a binary tree?
- Too tall (20+ levels for 1M records)
- Each level = 1 disk read
- 20 disk reads = 200ms (SLOW!)

### B-Trees are the Goldilocks solution
- **Fat and short** instead of tall and skinny
- Each node holds many keys (100+)
- Only 3-4 levels deep for millions of records
- **3-4 disk reads instead of 20!**

---

## Self-Balancing Magic

B-Trees automatically maintain balance:

✅ Insert 1M rows in random order → **stays balanced**  
✅ Delete half your data → **rebalances automatically**  
✅ Insert in ascending order (worst case for some trees) → **no problem**

**You never have to:**
- Manually rebuild indexes
- Worry about "hot spots"
- Deal with degraded performance over time

---

## Real-World Usage

B-Trees power:
- **Databases**: PostgreSQL, MySQL, SQLite, SQL Server, Oracle
- **File Systems**: NTFS, ext4, HFS+
- **Key-Value Stores**: MongoDB, CouchDB

**50+ years of optimization. Battle-tested at massive scale.**

---

## Next Steps

- [How B-Trees Power SQL Indexes](btree_sql_indexes.md)
- [B-Tree Search Operations](btree_search_operations.md)
- [Why B-Trees Dominate Databases](btree_advantages.md)
