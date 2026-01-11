# 🎓 SQL CASE Statement Practice Exercises

## 🚀 Getting Started

### **Step 1: Set Up Your Database**
1. Open your SQL environment (SQLite, MySQL Workbench, pgAdmin, or online tool like [SQLite Online](https://sqliteonline.com/))
2. Run the `sql_practice_setup.sql` file to create tables with sample data
3. Verify tables were created by running: `SELECT * FROM customers;`

---

## 📊 Sample Data Overview

### **Customers Table**
| customer_id | name         | total_spent | last_purchase_date | country |
|-------------|------------- |-------------|------------------- |---------|
| 1           | John Smith   | 1500.00     | 2025-11-20         | England |
| 2           | Maria Garcia | 800.00      | 2025-09-15         | India   |
| 3           | Chen Wei     | 2500.00     | 2025-11-25         | China   |
| ...         | ...          | ...         | ...                | ...     |

### **Products Table**
| product_id | product_name | price     | category       | units_sold |
|------------|--------------  |---------|----------------|------------|
| 1          | Laptop Pro     | 1200.00 | Electronics    | 150        |
| 2          | Wireless Mouse | 25.00   | Electronics    | 500        |
| ...        | ...            | ...     | ...            | ...        |

### **Orders Table**
| order_id    | customer_id | order_date | amount  | status    |
|-------------|-------------|------------|-------- |--------   |
| 101         | 1           | 2025-11-20 | 1200.00 | Completed |
| 102         | 2           | 2025-11-21 | 450.00  | Completed |
| ...         | ...         | ...        | ...     | ...       |

### **Employees Table**
| employee_id | name          | department | salary   | years_experience | performance_score |
|-------------|-------------  |-------------|----------|------------------|-------------------|
| 1           | Alice Johnson | Sales       | 65000    | 3                | 92                |
| 2           | Bob Williams  | Engineering | 95000    | 7                | 88                |
| ...         | ...           | ...         | ...      | ...              | ...               |

---

## 🟢 EASY EXERCISES - Basic CASE Statements

### **Exercise 1: Binary Flag**
**Problem:** Create a flag to identify high-spending customers (those who spent > $1000).

**Expected Output:**
| name         | total_spent | high_spender_flag |
|------------- |-------------|-------------------|
| John Smith   | 1500.00     | Yes               |
| Maria Garcia | 800.00      | No                |
| ...          | ...         | ...               |

<details>
<summary>💡 Hint</summary>

Use CASE with a simple condition:
```sql
CASE 
    WHEN total_spent > 1000 THEN 'Yes'
    ELSE 'No'
END
```
</details>

<details>
<summary>✅ Solution</summary>

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
</details>

---

### **Exercise 2: Price Categories**
**Problem:** Categorize products as 'Expensive' (price > $500), 'Moderate' ($100-$500), or 'Cheap' (< $100).

**Expected Output:**
| product_name   | price   | price_category |
|--------------  |-------  |----------------|
| Laptop Pro     | 1200.00 | Expensive      |
| Wireless Mouse | 25.00   | Cheap          |
| ..    .        | ...     | ...            |

<details>
<summary>💡 Hint</summary>

Use multiple WHEN conditions:
```sql
CASE 
    WHEN price > 500 THEN 'Expensive'
    WHEN price >= 100 THEN 'Moderate'
    ELSE 'Cheap'
END
```
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    product_name,
    price,
    CASE 
        WHEN price > 500 THEN 'Expensive'
        WHEN price >= 100 THEN 'Moderate'
        ELSE 'Cheap'
    END AS price_category
FROM products;
```
</details>

---

### **Exercise 3: Customer Activity Status**
**Problem:** Flag customers as 'Active' if last purchase was within 60 days, otherwise 'Inactive'.

**Expected Output:**
| name         | last_purchase_date | activity_status |
|------------- |------------------- |-----------------|
| John Smith   | 2025-11-20         | Active          |
| Maria Garcia | 2025-09-15         | Inactive        |
| ...          | ...                | ...             |

<details>
<summary>💡 Hint</summary>

Use date comparison:
```sql
CASE 
    WHEN last_purchase_date >= DATE('now', '-60 days') THEN 'Active'
    ELSE 'Inactive'
END
```
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    name,
    last_purchase_date,
    CASE 
        WHEN last_purchase_date >= DATE('now', '-60 days') THEN 'Active'
        ELSE 'Inactive'
    END AS activity_status
FROM customers;
```
</details>

---

## 🟡 MEDIUM EXERCISES - Multi-Condition CASE

### **Exercise 4: Country Type (The Airbnb Pattern!)**
**Problem:** Create a country_type flag with values:
- 'Land Countries' for countries containing 'land'
- 'Ending A Countries' for countries ending with 'a'
- 'Other Countries' for the rest

**Expected Output:**
| name          | country      | country_type |
|-------------  |------------- |--------------|
| John Smith    | England      | Land Countries |
| Maria Garcia  | India        | Ending A Countries |
| Sophie Martin | France       | Other Countries |
| ...           | ...          | ...          |

<details>
<summary>💡 Hint</summary>

Use LIKE with wildcards:
```sql
CASE 
    WHEN LOWER(country) LIKE '%land%' THEN 'Land Countries'
    WHEN LOWER(country) LIKE '%a' THEN 'Ending A Countries'
    ELSE 'Other Countries'
END
```
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    name,
    country,
    CASE 
        WHEN LOWER(country) LIKE '%land%' THEN 'Land Countries'
        WHEN LOWER(country) LIKE '%a' THEN 'Ending A Countries'
        ELSE 'Other Countries'
    END AS country_type
FROM customers;
```
</details>

---

### **Exercise 5: Order Priority**
**Problem:** Flag orders as 'Urgent' (amount > $10,000), 'High Priority' ($1,000-$10,000), or 'Normal' (< $1,000).

**Expected Output:**
| order_id | amount    | priority_flag |
|----------|-----------|---------------|
| 103      | 8500.00   | High Priority |
| 105      | 12000.00  | Urgent        |
| ...      | ...       | ...           |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    order_id,
    amount,
    CASE 
        WHEN amount > 10000 THEN 'Urgent'
        WHEN amount >= 1000 THEN 'High Priority'
        ELSE 'Normal'
    END AS priority_flag
FROM orders;
```
</details>

---

### **Exercise 6: Employee Performance Tier**
**Problem:** Assign performance tiers:
- 'Excellent' (score >= 90)
- 'Good' (score 80-89)
- 'Average' (score 70-79)
- 'Needs Improvement' (score < 70)

**Expected Output:**
| name          | performance_score | performance_tier |
|-------------  |-------------------|------------------|
| Alice Johnson | 92                | Excellent        |
| Carol Davis   | 75                | Average          |
| ...           | ...               | ...              |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    name,
    performance_score,
    CASE 
        WHEN performance_score >= 90 THEN 'Excellent'
        WHEN performance_score >= 80 THEN 'Good'
        WHEN performance_score >= 70 THEN 'Average'
        ELSE 'Needs Improvement'
    END AS performance_tier
FROM employees;
```
</details>

---

## 🔴 HARD EXERCISES - Complex CASE with Aggregation

### **Exercise 7: Customer Segments with Aggregation**
**Problem:** Calculate average spending per country_type (using the country categorization from Exercise 4).

**Expected Output:**
| country_type      | avg_spending |
|------------------|--------------|
| Land Countries    | 1650.00      |
| Ending A Countries| 1900.00      |
| Other Countries   | 775.00       |

<details>
<summary>💡 Hint</summary>

Use CASE in SELECT, then GROUP BY the CASE result:
```sql
SELECT 
    CASE ... END AS country_type,
    AVG(total_spent) as avg_spending
FROM customers
GROUP BY country_type;
```
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    CASE 
        WHEN LOWER(country) LIKE '%land%' THEN 'Land Countries'
        WHEN LOWER(country) LIKE '%a' THEN 'Ending A Countries'
        ELSE 'Other Countries'
    END AS country_type,
    ROUND(AVG(total_spent), 2) as avg_spending
FROM customers
GROUP BY country_type
ORDER BY avg_spending DESC;
```
</details>

---

### **Exercise 8: Salary Tiers by Department**
**Problem:** For each department, calculate the average salary and assign a tier:
- 'High Pay' (avg > $80,000)
- 'Medium Pay' ($60,000-$80,000)
- 'Low Pay' (< $60,000)

**Expected Output:**
| department      | avg_salary | pay_tier   |
|------------     |------------|----------  |
| Engineering     | 96000.00   | High Pay   |
| Marketing       | 70000.00   | Medium Pay |
| ...             | ...        | ...        |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    department,
    ROUND(AVG(salary), 2) as avg_salary,
    CASE 
        WHEN AVG(salary) > 80000 THEN 'High Pay'
        WHEN AVG(salary) >= 60000 THEN 'Medium Pay'
        ELSE 'Low Pay'
    END AS pay_tier
FROM employees
GROUP BY department;
```
</details>

---

### **Exercise 9: Senior Employee Flag with Multiple Conditions**
**Problem:** Flag employees as 'Senior' if they have 5+ years experience AND performance score > 85, otherwise 'Junior'.

**Expected Output:**
| name         | years_experience   | performance_score  | seniority_flag   |
|------------  |------------------  |------------------- |------------------|
| Bob Williams | 7                  | 88                 | Senior           |
| Eve Wilson   | 10                 | 95                 | Senior           |
| Alice Johnson| 3                  | 92                 | Junior           |
| ...          | ...                | ...                | ...              |

<details>
<summary>💡 Hint</summary>

Use AND in the WHEN condition:
```sql
CASE 
    WHEN years_experience >= 5 AND performance_score > 85 THEN 'Senior'
    ELSE 'Junior'
END
```
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    name,
    years_experience,
    performance_score,
    CASE 
        WHEN years_experience >= 5 AND performance_score > 85 THEN 'Senior'
        ELSE 'Junior'
    END AS seniority_flag
FROM employees;
```
</details>

---

### **Exercise 10: Product Performance Matrix**
**Problem:** Categorize products as:
- 'Star' if price > $200 AND units_sold > 150
- 'High Revenue' if only price > $200
- 'High Volume' if only units_sold > 150
- 'Underperformer' otherwise

**Expected Output:**
| product_name   | price   | units_sold | performance_category |
|--------------  |-------  |------------|---------------------|
| Laptop Pro     | 1200.00 | 150        | High Revenue         |
| Monitor 27"    | 450.00  | 180        | Star                 |
| ...            | ...     | ...        | ...                  |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    product_name,
    price,
    units_sold,
    CASE 
        WHEN price > 200 AND units_sold > 150 THEN 'Star'
        WHEN price > 200 THEN 'High Revenue'
        WHEN units_sold > 150 THEN 'High Volume'
        ELSE 'Underperformer'
    END AS performance_category
FROM products;
```
</details>

---

## 🎯 Challenge Exercise - The Full Airbnb Problem

### **Exercise 11: Average Days to Second Booking (Simplified)**
**Problem:** Using the customers table, calculate the average total_spent for each country_type.

This mimics the Airbnb problem structure:
1. Categorize countries using CASE
2. Group by the category
3. Calculate average
4. Round to 3 decimals

**Expected Output:**
| country_type      | avg_total_spent |
|------------ ------|-----------------|
| Land Countries    | 1650.000        |
| Ending A Countries| 1900.000        |
| Other Countries   | 775.000         |

<details>
<summary>✅ Solution</summary>

```sql
SELECT 
    CASE 
        WHEN LOWER(country) LIKE '%land%' THEN 'Land Countries'
        WHEN LOWER(country) LIKE '%a' THEN 'Ending A Countries'
        ELSE 'Other Countries'
    END AS country_type,
    ROUND(AVG(total_spent), 3) as avg_total_spent
FROM customers
GROUP BY country_type
ORDER BY avg_total_spent DESC;
```
</details>

---

## 💡 Practice Tips

1. **Start Simple**: Begin with Exercise 1 and work your way up
2. **Try Before Looking**: Attempt each exercise before checking the hint or solution
3. **Experiment**: Modify the conditions and see how results change
4. **Verify**: Always run `SELECT * FROM table_name` to see the raw data first
5. **Build Gradually**: Start with just the CASE, then add GROUP BY, then add ORDER BY

---

## 🚀 Next Steps

Once you've completed these exercises:
1. ✅ Try creating your own CASE statements
2. ✅ Combine CASE with JOINs
3. ✅ Use CASE in WHERE clauses (advanced)
4. ✅ Practice the full Airbnb problem with the actual tables

Happy practicing! 🎓
