# 🔢 SQL Math Functions Reference

**Quick reference for POWER, TRUNCATE, ROUND, and more**

---

## 🎯 POWER() - Exponents

**Purpose:** Raise a number to a power (e.g., 2³ = 8)

**Syntax:**
```sql
POWER(base, exponent)
```

**Examples:**

| Query | Result | Explanation |
|-------|--------|-------------|
| `POWER(2, 3)` | 8 | 2 × 2 × 2 = 8 |
| `POWER(10, 2)` | 100 | 10 × 10 = 100 |
| `POWER(1.05, 12)` | 1.7959 | Compound interest (5% for 12 months) |

**Real-World Use:**
```sql
-- Calculate compound interest
SELECT 
    start_price * POWER(1 + rate/100, months) AS final_price
FROM investments;
```

---

## ✂️ TRUNCATE() - Cut Off Decimals

**Purpose:** Remove decimal places (doesn't round, just cuts)

**Syntax:**
```sql
TRUNCATE(number, decimal_places)
```

**Examples:**

| Query | Result | Explanation |
|-------|--------|-------------|
| `TRUNCATE(123.456, 2)` | 123.45 | Cuts after 2 decimals |
| `TRUNCATE(123.456, 0)` | 123 | Cuts all decimals |
| `TRUNCATE(123.999, 1)` | 123.9 | Doesn't round! |

**vs ROUND():**
```sql
TRUNCATE(123.999, 1) → 123.9  (cuts)
ROUND(123.999, 1)    → 124.0  (rounds up)
```

---

## 🔄 ROUND() - Round to Nearest

**Purpose:** Round to the nearest value

**Syntax:**
```sql
ROUND(number, decimal_places)
```

**Examples:**

| Query | Result | Explanation |
|-------|--------|-------------|
| `ROUND(123.456, 2)` | 123.46 | Rounds up (6 > 5) |
| `ROUND(123.454, 2)` | 123.45 | Rounds down (4 < 5) |
| `ROUND(123.5, 0)` | 124 | Rounds to whole number |

---

## 📊 EXTRACT() - Get Part of a Date

**Purpose:** Pull out a specific part of a date (year, month, day)

**Syntax:**
```sql
EXTRACT(part FROM date)
```

**Examples:**

| Query | Result | Explanation |
|-------|--------|-------------|
| `EXTRACT(YEAR FROM '2023-08-15')` | 2023 | Gets the year |
| `EXTRACT(MONTH FROM '2023-08-15')` | 8 | Gets the month (August) |
| `EXTRACT(DAY FROM '2023-08-15')` | 15 | Gets the day |

**Real-World Use:**
```sql
-- Calculate months elapsed since January
SELECT 
    EXTRACT(MONTH FROM sale_date) - 1 AS months_elapsed
FROM sales;
```

---

## ➕ ABS() - Absolute Value

**Purpose:** Remove negative sign (distance from zero)

**Syntax:**
```sql
ABS(number)
```

**Examples:**

| Query | Result |
|-------|--------|
| `ABS(-5)` | 5 |
| `ABS(5)` | 5 |
| `ABS(-123.45)` | 123.45 |

---

## 📐 CEIL() and FLOOR() - Round Up/Down

**CEIL():** Always round **up** to the next integer  
**FLOOR():** Always round **down** to the previous integer

**Examples:**

| Query | Result |
|-------|--------|
| `CEIL(123.1)` | 124 |
| `CEIL(123.9)` | 124 |
| `FLOOR(123.1)` | 123 |
| `FLOOR(123.9)` | 123 |

---

## 🎯 MOD() - Remainder (Modulo)

**Purpose:** Get the remainder after division

**Syntax:**
```sql
MOD(dividend, divisor)
```

**Examples:**

| Query | Result | Explanation |
|-------|--------|-------------|
| `MOD(10, 3)` | 1 | 10 ÷ 3 = 3 remainder **1** |
| `MOD(15, 4)` | 3 | 15 ÷ 4 = 3 remainder **3** |
| `MOD(20, 5)` | 0 | 20 ÷ 5 = 4 remainder **0** |

**Use Case:** Check if a number is even/odd
```sql
SELECT 
    CASE 
        WHEN MOD(number, 2) = 0 THEN 'Even'
        ELSE 'Odd'
    END AS type
FROM numbers;
```

---

## 🧮 Quick Reference Table

| Function | Purpose | Example | Result |
|----------|---------|---------|--------|
| **POWER(x, y)** | x to the power of y | `POWER(2, 3)` | 8 |
| **TRUNCATE(x, d)** | Cut decimals | `TRUNCATE(123.99, 1)` | 123.9 |
| **ROUND(x, d)** | Round decimals | `ROUND(123.99, 1)` | 124.0 |
| **EXTRACT(p FROM d)** | Get date part | `EXTRACT(MONTH FROM date)` | 8 |
| **ABS(x)** | Absolute value | `ABS(-5)` | 5 |
| **CEIL(x)** | Round up | `CEIL(123.1)` | 124 |
| **FLOOR(x)** | Round down | `FLOOR(123.9)` | 123 |
| **MOD(x, y)** | Remainder | `MOD(10, 3)` | 1 |

---

## 💡 When to Use Each

**POWER():** Compound interest, exponential growth  
**TRUNCATE():** When you need exact cutoff (e.g., currency)  
**ROUND():** When you need proper rounding (e.g., averages)  
**EXTRACT():** When working with dates (months, years)  
**ABS():** When direction doesn't matter (distance, differences)  
**CEIL()/FLOOR():** When you need whole numbers (inventory, people)  
**MOD():** When you need to check divisibility (even/odd, cycles)
