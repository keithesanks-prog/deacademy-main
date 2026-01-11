# 🔀 When to Use CASE Statements - Recognition Guide

## 🎯 The Core Question

**Ask yourself:** 
> "Does the problem want me to **create new categories** or **transform values** based on conditions?"

If **YES** → You need a CASE statement!

---

## � Real SQL Interview Questions That Need CASE

Here are actual interview-style questions where CASE is necessary. I've **highlighted the trigger words** in each.

### **🟢 Easy - Recognizing CASE Needs**

#### **Question 1:**
> "Write a query to **categorize** products as 'Expensive' if price > $100, 'Moderate' if price between $50-$100, and 'Cheap' otherwise."

**Trigger words:** ✅ "categorize", "if...otherwise"  
**Need CASE?** YES - Creating price categories

---

#### **Question 2:**
> "For each employee, **create a flag** called 'senior_status' that shows 'Senior' if they have 5+ years of experience, else 'Junior'."

**Trigger words:** ✅ "create a flag", "if...else"  
**Need CASE?** YES - Creating binary flag based on condition

---

#### **Question 3:**
> "**Label** each order as 'Weekend Order' if placed on Saturday/Sunday, otherwise 'Weekday Order'."

**Trigger words:** ✅ "label", "if...otherwise"  
**Need CASE?** YES - Creating labels based on day of week

---

#### **Question 4:**
> "Calculate total revenue per region and **classify** each region as 'High Revenue' (>$1M), 'Medium Revenue' ($500K-$1M), or 'Low Revenue' (<$500K)."

**Trigger words:** ✅ "classify", explicit categories  
**Need CASE?** YES - Creating revenue tiers

---

#### **Question 5:**
> "**Segment** customers into 'Active' if they made a purchase in the last 30 days, 'Inactive' if last purchase was 30-90 days ago, and 'Churned' if more than 90 days."

**Trigger words:** ✅ "segment", explicit categories  
**Need CASE?** YES - Creating engagement segments

---

### **🟡 Medium - Multi-Condition CASE**

#### **Question 6:**
> "For each country, calculate average salary and **create a column named 'income_level'** with values 'High Income' for countries where avg salary > $80K, 'Middle Income' for $40K-$80K, and 'Low Income' for < $40K."

**Trigger words:** ✅ "create a column named X", "with values Y, Z, W"  
**Need CASE?** YES - Creating income level categories

---

#### **Question 7:**
> "Write a query to **flag** transactions as 'Potential Fraud' if amount > $10,000 AND location is different from customer's home country, otherwise 'Normal'."

**Trigger words:** ✅ "flag", "if...otherwise", multiple conditions  
**Need CASE?** YES - Creating fraud flags with AND logic

---

#### **Question 8:**
> "**Group** movies into genres: 'Action' if title contains 'fight' or 'war', 'Romance' if contains 'love', 'Comedy' if contains 'funny', else 'Other'."

**Trigger words:** ✅ "group into", pattern matching  
**Need CASE?** YES - Categorizing based on text patterns

---

#### **Question 9:**
> "For each student, calculate their average grade and **assign a letter grade**: 'A' for 90-100, 'B' for 80-89, 'C' for 70-79, 'D' for 60-69, 'F' for below 60."

**Trigger words:** ✅ "assign", range buckets  
**Need CASE?** YES - Creating grade buckets

---

#### **Question 10:**
> "**Categorize** each hour of the day as 'Morning' (6-11), 'Afternoon' (12-17), 'Evening' (18-21), or 'Night' (22-5)."

**Trigger words:** ✅ "categorize", time ranges  
**Need CASE?** YES - Creating time period buckets

---

### **🔴 Hard - Complex CASE Logic**

#### **Question 11:**
> "For each listing, calculate days to second booking and **create a country_type flag** with values 'Land Countries' for countries containing 'land', 'Ending A Countries' for countries ending with 'a', and 'Other Countries' for the rest. Then calculate average days per country type."

**Trigger words:** ✅ "create a flag", "with values X, Y, Z", pattern matching  
**Need CASE?** YES - This is the Airbnb problem!

---

#### **Question 12:**
> "**Classify** each sale as 'Upsell' if customer bought a more expensive product than their previous purchase, 'Repeat' if same price range, 'Downsell' if cheaper, or 'First Purchase' if no previous purchase."

**Trigger words:** ✅ "classify", comparing to previous state  
**Need CASE?** YES - Creating purchase type categories

---

