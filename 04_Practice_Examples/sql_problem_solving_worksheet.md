# 🎓 SQL Problem-Solving Worksheet
## Employee Salary Analysis Problem

---

## 📋 The Problem

**Find employees whose salaries are higher than BOTH:**
1. Their department manager's salary
2. The average salary of their department

**Return:** employee name, employee_salary, manager_salary, avg_dept_salary, department_name

---

## 📊 Available Tables

### **dim_employee_twitter**
| Column | Description |
|--------|-------------|
| user_id | Employee ID |
| name | Employee name |
| department_id | Which department |
| manager_id | Direct manager's user_id |
| salary_usd | Employee salary |

### **dim_dept_twitter**
| Column | Description |
|--------|-------------|
| deparment_id | Department ID |
| department_name | Department name |
| manager_id | Department manager's user_id |

---

## 🎯 Step 1: Understand the Requirements

### **Question 1:** What columns do we need in the final output?

Write them here:
1. _employee name__________________
2. _employee salary__________________
3. _manager salary__________________
4. _average department salary__________________
5. _department name__________________

<details>
<summary>✅ Answer</summary>

1. employee (name)
2. employee_salary
3. manager_salary
4. avg_dept_salary
5. department_name
</details>

---

### **Question 2:** What are the filter conditions?

Employee salary must be:
- Greater than: __manager salary_________________
- AND greater than: _average department salary__________________

<details>
<summary>✅ Answer</summary>

- Greater than: **manager's salary**
- AND greater than: **department average salary**
</details>

---

## 🔍 Step 2: Identify Data Sources

### **Question 3:** Where is each piece of data?

| Data Needed | Table | Column |
|-------------|-------|--------|
| Employee name | dim_employee_twitter | name |
| Employee salary | dim_employee_twitter | salary_usd |
| Department name | dim_dept_twitter | department_name |
| Manager salary | dim_employee_twitter | salary_usd (via manager_id) |
| Dept average | dim_employee_twitter | AVG(salary_usd) grouped by dept |

<details>
<summary>✅ Answer</summary>

| Data Needed | Table | Column |
|-------------|-------|--------|
| Employee name | dim_employee_twitter | name |
| Employee salary | dim_employee_twitter | salary_usd |
| Department name | dim_dept_twitter | department_name |
| Manager salary | dim_employee_twitter | salary_usd (via manager_id) |
| Dept average | dim_employee_twitter | AVG(salary_usd) grouped by dept |
</details>

---

## 🔨 Step 3: Build the Query Incrementally

### **Exercise 1: Get Employee and Department Info**

**Task:** Write a query to get employee name, salary, and department name.

```sql
SELECT 
    -- Fill in the columns you need
FROM dim_employee_twitter e
-- What JOIN do you need?
JOIN dim_dept_twitter d ON e.department_id = d.deparment_id;
```

**Your Answer:**
```sql
-- Write your query here
SELECT 
    e.name,
    e.salary_usd,
    d.department_name
FROM dim_employee_twitter e
JOIN dim_dept_twitter d ON e.department_id = d.deparment_id;




```

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    e.name,
    e.salary_usd,
    d.department_name
FROM dim_employee_twitter e
JOIN dim_dept_twitter d ON e.department_id = d.department_id;
```
</details>

**Test it!** Run this query. Do you see employee names and departments?

---

### **Exercise 2: Add Manager's Salary**

**Think about it:**
- The department table has `manager_id`
- The manager is also an employee in `dim_employee_twitter`
- You need to join the employee table **twice** (once for employee, once for manager)

**Task:** Add the manager's salary to your query.

**Hint:** Use a second JOIN with alias `m` for manager.

```sql
SELECT 
    e.name,
    e.salary_usd,
    d.department_name,
    -- Add manager salary here
FROM dim_employee_twitter e
JOIN dim_dept_twitter d ON e.department_id = d.deparment_id
-- Add another JOIN here for manager
```

**Your Answer:**
```sql
-- Write your query here
SELECT 
    e.name,
    e.salary_usd,
    d.department_name,
    m.salary_usd AS manager_salary
FROM dim_employee_twitter e
JOIN dim_dept_twitter d ON e.department_id = d.deparment_id
JOIN dim_employee_twitter m ON d.manager_id = m.user_id;



```

<details>
<summary>💡 Hint</summary>

The department's `manager_id` points to a `user_id` in the employee table. Join like this:
```sql
JOIN dim_employee_twitter m ON d.manager_id = m.user_id
```
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    e.name,
    e.salary_usd,
    d.department_name,
    m.salary_usd AS manager_salary
FROM dim_employee_twitter e
JOIN dim_dept_twitter d ON e.department_id = d.deparment_id
JOIN dim_employee_twitter m ON d.manager_id = m.user_id;
```
</details>

**Test it!** Do you now see both employee and manager salaries?

---

### **Exercise 3: Calculate Department Average (Subquery)**

**First, create the subquery separately:**

**Task:** Write a query that calculates the average salary for each department.

```sql
SELECT 
    -- What do you need to group by?
    -- What aggregate function calculates average?
FROM dim_employee_twitter
GROUP BY -- Fill this in
```

**Your Answer:**
```sql
-- Write your subquery here
SELECT 
    department_id,
    AVG(salary_usd) AS avg_salary
FROM dim_employee_twitter
GROUP BY department_id;



```

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    department_id,
    AVG(salary_usd) AS avg_salary
