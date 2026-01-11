# SQL Learning Summary

## 1. Window Functions
Window functions perform calculations across a set of table rows that are somehow related to the current row. Unlike aggregate functions, they do not cause rows to become grouped into a single output row.

### Key Functions Learned:
- **`LAG(column) OVER (ORDER BY ...)`**: Accesses data from the previous row. Useful for Year-over-Year (YoY) calculations.
- **`RANK() OVER (PARTITION BY ... ORDER BY ...)`**: Assigns a rank to each row within a partition. Useful for finding "Top N" items per group.
- **`AVG(column) OVER (PARTITION BY ...)`**: Calculates a running or group average without collapsing rows.

### Important Rule:
> ⚠️ **Window functions are calculated AFTER the `WHERE` clause.**
> You cannot filter by the result of a window function in the same query level. You must use a **CTE** or **Subquery**.

**Incorrect:**
```sql
SELECT * FROM sales WHERE RANK() OVER (...) <= 3
```

**Correct:**
```sql
WITH ranked_sales AS (
    SELECT *, RANK() OVER (...) as rnk FROM sales
)
SELECT * FROM ranked_sales WHERE rnk <= 3
```

## 2. Common Table Expressions (CTEs)
CTEs (`WITH name AS ...`) are temporary result sets that make queries more readable and modular.

### Structure:
```sql
WITH cte1 AS (
    SELECT ...
), -- Comma between CTEs
cte2 AS (
    SELECT ... FROM cte1
)
SELECT * FROM cte2;
```

## 3. Indexes
Indexes improve the speed of data retrieval operations.

- **B-Tree Index**: The default and most common. Good for equality (`=`) and range (`<`, `>`, `BETWEEN`) queries.
- **When to Index**: Columns used frequently in `WHERE`, `JOIN`, and `ORDER BY`.
- **Cardinality**: Indexes work best on columns with many unique values (High Cardinality), like IDs, Dates, or Emails. They are less effective on columns with few unique values (Low Cardinality), like Gender or Status.

### Checking Usage:
Use `EXPLAIN ANALYZE` to see if PostgreSQL is using your index ("Index Scan") or reading the whole table ("Seq Scan").

## 4. PostgreSQL Specifics
- **Date Extraction**: Use `EXTRACT(YEAR FROM date_col)` instead of `YEAR(date_col)`.
- **Dropping Tables**: Use `DROP TABLE table_name CASCADE` to automatically remove dependent objects (like views or foreign keys) to avoid errors.
