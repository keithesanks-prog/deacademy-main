# 🎧 Nike Products Analysis - Audio Lesson Companion

**This guide matches the audio lesson script. Follow along as you listen!**

---

## 🗣️ The Question

> "For products with available stock above 100 and ordered after January 1, 2023, calculate the average price by gender. Additionally, label each average price as 'Premium' if it's above 170, otherwise 'Affordable'. Round the average price to 2 decimal places. Output should contain: gender, avg_price, and price_tier."

---

## 📋 The Breakdown: 4 Requirements

### **Requirement 1: The Filters**
> *"For products with available stock above 100 and ordered after January 1, 2023"*

**SQL Translation:**
```sql
WHERE available_stocks > 100 
  AND order_date > '2023-01-01'
```

### **Requirement 2: The Grouping**
> *"calculate the average price by gender"*

**SQL Translation:**
```sql
GROUP BY gender
```

### **Requirement 3: The Calculation**
> *"Round the average price to 2 decimal places"*

**SQL Translation:**
```sql
ROUND(AVG(price), 2)
```

### **Requirement 4: The Labeling**
> *"label each average price as Premium if it's above 170, otherwise Affordable"*

**SQL Translation:**
```sql
CASE 
    WHEN AVG(price) > 170 THEN 'Premium' 
    ELSE 'Affordable' 
END
```

---

## 📊 The Tables

| Table | Columns Needed | Why? |
|-------|----------------|------|
| **dim_product_nike** | `price`, `gender`, `order_date` | Calculations & Grouping |
| **dim_category_nike** | `available_stocks` | Filtering |

**Action:** We MUST **JOIN** these tables on `category_id`.

---

## 🔨 Building the Query

### **Step 1: The SELECT Clause**
```sql
SELECT
    gender,
    ROUND(AVG(price), 2) AS avg_price,
    CASE 
        WHEN AVG(price) > 170 THEN 'Premium' 
        ELSE 'Affordable' 
    END AS price_tier
```

### **Step 2: The FROM and JOIN**
```sql
FROM dim_product_nike dpn
JOIN dim_category_nike dcn ON dcn.category_id = dpn.category_id
```

### **Step 3: The WHERE Clause**
```sql
WHERE available_stocks > 100 
  AND order_date > '2023-01-01'
```

### **Step 4: The GROUP BY Clause**
```sql
GROUP BY gender;
```

---

## ✅ The Complete Query

```sql
SELECT
    gender,
    ROUND(AVG(price), 2) AS avg_price,
    CASE 
        WHEN AVG(price) > 170 THEN 'Premium' 
        ELSE 'Affordable' 
    END AS price_tier
FROM dim_product_nike dpn
JOIN dim_category_nike dcn ON dcn.category_id = dpn.category_id
WHERE available_stocks > 100
  AND order_date > '2023-01-01'
GROUP BY gender;
```

---

## 🔄 Execution Flow Recap

1.  **JOIN**: Connects the data.
2.  **WHERE**: Filters out old orders and low stock items.
3.  **GROUP BY**: Groups remaining items by gender.
4.  **SELECT**: Calculates averages and applies labels.
