# 🎧 One Step at a Time: The Drill

**Stop. Don't write code. Just answer the 3 questions.**

---

## 🛑 The Problem

> "Calculate the **total revenue** for **Electronics** products sold in **Q4 2023**, but only for **stores** that had **more than 50 transactions**."

---

## 👣 Step 1: The Entity

**Question:** What does ONE row in the final output represent?
*(Hint: "We want revenue FOR...")*

<details>
<summary>👀 Click to Reveal Answer</summary>

**A Store.**

SQL Action:
```sql
GROUP BY store_id
```
</details>

---

## 👣 Step 2: The Filters

**Question:** Which rows are "trash" (ignore them)?
*(Hint: Look for specific categories and dates)*

<details>
<summary>👀 Click to Reveal Answer</summary>

**Non-Electronics** and **Non-Q4 Dates**.

SQL Action:
```sql
WHERE category = 'Electronics' 
  AND order_date BETWEEN '2023-10-01' AND '2023-12-31'
```
</details>

---

## 👣 Step 3: The Aggregates

**Question:** What math are we doing?
*(Hint: "Total" and "More than")*

<details>
<summary>👀 Click to Reveal Answer</summary>

**Summing Revenue** and **Counting Transactions**.

SQL Action:
```sql
SELECT SUM(revenue)
HAVING COUNT(*) > 50
```
</details>

---

## 🧩 Putting It Together

Only look at this AFTER you have answered the 3 steps above.

<details>
<summary>👀 Click to Reveal Full Query</summary>

```sql
SELECT store_id, SUM(revenue)
FROM sales
WHERE category = 'Electronics' 
  AND order_date BETWEEN '2023-10-01' AND '2023-12-31'
GROUP BY store_id
HAVING COUNT(*) > 50;
```
</details>
