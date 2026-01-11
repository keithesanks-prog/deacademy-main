# Data Modeling for Business Intelligence: Yelp Restaurant Reviews

## 🎯 Learning Objectives

By the end of this guide, you'll understand:
- How to identify fact vs dimension tables
- Star schema design principles
- Key BI metrics and how to model them
- Common data modeling patterns for analytics
- How to design for query performance

---

## 📊 The Business Context: Yelp Restaurant Reviews

**Business Questions We Need to Answer:**
- Which restaurants have the highest ratings?
- What are the review trends over time?
- Which users are most active reviewers?
- How do restaurant attributes affect ratings?
- What are the geographic patterns in reviews?

---

## 🏗️ Schema Overview

```dbml
Table dim_users {
  user_id varchar [pk]
  user_name varchar
  yelping_since datetime
  first_name varchar
  last_name varchar
  gender varchar
  email_id varchar
  phone_number int
  birth_date date
  age int
  country_code varchar
  country varchar
  state varchar
  postal_code varchar
}

Table dim_country {
  country_code varchar [pk]
  country varchar
  state varchar
  city varchar
  postal_code varchar
}

Table dim_restaurant {
  restaurant_id varchar [pk]
  restaurant_name varchar
  restaurant_start_date date
  restaurant_address varchar
  restaurant_county_code varchar
  restaurant_country varchar
  restaurant_state varchar
  restaurant_city varchar
  restaurant_postal_code varchar
  latitude varchar
  longitude varchar
}

Table fact_review {
  review_id varchar [pk]
  session_id varchar
  user_id varchar [ref: > dim_users.user_id]
  restaurant_id varchar [ref: > dim_restaurant.restaurant_id]
  review_date date
  review_time time
  type varchar
  score int
  tags varchar
  useful int
  summary varchar
  review_text varchar
}

Table fact_restaurant_attributes {
  restaurant_id varchar [pk, ref: > dim_restaurant.restaurant_id]
  bike_parking boolean
  accepts_bitcoin boolean
  accepts_credit_cards boolean
  garage_parking boolean
  street_parking boolean
  dogs_allowed boolean
  price_range varchar
  wheel_chair_accessible boolean
  valet_parking boolean
  parking_lot boolean
}
```

---

## 🎯 How to Think About Metrics (The Most Important Skill!)

### The Framework: Ask "What Do We Want to COUNT, SUM, or AVERAGE?"

When looking at any data model, ask yourself these questions:

#### 1. **What are we COUNTING?**
These become your **COUNT metrics**:
- Number of reviews
- Number of users  
- Number of restaurants
- Number of reviews per user
- Number of reviews per restaurant

**How to spot them**: Look for things that happen multiple times (events, transactions)

#### 2. **What are we MEASURING?**
These become your **SUM/AVG metrics**:
- Average review score
- Total "useful" votes
- Average age of reviewers
- Percentage of 5-star reviews

**How to spot them**: Look for numeric columns in fact tables (score, useful, etc.)

#### 3. **What are we COMPARING?**
These become your **GROUP BY dimensions**:
- Reviews by restaurant
- Reviews by user
- Reviews by geography (country, state, city)
- Reviews by time (year, month, day)
- Reviews by restaurant attributes (has parking, accepts bitcoin, etc.)

**How to spot them**: Look at dimension table attributes and fact table foreign keys

---

## 🧠 The Mental Model: "Slicing and Dicing"

Think of your data like a Rubik's cube - you can look at it from different angles:

### Example: Review Score (The Metric)

**Slice by Restaurant:**
```sql
-- "Which restaurants have the highest average rating?"
SELECT restaurant_name, AVG(score)
FROM fact_review
GROUP BY restaurant_name
```

**Slice by User:**
```sql
-- "Which users give the harshest ratings?"
SELECT user_name, AVG(score)
FROM fact_review
GROUP BY user_name
```

**Slice by Geography:**
```sql
-- "Which states have the highest-rated restaurants?"
SELECT state, AVG(score)
FROM fact_review
JOIN dim_restaurant ON ...
GROUP BY state
```

**Slice by Time:**
```sql
-- "Are ratings improving over time?"
SELECT YEAR(review_date), AVG(score)
FROM fact_review
GROUP BY YEAR(review_date)
```

