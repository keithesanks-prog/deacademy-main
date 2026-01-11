# Yelp Fake Review Detection - Data Model Guide

## 🚨 The Problem

**Yelp is facing an issue with fake reviews.** The goal is to find:
1. Reviewers who are fake
2. Restaurants that may have hired fake reviewers

## 🎯 What Metrics Actually Help Detect Fraud?

### ❌ What DOESN'T Help
- Bike parking vs ratings
- Restaurant attributes vs satisfaction
- General engagement metrics

### ✅ What DOES Help

#### 1. Suspicious User Behavior Patterns

**Review Velocity**
- Normal: 0-2 reviews per day
- Suspicious: 10+ reviews per day
```sql
SELECT user_id, 
       COUNT(*) / DATEDIFF(MAX(review_date), MIN(review_date)) AS reviews_per_day
FROM fact_review
GROUP BY user_id
HAVING reviews_per_day > 5
```

**Score Variance**
- Normal: StdDev of 1-2 (mix of ratings)
- Suspicious: StdDev of 0 (all 5-stars or all 1-stars)
```sql
SELECT user_id,
       STDDEV(score) AS score_variance,
       AVG(score) AS avg_score
FROM fact_review
GROUP BY user_id
HAVING score_variance < 0.5
```

**Review Length**
- Normal: 100+ characters
- Suspicious: <20 characters (generic "Great!" or "Terrible!")
```sql
SELECT user_id,
       AVG(LENGTH(review_text)) AS avg_length
FROM fact_review
GROUP BY user_id
HAVING avg_length < 20
```

**Account Age at First Review**
- Normal: Days/weeks after signup
- Suspicious: 0-1 days (immediate activity)

#### 2. Suspicious Restaurant Patterns

**Review Spike**
- Normal: Gradual growth
- Suspicious: 50+ reviews in 1 week
```sql
SELECT restaurant_id,
       COUNT(CASE WHEN review_date > DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) AS reviews_last_week,
       COUNT(*) AS total_reviews
FROM fact_review
GROUP BY restaurant_id
HAVING reviews_last_week > total_reviews * 0.5
```

**New Reviewer Ratio**
- Suspicious: >50% of reviews from accounts <30 days old

**Review Timing**
- Suspicious: Multiple reviews at exact same timestamp

#### 3. Network Analysis

**Reviewer Clusters**
- Groups of users who always review together
```sql
WITH user_pairs AS (
    SELECT a.user_id AS user1, b.user_id AS user2,
           COUNT(DISTINCT a.restaurant_id) AS shared_restaurants
    FROM fact_review a
    JOIN fact_review b ON a.restaurant_id = b.restaurant_id
    WHERE a.user_id < b.user_id
    GROUP BY a.user_id, b.user_id
)
SELECT * FROM user_pairs WHERE shared_restaurants > 10
```

**Cross-Restaurant Patterns**
- Same users giving 5-stars to one restaurant, 1-star to competitors

## 📊 Required Schema Additions

### New Table: fact_review_session
```dbml
Table fact_review_session {
  review_id varchar [pk]
  ip_address_hash varchar  // Hashed for privacy
  device_fingerprint varchar
  user_agent varchar
  session_duration_seconds int
  review_submission_time timestamp
}
```

**Why:** Detect multiple accounts from same device/IP

### New Table: dim_user_metadata
```dbml
Table dim_user_metadata {
  user_id varchar [pk]
  account_created_date date
  first_review_date date
  days_to_first_review int  // Suspicious if 0
  profile_photo_uploaded boolean
  friends_count int  // Fake accounts have 0
  verified_email boolean
  verified_phone boolean
}
```

**Why:** Profile completeness indicates real vs fake accounts

### New Table: fact_review_text_features
```dbml
Table fact_review_text_features {
  review_id varchar [pk]
  character_count int
  word_count int
  sentiment_score decimal
  text_hash varchar  // Detect copy-paste
  contains_urls boolean
  contains_phone boolean
}
```

**Why:** Analyze text patterns for fraud detection

## 🔍 Key Fraud Detection Queries

### Find Fake User Candidates
```sql
SELECT u.user_id, u.user_name,
       COUNT(r.review_id) AS review_count,
       STDDEV(r.score) AS score_variance,
       AVG(LENGTH(r.review_text)) AS avg_text_length,
       um.days_to_first_review,
       um.friends_count
FROM dim_users u
JOIN fact_review r ON u.user_id = r.user_id
JOIN dim_user_metadata um ON u.user_id = um.user_id
GROUP BY u.user_id
HAVING score_variance < 0.5  -- Only gives same rating
   AND avg_text_length < 30  -- Short, generic reviews
   AND days_to_first_review = 0  -- Reviewed immediately
   AND um.friends_count = 0  -- No social connections
```

### Find Restaurants with Suspicious Activity
```sql
SELECT r.restaurant_id, r.restaurant_name,
       COUNT(CASE WHEN DATEDIFF(NOW(), u.yelping_since) < 30 THEN 1 END) AS new_user_reviews,
       COUNT(*) AS total_reviews,
       (COUNT(CASE WHEN DATEDIFF(NOW(), u.yelping_since) < 30 THEN 1 END) * 100.0 / COUNT(*)) AS new_user_pct
FROM dim_restaurant r
JOIN fact_review fr ON r.restaurant_id = fr.restaurant_id
JOIN dim_users u ON fr.user_id = u.user_id
GROUP BY r.restaurant_id
HAVING new_user_pct > 50  -- More than half from new accounts
```

## 📚 Key Takeaways

1. **Behavioral patterns** matter more than static attributes
2. **Velocity metrics** (reviews per day) are strong fraud indicators
3. **Network analysis** reveals coordinated fake review campaigns
4. **Account metadata** (age, completeness) separates real from fake
5. **Text analysis** detects copy-paste and generic reviews
6. **Timing patterns** reveal bot activity (exact timestamps)

## 🎯 What Makes This Different from Generic BI?

| Generic BI Metrics | Fraud Detection Metrics |
|-------------------|------------------------|
| Average rating | Score variance (all 5s or all 1s) |
| Reviews per restaurant | Review spike (sudden increase) |
| User engagement | Review velocity (too many too fast) |
| Restaurant attributes | Account age at first review |
| Geographic distribution | IP/device clustering |