FROM dim_employee_twitter
GROUP BY department_id;
```
</details>

**Test it!** Run this separately. Do you see one row per department with an average?

---

### **Exercise 4: Add Department Average to Main Query**

**Task:** Now join the subquery from Exercise 3 to your main query from Exercise 2.

**Hint:** Treat the subquery like a table and give it an alias like `dept_avg`.

```sql
SELECT 
    e.name,
    e.salary_usd,
    d.department_name,
    m.salary_usd AS manager_salary,
    -- Add department average here
FROM dim_employee_twitter e
JOIN dim_dept_twitter d ON e.department_id = d.deparment_id
JOIN dim_employee_twitter m ON d.manager_id = m.user_id
-- Add subquery JOIN here
```

**Your Answer:**
```sql
-- Write your complete query here









```

<details>
<summary>💡 Hint</summary>

Join the subquery on `department_id`:
```sql
JOIN (
    SELECT department_id, AVG(salary_usd) AS avg_salary
    FROM dim_employee_twitter
    GROUP BY department_id
) dept_avg ON e.department_id = dept_avg.department_id
```
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    e.name,
    e.salary_usd,
    d.department_name,
    m.salary_usd AS manager_salary,
    dept_avg.avg_salary AS avg_dept_salary
FROM dim_employee_twitter e
JOIN dim_dept_twitter d ON e.department_id = d.deparment_id
JOIN dim_employee_twitter m ON d.manager_id = m.user_id
JOIN (
    SELECT 
        department_id,
        AVG(salary_usd) AS avg_salary
    FROM dim_employee_twitter
    GROUP BY department_id
) dept_avg ON e.department_id = dept_avg.department_id;
```
</details>

**Test it!** Do you see all the columns you need?

---

### **Exercise 5: Add Filter Conditions**

**Task:** Add a WHERE clause to filter employees whose salary is greater than BOTH the manager's salary AND the department average.

**Think:**
- You need TWO conditions
- Both must be true (use `AND`)
- Compare employee salary to manager salary
- Compare employee salary to department average

```sql
-- Take your query from Exercise 4 and add WHERE clause here
WHERE -- Fill in your conditions


```

**Your Answer:**
```sql
-- Write your complete query with WHERE clause here













```

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    e.name AS employee,
    e.salary_usd AS employee_salary,
    m.salary_usd AS manager_salary,
    dept_avg.avg_salary AS avg_dept_salary,
    d.department_name
FROM dim_employee_twitter e
JOIN dim_dept_twitter d ON e.department_id = d.deparment_id
JOIN dim_employee_twitter m ON d.manager_id = m.user_id
JOIN (
    SELECT 
        department_id,
        AVG(salary_usd) AS avg_salary
    FROM dim_employee_twitter
    GROUP BY department_id
) dept_avg ON e.department_id = dept_avg.department_id
WHERE e.salary_usd > m.salary_usd
  AND e.salary_usd > dept_avg.avg_salary
ORDER BY e.salary_usd DESC;
```
</details>

---

## 🎯 Step 4: Verify Your Understanding

### **Question 4:** What does this query do?

Explain in your own words:

1. What tables are we joining?
   - ___________________
   - ___________________
   - ___________________

2. Why do we join `dim_employee_twitter` twice?
   - ___________________

3. What does the subquery calculate?
   - ___________________

4. What are the two filter conditions?
   - ___________________
   - ___________________

<details>
<summary>✅ Answers</summary>

1. **Tables:**
   - dim_employee_twitter (for employees)
   - dim_dept_twitter (for department names)
   - dim_employee_twitter again (for managers)
   - Subquery (for department averages)

2. **Why twice?**
   - Once for the employee's data (alias `e`)
   - Once for the manager's data (alias `m`)
   - This is called a self-join

3. **Subquery calculates:**
   - Average salary for each department

4. **Filter conditions:**
   - Employee salary > Manager salary
   - Employee salary > Department average salary
</details>

---

## 💡 Key Concepts You Learned

- [ ] **Self-Join**: Joining a table to itself to get related data
- [ ] **Subquery**: Creating a temporary result set to join back
- [ ] **Aggregate Functions**: Using AVG() with GROUP BY
- [ ] **Multiple JOINs**: Connecting multiple tables together
- [ ] **Complex WHERE**: Using AND to combine multiple conditions

---

## 🚀 Challenge: Alternative Approach

**Can you rewrite this using a Window Function instead of a subquery?**

**Hint:** Use `AVG() OVER (PARTITION BY department_id)`

```sql
-- Try writing it here








```

<details>
<summary>✅ Solution</summary>

```sql
WITH employee_data AS (
    SELECT 
        e.name AS employee,
        e.salary_usd AS employee_salary,
        m.salary_usd AS manager_salary,
        AVG(e.salary_usd) OVER (PARTITION BY e.department_id) AS avg_dept_salary,
        d.department_name
    FROM dim_employee_twitter e
    JOIN dim_dept_twitter d ON e.department_id = d.deparment_id
    JOIN dim_employee_twitter m ON d.manager_id = m.user_id
)
SELECT *
FROM employee_data
WHERE employee_salary > manager_salary
  AND employee_salary > avg_dept_salary
ORDER BY employee_salary DESC;
```
</details>

---

## ✅ Summary

You've learned how to:
1. ✅ Break down complex requirements
2. ✅ Identify data sources across multiple tables
3. ✅ Build queries incrementally
4. ✅ Use self-joins to get related data
5. ✅ Calculate aggregates with subqueries
6. ✅ Apply multiple filter conditions

**Great job!** 🎉