**The Pattern**: Same metric (AVG score), different dimensions (restaurant, user, geography, time)

---

## 📊 Metric Categories in This Schema

### Core Business Metrics

**1. Review Volume Metrics**
- Total reviews
- Reviews per restaurant
- Reviews per user
- Reviews per day/month/year

**Why they matter**: Indicates platform engagement and growth

**2. Quality Metrics**
- Average review score
- Percentage of 5-star reviews
- Percentage of 1-star reviews
- Distribution of scores (1-5)

**Why they matter**: Indicates customer satisfaction and restaurant quality

**3. Engagement Metrics**
- "Useful" votes per review
- Reviews with text vs without
- Average review length
- Reviews with tags

**Why they matter**: Indicates review quality and user engagement

**4. User Behavior Metrics**
- Reviews per user (activity level)
- Average score given by user (harsh vs generous)
- User tenure (time since yelping_since)
- Geographic distribution of users

**Why they matter**: Understand user segments and behavior patterns

**5. Restaurant Attribute Metrics**
- Correlation between attributes and ratings
  - Do restaurants with bike parking get higher ratings?
  - Do restaurants accepting bitcoin get more reviews?
  - Does wheelchair accessibility affect ratings?

**Why they matter**: Identify features that drive customer satisfaction

---

## 🔍 How to Identify Missing Metrics

### Ask These Questions:

**1. "What decisions will this data support?"**
- Should a restaurant add bike parking? → Need: bike_parking vs avg_rating
- Which cities should we expand to? → Need: reviews by city, avg_rating by city
- Are new users more active? → Need: reviews by user tenure

**2. "What's missing from the current schema?"**

Looking at our schema, we're missing:
- ❌ **Time dimension**: No easy way to analyze trends over time
- ❌ **Review response time**: How long until restaurant responds?
- ❌ **User loyalty**: Repeat reviews of same restaurant
- ❌ **Competitive metrics**: How does this restaurant compare to others nearby?

**3. "What would a dashboard show?"**

Imagine a Yelp analytics dashboard. What charts would you see?
- Top 10 restaurants by rating → Need: restaurant_name, avg_score
- Review trends over time → Need: date dimension, review_count
- User activity heatmap → Need: user_id, review_count, last_review_date
- Geographic distribution → Need: state/city, review_count

---

## 💡 Practical Exercise: Identify Metrics

