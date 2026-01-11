# 🔪 SQL String Splitting: Visual Breakdown

**How to split one column into multiple columns**

---

## 🎯 Example 1: Split Full Name into First and Last

### **The Data:**
| full_name |
|-----------|
| John Doe |
| Jane Smith |

### **The Goal:**
| first_name | last_name |
|------------|-----------|
| John | Doe |
| Jane | Smith |

---

## 🔨 Method 1: SUBSTRING_INDEX (MySQL)

### **The Expression:**
```sql
SUBSTRING_INDEX(full_name, ' ', 1)  -- First name
SUBSTRING_INDEX(full_name, ' ', -1) -- Last name
```

### **Visual Breakdown:**

```
Input: 'John Doe'

Step 1: Find the first part (before the space)
┌─────────────────────────────────┐
│ SUBSTRING_INDEX('John Doe', ' ', 1) │
│                                 │
│ Find the delimiter: ' '         │
│ Take 1st occurrence             │
│ = 'John'                        │
└─────────────────────────────────┘

Step 2: Find the last part (after the space)
┌─────────────────────────────────┐
│ SUBSTRING_INDEX('John Doe', ' ', -1)│
│                                 │
│ Find the delimiter: ' '         │
│ Take from the END (-1)          │
│ = 'Doe'                         │
└─────────────────────────────────┘
```

### **Full Query:**
```sql
SELECT 
    SUBSTRING_INDEX(full_name, ' ', 1) AS first_name,
    SUBSTRING_INDEX(full_name, ' ', -1) AS last_name
FROM people;
```

---

## 🎯 Example 2: Split Email into Username and Domain

### **The Data:**
| email |
|-------|
| john@example.com |
| jane@company.org |

### **The Goal:**
| username | domain |
|----------|--------|
| john | example.com |
| jane | company.org |

### **The Expression:**
```sql
SUBSTRING_INDEX(email, '@', 1)  -- Username
SUBSTRING_INDEX(email, '@', -1) -- Domain
```

### **Visual Breakdown:**

```
Input: 'john@example.com'

Step 1: Get username (before @)
┌─────────────────────────────────────┐
│ SUBSTRING_INDEX('john@example.com', '@', 1) │
│                                     │
│ Delimiter: '@'                      │
│ Position: 1 (first occurrence)      │
│ = 'john'                            │
└─────────────────────────────────────┘

Step 2: Get domain (after @)
┌─────────────────────────────────────┐
│ SUBSTRING_INDEX('john@example.com', '@', -1)│
│                                     │
│ Delimiter: '@'                      │
│ Position: -1 (from the end)         │
│ = 'example.com'                     │
└─────────────────────────────────────┘
```

---

## 🎯 Example 3: Split Phone Number

### **The Data:**
| phone |
|-------|
| 555-123-4567 |
| 555-987-6543 |

### **The Goal:**
| area_code | prefix | line |
|-----------|--------|------|
| 555 | 123 | 4567 |
| 555 | 987 | 6543 |

### **The Expression:**
```sql
SUBSTRING_INDEX(phone, '-', 1)                    -- Area code
SUBSTRING_INDEX(SUBSTRING_INDEX(phone, '-', 2), '-', -1)  -- Prefix
SUBSTRING_INDEX(phone, '-', -1)                   -- Line number
```

### **Visual Breakdown (Prefix - The Tricky One):**

```
Input: '555-123-4567'

Step 1: Get first 2 parts
┌─────────────────────────────────┐
│ SUBSTRING_INDEX('555-123-4567', '-', 2) │
│ = '555-123'                     │
└─────────────────────────────────┘
        ↓
Step 2: Get the last part of that
┌─────────────────────────────────┐
│ SUBSTRING_INDEX('555-123', '-', -1) │
│ = '123'                         │
└─────────────────────────────────┘
```

**Full Query:**
```sql
SELECT 
    SUBSTRING_INDEX(phone, '-', 1) AS area_code,
    SUBSTRING_INDEX(SUBSTRING_INDEX(phone, '-', 2), '-', -1) AS prefix,
    SUBSTRING_INDEX(phone, '-', -1) AS line
FROM contacts;
```

---

## 🎯 Example 4: SPLIT_PART (PostgreSQL)

**PostgreSQL uses a simpler function:**

```sql
SPLIT_PART(text, delimiter, position)
```

### **Example:**
```sql
SELECT 
    SPLIT_PART('John Doe', ' ', 1) AS first_name,  -- 'John'
    SPLIT_PART('John Doe', ' ', 2) AS last_name    -- 'Doe'
FROM people;
```

**Visual:**
```
'John Doe'
  ↓ Split by ' '
['John', 'Doe']
  ↓ Position 1 = 'John'
  ↓ Position 2 = 'Doe'
```

---

## 🎯 TRUNCATE vs String Splitting

### **TRUNCATE (Numbers Only)**
```sql
TRUNCATE(123.456, 2)  -- Cuts decimals
= 123.45
```

**NOT for strings!**

### **String Splitting (Text Only)**
```sql
SUBSTRING_INDEX('John Doe', ' ', 1)  -- Splits text
= 'John'
```

**NOT for numbers!**

---

## 📊 Quick Reference

| Function | Database | Purpose | Example |
|----------|----------|---------|---------|
| **SUBSTRING_INDEX** | MySQL | Split strings | `SUBSTRING_INDEX('a-b', '-', 1)` → `'a'` |
| **SPLIT_PART** | PostgreSQL | Split strings | `SPLIT_PART('a-b', '-', 1)` → `'a'` |
| **SUBSTRING** | All | Extract part | `SUBSTRING('hello', 1, 3)` → `'hel'` |
| **TRUNCATE** | All | Cut decimals | `TRUNCATE(123.99, 1)` → `123.9` |

---

## 💡 The Pattern

**SUBSTRING_INDEX syntax:**
```sql
SUBSTRING_INDEX(text, delimiter, position)
```

- **Positive position**: Count from the left
- **Negative position**: Count from the right

**Examples:**
```
'a-b-c-d'
SUBSTRING_INDEX(..., '-', 1)  → 'a'
SUBSTRING_INDEX(..., '-', 2)  → 'a-b'
SUBSTRING_INDEX(..., '-', -1) → 'd'
SUBSTRING_INDEX(..., '-', -2) → 'c-d'
```
