Absolutely — here is your SQL Notebook in **pure Markdown format**, ready to paste directly into:

* Notion
* Obsidian
* VSCode
* GitHub
* Jupyter Notebook (Markdown cell)
* Any Markdown editor

I’ve formatted it cleanly with headings, code blocks, lists, and spacing so it renders beautifully.

---

# 📘 **SQL Learning Notebook — Markdown Version**

````markdown
# 🧠 SQL Notebook
_A structured reference guide based on everything we've covered so far._

---

# -------------------------------------
# SECTION 1 — SQL FOUNDATIONS
# -------------------------------------

## 🔹 1.1 SELECT Basics

```sql
SELECT column1, column2
FROM table_name;
````

`SELECT *` returns all columns.

---

## 🔹 1.2 WHERE (Filtering Rows)

```sql
SELECT *
FROM table
WHERE column = value;
```

Common operators:

* `=`, `<>`
* `>`, `<`, `>=`, `<=`

---

## 🔹 1.3 Comparison + Logical Operators

```sql
WHERE price > 100
AND city = 'NY'
```

Logical operators:

* `AND`
* `OR`
* `NOT`

---

## 🔹 1.4 IN, LIKE, BETWEEN, IS NULL

```sql
WHERE city IN ('NY', 'LA')
WHERE name LIKE '%son'
WHERE price BETWEEN 100 AND 300
WHERE email IS NULL
```

---

# -------------------------------------

# SECTION 2 — GROUPING & AGGREGATION

# -------------------------------------

Aggregation functions:

* COUNT(*)
* SUM()
* AVG()
* MIN()
* MAX()

### GROUP BY groups rows before aggregating:

```sql
SELECT city, COUNT(*) AS num_users
FROM users
GROUP BY city;
```

### HAVING filters AFTER GROUP BY:

```sql
SELECT city, COUNT(*) AS num_users
FROM users
GROUP BY city
HAVING COUNT(*) > 100;
```

---

# -------------------------------------

# SECTION 3 — JOINS

# -------------------------------------

## 🔹 3.1 INNER JOIN

```sql
SELECT *
FROM tableA a
JOIN tableB b
  ON a.id = b.id;
```

## 🔹 3.2 LEFT JOIN

```sql
SELECT *
FROM tableA a
LEFT JOIN tableB b
  ON a.id = b.id;
```

## 🔹 3.3 RIGHT JOIN / FULL JOIN

Less used, but good to know.

---

# -------------------------------------

# SECTION 4 — CTEs (Common Table Expressions)

# -------------------------------------

## 🔹 What is a CTE?

A temporary named table created using `WITH`.

## 🔹 Why use CTEs?

* Cleaner code
* Break problems into steps
* Required for multi-stage transformations

Example:

```sql
WITH counts AS (
  SELECT brand, payment_method, COUNT(*) AS cnt
  FROM fact_sales_tesla
  GROUP BY brand, payment_method
)
SELECT *
FROM counts;
```

---

# -------------------------------------

# SECTION 5 — WINDOW FUNCTIONS

# -------------------------------------

Window functions operate **without collapsing rows** (unlike GROUP BY).

---

## 🔹 5.1 ROW_NUMBER()

Assigns a ranking to each row, restarting per group.

```sql
ROW_NUMBER() OVER (
  PARTITION BY group_column
  ORDER BY sort_column DESC
) AS rn
```

### Breakdown:

* PARTITION BY → split into groups
* ORDER BY → sort within each group
* ROW_NUMBER → assign 1, 2, 3…

Used for:

* “most used” per category
* “top customer” per region
* “first purchase per user”
* etc.

---

## 🔹 5.2 PARTITION BY explained simply

> Splits the table into multiple mini-tables based on a column.

Example:

```sql
PARTITION BY brand
```

Creates:

* One group for each brand
* Row numbers restart in each group

---

# -------------------------------------

# SECTION 6 — UNIVERSAL SQL PROBLEM TEMPLATE

# -------------------------------------

### ✔ STEP 1 — Identify groups

(brand, user, city, etc.)

### ✔ STEP 2 — Identify metrics

(COUNT, SUM, AVG, etc.)

### ✔ STEP 3 — Aggregate

(GROUP BY)

### ✔ STEP 4 — Rank inside each group

(ROW_NUMBER + PARTITION BY)

### ✔ STEP 5 — Filter to final result

(WHERE rn = 1, LIMIT, etc.)

This template solves the majority of SQL interview problems.

---

# -------------------------------------

# SECTION 7 — PRACTICE EXAMPLES WE COVERED

# -------------------------------------

## ⭐ 7.1 Most-used payment method per brand

```sql
WITH method_counts AS (
  SELECT brand, payment_method, COUNT(*) AS cnt
  FROM fact_sales_tesla
  GROUP BY brand, payment_method
),

ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY brand
      ORDER BY cnt DESC
    ) AS rn
  FROM method_counts
)

SELECT brand, payment_method
FROM ranked
WHERE rn = 1;
```

---

## ⭐ 7.2 Cities: “Too Expensive” or “Not Expensive”

```sql
SELECT city,
       CASE WHEN AVG(price/sqft) > 1.25 * (SELECT AVG(price/sqft)
                                           FROM fact_agreements_zillow)
            THEN 'Too Expensive'
            ELSE 'Not Expensive'
       END AS status
FROM fact_agreements_zillow
GROUP BY city;
```

---

## ⭐ 7.3 Most-bought + Best-sold coin

```sql
WITH bought AS (
  SELECT cryptocurrency
  FROM fact_transactions_coinbase
  WHERE transaction_type = 'buy'
  GROUP BY cryptocurrency
  ORDER BY SUM(number_of_coins) DESC
  LIMIT 1
),
sold AS (
  SELECT cryptocurrency
  FROM fact_transactions_coinbase
  WHERE transaction_type = 'sale'
  GROUP BY cryptocurrency
  ORDER BY SUM(number_of_coins) DESC
  LIMIT 1
)

SELECT cryptocurrency, 'Most-bought coin' AS status FROM bought
UNION ALL
SELECT cryptocurrency, 'Best-sold coin'   AS status FROM sold;
```

---

# -------------------------------------

# SECTION 8 — COMMON SQL PATTERNS

# -------------------------------------

## ⭐ 8.1 Top N per group

```sql
ROW_NUMBER() OVER (
  PARTITION BY group_column
  ORDER BY metric DESC
)
```

Filter:

```sql
WHERE rn = 1;
```

---

## ⭐ 8.2 Aggregation Checklist

When aggregating:

* SELECT aggregated values
* GROUP BY non-aggregated values
* HAVING for post-group filtering

---

## ⭐ 8.3 Subquery pattern

```sql
SELECT ...
FROM (
   SELECT ...
   FROM table
) AS t;
```

---

## ⭐ 8.4 CTE Chaining

```sql
WITH step1 AS (...),
     step2 AS (... FROM step1),
     step3 AS (... FROM step2)
SELECT *
FROM step3;
```

---

# -------------------------------------

# SECTION 9 — SQL EXECUTION ORDER

# -------------------------------------

SQL processes clauses in this order:

1. FROM
2. JOIN
3. WHERE
4. GROUP BY
5. HAVING
6. SELECT
7. ORDER BY
8. LIMIT

Window functions run **between GROUP BY and SELECT**.

---

# -------------------------------------

# SECTION 10 — SQL MINDSET

# -------------------------------------

SQL is **not** procedural like Python.

SQL is:

* Declarative
* Step-by-step data shaping
* About building intermediate tables
* About transforming data INTO the answer

### The SQL workflow:

> Build → Shape → Filter → Return


```