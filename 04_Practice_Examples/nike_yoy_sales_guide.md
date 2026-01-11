# Nike Year-over-Year Sales Analysis

## 📋 The Problem

**Calculate the year-over-year (YoY) percent change in total Nike product sales.**

**Requirements:**
- Return each year with the percentage change in sales compared to the previous year
- Round to 2 decimal places
- If a previous year does not exist for comparison, return NULL

**Output:** `order_year`, `percent_change`

---

## 🎯 Understanding Year-over-Year (YoY) Change

### What is YoY?

**Year-over-Year** compares this year's performance to last year's.

**Formula:**
```
YoY % Change = ((This Year - Last Year) / Last Year) × 100
```

**Example:**
- 2022 Sales: $10,000
- 2023 Sales: $12,000
- YoY Change: ((12,000 - 10,000) / 10,000) × 100 = **20%**

---

## 🔨 Step-by-Step Solution

### Step 1: Calculate Total Sales Per Year

First, let's see how much we sold each year:

```sql
SELECT 
    EXTRACT(YEAR FROM order_date) as order_year,
    SUM(total_sales) as total_sales
FROM sales
GROUP BY EXTRACT(YEAR FROM order_date)
ORDER BY order_year;
```

**Run this first!** You should see something like:

```
order_year | total_sales
-----------|------------
2022       | 35,000.00
2023       | 48,500.00
2024       | 11,360.00
```

---

### Step 2: Get Previous Year's Sales Using LAG()

Now we need to compare each year to the previous year. We use the **window function `LAG()`**:

```sql
SELECT 
    EXTRACT(YEAR FROM order_date) as order_year,
    SUM(total_sales) as total_sales,
    LAG(SUM(total_sales)) OVER (ORDER BY EXTRACT(YEAR FROM order_date)) as previous_year_sales
FROM sales
GROUP BY EXTRACT(YEAR FROM order_date)
ORDER BY order_year;
```

**What LAG() does:** Gets the value from the previous row.

**Result:**
```
order_year | total_sales | previous_year_sales
-----------|-------------|--------------------
2022       | 35,000.00   | NULL (no previous year)
2023       | 48,500.00   | 35,000.00
2024       | 11,360.00   | 48,500.00
```

---

### Step 3: Calculate the Percent Change

Now apply the YoY formula:

```sql
SELECT 
    EXTRACT(YEAR FROM order_date) as order_year,
    SUM(total_sales) as total_sales,
    LAG(SUM(total_sales)) OVER (ORDER BY EXTRACT(YEAR FROM order_date)) as previous_year_sales,
    ROUND(
        (SUM(total_sales) - LAG(SUM(total_sales)) OVER (ORDER BY EXTRACT(YEAR FROM order_date))) 
        / LAG(SUM(total_sales)) OVER (ORDER BY EXTRACT(YEAR FROM order_date)) 
        * 100,
        2
    ) as percent_change
FROM sales
GROUP BY EXTRACT(YEAR FROM order_date)
ORDER BY order_year;
```

**Result:**
```
order_year | total_sales | previous_year_sales | percent_change
-----------|-------------|---------------------|---------------
2022       | 35,000.00   | NULL                | NULL
2023       | 48,500.00   | 35,000.00           | 38.57
2024       | 11,360.00   | 48,500.00           | -76.58
```

---

### Step 4: Clean Up (Final Query)

Remove the intermediate columns for the final output:

```sql
SELECT 
    EXTRACT(YEAR FROM order_date) as order_year,
    ROUND(
        (SUM(total_sales) - LAG(SUM(total_sales)) OVER (ORDER BY EXTRACT(YEAR FROM order_date))) 
        / LAG(SUM(total_sales)) OVER (ORDER BY EXTRACT(YEAR FROM order_date)) 
        * 100,
        2
    ) as percent_change
FROM sales
GROUP BY EXTRACT(YEAR FROM order_date)
ORDER BY order_year;
```

**Final Result:**
```
order_year | percent_change
-----------|---------------
2022       | NULL
2023       | 38.57
2024       | -76.58
```

---

## 🧠 Understanding the Query

### Why Use LAG()?

**`LAG()`** is a window function that looks at the **previous row**.

```sql
LAG(SUM(total_sales)) OVER (ORDER BY EXTRACT(YEAR FROM order_date))
```

**Breakdown:**
- `LAG(...)` - Get the previous row's value
- `SUM(total_sales)` - The value we want from the previous row
- `OVER (ORDER BY year)` - Order by year so "previous" means "last year"

---

### Why the Complex Formula?

```sql
(SUM(total_sales) - LAG(SUM(total_sales)) OVER (...)) 
/ LAG(SUM(total_sales)) OVER (...) 
* 100
```

**This is just:**
```
(This Year - Last Year) / Last Year × 100
```

**We have to repeat `LAG(...)` because:**
- First use: Get the difference (numerator)
- Second use: Divide by last year (denominator)

