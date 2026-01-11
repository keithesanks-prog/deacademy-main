# 🎓 Building Complex Queries: The Tesla Pricing Problem

**Learn to build queries step-by-step, not all at once.**

---

## 📋 The Problem Statement

> "Find the price of each car at the time of sale. Display the **two highest prices** for each brand. Assume the start price is from January 2023 and all the cars were sold later that year."

---

## 🗂️ The Tables

**Table 1: fact_sales_tesla**
| VIN | brand | payment_method | sale_date |
|-----|-------|----------------|-----------|
| 292BOY | Model 3 | Cash | 2023-08-06 |
| 483XYZ | Model S | Credit | 2023-03-15 |

**Table 2: dim_brands_tesla**
| brand | start_price | monthly_inflation_rate |
|-------|-------------|------------------------|
| Model 3 | 116.95 | 0.67 |
| Model S | 142.00 | 0.67 |

**Note:** Prices are in thousands (116.95 = $116,950).

---

## 🛠️ Step-by-Step Query Building

### **Step 1: Understand the Math (Compound Interest)**

**Formula:**
```
Final Price = Start Price × (1 + rate)^months
```

**Example:**
- Start: $116,950
- Rate: 0.67% per month
- Months: 7 (January → August)
- Calculation: `116,950 × (1.0067)^7 = $122,520`

---

### **Step 2: Calculate Months Elapsed**

**Query:**
```sql
SELECT 
    VIN,
    brand,
    sale_date,
    EXTRACT(MONTH FROM sale_date) AS sale_month,
    EXTRACT(MONTH FROM sale_date) - 1 AS months_elapsed
FROM fact_sales_tesla;
```

**Result:**
| VIN | brand | sale_date | sale_month | months_elapsed |
|-----|-------|-----------|------------|----------------|
| 292BOY | Model 3 | 2023-08-06 | 8 | **7** |
| 483XYZ | Model S | 2023-03-15 | 3 | **2** |

**Why `-1`?**
- January (Month 1) → 0 months elapsed
- August (Month 8) → 7 months elapsed

---

### **Step 3: Join to Get Start Price and Inflation Rate**

**Query:**
```sql
SELECT 
    f.VIN,
    f.brand,
    f.sale_date,
    d.start_price,
    d.monthly_inflation_rate,
    EXTRACT(MONTH FROM f.sale_date) - 1 AS months_elapsed
FROM fact_sales_tesla f
JOIN dim_brands_tesla d ON f.brand = d.brand;
```

**Result:**
| VIN | brand | sale_date | start_price | monthly_inflation_rate | months_elapsed |
|-----|-------|-----------|-------------|------------------------|----------------|
| 292BOY | Model 3 | 2023-08-06 | 116.95 | 0.67 | 7 |
| 483XYZ | Model S | 2023-03-15 | 142.00 | 0.67 | 2 |

---

### **Step 4: Calculate the Inflation Multiplier**

**Query:**
```sql
SELECT 
    f.VIN,
    f.brand,
    d.start_price,
    EXTRACT(MONTH FROM f.sale_date) - 1 AS months_elapsed,
    POWER(1 + d.monthly_inflation_rate/100, EXTRACT(MONTH FROM f.sale_date) - 1) AS multiplier
FROM fact_sales_tesla f
JOIN dim_brands_tesla d ON f.brand = d.brand;
```

**Result:**
| VIN | brand | start_price | months_elapsed | multiplier |
|-----|-------|-------------|----------------|------------|
| 292BOY | Model 3 | 116.95 | 7 | 1.0476 |
| 483XYZ | Model S | 142.00 | 2 | 1.0134 |

**Breakdown:**
- `1 + 0.67/100 = 1.0067`
- `POWER(1.0067, 7) = 1.0476` (4.76% increase)

---

### **Step 5: Calculate the Final Sale Price**

**Query:**
```sql
SELECT 
    f.VIN,
    f.brand,
    d.start_price,
    TRUNCATE(
        d.start_price * POWER(1 + d.monthly_inflation_rate/100, EXTRACT(MONTH FROM f.sale_date) - 1),
        2
    ) AS sale_price
FROM fact_sales_tesla f
JOIN dim_brands_tesla d ON f.brand = d.brand;
```

