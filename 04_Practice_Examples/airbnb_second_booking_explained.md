# 🏠 Airbnb Second Booking Analysis - Complete Walkthrough

## 📋 Problem Statement

**Objective:** Write a query that outputs the average time taken (in days) from listing creation to the **second booking** for three groups of countries. Round to 3 decimals.

**Country Grouping Rules:**
- **Group 1 (Land Countries)**: Countries with 'land' in their name (e.g., England, Finland, Poland)
- **Group 2 (Ending A Countries)**: Countries ending with letter 'a' (e.g., India, Australia, China)
- **Group 3 (Other Countries)**: All remaining countries

**Output Column Names:**
- `country_type`: The category flag ('Land Countries', 'Ending A Countries', or 'Other Countries')
- `avg_days_to_second_booking`: Average days rounded to 3 decimals

---

## 📊 Sample Data

### `dim_bookings_airbnb`
| reservation_id | listing_id | reservation_time |
|----------------|------------|------------------|
| 1.566E+75 | 64a785 | 2019-11-11 00:08:33 |
| 1.567E+75 | 64a785 | 2019-11-15 10:20:00 |
| 1.568E+75 | 573064 | 2021-05-10 14:30:00 |

### `dim_listings_airbnb`
| listing_id | country | listing_created_at |
|------------|---------|-------------------|
| 64a785 | England | 2019-11-01 09:15:41 |
| 573064 | Australia | 2021-05-07 09:15:41 |

---

## 🎯 The Key Insight: Why ROW_NUMBER()?

### The Critical Question:
> **"Does the problem require me to select a specific row based on its order within a group?"**

✅ **YES!** We need:
- A **specific row** (the 2nd booking)
- Based on its **order** (chronologically)
- **Within a group** (per listing)

This is the **textbook use case** for `ROW_NUMBER()`.

---

## 🔧 Progressive Query Building

Let's build this query step-by-step and see how the results evolve at each stage.

---

### **🔹 Stage 1: Start with a Simple Join**

**Query:**
```sql
SELECT
    L.listing_id,
    L.country,
    L.listing_created_at,
    B.reservation_time
FROM 
    dim_bookings_airbnb B
INNER JOIN 
    dim_listings_airbnb L
    ON L.listing_id = B.listing_id
ORDER BY L.listing_id, B.reservation_time;
```

**Result at Stage 1:**
| listing_id | country | listing_created_at | reservation_time |
|------------|---------|-------------------|------------------|
| 64a785 | England | 2019-11-01 09:15:41 | 2019-11-11 08:33:00 |
| 64a785 | England | 2019-11-01 09:15:41 | 2019-11-15 10:20:00 |
| 64a785 | England | 2019-11-01 09:15:41 | 2019-11-20 14:00:00 |
| 573064 | Australia | 2021-05-07 09:15:41 | 2021-05-10 14:30:00 |
| 573064 | Australia | 2021-05-07 09:15:41 | 2021-05-12 09:00:00 |
| 573064 | Australia | 2021-05-07 09:15:41 | 2021-05-18 11:45:00 |
| 892341 | India | 2020-03-15 10:00:00 | 2020-03-20 12:00:00 |
| 892341 | India | 2020-03-15 10:00:00 | 2020-04-01 15:30:00 |

**What we see:** All bookings joined with their listing details. Multiple rows per listing, but no way to identify which is the 2nd booking yet.

---

### **🔹 Stage 2: Add ROW_NUMBER() to Rank Bookings**

**Query:**
```sql
SELECT
    L.listing_id,
    L.country,
    L.listing_created_at,
    B.reservation_time,
    ROW_NUMBER() OVER (
        PARTITION BY L.listing_id
        ORDER BY B.reservation_time ASC
    ) AS reservation_number
FROM 
    dim_bookings_airbnb B
INNER JOIN 
    dim_listings_airbnb L
    ON L.listing_id = B.listing_id
ORDER BY L.listing_id, B.reservation_time;
```

