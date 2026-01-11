# 🎓 String Splitting - Complete Visual Guide

## 🎯 The Goal

We want to turn this:
```
'Apple - iPhone 14 Pro'
```

Into this:
```
Brand: 'Apple'
Model: 'iPhone 14 Pro'
```

---

## 📐 Step 1: Understanding String Positions

Strings in SQL are **1-indexed** (counting starts at 1, not 0).

```
'Apple - iPhone 14 Pro'
 ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
 123456789...
```

Let me show you each character with its position:

| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 |
|----------|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|----|----|----|----|----|----|----|
| Character| A | p | p | l | e | (space) | - | (space) | i | P | h | o | n | e | (space) | 1 | 4 | (space) | P | r | o |

**Key positions:**
- Position 1-5: `'Apple'`
- Position 6: `' '` (space)
- Position 7: `'-'` (the delimiter!)
- Position 8: `' '` (space)
- Position 9-22: `'iPhone 14 Pro'`

---

## 🔍 Step 2: Finding the Delimiter with INSTR()

`INSTR(string, substring)` finds the **position** of a substring.

```sql
INSTR('Apple - iPhone 14 Pro', '-')
```

**What SQL does:**
1. Looks through the string character by character
2. Finds `-` at position **7**
3. Returns **7**

**Visual:**
```
'Apple - iPhone 14 Pro'
       ↑
    Position 7
```

---

## ✂️ Step 3: Extracting the Brand with SUBSTR()

`SUBSTR(string, start, length)` extracts part of a string.

### **Formula for Brand:**
```sql
SUBSTR('Apple - iPhone 14 Pro', 1, 6)
       ↑                        ↑  ↑
       string                start length
```

**What this means:**
- Start at position **1**
- Take **6** characters

**Calculation:**
- Length = delimiter_position - 1
- Length = 7 - 1 = **6**

**Visual:**
```
'Apple - iPhone 14 Pro'
 ↓↓↓↓↓↓
 123456  ← We take these 6 characters
```

**Result:** `'Apple '` (note the trailing space!)

---

## 🧹 Step 4: Cleaning with TRIM()

`TRIM(string)` removes spaces from both ends.

```sql
TRIM('Apple ')
```

**What TRIM does:**
```
Before: 'Apple '
         ↑    ↑
       start  space here!

After:  'Apple'
         ↑   ↑
       start end (no space!)
```

**Result:** `'Apple'` ✅

---

## 🎯 Putting It All Together - Brand Extraction

```sql
TRIM(SUBSTR('Apple - iPhone 14 Pro', 1, INSTR('Apple - iPhone 14 Pro', '-') - 1))
```

**Let's break this down from inside out:**

### **Level 1 (Innermost): Find delimiter**
```sql
INSTR('Apple - iPhone 14 Pro', '-')
→ 7
```

### **Level 2: Calculate length**
```sql
7 - 1
→ 6
```

### **Level 3: Extract substring**
```sql
SUBSTR('Apple - iPhone 14 Pro', 1, 6)
→ 'Apple '
```

### **Level 4 (Outermost): Remove spaces**
```sql
TRIM('Apple ')
→ 'Apple'
```

**Final Result:** `'Apple'` ✅

---

## 📱 Now Let's Extract the Model

### **Formula for Model:**
```sql
SUBSTR('Apple - iPhone 14 Pro', 8)
       ↑                        ↑
       string                start (no length = go to end)
```

**What this means:**
- Start at position **8** (right after the delimiter and space)
- Take everything to the end

**Calculation:**
- Start = delimiter_position + 1
- Start = 7 + 1 = **8**

**Visual:**
```
'Apple - iPhone 14 Pro'
        ↑↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        8 9 10 11...22  ← We take from position 8 to the end
```

**Result:** `' iPhone 14 Pro'` (note the leading space!)

---

## 🧹 Clean the Model with TRIM()

```sql
TRIM(' iPhone 14 Pro')
→ 'iPhone 14 Pro'
```

---

## 🎯 Complete Query - Step by Step

