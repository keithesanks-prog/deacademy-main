# Late Delivery Analysis - Step-by-Step Training Guide

## 🎯 Problem Statement

**Calculate the percentage of orders that took longer than 45 minutes to deliver, grouped by road traffic condition.**

---

## 📊 Step 1: Understand Your Data

Before writing any code, understand what you have:

### Available Fields:
- `order_date` - Date of order (string: "3/13/22")
- `order_time` - Time order was placed (string: "11:55:00")
- `order_picked_time` - Time delivery person picked up order (string: "12:05:00")
- `delivery_duration` - Minutes from pickup to customer delivery (integer: 42)
- `road_traffic` - Traffic condition (string: "High", "Medium", "Low", "Jam")

### What You Need to Calculate:
**Total Delivery Time** = (pickup time - order time) + delivery_duration

### Example:
```
order_time:        11:55:00
order_picked_time: 12:05:00  → 10 minutes prep/pickup
delivery_duration: 42         → 42 minutes driving
TOTAL:             52 minutes (LATE! > 45 min)
```

---

## 🔧 Step 2: Break Down the Problem

Ask yourself: **What do I need to do?**

1. ✅ Load the data
2. ✅ Convert time strings to datetime objects (can't do math on strings!)
3. ✅ Calculate total delivery time
4. ✅ Identify which orders are "late" (> 45 min)
5. ✅ Group by traffic condition
6. ✅ Calculate percentage of late orders per group

---

## 💭 Step 3: Think Through Each Step

### **Question 1: Why convert to datetime?**
- `order_time` is stored as `"11:55:00"` (string/text)
- You can't subtract strings: `"12:05:00" - "11:55:00"` = ERROR!
- Need to convert to datetime objects first

### **Question 2: Why combine date + time?**
- Time alone doesn't account for different days
- `11:55:00` on 3/13 vs `11:55:00` on 3/14 are different moments
- Must combine: `"3/13/22" + " " + "11:55:00"` = `"3/13/22 11:55:00"`

### **Question 3: How to identify late deliveries?**
- Create a boolean column: `is_late = total_time > 45`
- `True` = late, `False` = on time

### **Question 4: How to calculate percentage?**
- Group by `road_traffic`
- Count total orders per group
- Sum the `True` values in `is_late` (True = 1, False = 0)
- Percentage = (late_orders / total_orders) × 100

---

## 📝 Step 4: Pandas Operations You Need

### **Operation 1: Load Data**
```python
pd.read_csv('filename.csv')
```

### **Operation 2: Convert to Datetime - DETAILED BREAKDOWN**

#### **What You're Starting With:**
```python
# Your CSV has these as SEPARATE columns (both are strings):
order_date = "3/13/22"
order_time = "11:55:00"
```

#### **Step 2a: Combine Date + Time**
```python
# Use + to concatenate (join) strings, with ' ' (space) in between
fog_df['order_date'] + ' ' + fog_df['order_time']

# Result: "3/13/22" + " " + "11:55:00" = "3/13/22 11:55:00"
```

#### **Step 2b: Convert String to Datetime Object**
```python
# Wrap the combined string in pd.to_datetime()
fog_df['order_datetime'] = pd.to_datetime(
    fog_df['order_date'] + ' ' + fog_df['order_time']
)

# Before: "3/13/22 11:55:00" (string - can't do math)
# After:  Timestamp('2022-03-13 11:55:00') (datetime - can do math!)
```

#### **Why the Format Parameter?**
```python
# If your dates don't auto-parse, specify the format:
pd.to_datetime(string, format='%m/%d/%y %H:%M:%S')

# Format codes:
# %m = month (01-12)
# %d = day (01-31)
# %y = 2-digit year (22)
# %H = hour 24-hour format (00-23)
# %M = minute (00-59)
# %S = second (00-59)
```

#### **Complete Example:**
```python
# Do this for BOTH time fields:
fog_df['order_datetime'] = pd.to_datetime(
    fog_df['order_date'] + ' ' + fog_df['order_time']
)
fog_df['picked_datetime'] = pd.to_datetime(
    fog_df['order_date'] + ' ' + fog_df['order_picked_time']
)
```

---

### **Operation 3: Calculate Total Delivery Time - DETAILED BREAKDOWN**

#### **Part 1: Calculate Prep + Pickup Time**
```python
# Subtract two datetime objects
fog_df['picked_datetime'] - fog_df['order_datetime']

# Example:
# picked:  2022-03-13 12:05:00
# order:   2022-03-13 11:55:00
# Result:  Timedelta('0 days 00:10:00')  ← This is a timedelta object
```

#### **Part 2: Convert Timedelta to Minutes**
```python
# Use .dt.total_seconds() to get seconds, then divide by 60
(fog_df['picked_datetime'] - fog_df['order_datetime']).dt.total_seconds() / 60

# Example:
# Timedelta('0 days 00:10:00')
# .dt.total_seconds() → 600 seconds
# / 60 → 10.0 minutes
```

#### **Part 3: Add Delivery Duration**
```python
# delivery_duration is already in minutes (integer)
# Just add it to the prep+pickup time
prep_pickup_minutes + fog_df['delivery_duration']

# Example:
# 10 minutes (prep+pickup) + 42 minutes (driving) = 52 minutes total
```

#### **Complete Calculation:**
```python
fog_df['total_delivery_time'] = (
    (fog_df['picked_datetime'] - fog_df['order_datetime']).dt.total_seconds() / 60  # prep + pickup
    + fog_df['delivery_duration']  # driving time
)

# Visual breakdown:
# (picked - order)           → Timedelta object
# .dt.total_seconds()        → 600 seconds
# / 60                       → 10.0 minutes
# + delivery_duration        → 10.0 + 42 = 52.0 minutes
```

#### **Why the Parentheses?**
```python
# The outer parentheses let you split the expression across multiple lines
fog_df['total_delivery_time'] = (
    line1
    + line2
)

# Without them, Python would think line 1 is complete
```

---

### **Operation 4: Create Boolean Column**
```python
df['is_late'] = df['total_time'] > 45
```

### **Operation 5: Group and Aggregate**
```python
df.groupby('column').agg(
    new_col1=('source_col1', 'count'),
    new_col2=('source_col2', 'sum')
)
```

### **Operation 6: Calculate Percentage**
```python
result['percentage'] = (numerator / denominator * 100).round(2)
```

---

## 🎓 Step 5: Practice Approach

### **Start Small:**
1. Load the data and print first few rows
2. Check data types with `.dtypes`
3. Convert ONE time column to datetime
4. Calculate time difference for ONE row manually
5. Then scale up to all rows

### **Build Incrementally:**
```python
# Step 1: Load
df = pd.read_csv('file.csv')
print(df.head())

# Step 2: Convert times
df['order_datetime'] = pd.to_datetime(...)
print(df[['order_time', 'order_datetime']].head())

# Step 3: Calculate total time
df['total_time'] = ...
print(df[['order_id', 'total_time']].head())

# Step 4: Identify late
df['is_late'] = ...
print(df[['order_id', 'total_time', 'is_late']].head())

# Step 5: Group and aggregate
result = df.groupby(...).agg(...)
print(result)
```

---

## 🧠 Key Concepts to Remember

### **1. String vs Datetime**
- CSV files store everything as strings (text)
- Must convert to datetime to do time math
- Use `pd.to_datetime()` for conversion

### **2. Combining Columns**
- Use `+` to concatenate strings
- `' '` adds a space between date and time
- Format must match your data structure

### **3. Boolean Logic**
- `>` creates True/False values
- `sum()` on boolean treats True=1, False=0
- Perfect for counting "how many are True"

### **4. GroupBy + Agg Pattern**
```python
df.groupby('category').agg(
    count_col=('id', 'count'),    # Count rows
    sum_col=('boolean', 'sum'),   # Sum True values
    avg_col=('number', 'mean')    # Average
)
```

---

## ✅ Self-Check Questions

Before you start coding, ask yourself:

1. **What data types are my time columns?** (Check with `.dtypes`)
2. **Can I subtract strings?** (No! Need datetime)
3. **What's the formula for total delivery time?** (pickup - order + duration)
4. **How do I identify late orders?** (Boolean: total_time > 45)
5. **What am I grouping by?** (road_traffic)
6. **What am I counting?** (Total orders and late orders per group)
7. **How do I calculate percentage?** (late / total × 100)

---

## 🎯 Expected Output

Your final result should look like:

```
road_traffic  total_orders  late_orders  late_percentage
Jam                  5            5           100.00
High                 4            3            75.00
Medium               7            3            42.86
Low                  6            0             0.00
```

---

## 💡 Tips for Success

1. **Print often** - Check your work at each step
2. **Start simple** - Get one thing working before moving on
3. **Use `.head()`** - Look at a few rows to verify
4. **Check data types** - Use `.dtypes` and `type()` frequently
5. **Test on one row** - Manually verify your logic works
6. **Build incrementally** - Don't write everything at once

---

## 🚀 Now Try It Yourself!

Open your notebook and work through the problem step by step. Use this guide as a reference, but try to write the code yourself. Good luck! 🎓
