# 🎓 SQL Date/Time Functions Practice Exercises

## 🚀 Getting Started

### **Step 1: Set Up Your Database**
1. Open your SQL environment (MySQL Workbench, online SQL tool, etc.)
2. Run the `sql_datetime_practice_setup.sql` file to create tables with sample data
3. Verify tables were created by running: `SELECT * FROM video_views;`

---

## 📚 Date/Time Functions Reference

### **TIMESTAMPDIFF(unit, start, end)**
Calculates the difference between two datetime values.

**Units:**
- `SECOND` - difference in seconds
- `MINUTE` - difference in minutes  
- `HOUR` - difference in hours
- `DAY` - difference in days
- `MONTH` - difference in months
- `YEAR` - difference in years

**Example:**
```sql
TIMESTAMPDIFF(MINUTE, '2021-01-01 10:00:00', '2021-01-01 11:30:00')  → 90
```

### **YEAR(date), MONTH(date), DAY(date)**
Extract parts of a date.

```sql
YEAR('2021-03-15')   → 2021
MONTH('2021-03-15')  → 3
DAY('2021-03-15')    → 15
```

### **NOW(), CURDATE(), CURTIME()**
Get current date/time.

```sql
NOW()      → '2025-11-27 15:20:30'
CURDATE()  → '2025-11-27'
CURTIME()  → '15:20:30'
```

---

## 🟢 EASY EXERCISES - Basic Time Calculations

### **Exercise 1: Calculate Watch Time in Minutes**
**Problem:** Calculate how many minutes each person watched their video.

**Sample Data:**
| user_name | video_title | start_time | end_time |
|-----------|-------------|------------|----------|
| Alice | SQL Tutorial Part 1 | 2021-01-15 14:30:00 | 2021-01-15 15:45:00 |

**Expected Output:**
| user_name | video_title | watch_minutes |
|-----------|-------------|---------------|
| Alice | SQL Tutorial Part 1 | 75 |
| Bob | Python Basics | 150 |

<details>
<summary>💡 Hint</summary>

Use `TIMESTAMPDIFF(MINUTE, start_time, end_time)`
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    user_name,
    video_title,
    TIMESTAMPDIFF(MINUTE, start_time, end_time) AS watch_minutes
FROM video_views;
```
</details>

---

### **Exercise 2: Calculate Watch Time in Hours**
**Problem:** Calculate watch time in hours (with decimals).

**Expected Output:**
| user_name | video_title | watch_hours |
|-----------|-------------|-------------|
| Alice | SQL Tutorial Part 1 | 1.25 |
| Bob | Python Basics | 2.50 |

<details>
<summary>💡 Hint</summary>

Divide minutes by 60.0 to get hours with decimals
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    user_name,
    video_title,
    ROUND(TIMESTAMPDIFF(MINUTE, start_time, end_time) / 60.0, 2) AS watch_hours
FROM video_views;
```
</details>

---

### **Exercise 3: Calculate Subscription Duration in Days**
**Problem:** Calculate how many days each subscription lasted.

**Expected Output:**
| user_name | plan_type | duration_days |
|-----------|-----------|---------------|
| Alice Johnson | Premium | 364 |
| Bob Williams | Basic | 184 |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    user_name,
    plan_type,
    TIMESTAMPDIFF(DAY, start_date, end_date) AS duration_days
FROM subscriptions;
```
</details>

---

### **Exercise 4: Calculate Subscription Duration in Months**
**Problem:** Calculate subscription duration in months.

**Expected Output:**
| user_name | plan_type | duration_months |
|-----------|-----------|-----------------|
| Alice Johnson | Premium | 12 |
| Bob Williams | Basic | 6 |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    user_name,
    plan_type,
    TIMESTAMPDIFF(MONTH, start_date, end_date) AS duration_months
FROM subscriptions;
```
</details>

---

## 🟡 MEDIUM EXERCISES - Aggregation with Time

### **Exercise 5: Total Watch Time Per User**
**Problem:** Calculate total minutes watched by each user across all videos.

