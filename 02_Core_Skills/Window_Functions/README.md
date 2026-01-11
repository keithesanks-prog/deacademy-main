# SQL Pattern Recognition - Quick Start Guide

Welcome to your pattern recognition training program! This guide will help you systematically improve your ability to identify when to use window functions, GROUP BY, subqueries, and other SQL patterns.

---

## 🎯 Your Goal

**In 2 weeks, you should be able to:**
- Identify the correct SQL approach from reading a problem statement (80% accuracy)
- Recognize pattern trigger phrases in < 30 seconds
- Confidently tackle SQL interview questions

---

## 📚 Your Training Materials

### 1. **Pattern Recognition Guide** 
[`pattern_recognition_guide.md`](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/pattern_recognition_guide.md)

Your main reference document. Read this first to understand:
- The 3-second decision framework
- Trigger phrases for each pattern type
- Common mistakes to avoid
- Visual flowcharts

**Action:** Read through once, then bookmark for quick reference.

---

### 2. **Practice Problems** 
[`pattern_practice_problems.md`](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/pattern_practice_problems.md)

30 progressive problems (10 basic, 10 intermediate, 10 advanced) with detailed solutions.

**Action:** Complete 5 problems per day for 6 days.

---

### 3. **Database Setup** 
[`practice_database_setup.sql`](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/practice_database_setup.sql)

Sample `employees_prc` table with 30 employees across 4 departments.