For each business question, identify:
1. The metric (what you're measuring)
2. The dimension (how you're slicing it)
3. The tables you need

### Question 1: "Which restaurants improved the most this year?"
- **Metric**: Change in average rating
- **Dimension**: Restaurant, time (year)
- **Tables**: fact_review, dim_restaurant
- **SQL Pattern**: 
  ```sql
  AVG(score) in 2024 - AVG(score) in 2023
  GROUP BY restaurant_name
  ```

### Question 2: "Do female users give higher ratings than male users?"
- **Metric**: Average score
- **Dimension**: Gender
- **Tables**: fact_review, dim_users
- **SQL Pattern**:
  ```sql
  AVG(score)
  GROUP BY gender
  ```

### Question 3: "What percentage of restaurants accept credit cards?"
- **Metric**: Count of restaurants
- **Dimension**: accepts_credit_cards (boolean)
- **Tables**: fact_restaurant_attributes
- **SQL Pattern**:
  ```sql
  COUNT(*) / (SELECT COUNT(*) FROM fact_restaurant_attributes)
  WHERE accepts_credit_cards = true
  ```

---

## 🔍 Identifying Fact vs Dimension Tables

### Dimension Tables (The "Who, What, Where, When")

**dim_users** - Describes WHO is reviewing
- **Purpose**: User demographics and profile information
- **Grain**: One row per user
- **Type**: Slowly Changing Dimension (SCD Type 2 candidate)
- **Key Attributes**: Demographics (age, gender), location, tenure (yelping_since)

**dim_restaurant** - Describes WHAT is being reviewed
- **Purpose**: Restaurant details and location
- **Grain**: One row per restaurant
- **Type**: SCD Type 2 (restaurants can change location, name)
- **Key Attributes**: Name, location (address, lat/long), start date

**dim_country** - Describes WHERE (geographic hierarchy)
- **Purpose**: Geographic reference data
- **Grain**: One row per country/state/city/postal code combination
- **Type**: Static reference dimension
- **Key Attributes**: Geographic hierarchy for rollups

### Fact Tables (The "Measurements")

**fact_review** - The EVENTS (reviews happening)
- **Purpose**: Captures review transactions
- **Grain**: One row per review
- **Type**: Transaction fact table
- **Measures**: score, useful count
- **Dimensions**: user_id, restaurant_id, review_date, review_time

**fact_restaurant_attributes** - The SNAPSHOT (current state)
- **Purpose**: Current restaurant features/amenities
- **Grain**: One row per restaurant
- **Type**: Factless fact table (mostly boolean attributes)
- **Measures**: Boolean flags (can be counted/aggregated)

---

## 🎯 Key BI Metrics & How to Calculate Them

### 1. Average Restaurant Rating
```sql
SELECT 
    r.restaurant_name,
    AVG(fr.score) AS avg_rating,
    COUNT(fr.review_id) AS review_count
FROM fact_review fr
JOIN dim_restaurant r ON fr.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_name
ORDER BY avg_rating DESC;
```

### 2. Most Active Reviewers
```sql
SELECT 
    u.user_name,
    u.yelping_since,
    COUNT(fr.review_id) AS total_reviews,
    AVG(fr.score) AS avg_score_given
FROM fact_review fr
JOIN dim_users u ON fr.user_id = u.user_id
GROUP BY u.user_name, u.yelping_since
ORDER BY total_reviews DESC;
```

### 3. Reviews by Geographic Region
```sql
SELECT 
    c.country,
    c.state,
    COUNT(fr.review_id) AS review_count,
    AVG(fr.score) AS avg_rating
FROM fact_review fr
JOIN dim_restaurant r ON fr.restaurant_id = r.restaurant_id
JOIN dim_country c ON r.restaurant_county_code = c.country_code
GROUP BY c.country, c.state
ORDER BY review_count DESC;
```

### 4. Restaurant Attributes Impact on Ratings
```sql
SELECT 
    CASE WHEN fra.bike_parking THEN 'Has Bike Parking' ELSE 'No Bike Parking' END AS parking_type,
    AVG(fr.score) AS avg_rating,
    COUNT(DISTINCT fr.restaurant_id) AS restaurant_count
FROM fact_review fr
JOIN fact_restaurant_attributes fra ON fr.restaurant_id = fra.restaurant_id
GROUP BY fra.bike_parking;
```

---

## 🚨 Data Modeling Issues to Fix

### Issue 1: Redundant Geography Data
**Problem**: `dim_users` and `dim_restaurant` both have country, state, postal_code columns

**Better Design**: Use `dim_country` as the single source of truth
```dbml
-- BEFORE (Redundant)
Table dim_users {
  country_code varchar
  country varchar  -- ❌ Redundant
  state varchar    -- ❌ Redundant
  postal_code varchar
}

-- AFTER (Normalized)
Table dim_users {
  user_id varchar [pk]
  country_code varchar [ref: > dim_country.country_code]
  -- Remove country, state - get from dim_country via join
}
```

### Issue 2: Data Type Inconsistencies
**Problem**: 
- `latitude` and `longitude` are VARCHAR (should be DECIMAL/FLOAT)
- `phone_number` is INT (should be VARCHAR to preserve leading zeros)
- `age` is stored (should be calculated from birth_date)

**Fix**:
```dbml
Table dim_restaurant {
  latitude decimal(10, 8)   -- ✅ Proper geo type
  longitude decimal(11, 8)  -- ✅ Proper geo type
}

Table dim_users {
  phone_number varchar      -- ✅ Preserve formatting
  birth_date date           -- ✅ Store DOB
  -- Remove age column, calculate in queries
}
```

### Issue 3: Grain Mismatch in dim_country
**Problem**: `dim_country` has country, state, city, postal_code all in one row - unclear grain

**Better Design**: Create a proper geographic hierarchy
```dbml
Table dim_geography {
  geo_key int [pk]
  postal_code varchar
  city varchar
  state varchar
  country varchar
  country_code varchar
}
-- Grain: One row per postal code (finest level)
```

---

## 📈 Star Schema Design Pattern

```
         dim_users                    dim_restaurant
             |                              |
             |                              |
             +--------fact_review-----------+
                          |
                          |
                    dim_country
                    
                    
         fact_restaurant_attributes
                    |
                    |
              dim_restaurant
```

**Why This Works:**
- ✅ Fact tables in the center (reviews, attributes)
- ✅ Dimension tables around the edges
- ✅ Foreign keys point from facts to dimensions
- ✅ Enables simple, fast queries with star joins

---

## 🔄 Slowly Changing Dimensions (SCD)

### SCD Type 1: Overwrite (No History)
**Use for**: Minor corrections, non-critical changes
```sql
-- Example: User changes email
UPDATE dim_users 
SET email_id = 'newemail@example.com'
WHERE user_id = 'U123';
-- Old email is lost
```

### SCD Type 2: Add New Row (Track History)
**Use for**: Important changes you need to track
```dbml
Table dim_restaurant_scd2 {
  restaurant_key int [pk]        -- Surrogate key
  restaurant_id varchar          -- Natural key
  restaurant_name varchar
  restaurant_address varchar
  effective_date date
  expiration_date date
  is_current boolean
}
```

**Example**: Restaurant moves locations
```sql
-- Old record
INSERT INTO dim_restaurant_scd2 VALUES
(1, 'R001', 'Pizza Place', '123 Old St', '2020-01-01', '2024-12-31', false);

-- New record (current)
INSERT INTO dim_restaurant_scd2 VALUES
(2, 'R001', 'Pizza Place', '456 New Ave', '2025-01-01', '9999-12-31', true);
```

---

## 💡 Best Practices for BI Data Models

### 1. Use Surrogate Keys
```dbml
Table dim_users {
  user_key int [pk]          -- ✅ Surrogate (auto-increment)
  user_id varchar [unique]   -- ✅ Natural key (from source)
}
```

### 2. Denormalize for Performance
```sql
-- Instead of joining 3 tables for every query:
SELECT u.country, u.state, u.city  -- ✅ Fast
FROM dim_users u;

-- Better than:
SELECT c.country, c.state, c.city  -- ❌ Slower
FROM dim_users u
JOIN dim_country c ON u.country_code = c.country_code;
```

### 3. Add Date Dimensions
```dbml
Table dim_date {
  date_key int [pk]
  full_date date
  year int
  quarter int
  month int
  month_name varchar
  day_of_week int
  day_name varchar
  is_weekend boolean
  is_holiday boolean
}
```

### 4. Pre-Aggregate for Common Queries
```dbml
Table fact_restaurant_daily_summary {
  restaurant_id varchar
  review_date date
  review_count int
  avg_score decimal
  total_useful int
}
-- Grain: One row per restaurant per day
```

---

## 🎓 Practice Exercises

### Exercise 1: Identify the Grain
For each table, state the grain (one row represents...):
- `fact_review`: _______________
- `dim_users`: _______________
- `fact_restaurant_attributes`: _______________

### Exercise 2: Design a Query
Write SQL to answer: "What percentage of 5-star reviews mention 'great service' in the review text?"

### Exercise 3: Add a Dimension
Design a `dim_time` table to complement `fact_review.review_time`. What columns would you include?

### Exercise 4: Identify SCD Type
Which SCD type would you use for:
- User's age? _______________
- Restaurant's name? _______________
- User's email? _______________

---

## 📚 Key Takeaways

1. **Fact tables** store measurements/events (reviews, transactions)
2. **Dimension tables** store descriptive attributes (who, what, where)
3. **Star schema** = Facts in center, dimensions around edges
4. **Grain** = What one row represents (be specific!)
5. **SCD** = How you handle changes over time
6. **Denormalize** dimensions for query performance
7. **Use surrogate keys** for flexibility

---

## 🔗 Related Resources

- [Star Schema Design Guide](star_schema_design_guide.html)
- [SCD Types Guide](scd_types_guide.md)
- [DBML Syntax Guide](dbml_syntax_guide.md)
- [Dimensional Modeling Guide](dimensional_modeling_guide.md)
