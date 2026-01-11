# 📅 SQL EXTRACT Function: Complete Guide

**Pull specific parts from dates (year, month, day, etc.)**

---

## 📝 Basic Syntax

```sql
EXTRACT(part FROM date_column)
```

**Parts you can extract:**
- `YEAR`, `MONTH`, `DAY`
- `HOUR`, `MINUTE`, `SECOND`
- `QUARTER`, `WEEK`

---

## 🎯 Common Extractions

### **1. EXTRACT YEAR**
```sql
SELECT EXTRACT(YEAR FROM '2023-11-29') AS year;
-- Result: 2023
```

### **2. EXTRACT MONTH**
```sql
SELECT EXTRACT(MONTH FROM '2023-11-29') AS month;
-- Result: 11
```

### **3. EXTRACT DAY**
```sql
SELECT EXTRACT(DAY FROM '2023-11-29') AS day;
-- Result: 29
```

---

## 📊 Visual Examples

### **Example 1: Breaking Down a Date**

**Before:**
| order_date |
|------------|
| 2023-11-29 |

**Query:**
```sql
SELECT 
    order_date,
    EXTRACT(YEAR FROM order_date) AS year,
    EXTRACT(MONTH FROM order_date) AS month,
    EXTRACT(DAY FROM order_date) AS day
FROM orders;
```

**After:**
| order_date | year | month | day |
|------------|------|-------|-----|
| 2023-11-29 | 2023 | 11 | 29 |

---

### **Example 2: Filter by Month**

**Get all orders from November:**
```sql
SELECT *
FROM orders
WHERE EXTRACT(MONTH FROM order_date) = 11;
```

---

### **Example 3: Group by Year**

**Total sales per year:**
```sql
SELECT 
    EXTRACT(YEAR FROM order_date) AS year,
    SUM(order_amount) AS total_sales
FROM orders
GROUP BY year;
```

**Result:**
| year | total_sales |
|------|-------------|
| 2022 | 150000 |
| 2023 | 280000 |

---

## 🔍 All Available Parts

| Part | Returns | Example |
|------|---------|---------|
| **YEAR** | 4-digit year | `2023` |
| **MONTH** | Month (1-12) | `11` |
| **DAY** | Day of month (1-31) | `29` |
| **HOUR** | Hour (0-23) | `14` |
| **MINUTE** | Minute (0-59) | `30` |
| **SECOND** | Second (0-59) | `45` |
| **QUARTER** | Quarter (1-4) | `4` |
| **WEEK** | Week of year (1-53) | `48` |

---

## 💡 Real-World Use Cases

### **Use Case 1: Calculate Months Elapsed**

**Problem:** How many months since January 2023?

```sql
SELECT 
    order_date,
    EXTRACT(MONTH FROM order_date) - 1 AS months_elapsed
FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2023;
```

**Example:**
- Order date: `2023-08-15`
- Month: `8`
- Months elapsed: `8 - 1 = 7`

---

### **Use Case 2: Filter by Quarter**

**Get Q4 2023 orders:**
```sql
SELECT *
FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2023
  AND EXTRACT(QUARTER FROM order_date) = 4;
```

**Q4 = October, November, December**

---

### **Use Case 3: Group by Month Name**

**Sales per month (with month names):**
```sql
SELECT 
    EXTRACT(MONTH FROM order_date) AS month_num,
    CASE EXTRACT(MONTH FROM order_date)
        WHEN 1 THEN 'January'
        WHEN 2 THEN 'February'
        WHEN 3 THEN 'March'
        WHEN 4 THEN 'April'
        WHEN 5 THEN 'May'
        WHEN 6 THEN 'June'
        WHEN 7 THEN 'July'
        WHEN 8 THEN 'August'
        WHEN 9 THEN 'September'
        WHEN 10 THEN 'October'
        WHEN 11 THEN 'November'
        WHEN 12 THEN 'December'
    END AS month_name,
    SUM(order_amount) AS total_sales
FROM orders
GROUP BY month_num, month_name
ORDER BY month_num;
```

---

## 🎯 Combining with Date Arithmetic

**Calculate days between dates:**
```sql
SELECT 
    order_date,
    EXTRACT(MONTH FROM order_date) - 1 AS months_since_jan,
    DATEDIFF(order_date, '2023-01-01') AS days_since_jan
FROM orders;
```

---

## 📊 Practical Example: The Tesla Problem

**Calculate months elapsed for compound interest:**

```sql
SELECT 
    sale_date,
    EXTRACT(MONTH FROM sale_date) - 1 AS months_elapsed,
    start_price * POWER(1.0067, EXTRACT(MONTH FROM sale_date) - 1) AS inflated_price
FROM sales;
```

**Breakdown:**
- Sale date: `2023-08-06`
- Month: `8`
- Months elapsed: `8 - 1 = 7`
- Inflated price: `start_price × 1.0067^7`

---

## ⚠️ Common Mistakes

### **Mistake 1: Forgetting FROM keyword**
```sql
-- ❌ Wrong
EXTRACT(MONTH order_date)

-- ✅ Correct
EXTRACT(MONTH FROM order_date)
```

### **Mistake 2: Using quotes around the part**
```sql
-- ❌ Wrong
EXTRACT('MONTH' FROM order_date)

-- ✅ Correct
EXTRACT(MONTH FROM order_date)
```

---

## 🎯 Quick Reference

| Task | Function | Example |
|------|----------|---------|
| Get year | `EXTRACT(YEAR FROM date)` | `2023` |
| Get month | `EXTRACT(MONTH FROM date)` | `11` |
| Get day | `EXTRACT(DAY FROM date)` | `29` |
| Get quarter | `EXTRACT(QUARTER FROM date)` | `4` |
| Get hour | `EXTRACT(HOUR FROM datetime)` | `14` |
| Filter by month | `WHERE EXTRACT(MONTH FROM date) = 11` | November only |
| Group by year | `GROUP BY EXTRACT(YEAR FROM date)` | Aggregate per year |

---

## 💡 MySQL Alternatives

**MySQL also has specific functions:**

| EXTRACT | MySQL Alternative |
|---------|-------------------|
| `EXTRACT(YEAR FROM date)` | `YEAR(date)` |
| `EXTRACT(MONTH FROM date)` | `MONTH(date)` |
| `EXTRACT(DAY FROM date)` | `DAY(date)` |

**Both work the same!**

```sql
-- These are equivalent:
EXTRACT(MONTH FROM order_date)
MONTH(order_date)
```
