# 🔍 How to Parse SQL Questions: Signal Words Guide

**Learn to identify key phrases that tell you EXACTLY what to do**

---

## 🎯 The Question Breakdown Method

**For every SQL question, ask yourself:**

1. **What columns do I need?** (SELECT)
2. **What's the grouping?** (PARTITION BY)
3. **What's the sorting?** (ORDER BY)
4. **What function do I use?** (LEAD, RANK, AVG, etc.)
5. **What are the edge cases?** (NULL handling, defaults)

---

## 📊 Example Question Breakdown

**Question:**
> "Retrieve a list of products along with their product_name, category and unit_price, including the name as "next_product_name" and price as "next_product_price" of the next higher-priced product **within the same category**. Additionally add 'X' to name in case where it is the last product in the list as per higher price logic and '0' for the price."

---

## 🔑 Signal Words & What They Mean

### **1. "within the same category"**
```
Signal: "within the same [column]"
Translation: PARTITION BY category
```

**Other examples:**
- "within each department" → `PARTITION BY department`
- "per customer" → `PARTITION BY customer_id`
- "for each region" → `PARTITION BY region`

---

### **2. "next higher-priced product"**
```
Signal: "next higher"
Translation: ORDER BY price ASC + LEAD()
```

**Why ASC?**
- "next higher" means you're going FROM low TO high
- Start at lowest, LEAD to next higher
- ASC = 100 → 200 → 300

**If it said "next lower-priced":**
- ORDER BY price DESC
- Start at highest, LEAD to next lower
- DESC = 300 → 200 → 100

---

### **3. "add 'X' to name... where it is the last product"**
```
Signal: "add [value] where it is the last"
Translation: Default value in LEAD()
```

**Syntax:**
```sql
LEAD(product_name, 1, 'X')  -- 'X' if no next row
LEAD(unit_price, 1, 0)      -- 0 if no next row
```

---

## 📝 Step-by-Step Question Parsing

**Question:**
> "Retrieve a list of products along with their product_name, category and unit_price, including the name as "next_product_name" and price as "next_product_price" of the next higher-priced product within the same category. Additionally add 'X' to name in case where it is the last product in the list as per higher price logic and '0' for the price."

---

### **Step 1: Identify Columns (SELECT)**

**Signal:** "Retrieve... product_name, category and unit_price"

```sql
SELECT
    product_name,
    category,
    unit_price,
    ...
```

---

### **Step 2: Identify Grouping (PARTITION BY)**

**Signal:** "within the same category"

```sql
PARTITION BY category
```

**Translation:** Each category is a separate group.

---

### **Step 3: Identify Sorting (ORDER BY)**

**Signal:** "next higher-priced"

```sql
ORDER BY unit_price ASC
```

**Why ASC?**
- "higher" means going UP
- Start low, go to higher
- ASC = ascending = low to high

---

### **Step 4: Identify Function**

**Signal:** "next... product"

```sql
LEAD(product_name, 1, 'X')
LEAD(unit_price, 1, 0)
```

**Translation:** Get value from the NEXT row.

---

### **Step 5: Identify Defaults**

**Signal:** "add 'X'... where it is the last product"

```sql
LEAD(product_name, 1, 'X')  -- Default to 'X'
LEAD(unit_price, 1, 0)      -- Default to 0
```

---

## ✅ Final Query

```sql
SELECT
    product_name,
    category,
    unit_price,
    LEAD(product_name, 1, 'X') OVER (
        PARTITION BY category 
        ORDER BY unit_price ASC
    ) AS next_product_name,
    LEAD(unit_price, 1, 0) OVER (
        PARTITION BY category 
        ORDER BY unit_price ASC
    ) AS next_product_price
FROM products;
```

---

## 🎯 Common Signal Words

### **Grouping Signals (PARTITION BY)**
| Signal | Means | Example |
|--------|-------|---------|
| "within the same [X]" | PARTITION BY X | "within the same category" |
| "per [X]" | PARTITION BY X | "per department" |
| "for each [X]" | PARTITION BY X | "for each customer" |
| "by [X]" | PARTITION BY X | "by region" |

---

### **Sorting Signals (ORDER BY)**
| Signal | Direction | Example |
|--------|-----------|---------|
| "highest to lowest" | DESC | ORDER BY price DESC |
| "lowest to highest" | ASC | ORDER BY price ASC |
| "next higher" | ASC | ORDER BY price ASC |
| "next lower" | DESC | ORDER BY price DESC |
| "most recent first" | DESC | ORDER BY date DESC |
| "oldest first" | ASC | ORDER BY date ASC |

---

### **Function Signals**
| Signal | Function | Example |
|--------|----------|---------|
| "next [X]" | LEAD() | "next product" |
| "previous [X]" | LAG() | "previous order" |
| "rank" | RANK() | "rank customers" |
| "row number" | ROW_NUMBER() | "number the rows" |
| "average per [X]" | AVG() OVER (PARTITION BY X) | "average per department" |
| "total per [X]" | SUM() OVER (PARTITION BY X) | "total per category" |

---

### **Default Value Signals**
| Signal | Means | Example |
|--------|-------|---------|
| "add 'X' where last" | Default value | LEAD(..., 1, 'X') |
| "use 0 if no next" | Default value | LEAD(..., 1, 0) |
| "show NULL if..." | Default NULL | LEAD(..., 1, NULL) |

---

## 🔍 Practice: Parse This Question

**Question:**
> "Show each employee's salary and the salary of the previous higher-paid employee within their department. If they are the highest paid, show 'Top Earner' and 0."

<details>
<summary>Click to see the breakdown</summary>

**Step 1: Columns**
- "employee's salary" → `salary`
- "previous... employee" → Need employee name too

**Step 2: Grouping**
- "within their department" → `PARTITION BY department`

**Step 3: Sorting**
- "previous higher-paid" → Start high, go to previous (lower)
- ORDER BY salary DESC

**Step 4: Function**
- "previous" → `LAG()` (not LEAD!)

**Step 5: Defaults**
- "show 'Top Earner' and 0" → `LAG(..., 1, 'Top Earner')` and `LAG(..., 1, 0)`

**Query:**
```sql
SELECT
    employee_name,
    department,
    salary,
    LAG(employee_name, 1, 'Top Earner') OVER (
        PARTITION BY department 
        ORDER BY salary DESC
    ) AS previous_higher_employee,
    LAG(salary, 1, 0) OVER (
        PARTITION BY department 
        ORDER BY salary DESC
    ) AS previous_higher_salary
FROM employees;
```

</details>

---

## 💡 Quick Checklist

**When reading a question, highlight:**

- [ ] **Grouping words:** "within", "per", "for each", "by"
- [ ] **Direction words:** "higher", "lower", "next", "previous"
- [ ] **Function words:** "rank", "number", "average", "total", "next", "previous"
- [ ] **Default words:** "if last", "if first", "if no", "show [X]"

---

## 🚀 Key Takeaways

1. **"within the same [X]"** = `PARTITION BY X`
2. **"next higher"** = `ORDER BY ASC` + `LEAD()`
3. **"next lower"** = `ORDER BY DESC` + `LEAD()`
4. **"previous"** = `LAG()` instead of `LEAD()`
5. **"add [X] if last"** = Default value in window function
