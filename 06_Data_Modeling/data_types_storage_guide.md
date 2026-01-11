# 📊 Data Types & Storage - Reference Guide

**Essential guide for data modeling and database design**

---

## 🎯 The Storage Analogy

Think of data types like **different sized containers**:
- `TINYINT` = Shot glass (tiny, holds 1-255)
- `INT` = Water bottle (medium, holds millions)
- `BIGINT` = Swimming pool (huge, holds trillions)
- `CHAR(10)` = Fixed box (always 10 spaces, even if empty)
- `VARCHAR(100)` = Expandable bag (uses only what you need, up to 100)

---

## 📏 Numeric Data Types

### **Integer Types** (Whole Numbers)

| Type | Storage | Range | When to Use | Example |
|------|---------|-------|-------------|---------|
| **TINYINT** | 1 byte | 0 to 255 | Age, status codes, small counts | Age: 25 |
| **SMALLINT** | 2 bytes | -32,768 to 32,767 | Year, quantity | Year: 2024 |
| **INT** | 4 bytes | -2.1B to 2.1B | IDs, counts, most numbers | UserID: 1,234,567 |
| **BIGINT** | 8 bytes | -9.2 quintillion to 9.2 quintillion | Very large numbers, timestamps | Views: 9,876,543,210 |

**💡 Analogy:**
- TINYINT = **Shot glass** (1 oz)
- SMALLINT = **Coffee cup** (8 oz)
- INT = **Water bottle** (32 oz)
- BIGINT = **Swimming pool** (thousands of gallons)

**🎯 Rule of Thumb:**
- Use smallest type that fits your data
- Age? TINYINT (never > 255)
- Population? INT (millions)
- Social media likes? BIGINT (billions)

---

### **Decimal Types** (Numbers with Decimals)

| Type | Storage | Precision | When to Use | Example |
|------|---------|-----------|-------------|---------|
| **DECIMAL(10,2)** | Variable | Exact | Money, prices | Price: $19.99 |
| **FLOAT** | 4 bytes | ~7 digits | Scientific calculations | 3.14159 |
| **DOUBLE** | 8 bytes | ~15 digits | High precision science | 3.141592653589793 |

**💡 Analogy:**
- DECIMAL = **Cash register** (exact: $19.99)
- FLOAT = **Ruler** (approximate: ~3.14 inches)
- DOUBLE = **Laser measure** (very precise: 3.141592653589793 meters)

**⚠️ IMPORTANT:**
- **ALWAYS use DECIMAL for money!** (FLOAT/DOUBLE have rounding errors)
- DECIMAL(10,2) = 10 total digits, 2 after decimal
  - Max: 99,999,999.99
  - Example: $1,234.56

---

## 📝 String/Text Data Types

### **Fixed vs Variable Length**

| Type | Storage | Max Length | Padding | When to Use |
|------|---------|------------|---------|-------------|
| **CHAR(n)** | n bytes | 255 | Adds spaces | Fixed-length codes |
| **VARCHAR(n)** | Variable | 65,535 | No padding | Names, emails, text |
| **TEXT** | Variable | 65,535 | No padding | Long descriptions |
| **MEDIUMTEXT** | Variable | 16 MB | No padding | Articles |
| **LONGTEXT** | Variable | 4 GB | No padding | Books, large content |

**💡 Analogy: Storage Boxes**

**CHAR(10) = Fixed Box:**
```
┌──────────┐
│"Hi      "│  ← Always 10 spaces (wastes 8!)
└──────────┘
```

**VARCHAR(10) = Expandable Bag:**
```
┌──┐
│Hi│  ← Uses only 2 spaces!
└──┘
```

**🎯 When to Use:**

**CHAR:**
- ✅ State codes: `CHAR(2)` → "CA", "NY"
- ✅ Country codes: `CHAR(3)` → "USA", "CAN"
- ✅ Zip codes: `CHAR(5)` → "90210"
- ✅ Fixed-length IDs

**VARCHAR:**
- ✅ Names: `VARCHAR(100)`
- ✅ Emails: `VARCHAR(255)`
- ✅ Addresses: `VARCHAR(500)`
- ✅ Anything variable length!

**TEXT:**
- ✅ Blog posts
- ✅ Product descriptions
- ✅ Comments
- ✅ Long content

---

## 📅 Date & Time Data Types

| Type | Storage | Format | Range | Example |
|------|---------|--------|-------|---------|
| **DATE** | 3 bytes | YYYY-MM-DD | 1000-01-01 to 9999-12-31 | 2024-12-11 |
| **TIME** | 3 bytes | HH:MM:SS | -838:59:59 to 838:59:59 | 14:30:00 |
| **DATETIME** | 8 bytes | YYYY-MM-DD HH:MM:SS | 1000-01-01 to 9999-12-31 | 2024-12-11 14:30:00 |
| **TIMESTAMP** | 4 bytes | YYYY-MM-DD HH:MM:SS | 1970-01-01 to 2038-01-19 | 2024-12-11 14:30:00 |

