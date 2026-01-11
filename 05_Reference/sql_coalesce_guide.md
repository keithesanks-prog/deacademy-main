# 🛡️ SQL COALESCE Function: Complete Guide

**Handle NULL values by providing fallback defaults**

---

## 🤔 What is COALESCE?

**COALESCE** is a function that **replaces NULL values** with a default value you specify.

**The Problem:**
- NULL values can break calculations (`NULL * 5 = NULL`)
- NULL values look bad in reports (empty cells)
- NULL values cause errors in string operations

**The Solution:**
```sql
COALESCE(value, 'default')
```

**In Plain English:** "If this value is NULL, use this other value instead."

---

## 💡 Real-World Analogy

**Think of COALESCE like a backup plan:**

```
Plan A: Use your phone number
  ↓ (NULL? Try Plan B)
Plan B: Use your mobile number
  ↓ (NULL? Try Plan C)
Plan C: Use 'No Phone Available'
```

**SQL:**
```sql
COALESCE(phone, mobile, 'No Phone Available')
```

---

## 📝 Basic Syntax

```sql
COALESCE(expression1, expression2, expression3, ...)
```

**Returns:** The **first non-NULL value** in the list.

**Examples:**
- `COALESCE(NULL, 'Hello')` → `'Hello'`
- `COALESCE(5, 10)` → `5` (5 is not NULL, so it returns 5)
- `COALESCE(NULL, NULL, 'Default')` → `'Default'`

---

## 🎯 How COALESCE Works

**Think of it like a waterfall:**

```
COALESCE(value1, value2, value3, 'default')
    ↓
Is value1 NULL? → No → Return value1 ✅
    ↓
Is value2 NULL? → No → Return value2 ✅
    ↓
Is value3 NULL? → No → Return value3 ✅
    ↓
Return 'default' ✅
```

---

## 📊 Visual Examples

### **Example 1: Simple Replacement**

**Before:**
| product_name | unit_price |
|--------------|------------|
| Laptop | 1200.00 |
| Mouse | NULL |
| Keyboard | 79.99 |

**Query:**
```sql
SELECT 
    product_name,
    COALESCE(unit_price, 0.00) AS adjusted_price
FROM products;
```

**After:**
| product_name | adjusted_price |
|--------------|----------------|
| Laptop | 1200.00 |
| Mouse | **0.00** |
| Keyboard | 79.99 |

---

### **Example 2: Multiple Fallbacks**

**Before:**
| employee | phone | mobile | office_phone |
|----------|-------|--------|--------------|
| Alice | NULL | NULL | 555-1234 |
| Bob | 555-5678 | NULL | NULL |
| Charlie | NULL | 555-9012 | NULL |

**Query:**
```sql
SELECT 
    employee,
    COALESCE(phone, mobile, office_phone, 'No Phone') AS contact_number
FROM employees;
```

**After:**
| employee | contact_number |
|----------|----------------|
| Alice | 555-1234 |
| Bob | 555-5678 |
| Charlie | 555-9012 |

**COALESCE checks each column in order and returns the first non-NULL value!**

---

## 🔍 Common Use Cases

### **Use Case 1: Default Values**

**Replace NULL with 0 for calculations:**
```sql
SELECT 
    order_id,
    COALESCE(quantity, 0) * COALESCE(unit_price, 0) AS total_amount
FROM order_details;
```

**Why?** `NULL * 100 = NULL`, but `0 * 100 = 0`

---

### **Use Case 2: String Concatenation**

**Avoid NULL in full names:**
```sql
SELECT 
    CONCAT(first_name, ' ', COALESCE(middle_name, ''), ' ', last_name) AS full_name
FROM customers;
```

**Example:**
- Input: `first_name = 'John'`, `middle_name = NULL`, `last_name = 'Doe'`
- Without COALESCE: `'John  Doe'` (double space)
- With COALESCE: `'John  Doe'` (still double space, but no NULL error)

**Better approach:**
```sql
SELECT 
    CONCAT_WS(' ', first_name, middle_name, last_name) AS full_name
FROM customers;
```
*(CONCAT_WS automatically skips NULLs)*

---

### **Use Case 3: Manager Hierarchy (Your Problem!)**

