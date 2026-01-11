# 🎧 SQL Date Arithmetic: MySQL vs SQL Server vs PostgreSQL

**This guide shows you the syntax differences across the 3 major SQL databases.**

---

## 📅 Function 1: Adding Days to a Date

**Goal:** Add 7 days to `'2025-08-09'`

### **MySQL**
```sql
DATE_ADD('2025-08-09', INTERVAL 7 DAY)
```
**Result:** `'2025-08-16'`

### **SQL Server**
```sql
DATEADD(day, 7, '2025-08-09')
```
**Result:** `'2025-08-16'`

### **PostgreSQL**
```sql
'2025-08-09'::date + INTERVAL '7 days'
```
**Result:** `'2025-08-16'`

---

## 📅 Function 2: Subtracting Days from a Date

**Goal:** Subtract 3 days from `'2025-08-09'`

### **MySQL**
```sql
DATE_SUB('2025-08-09', INTERVAL 3 DAY)
```
**Result:** `'2025-08-06'`

### **SQL Server**
```sql
DATEADD(day, -3, '2025-08-09')
```
**Result:** `'2025-08-06'`

### **PostgreSQL**
```sql
'2025-08-09'::date - INTERVAL '3 days'
```
**Result:** `'2025-08-06'`

---

## 📅 Function 3: Difference Between Two Dates

**Goal:** Find days between `'2025-08-15'` and `'2025-08-09'`

### **MySQL**
```sql
DATEDIFF('2025-08-15', '2025-08-09')
```
**Result:** `6`

### **SQL Server**
```sql
DATEDIFF(day, '2025-08-09', '2025-08-15')
```
**Result:** `6`

### **PostgreSQL**
```sql
'2025-08-15'::date - '2025-08-09'::date
```
**Result:** `6`

---

## 🎯 Quick Reference Table

| Operation | MySQL | SQL Server | PostgreSQL |
|-----------|-------|------------|------------|
| **Add Days** | `DATE_ADD(date, INTERVAL n DAY)` | `DATEADD(day, n, date)` | `date + INTERVAL 'n days'` |
| **Subtract Days** | `DATE_SUB(date, INTERVAL n DAY)` | `DATEADD(day, -n, date)` | `date - INTERVAL 'n days'` |
| **Difference** | `DATEDIFF(date1, date2)` | `DATEDIFF(day, date2, date1)` | `date1 - date2` |

---

## ⚠️ Key Differences to Watch

### **1. Argument Order**

**MySQL:**
```sql
DATE_ADD(date, INTERVAL 7 DAY)
       ↑ date first
```

**SQL Server:**
```sql
DATEADD(day, 7, date)
            ↑ date last
```

---

### **2. INTERVAL Keyword**

**MySQL:** Uses `INTERVAL` keyword
```sql
INTERVAL 7 DAY
```

**SQL Server:** No `INTERVAL` keyword
```sql
7  -- Just the number
```

**PostgreSQL:** Uses `INTERVAL` with quotes
```sql
INTERVAL '7 days'
```

---

### **3. DATEDIFF Argument Order**

**MySQL:**
```sql
DATEDIFF(end_date, start_date)
```

**SQL Server:**
```sql
DATEDIFF(unit, start_date, end_date)
         ↑ Must specify 'day', 'month', etc.
```

---

## 💡 How to Remember

**MySQL:** Think "Date function, then INTERVAL"
- `DATE_ADD(date, INTERVAL n DAY)`

**SQL Server:** Think "Function name has the unit in it"
- `DATEADD(day, n, date)`

**PostgreSQL:** Think "Math operators"
- `date + INTERVAL '7 days'`
- `date1 - date2`

---

## 🚀 Real-World Example

**Problem:** Calculate expected delivery (7 days after order) and last cancellation date (3 days before order).

### **MySQL**
```sql
SELECT 
    order_date,
    DATE_ADD(order_date, INTERVAL 7 DAY) AS delivery,
    DATE_SUB(order_date, INTERVAL 3 DAY) AS cancel_by
FROM orders;
```

### **SQL Server**
```sql
SELECT 
    order_date,
    DATEADD(day, 7, order_date) AS delivery,
    DATEADD(day, -3, order_date) AS cancel_by
FROM orders;
```

### **PostgreSQL**
```sql
SELECT 
    order_date,
    order_date + INTERVAL '7 days' AS delivery,
    order_date - INTERVAL '3 days' AS cancel_by
FROM orders;
```