**Action:** 
1. Go to [DB Fiddle](https://www.db-fiddle.com/) (PostgreSQL)
2. Copy the entire SQL file into the left panel
3. Click "Run" to create the database
4. Now you can practice queries in the right panel!

**Alternative online SQL editors:**
- [SQLite Online](https://sqliteonline.com/) - No signup required
- [SQL Fiddle](http://sqlfiddle.com/) - Classic option
- [OneCompiler SQL](https://onecompiler.com/postgresql) - Clean interface

---

### 4. **Progress Tracker** 
[`pattern_recognition_tracker.md`](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/pattern_recognition_tracker.md)

Track your daily progress, accuracy rates, and weak areas.

**Action:** Update after each practice session.

---

## 🗓️ 2-Week Training Schedule

### **Week 1: Foundation Building**

| Day | Activity | Time | Goal |
|-----|----------|------|------|
| **Day 1** | Read pattern recognition guide | 30 min | Understand framework |
| **Day 2** | Problems 1-5 (Basic) | 30 min | 4/5 correct |
| **Day 3** | Problems 6-10 (Basic) | 30 min | 4/5 correct |
| **Day 4** | Review mistakes, retry failed problems | 30 min | Understand why you missed them |
| **Day 5** | Problems 11-15 (Intermediate) | 30 min | 3/5 correct |
| **Day 6** | Problems 16-20 (Intermediate) | 30 min | 4/5 correct |
| **Day 7** | Rest / Review trigger phrases | 15 min | Refresh memory |

**Week 1 Target:** 70% accuracy (14/20 problems)

---

### **Week 2: Mastery & Speed**

| Day | Activity | Time | Goal |
|-----|----------|------|------|
| **Day 8** | Problems 21-25 (Advanced) | 45 min | 3/5 correct |
| **Day 9** | Problems 26-30 (Advanced) | 45 min | 4/5 correct |
| **Day 10** | Retry all missed problems | 45 min | 80% correct on retry |
| **Day 11** | Speed drill: Identify pattern only (no solving) | 30 min | < 30 sec per problem |
| **Day 12** | 5 random LeetCode SQL Medium problems | 60 min | Identify pattern correctly |
| **Day 13** | 3 LeetCode SQL Hard problems | 60 min | Identify pattern correctly |
| **Day 14** | Final assessment: 10 random problems | 45 min | 8/10 correct |

**Week 2 Target:** 80% accuracy (24/30 problems total)

---

## 🚀 How to Practice Effectively

### **Step-by-Step Process for Each Problem:**

1. **Read the problem statement carefully**
   - Don't rush to write SQL
   - Highlight key phrases

2. **Identify the pattern (30 seconds max)**
   - Ask: "Do I need individual rows?"
   - Ask: "Do I need to compare within groups?"
   - Look for trigger phrases

3. **Write your solution**
   - Start with the pattern structure
   - Fill in the details

4. **Test in online SQL editor**
   - Run your query against the sample data
   - Verify results match expected output

5. **Check the provided solution**
   - Even if you got it right, compare approaches
   - Learn alternative methods

6. **Track your result**
   - Update progress tracker
   - Note any patterns you struggled with

---

## 🎯 Pattern Recognition Cheat Sheet

Keep this visible while practicing:

### **Window Function Signals:**
- ✅ "top N **per/in each**"
- ✅ "highest/lowest **in each**"
- ✅ "**rank** within"
- ✅ "**running** total/average"
- ✅ "**previous/next**"
- ✅ "compare to **department** average" (when showing individual rows)

### **GROUP BY Signals:**
- ✅ "**total** per"
- ✅ "**count** of each"
- ✅ "**average** by"
- ✅ Only need summary, not individual rows

### **Subquery Signals:**
- ✅ "employees who earn **more than average**"
- ✅ "departments **with more than** X"
- ✅ "customers who **never** ordered"

---

## 📊 Self-Assessment Checkpoints

### **After Week 1:**
- [ ] Can identify GROUP BY vs Window Function 70% of the time
- [ ] Understand when to use PARTITION BY
- [ ] Know the difference between ROW_NUMBER, RANK, and DENSE_RANK
- [ ] Can write basic window functions without reference

### **After Week 2:**
- [ ] Can identify correct pattern in < 30 seconds
- [ ] 80%+ accuracy on practice problems
- [ ] Comfortable with LAG/LEAD functions
- [ ] Can handle complex multi-step problems
- [ ] Ready for SQL technical interviews

---

## 💡 Tips for Success

1. **Don't skip the "identify pattern" step**
   - It's tempting to jump straight to writing SQL
   - Force yourself to identify the pattern first
   - This builds the recognition muscle

2. **Use online SQL editors, not just reading**
   - Actually running queries reinforces learning
   - You'll catch mistakes you'd miss by reading
   - Builds confidence

3. **Track your weak spots**
   - If you keep missing "running total" problems, do 5 more
   - Focused practice on weak areas yields fastest improvement

4. **Review trigger phrases daily**
   - Spend 2 minutes each morning reviewing the cheat sheet
   - Pattern recognition is about repetition

5. **Explain your reasoning out loud**
   - Before writing SQL, say: "This is a window function because..."
   - Verbalizing helps solidify understanding

---

## 🎓 After Completing This Program

Once you've hit 80% accuracy, you're ready for:

1. **LeetCode SQL Problems**
   - Start with Medium difficulty
   - Focus on: "Top K", "Running Totals", "Consecutive Numbers"

2. **HackerRank SQL**
   - Advanced Select
   - Aggregation challenges

3. **Real Interview Prep**
   - Practice explaining your approach verbally
   - Time yourself (most SQL interviews allow 15-30 min per problem)

4. **Update Your Skills Assessment**
   - Window Functions: 6/10 → 8/10 ✅
   - Subqueries: 7/10 → 8/10 ✅
   - Pattern Recognition: NEW SKILL! 8/10 ✅

---

## 🆘 Stuck? Here's What to Do

### **If you're struggling with a problem:**
1. Re-read the pattern recognition guide section for that pattern type
2. Look at a similar solved problem
3. Try to identify just the pattern (don't solve yet)
4. Check the solution and understand WHY that approach works
5. Close the solution and try to recreate it from memory

### **If you're not improving:**
- You might be moving too fast - slow down and focus on understanding
- Review the decision flowchart before each problem
- Do 3 problems per day instead of 5, but do them thoroughly
- Take notes on why you missed each problem

---

## 📈 Measuring Success

**You'll know you're improving when:**
- ✅ You can identify the pattern before reading the full problem
- ✅ Trigger phrases jump out at you immediately
- ✅ You feel confident choosing between window functions and GROUP BY
- ✅ You can explain WHY a certain approach is correct
- ✅ You're getting problems right on the first try

---

## 🎯 Your Commitment

**I commit to:**
- [ ] Practicing 30 minutes per day for 2 weeks
- [ ] Completing all 30 practice problems
- [ ] Tracking my progress honestly
- [ ] Reviewing mistakes instead of just moving on
- [ ] Testing queries in an online SQL editor

**Start Date:** ___/___/2025  
**Target Completion:** ___/___/2025

---

## 🚀 Ready to Start?

1. **Right now:** Open [DB Fiddle](https://www.db-fiddle.com/)
2. **Copy/paste:** The contents of `practice_database_setup.sql`
3. **Run it:** Click "Run" to create your practice database
4. **Start:** Open `pattern_practice_problems.md` and begin with Problem 1

**Remember:** You're not "bad at this" - you just haven't practiced enough yet. Every expert started exactly where you are now.

Let's build this skill together! 💪

---

## 📞 Quick Reference

- **Pattern Guide:** [`pattern_recognition_guide.md`](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/pattern_recognition_guide.md)
- **Practice Problems:** [`pattern_practice_problems.md`](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/pattern_practice_problems.md)
- **Database Setup:** [`practice_database_setup.sql`](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/practice_database_setup.sql)
- **Progress Tracker:** [`pattern_recognition_tracker.md`](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/pattern_recognition_tracker.md)
- **Online SQL Editor:** [DB Fiddle](https://www.db-fiddle.com/)

Good luck! 🎉