#### **Question 13:**
> "For each user, **create a loyalty_tier** column: 'Platinum' if total_spend > $10K AND orders > 50, 'Gold' if total_spend > $5K OR orders > 30, 'Silver' if total_spend > $1K, else 'Bronze'."

**Trigger words:** ✅ "create a column", complex AND/OR logic  
**Need CASE?** YES - Creating tiers with nested conditions

---

#### **Question 14:**
> "**Segment** products by performance: 'Star' if revenue > average AND units_sold > average, 'High Revenue' if only revenue > average, 'High Volume' if only units_sold > average, else 'Underperformer'."

**Trigger words:** ✅ "segment", multiple metric comparisons  
**Need CASE?** YES - Creating performance matrix categories

---

#### **Question 15:**
> "For each employee, **assign a bonus tier**: 'Tier 1' (20% bonus) if performance_score > 90 AND tenure > 3 years, 'Tier 2' (15% bonus) if performance_score > 80 OR tenure > 5 years, 'Tier 3' (10% bonus) if performance_score > 70, else 'No Bonus'."

**Trigger words:** ✅ "assign", complex conditions with AND/OR  
**Need CASE?** YES - Creating bonus tiers with nested logic

---

## 🎯 Pattern Recognition Summary

After reading these questions, you should notice:

### **🔴 RED FLAGS (100% need CASE):**
- "Create a column named X with values Y, Z, W"
- "Create a flag called..."
- "Assign [categories]"

### **🟠 ORANGE FLAGS (90% need CASE):**
- "Categorize/Classify/Label/Segment/Flag"
- "Group into [specific categories]"
- Explicit category names given in quotes

### **🟡 YELLOW FLAGS (75% need CASE):**
- "If...then...else" logic
- "Based on [condition]"
- Range descriptions (0-10, 10-20, etc.)
- Pattern matching (contains, starts with, ends with)

---

## �🚨 Signal Words That Scream "CASE!"

### **🔹 Direct CASE Signals (90% certainty)**

| Signal Word/Phrase | Example | What it means |
|-------------------|---------|---------------|
| **"Categorize"** | "Categorize customers as..." | Create groups/labels |
| **"Group into"** | "Group countries into 3 types" | Create categories |
| **"Label as"** | "Label transactions as fraud/safe" | Assign labels |
| **"Flag as"** | "Flag orders as urgent/normal" | Create binary/multi flags |
| **"Classify"** | "Classify products by price range" | Put into buckets |
| **"Create a column named X with values Y, Z"** | "Create country_type with 'Land', 'Ending A', 'Other'" | Explicit CASE needed |

### **🔹 Conditional Logic Signals (80% certainty)**

| Signal Word/Phrase | Example | What it means |
|-------------------|---------|---------------|
| **"If...then...else"** | "If price > 100 then 'expensive' else 'cheap'" | Conditional logic |
| **"Based on"** | "Based on salary, assign tier" | Condition-based assignment |
| **"Depending on"** | "Depending on age, categorize users" | Conditional categorization |
| **"When...should be"** | "When country has 'land', should be 'Land Countries'" | Conditional assignment |
| **"For X, use Y; for Z, use W"** | "For USA use 'Domestic', for others use 'International'" | Multiple conditions |

### **🔹 Bucketing/Binning Signals (75% certainty)**

| Signal Word/Phrase | Example | What it means |
|-------------------|---------|---------------|
| **"Range"** | "Age ranges: 0-18, 19-65, 65+" | Create buckets |
| **"Tier"** | "Create price tiers: low/medium/high" | Stratify data |
| **"Segment"** | "Segment customers by spend" | Create segments |
| **"Bucket"** | "Bucket sales into quartiles" | Group into bins |

---

## 📋 The Airbnb Problem - Annotated

Let me show you the EXACT words that should trigger "I need CASE":

> Write a query which outputs the average time taken in days from listing created to second booking for **three groups** of countries.
>
> **Group 1** countries should have 'land' as character in their name, such as England.  
> **Group 2** should have countries ending with letter 'a'  
> **Group 3** should be the 'Other' countries  
> Using the above criteria, **create a flag** with the column named **country_type** and the values being **'Land Countries', 'Ending A Countries', or 'Other Countries'**

### **🚨 CASE Triggers Found:**

1. ✅ **"three groups"** → Creating categories
2. ✅ **"Group 1... Group 2... Group 3"** → Multiple conditions
3. ✅ **"create a flag"** → Direct CASE signal
4. ✅ **"column named country_type"** → New column with custom values
5. ✅ **"values being 'X', 'Y', or 'Z'"** → Explicit value assignment
6. ✅ **"should have/should be"** → Conditional logic

