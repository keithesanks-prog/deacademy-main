import pandas as pd
import sqlalchemy

# Connect to reddit_practice_db
db_connection_str = "mysql+pymysql://python_user:password@127.0.0.1:3306/reddit_practice_db"
engine = sqlalchemy.create_engine(db_connection_str)

print("🎯 Reddit LAG Window Function Practice")
print("=" * 80)

# ==========================================
# QUERY 1: Show posting patterns for each publisher
# ==========================================
print("\n📊 QUERY 1: Publisher Posting Patterns")
print("=" * 80)

query1 = """
WITH posts_with_gaps AS (
    SELECT
        publisher_id,
        creation_date,
        LAG(creation_date) OVER (PARTITION BY publisher_id ORDER BY creation_date) AS prev_post_date,
        DATEDIFF(
            creation_date, 
            LAG(creation_date) OVER (PARTITION BY publisher_id ORDER BY creation_date)
        ) AS days_between_posts
    FROM fact_reddit
)
SELECT 
    p.name,
    pwg.creation_date,
    pwg.prev_post_date,
    pwg.days_between_posts,
    CASE 
        WHEN pwg.days_between_posts >= 7 THEN '✅ Qualifies'
        WHEN pwg.days_between_posts IS NULL THEN 'First Post'
        ELSE '❌ Too Soon'
    END AS gap_status
FROM posts_with_gaps pwg
JOIN dim_publishers_reddit p ON pwg.publisher_id = p.publisher_id
ORDER BY p.name, pwg.creation_date
LIMIT 30;
"""

df1 = pd.read_sql(query1, engine)
print(df1.to_string(index=False))

# ==========================================
# QUERY 2: Count gaps per publisher
# ==========================================
print("\n\n📊 QUERY 2: Gap Analysis per Publisher")
print("=" * 80)

query2 = """
WITH posts_with_gaps AS (
    SELECT
        publisher_id,
        creation_date,
        DATEDIFF(
            creation_date, 
            LAG(creation_date) OVER (PARTITION BY publisher_id ORDER BY creation_date)
        ) AS days_between_posts
    FROM fact_reddit
),
publisher_gap_check AS (
    SELECT
        publisher_id,
        COUNT(*) AS total_posts,
        COUNT(CASE WHEN days_between_posts >= 7 THEN 1 END) AS gaps_of_7plus_days
    FROM posts_with_gaps
    GROUP BY publisher_id
)
SELECT
    p.name,
    pgc.total_posts,
    pgc.gaps_of_7plus_days,
    CASE 
        WHEN pgc.total_posts >= 3 AND pgc.gaps_of_7plus_days >= 2 THEN '✅ QUALIFIES'
        ELSE '❌ Does not qualify'
    END AS status
FROM publisher_gap_check pgc
JOIN dim_publishers_reddit p ON pgc.publisher_id = p.publisher_id
ORDER BY pgc.gaps_of_7plus_days DESC, pgc.total_posts DESC;
"""

df2 = pd.read_sql(query2, engine)
print(df2.to_string(index=False))

# ==========================================
# QUERY 3: THE FINAL ANSWER
# ==========================================
print("\n\n📊 QUERY 3: THE FINAL ANSWER")
print("=" * 80)

query3 = """
WITH posts_with_gaps AS (
    SELECT
        publisher_id,
        creation_date,
        DATEDIFF(
            creation_date, 
            LAG(creation_date) OVER (PARTITION BY publisher_id ORDER BY creation_date)
        ) AS days_between_posts
    FROM fact_reddit
),
publisher_gap_check AS (
    SELECT
        publisher_id,
        COUNT(*) AS total_posts,
        COUNT(CASE WHEN days_between_posts >= 7 THEN 1 END) AS gaps_of_7plus_days
    FROM posts_with_gaps
    GROUP BY publisher_id
)
SELECT
    COUNT(*) AS number_of_publishers
FROM publisher_gap_check
WHERE total_posts >= 3
  AND gaps_of_7plus_days >= 2;
"""

df3 = pd.read_sql(query3, engine)
print("\n🎯 Number of publishers with 3+ posts and 7+ day gaps:")
print(df3.to_string(index=False))

print("\n" + "=" * 80)
print("✅ These publishers have at least 3 posts where every two consecutive")
print("   posts are separated by at least one week (7+ days)")
print("=" * 80)

# ==========================================
# BONUS: Show one publisher's timeline
# ==========================================
print("\n\n📊 BONUS: Detailed Timeline for One Qualifying Publisher")
print("=" * 80)

bonus_query = """
WITH posts_with_gaps AS (
    SELECT
        publisher_id,
        creation_date,
        DATEDIFF(
            creation_date, 
            LAG(creation_date) OVER (PARTITION BY publisher_id ORDER BY creation_date)
        ) AS days_between_posts
    FROM fact_reddit
),
publisher_gap_check AS (
    SELECT
        publisher_id,
        COUNT(*) AS total_posts,
        COUNT(CASE WHEN days_between_posts >= 7 THEN 1 END) AS gaps_of_7plus_days
    FROM posts_with_gaps
    GROUP BY publisher_id
    HAVING COUNT(*) >= 3 AND COUNT(CASE WHEN days_between_posts >= 7 THEN 1 END) >= 2
    LIMIT 1
)
SELECT 
    p.name,
    pwg.creation_date,
    pwg.days_between_posts,
    CASE 
        WHEN pwg.days_between_posts >= 7 THEN '✅'
        WHEN pwg.days_between_posts IS NULL THEN '-'
        ELSE '❌'
    END AS qualifies
FROM posts_with_gaps pwg
JOIN publisher_gap_check pgc ON pwg.publisher_id = pgc.publisher_id
JOIN dim_publishers_reddit p ON pwg.publisher_id = p.publisher_id
ORDER BY pwg.creation_date;
"""

df_bonus = pd.read_sql(bonus_query, engine)
print(df_bonus.to_string(index=False))

print("\n\n🎓 Practice Tips:")
print("- Try changing the threshold from 7 to 14 days")
print("- Modify to find publishers with ALL gaps >= 7 days")
print("- Add more conditions (e.g., minimum score)")
print("- Explore the data with different filters")
