# 🧠 How to Break Down SQL Problems - A Systematic Approach

## 🎯 The Framework: 5 Questions to Ask

When you see any SQL problem, ask yourself these 5 questions in order:

### **1. What is the FINAL OUTPUT?**
- What columns do I need to show?
- What does each row represent?
- How should it be sorted?

### **2. What GROUPS am I analyzing?**
- Am I looking at data per customer? Per product? Per region?
- Do I need to partition/group the data?

### **3. What CALCULATIONS do I need?**
- Counting? Summing? Averaging?
- Ranking? Finding max/min?
- Date differences? String matching?

### **4. What FILTERS do I need?**
- Do I need specific rows (WHERE)?
- Do I need specific ranks (1st, 2nd, Nth)?
- Do I need to filter after grouping (HAVING)?

### **5. What ORDER of operations?**
- What needs to happen first?
- Can I break this into steps (CTEs)?

---

## 📝 Example: The Airbnb Problem

Let's apply this framework to the Airbnb second booking problem:

### **Original Question:**
> Write a query which outputs the average time taken in days from listing created to second booking for three groups of countries. Round them at 3 decimals.
>
> Group 1 countries should have 'land' in their name, such as England.  
> Group 2 should have countries ending with letter 'a'  
> Group 3 should be the 'Other' countries

---

## 🔍 Step-by-Step Breakdown

### **Question 1: What is the FINAL OUTPUT?**

**Highlight the key words:**
> "outputs the **average time** taken in days... for **three groups of countries**"

**Answer:**
- **Columns needed:**
  - `country_type` (the group name)
  - `avg_days_to_second_booking` (the average)
- **Each row represents:** One country group
- **Expected rows:** 3 rows (Land Countries, Ending A Countries, Other Countries)
- **Sorted:** By average days (descending)

**Write it down:**
```
FINAL OUTPUT:
- 3 rows (one per country group)
- Column 1: country_type
- Column 2: avg_days_to_second_booking (rounded to 3 decimals)
```

---

### **Question 2: What GROUPS am I analyzing?**

**Highlight the key words:**
> "**second booking**" and "**for three groups of countries**"

**Answer:**
- **Primary grouping:** By listing (to find the 2nd booking per listing)
- **Secondary grouping:** By country type (to calculate averages)

**Write it down:**
```
GROUPS:
1. Per listing (to identify 2nd booking)
2. Per country type (to calculate average)
```

---

### **Question 3: What CALCULATIONS do I need?**

**Highlight the key words:**
> "**average time** taken in **days** from **listing created** to **second booking**"

**Answer:**
- **Ranking:** ROW_NUMBER() to identify the 2nd booking per listing
- **Date math:** DATEDIFF(reservation_time, listing_created_at)
- **Aggregation:** AVG() of the days
- **Rounding:** ROUND(..., 3)
- **Categorization:** CASE statement for country groups

**Write it down:**
```
CALCULATIONS:
1. ROW_NUMBER() to rank bookings per listing
2. DATEDIFF() to calculate days
3. CASE to categorize countries
4. AVG() to get average per group
5. ROUND() to 3 decimals
```

---

### **Question 4: What FILTERS do I need?**

**Highlight the key words:**
> "**second booking**"

**Answer:**
- Filter to only rows where `reservation_number = 2`

**Write it down:**
```
FILTERS:
- WHERE reservation_number = 2 (only 2nd bookings)
```

---

### **Question 5: What ORDER of operations?**

**Think about dependencies:**
- Can't calculate days until I know which is the 2nd booking
- Can't find 2nd booking until I rank them
- Can't rank until I join the tables
- Can't average until I categorize
- Can't categorize until I have the days calculated

**Answer:**
```
ORDER OF OPERATIONS:
1. JOIN bookings + listings
2. RANK bookings per listing (ROW_NUMBER)
3. FILTER to 2nd booking only
4. CALCULATE days difference
5. CATEGORIZE countries
6. GROUP BY country type
7. CALCULATE average
```

---

## 🎨 Visual Breakdown Template

Use this template for any SQL problem:

```
┌─────────────────────────────────────────┐
│ PROBLEM: [Write the question here]      │
└─────────────────────────────────────────┘

📊 FINAL OUTPUT:
   Rows: [What does each row represent?]
   Columns: [List them]
   
👥 GROUPS:
   [What am I grouping by?]
   
🧮 CALCULATIONS:
   [What functions do I need?]
   
🔍 FILTERS:
   [What rows do I keep/remove?]
   
📋 ORDER OF OPERATIONS:
   1. [First step]
   2. [Second step]
   ...
```

---

## 🔑 Key Signal Words in SQL Problems

Learn to recognize these trigger words:

### **ROW_NUMBER() Signals:**
- "**Nth** [something]" → 2nd booking, 3rd purchase, 1st login
- "**Most recent**" → ROW_NUMBER() with ORDER BY date DESC
- "**Top N per group**" → ROW_NUMBER() with PARTITION BY
- "**First/Last**" → ROW_NUMBER() = 1 or MAX rank

### **GROUP BY Signals:**
- "**Per** [something]" → per customer, per product, per region
- "**Each** [something]" → each category, each month
- "**Total/Average/Count by** [something]"