**Conclusion:** This problem is SCREAMING for a CASE statement! 🔊

---

## 🎓 Practice: Spot the CASE

### **Example 1:**
> "Calculate total revenue per product and label products as 'High Performer' if revenue > $10,000, otherwise 'Low Performer'"

**Your analysis:**
- Signal words: **"label"**, **"if...otherwise"**
- Need CASE? **YES** ✅
- Why? Creating labels based on conditions

<details>
<summary>Solution</summary>

```sql
SELECT 
    product,
    SUM(revenue) as total_revenue,
    CASE 
        WHEN SUM(revenue) > 10000 THEN 'High Performer'
        ELSE 'Low Performer'
    END AS performance_label
FROM sales
GROUP BY product;
```
</details>

---

### **Example 2:**
> "Find the average order value per customer"

**Your analysis:**
- Signal words: None related to CASE
- Need CASE? **NO** ❌
- Why? Just aggregation, no categorization

<details>
<summary>Solution</summary>

```sql
SELECT 
    customer_id,
    AVG(order_value) as avg_order_value
FROM orders
GROUP BY customer_id;
```
</details>

---

### **Example 3:**
> "Segment users into age groups: 'Youth' (0-17), 'Adult' (18-64), 'Senior' (65+)"

**Your analysis:**
- Signal words: **"Segment"**, **"age groups"**, explicit categories
- Need CASE? **YES** ✅
- Why? Creating age buckets with custom labels

<details>
<summary>Solution</summary>

```sql
SELECT 
    user_id,
    age,
    CASE 
        WHEN age BETWEEN 0 AND 17 THEN 'Youth'
        WHEN age BETWEEN 18 AND 64 THEN 'Adult'
        ELSE 'Senior'
    END AS age_group
FROM users;
```
</details>

---

### **Example 4:**
> "For each region, calculate total sales. Classify regions as 'Top Tier' if sales > $1M, 'Mid Tier' if sales between $500K-$1M, otherwise 'Low Tier'"

**Your analysis:**
- Signal words: **"Classify"**, **"if...otherwise"**, explicit tiers
- Need CASE? **YES** ✅
- Why? Creating tiers based on sales ranges

<details>
<summary>Solution</summary>

```sql
SELECT 
    region,
    SUM(sales) as total_sales,
    CASE 
        WHEN SUM(sales) > 1000000 THEN 'Top Tier'
        WHEN SUM(sales) BETWEEN 500000 AND 1000000 THEN 'Mid Tier'
        ELSE 'Low Tier'
    END AS tier
FROM sales_data
GROUP BY region;
```
</details>

---

### **Example 5:**
> "Count the number of orders per day"

**Your analysis:**
- Signal words: None related to CASE
- Need CASE? **NO** ❌
- Why? Simple aggregation, no categorization

<details>
<summary>Solution</summary>

```sql
SELECT 
    DATE(order_date) as day,
    COUNT(*) as order_count
FROM orders
GROUP BY DATE(order_date);
```
</details>

---

## 🔍 Decision Tree

```
Does the problem ask you to:
│
├─ Create new categories/groups? ────────────────────────► YES → CASE
│
├─ Assign labels/flags based on conditions? ─────────────► YES → CASE
│
├─ Transform values (if X then Y, else Z)? ──────────────► YES → CASE
│
├─ Create buckets/ranges/tiers? ─────────────────────────► YES → CASE
│
├─ Just calculate/aggregate existing data? ──────────────► NO → No CASE needed
│
└─ Just filter/join/rank data? ──────────────────────────► NO → No CASE needed
```

---

## 📝 Common CASE Patterns

### **Pattern 1: Simple Binary Flag**
```sql
CASE 
    WHEN condition THEN 'Yes'
    ELSE 'No'
END AS flag_name
```

**Example:** Flag expensive products
```sql
CASE 
    WHEN price > 100 THEN 'Expensive'
    ELSE 'Affordable'
END AS price_category
```

---

### **Pattern 2: Multiple Categories**
```sql
CASE 
    WHEN condition1 THEN 'Category A'
    WHEN condition2 THEN 'Category B'
    WHEN condition3 THEN 'Category C'
    ELSE 'Other'
END AS category_name
```

**Example:** The Airbnb problem
```sql
CASE 
    WHEN LOWER(country) LIKE '%land%' THEN 'Land Countries'
    WHEN LOWER(country) LIKE '%a' THEN 'Ending A Countries'
    ELSE 'Other Countries'
END AS country_type
```

---

