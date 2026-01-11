-- ============================================
-- HOW TO DEBUG / INSPECT INTERMEDIATE STEPS
-- ============================================
-- SQL runs as a single block, so you can't usually see "live" updates.
-- BUT, you can inspect each step by changing the final SELECT.

-- Here is the same query, but set up for inspection:

-- Step 1: Identify the last 3 games
WITH recent_games AS (
    SELECT game_id, game_date
    FROM games
    ORDER BY game_date DESC
    LIMIT 3
),
-- Step 2: Calculate total points for each player in those games
player_totals AS (
    SELECT 
        p.team_name,
        p.player_name,
        SUM(pgs.points) AS total_points,
        COUNT(pgs.game_id) as games_played -- Added for visibility
    FROM 
        player_game_stats pgs
    JOIN 
        players p ON pgs.player_id = p.player_id
    WHERE 
        pgs.game_id IN (SELECT game_id FROM recent_games)
    GROUP BY 
        p.team_name, p.player_name
),
-- Step 3: Rank players within their team
ranked_players AS (
    SELECT
        team_name,
        player_name,
        total_points,
        RANK() OVER (PARTITION BY team_name ORDER BY total_points DESC) as rank_in_team
    FROM
        player_totals
)
-- ============================================
-- 🕵️ DEBUGGING ZONE
-- ============================================
-- Uncomment ONE of the SELECT statements below to see that step's data!

-- 👉 OPTION 1: See which games were selected (Step 1)
-- SELECT * FROM recent_games;

-- 👉 OPTION 2: See the raw totals before ranking (Step 2)
-- SELECT * FROM player_totals ORDER BY total_points DESC;

-- 👉 OPTION 3: See the rankings before filtering (Step 3)
-- SELECT * FROM ranked_players ORDER BY team_name, rank_in_team;

-- 👉 OPTION 4: The Final Result (Step 4)
SELECT 
    team_name,
    rank_in_team,
    player_name,
    total_points
FROM 
    ranked_players
WHERE 
    rank_in_team <= 3
ORDER BY 
    team_name, rank_in_team;
