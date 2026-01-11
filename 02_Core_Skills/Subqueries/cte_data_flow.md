# Understanding CTEs: The "Assembly Line" of Data

You asked: *"What is being pushed from one CTE to another, and how do I know what is available?"*

Think of a CTE as a **Temporary Table** that only exists for the duration of your query.

## 🏭 The Assembly Line Analogy

Imagine a factory line.
1.  **Station 1 (`sales`)**: Raw materials come in. We group them and sum them up. We put the result in a box.
2.  **Station 2 (`sales_change`)**: Takes the box from Station 1. It adds a label (YoY calculation). It passes the box to the next guy.
3.  **Final Station (`SELECT`)**: Takes the box from Station 2 and shows it to the customer.

## 🔍 Visualizing the Data Flow

Let's look at your Nike query step-by-step.

### STEP 1: The `sales` CTE
```sql
WITH sales AS (
    SELECT
        EXTRACT(YEAR FROM order_date) AS order_year,  -- Column 1
        SUM(price) AS total_sales                     -- Column 2
    FROM dim_product_nike
    GROUP BY 1
)
```
**👉 WHAT IS AVAILABLE NOW?**
Only the columns you selected!
*   `order_year`
*   `total_sales`
*(Note: `order_date`, `price`, `product_name` are GONE. You didn't select them, so they didn't make it into the box.)*

---

### STEP 2: The `sales_change` CTE
```sql
sales_change AS (
    SELECT
        order_year,      -- Available because it came from 'sales'
        total_sales,     -- Available because it came from 'sales'
        LAG(total_sales) OVER (...) as prev_sales  -- NEW calculated column
    FROM
        sales            -- 👈 LOOK! We are reading from the result of Step 1
)
```
**👉 WHAT IS AVAILABLE NOW?**
*   `order_year` (passed through)
*   `total_sales` (passed through)
*   `prev_sales` (newly created)

---

### STEP 3: The Final SELECT
```sql
SELECT
    order_year,
    total_sales,
    prev_sales
FROM
    sales_change         -- 👈 Reading from the result of Step 2
```

## 💡 The Golden Rule

> **"If you don't SELECT it, you can't use it later."**

If Step 1 calculates `SUM(price)` but forgets to select `order_year`, then Step 2 **cannot** see the year. It's like building a car engine but forgetting to put it in the car before sending it to the painting station. The painter can't paint the engine because it's not there!

### How to know what's available?
Look at the `SELECT` list of the **previous** CTE. That is your "menu" of available ingredients for the next step.
