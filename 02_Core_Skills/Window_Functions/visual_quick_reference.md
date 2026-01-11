# SQL Pattern Recognition - Visual Quick Reference

Use these visual guides while practicing to quickly identify the right SQL pattern.

---

## 🎯 Decision Flowchart

Use this flowchart to systematically identify which SQL approach to use:

![SQL Pattern Decision Flowchart](C:/Users/ksank/.gemini/antigravity/brain/28a9732c-190a-4cfd-89d5-516ac67b97fc/sql_pattern_flowchart_1764448792911.png)

**How to use:**
1. Start at the top: "Read SQL Problem Statement"
2. Follow the decision diamonds based on your answers
3. Land on the correct approach (Window Function, GROUP BY, or Subquery)

---

## 📋 Trigger Phrases Cheat Sheet

Keep this visible while solving problems - it shows the key phrases that signal each pattern type:

![SQL Trigger Phrases Cheat Sheet](C:/Users/ksank/.gemini/antigravity/brain/28a9732c-190a-4cfd-89d5-516ac67b97fc/sql_trigger_phrases_cheatsheet_1764448906085.png)

**Quick lookup:**
- **Orange (Window Functions):** "top N per", "highest in each", "running total", "previous/next"
- **Green (GROUP BY):** "total per", "count of each", "average by"
- **Blue (Subqueries):** "more than average", "never ordered", "employees who"

---

## 🔑 The One Question That Solves Most Problems

> **"Do I need to see INDIVIDUAL ROWS along with GROUP-LEVEL calculations?"**

- ✅ **YES** → Window Function
- ❌ **NO** → GROUP BY (if summarizing) or Subquery (if filtering)

---

## 💡 Common Scenarios

### Scenario 1: "Find the highest salary in each department"

**Analysis:**
- "highest salary" → need MAX
- "in each department" → grouping needed
- **Do I need employee names?** 
  - NO → `GROUP BY department`
  - YES → `ROW_NUMBER() OVER (PARTITION BY department ...)`

---

### Scenario 2: "Show each employee and their department's average"

**Analysis:**
- "each employee" → need individual rows ✅
- "department's average" → need group calculation ✅
- **Both needed on same row** → Window Function!

```sql
SELECT 
    employee_name,
    AVG(salary) OVER (PARTITION BY department) as dept_avg
FROM employees_prc;
```

---

### Scenario 3: "Count employees per department"

**Analysis:**
- "count per department" → aggregate
- Don't need individual employee rows → GROUP BY

```sql
SELECT department, COUNT(*)
FROM employees_prc
GROUP BY department;
```

---

## 🎓 Practice Drill

Before solving any problem, spend 10 seconds asking:

1. ✅ **What's the output?** (Individual rows or summary?)
2. ✅ **Is there grouping?** (Look for "each", "per", "by")
3. ✅ **Do I need row + group data together?** (Window function signal)
4. ✅ **What are the trigger phrases?** (Check cheat sheet)

---

## 📚 Full Training Materials

- **Start Here:** [Quick Start Guide](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/README.md)
- **Reference:** [Pattern Recognition Guide](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/pattern_recognition_guide.md)
- **Practice:** [30 Practice Problems](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/pattern_practice_problems.md)
- **Database:** [SQL Setup File](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/practice_database_setup.sql)
- **Track Progress:** [Progress Tracker](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/pattern_recognition_tracker.md)

---

## 🚀 Ready to Practice?

1. Open [DB Fiddle](https://www.db-fiddle.com/) in a new tab
2. Copy the SQL from `practice_database_setup.sql`
3. Keep this visual reference open on a second monitor (or print it)
4. Start with Problem 1 from the practice problems

**You've got this!** 💪