```sql
SELECT 
    phone_name,
    
    -- BRAND EXTRACTION
    TRIM(                                      -- 4. Remove spaces
        SUBSTR(                                -- 3. Extract substring
            phone_name,                        -- From this column
            1,                                 -- Start at position 1
            INSTR(phone_name, '-') - 1         -- Length = position of '-' minus 1
        )
    ) AS brand,
    
    -- MODEL EXTRACTION
    TRIM(                                      -- 4. Remove spaces
        SUBSTR(                                -- 3. Extract substring
            phone_name,                        -- From this column
            INSTR(phone_name, '-') + 1         -- Start after the '-'
        )
    ) AS model
    
FROM phones;
```

---

## 🔢 Real Example with Numbers

**Input:** `'Apple - iPhone 14 Pro'`

### **Brand Extraction:**

**Step 1:** Find delimiter
```sql
INSTR('Apple - iPhone 14 Pro', '-') = 7
```

**Step 2:** Calculate where to stop
```sql
7 - 1 = 6
```

**Step 3:** Extract characters 1 through 6
```sql
SUBSTR('Apple - iPhone 14 Pro', 1, 6) = 'Apple '
```

**Step 4:** Remove spaces
```sql
TRIM('Apple ') = 'Apple'
```

### **Model Extraction:**

**Step 1:** Find delimiter
```sql
INSTR('Apple - iPhone 14 Pro', '-') = 7
```

**Step 2:** Calculate where to start
```sql
7 + 1 = 8
```

**Step 3:** Extract from position 8 to end
```sql
SUBSTR('Apple - iPhone 14 Pro', 8) = ' iPhone 14 Pro'
```

**Step 4:** Remove spaces
```sql
TRIM(' iPhone 14 Pro') = 'iPhone 14 Pro'
```

---

## 🎨 Visual Summary

```
Original String:
'Apple - iPhone 14 Pro'
 ↓↓↓↓↓ ↓ ↓↓↓↓↓↓↓↓↓↓↓↓↓↓
 Brand - Model
 
Position 1-5:  Brand characters
Position 6:    Space (we don't want this)
Position 7:    Delimiter '-'
Position 8:    Space (we don't want this)
Position 9-22: Model characters

SUBSTR for Brand:
'Apple - iPhone 14 Pro'
 ↓↓↓↓↓↓ ← Take positions 1-6
 'Apple '
 
TRIM for Brand:
'Apple ' → 'Apple'

SUBSTR for Model:
'Apple - iPhone 14 Pro'
        ↓↓↓↓↓↓↓↓↓↓↓↓↓↓ ← Take from position 8 to end
        ' iPhone 14 Pro'

TRIM for Model:
' iPhone 14 Pro' → 'iPhone 14 Pro'
```

---

## 🧪 Practice Exercise

Try to predict the output for each step:

**Input:** `'Samsung : Galaxy S23'`

**Question 1:** What does `INSTR('Samsung : Galaxy S23', ':')` return?
<details>
<summary>Answer</summary>
9 (the colon is at position 9)
</details>

**Question 2:** What does `SUBSTR('Samsung : Galaxy S23', 1, 8)` return?
<details>
<summary>Answer</summary>
'Samsung ' (positions 1-8, includes trailing space)
</details>

**Question 3:** What does `TRIM('Samsung ')` return?
<details>
<summary>Answer</summary>
'Samsung' (space removed)
</details>

**Question 4:** What does `SUBSTR('Samsung : Galaxy S23', 10)` return?
<details>
<summary>Answer</summary>
' Galaxy S23' (from position 10 to end, includes leading space)
</details>

**Question 5:** What does `TRIM(' Galaxy S23')` return?
<details>
<summary>Answer</summary>
'Galaxy S23' (space removed)
</details>

---

## 💡 Key Takeaways

1. **INSTR()** finds the **position** of a character (returns a number)
2. **SUBSTR()** extracts **part of a string** using positions
3. **TRIM()** removes **spaces** from both ends
4. **Functions nest** from inside out: TRIM wraps SUBSTR
5. **Brand formula:** `TRIM(SUBSTR(string, 1, delimiter_pos - 1))`
6. **Model formula:** `TRIM(SUBSTR(string, delimiter_pos + 1))`

---

## 🚀 Next Step

Now try this query yourself:

```sql
SELECT 
    phone_name,
    TRIM(SUBSTR(phone_name, 1, INSTR(phone_name, '-') - 1)) AS brand,
    TRIM(SUBSTR(phone_name, INSTR(phone_name, '-') + 1)) AS model
FROM phones
WHERE phone_name = 'Apple - iPhone 14 Pro';
```

Does this help? Try running it and see the magic happen! ✨
