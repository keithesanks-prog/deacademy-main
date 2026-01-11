# 🎓 Self-Joins Mastery: The Overlapping Meetings Problem

## 📋 Problem Statement

**Find participants who:**
1. Were **confirmed** in overlapping meetings
2. Were also in at least **two non-overlapping** meetings
3. Return: `participant_id`, `overlapped_meeting_count`

---

## 📊 Understanding the Data

### Tables:
```sql
-- fact_participations_zoom
meeting_id | participant_id | status
41342      | 1177          | Not confirmed

-- dim_meetings_zoom
meeting_id | organizer_id | start_timestamp      | end_timestamp
32179      | 1316         | 2022-12-6 15:00:00  | 2022-12-6 16:00:00
```

---

## 🧠 Conceptual Breakdown

### What Does "Overlapping Meetings" Mean?

Two meetings overlap if:
- Meeting A starts **before** Meeting B ends
- Meeting B starts **before** Meeting A ends

**Visual Example:**

```
Meeting 1:  [========]
Meeting 2:      [========]
            ↑
         Overlap!

Meeting 1:  [====]
Meeting 2:          [====]
            No overlap
```

---

## 🔍 Step-by-Step Solution

### **Step 1: Understanding Self-Join for Time Overlap**

We need to join `dim_meetings_zoom` to **itself** to compare every meeting with every other meeting.

```sql
FROM dim_meetings_zoom m1
JOIN dim_meetings_zoom m2
    ON m1.meeting_id < m2.meeting_id  -- Avoid duplicates and self-matching
```

**Why `m1.meeting_id < m2.meeting_id`?**
- Prevents comparing a meeting to itself
- Prevents duplicate pairs (Meeting 1→2 and Meeting 2→1)

---

### **Step 2: Detecting Time Overlap**

Two meetings overlap when:

```sql
AND m1.start_timestamp < m2.end_timestamp    -- M1 starts before M2 ends
AND m2.start_timestamp < m1.end_timestamp    -- M2 starts before M1 ends
```

**Visual Proof:**

```
Case 1: Overlap
M1: [==========]
M2:      [==========]
    ↑              ↑
M1.start < M2.end  ✅
M2.start < M1.end  ✅

Case 2: No Overlap
M1: [====]
M2:         [====]
    ↑          ↑
M1.start < M2.end  ✅
M2.start < M1.end  ❌ (M2 starts AFTER M1 ends)
```

---

### **Step 3: Join with Participations**

Now we need to check if the **same participant** was in both overlapping meetings:

```sql
JOIN fact_participations_zoom p1 
    ON m1.meeting_id = p1.meeting_id
JOIN fact_participations_zoom p2 
    ON m2.meeting_id = p2.meeting_id
    AND p1.participant_id = p2.participant_id  -- Same person!
```

---

### **Step 4: Filter for Confirmed Status**

```sql
WHERE p1.status = 'Confirmed' 
  AND p2.status = 'Confirmed'
```

---

### **Step 5: Count Overlapping Meetings per Participant**

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
GROUP BY p1.participant_id
```

---

### **Step 6: Filter for Non-Overlapping Meetings**

We need participants who were ALSO in at least 2 non-overlapping meetings.

**Strategy**: Use a CTE to find non-overlapping meeting pairs for each participant.

```sql
WITH non_overlapping AS (
    SELECT 
        p1.participant_id,
        COUNT(DISTINCT m1.meeting_id) AS non_overlap_count
    FROM dim_meetings_zoom m1
    JOIN dim_meetings_zoom m2
        ON m1.meeting_id < m2.meeting_id
        AND (m1.end_timestamp <= m2.start_timestamp 
             OR m2.end_timestamp <= m1.start_timestamp)  -- No overlap!
    JOIN fact_participations_zoom p1 ON m1.meeting_id = p1.meeting_id
    JOIN fact_participations_zoom p2 ON m2.meeting_id = p2.meeting_id
        AND p1.participant_id = p2.participant_id
    WHERE p1.status = 'Confirmed' 
      AND p2.status = 'Confirmed'
    GROUP BY p1.participant_id
    HAVING COUNT(DISTINCT m1.meeting_id) >= 2
)
```

---

## 🎯 Complete Solution

```sql
-- CTE 1: Find participants with overlapping meetings
WITH overlapping_meetings AS (
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
    GROUP BY p1.participant_id
),
-- CTE 2: Find participants in at least 2 non-overlapping meetings
non_overlapping_participants AS (
    SELECT DISTINCT
        p1.participant_id
    FROM dim_meetings_zoom m1
    JOIN dim_meetings_zoom m2
        ON m1.meeting_id < m2.meeting_id
        AND (m1.end_timestamp <= m2.start_timestamp 
             OR m2.end_timestamp <= m1.start_timestamp)
    JOIN fact_participations_zoom p1 ON m1.meeting_id = p1.meeting_id
    JOIN fact_participations_zoom p2 ON m2.meeting_id = p2.meeting_id
        AND p1.participant_id = p2.participant_id
    WHERE p1.status = 'Confirmed' 
      AND p2.status = 'Confirmed'
    GROUP BY p1.participant_id
    HAVING COUNT(DISTINCT m1.meeting_id) >= 2
)
-- Final: Combine both conditions
SELECT 
    om.participant_id,
    om.overlapped_meeting_count
