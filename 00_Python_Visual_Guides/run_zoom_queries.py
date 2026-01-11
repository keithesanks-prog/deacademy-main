import pandas as pd
import sqlalchemy

# Connect to zoom_practice_db
db_connection_str = "mysql+pymysql://python_user:password@127.0.0.1:3306/zoom_practice_db"
engine = sqlalchemy.create_engine(db_connection_str)

print("🎯 Zoom Meetings Self-Join Practice Queries")
print("=" * 80)

# ==========================================
# QUERY 1: Show all overlapping meetings
# ==========================================
print("\n📊 QUERY 1: All Overlapping Meeting Pairs")
print("=" * 80)

query1 = """
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
ORDER BY m1.meeting_id, m2.meeting_id;
"""

df1 = pd.read_sql(query1, engine)
print(df1.to_string(index=False))
print(f"\nTotal overlapping pairs: {len(df1)}")

# ==========================================
# QUERY 2: Participants in overlapping meetings
# ==========================================
print("\n\n📊 QUERY 2: Participants in Overlapping Meetings (Confirmed)")
print("=" * 80)

query2 = """
SELECT 
    p1.participant_id,
    COUNT(*) AS overlapped_meeting_count
FROM dim_meetings_zoom m1
JOIN dim_meetings_zoom m2
    ON m1.meeting_id < m2.meeting_id
    AND m1.start_timestamp < m2.end_timestamp
    AND m2.start_timestamp < m1.end_timestamp
JOIN fact_participations_zoom p1 ON m1.meeting_id = p1.meeting_id
JOIN fact_participations_zoom p2 ON m2.meeting_id = p2.meeting_id
    AND p1.participant_id = p2.participant_id
WHERE p1.status = 'Confirmed' 
  AND p2.status = 'Confirmed'
GROUP BY p1.participant_id
ORDER BY overlapped_meeting_count DESC;
"""

df2 = pd.read_sql(query2, engine)
print(df2.to_string(index=False))

# ==========================================
# QUERY 3: FINAL SOLUTION - The complete problem
# ==========================================
print("\n\n📊 QUERY 3: FINAL SOLUTION - Participants with Overlapping + Non-Overlapping")
print("=" * 80)

query3 = """
WITH overlapping_meetings AS (
    SELECT 
        p1.participant_id,
        COUNT(*) AS overlapped_meeting_count
    FROM dim_meetings_zoom m1
    JOIN dim_meetings_zoom m2
        ON m1.meeting_id < m2.meeting_id
        AND m1.start_timestamp < m2.end_timestamp
        AND m2.start_timestamp < m1.end_timestamp
    JOIN fact_participations_zoom p1 ON m1.meeting_id = p1.meeting_id
    JOIN fact_participations_zoom p2 ON m2.meeting_id = p2.meeting_id
        AND p1.participant_id = p2.participant_id
    WHERE p1.status = 'Confirmed' 
      AND p2.status = 'Confirmed'
    GROUP BY p1.participant_id
),
non_overlapping_participants AS (
    SELECT DISTINCT
        p1.participant_id
    FROM dim_meetings_zoom m1
    JOIN dim_meetings_zoom m2
        ON m1.meeting_id < m2.meeting_id
        AND (m1.end_timestamp <= m2.start_timestamp 
             OR m2.end_timestamp <= m1.start_timestamp)
    JOIN fact_participations_zoom p1 ON m1.meeting_id = p1.meeting_id
    JOIN fact_participations_zoom p2 ON m2.meeting_id = p2.meeting_id
        AND p1.participant_id = p2.participant_id
    WHERE p1.status = 'Confirmed' 
      AND p2.status = 'Confirmed'
    GROUP BY p1.participant_id
    HAVING COUNT(DISTINCT m1.meeting_id) >= 2
)
SELECT 
    om.participant_id,
    om.overlapped_meeting_count
FROM overlapping_meetings om
INNER JOIN non_overlapping_participants nop 
    ON om.participant_id = nop.participant_id
ORDER BY om.overlapped_meeting_count DESC;
"""

df3 = pd.read_sql(query3, engine)
print(df3.to_string(index=False))

print("\n" + "=" * 80)
print("✅ These are the participants who meet BOTH criteria:")
print("   1. Were confirmed in overlapping meetings")
print("   2. Were also in at least 2 non-overlapping meetings")
print("=" * 80)

# ==========================================
# BONUS: Show details for one participant
# ==========================================
if len(df3) > 0:
    sample_participant = df3.iloc[0]['participant_id']
    
    print(f"\n\n📊 BONUS: Detailed View for Participant {sample_participant}")
    print("=" * 80)
    
    detail_query = f"""
    SELECT 
        m.meeting_id,
        m.start_timestamp AS start_time,
        m.end_timestamp AS end_time,
        p.status
    FROM fact_participations_zoom p
    JOIN dim_meetings_zoom m ON p.meeting_id = m.meeting_id
    WHERE p.participant_id = {sample_participant}
    ORDER BY m.start_timestamp;
    """
    
    df_detail = pd.read_sql(detail_query, engine)
    print(df_detail.to_string(index=False))

print("\n\n🎓 Practice Tips:")
print("- Try modifying the queries to remove filters and see what changes")
print("- Experiment with different overlap conditions")
print("- Add more participants or meetings to the database")
print("- Try the practice variations from self_join_mastery.md")