### **CASE Signals:**
- "**Categorize/Group into**"
- "**If...then...else**"
- "**Label as**"
- "**Flag as**"

### **JOIN Signals:**
- "**Combine** data from..."
- "**Match** [table A] with [table B]"
- Multiple tables mentioned

### **Date Math Signals:**
- "**Days/Months/Years between**"
- "**Time taken from X to Y**"
- "**Duration**"

---

## 💡 The Airbnb Problem - Annotated

Let me show you how to mark up the original question:

> Write a query which outputs the **[FINAL OUTPUT: AVG]** **[CALC: average]** time taken in **[CALC: days]** from **[CALC: listing created]** to **[FILTER: second]** **[ROW_NUMBER: booking]** for **[GROUP BY: three groups]** of **[GROUP BY: countries]**. **[CALC: Round]** them at **[CALC: 3 decimals]**.
>
> **[CASE: Group 1]** countries should have **[CASE: 'land']** in their name, such as England.  
> **[CASE: Group 2]** should have countries **[CASE: ending with letter 'a']**  
> **[CASE: Group 3]** should be the **[CASE: 'Other']** countries

**After marking it up, you can see:**
- ✅ Need ROW_NUMBER() (for "second booking")
- ✅ Need CASE statement (for categorizing countries)
- ✅ Need GROUP BY (for "three groups")
- ✅ Need AVG() and ROUND() (for "average" and "3 decimals")
- ✅ Need DATEDIFF() (for "days from...to")

---

## 🎯 Practice: Breaking Down New Problems

### **Example Problem 1:**
> "Find the top 3 products by revenue in each category"

**Your turn! Answer these:**
1. **Final Output:** ?
2. **Groups:** ?
3. **Calculations:** ?
4. **Filters:** ?
5. **Order:** ?

<details>
<summary>Click to see the breakdown</summary>

1. **Final Output:** Product name, category, revenue (3 rows per category)
2. **Groups:** Per category
3. **Calculations:** ROW_NUMBER() to rank by revenue, SUM() for revenue
4. **Filters:** WHERE rank <= 3
5. **Order:** 
   - Calculate revenue per product
   - Rank products within each category
   - Filter to top 3

**SQL Pattern:**
```sql
WITH ranked AS (
    SELECT 
        category,
        product,
        SUM(revenue) as total_revenue,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(revenue) DESC) as rn
    FROM sales
    GROUP BY category, product
)
SELECT * FROM ranked WHERE rn <= 3;
```
</details>

---

### **Example Problem 2:**
> "Calculate the percentage of users who made a second purchase within 30 days of their first purchase"

**Your turn! Answer these:**
1. **Final Output:** ?
2. **Groups:** ?
3. **Calculations:** ?
4. **Filters:** ?
5. **Order:** ?

<details>
<summary>Click to see the breakdown</summary>

1. **Final Output:** Single number (percentage)
2. **Groups:** Per user (to find 1st and 2nd purchase)
3. **Calculations:** 
   - ROW_NUMBER() to identify 1st and 2nd purchase
   - DATEDIFF() to calculate days between
   - COUNT() and division for percentage
4. **Filters:** 
   - WHERE rank = 1 or rank = 2
   - WHERE days <= 30
5. **Order:**
   - Rank purchases per user
   - Get 1st and 2nd purchase dates
   - Calculate days between
   - Count users with <= 30 days
   - Divide by total users

</details>

---

## ✅ Checklist: Before You Start Coding

Before writing any SQL, make sure you can answer:

- [ ] What does each row in my final output represent?
- [ ] How many rows should I expect?
- [ ] What columns do I need?
- [ ] Do I need to rank within groups? (ROW_NUMBER?)
- [ ] Do I need to aggregate? (SUM, AVG, COUNT?)
- [ ] Do I need to categorize? (CASE?)
- [ ] What's the logical order of operations?
- [ ] Can I break this into 2-3 clear steps?

---

## 🚀 The Universal SQL Problem-Solving Pattern

Once you've broken down the problem, most SQL solutions follow this pattern:

```sql
-- STEP 1: Prepare the data (JOIN, basic calculations)
WITH step1 AS (
    SELECT ...
    FROM table1
    JOIN table2 ON ...
),

-- STEP 2: Rank or partition if needed
step2 AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) as rn
    FROM step1
),

-- STEP 3: Filter to what you need
step3 AS (
    SELECT ...
    FROM step2
    WHERE rn = 1  -- or whatever filter
)

-- STEP 4: Final aggregation and formatting
SELECT 
    CASE ... END as category,
    ROUND(AVG(...), 3) as metric
FROM step3
GROUP BY 1
ORDER BY 2 DESC;
```

---

## 💭 Summary

**The key to breaking down SQL problems:**

1. **Read slowly** - highlight key words
2. **Ask the 5 questions** - write down answers
3. **Identify signal words** - ROW_NUMBER, GROUP BY, CASE, etc.
4. **Map the flow** - what order do operations need to happen?
5. **Start simple** - build the query step by step

**Remember:** Every complex SQL query is just simple steps chained together. Break it down, and it becomes manageable! 🎯