**Result:**
| VIN | brand | start_price | sale_price |
|-----|-------|-------------|------------|
| 292BOY | Model 3 | 116.95 | **122.52** |
| 483XYZ | Model S | 142.00 | **143.90** |

**Calculation for Model 3:**
- `116.95 × 1.0476 = 122.52`

---

### **Step 6: Wrap in a CTE (For Readability)**

**Query:**
```sql
WITH prices AS (
    SELECT 
        f.VIN,
        f.brand,
        f.sale_date,
        TRUNCATE(
            d.start_price * POWER(1 + d.monthly_inflation_rate/100, EXTRACT(MONTH FROM f.sale_date) - 1),
            2
        ) AS sale_price
    FROM fact_sales_tesla f
    JOIN dim_brands_tesla d ON f.brand = d.brand
)
SELECT * FROM prices;
```

**Why a CTE?**
- Makes the query easier to read.
- Separates the "calculation" step from the "ranking" step.

---

### **Step 7: Add Window Function for Top 2 per Brand**

**Query:**
```sql
WITH prices AS (
    SELECT 
        f.VIN,
        f.brand,
        f.sale_date,
        TRUNCATE(
            d.start_price * POWER(1 + d.monthly_inflation_rate/100, EXTRACT(MONTH FROM f.sale_date) - 1),
            2
        ) AS sale_price
    FROM fact_sales_tesla f
    JOIN dim_brands_tesla d ON f.brand = d.brand
)
SELECT 
    brand,
    VIN,
    sale_price,
    RANK() OVER (PARTITION BY brand ORDER BY sale_price DESC) AS rnk
FROM prices;
```

**Result:**
| brand | VIN | sale_price | rnk |
|-------|-----|------------|-----|
| Model 3 | ABC123 | 125.00 | 1 |
| Model 3 | 292BOY | 122.52 | 2 |
| Model 3 | DEF456 | 120.00 | 3 |
| Model S | GHI789 | 150.00 | 1 |
| Model S | 483XYZ | 143.90 | 2 |

---

### **Step 8: Filter to Top 2**

**Final Query:**
```sql
WITH prices AS (
    SELECT 
        f.VIN,
        f.brand,
        f.sale_date,
        TRUNCATE(
            d.start_price * POWER(1 + d.monthly_inflation_rate/100, EXTRACT(MONTH FROM f.sale_date) - 1),
            2
        ) AS sale_price
    FROM fact_sales_tesla f
    JOIN dim_brands_tesla d ON f.brand = d.brand
),
ranked AS (
    SELECT 
        brand,
        VIN,
        sale_price,
        RANK() OVER (PARTITION BY brand ORDER BY sale_price DESC) AS rnk
    FROM prices
)
SELECT brand, VIN, sale_price
FROM ranked
WHERE rnk <= 2;
```

**Final Result:**
| brand | VIN | sale_price |
|-------|-----|------------|
| Model 3 | ABC123 | 125.00 |
| Model 3 | 292BOY | 122.52 |
| Model S | GHI789 | 150.00 |
| Model S | 483XYZ | 143.90 |

---

## 🎯 The Building Process (Summary)

1. **Understand the math** (compound interest formula)
2. **Calculate months elapsed** (`EXTRACT(MONTH) - 1`)
3. **Join tables** to get start price and rate
4. **Calculate multiplier** (`POWER(1 + rate/100, months)`)
5. **Calculate final price** (`start_price × multiplier`)
6. **Wrap in CTE** (for readability)
7. **Add window function** (`RANK() OVER (PARTITION BY...)`)
8. **Filter** (`WHERE rnk <= 2`)

---

## 💡 Key Takeaways

**Don't write the full query at once!**
- Build it step-by-step.
- Test each step with `SELECT *` to see the intermediate results.
- Use CTEs to break complex logic into chunks.

**The pattern:**
```
Raw Data → Calculations → Ranking → Filtering
```
