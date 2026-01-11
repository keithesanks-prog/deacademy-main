# 🧹 SQL TRIM Function: Complete Guide

**Remove unwanted spaces and characters from strings**

---

## 📝 Basic Syntax

```sql
TRIM([LEADING | TRAILING | BOTH] [characters] FROM string)
```

**Simplified (most common):**
```sql
TRIM(string)  -- Removes leading and trailing spaces
```

---

## 🎯 The Three Types of TRIM

### **1. TRIM() - Remove Both Sides (Default)**
```sql
SELECT TRIM('  Hello  ') AS result;
-- Result: 'Hello'
```

### **2. LTRIM() - Remove Left Side Only**
```sql
SELECT LTRIM('  Hello  ') AS result;
-- Result: 'Hello  '
```

### **3. RTRIM() - Remove Right Side Only**
```sql
SELECT RTRIM('  Hello  ') AS result;
-- Result: '  Hello'
```

---

## 📊 Visual Examples

### **Example 1: Basic TRIM**

**Before:**
| address |
|---------|
| `'  123 Main St  '` |

**Query:**
```sql
SELECT TRIM(address) AS trimmed_address
FROM customers;
```

**After:**
| trimmed_address |
|-----------------|
| `'123 Main St'` |

---

### **Example 2: TRIM Specific Characters**

**Before:**
| product_name |
|--------------|
| `'...Laptop...'` |

**Query:**
```sql
SELECT TRIM('.' FROM product_name) AS cleaned_name
FROM products;
```

**After:**
| cleaned_name |
|--------------|
| `'Laptop'` |

---

### **Example 3: TRIM LEADING**

**Before:**
| code |
|------|
| `'000123'` |

**Query:**
```sql
SELECT TRIM(LEADING '0' FROM code) AS trimmed_code
FROM products;
```

**After:**
| trimmed_code |
|--------------|
| `'123'` |

---

## 🔍 Common Use Cases

### **Use Case 1: Clean User Input**
```sql
SELECT 
    customer_id,
    TRIM(customer_name) AS clean_name,
    TRIM(email) AS clean_email
FROM customers;
```

### **Use Case 2: Remove Prefixes**
```sql
SELECT 
    TRIM(LEADING 'Mr. ' FROM name) AS first_name
FROM employees;
```
**Example:** `'Mr. John Smith'` → `'John Smith'`

### **Use Case 3: Remove File Extensions**
```sql
SELECT 
    TRIM(TRAILING '.txt' FROM filename) AS base_name
FROM files;
```
**Example:** `'document.txt'` → `'document'`

---

## 💡 MySQL-Specific Syntax

**MySQL supports all three:**

| Function | Removes | Example |
|----------|---------|---------|
| **TRIM()** | Both sides | `TRIM('  Hi  ')` → `'Hi'` |
| **LTRIM()** | Left side | `LTRIM('  Hi  ')` → `'Hi  '` |
| **RTRIM()** | Right side | `RTRIM('  Hi  ')` → `'  Hi'` |

---

## 🎯 Practice Problem Solution

**Question:** Retrieve customer information with trimmed address.

```sql
SELECT 
    customer_id,
    customer_name AS FullName,
    TRIM(address) AS TrimmedAddress,
    city
FROM customers;
```

---

## 📊 Before & After Comparison

**Before TRIM:**
| customer_id | customer_name | address | city |
|-------------|---------------|---------|------|
| 101 | John Smith | `'  123 Main St  '` | New York |
| 102 | Alice Johnson | `'456 Elm Ave'` | Los Angeles |

**After TRIM:**
| customer_id | FullName | TrimmedAddress | city |
|-------------|----------|----------------|------|
| 101 | John Smith | `'123 Main St'` | New York |
| 102 | Alice Johnson | `'456 Elm Ave'` | Los Angeles |

---

## 🔧 Advanced: Trimming Multiple Characters

**Remove multiple characters:**
```sql
SELECT TRIM('.,!? ' FROM text_column) AS cleaned_text
FROM messages;
```

**Example:**
- Input: `'...Hello!!!'`
- Output: `'Hello'`

---

## ⚠️ Common Mistakes

### **Mistake 1: Forgetting FROM keyword**
```sql
-- ❌ Wrong
TRIM('0' code)

-- ✅ Correct
TRIM('0' FROM code)
```

### **Mistake 2: Trying to TRIM middle spaces**
```sql
-- TRIM only removes leading/trailing spaces
TRIM('Hello  World')  -- Still has double space in middle
-- Result: 'Hello  World'

-- Use REPLACE for middle spaces
REPLACE('Hello  World', '  ', ' ')
-- Result: 'Hello World'
```

---

## 🎯 Quick Reference

| Task | Function | Example |
|------|----------|---------|
| Remove all spaces (both sides) | `TRIM()` | `TRIM('  Hi  ')` |
| Remove left spaces | `LTRIM()` | `LTRIM('  Hi')` |
| Remove right spaces | `RTRIM()` | `RTRIM('Hi  ')` |
| Remove specific character | `TRIM(char FROM str)` | `TRIM('.' FROM '..Hi..')` |
| Remove leading zeros | `TRIM(LEADING '0' FROM str)` | `TRIM(LEADING '0' FROM '00123')` |

---

## 💡 Pro Tip: Combining TRIM with Other Functions

**Clean and concatenate:**
```sql
SELECT 
    CONCAT(TRIM(first_name), ' ', TRIM(last_name)) AS full_name
FROM employees;
```

**Clean and compare:**
```sql
SELECT *
FROM customers
WHERE TRIM(LOWER(email)) = 'john@example.com';
```
