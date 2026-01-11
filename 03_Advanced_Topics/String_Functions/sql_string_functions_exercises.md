# 🎓 SQL String Functions Practice Exercises

## 🚀 Getting Started

### **Step 1: Set Up Your Database**
1. Open SQLite Online (https://sqliteonline.com/)
2. Run the `sql_string_practice_setup.sql` file to create tables with sample data
3. Verify tables were created by running: `SELECT * FROM phones;`

---

## 📚 String Functions Reference

Before starting exercises, here are the key functions you'll use:

### **INSTR(string, substring)**
Finds the position of substring in string (returns 0 if not found)
```sql
INSTR('Hello World', 'World')  → 7
INSTR('Hello World', 'xyz')    → 0
```

### **SUBSTR(string, start, length)**
Extracts a substring
```sql
SUBSTR('Hello World', 1, 5)   → 'Hello'
SUBSTR('Hello World', 7)      → 'World'
```

### **TRIM(string)**
Removes leading and trailing spaces
```sql
TRIM('  Hello  ')  → 'Hello'
```

### **UPPER(string) / LOWER(string)**
Converts case
```sql
UPPER('hello')  → 'HELLO'
LOWER('HELLO')  → 'hello'
```

### **LENGTH(string)**
Returns string length
```sql
LENGTH('Hello')  → 5
```

### **REPLACE(string, old, new)**
Replaces text
```sql
REPLACE('Hello World', 'World', 'SQL')  → 'Hello SQL'
```

---

## 🟢 EASY EXERCISES - Basic String Functions

### **Exercise 1: Extract Email Domain**
**Problem:** Extract the domain from email addresses (everything after @)

**Sample Data:**
| email |
|-------|
| john.smith@gmail.com |
| maria.garcia@yahoo.com |

**Expected Output:**
| email | domain |
|-------|--------|
| john.smith@gmail.com | gmail.com |
| maria.garcia@yahoo.com | yahoo.com |

<details>
<summary>💡 Hint</summary>

1. Find position of '@' using `INSTR(email, '@')`
2. Extract everything after '@' using `SUBSTR(email, position + 1)`
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    email,
    SUBSTR(email, INSTR(email, '@') + 1) AS domain
FROM emails;
```
</details>

---

### **Exercise 2: Extract Email Username**
**Problem:** Extract the username from email addresses (everything before @)

**Expected Output:**
| email | username |
|-------|----------|
| john.smith@gmail.com | john.smith |
| jbrown@gmail.com | jbrown |

<details>
<summary>💡 Hint</summary>

Use `SUBSTR(email, 1, INSTR(email, '@') - 1)`
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    email,
    SUBSTR(email, 1, INSTR(email, '@') - 1) AS username
FROM emails;
```
</details>

---

### **Exercise 3: Get First Name from Full Name**
**Problem:** Extract first name from `full_name` (everything before the first space)

**Sample Data:**
| full_name |
|-----------|
| John Smith |
| Maria Garcia |

**Expected Output:**
| full_name | first_name |
|-----------|------------|
| John Smith | John |
| Maria Garcia | Maria |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    full_name,
    SUBSTR(full_name, 1, INSTR(full_name, ' ') - 1) AS first_name
FROM emails;
```
</details>

---

### **Exercise 4: Get Last Name from Full Name**
**Problem:** Extract last name from `full_name` (everything after the first space)

**Expected Output:**
| full_name | last_name |
|-----------|-----------|
| John Smith | Smith |
| Maria Garcia | Garcia |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    full_name,
    TRIM(SUBSTR(full_name, INSTR(full_name, ' ') + 1)) AS last_name
FROM emails;
```
</details>

---

## 🟡 MEDIUM EXERCISES - String Splitting

### **Exercise 5: Split Phone Names (The Main Challenge!)**
**Problem:** Split `phone_name` into brand and model. Delimiters can be: `-`, `:`, `*`, or `~`

**Sample Data:**
| phone_name |
|------------|
| Apple - iPhone 14 Pro |
| Samsung : Galaxy S23 |
| Google * Pixel 7 |

**Expected Output:**
| phone_name | brand | model |
|------------|-------|-------|
| Apple - iPhone 14 Pro | Apple | iPhone 14 Pro |
| Samsung : Galaxy S23 | Samsung | Galaxy S23 |
| Google * Pixel 7 | Google | Pixel 7 |

<details>
<summary>💡 Hint</summary>

1. Use `GREATEST()` to find which delimiter exists
2. Extract brand: `SUBSTR(phone_name, 1, position - 1)`
3. Extract model: `SUBSTR(phone_name, position + 1)`
4. Don't forget `TRIM()` to remove spaces!
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    phone_name,
    TRIM(SUBSTR(phone_name, 1, 
        GREATEST(
            INSTR(phone_name, '-'),
            INSTR(phone_name, ':'),
            INSTR(phone_name, '*'),
            INSTR(phone_name, '~')
        ) - 1
    )) AS brand,
    TRIM(SUBSTR(phone_name, 
        GREATEST(
            INSTR(phone_name, '-'),
            INSTR(phone_name, ':'),
            INSTR(phone_name, '*'),
            INSTR(phone_name, '~')
        ) + 1
    )) AS model
FROM phones;
```
</details>

---

### **Exercise 6: Extract Product Category from Code**
**Problem:** Extract the category from `product_code` (first part before first `-`)

**Sample Data:**
| product_code |
|--------------|
| ELEC-LAP-001 |
| FURN-CHA-023 |

**Expected Output:**
| product_code | category |
|--------------|----------|
| ELEC-LAP-001 | ELEC |
| FURN-CHA-023 | FURN |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    product_code,
    SUBSTR(product_code, 1, INSTR(product_code, '-') - 1) AS category
FROM product_codes;
```
</details>

---

### **Exercise 7: Extract Product Type from Code**
**Problem:** Extract the product type (middle part between first and second `-`)

**Sample Data:**
| product_code |
|--------------|
| ELEC-LAP-001 |
| FURN-CHA-023 |

**Expected Output:**
| product_code | product_type |
|--------------|--------------|
| ELEC-LAP-001 | LAP |
| FURN-CHA-023 | CHA |

<details>
<summary>💡 Hint</summary>

1. Find first `-` position
2. Find second `-` position (search starting after first `-`)
3. Extract text between them
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    product_code,
    SUBSTR(
        product_code,
        INSTR(product_code, '-') + 1,
        INSTR(SUBSTR(product_code, INSTR(product_code, '-') + 1), '-') - 1
    ) AS product_type
FROM product_codes;
```
</details>

---

### **Exercise 8: Extract City from Address**
**Problem:** Extract the city (second part) from `full_address`

**Sample Data:**
| full_address |
|--------------|
| 123 Main St, New York, NY, 10001 |
| 456 Oak Ave, Los Angeles, CA, 90001 |

**Expected Output:**
| full_address | city |
|--------------|------|
| 123 Main St, New York, NY, 10001 | New York |
| 456 Oak Ave, Los Angeles, CA, 90001 | Los Angeles |

<details>
<summary>💡 Hint</summary>

1. Find first comma position
2. Find second comma position
3. Extract text between them
4. TRIM to remove spaces
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    full_address,
    TRIM(SUBSTR(
        full_address,
        INSTR(full_address, ',') + 1,
        INSTR(SUBSTR(full_address, INSTR(full_address, ',') + 1), ',') - 1
    )) AS city
FROM addresses;
```
</details>

---

## 🔴 HARD EXERCISES - Complex String Manipulation

### **Exercise 9: Categorize Email Providers**
**Problem:** Create a category for email providers:
- 'Google' for gmail.com
- 'Microsoft' for outlook.com or hotmail.com
- 'Yahoo' for yahoo.com
- 'Corporate' for company.com
- 'Other' for everything else

**Expected Output:**
| email | provider_category |
|-------|-------------------|
| john.smith@gmail.com | Google |
| anna.k@outlook.com | Microsoft |
| chen.wei@company.com | Corporate |

<details>
<summary>💡 Hint</summary>

Combine string extraction with CASE statement!
1. Extract domain using SUBSTR and INSTR
2. Use CASE to categorize the domain
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    email,
    CASE 
        WHEN SUBSTR(email, INSTR(email, '@') + 1) = 'gmail.com' THEN 'Google'
        WHEN SUBSTR(email, INSTR(email, '@') + 1) IN ('outlook.com', 'hotmail.com') THEN 'Microsoft'
        WHEN SUBSTR(email, INSTR(email, '@') + 1) = 'yahoo.com' THEN 'Yahoo'
        WHEN SUBSTR(email, INSTR(email, '@') + 1) = 'company.com' THEN 'Corporate'
        ELSE 'Other'
    END AS provider_category
FROM emails;
```
</details>

---

### **Exercise 10: Count Users Per Email Provider**
**Problem:** Count how many users use each email provider category (combine Exercise 9 with GROUP BY)

**Expected Output:**
| provider_category | user_count |
|-------------------|------------|
| Google | 3 |
| Microsoft | 2 |
| Corporate | 2 |
| Yahoo | 1 |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    CASE 
        WHEN SUBSTR(email, INSTR(email, '@') + 1) = 'gmail.com' THEN 'Google'
        WHEN SUBSTR(email, INSTR(email, '@') + 1) IN ('outlook.com', 'hotmail.com') THEN 'Microsoft'
        WHEN SUBSTR(email, INSTR(email, '@') + 1) = 'yahoo.com' THEN 'Yahoo'
        WHEN SUBSTR(email, INSTR(email, '@') + 1) = 'company.com' THEN 'Corporate'
        ELSE 'Other'
    END AS provider_category,
    COUNT(*) AS user_count
FROM emails
GROUP BY provider_category
ORDER BY user_count DESC;
```
</details>

---

### **Exercise 11: Average Price by Phone Brand**
**Problem:** Calculate average price per phone brand (extract brand from phone_name, then aggregate)

**Expected Output:**
| brand | avg_price |
|-------|-----------|
| Apple | 999.00 |
| Samsung | 899.00 |
| Google | 599.00 |

<details>
<summary>💡 Hint</summary>

Combine string splitting with aggregation!
1. Extract brand using SUBSTR, GREATEST, INSTR
2. Use GROUP BY brand
3. Calculate AVG(price)
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    TRIM(SUBSTR(phone_name, 1, 
        GREATEST(
            INSTR(phone_name, '-'),
            INSTR(phone_name, ':'),
            INSTR(phone_name, '*'),
            INSTR(phone_name, '~')
        ) - 1
    )) AS brand,
    ROUND(AVG(price), 2) AS avg_price
FROM phones
GROUP BY brand
ORDER BY avg_price DESC;
```
</details>

---

### **Exercise 12: Product Inventory by Category**
**Problem:** Calculate total stock per product category (extract category from product_code)

**Expected Output:**
| category | total_stock |
|----------|-------------|
| ELEC | 471 |
| FURN | 154 |
| APPL | 167 |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    SUBSTR(product_code, 1, INSTR(product_code, '-') - 1) AS category,
    SUM(stock) AS total_stock
FROM product_codes
GROUP BY category
ORDER BY total_stock DESC;
```
</details>

---

## 🎯 Challenge Exercise - The Full Phone Problem

### **Exercise 13: Phone Analysis Report**
**Problem:** Create a comprehensive report showing:
- Brand
- Model
- Price
- Price category ('Premium' > $700, 'Mid-range' $400-$700, 'Budget' < $400)
- Average price for that brand

**Expected Output:**
| brand | model | price | price_category | brand_avg_price |
|-------|-------|-------|----------------|-----------------|
| Apple | iPhone 14 Pro | 999.00 | Premium | 999.00 |
| Samsung | Galaxy S23 | 899.00 | Premium | 899.00 |
| Google | Pixel 7 | 599.00 | Mid-range | 599.00 |

<details>
<summary>💡 Hint</summary>

This combines:
1. String splitting (brand/model extraction)
2. CASE statement (price categorization)
3. Window function or subquery (brand average)
</details>

<details>
<summary>✅ Solution</summary>

```sql
WITH phone_details AS (
    SELECT 
        phone_id,
        phone_name,
        price,
        TRIM(SUBSTR(phone_name, 1, 
            GREATEST(
                INSTR(phone_name, '-'),
                INSTR(phone_name, ':'),
                INSTR(phone_name, '*'),
                INSTR(phone_name, '~')
            ) - 1
        )) AS brand,
        TRIM(SUBSTR(phone_name, 
            GREATEST(
                INSTR(phone_name, '-'),
                INSTR(phone_name, ':'),
                INSTR(phone_name, '*'),
                INSTR(phone_name, '~')
            ) + 1
        )) AS model
    FROM phones
)
SELECT 
    brand,
    model,
    price,
    CASE 
        WHEN price > 700 THEN 'Premium'
        WHEN price >= 400 THEN 'Mid-range'
        ELSE 'Budget'
    END AS price_category,
    ROUND((SELECT AVG(price) FROM phone_details pd2 WHERE pd2.brand = pd.brand), 2) AS brand_avg_price
FROM phone_details pd
ORDER BY price DESC;
```
</details>

---

## 💡 Practice Tips

1. **Start Simple**: Begin with Exercise 1 and work your way up
2. **Test Each Part**: Break complex queries into steps
3. **Use SELECT to Debug**: Test `INSTR()` and `SUBSTR()` separately first
4. **Draw It Out**: Visualize string positions on paper
5. **Check Edge Cases**: What if there's no delimiter? No space?

---

## 🔧 Common Patterns

### **Pattern 1: Extract Before Delimiter**
```sql
SUBSTR(string, 1, INSTR(string, delimiter) - 1)
```

### **Pattern 2: Extract After Delimiter**
```sql
SUBSTR(string, INSTR(string, delimiter) + 1)
```

### **Pattern 3: Find Multiple Delimiters**
```sql
GREATEST(
    INSTR(string, 'delim1'),
    INSTR(string, 'delim2'),
    INSTR(string, 'delim3')
)
```

### **Pattern 4: Extract Middle Part**
```sql
SUBSTR(
    string,
    first_delimiter_pos + 1,
    second_delimiter_pos - first_delimiter_pos - 1
)
```

---

## ✅ Completion Checklist

Track your progress:

- [ ] Exercise 1: Extract Email Domain
- [ ] Exercise 2: Extract Email Username
- [ ] Exercise 3: Get First Name
- [ ] Exercise 4: Get Last Name
- [ ] Exercise 5: Split Phone Names ⭐ (Main Challenge)
- [ ] Exercise 6: Extract Product Category
- [ ] Exercise 7: Extract Product Type
- [ ] Exercise 8: Extract City
- [ ] Exercise 9: Categorize Email Providers
- [ ] Exercise 10: Count Users Per Provider
- [ ] Exercise 11: Average Price by Brand
- [ ] Exercise 12: Product Inventory by Category
- [ ] Exercise 13: Phone Analysis Report 🏆 (Final Challenge)

---

## 🚀 Next Steps

Once you've completed these exercises:
1. ✅ Try creating your own string manipulation queries
2. ✅ Combine string functions with JOINs
3. ✅ Practice with real-world messy data
4. ✅ Learn REGEXP (regular expressions) for advanced patterns

Happy practicing! 🎓
