# 🎧 SQL MAX Function Pitfalls - Audio Lesson Companion

**This guide matches the audio lesson script. Follow along as you listen!**

---

## 🎯 The Goal

**Question:**
"Retrieve the employee details (name, salary) of the employee with the **highest salary** in **each department**."

---

## ❌ The "Groupwise Max" Trap

**The Incorrect Query:**
```sql
SELECT 
    first_name, 
    department, 
    MAX(salary)   -- This is fine
FROM employees
GROUP BY department;
```

**Why it Fails:**
- The database groups rows by `department`.
- It calculates `MAX(salary)` correctly (e.g., 90,000).
- **BUT**: It doesn't know which `first_name` belongs to that salary!
- **Result**: You get the correct Max Salary, but a **RANDOM** name.

---

## ✅ The Solution: Subquery + JOIN

We need to find the "Winners" first, then find the full details.

### **Step 1: Find the Winners (The Subquery)**
Create a list of departments and their top salaries.

```sql
SELECT department, MAX(salary) as max_sal 
FROM employees 
GROUP BY department
```
*(This returns: Sales - 80k, IT - 70k, etc.)*

### **Step 2: Join Back to Original Table**
Find the employee who matches **BOTH** the department **AND** the max salary.

```sql
SELECT 
    E.first_name, 
    E.last_name, 
    E.department, 
    E.salary
FROM employees E
JOIN (
    -- The "Winners Table"
    SELECT department, MAX(salary) as max_sal 
    FROM employees 
    GROUP BY department
) M 
ON E.department = M.department 
AND E.salary = M.max_sal;  -- The Critical Match!
```

---

## 🚀 Visualizing the Logic

**1. Original Table (Employees)**
| Name | Dept | Salary |
|------|------|--------|
| John | Sales| 65k |
| Mike | Sales| **80k**|
| Jane | IT | **70k**|

**2. The Subquery (M)**
| Dept | Max_Sal |
|------|---------|
| Sales| 80k |
| IT | 70k |

**3. The JOIN (E + M)**
- Does John (Sales, 65k) match (Sales, 80k)? **NO** ❌
- Does Mike (Sales, 80k) match (Sales, 80k)? **YES** ✅ -> **Winner!**
- Does Jane (IT, 70k) match (IT, 70k)? **YES** ✅ -> **Winner!**

---

## 💡 Key Takeaway

To find the **row** with the max value:
1.  Calculate the MAX in a subquery.
2.  JOIN it back to the main table.
3.  Match on **Grouping Column** AND **Max Value Column**.
