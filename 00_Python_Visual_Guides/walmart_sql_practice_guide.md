# 🎯 Walmart Database - SQL Mastery Practice

This workbook maps concepts from your **SQL Mastery Guide** to the **Walmart star schema database**.

---

## 📊 Your Database Schema

### Fact Table
- **`fact_sales`**: transaction_id, date_key, product_id, store_id, customer_id, quantity, total_amount

### Dimension Tables
- **`dim_products`**: product_id, product_name, category, price, cost
- **`dim_stores`**: store_id, store_name, city, state, region
- **`dim_customers`**: customer_id, customer_name, segment
- **`dim_date`**: date_key, date, year, month, quarter, day_name

---

## 🧹 Section 1: Data Cleaning & String Functions

### Exercise 1.1: Extract Store City
**Concept**: `SUBSTRING_INDEX` - Extracting parts of strings

```sql
-- Store names are formatted as "Store 1 - Austin"
-- Extract just the city name

SELECT 
    store_name,
    SUBSTRING_INDEX(store_name, ' - ', -1) AS city_extracted
FROM dim_stores;
```

**Challenge**: Compare your extracted city with the actual `city` column. Do they match?

---

### Exercise 1.2: Product Name Cleanup
**Concept**: `CONCAT`, `UPPER`, `TRIM`

```sql
-- Create a formatted product display name
-- Format: "CATEGORY: Product Name ($price)"

SELECT 
    product_id,
    CONCAT(
        UPPER(category), 
        ': ', 
        product_name, 
        ' ($', 
        price, 
        ')'
    ) AS display_name
FROM dim_products
LIMIT 10;
```

---

### Exercise 1.3: Handle Missing Data
**Concept**: `COALESCE` - Dealing with NULLs

```sql
-- If a customer has no segment, show 'Unknown'

SELECT 
    customer_name,
    COALESCE(segment, 'Unknown') AS customer_segment
FROM dim_customers;
```

---

## 🪟 Section 2: Window Functions

### Exercise 2.1: Month-over-Month Sales Growth
**Concept**: `LAG` - Looking at previous rows

```sql
WITH monthly_sales AS (
    SELECT 
        d.year,
        d.month,
        SUM(f.total_amount) AS total_sales
    FROM fact_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY d.year, d.month
    ORDER BY d.year, d.month
)
SELECT 
    year,
    month,
    total_sales,
    LAG(total_sales, 1) OVER (ORDER BY year, month) AS prev_month_sales,
    total_sales - LAG(total_sales, 1) OVER (ORDER BY year, month) AS growth
FROM monthly_sales;
```

**Question**: Which month had the biggest sales growth?

---

### Exercise 2.2: Top 3 Products per Category
**Concept**: `RANK` vs `DENSE_RANK` vs `ROW_NUMBER`

```sql
WITH product_sales AS (
    SELECT 
        p.category,
        p.product_name,
        SUM(f.total_amount) AS total_revenue,
        ROW_NUMBER() OVER (PARTITION BY p.category ORDER BY SUM(f.total_amount) DESC) AS row_num,
        RANK() OVER (PARTITION BY p.category ORDER BY SUM(f.total_amount) DESC) AS rank_num,
        DENSE_RANK() OVER (PARTITION BY p.category ORDER BY SUM(f.total_amount) DESC) AS dense_rank_num
    FROM fact_sales f
    JOIN dim_products p ON f.product_id = p.product_id
    GROUP BY p.category, p.product_name
)
SELECT *
FROM product_sales
WHERE row_num <= 3
ORDER BY category, total_revenue DESC;
```

**Challenge**: Change `row_num` to `rank_num` or `dense_rank_num`. How do the results differ?

---

### Exercise 2.3: Running Total by Quarter
**Concept**: `SUM() OVER` - Cumulative calculations

```sql
WITH quarterly_sales AS (
    SELECT 
        d.quarter,
        SUM(f.total_amount) AS quarter_sales
    FROM fact_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    GROUP BY d.quarter
    ORDER BY d.quarter
)
SELECT 
    quarter,
    quarter_sales,
    SUM(quarter_sales) OVER (ORDER BY quarter) AS running_total
FROM quarterly_sales;
```

---

## 🚀 Section 3: Advanced CTEs & Logic

### Exercise 3.1: High-Value Customers
**Concept**: CTEs with `HAVING` clause

```sql
WITH customer_spending AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.segment,
        COUNT(f.transaction_id) AS num_purchases,
        SUM(f.total_amount) AS total_spent
    FROM fact_sales f
    JOIN dim_customers c ON f.customer_id = c.customer_id
    GROUP BY c.customer_id, c.customer_name, c.segment
    HAVING COUNT(f.transaction_id) >= 5  -- Only frequent shoppers
)
SELECT 
    customer_name,
    segment,
    num_purchases,
    total_spent,
    CASE 
        WHEN total_spent > 500 THEN 'VIP'
        WHEN total_spent > 200 THEN 'Gold'
        ELSE 'Silver'
    END AS customer_tier
FROM customer_spending
ORDER BY total_spent DESC;
```

**Question**: How many VIP customers do you have?

---

### Exercise 3.2: Product Profitability Analysis
**Concept**: Calculated fields, `CASE WHEN`

```sql
SELECT 
    p.product_name,
    p.category,
    p.price,
    p.cost,
    (p.price - p.cost) AS profit_per_unit,
    SUM(f.quantity) AS units_sold,
    SUM(f.quantity * (p.price - p.cost)) AS total_profit,
    CASE 
        WHEN (p.price - p.cost) / p.price > 0.5 THEN 'High Margin'
        WHEN (p.price - p.cost) / p.price > 0.3 THEN 'Medium Margin'
        ELSE 'Low Margin'
    END AS margin_category
FROM dim_products p
JOIN fact_sales f ON p.product_id = f.product_id
GROUP BY p.product_id, p.product_name, p.category, p.price, p.cost
ORDER BY total_profit DESC
LIMIT 10;
```

