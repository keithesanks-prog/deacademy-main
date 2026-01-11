# 🔮 SQL LEAD() Function: Complete Guide

**Access data from the NEXT row without self-joins**

---

## 🤔 What is LEAD()?

**LEAD()** is a window function that lets you **peek at the next row** in your result set.

**In Plain English:** "Show me the value from the row below this one."

---

## 📝 Basic Syntax

```sql
LEAD(column, offset, default_value) OVER (ORDER BY sort_column)
```

**Parameters:**
- `column` - Which column to get from the next row
- `offset` - How many rows ahead to look (default: 1)
- `default_value` - What to show if there's no next row (default: NULL)
- `ORDER BY` - Determines what "next" means

---

## 📊 Visual Example: Simple LEAD()

**Sample Data:**
| product_name | price |
|--------------|-------|
| Laptop | 1000 |
| Mouse | 25 |
| Keyboard | 80 |

**Query:**
```sql
SELECT
    product_name,
    price,
    LEAD(product_name) OVER (ORDER BY price DESC) AS next_product
FROM products;
```

**Visual Execution:**
```
Step 1: ORDER BY price DESC
┌──────────────┬───────┐
│ product_name │ price │
├──────────────┼───────┤
│ Laptop       │ 1000  │ ← Current row
│ Keyboard     │ 80    │ ← LEAD gets this
│ Mouse        │ 25    │
└──────────────┴───────┘

Step 2: LEAD looks at next row
Laptop → LEAD() → Keyboard
```

**Result:**
| product_name | price | next_product |
|--------------|-------|--------------|
| Laptop | 1000 | Keyboard |
| Keyboard | 80 | Mouse |
| Mouse | 25 | NULL |

---

## 🎯 LEAD() with PARTITION BY

**The Problem:** Get the next higher-priced product **within the same category**.

**Sample Data:**
| product_name | category | unit_price |
|--------------|----------|------------|
| Laptop | Electronics | 1000.00 |
| Smartphone | Electronics | 500.00 |
| Headphones | Electronics | 80.00 |
| Coffee Maker | Appliances | 50.00 |
| Blender | Appliances | 30.00 |

**Query:**
```sql
SELECT
    product_name,
    category,
    unit_price,
    LEAD(product_name, 1, 'X') OVER (
        PARTITION BY category 
        ORDER BY unit_price DESC
    ) AS next_product_name,
    LEAD(unit_price, 1, 0) OVER (
        PARTITION BY category 
        ORDER BY unit_price DESC
    ) AS next_product_price
FROM products;
```

---

## 🔍 Step-by-Step Execution

**Step 1: PARTITION BY category**
```
Creates 2 windows:

Electronics:                Appliances:
┌──────────────┬───────┐    ┌──────────────┬───────┐
│ product_name │ price │    │ product_name │ price │
├──────────────┼───────┤    ├──────────────┼───────┤
│ Laptop       │ 1000  │    │ Coffee Maker │ 50    │
│ Smartphone   │ 500   │    │ Blender      │ 30    │
│ Headphones   │ 80    │    └──────────────┴───────┘
└──────────────┴───────┘
```

**Step 2: ORDER BY unit_price DESC (within each partition)**
```
Electronics (sorted):       Appliances (sorted):
1. Laptop (1000)            1. Coffee Maker (50)
2. Smartphone (500)         2. Blender (30)
3. Headphones (80)
```

**Step 3: LEAD() looks at next row in each partition**
```
Electronics:
Laptop → LEAD → Smartphone
Smartphone → LEAD → Headphones
Headphones → LEAD → NULL (no next row, use 'X' and 0)

Appliances:
Coffee Maker → LEAD → Blender
Blender → LEAD → NULL (no next row, use 'X' and 0)
```

**Final Result:**
| product_name | category | unit_price | next_product_name | next_product_price |
|--------------|----------|------------|-------------------|--------------------|
| Laptop | Electronics | 1000.00 | Smartphone | 500.00 |
| Smartphone | Electronics | 500.00 | Headphones | 80.00 |
| Headphones | Electronics | 80.00 | X | 0.00 |
| Coffee Maker | Appliances | 50.00 | Blender | 30.00 |
| Blender | Appliances | 30.00 | X | 0.00 |

---

## 💡 Understanding the Parameters

### **1. Offset (How Many Rows Ahead)**
```sql
LEAD(price, 1)  -- Next row (default)
LEAD(price, 2)  -- 2 rows ahead
LEAD(price, 3)  -- 3 rows ahead
```

**Example:**
| product | price | LEAD(price, 1) | LEAD(price, 2) |
|---------|-------|----------------|----------------|
| A | 100 | 50 | 25 |
| B | 50 | 25 | NULL |
| C | 25 | NULL | NULL |

---

### **2. Default Value (What to Show if No Next Row)**
```sql
LEAD(price, 1, 0)      -- Show 0 if no next row
LEAD(price, 1, -1)     -- Show -1 if no next row
LEAD(name, 1, 'X')     -- Show 'X' if no next row
```

**Example:**
| product | price | LEAD(price, 1, 0) | LEAD(price, 1, -1) |
|---------|-------|-------------------|--------------------|
| A | 100 | 50 | 50 |
| B | 50 | 25 | 25 |
| C | 25 | **0** | **-1** |

---

## 🎯 Common Use Cases

### **Use Case 1: Calculate Change Between Rows**
```sql
SELECT
    date,
    sales,
    LEAD(sales) OVER (ORDER BY date) AS next_day_sales,
    LEAD(sales) OVER (ORDER BY date) - sales AS sales_change
FROM daily_sales;
```

