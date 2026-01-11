# 🎬 Tesla Pricing: Visual Data Transformation

**Watch the data change at each step!**

---

## 📊 Starting Tables

### **fact_sales_tesla**
| VIN | brand | sale_date |
|-----|-------|-----------|
| ABC123 | Model 3 | 2023-08-06 |
| DEF456 | Model 3 | 2023-03-15 |
| GHI789 | Model S | 2023-11-20 |
| JKL012 | Model S | 2023-02-10 |

### **dim_brands_tesla**
| brand | start_price | monthly_inflation_rate |
|-------|-------------|------------------------|
| Model 3 | 116.95 | 0.67 |
| Model S | 142.00 | 0.67 |

---

## 🔨 Step 1: Extract the Month

**Query:**
```sql
SELECT 
    VIN,
    brand,
    sale_date,
    EXTRACT(MONTH FROM sale_date) AS sale_month
FROM fact_sales_tesla;
```

**Result:**
| VIN | brand | sale_date | sale_month |
|-----|-------|-----------|------------|
| ABC123 | Model 3 | 2023-08-06 | **8** |
| DEF456 | Model 3 | 2023-03-15 | **3** |
| GHI789 | Model S | 2023-11-20 | **11** |
| JKL012 | Model S | 2023-02-10 | **2** |

---

## 🔨 Step 2: Calculate Months Elapsed

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
| ABC123 | Model 3 | 2023-08-06 | 8 | **7** |
| DEF456 | Model 3 | 2023-03-15 | 3 | **2** |
| GHI789 | Model S | 2023-11-20 | 11 | **10** |
| JKL012 | Model S | 2023-02-10 | 2 | **1** |

**Why?**
- January = Month 1 → 0 months elapsed
- August = Month 8 → 7 months elapsed

---

## 🔨 Step 3: JOIN to Get Pricing Info

**Query:**
```sql
SELECT 
    f.VIN,
    f.brand,
    f.sale_date,
    EXTRACT(MONTH FROM f.sale_date) - 1 AS months_elapsed,
    d.start_price,
    d.monthly_inflation_rate
FROM fact_sales_tesla f
JOIN dim_brands_tesla d ON f.brand = d.brand;
```

**Result:**
| VIN | brand | sale_date | months_elapsed | start_price | monthly_inflation_rate |
|-----|-------|-----------|----------------|-------------|------------------------|
| ABC123 | Model 3 | 2023-08-06 | 7 | **116.95** | **0.67** |
| DEF456 | Model 3 | 2023-03-15 | 2 | **116.95** | **0.67** |
| GHI789 | Model S | 2023-11-20 | 10 | **142.00** | **0.67** |
| JKL012 | Model S | 2023-02-10 | 1 | **142.00** | **0.67** |

---

## 🔨 Step 4: Calculate Inflation Multiplier

**Formula:** `(1 + rate/100)^months`

**Query:**
```sql
SELECT 
    f.VIN,
    f.brand,
    EXTRACT(MONTH FROM f.sale_date) - 1 AS months_elapsed,
    d.start_price,
    POWER(1 + d.monthly_inflation_rate/100, EXTRACT(MONTH FROM f.sale_date) - 1) AS multiplier
FROM fact_sales_tesla f
JOIN dim_brands_tesla d ON f.brand = d.brand;
```

**Result:**
| VIN | brand | months_elapsed | start_price | multiplier |
|-----|-------|----------------|-------------|------------|
| ABC123 | Model 3 | 7 | 116.95 | **1.0476** |
| DEF456 | Model 3 | 2 | 116.95 | **1.0134** |
| GHI789 | Model S | 10 | 142.00 | **1.0692** |
| JKL012 | Model S | 1 | 142.00 | **1.0067** |

**Math Breakdown (ABC123):**
- `1 + 0.67/100 = 1.0067`
- `1.0067^7 = 1.0476` (4.76% increase)

---

## 🔨 Step 5: Calculate Final Sale Price

**Formula:** `start_price × multiplier`

**Query:**
```sql
SELECT 
    f.VIN,
    f.brand,
    d.start_price,
    POWER(1 + d.monthly_inflation_rate/100, EXTRACT(MONTH FROM f.sale_date) - 1) AS multiplier,
    TRUNCATE(d.start_price * POWER(1 + d.monthly_inflation_rate/100, EXTRACT(MONTH FROM f.sale_date) - 1), 2) AS sale_price
FROM fact_sales_tesla f
JOIN dim_brands_tesla d ON f.brand = d.brand;
```

**Result:**
| VIN | brand | start_price | multiplier | sale_price |
|-----|-------|-------------|------------|------------|
| ABC123 | Model 3 | 116.95 | 1.0476 | **122.52** |
| DEF456 | Model 3 | 116.95 | 1.0134 | **118.52** |
| GHI789 | Model S | 10 | 1.0692 | **151.83** |
| JKL012 | Model S | 1 | 1.0067 | **142.95** |

**Math Breakdown (ABC123):**
- `116.95 × 1.0476 = 122.52`

---

## 🔨 Step 6: Add Window Function (Ranking)

**Query:**
```sql
WITH prices AS (
    SELECT 
        f.VIN,
        f.brand,
        TRUNCATE(d.start_price * POWER(1 + d.monthly_inflation_rate/100, EXTRACT(MONTH FROM f.sale_date) - 1), 2) AS sale_price
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
| Model 3 | ABC123 | 122.52 | **1** |
| Model 3 | DEF456 | 118.52 | **2** |
| Model S | GHI789 | 151.83 | **1** |
| Model S | JKL012 | 142.95 | **2** |

**What PARTITION BY does:**
- Splits into 2 groups (Model 3, Model S)
- Ranks within each group separately

---

## 🔨 Step 7: Filter to Top 2

**Query:**
```sql
WITH prices AS (
    SELECT 
        f.VIN,
        f.brand,
        TRUNCATE(d.start_price * POWER(1 + d.monthly_inflation_rate/100, EXTRACT(MONTH FROM f.sale_date) - 1), 2) AS sale_price
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

**Filter Applied:**
| brand | VIN | sale_price | rnk | Keep? |
|-------|-----|------------|-----|-------|
| Model 3 | ABC123 | 122.52 | 1 | ✅ |
| Model 3 | DEF456 | 118.52 | 2 | ✅ |
| Model S | GHI789 | 151.83 | 1 | ✅ |
| Model S | JKL012 | 142.95 | 2 | ✅ |

**Final Result:**
| brand | VIN | sale_price |
|-------|-----|------------|
| Model 3 | ABC123 | 122.52 |
| Model 3 | DEF456 | 118.52 |
| Model S | GHI789 | 151.83 |
| Model S | JKL012 | 142.95 |

---

## 🎯 Summary: Data Flow

```
Step 1: Extract Month
  sale_date → sale_month

Step 2: Calculate Months Elapsed
  sale_month → months_elapsed

Step 3: JOIN Tables
  + start_price, monthly_inflation_rate

Step 4: Calculate Multiplier
  (1 + rate/100)^months → multiplier

Step 5: Calculate Sale Price
  start_price × multiplier → sale_price

Step 6: Add Ranking
  RANK() OVER (PARTITION BY brand...) → rnk

Step 7: Filter
  WHERE rnk <= 2
```
