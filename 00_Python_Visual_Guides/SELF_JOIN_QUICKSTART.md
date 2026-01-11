# 🎯 Self-Join Practice Setup - Quick Start Guide

## ✅ What Was Created

### 1. **Database: `zoom_practice_db`**
   - 20 meetings with strategic overlaps
   - 15 participants with various participation patterns
   - Realistic timestamps spanning 3 days

### 2. **Tables:**
   - `dim_meetings_zoom` - Meeting schedules
   - `fact_participations_zoom` - Who attended which meetings

### 3. **Practice Files:**
   - `self_join_mastery.md` - Complete tutorial
   - `create_zoom_database.py` - Database setup script
   - `run_zoom_queries.py` - Practice queries

---

## 🚀 How to Practice

### **Option 1: Run the Practice Script**
```bash
python run_zoom_queries.py
```

This will show you:
- All overlapping meeting pairs
- Participants in overlapping meetings
- **THE FINAL SOLUTION** - Participants meeting both criteria

### **Option 2: Use Jupyter Notebook**
```python
%%sql
USE zoom_practice_db;

-- Your queries here
```

### **Option 3: Use Python**
```python
import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine(
    "mysql+pymysql://python_user:password@127.0.0.1:3306/zoom_practice_db"
)

query = """
-- Your SQL query here
"""

df = pd.read_sql(query, engine)
print(df)
```

---

## 📝 Practice Exercises

### **Exercise 1: Find All Overlapping Meetings**
```sql
SELECT 
    m1.meeting_id AS meeting_1,
    m2.meeting_id AS meeting_2
FROM dim_meetings_zoom m1
JOIN dim_meetings_zoom m2
    ON m1.meeting_id < m2.meeting_id
    AND m1.start_timestamp < m2.end_timestamp
    AND m2.start_timestamp < m1.end_timestamp;
```

### **Exercise 2: Count Overlaps per Participant**
```sql
SELECT 
    p1.participant_id,
    COUNT(*) AS overlapped_meeting_count
FROM dim_meetings_zoom m1
JOIN dim_meetings_zoom m2
    ON m1.meeting_id < m2.meeting_id
    AND m1.start_timestamp < m2.end_timestamp
    AND m2.start_timestamp < m1.end_timestamp
JOIN fact_participations_zoom p1 ON m1.meeting_id = p1.meeting_id
JOIN fact_participations_zoom p2 ON m2.meeting_id = p2.meeting_id
    AND p1.participant_id = p2.participant_id
WHERE p1.status = 'Confirmed' 
  AND p2.status = 'Confirmed'
GROUP BY p1.participant_id;
```

### **Exercise 3: The Complete Solution**
See `self_join_mastery.md` for the full query!

---

## 🔍 Explore the Data

### View all meetings:
```sql
SELECT * FROM dim_meetings_zoom ORDER BY start_timestamp;
```

### View all participations:
```sql
SELECT * FROM fact_participations_zoom ORDER BY participant_id, meeting_id;
```

### See a specific participant's schedule:
```sql
SELECT 
    p.participant_id,
    m.meeting_id,
    m.start_timestamp,
    m.end_timestamp,
    p.status
FROM fact_participations_zoom p
JOIN dim_meetings_zoom m ON p.meeting_id = m.meeting_id
WHERE p.participant_id = 1
ORDER BY m.start_timestamp;
```

---

## 💡 Key Learning Points

1. **Self-Join Syntax**: `FROM table t1 JOIN table t2`
2. **Avoid Duplicates**: `t1.id < t2.id`
3. **Time Overlap**: `t1.start < t2.end AND t2.start < t1.end`
4. **Same Entity**: `p1.participant_id = p2.participant_id`

---

## 📚 Resources

- **Tutorial**: `self_join_mastery.md`
- **Database**: `zoom_practice_db`
- **Practice Script**: `run_zoom_queries.py`
- **Walmart Practice**: `walmart_sql_practice_guide.md`

---

## 🎓 Next Steps

1. Read `self_join_mastery.md` 
2. Run `python run_zoom_queries.py` to see the solution
3. Try modifying the queries
4. Experiment with different filters
5. Apply the concepts to the Walmart database!

Happy practicing! 🚀