**Result at Stage 2:**
| listing_id | country | listing_created_at | reservation_time | reservation_number |
|------------|---------|-------------------|------------------|--------------------|
| 64a785 | England | 2019-11-01 09:15:41 | 2019-11-11 08:33:00 | **1** |
| 64a785 | England | 2019-11-01 09:15:41 | 2019-11-15 10:20:00 | **2** ← We want this! |
| 64a785 | England | 2019-11-01 09:15:41 | 2019-11-20 14:00:00 | **3** |
| 573064 | Australia | 2021-05-07 09:15:41 | 2021-05-10 14:30:00 | **1** |
| 573064 | Australia | 2021-05-07 09:15:41 | 2021-05-12 09:00:00 | **2** ← We want this! |
| 573064 | Australia | 2021-05-07 09:15:41 | 2021-05-18 11:45:00 | **3** |
| 892341 | India | 2020-03-15 10:00:00 | 2020-03-20 12:00:00 | **1** |
| 892341 | India | 2020-03-15 10:00:00 | 2020-04-01 15:30:00 | **2** ← We want this! |

**What changed:** Now each booking has a rank! Notice how the ranking **resets to 1** for each new listing_id. The 2nd booking for each listing is clearly marked.

---

### **🔹 Stage 3: Filter to Only 2nd Bookings**

**Query:**
```sql
WITH cte AS (
    SELECT
        L.listing_id,
        L.country,
        L.listing_created_at,
        B.reservation_time,
        ROW_NUMBER() OVER (
            PARTITION BY L.listing_id
            ORDER BY B.reservation_time ASC
        ) AS reservation_number
    FROM 
        dim_bookings_airbnb B
    INNER JOIN 
        dim_listings_airbnb L
        ON L.listing_id = B.listing_id
)
SELECT *
FROM cte
WHERE reservation_number = 2;
```

**Result at Stage 3:**
| listing_id | country | listing_created_at | reservation_time | reservation_number |
|------------|---------|-------------------|------------------|--------------------|
| 64a785 | England | 2019-11-01 09:15:41 | 2019-11-15 10:20:00 | 2 |
| 573064 | Australia | 2021-05-07 09:15:41 | 2021-05-12 09:00:00 | 2 |
| 892341 | India | 2020-03-15 10:00:00 | 2020-04-01 15:30:00 | 2 |

**What changed:** Now we only have the 2nd booking for each listing! All other bookings (1st, 3rd, 4th, etc.) are filtered out.

---

### **🔹 Stage 4: Calculate Days to 2nd Booking**

**Query:**
```sql
WITH cte AS (
    SELECT
        L.listing_id,
        L.country,
        L.listing_created_at,
        B.reservation_time,
        ROW_NUMBER() OVER (
            PARTITION BY L.listing_id
            ORDER BY B.reservation_time ASC
        ) AS reservation_number
    FROM 
        dim_bookings_airbnb B
    INNER JOIN 
        dim_listings_airbnb L
        ON L.listing_id = B.listing_id
)
SELECT 
    listing_id,
    country,
    DATEDIFF(reservation_time, listing_created_at) AS time_to_second_booking_days
FROM cte
WHERE reservation_number = 2;
```

**Result at Stage 4:**
| listing_id | country | time_to_second_booking_days |
|------------|---------|----------------------------|
| 64a785 | England | 14 |
| 573064 | Australia | 5 |
| 892341 | India | 17 |

**What changed:** We now have the **number of days** from listing creation to the 2nd booking for each listing.

---

### **🔹 Stage 5: Add Country Categorization (No Grouping Yet)**

**Query:**
```sql
WITH cte AS (
    SELECT
        L.listing_id,
        L.country,
        L.listing_created_at,
        B.reservation_time,
        ROW_NUMBER() OVER (
            PARTITION BY L.listing_id
            ORDER BY B.reservation_time ASC
        ) AS reservation_number
    FROM 
        dim_bookings_airbnb B
    INNER JOIN 
        dim_listings_airbnb L
        ON L.listing_id = B.listing_id
),
second_reservation AS (
    SELECT
        country,
        DATEDIFF(reservation_time, listing_created_at) AS time_to_second_booking_days
    FROM cte
    WHERE reservation_number = 2
)
SELECT 
    country,
    CASE 
        WHEN LOWER(country) LIKE '%land%' THEN 'Land Countries'
        WHEN LOWER(country) LIKE '%a' THEN 'Ending A Countries'
        ELSE 'Other Countries' 
    END AS country_type,
    time_to_second_booking_days
FROM second_reservation;
```