### **Pattern 3: Range Bucketing**
```sql
CASE 
    WHEN value BETWEEN low1 AND high1 THEN 'Bucket 1'
    WHEN value BETWEEN low2 AND high2 THEN 'Bucket 2'
    ELSE 'Bucket 3'
END AS bucket_name
```

**Example:** Age groups
```sql
CASE 
    WHEN age BETWEEN 0 AND 17 THEN 'Youth'
    WHEN age BETWEEN 18 AND 64 THEN 'Adult'
    ELSE 'Senior'
END AS age_group
```

---

### **Pattern 4: Text Pattern Matching**
```sql
CASE 
    WHEN column LIKE 'pattern1%' THEN 'Type A'
    WHEN column LIKE '%pattern2' THEN 'Type B'
    WHEN column LIKE '%pattern3%' THEN 'Type C'
    ELSE 'Type D'
END AS type_name
```

**Example:** Email domain categorization
```sql
CASE 
    WHEN email LIKE '%@gmail.com' THEN 'Gmail'
    WHEN email LIKE '%@yahoo.com' THEN 'Yahoo'
    WHEN email LIKE '%@company.com' THEN 'Corporate'
    ELSE 'Other'
END AS email_type
```

---

## ⚠️ When NOT to Use CASE

### **❌ Don't use CASE when:**

1. **You're just filtering data**
   ```sql
   -- WRONG: Using CASE in WHERE
   WHERE CASE WHEN status = 'active' THEN 1 ELSE 0 END = 1
   
   -- RIGHT: Direct condition
   WHERE status = 'active'
   ```

2. **You're just aggregating**
   ```sql
   -- Don't need CASE for simple aggregation
   SELECT region, SUM(sales)
   FROM sales_data
   GROUP BY region;
   ```

3. **You're just joining tables**
   ```sql
   -- No CASE needed for joins
   SELECT *
   FROM orders O
   JOIN customers C ON O.customer_id = C.id;
   ```

---

## ✅ Quick Checklist

Before writing a CASE statement, verify:

- [ ] Am I creating **new categories** that don't exist in the data?
- [ ] Am I **transforming values** based on conditions?
- [ ] Does the problem explicitly mention **"if...then"** logic?
- [ ] Do I see words like "categorize", "label", "flag", "classify"?
- [ ] Am I creating **buckets/ranges/tiers**?

If you answered **YES** to any of these → Use CASE!

---

## 🎯 Real-World CASE Examples

### **E-commerce:**
- Categorize customers by lifetime value (VIP, Regular, New)
- Flag orders as "Rush" or "Standard" based on shipping preference
- Segment products by price range

### **Finance:**
- Classify transactions as "Fraud Risk" based on amount/location
- Create credit score tiers (Excellent, Good, Fair, Poor)
- Label accounts as "Active", "Dormant", "Closed"

### **Analytics:**
- Bucket users by engagement level (High, Medium, Low)
- Categorize time periods (Morning, Afternoon, Evening, Night)
- Flag anomalies based on thresholds

---

## 💡 Pro Tips

### **Tip 1: Order Matters**
```sql
-- WRONG: 'Other' will never be reached
CASE 
    WHEN country LIKE '%a' THEN 'Ending A'
    WHEN country = 'India' THEN 'India Specific'  -- India already matched above!
END

-- RIGHT: Most specific conditions first
CASE 
    WHEN country = 'India' THEN 'India Specific'
    WHEN country LIKE '%a' THEN 'Ending A'
END
```

### **Tip 2: Always Include ELSE**
```sql
-- RISKY: What if no condition matches? Returns NULL
CASE 
    WHEN age < 18 THEN 'Minor'
    WHEN age < 65 THEN 'Adult'
END

-- SAFE: Catches everything else
CASE 
    WHEN age < 18 THEN 'Minor'
    WHEN age < 65 THEN 'Adult'
    ELSE 'Senior'
END
```

### **Tip 3: Use LOWER() for Text Matching**
```sql
-- RISKY: Won't match "ENGLAND" or "England"
WHEN country LIKE '%land%'

-- SAFE: Matches any case
WHEN LOWER(country) LIKE '%land%'
```

---

## 🎓 Summary

**You need CASE when the problem asks you to:**
1. ✅ Create categories/groups
2. ✅ Assign labels/flags
3. ✅ Transform values conditionally
4. ✅ Create buckets/ranges/tiers

**Signal words to watch for:**
- Categorize, classify, label, flag, segment
- If...then...else, based on, depending on
- Create a column with values X, Y, Z
- Group into, ranges, tiers

**Remember:** If you're creating something NEW that doesn't exist in the raw data, you probably need CASE! 🚀
