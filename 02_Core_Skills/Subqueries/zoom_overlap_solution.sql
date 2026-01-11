-- ============================================
-- SQL TRAINING: Finding Users with Overlapping Meetings
-- ============================================

/*
PROBLEM STATEMENT:
Find the number of users who:
1. Organized a meeting (they are the organizer)
2. Were invited to ANOTHER meeting (they are a participant)
3. The two meetings have overlapping timestamps

OUTPUT: participant_count (the count of such users)
*/

-- ============================================
-- STEP 1: Understanding Time Overlap Logic
-- ============================================

/*
Two time ranges overlap if:
- Meeting A starts BEFORE Meeting B ends
AND
- Meeting B starts BEFORE Meeting A ends

Example:
Meeting A: 9:00 - 10:00
Meeting B: 9:30 - 11:00
✅ OVERLAP (9:30 is before 10:00, and 9:00 is before 11:00)

Meeting A: 9:00 - 10:00
Meeting C: 10:00 - 11:00
❌ NO OVERLAP (they touch but don't overlap)
*/

-- ============================================
-- STEP 2: Break Down the Problem
-- ============================================

/*
We need to find users where:
1. They organized meeting M1 (organizer_id in dim_meetings_zoom)
2. They were invited to meeting M2 (participant_id in fact_participations_zoom)
3. M1 and M2 are different meetings (M1.meeting_id != M2.meeting_id)
4. M1 and M2 overlap in time
*/

-- ============================================
-- STEP 3: Build the Query Step-by-Step
-- ============================================

-- Step 3a: Get all meetings a user ORGANIZED
SELECT
    organizer_id AS user_id,
    meeting_id AS organized_meeting_id,
    start_timestamp AS org_start,
    end_timestamp AS org_end
FROM dim_meetings_zoom;

-- Step 3b: Get all meetings a user was INVITED TO
SELECT
    participant_id AS user_id,
    meeting_id AS invited_meeting_id
FROM fact_participations_zoom;

-- Step 3c: Join to get the invited meeting details
SELECT
    fp.participant_id AS user_id,
    fp.meeting_id AS invited_meeting_id,
    dm.start_timestamp AS inv_start,
    dm.end_timestamp AS inv_end
FROM
    fact_participations_zoom fp
    JOIN dim_meetings_zoom dm ON fp.meeting_id = dm.meeting_id;

-- ============================================
-- STEP 4: Complete Solution
-- ============================================

WITH
    organized_meetings AS (
        -- Meetings the user organized
        SELECT
            organizer_id AS user_id,
            meeting_id AS org_meeting_id,
            start_timestamp AS org_start,
            end_timestamp AS org_end
        FROM dim_meetings_zoom
    ),
    invited_meetings AS (
        -- Meetings the user was invited to
        SELECT
            fp.participant_id AS user_id,
            fp.meeting_id AS inv_meeting_id,
            dm.start_timestamp AS inv_start,
            dm.end_timestamp AS inv_end
        FROM
            fact_participations_zoom fp
            JOIN dim_meetings_zoom dm ON fp.meeting_id = dm.meeting_id
    )
SELECT COUNT(DISTINCT om.user_id) AS participant_count
FROM
    organized_meetings om
    JOIN invited_meetings im ON om.user_id = im.user_id -- Same user
    AND om.org_meeting_id != im.inv_meeting_id -- Different meetings
    AND om.org_start < im.inv_end -- Overlap condition 1
    AND im.inv_start < om.org_end;
-- Overlap condition 2

-- ============================================
-- ALTERNATIVE SOLUTION (Without CTEs)
-- ============================================

SELECT COUNT(DISTINCT dm_org.organizer_id) AS participant_count
FROM
    dim_meetings_zoom dm_org -- Meetings they organized
    JOIN fact_participations_zoom fp ON dm_org.organizer_id = fp.participant_id -- Same user invited elsewhere
    JOIN dim_meetings_zoom dm_inv ON fp.meeting_id = dm_inv.meeting_id -- Get invited meeting details
WHERE
    dm_org.meeting_id != dm_inv.meeting_id -- Different meetings
    AND dm_org.start_timestamp < dm_inv.end_timestamp -- Overlap condition 1
    AND dm_inv.start_timestamp < dm_org.end_timestamp;
-- Overlap condition 2

-- ============================================
-- EXPECTED RESULT WITH SAMPLE DATA
-- ============================================

/*
Based on the sample data:

User 1:
- Organized: 1001 (9:00-10:00), 1002 (14:00-15:30)
- Invited to: 2001 (9:30-11:00), 3001 (14:15-15:00), 4002 (15:00-16:00)
- Overlaps: 
* 1001 overlaps with 2001 ✅
* 1002 overlaps with 3001 ✅
* 1002 overlaps with 4002 ✅

User 2:
- Organized: 2001 (9:30-11:00), 2002 (13:00-14:00)
- Invited to: 1001 (9:00-10:00)
- Overlaps:
* 2001 overlaps with 1001 ✅

User 3:
- Organized: 3001 (14:15-15:00), 3002 (16:00-17:00)
- Invited to: 1002 (14:00-15:30)
- Overlaps:
* 3001 overlaps with 1002 ✅

User 4:
- Organized: 4001 (10:00-11:00), 4002 (15:00-16:00)
- Invited to: 1002 (14:00-15:30)
- Overlaps:
* 4002 overlaps with 1002 ✅

RESULT: participant_count = 4 (Users 1, 2, 3, and 4)
*/