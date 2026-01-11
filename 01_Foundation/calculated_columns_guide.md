# 🧮 SQL Calculated Columns: Complete Guide

**Do math directly in the SELECT clause**

---

## 🤔 What Are Calculated Columns?

**Calculated columns** are new columns you create by doing math operations on existing columns or functions.

**In Plain English:** "Take this column, do some math, and show the result as a new column."

---

## 📝 Basic Syntax

```sql
SELECT
    column1,
    column2,
    column1 + column2 AS sum_column,
    column1 - column2 AS difference_column
FROM table;
```

**Key parts:**
1. Use existing columns
2. Apply math operators (`+`, `-`, `*`, `/`)
3. Give the result a name with `AS`

---

## 📊 Visual Example: Salary Difference

### **The Query**
```sql
SELECT
    first_name,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) AS difference
FROM employees;
```

### **Step-by-Step Visualization**

**Step 1: Start with base columns**
```
┌─────────────┬────────┐
│ first_name  │ salary │
├─────────────┼────────┤
│ Alice       │ 60000  │
│ Bob         │ 50000  │
│ Charlie     │ 80000  │
│ Dave        │ 70000  │
└─────────────┴────────┘
```

**Step 2: Add calculated average**
```
┌─────────────┬────────┬──────────┐
│ first_name  │ salary │ dept_avg │
├─────────────┼────────┼──────────┤
│ Alice       │ 60000  │ 55000    │ ← AVG(60000, 50000)
│ Bob         │ 50000  │ 55000    │ ← AVG(60000, 50000)
│ Charlie     │ 80000  │ 75000    │ ← AVG(80000, 70000)
│ Dave        │ 70000  │ 75000    │ ← AVG(80000, 70000)
└─────────────┴────────┴──────────┘
```

**Step 3: Calculate difference (salary - dept_avg)**
```
┌─────────────┬────────┬──────────┬────────────┐
│ first_name  │ salary │ dept_avg │ difference │
├─────────────┼────────┼──────────┼────────────┤
│ Alice       │ 60000  │ 55000    │ +5000      │ ← 60000 - 55000
│ Bob         │ 50000  │ 55000    │ -5000      │ ← 50000 - 55000
│ Charlie     │ 80000  │ 75000    │ +5000      │ ← 80000 - 75000
│ Dave        │ 70000  │ 75000    │ -5000      │ ← 70000 - 75000
└─────────────┴────────┴──────────┴────────────┘
```

**Visual breakdown for Alice's row:**
```
salary = 60000
   ↓
dept_avg = 55000
   ↓
difference = 60000 - 55000 = 5000
```

---

## 🎯 Common Calculations

### **1. Addition**
```sql
SELECT
    price,
    tax,
    price + tax AS total_cost
FROM orders;
```

**Example:**
| price | tax | total_cost |
|-------|-----|------------|
| 100 | 10 | 110 |
| 200 | 20 | 220 |

---

### **2. Subtraction**
```sql
SELECT
    revenue,
    costs,
    revenue - costs AS profit
FROM sales;
```

**Example:**
| revenue | costs | profit |
|---------|-------|--------|
| 1000 | 600 | 400 |
| 2000 | 1200 | 800 |

---

### **3. Multiplication**
```sql
SELECT
    quantity,
    unit_price,
    quantity * unit_price AS total_price
FROM order_items;
```

**Example:**
| quantity | unit_price | total_price |
|----------|------------|-------------|
| 5 | 20 | 100 |
| 10 | 15 | 150 |

---

### **4. Division (Percentage)**
```sql
SELECT
    sales,
    target,
    (sales / target) * 100 AS percent_of_target
FROM performance;
```

**Example:**
| sales | target | percent_of_target |
|-------|--------|-------------------|
| 80 | 100 | 80.0 |
| 120 | 100 | 120.0 |

---

## 🔗 Combining with Window Functions

### **Example: Percentage of Department Average**
```sql
SELECT
    employee,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg,
    (salary / AVG(salary) OVER (PARTITION BY department)) * 100 AS percent_of_avg
FROM employees;
```