**Expected Output:**
| user_name | total_watch_minutes |
|-----------|---------------------|
| Alice | 345 |
| Bob | 315 |
| Carol | 240 |

<details>
<summary>💡 Hint</summary>

Use `SUM(TIMESTAMPDIFF(...))` with `GROUP BY user_name`
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    user_name,
    SUM(TIMESTAMPDIFF(MINUTE, start_time, end_time)) AS total_watch_minutes
FROM video_views
GROUP BY user_name
ORDER BY total_watch_minutes DESC;
```
</details>

---

### **Exercise 6: Users Who Watched More Than 3 Hours**
**Problem:** Find users who watched more than 180 minutes (3 hours) total.

**Expected Output:**
| user_name | total_watch_minutes |
|-----------|---------------------|
| Alice | 345 |
| Bob | 315 |
| Carol | 240 |

<details>
<summary>💡 Hint</summary>

Use `HAVING` to filter after aggregation
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    user_name,
    SUM(TIMESTAMPDIFF(MINUTE, start_time, end_time)) AS total_watch_minutes
FROM video_views
GROUP BY user_name
HAVING SUM(TIMESTAMPDIFF(MINUTE, start_time, end_time)) > 180
ORDER BY total_watch_minutes DESC;
```
</details>

---

### **Exercise 7: Average Shipping Time**
**Problem:** Calculate average time (in hours) from order to shipment.

**Expected Output:**
| avg_shipping_hours |
|--------------------|
| 25.5 |

<details>
<summary>💡 Hint</summary>

Use `AVG(TIMESTAMPDIFF(HOUR, order_date, shipped_date))`
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    ROUND(AVG(TIMESTAMPDIFF(HOUR, order_date, shipped_date)), 1) AS avg_shipping_hours
FROM orders;
```
</details>

---

### **Exercise 8: Average Delivery Time**
**Problem:** Calculate average time (in days) from shipment to delivery.

**Expected Output:**
| avg_delivery_days |
|-------------------|
| 4.2 |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    ROUND(AVG(TIMESTAMPDIFF(DAY, shipped_date, delivered_date)), 1) AS avg_delivery_days
FROM orders;
```
</details>

---

## 🔴 HARD EXERCISES - Complex Time Calculations

### **Exercise 9: Filter by Year**
**Problem:** Find all video views that happened in 2021.

**Expected Output:**
| user_name | video_title | start_time |
|-----------|-------------|------------|
| Alice | SQL Tutorial Part 1 | 2021-01-15 14:30:00 |
| Bob | Python Basics | 2021-02-20 09:00:00 |

<details>
<summary>💡 Hint</summary>

Use `YEAR(start_time) = 2021`
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    user_name,
    video_title,
    start_time
FROM video_views
WHERE YEAR(start_time) = 2021;
```
</details>

---

### **Exercise 10: Total Watch Time Per User in 2021**
**Problem:** Calculate total watch minutes per user, but only for views in 2021.

**Expected Output:**
| user_name | total_minutes_2021 |
|-----------|--------------------|
| Alice | 345 |
| Bob | 315 |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    user_name,
    SUM(TIMESTAMPDIFF(MINUTE, start_time, end_time)) AS total_minutes_2021
FROM video_views
WHERE YEAR(start_time) = 2021
GROUP BY user_name
ORDER BY total_minutes_2021 DESC;
```
</details>

---

### **Exercise 11: Users Who Watched > 5 Hours in 2021**
**Problem:** Find users who watched more than 300 minutes (5 hours) in 2021.

**Expected Output:**
| user_name | total_minutes |
|-----------|---------------|
| Alice | 345 |
| Bob | 315 |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    user_name,
    SUM(TIMESTAMPDIFF(MINUTE, start_time, end_time)) AS total_minutes
