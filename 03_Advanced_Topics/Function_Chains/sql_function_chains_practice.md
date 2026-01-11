# 🧩 SQL Function Chains: Practice Problems

**Learn to break down complex questions into function chains**

---

## 🎯 Problem 1: Calculate Inflated Price

### **The Question:**
> "A product's base price is $100. It increases by 3% each month. What is the price after 6 months, rounded to 2 decimal places?"

### **Step 1: Identify What You Need**
- **Base price**: 100
- **Monthly increase**: 3% (0.03)
- **Time period**: 6 months
- **Output format**: 2 decimal places

### **Step 2: Break Down the Logic**

```
Question: "What is the price after 6 months?"
→ Need: Compound interest formula

Question: "Rounded to 2 decimal places?"
→ Need: ROUND() function

Order:
1. Calculate growth: POWER(1 + 0.03, 6)
2. Multiply by base: 100 * (result)
3. Round: ROUND((result), 2)
```

### **Step 3: Build the Function Chain**

```sql
ROUND(100 * POWER(1 + 0.03, 6), 2)
```

### **Step 4: Visual Execution**

```
Step 1: Calculate growth multiplier
┌─────────────────────┐
│ POWER(1.03, 6)      │
│ = 1.1941            │
└─────────────────────┘
        ↓
Step 2: Multiply by base price
┌─────────────────────┐
│ 100 * 1.1941        │
│ = 119.41            │
└─────────────────────┘
        ↓
Step 3: Round to 2 decimals
┌─────────────────────┐
│ ROUND(119.41, 2)    │
│ = 119.41            │
└─────────────────────┘

Answer: $119.41
```

---

## 🎯 Problem 2: Find Top 2 Salaries per Department

### **The Question:**
> "Show the 2 highest-paid employees in each department."

### **Step 1: Identify What You Need**
- **Group by**: Department
- **Ranking**: Top 2 per group
- **Sort by**: Salary (highest first)

### **Step 2: Break Down the Logic**

```
Question: "In each department"
→ Need: PARTITION BY department

Question: "Highest-paid"
→ Need: ORDER BY salary DESC

Question: "Top 2"
→ Need: RANK() or ROW_NUMBER()
→ Then: WHERE rank <= 2
```

### **Step 3: Build the Function Chain**

```sql
WITH ranked AS (
    SELECT 
        employee_name,
        department,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
    FROM employees
)
SELECT * FROM ranked WHERE rn <= 2;
```

### **Step 4: Visual Execution**

```
Step 1: PARTITION BY department (Split into groups)
┌─────────────────────────────────────┐
│         Sales Department            │
│  name   | salary                    │
│  Alice  | 80000                     │
│  Bob    | 70000                     │
│  Carol  | 60000                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│         IT Department               │
│  name   | salary                    │
│  Dave   | 90000                     │
│  Eve    | 85000                     │
└─────────────────────────────────────┘
        ↓
Step 2: ORDER BY salary DESC (Sort within groups)
┌─────────────────────────────────────┐
│         Sales (Sorted)              │
│  name   | salary                    │
│  Alice  | 80000  ← Highest          │
│  Bob    | 70000                     │
│  Carol  | 60000  ← Lowest           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│         IT (Sorted)                 │
│  name   | salary                    │
│  Dave   | 90000  ← Highest          │
│  Eve    | 85000  ← Lowest           │
└─────────────────────────────────────┘
        ↓
Step 3: ROW_NUMBER() (Assign ranks)
┌─────────────────────────────────────┐
│         Sales (Ranked)              │
│  name   | salary | rn               │
│  Alice  | 80000  | 1                │
│  Bob    | 70000  | 2                │
│  Carol  | 60000  | 3                │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│         IT (Ranked)                 │
│  name   | salary | rn               │
│  Dave   | 90000  | 1                │
│  Eve    | 85000  | 2                │
└─────────────────────────────────────┘
        ↓
Step 4: WHERE rn <= 2 (Filter)
┌──────────┬────────┬────┐
│   name   │ salary │ rn │
├──────────┼────────┼────┤
│  Alice   │ 80000  │ 1  │
│  Bob     │ 70000  │ 2  │
│  Dave    │ 90000  │ 1  │
│  Eve     │ 85000  │ 2  │
└──────────┴────────┴────┘
```

---

## 🎯 Problem 3: Calculate Months Between Dates