**Visual:**
```
┌──────────┬────────┬──────────┬─────────────────┐
│ employee │ salary │ dept_avg │ percent_of_avg  │
├──────────┼────────┼──────────┼─────────────────┤
│ Alice    │ 60000  │ 55000    │ 109.09          │ ← (60000/55000)*100
│ Bob      │ 50000  │ 55000    │ 90.91           │ ← (50000/55000)*100
│ Charlie  │ 80000  │ 75000    │ 106.67          │ ← (80000/75000)*100
│ Dave     │ 70000  │ 75000    │ 93.33           │ ← (70000/75000)*100
└──────────┴────────┴──────────┴─────────────────┘
```

**Interpretation:**
- Alice earns 109% of Sales average (9% above)
- Bob earns 91% of Sales average (9% below)

---

## 🎯 Complex Calculations

### **Example: Total Compensation**
```sql
SELECT
    employee,
    base_salary,
    base_salary * 0.10 AS bonus,
    base_salary * 0.05 AS benefits,
    base_salary + (base_salary * 0.10) + (base_salary * 0.05) AS total_comp
FROM employees;
```

**Visual:**
```
┌──────────┬─────────────┬───────┬──────────┬────────────┐
│ employee │ base_salary │ bonus │ benefits │ total_comp │
├──────────┼─────────────┼───────┼──────────┼────────────┤
│ Alice    │ 50000       │ 5000  │ 2500     │ 57500      │
│          │             │   ↑   │    ↑     │     ↑      │
│          │             │  10%  │   5%     │ Sum of all │
└──────────┴─────────────┴───────┴──────────┴────────────┘
```

---

## 💡 Order of Operations

**SQL follows standard math order (PEMDAS):**

1. **Parentheses** `()`
2. **Multiplication/Division** `*`, `/`
3. **Addition/Subtraction** `+`, `-`

**Example:**
```sql
SELECT
    price * quantity + tax,           -- Multiply first, then add
    price * (quantity + tax)          -- Add first, then multiply
FROM orders;
```

**With values (price=10, quantity=5, tax=2):**
```
price * quantity + tax = 10 * 5 + 2 = 50 + 2 = 52
price * (quantity + tax) = 10 * (5 + 2) = 10 * 7 = 70
```

---

## ⚠️ Common Mistakes

### **Mistake 1: Dividing by Zero**
```sql
-- ❌ Wrong (crashes if denominator is 0)
SELECT revenue / costs AS profit_margin

-- ✅ Correct (handles zero)
SELECT 
    CASE 
        WHEN costs = 0 THEN 0
        ELSE revenue / costs
    END AS profit_margin
```

### **Mistake 2: NULL Values**
```sql
-- ❌ Wrong (NULL + anything = NULL)
SELECT price + tax AS total

-- ✅ Correct (replace NULL with 0)
SELECT price + COALESCE(tax, 0) AS total
```

---

## 🎯 Practice Problem

**Problem:** Calculate each product's price difference from the category average.

**Sample Data:**
| product | category | price |
|---------|----------|-------|
| Laptop | Electronics | 1200 |
| Mouse | Electronics | 25 |
| Desk | Furniture | 300 |
| Chair | Furniture | 150 |

<details>
<summary>Click for solution</summary>

```sql
SELECT
    product,
    category,
    price,
    AVG(price) OVER (PARTITION BY category) AS category_avg,
    price - AVG(price) OVER (PARTITION BY category) AS price_difference
FROM products;
```

**Result:**
| product | category | price | category_avg | price_difference |
|---------|----------|-------|--------------|------------------|
| Laptop | Electronics | 1200 | 612.50 | +587.50 |
| Mouse | Electronics | 25 | 612.50 | -587.50 |
| Desk | Furniture | 300 | 225.00 | +75.00 |
| Chair | Furniture | 150 | 225.00 | -75.00 |

</details>

---

## 🚀 Key Takeaways

1. **You can do math in SELECT** - Just like Excel formulas
2. **Use any operator** - `+`, `-`, `*`, `/`
3. **Combine columns and functions** - `salary - AVG(salary)`
4. **Give results names** - `AS difference`
5. **Watch for NULL and zero** - Use COALESCE and CASE
