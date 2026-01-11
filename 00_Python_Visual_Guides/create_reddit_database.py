import pandas as pd
import sqlalchemy
from datetime import datetime, timedelta
import random
import string

print("🎯 Creating Reddit Practice Database")
print("=" * 70)

# Connect to MySQL
username = 'python_user'
password = 'password'
host = '127.0.0.1'
port = '3306'
db_name = "reddit_practice_db"

# Create database if not exists
root_conn = f"mysql+pymysql://{username}:{password}@{host}:{port}"
engine = sqlalchemy.create_engine(root_conn)
with engine.connect() as conn:
    conn.execute(sqlalchemy.text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
    conn.commit()

# Connect to the new database
db_connection_str = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"
db_engine = sqlalchemy.create_engine(db_connection_str)

print(f"✅ Connected to '{db_name}'!\n")

# ==========================================
# 1. CREATE dim_publishers_reddit
# ==========================================
print("👥 Creating dim_publishers_reddit table...")

cities = ['Indiana', 'California', 'Texas', 'New York', 'Florida', 'Illinois', 'Ohio', 'Pennsylvania']
first_names = ['Dylann', 'Sarah', 'Michael', 'Emma', 'James', 'Olivia', 'Robert', 'Sophia', 'William', 'Isabella']
last_names = ['Bennett', 'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez']

publishers = []
for i in range(20):
    publisher_id = 'GB' + ''.join(random.choices(string.digits, k=20))
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    city = random.choice(cities)
    publishers.append([publisher_id, name, city])

df_publishers = pd.DataFrame(publishers, columns=['publisher_id', 'name', 'city'])
df_publishers.to_sql('dim_publishers_reddit', db_engine, if_exists='replace', index=False)
print(f"✅ Created dim_publishers_reddit with {len(publishers)} publishers")

# ==========================================
# 2. CREATE fact_reddit
# ==========================================
print("\n📝 Creating fact_reddit table...")

base_date = datetime(2022, 10, 1)
posts = []

# Create strategic posting patterns
publisher_patterns = {
    # Publishers that QUALIFY (3+ posts with 7+ day gaps)
    0: [0, 10, 20, 30],      # 4 posts, all gaps 10 days
    1: [0, 7, 14, 21, 28],   # 5 posts, all gaps 7 days
    2: [0, 15, 35, 50],      # 4 posts, gaps: 15, 20, 15 days
    3: [0, 8, 16, 24],       # 4 posts, all gaps 8 days
    
    # Publishers that DON'T QUALIFY
    4: [0, 3, 10, 13],       # 4 posts, gaps: 3, 7, 3 (only 1 gap of 7+)
    5: [0, 1, 2, 3],         # 4 posts, all gaps 1 day
    6: [0, 20],              # Only 2 posts
    7: [0, 5, 15],           # 3 posts, gaps: 5, 10 (only 1 gap of 7+)
    
    # More qualifying publishers
    8: [0, 9, 18, 27, 36],   # 5 posts, all gaps 9 days
    9: [0, 14, 28, 42],      # 4 posts, all gaps 14 days
}

# Generate posts
post_id = 1
for pub_idx, day_offsets in publisher_patterns.items():
    publisher_id = df_publishers.iloc[pub_idx]['publisher_id']
    
    for day_offset in day_offsets:
        post_date = base_date + timedelta(days=day_offset)
        post_id_str = 'VH' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        comm_num = random.randint(10, 100)
        score = random.randint(20, 100)
        content = f"Sample post content {post_id} from publisher {pub_idx}"
        
        posts.append([post_id_str, publisher_id, comm_num, score, post_date, content])
        post_id += 1

# Add random posts for remaining publishers
for pub_idx in range(10, 20):
    publisher_id = df_publishers.iloc[pub_idx]['publisher_id']
    num_posts = random.randint(1, 5)
    
    for _ in range(num_posts):
        day_offset = random.randint(0, 60)
        post_date = base_date + timedelta(days=day_offset)
        post_id_str = 'VH' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        comm_num = random.randint(10, 100)
        score = random.randint(20, 100)
        content = f"Random post content from publisher {pub_idx}"
        
        posts.append([post_id_str, publisher_id, comm_num, score, post_date, content])

df_posts = pd.DataFrame(posts, columns=['post_id', 'publisher_id', 'comm_num', 'score', 'creation_date', 'content'])
df_posts.to_sql('fact_reddit', db_engine, if_exists='replace', index=False)
print(f"✅ Created fact_reddit with {len(posts)} posts")

# ==========================================
# 3. SHOW SAMPLE DATA
# ==========================================
print("\n" + "=" * 70)
print("📊 Sample Data Preview")
print("=" * 70)

print("\n🔍 First 5 Publishers:")
print(df_publishers.head().to_string(index=False))

print("\n🔍 First 10 Posts:")
print(df_posts[['post_id', 'publisher_id', 'creation_date', 'score']].head(10).to_string(index=False))

# ==========================================
# 4. RUN THE SOLUTION QUERY
# ==========================================
print("\n" + "=" * 70)
print("🎯 Running the Solution Query")
print("=" * 70)

solution_query = """
WITH posts_with_gaps AS (
    SELECT
        publisher_id,
        creation_date,
        DATEDIFF(creation_date, LAG(creation_date) OVER (PARTITION BY publisher_id ORDER BY creation_date)) AS days_between_posts
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

df_result = pd.read_sql(solution_query, db_engine)
print("\n📈 RESULT:")
print(df_result.to_string(index=False))

# ==========================================
# 5. SHOW QUALIFYING PUBLISHERS
# ==========================================
print("\n" + "=" * 70)
print("✅ Publishers That Qualify")
print("=" * 70)

detail_query = """
WITH posts_with_gaps AS (
    SELECT
        publisher_id,
        creation_date,
        DATEDIFF(creation_date, LAG(creation_date) OVER (PARTITION BY publisher_id ORDER BY creation_date)) AS days_between_posts
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
    pgc.gaps_of_7plus_days
FROM publisher_gap_check pgc
JOIN dim_publishers_reddit p ON pgc.publisher_id = p.publisher_id
WHERE total_posts >= 3
  AND gaps_of_7plus_days >= 2
ORDER BY gaps_of_7plus_days DESC, total_posts DESC;
"""

df_qualifying = pd.read_sql(detail_query, db_engine)
print(df_qualifying.to_string(index=False))

print("\n" + "=" * 70)
print("✅ Database setup complete!")
print("=" * 70)
print("\nYou can now practice the LAG query!")
print("Database: reddit_practice_db")
print("Tables: dim_publishers_reddit, fact_reddit")
print("\nTry modifying the query or exploring the data!")
