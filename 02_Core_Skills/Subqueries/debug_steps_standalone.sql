-- ============================================
-- DEBUGGING: RUNNABLE STEPS
-- ============================================
-- Instead of uncommenting parts of a big query, 
-- here are the steps as separate, runnable queries.
-- Highlight one block at a time and run it!

-- ============================================
-- 🕵️ STEP 1: CHECK THE GAMES
-- ============================================
-- Goal: Are we actually getting the last 3 games?
WITH recent_games AS (
    SELECT game_id, game_date
    FROM games
    ORDER BY game_date DESC
    LIMIT 3
)
SELECT * FROM recent_games;
-- 👆 Highlight from "WITH" to ";" and run!


-- ============================================
-- 🕵️ STEP 2: CHECK THE TOTALS
-- ============================================
-- Goal: Are the point totals correct for those games?
WITH recent_games AS (
    SELECT game_id
    FROM games
    ORDER BY game_date DESC
    LIMIT 3
),
player_totals AS (
    SELECT 
        p.team_name,
        p.player_name,
        SUM(pgs.points) AS total_points
    FROM 
        player_game_stats pgs
    JOIN 
        players p ON pgs.player_id = p.player_id
    WHERE 
    -- This is a subquery that gets the game_id from the recent_games CTE
    -- and checks if the game_id in the player_game_stats table is in the recent_games CTE
        pgs.game_id IN (SELECT game_id FROM recent_games)
    GROUP BY 
        p.team_name, p.player_name
)
SELECT * FROM player_totals ORDER BY total_points DESC;
-- 👆 Highlight from "WITH" to ";" and run!


-- ============================================
-- 🕵️ STEP 3: CHECK THE RANKINGS
-- ============================================
-- Goal: Did the ranking function work correctly?
WITH recent_games AS (
    SELECT game_id
    FROM games
    ORDER BY game_date DESC
    LIMIT 3
),
player_totals AS (
    SELECT 
        p.team_name,
        p.player_name,
        SUM(pgs.points) AS total_points
    FROM 
        player_game_stats pgs
    JOIN 
        players p ON pgs.player_id = p.player_id
    WHERE 
        pgs.game_id IN (SELECT game_id FROM recent_games)
    GROUP BY 
        p.team_name, p.player_name
),
ranked_players AS (
    SELECT
        team_name,
        player_name,
        total_points,
        RANK() OVER (PARTITION BY team_name ORDER BY total_points DESC) as rank_in_team
    FROM
        player_totals
)
SELECT * FROM ranked_players ORDER BY team_name, rank_in_team;


-- ============================================
-- 🏆 STEP 4: FINAL RESULT
-- ============================================
-- Goal: The final answer (Top 3 per team)
WITH recent_games AS (
    SELECT game_id
    FROM games
    ORDER BY game_date DESC
    LIMIT 3
),
player_totals AS (
    SELECT 
        p.team_name,
        p.player_name,
        SUM(pgs.points) AS total_points
    FROM 
        player_game_stats pgs
    JOIN 
        players p ON pgs.player_id = p.player_id
    WHERE 
        pgs.game_id IN (SELECT game_id FROM recent_games)
    GROUP BY 
        p.team_name, p.player_name
),
ranked_players AS (
    SELECT
        team_name,
        player_name,
        total_points,
        RANK() OVER (PARTITION BY team_name ORDER BY total_points DESC) as rank_in_team
    FROM
        player_totals
)
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
