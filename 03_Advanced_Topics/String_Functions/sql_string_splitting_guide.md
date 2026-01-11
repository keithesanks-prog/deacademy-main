# 📱 SQL String Splitting Guide - Phone Names Problem

## 🎯 Problem Statement

Split `phone_names` like `'Acer - Iconia Talk S'` into two columns:
- **brand**: `'Acer'`
- **model_name**: `'Iconia Talk S'`

**Delimiters can be:** `-`, `:`, `*`, or `~`

---

## 🔍 Understanding the Problem

### **Sample Data:**
| phone_names | Desired Output |
|-------------|----------------|
| `'Acer - Iconia Talk S'` | brand: `'Acer'`, model: `'Iconia Talk S'` |
| `'Apple * iPhone 12'` | brand: `'Apple'`, model: `'iPhone 12'` |
| `'Samsung : Galaxy S21'` | brand: `'Samsung'`, model: `'Galaxy S21'` |
| `'Google ~ Pixel 6'` | brand: `'Google'`, model: `'Pixel 6'` |

---

## 💡 Solution Strategy

### **Step 1: Find the Delimiter Position**

We need to find which delimiter exists and where it is:

```sql
-- Find position of each delimiter
INSTR(phone_names, '-')  -- Returns position of '-', or 0 if not found
INSTR(phone_names, ':')  -- Returns position of ':', or 0 if not found
INSTR(phone_names, '*')  -- Returns position of '*', or 0 if not found
INSTR(phone_names, '~')  -- Returns position of '~', or 0 if not found
```

### **Step 2: Get the Actual Delimiter Position**

Use `MAX()` to find which delimiter exists:

```sql
MAX(
    INSTR(phone_names, '-'),
    INSTR(phone_names, ':'),
    INSTR(phone_names, '*'),
    INSTR(phone_names, '~')
) AS delimiter_position
```

### **Step 3: Extract Brand (Before Delimiter)**

```sql
TRIM(SUBSTR(phone_names, 1, delimiter_position - 1)) AS brand
```

**Breakdown:**
- `SUBSTR(phone_names, 1, delimiter_position - 1)` - Get text from position 1 to just before delimiter
- `TRIM()` - Remove leading/trailing spaces

### **Step 4: Extract Model (After Delimiter)**

```sql
TRIM(SUBSTR(phone_names, delimiter_position + 1)) AS model_name
```

**Breakdown:**
- `SUBSTR(phone_names, delimiter_position + 1)` - Get text starting after the delimiter
- `TRIM()` - Remove leading/trailing spaces

---

## ✅ Complete Solution

### **Method 1: Using Subquery (Easier to Understand)**

```sql
SELECT 
    phone_id,
    phone_names,
    price_usd,
    TRIM(SUBSTR(phone_names, 1, delimiter_pos - 1)) AS brand,
    TRIM(SUBSTR(phone_names, delimiter_pos + 1)) AS model_name
FROM (
    SELECT 
        phone_id,
        phone_names,
        price_usd,
        MAX(
            INSTR(phone_names, '-'),
            INSTR(phone_names, ':'),
            INSTR(phone_names, '*'),
            INSTR(phone_names, '~')
        ) AS delimiter_pos
    FROM dim_phones_apple
) AS phones_with_delimiter;
```

---

### **Method 2: Using CASE (More Explicit)**

```sql
SELECT 
    phone_id,
    phone_names,
    price_usd,
    CASE
        WHEN INSTR(phone_names, '-') > 0 THEN 
            TRIM(SUBSTR(phone_names, 1, INSTR(phone_names, '-') - 1))
        WHEN INSTR(phone_names, ':') > 0 THEN 
            TRIM(SUBSTR(phone_names, 1, INSTR(phone_names, ':') - 1))
        WHEN INSTR(phone_names, '*') > 0 THEN 
            TRIM(SUBSTR(phone_names, 1, INSTR(phone_names, '*') - 1))
        WHEN INSTR(phone_names, '~') > 0 THEN 
            TRIM(SUBSTR(phone_names, 1, INSTR(phone_names, '~') - 1))
    END AS brand,
    CASE
        WHEN INSTR(phone_names, '-') > 0 THEN 
            TRIM(SUBSTR(phone_names, INSTR(phone_names, '-') + 1))
        WHEN INSTR(phone_names, ':') > 0 THEN 
            TRIM(SUBSTR(phone_names, INSTR(phone_names, ':') + 1))
        WHEN INSTR(phone_names, '*') > 0 THEN 
            TRIM(SUBSTR(phone_names, INSTR(phone_names, '*') + 1))
        WHEN INSTR(phone_names, '~') > 0 THEN 
            TRIM(SUBSTR(phone_names, INSTR(phone_names, '~') + 1))
    END AS model_name
FROM dim_phones_apple;
```

---

## 📊 Expected Output