**Result at Stage 5:**
| country | country_type | time_to_second_booking_days |
|---------|--------------|----------------------------|
| England | Land Countries | 14 |
| Australia | Ending A Countries | 5 |
| India | Ending A Countries | 17 |
| Finland | Land Countries | 7 |
| Poland | Land Countries | 12 |
| China | Ending A Countries | 20 |
| France | Other Countries | 25 |
| Japan | Other Countries | 18 |

**What changed:** Each country is now categorized into one of the three groups. Still showing individual listings, not aggregated yet.

---

### **🔹 Stage 6: Group and Calculate Average (FINAL)**

**Query:**
```sql
WITH cte AS (
    SELECT
        L.listing_id,
        L.country,
        L.listing_created_at,
        B.reservation_time,
        ROW_NUMBER() OVER (
            PARTITION BY L.listing_id
            ORDER BY B.reservation_time ASC
        ) AS reservation_number
    FROM 
        dim_bookings_airbnb B
    INNER JOIN 
        dim_listings_airbnb L
        ON L.listing_id = B.listing_id
),
second_reservation AS (
    SELECT
        country,
        DATEDIFF(reservation_time, listing_created_at) AS time_to_second_booking_days
    FROM cte
    WHERE reservation_number = 2
)
SELECT 
    CASE 
        WHEN LOWER(country) LIKE '%land%' THEN 'Land Countries'
        WHEN LOWER(country) LIKE '%a' THEN 'Ending A Countries'
        ELSE 'Other Countries' 
    END AS country_type,
    ROUND(AVG(time_to_second_booking_days), 3) AS avg_days_to_second_booking
FROM second_reservation
GROUP BY 1
ORDER BY avg_days_to_second_booking DESC;
```

**FINAL Result:**
| country_type | avg_days_to_second_booking |
|--------------|---------------------------|
| Other Countries | 21.500 |
| Ending A Countries | 14.000 |
| Land Countries | 11.000 |

**What changed:** 
- **GROUP BY** collapsed multiple rows per country_type into single rows
- **AVG()** calculated the average days for each category
- **ROUND()** formatted to 3 decimal places
- **ORDER BY** sorted by average days (descending)

**Final Insight:** 
- "Land Countries" get their 2nd booking fastest (11 days on average)
- "Other Countries" take longest (21.5 days on average)

---

## 📊 Visual Summary of Transformation

```
Stage 1: All bookings joined
    ↓
Stage 2: Add ranking (1, 2, 3...) per listing
    ↓
Stage 3: Filter to only rank = 2
    ↓
Stage 4: Calculate days difference
    ↓
Stage 5: Categorize countries
    ↓
Stage 6: Group by category and average
    ↓
FINAL ANSWER ✅
```

---

## 🧠 Complete Solution

```sql
WITH cte AS (
    -- Step 1: Join listings and bookings and rank the reservations.
    SELECT
        L.listing_id,
        L.country,
        L.listing_created_at,
        B.reservation_time,
        
        -- Steps 2 & 3: Partition, Order, and Rank the reservations per listing.
        ROW_NUMBER() OVER (
            PARTITION BY L.listing_id  -- Resets the rank for every Listing ID
            ORDER BY B.reservation_time ASC -- Sorts the reservations chronologically
        ) AS reservation_number
    FROM 
        dim_bookings_airbnb B
    INNER JOIN 
        dim_listings_airbnb L
        ON L.listing_id = B.listing_id
),

second_reservation AS (
    -- Step 4: Filter to isolate only the **second** reservation (rank = 2).
    SELECT
        country,
        DATEDIFF(reservation_time, listing_created_at) AS time_to_second_booking_days
    FROM 
        cte
    WHERE 
        reservation_number = 2
)

-- Step 5: Group by country type and calculate the final average.
SELECT 
    CASE 
        WHEN LOWER(country) LIKE '%land%' THEN 'Land Countries'
        WHEN LOWER(country) LIKE '%a' THEN 'Ending A Countries'
        ELSE 'Other Countries' 
    END AS country_type,
    
    ROUND(AVG(time_to_second_booking_days), 3) AS avg_days_to_second_booking
FROM 
    second_reservation
GROUP BY 
    1
ORDER BY
    avg_days_to_second_booking DESC;
```