---

### Exercise 3.3: Regional Performance Comparison
**Concept**: Conditional aggregation (Pivot technique)

```sql
SELECT 
    d.quarter,
    SUM(CASE WHEN s.region = 'East' THEN f.total_amount ELSE 0 END) AS east_sales,
    SUM(CASE WHEN s.region = 'West' THEN f.total_amount ELSE 0 END) AS west_sales,
    SUM(CASE WHEN s.region = 'South' THEN f.total_amount ELSE 0 END) AS south_sales,
    SUM(CASE WHEN s.region = 'Midwest' THEN f.total_amount ELSE 0 END) AS midwest_sales
FROM fact_sales f
JOIN dim_stores s ON f.store_id = s.store_id
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.quarter
ORDER BY d.quarter;
```

**This is a PIVOT!** - Turning region rows into columns.

---

## 🧩 Section 4: Data Shaping

### Exercise 4.1: Day-of-Week Sales Pattern
**Concept**: Pivot - Rows to columns

```sql
SELECT 
    SUM(CASE WHEN d.day_name = 'Monday' THEN f.total_amount ELSE 0 END) AS monday_sales,
    SUM(CASE WHEN d.day_name = 'Tuesday' THEN f.total_amount ELSE 0 END) AS tuesday_sales,
    SUM(CASE WHEN d.day_name = 'Wednesday' THEN f.total_amount ELSE 0 END) AS wednesday_sales,
    SUM(CASE WHEN d.day_name = 'Thursday' THEN f.total_amount ELSE 0 END) AS thursday_sales,
    SUM(CASE WHEN d.day_name = 'Friday' THEN f.total_amount ELSE 0 END) AS friday_sales,
    SUM(CASE WHEN d.day_name = 'Saturday' THEN f.total_amount ELSE 0 END) AS saturday_sales,
    SUM(CASE WHEN d.day_name = 'Sunday' THEN f.total_amount ELSE 0 END) AS sunday_sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key;
```

**Question**: Which day of the week has the highest sales?

---

## ⚔️ Section 5: Real-World Challenges

### Challenge 5.1: Customer Retention Analysis
**Goal**: Find customers who made purchases in BOTH Q1 and Q4

```sql
WITH q1_customers AS (
    SELECT DISTINCT c.customer_id
    FROM fact_sales f
    JOIN dim_customers c ON f.customer_id = c.customer_id
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE d.quarter = 'Q1'
),
q4_customers AS (
    SELECT DISTINCT c.customer_id
    FROM fact_sales f
    JOIN dim_customers c ON f.customer_id = c.customer_id
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE d.quarter = 'Q4'
)
SELECT 
    c.customer_name,
    c.segment
FROM dim_customers c
WHERE c.customer_id IN (SELECT customer_id FROM q1_customers)
  AND c.customer_id IN (SELECT customer_id FROM q4_customers);
```

---

### Challenge 5.2: Store Performance Ranking
**Goal**: Rank stores by total revenue, show top 3 per region

```sql
WITH store_revenue AS (
    SELECT 
        s.store_id,
        s.store_name,
        s.region,
        SUM(f.total_amount) AS total_revenue
    FROM fact_sales f
    JOIN dim_stores s ON f.store_id = s.store_id
    GROUP BY s.store_id, s.store_name, s.region
)
SELECT 
    region,
    store_name,
    total_revenue,
    RANK() OVER (PARTITION BY region ORDER BY total_revenue DESC) AS rank_in_region
FROM store_revenue
WHERE rank_in_region <= 3
ORDER BY region, rank_in_region;
```

---

### Challenge 5.3: Product Basket Analysis
**Goal**: Find products frequently bought together

```sql
WITH product_pairs AS (
    SELECT 
        f1.product_id AS product_a,
        f2.product_id AS product_b,
        COUNT(*) AS times_bought_together
    FROM fact_sales f1
    JOIN fact_sales f2 
        ON f1.customer_id = f2.customer_id 
        AND f1.date_key = f2.date_key
        AND f1.product_id < f2.product_id  -- Avoid duplicates
    GROUP BY f1.product_id, f2.product_id
    HAVING COUNT(*) >= 3  -- Bought together at least 3 times
)
SELECT 
    p1.product_name AS product_1,
    p2.product_name AS product_2,
    pp.times_bought_together
FROM product_pairs pp
JOIN dim_products p1 ON pp.product_a = p1.product_id
JOIN dim_products p2 ON pp.product_b = p2.product_id
ORDER BY times_bought_together DESC
LIMIT 10;
```

---

## 🎓 Learning Path

1. **Start with Section 1** (Data Cleaning) - Get comfortable with string functions
2. **Move to Section 2** (Window Functions) - Master LAG, LEAD, RANK
3. **Progress to Section 3** (CTEs) - Build complex multi-step queries
4. **Practice Section 4** (Pivoting) - Reshape data for reports
5. **Challenge yourself with Section 5** - Real business problems

---

## 💡 Tips

- **Run queries in small pieces** - Test each CTE separately
- **Use LIMIT 10** while developing - Don't overwhelm yourself with data
- **Comment your code** - Explain what each part does
- **Experiment** - Change the filters, try different columns
- **Compare results** - Run similar queries with different window functions

---

## 🚀 Next Steps

Once you've mastered these, try:
- Creating your own queries
- Combining multiple concepts (e.g., LAG + CASE WHEN)
- Building a full sales dashboard query
- Writing queries to answer business questions

**Good luck!** 🎉