| phone_id | phone_names | price_usd | brand | model_name |
|----------|-------------|-----------|-------|------------|
| 2695bb9 | Acer - Iconia Talk S | 759.91 | Acer | Iconia Talk S |
| 123abc | Apple * iPhone 12 | 999.00 | Apple | iPhone 12 |
| 456def | Samsung : Galaxy S21 | 899.00 | Samsung | Galaxy S21 |

---

## 🔧 Key SQL Functions Used

### **INSTR(string, substring)**
Returns the position of substring in string (1-indexed), or 0 if not found.

```sql
INSTR('Acer - Iconia', '-')  → 6  (position of '-')
INSTR('Acer - Iconia', '*')  → 0  (not found)
```

### **SUBSTR(string, start, length)**
Extracts a substring starting at position `start` for `length` characters.

```sql
SUBSTR('Acer - Iconia', 1, 4)   → 'Acer'
SUBSTR('Acer - Iconia', 8)      → 'Iconia' (from position 8 to end)
```

### **TRIM(string)**
Removes leading and trailing whitespace.

```sql
TRIM('  Acer  ')  → 'Acer'
```

### **MAX(value1, value2, ...)**
Returns the largest value.

```sql
MAX(0, 6, 0, 0)  → 6
```

---

## 💡 Step-by-Step Example

**Input:** `'Acer - Iconia Talk S'`

### **Step 1: Find delimiter positions**
```sql
INSTR('Acer - Iconia Talk S', '-')  → 6
INSTR('Acer - Iconia Talk S', ':')  → 0
INSTR('Acer - Iconia Talk S', '*')  → 0
INSTR('Acer - Iconia Talk S', '~')  → 0
```

### **Step 2: Get the actual position**
```sql
MAX(6, 0, 0, 0)  → 6
```

### **Step 3: Extract brand**
```sql
SUBSTR('Acer - Iconia Talk S', 1, 6 - 1)  → 'Acer '
TRIM('Acer ')  → 'Acer'
```

### **Step 4: Extract model**
```sql
SUBSTR('Acer - Iconia Talk S', 6 + 1)  → ' Iconia Talk S'
TRIM(' Iconia Talk S')  → 'Iconia Talk S'
```

**Final Output:** brand = `'Acer'`, model_name = `'Iconia Talk S'`

---

## 🎯 Practice Exercise

Try this query with your data:

```sql
SELECT 
    phone_id,
    phone_names,
    price_usd,
    TRIM(SUBSTR(phone_names, 1, 
        MAX(
            INSTR(phone_names, '-'),
            INSTR(phone_names, ':'),
            INSTR(phone_names, '*'),
            INSTR(phone_names, '~')
        ) - 1
    )) AS brand,
    TRIM(SUBSTR(phone_names, 
        MAX(
            INSTR(phone_names, '-'),
            INSTR(phone_names, ':'),
            INSTR(phone_names, '*'),
            INSTR(phone_names, '~')
        ) + 1
    )) AS model_name
FROM dim_phones_apple;
```

---

## 🚨 Common Mistakes to Avoid

### **❌ Mistake 1: Forgetting TRIM()**
```sql
SUBSTR(phone_names, 1, pos - 1)  -- May have trailing spaces
```

### **✅ Correct:**
```sql
TRIM(SUBSTR(phone_names, 1, pos - 1))  -- No spaces
```

### **❌ Mistake 2: Wrong SUBSTR positions**
```sql
SUBSTR(phone_names, pos)  -- Includes the delimiter!
```

### **✅ Correct:**
```sql
SUBSTR(phone_names, pos + 1)  -- Starts after delimiter
```

---

## 💡 Alternative: REPLACE Approach

If you want to standardize all delimiters first:

```sql
SELECT 
    phone_id,
    TRIM(SUBSTR(
        REPLACE(REPLACE(REPLACE(phone_names, ':', '-'), '*', '-'), '~', '-'),
        1,
        INSTR(REPLACE(REPLACE(REPLACE(phone_names, ':', '-'), '*', '-'), '~', '-'), '-') - 1
    )) AS brand,
    TRIM(SUBSTR(
        REPLACE(REPLACE(REPLACE(phone_names, ':', '-'), '*', '-'), '~', '-'),
        INSTR(REPLACE(REPLACE(REPLACE(phone_names, ':', '-'), '*', '-'), '~', '-'), '-') + 1
    )) AS model_name
FROM dim_phones_apple;
```

This replaces all delimiters with `-` first, then splits on `-`.

---

## ✅ Summary

**To split strings in SQL:**
1. Find the delimiter position using `INSTR()`
2. Extract text before delimiter using `SUBSTR(string, 1, position - 1)`
3. Extract text after delimiter using `SUBSTR(string, position + 1)`
4. Use `TRIM()` to remove spaces
5. Use `MAX()` when multiple possible delimiters exist

Good luck! 🚀