### **The Question:**
> "How many months have passed between January 2023 and a sale date of August 15, 2023?"

### **Step 1: Identify What You Need**
- **Start date**: January 2023 (Month 1)
- **Sale date**: August 15, 2023 (Month 8)
- **Calculation**: Month difference

### **Step 2: Break Down the Logic**

```
Question: "How many months have passed?"
→ Need: EXTRACT(MONTH FROM date)
→ Then: Subtract starting month (1)

Order:
1. Extract month from sale_date
2. Subtract 1 (for January)
```

### **Step 3: Build the Function Chain**

```sql
EXTRACT(MONTH FROM '2023-08-15') - 1
```

### **Step 4: Visual Execution**

```
Step 1: Extract the month
┌─────────────────────┐
│ EXTRACT(MONTH FROM  │
│  '2023-08-15')      │
│ = 8                 │
└─────────────────────┘
        ↓
Step 2: Subtract starting month
┌─────────────────────┐
│      8 - 1          │
│      = 7            │
└─────────────────────┘

Answer: 7 months
```

---

## 🎯 Problem 4: Average of Squared Values

### **The Question:**
> "Calculate the average of the squared prices, rounded to 1 decimal place."

### **Step 1: Identify What You Need**
- **Transform**: Square each price
- **Aggregate**: Average
- **Format**: 1 decimal place

### **Step 2: Break Down the Logic**

```
Question: "Squared prices"
→ Need: POWER(price, 2)

Question: "Average"
→ Need: AVG(...)

Question: "Rounded to 1 decimal"
→ Need: ROUND(..., 1)

Order:
1. Square: POWER(price, 2)
2. Average: AVG(...)
3. Round: ROUND(..., 1)
```

### **Step 3: Build the Function Chain**

```sql
ROUND(AVG(POWER(price, 2)), 1)
```

### **Step 4: Visual Execution**

```
Input: prices = [10, 20, 30]

Step 1: Square each price
┌─────────────────────┐
│ POWER(10, 2) = 100  │
│ POWER(20, 2) = 400  │
│ POWER(30, 2) = 900  │
└─────────────────────┘
        ↓
Step 2: Calculate average
┌─────────────────────┐
│ AVG(100, 400, 900)  │
│ = 466.67            │
└─────────────────────┘
        ↓
Step 3: Round to 1 decimal
┌─────────────────────┐
│ ROUND(466.67, 1)    │
│ = 466.7             │
└─────────────────────┘

Answer: 466.7
```

---

## 🧠 Your Turn: Practice Problems

### **Problem A:**
> "A car's value depreciates by 15% each year. If it starts at $30,000, what is its value after 3 years, truncated to 2 decimals?"

<details>
<summary>Click for breakdown</summary>

**Logic:**
1. Depreciation = multiply by 0.85 each year
2. After 3 years: `POWER(0.85, 3)`
3. Multiply by start value: `30000 * ...`
4. Truncate: `TRUNCATE(..., 2)`

**Answer:**
```sql
TRUNCATE(30000 * POWER(0.85, 3), 2)
```
</details>

---

### **Problem B:**
> "Find the 3rd highest salary in the company (no ties, unique ranking)."

<details>
<summary>Click for breakdown</summary>

**Logic:**
1. No partitioning (whole company)
2. Unique ranking: `ROW_NUMBER()`
3. Sort by salary: `ORDER BY salary DESC`
4. Filter: `WHERE rn = 3`

**Answer:**
```sql
WITH ranked AS (
    SELECT salary, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn
    FROM employees
)
SELECT salary FROM ranked WHERE rn = 3;
```
</details>

---

### **Problem C:**
> "Combine first name and last name with a hyphen, then convert to uppercase."

<details>
<summary>Click for breakdown</summary>

**Logic:**
1. Combine: `CONCAT(first_name, '-', last_name)`
2. Uppercase: `UPPER(...)`

**Answer:**
```sql
UPPER(CONCAT(first_name, '-', last_name))
```
</details>

---

## 💡 The Pattern

**Every complex SQL expression follows this pattern:**

```
1. Read the question
2. Identify the transformations needed
3. Determine the order (inside → out)
4. Build the function chain
5. Visualize the execution
```

**Key Questions to Ask:**
- "What data do I start with?"
- "What transformations are needed?"
- "What's the final output format?"
- "Which function goes inside which?"
