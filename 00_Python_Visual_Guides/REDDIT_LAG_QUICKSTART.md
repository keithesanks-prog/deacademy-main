# 🎯 Reddit LAG Practice - Quick Start

## ✅ What Was Created

### **Database: `reddit_practice_db`**
- 20 publishers with various posting patterns
- ~50+ posts with strategic timing
- Some publishers qualify, some don't

### **Tables:**
- `dim_publishers_reddit` - Publisher info (id, name, city)
- `fact_reddit` - Posts (post_id, publisher_id, creation_date, score, etc.)

---

## 🚀 How to Practice

### **Run the Practice Script:**
```bash
python run_reddit_queries.py
```

This shows:
1. **Posting patterns** for each publisher
2. **Gap analysis** - who qualifies and who doesn't
3. **THE FINAL ANSWER** - count of qualifying publishers
4. **Detailed timeline** for one qualifying publisher

---

## 📝 The Query to Master

```sql
WITH posts_with_gaps AS (
    SELECT
        publisher_id,
        creation_date,
        DATEDIFF(
            creation_date, 
            LAG(creation_date) OVER (PARTITION BY publisher_id ORDER BY creation_date)
        ) AS days_between_posts
    FROM fact_reddit
),
publisher_gap_check AS (
    SELECT
        publisher_id,
        COUNT(*) AS total_posts,
        COUNT(CASE WHEN days_between_posts >= 7 THEN 1 END) AS gaps_of_7plus_days
    FROM posts_with_gaps
    GROUP BY publisher_id
)
SELECT
    COUNT(*) AS number_of_publishers
FROM publisher_gap_check
WHERE total_posts >= 3
  AND gaps_of_7plus_days >= 2;
```

---

## 🔑 Key Concepts

1. **LAG() with PARTITION BY** - Look at previous post per publisher
2. **DATEDIFF()** - Calculate days between dates
3. **COUNT(CASE WHEN ...)** - Conditional counting
4. **n posts = n-1 gaps** - Why we need >= 2 gaps for 3 posts

---

## 🎓 Practice Exercises

### **Exercise 1: Show Qualifying Publishers**
```sql
-- Instead of just counting, show WHO qualifies
SELECT
    p.name,
    pgc.total_posts,
    pgc.gaps_of_7plus_days
FROM publisher_gap_check pgc
JOIN dim_publishers_reddit p ON pgc.publisher_id = p.publisher_id
WHERE total_posts >= 3 AND gaps_of_7plus_days >= 2;
```

### **Exercise 2: Change the Threshold**
```sql
-- Find publishers with 14+ day gaps instead of 7+
COUNT(CASE WHEN days_between_posts >= 14 THEN 1 END)
```

### **Exercise 3: Require ALL Gaps to Qualify**
```sql
-- All gaps must be 7+ days
WHERE total_posts >= 3
  AND gaps_of_7plus_days = total_posts - 1  -- ALL gaps qualify
```

---

## 📚 Resources

- **Full Tutorial**: `lag_window_functions_reddit.md`
- **SQL Mastery Guide**: `sql_mastery_guide.html` (Window Functions tab)
- **Database**: `reddit_practice_db`
- **Practice Script**: `run_reddit_queries.py`

---

Happy practicing! 🚀