FROM overlapping_meetings om
INNER JOIN non_overlapping_participants nop 
    ON om.participant_id = nop.participant_id
ORDER BY om.overlapped_meeting_count DESC;
```

---

## 🧪 Test Data Example

Let's trace through with sample data:

### Sample Meetings:
```
Meeting 1: 2022-12-06 15:00 - 16:00
Meeting 2: 2022-12-06 15:30 - 16:30  (Overlaps with M1)
Meeting 3: 2022-12-06 17:00 - 18:00  (No overlap)
Meeting 4: 2022-12-06 19:00 - 20:00  (No overlap)
```

### Sample Participations:
```
Participant 101: Confirmed in M1, M2, M3, M4
Participant 102: Confirmed in M1, M2
```

### Expected Output:
```
participant_id | overlapped_meeting_count
101            | 1  (M1 and M2 overlap, AND 101 is in M3+M4 non-overlapping)
102            | 1  (M1 and M2 overlap, BUT 102 is NOT in 2+ non-overlapping) ❌ Filtered out
```

---

## 🎨 Visual Diagram

```
Self-Join Visualization:

dim_meetings (m1)          dim_meetings (m2)
┌──────────────────┐       ┌──────────────────┐
│ Meeting 1        │       │ Meeting 2        │
│ 15:00 - 16:00    │◄─────▶│ 15:30 - 16:30    │
└──────────────────┘       └──────────────────┘
         │                          │
         │                          │
    ┌────▼────┐                ┌───▼─────┐
    │ Part 101│                │ Part 101│
    │Confirmed│                │Confirmed│
    └─────────┘                └─────────┘
         │                          │
         └──────────┬───────────────┘
                    │
            Same participant in
            overlapping meetings!
```

---

## 💡 Key Self-Join Concepts

### 1. **Avoid Duplicates**
```sql
m1.meeting_id < m2.meeting_id
```
Without this: You'd get (M1, M2) AND (M2, M1) - same pair twice!

### 2. **Time Overlap Logic**
```sql
m1.start < m2.end AND m2.start < m1.end
```
This is the **universal overlap detection formula**.

### 3. **Same Entity in Both Rows**
```sql
p1.participant_id = p2.participant_id
```
We want the SAME person in both overlapping meetings.

### 4. **Counting Pairs vs Meetings**
- `COUNT(*)` counts **pairs** of overlapping meetings
- `COUNT(DISTINCT m1.meeting_id)` counts **unique meetings**

---

## 🚀 Practice Variations

### Variation 1: Find ALL overlapping meetings (not just for participants)
```sql
SELECT 
    m1.meeting_id AS meeting_1,
    m2.meeting_id AS meeting_2,
    m1.start_timestamp AS m1_start,
    m1.end_timestamp AS m1_end,
    m2.start_timestamp AS m2_start,
    m2.end_timestamp AS m2_end
FROM dim_meetings_zoom m1
JOIN dim_meetings_zoom m2
    ON m1.meeting_id < m2.meeting_id
    AND m1.start_timestamp < m2.end_timestamp
    AND m2.start_timestamp < m1.end_timestamp;
```

### Variation 2: Find the maximum overlap duration
```sql
SELECT 
    m1.meeting_id,
    m2.meeting_id,
    TIMESTAMPDIFF(MINUTE,
        GREATEST(m1.start_timestamp, m2.start_timestamp),
        LEAST(m1.end_timestamp, m2.end_timestamp)
    ) AS overlap_minutes
FROM dim_meetings_zoom m1
JOIN dim_meetings_zoom m2
    ON m1.meeting_id < m2.meeting_id
    AND m1.start_timestamp < m2.end_timestamp
    AND m2.start_timestamp < m1.end_timestamp;
```

---

## ✅ Common Mistakes to Avoid

### ❌ Mistake 1: Forgetting `m1.meeting_id < m2.meeting_id`
**Result**: Duplicates and self-matches

### ❌ Mistake 2: Wrong overlap logic
```sql
-- WRONG:
AND m1.start_timestamp < m2.start_timestamp
-- This misses cases where M2 starts before M1!
```

### ❌ Mistake 3: Not matching same participant
```sql
-- WRONG: Missing this line
AND p1.participant_id = p2.participant_id
-- Result: Counts ANY two people in overlapping meetings
```

---

## 🎯 Summary

**Self-joins are used when you need to:**
1. Compare rows within the same table
2. Find relationships between entities (overlap, hierarchy, similarity)
3. Detect patterns (consecutive events, duplicates)

**The overlapping meetings problem teaches:**
- ✅ Time-based comparisons
- ✅ Avoiding duplicate pairs
- ✅ Matching same entity across rows
- ✅ Complex filtering with CTEs

---

Now try building this query step by step! Start with just the overlap detection, then add participants, then add the filters. 🚀