---

### Alternative: Using a CTE (Cleaner!)

```sql
WITH yearly_sales AS (
    SELECT 
        EXTRACT(YEAR FROM order_date) as order_year,
        SUM(total_sales) as total_sales,
        LAG(SUM(total_sales)) OVER (ORDER BY EXTRACT(YEAR FROM order_date)) as previous_year_sales
    FROM sales
    GROUP BY EXTRACT(YEAR FROM order_date)
)
SELECT 
    order_year,
    ROUND(
        (total_sales - previous_year_sales) / previous_year_sales * 100,
        2
    ) as percent_change
FROM yearly_sales
ORDER BY order_year;
```

**This is easier to read!** We:
1. Calculate yearly sales and previous year in the CTE
2. Apply the formula in the main query

---

## 💡 Key Concepts

### 1. Window Functions Don't Collapse Rows

Unlike `GROUP BY`, window functions let you:
- Keep all rows
- Add calculated columns based on other rows

```sql
-- GROUP BY: Collapses to one row per year
SELECT year, SUM(sales) FROM sales GROUP BY year;

-- Window Function: Keeps all rows, adds comparison
SELECT year, sales, LAG(sales) OVER (ORDER BY year) FROM sales;
```

---

### 2. LAG() vs LEAD()

```sql
-- LAG: Look at PREVIOUS row
LAG(sales) OVER (ORDER BY year)  -- Last year's sales

-- LEAD: Look at NEXT row
LEAD(sales) OVER (ORDER BY year) -- Next year's sales
```

---

### 3. Handling NULL

When there's no previous year (like 2022), `LAG()` returns `NULL`.

**The formula handles this automatically:**
```sql
(35000 - NULL) / NULL * 100 = NULL
```

**This is correct!** You can't calculate YoY change for the first year.

---

## 🎯 Practice Variations

### Variation 1: YoY Change by Product

Calculate YoY change for each product separately:

```sql
WITH product_yearly_sales AS (
    SELECT 
        EXTRACT(YEAR FROM order_date) as order_year,
        entry_id,
        SUM(total_sales) as total_sales,
        LAG(SUM(total_sales)) OVER (PARTITION BY entry_id ORDER BY EXTRACT(YEAR FROM order_date)) as previous_year_sales
    FROM sales
    GROUP BY EXTRACT(YEAR FROM order_date), entry_id
)
SELECT 
    order_year,
    entry_id,
    ROUND(
        (total_sales - previous_year_sales) / previous_year_sales * 100,
        2
    ) as percent_change
FROM product_yearly_sales
ORDER BY entry_id, order_year;
```

**Key difference:** `PARTITION BY entry_id` - calculates YoY separately for each product!

---

### Variation 2: Month-over-Month Change

Same concept, but compare months instead of years:

```sql
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as order_month,
        SUM(total_sales) as total_sales,
        LAG(SUM(total_sales)) OVER (ORDER BY DATE_TRUNC('month', order_date)) as previous_month_sales
    FROM sales
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    order_month,
    ROUND(
        (total_sales - previous_month_sales) / previous_month_sales * 100,
        2
    ) as percent_change
FROM monthly_sales
ORDER BY order_month;
```

---

## 🔑 Key Takeaways

1. **YoY Formula:** `(This Year - Last Year) / Last Year × 100`
2. **LAG() Window Function:** Gets the previous row's value
3. **ORDER BY in OVER:** Determines what "previous" means
4. **PARTITION BY:** Calculates separately for each group
5. **NULL Handling:** First year has no previous year → NULL
6. **CTEs Make It Cleaner:** Calculate intermediate values first

---

## ✅ Complete Solution

```sql
-- Option 1: Direct calculation
SELECT 
    EXTRACT(YEAR FROM order_date) as order_year,
    ROUND(
        (SUM(total_sales) - LAG(SUM(total_sales)) OVER (ORDER BY EXTRACT(YEAR FROM order_date))) 
        / LAG(SUM(total_sales)) OVER (ORDER BY EXTRACT(YEAR FROM order_date)) 
        * 100,
        2
    ) as percent_change
FROM sales
GROUP BY EXTRACT(YEAR FROM order_date)
ORDER BY order_year;

-- Option 2: Using CTE (recommended - easier to read!)
WITH yearly_sales AS (
    SELECT 
        EXTRACT(YEAR FROM order_date) as order_year,
        SUM(total_sales) as total_sales,
        LAG(SUM(total_sales)) OVER (ORDER BY EXTRACT(YEAR FROM order_date)) as previous_year_sales
    FROM sales
    GROUP BY EXTRACT(YEAR FROM order_date)
)
SELECT 
    order_year,
    ROUND(
        (total_sales - previous_year_sales) / NULLIF(previous_year_sales, 0) * 100,
        2
    ) as percent_change
FROM yearly_sales
ORDER BY order_year;
```

---

**Great practice for combining window functions with aggregates!** 🚀