**Result:**
| date | sales | next_day_sales | sales_change |
|------|-------|----------------|--------------|
| 2023-01-01 | 100 | 150 | +50 |
| 2023-01-02 | 150 | 120 | -30 |
| 2023-01-03 | 120 | NULL | NULL |

---

### **Use Case 2: Find Next Event**
```sql
SELECT
    customer_id,
    order_date,
    LEAD(order_date) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) AS next_order_date
FROM orders;
```

**Shows when each customer's next order was.**

---

### **Use Case 3: Compare Current vs Next**
```sql
SELECT
    month,
    revenue,
    LEAD(revenue) OVER (ORDER BY month) AS next_month_revenue,
    CASE 
        WHEN LEAD(revenue) OVER (ORDER BY month) > revenue 
        THEN 'Growing'
        ELSE 'Declining'
    END AS trend
FROM monthly_revenue;
```

---

## 🏆 Practical Example: Comparing Rankings

**Problem:** Show each player's home runs and the home runs of the next 2 players behind them (per league).

**Sample Data:**
| player | league | home_runs |
|--------|--------|-----------|
| Aaron Judge | AL | 62 |
| Mike Trout | AL | 40 |
| Shohei Ohtani | AL | 34 |
| Giancarlo Stanton | AL | 31 |
| Mookie Betts | NL | 35 |
| Pete Alonso | NL | 40 |

**Query:**
```sql
SELECT
    player,
    league,
    home_runs,
    LEAD(home_runs, 1, 0) OVER (
        PARTITION BY league 
        ORDER BY home_runs DESC
    ) AS second_place,
    LEAD(home_runs, 2, 0) OVER (
        PARTITION BY league 
        ORDER BY home_runs DESC
    ) AS third_place
FROM baseball_stats;
```

**Result:**
| player | league | home_runs | second_place | third_place |
|--------|--------|-----------|--------------|-------------|
| Aaron Judge | AL | 62 | 40 | 34 |
| Mike Trout | AL | 40 | 34 | 31 |
| Shohei Ohtani | AL | 34 | 31 | 0 |
| Giancarlo Stanton | AL | 31 | 0 | 0 |
| Pete Alonso | NL | 40 | 35 | 0 |
| Mookie Betts | NL | 35 | 0 | 0 |

**Breakdown:**
- **LEAD(..., 1, 0)** - Look 1 row ahead (2nd place)
- **LEAD(..., 2, 0)** - Look 2 rows ahead (3rd place)
- **PARTITION BY league** - Separate AL and NL
- **ORDER BY home_runs DESC** - Highest first
- **Default 0** - Show 0 if no player exists

**Visual for Aaron Judge's row:**
```
AL (sorted by home_runs DESC):
1. Aaron Judge (62)  ← Current row
2. Mike Trout (40)   ← LEAD(..., 1) gets this
3. Ohtani (34)       ← LEAD(..., 2) gets this
4. Stanton (31)
```

---

## 🔄 LEAD() vs LAG()

| Function | Direction | Example |
|----------|-----------|---------|
| **LEAD()** | Looks **forward** (next row) | "What's the next sale?" |
| **LAG()** | Looks **backward** (previous row) | "What was the previous sale?" |

**Visual:**
```
Row 1: A  ← LAG looks here
Row 2: B  ← Current row
Row 3: C  ← LEAD looks here
```

---

## ⚠️ Common Mistakes

### **Mistake 1: Forgetting ORDER BY**
```sql
-- ❌ Wrong (random "next" row)
LEAD(price) OVER (PARTITION BY category)

-- ✅ Correct (ordered "next" row)
LEAD(price) OVER (PARTITION BY category ORDER BY price DESC)
```

### **Mistake 2: Not Handling NULL**
```sql
-- ❌ Wrong (last row shows NULL)
LEAD(product_name) OVER (ORDER BY price)

-- ✅ Correct (last row shows 'X')
LEAD(product_name, 1, 'X') OVER (ORDER BY price)
```

---

## 🎯 Practice Problem

**Problem:** Show each employee's salary and their next higher-paid colleague's salary in the same department.

**Sample Data:**
| employee | department | salary |
|----------|------------|--------|
| Alice | Sales | 60000 |
| Bob | Sales | 50000 |
| Charlie | IT | 80000 |
| Dave | IT | 70000 |

<details>
<summary>Click for solution</summary>

```sql
SELECT
    employee,
    department,
    salary,
    LEAD(employee, 1, 'Highest') OVER (
        PARTITION BY department 
        ORDER BY salary DESC
    ) AS next_higher_employee,
    LEAD(salary, 1, 0) OVER (
        PARTITION BY department 
        ORDER BY salary DESC
    ) AS next_higher_salary
FROM employees;
```

**Result:**
| employee | department | salary | next_higher_employee | next_higher_salary |
|----------|------------|--------|----------------------|--------------------|
| Alice | Sales | 60000 | Bob | 50000 |
| Bob | Sales | 50000 | Highest | 0 |
| Charlie | IT | 80000 | Dave | 70000 |
| Dave | IT | 70000 | Highest | 0 |

</details>

---

## 🚀 Key Takeaways

1. **LEAD() looks forward** to the next row
2. **Use PARTITION BY** to look within groups
3. **ORDER BY determines** what "next" means
4. **Set default values** to handle the last row
5. **Combine with calculations** to find changes/trends
