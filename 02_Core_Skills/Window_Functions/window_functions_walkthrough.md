# 🎬 Window Functions: YouTuber Example Walkthrough

**Follow the data transformation step-by-step!**

---

## 📊 Starting Data

| category  | youtuber  | video_views |
|---------- |---------- |-------------|
| Gaming    | Alice     | 50000       |
| Gaming    | Bob       | 30000       |
| Gaming    | Charlie   | 20000       |
| Gaming    | Dave      | 10000       |
| Music     | Eve       | 40000       |
| Music     | Frank     | 25000       |
| Music     | Grace     | 15000       |
| Music     | Henry     | 5000        |

---

## 🎯 The Goal

**Find the top 3 YouTubers in EACH category.**

---

## 🔨 Step 1: Add the RANK Column

**Query:**
```sql
SELECT 
    category,
    youtuber,
    video_views,
    RANK() OVER (PARTITION BY category ORDER BY video_views DESC) AS rnk
FROM youtubers;
```

**What PARTITION BY does:**

### **Gaming Window:**
| youtuber  | video_views | rnk   |
|---------- |-------------|-----  |
| Alice     | 50000       | **1** |
| Bob       | 30000       | **2** |
| Charlie   | 20000       | **3** |
| Dave      | 10000       | **4** |

### **Music Window:**
| youtuber  | video_views | rnk   |
|---------- |-------------|-----  |
| Eve       | 40000       | **1** |
| Frank     | 25000       | **2** |
| Grace     | 15000       | **3** |
| Henry     | 5000        | **4** |

**Combined Result:**

| category  | youtuber  | video_views | rnk   |
|---------- |---------- |-------------|-----  |
| Gaming    | Alice     | 50000       | **1** |
| Gaming    | Bob       | 30000       | **2** |
| Gaming    | Charlie   | 20000       | **3** |
| Gaming    | Dave      | 10000       | **4** |
| Music     | Eve       | 40000       | **1** |
| Music     | Frank     | 25000       | **2** |
| Music     | Grace     | 15000       | **3** |
| Music     | Henry     | 5000        | **4** |

---

## 🔍 Step 2: Filter to Top 3

**Query:**
```sql
SELECT *
FROM (
    SELECT 
        category,
        youtuber,
        video_views,
        RANK() OVER (PARTITION BY category ORDER BY video_views DESC) AS rnk
    FROM youtubers
) a
WHERE a.rnk <= 3;
```

**Filter Applied:**

| category  | youtuber  | video_views | rnk   | Keep? |
|---------- |---------- |-------------|-----  |-------|
| Gaming    | Alice     | 50000       | **1** | ✅ |
| Gaming    | Bob       | 30000       | **2** | ✅ |
| Gaming    | Charlie   | 20000       | **3** | ✅ |
| Gaming    | Dave      | 10000       | **4** | ❌ |
| Music     | Eve       | 40000       | **1** | ✅ |
| Music     | Frank     | 25000       | **2** | ✅ |
| Music     | Grace     | 15000       | **3** | ✅ |
| Music     | Henry     | 5000        | **4** | ❌ |

**Final Result:**

| category  | youtuber  | video_views | rnk   |
|---------- |---------- |-------------|-----  |
| Gaming    | Alice     | 50000       | **1** |
| Gaming    | Bob       | 30000       | **2** |
| Gaming    | Charlie   | 20000       | **3** |
| Music     | Eve       | 40000       | **1** |
| Music     | Frank     | 25000       | **2** |
| Music     | Grace     | 15000       | **3** |

---

## 🎓 Comparing the 3 Ranking Functions

**Scenario:** Bob and Charlie both have 30,000 views.

| youtuber  | views     | ROW_NUMBER | RANK | DENSE_RANK |
|---------- |-----------|------------|------|------------|
| Alice     | 50000     | 1          | 1    | 1          |
| Bob       | 30000     | 2          | 2    | 2          |
| Charlie   | 30000     | **3**      | **2** | **2**      |
| Dave      | 20000     | 4          | **4** | **3**      |

**Notice:**
- **ROW_NUMBER**: Bob gets 2, Charlie gets 3 (unique numbers)
- **RANK**: Bob and Charlie both get 2, Dave gets 4 (skips 3)
- **DENSE_RANK**: Bob and Charlie both get 2, Dave gets 3 (no skip)

---

## 💡 Why Use a Subquery?

**This doesn't work:**
```sql
SELECT *
FROM youtubers
WHERE RANK() OVER (...) <= 3;  -- ERROR!
```

**Why?** Window functions are calculated AFTER the WHERE clause runs.

**Solution:** Calculate the rank first (in a subquery), then filter.