**💡 Analogy:**
- **DATE** = Calendar page (just the day)
- **TIME** = Clock (just the time)
- **DATETIME** = Calendar + Clock (both!)
- **TIMESTAMP** = Digital watch with timezone

**🎯 When to Use:**

**DATE:**
- ✅ Birthday: `1990-05-15`
- ✅ Event date
- ✅ No time needed

**DATETIME:**
- ✅ Order placed: `2024-12-11 14:30:00`
- ✅ Post created
- ✅ Need exact time

**TIMESTAMP:**
- ✅ Last login
- ✅ Record created/updated
- ✅ Auto-updates on change

---

## 💾 Storage Size Comparison

**Visual Comparison:**

```
TINYINT (1 byte)    ▪
SMALLINT (2 bytes)  ▪▪
INT (4 bytes)       ▪▪▪▪
BIGINT (8 bytes)    ▪▪▪▪▪▪▪▪

CHAR(10)            ▪▪▪▪▪▪▪▪▪▪ (always 10)
VARCHAR(10) "Hi"    ▪▪ (only 2 used)

DATE (3 bytes)      ▪▪▪
DATETIME (8 bytes)  ▪▪▪▪▪▪▪▪
```

---

## 🎯 Data Modeling Best Practices

### **1. Choose the Right Size**

❌ **BAD:**
```sql
CREATE TABLE users (
    age BIGINT,           -- Overkill! Max age is ~120
    zip_code VARCHAR(255) -- Waste! Zip is always 5-10 chars
);
```

✅ **GOOD:**
```sql
CREATE TABLE users (
    age TINYINT,          -- Perfect! 0-255
    zip_code CHAR(5)      -- Exact fit for US zip
);
```

### **2. Money = DECIMAL, Always!**

❌ **BAD:**
```sql
price FLOAT  -- Rounding errors! $0.01 becomes $0.0099999
```

✅ **GOOD:**
```sql
price DECIMAL(10,2)  -- Exact! $19.99 stays $19.99
```

### **3. Use VARCHAR for Variable Text**

❌ **BAD:**
```sql
name CHAR(100)  -- Wastes 90 bytes for "Alice"
```

✅ **GOOD:**
```sql
name VARCHAR(100)  -- Uses only 5 bytes for "Alice"
```

### **4. TIMESTAMP for Auto-Updates**

✅ **GOOD:**
```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

---

## 📊 Real-World Example: E-Commerce Database

```sql
CREATE TABLE products (
    -- IDs
    product_id INT PRIMARY KEY,              -- Millions of products
    category_id SMALLINT,                    -- Few hundred categories
    
    -- Text
    name VARCHAR(200),                       -- Variable length
    sku CHAR(10),                           -- Fixed: "PROD-12345"
    description TEXT,                        -- Long text
    
    -- Numbers
    price DECIMAL(10,2),                    -- Money: $9,999,999.99
    stock_quantity INT,                      -- Can be millions
    weight_kg DECIMAL(8,2),                 -- 999,999.99 kg
    
    -- Flags
    is_active TINYINT(1),                   -- Boolean: 0 or 1
    rating TINYINT,                         -- 1-5 stars
    
    -- Dates
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    launch_date DATE                         -- Just the day
);
```

---

## 🎓 Quick Decision Tree

**Choosing Data Type:**

```
Is it a number?
├─ Yes → Whole number?
│  ├─ Yes → How big?
│  │  ├─ 0-255 → TINYINT
│  │  ├─ Thousands → SMALLINT
│  │  ├─ Millions → INT
│  │  └─ Billions+ → BIGINT
│  └─ No (decimals) → Money?
│     ├─ Yes → DECIMAL(10,2)
│     └─ No → FLOAT/DOUBLE
└─ No → Text?
   ├─ Fixed length? → CHAR(n)
   ├─ Variable length? → VARCHAR(n)
   ├─ Long text? → TEXT
   └─ Date/Time?
      ├─ Just date → DATE
      ├─ Date + Time → DATETIME
      └─ Auto-update → TIMESTAMP
```

---

## 💡 Key Takeaways

1. **Size Matters** - Use smallest type that fits
2. **Money = DECIMAL** - Never FLOAT for currency
3. **CHAR vs VARCHAR** - Fixed vs. Variable
4. **TIMESTAMP** - Auto-updates for created/updated
5. **Think Storage** - Millions of rows = bytes matter!

---

## 📚 Common Patterns

| Data | Type | Example |
|------|------|---------|
| User ID | INT | 1234567 |
| Age | TINYINT | 25 |
| Price | DECIMAL(10,2) | $19.99 |
| Name | VARCHAR(100) | "Alice Smith" |
| Email | VARCHAR(255) | "alice@example.com" |
| State | CHAR(2) | "CA" |
| Description | TEXT | Long paragraph... |
| Birthday | DATE | 1990-05-15 |
| Order Time | DATETIME | 2024-12-11 14:30:00 |
| Last Login | TIMESTAMP | Auto-updates |

---

**Remember:** Choose data types like choosing containers - use the right size for the job!
