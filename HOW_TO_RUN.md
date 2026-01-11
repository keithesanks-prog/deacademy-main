# 🚀 Quick Start Guide - Running Your SQL Practice Environment

## ✅ You Already Have SQLite Online Open!

I can see you have https://sqliteonline.com/ open in your browser. Perfect! Now follow these simple steps:

---

## 📋 Step-by-Step Instructions

### **Step 1: Copy the Setup SQL**
1. Open the file `sql_practice_setup.sql` (you already have it open!)
2. Press `Ctrl + A` to select all
3. Press `Ctrl + C` to copy

---

### **Step 2: Paste into SQLite Online**
1. Go to your browser tab with SQLite Online
2. Click in the **large text area** (the SQL editor)
3. Clear any existing text
4. Press `Ctrl + V` to paste your setup SQL

---

### **Step 3: Run the Setup**
1. Click the **"Run"** button (blue button at the top)
2. Wait a few seconds
3. You should see output showing your tables were created

---

### **Step 4: Verify It Worked**
Run this simple query to check:
```sql
SELECT * FROM customers;
```

You should see 8 customers with names like John Smith, Maria Garcia, etc.

---

### **Step 5: Start Practicing!**
Now open `sql_case_practice_exercises.md` and try Exercise 1:

```sql
SELECT 
    name,
    total_spent,
    CASE 
        WHEN total_spent > 1000 THEN 'Yes'
        ELSE 'No'
    END AS high_spender_flag
FROM customers;
```

Just paste this into the SQL editor and click "Run"!

---

## 🎯 Quick Reference

### **To Run Any Query:**
1. Clear the SQL editor (or select all and delete)
2. Paste your query
3. Click "Run"
4. See results below

### **To See All Data in a Table:**
```sql
SELECT * FROM customers;
SELECT * FROM products;
SELECT * FROM orders;
SELECT * FROM employees;
```

### **To Clear and Start Fresh:**
Just refresh the browser page and paste the setup SQL again!

---

## 💡 Pro Tips

- **Save your work**: Copy successful queries to a text file
- **Experiment**: Change the CASE conditions and see what happens
- **One query at a time**: Run one SELECT statement at a time for clearer results
- **Check the data first**: Always run `SELECT * FROM table_name` to see what you're working with

---

## 🆘 Troubleshooting

**Problem:** "No such table" error  
**Solution:** Run the setup SQL again (Step 1-3)

**Problem:** No results showing  
**Solution:** Make sure you clicked "Run" and scroll down to see results

**Problem:** Syntax error  
**Solution:** Check for typos, missing commas, or unclosed quotes

---

## ✅ You're Ready!

You now have:
- ✅ 4 tables with sample data
- ✅ A working SQL environment
- ✅ 11 practice exercises to work through

Start with Exercise 1 in `sql_case_practice_exercises.md` and have fun! 🎓
