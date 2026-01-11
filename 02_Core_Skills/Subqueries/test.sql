-- ============================================
-- TOP 3 PLAYERS IN LAST 3 GAMES
-- ============================================

-- Step 1: Identify the last 3 games
WITH recent_games AS (
    SELECT game_id
    FROM games
    ORDER BY game_date DESC
    LIMIT 3
),
-- Step 2: Calculate total points for each player in those games
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
-- Step 4: Filter for top 3
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
