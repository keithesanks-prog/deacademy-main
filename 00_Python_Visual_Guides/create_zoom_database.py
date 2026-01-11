import pandas as pd
import sqlalchemy
from datetime import datetime, timedelta
import random

print("🎯 Creating Zoom Meetings Database for Self-Join Practice")
print("=" * 70)

# Connect to MySQL
username = 'python_user'
password = 'password'
host = '127.0.0.1'
port = '3306'
db_name = "zoom_practice_db"

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
# 1. CREATE dim_meetings_zoom
# ==========================================
print("📅 Creating dim_meetings_zoom table...")

meetings = []
base_date = datetime(2022, 12, 6, 9, 0, 0)  # Start at 9 AM

# Create 20 meetings with various overlaps
meeting_configs = [
    # Morning meetings (some overlapping)
    (1, 1, 0, 60),      # 9:00-10:00
    (2, 2, 30, 90),     # 9:30-11:00 (overlaps with M1)
    (3, 3, 90, 60),     # 10:30-11:30 (overlaps with M2)
    (4, 4, 180, 60),    # 12:00-13:00 (no overlap)
    
    # Afternoon meetings
    (5, 5, 240, 60),    # 13:00-14:00
    (6, 6, 270, 90),    # 13:30-15:00 (overlaps with M5)
    (7, 7, 360, 60),    # 15:00-16:00 (no overlap)
    (8, 8, 390, 90),    # 15:30-17:00 (overlaps with M7)
    
    # Evening meetings
    (9, 9, 480, 60),    # 17:00-18:00
    (10, 10, 540, 60),  # 18:00-19:00 (no overlap)
    
    # Next day - more overlaps
    (11, 1, 1440, 60),  # Day 2: 9:00-10:00
    (12, 2, 1470, 60),  # Day 2: 9:30-10:30 (overlaps with M11)
    (13, 3, 1500, 60),  # Day 2: 10:00-11:00 (overlaps with M12)
    (14, 4, 1560, 60),  # Day 2: 11:00-12:00 (no overlap)
    
    # Day 3 - complex overlaps
    (15, 5, 2880, 120), # Day 3: 9:00-11:00
    (16, 6, 2940, 120), # Day 3: 10:00-12:00 (overlaps with M15)
    (17, 7, 3000, 60),  # Day 3: 11:00-12:00 (overlaps with M16)
    (18, 8, 3060, 60),  # Day 3: 12:00-13:00 (no overlap)
    (19, 9, 3120, 60),  # Day 3: 13:00-14:00
    (20, 10, 3180, 60), # Day 3: 14:00-15:00 (no overlap)
]

for meeting_id, organizer_id, start_offset_mins, duration_mins in meeting_configs:
    start_time = base_date + timedelta(minutes=start_offset_mins)
    end_time = start_time + timedelta(minutes=duration_mins)
    meetings.append([meeting_id, organizer_id, start_time, end_time])

df_meetings = pd.DataFrame(meetings, columns=['meeting_id', 'organizer_id', 'start_timestamp', 'end_timestamp'])
df_meetings.to_sql('dim_meetings_zoom', db_engine, if_exists='replace', index=False)
print(f"✅ Created dim_meetings_zoom with {len(meetings)} meetings")

# ==========================================
# 2. CREATE fact_participations_zoom
# ==========================================
print("\n👥 Creating fact_participations_zoom table...")

participations = []
num_participants = 15

# Create strategic participations to demonstrate the problem
participation_patterns = {
    # Participant 1: In many overlapping meetings + non-overlapping
    1: {'meetings': [1, 2, 3, 4, 5, 10, 14, 18], 'status': 'Confirmed'},
    
    # Participant 2: In overlapping meetings but NOT in 2+ non-overlapping
    2: {'meetings': [1, 2, 3], 'status': 'Confirmed'},
    
    # Participant 3: In overlapping + enough non-overlapping
    3: {'meetings': [5, 6, 7, 8, 10, 14], 'status': 'Confirmed'},
    
    # Participant 4: In overlapping + non-overlapping
    4: {'meetings': [11, 12, 13, 14, 18, 20], 'status': 'Confirmed'},
    
    # Participant 5: In overlapping + non-overlapping
    5: {'meetings': [15, 16, 17, 18, 19, 20], 'status': 'Confirmed'},
    
    # Participant 6: Only non-overlapping meetings
    6: {'meetings': [4, 7, 10, 14, 18, 20], 'status': 'Confirmed'},
    
    # Participant 7: Mix of confirmed and not confirmed
    7: {'meetings': [1, 2], 'status': 'Not confirmed'},
    
    # Participant 8: In overlapping + non-overlapping
    8: {'meetings': [1, 2, 4, 7, 10], 'status': 'Confirmed'},
    
    # Participants 9-15: Random patterns
}

# Add strategic participants
for participant_id, config in participation_patterns.items():
    for meeting_id in config['meetings']:
        participations.append([meeting_id, participant_id, config['status']])

# Add some random participants
for participant_id in range(9, 16):
    num_meetings = random.randint(2, 6)
    selected_meetings = random.sample(range(1, 21), num_meetings)
    status = random.choice(['Confirmed', 'Confirmed', 'Confirmed', 'Not confirmed'])
    for meeting_id in selected_meetings:
        participations.append([meeting_id, participant_id, status])

df_participations = pd.DataFrame(participations, columns=['meeting_id', 'participant_id', 'status'])
df_participations.to_sql('fact_participations_zoom', db_engine, if_exists='replace', index=False)
print(f"✅ Created fact_participations_zoom with {len(participations)} participation records")

# ==========================================
# 3. SHOW SAMPLE DATA
# ==========================================
print("\n" + "=" * 70)
print("📊 Sample Data Preview")
print("=" * 70)

print("\n🔍 First 5 Meetings:")
print(df_meetings.head().to_string(index=False))

print("\n🔍 First 10 Participations:")
print(df_participations.head(10).to_string(index=False))

# ==========================================
# 4. SHOW OVERLAPPING MEETINGS
# ==========================================
print("\n" + "=" * 70)
print("🔄 Overlapping Meeting Pairs (for verification)")
print("=" * 70)

overlap_query = """
SELECT 
    m1.meeting_id AS meeting_1,
    m1.start_timestamp AS m1_start,
    m1.end_timestamp AS m1_end,
    m2.meeting_id AS meeting_2,
    m2.start_timestamp AS m2_start,
    m2.end_timestamp AS m2_end
FROM dim_meetings_zoom m1
JOIN dim_meetings_zoom m2
    ON m1.meeting_id < m2.meeting_id
    AND m1.start_timestamp < m2.end_timestamp
    AND m2.start_timestamp < m1.end_timestamp
ORDER BY m1.meeting_id, m2.meeting_id
LIMIT 10;
"""

df_overlaps = pd.read_sql(overlap_query, db_engine)
print(df_overlaps.to_string(index=False))

print("\n" + "=" * 70)
print("✅ Database setup complete!")
print("=" * 70)
print("\nYou can now practice the self-join queries!")
print("\nTry running the query from self_join_mastery.md")
print("Database: zoom_practice_db")
print("Tables: dim_meetings_zoom, fact_participations_zoom")