FROM video_views
WHERE YEAR(start_time) = 2021
GROUP BY user_name
HAVING SUM(TIMESTAMPDIFF(MINUTE, start_time, end_time)) > 300
ORDER BY total_minutes DESC;
```
</details>

---

### **Exercise 12: Days Since Event**
**Problem:** Calculate how many days ago each event happened (from today).

**Expected Output:**
| event_name | event_date | days_ago |
|------------|------------|----------|
| Tech Conference 2021 | 2021-03-15 | 1718 |
| Data Summit | 2021-06-20 | 1621 |

<details>
<summary>💡 Hint</summary>

Use `TIMESTAMPDIFF(DAY, event_date, CURDATE())`
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    event_name,
    event_date,
    TIMESTAMPDIFF(DAY, event_date, CURDATE()) AS days_ago
FROM events
ORDER BY days_ago;
```
</details>

---

### **Exercise 13: Subscription Revenue Calculation**
**Problem:** Calculate total revenue for each subscription (monthly_price × months active).

**Expected Output:**
| user_name | plan_type | months_active | total_revenue |
|-----------|-----------|---------------|---------------|
| Alice Johnson | Premium | 12 | 239.88 |
| Bob Williams | Basic | 6 | 59.94 |

<details>
<summary>💡 Hint</summary>

Multiply `TIMESTAMPDIFF(MONTH, ...)` by `monthly_price`
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    user_name,
    plan_type,
    TIMESTAMPDIFF(MONTH, start_date, end_date) AS months_active,
    ROUND(TIMESTAMPDIFF(MONTH, start_date, end_date) * monthly_price, 2) AS total_revenue
FROM subscriptions
ORDER BY total_revenue DESC;
```
</details>

---

## 🎯 Challenge Exercise - The Netflix Problem

### **Exercise 14: Top 5 Watchers with > 40 Hours**
**Problem:** Find top 5 users who watched more than 2400 minutes (40 hours) total. Show name and total minutes.

**Expected Output:**
| user_name | total_minutes |
|-----------|---------------|
| Alice | 345 |
| Bob | 315 |
| Carol | 240 |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    user_name,
    SUM(TIMESTAMPDIFF(MINUTE, start_time, end_time)) AS total_minutes
FROM video_views
GROUP BY user_name
HAVING SUM(TIMESTAMPDIFF(MINUTE, start_time, end_time)) > 2400
ORDER BY total_minutes DESC
LIMIT 5;
```

**Note:** With the sample data, no users exceed 2400 minutes. Adjust the threshold to see results!
</details>

---

## 💡 Common Patterns

### **Pattern 1: Calculate Duration**
```sql
TIMESTAMPDIFF(unit, start_datetime, end_datetime)
```

### **Pattern 2: Filter by Year**
```sql
WHERE YEAR(date_column) = 2021
```

### **Pattern 3: Sum Durations Per Group**
```sql
SELECT 
    group_column,
    SUM(TIMESTAMPDIFF(MINUTE, start, end)) AS total
FROM table
GROUP BY group_column;
```

### **Pattern 4: Filter Aggregated Time**
```sql
HAVING SUM(TIMESTAMPDIFF(MINUTE, start, end)) > threshold
```

---

## ✅ Completion Checklist

- [ ] Exercise 1: Calculate Watch Time in Minutes
- [ ] Exercise 2: Calculate Watch Time in Hours
- [ ] Exercise 3: Subscription Duration in Days
- [ ] Exercise 4: Subscription Duration in Months
- [ ] Exercise 5: Total Watch Time Per User
- [ ] Exercise 6: Users Who Watched > 3 Hours
- [ ] Exercise 7: Average Shipping Time
- [ ] Exercise 8: Average Delivery Time
- [ ] Exercise 9: Filter by Year
- [ ] Exercise 10: Total Watch Time in 2021
- [ ] Exercise 11: Users > 5 Hours in 2021
- [ ] Exercise 12: Days Since Event
- [ ] Exercise 13: Subscription Revenue
- [ ] Exercise 14: Top 5 Watchers 🏆

---

## 🚀 Next Steps

Once you've completed these exercises:
1. ✅ Practice with different time units (SECOND, HOUR, DAY, MONTH, YEAR)
2. ✅ Combine date functions with JOINs
3. ✅ Use date functions in CASE statements
4. ✅ Practice with real-world datasets

Happy practicing! 🎓