**Handle employees without managers:**
```sql
SELECT
    e.employee_id,
    e.first_name AS employee_first_name,
    COALESCE(m.first_name, 'Manager') AS manager_name,
    COALESCE(CAST(m.employee_id AS CHAR), 'X') AS manager_id
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;
```

**Breakdown:**
- `COALESCE(m.first_name, 'Manager')` → If manager is NULL, show 'Manager'
- `COALESCE(CAST(m.employee_id AS CHAR), 'X')` → If manager_id is NULL, show 'X'

---

## 🎯 Solution to Your Question

```sql
SELECT
    e.employee_id,
    e.first_name AS employee_first_name,
    COALESCE(m.first_name, 'Manager') AS manager_name,
    COALESCE(CAST(m.employee_id AS CHAR), 'X') AS manager_id
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;
```

**Why CAST?** Because `manager_id` is an INT, but we want to return 'X' (a string). CAST converts the INT to CHAR so both types match.

---

## 📊 Step-by-Step Walkthrough

**Sample Data:**
| employee_id | first_name | manager_id |
|-------------|------------|------------|
| 1 | John | 3 |
| 5 | Robert | NULL |

**Step 1: LEFT JOIN**
```
e.employee_id=1, e.first_name='John', e.manager_id=3
m.employee_id=3, m.first_name='Mike'

e.employee_id=5, e.first_name='Robert', e.manager_id=NULL
m.employee_id=NULL, m.first_name=NULL
```

**Step 2: COALESCE**
```
Row 1:
  COALESCE(m.first_name, 'Manager') → COALESCE('Mike', 'Manager') → 'Mike'
  COALESCE(m.employee_id, 'X') → COALESCE(3, 'X') → '3'

Row 2:
  COALESCE(m.first_name, 'Manager') → COALESCE(NULL, 'Manager') → 'Manager'
  COALESCE(m.employee_id, 'X') → COALESCE(NULL, 'X') → 'X'
```

**Final Result:**
| employee_id | employee_first_name | manager_name | manager_id |
|-------------|---------------------|--------------|------------|
| 1 | John | Mike | 3 |
| 5 | Robert | Manager | X |

---

## 💡 COALESCE vs CASE

**Both work the same:**

### **Using COALESCE:**
```sql
COALESCE(m.first_name, 'Manager')
```

### **Using CASE:**
```sql
CASE 
    WHEN m.first_name IS NULL THEN 'Manager'
    ELSE m.first_name
END
```

**COALESCE is just shorter!** Use it when you're replacing NULL with a default.

---

## ⚠️ Common Mistakes

### **Mistake 1: Type Mismatch**
```sql
-- ❌ Wrong (mixing INT and VARCHAR)
COALESCE(manager_id, 'X')

-- ✅ Correct (convert INT to VARCHAR first)
COALESCE(CAST(manager_id AS CHAR), 'X')
```

### **Mistake 2: Using COALESCE for Empty Strings**
```sql
-- ❌ Wrong (COALESCE doesn't replace empty strings)
COALESCE(name, 'Unknown')  -- If name = '', still returns ''

-- ✅ Correct (use NULLIF first)
COALESCE(NULLIF(name, ''), 'Unknown')
```

---

## 🎯 Quick Reference

| Task | Function | Example |
|------|----------|---------|
| Replace NULL with 0 | `COALESCE(value, 0)` | `COALESCE(price, 0)` |
| Replace NULL with text | `COALESCE(value, 'default')` | `COALESCE(name, 'Unknown')` |
| Multiple fallbacks | `COALESCE(v1, v2, v3, 'default')` | `COALESCE(phone, mobile, 'N/A')` |
| Convert type first | `COALESCE(CAST(int_col AS CHAR), 'X')` | `COALESCE(CAST(id AS CHAR), 'N/A')` |

---

## 💡 Pro Tip: COALESCE in Calculations

**Always use COALESCE in calculations to avoid NULL results:**

```sql
-- ❌ Bad (if quantity is NULL, result is NULL)
SELECT quantity * price AS total

-- ✅ Good (if quantity is NULL, uses 0)
SELECT COALESCE(quantity, 0) * COALESCE(price, 0) AS total
```