---

## 🔑 Key SQL Concepts Demonstrated

### 1. **ROW_NUMBER() with PARTITION BY**
The star of this solution. Enables ranking within groups.

```sql
ROW_NUMBER() OVER (
    PARTITION BY group_column  -- Creates separate groups
    ORDER BY sort_column       -- Defines ranking order
)
```

### 2. **Multi-Stage CTEs**
Breaking complex problems into manageable steps:
- **CTE 1**: Join and rank
- **CTE 2**: Filter and calculate
- **Final SELECT**: Categorize and aggregate

### 3. **CASE for Dynamic Categorization**
Creating custom groupings from text patterns.

### 4. **Date Arithmetic**
Using `DATEDIFF()` to calculate time differences.

### 5. **Aggregate Functions with GROUP BY**
Calculating averages per category.

---

## 💡 Why This Pattern Matters

This problem demonstrates the **"Nth per Group"** pattern, which appears frequently in:

- **E-commerce**: "2nd purchase per customer"
- **Analytics**: "Top 3 products per category"
- **User Behavior**: "First login per user per month"
- **Finance**: "Latest transaction per account"

### The Universal Template:

```sql
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY group_column
            ORDER BY sort_column
        ) AS rn
    FROM table_name
)
SELECT *
FROM ranked
WHERE rn = N;  -- Replace N with desired rank (1, 2, 3, etc.)
```

---

## 🎓 Practice Variations

Try modifying this problem:

1. **Change the rank**: Find average days to the **3rd** booking instead
2. **Different grouping**: Group by listing type instead of country
3. **Different metric**: Calculate **median** instead of average
4. **Add filters**: Only include listings created in 2021
5. **Multiple ranks**: Compare 1st vs 2nd vs 3rd booking times

---

## 🚨 Common Mistakes to Avoid

### ❌ Mistake 1: Using GROUP BY without ROW_NUMBER()
```sql
-- WRONG: This doesn't isolate the 2nd booking
SELECT country, AVG(DATEDIFF(reservation_time, listing_created_at))
FROM bookings
GROUP BY country;
```

### ❌ Mistake 2: Wrong ORDER BY direction
```sql
-- WRONG: DESC would make the latest booking = 1
ROW_NUMBER() OVER (PARTITION BY listing_id ORDER BY reservation_time DESC)
```

### ❌ Mistake 3: Missing PARTITION BY
```sql
-- WRONG: This ranks ALL bookings globally, not per listing
ROW_NUMBER() OVER (ORDER BY reservation_time ASC)
```

### ❌ Mistake 4: Incorrect DATEDIFF syntax
```sql
-- WRONG: Arguments in wrong order
DATEDIFF(listing_created_at, reservation_time)  -- Returns negative values!
```

---

## ✅ Verification Checklist

Before submitting your solution, verify:

- [ ] ROW_NUMBER() uses PARTITION BY listing_id
- [ ] ORDER BY sorts chronologically (ASC for earliest first)
- [ ] Filter uses `WHERE reservation_number = 2`
- [ ] DATEDIFF has correct argument order
- [ ] CASE statement covers all three groups
- [ ] Result is rounded to 3 decimals
- [ ] Column names match requirements exactly

---

## 🎯 Summary

This problem perfectly illustrates when ROW_NUMBER() is **mandatory**:

> **"Does the problem require me to select a specific row based on its order within a group?"**

If YES → Use ROW_NUMBER() with PARTITION BY

The solution follows a clear pattern:
1. **Rank** (ROW_NUMBER)
2. **Filter** (WHERE rn = N)
3. **Aggregate** (AVG, SUM, etc.)
4. **Group** (GROUP BY)

Master this pattern, and you'll solve 80% of SQL interview problems! 🚀
