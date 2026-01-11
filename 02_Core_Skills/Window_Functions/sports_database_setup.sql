-- =====================================================
-- SPORTS STATS DATABASE - ROW_NUMBER() PRACTICE
-- =====================================================
-- Copy this into DB Fiddle: https://www.db-fiddle.com/
-- Select PostgreSQL for best compatibility
-- =====================================================

-- Drop tables if they exist
DROP TABLE IF EXISTS player_stats;
DROP TABLE IF EXISTS game_results;

-- =====================================================
-- TABLE 1: NBA Player Season Stats (2023-24)
-- =====================================================
CREATE TABLE player_stats (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(100),
    team VARCHAR(50),
    position VARCHAR(10),
    points_per_game DECIMAL(4,1),
    rebounds_per_game DECIMAL(4,1),
    assists_per_game DECIMAL(4,1),
    games_played INT,
    draft_year INT
);

-- Insert realistic NBA-style data
INSERT INTO player_stats VALUES
-- Lakers
(1, 'LeBron James', 'Lakers', 'SF', 25.7, 7.3, 8.3, 71, 2003),
(2, 'Anthony Davis', 'Lakers', 'PF', 24.7, 12.6, 3.5, 76, 2012),
(3, 'D''Angelo Russell', 'Lakers', 'PG', 18.0, 3.1, 6.3, 76, 2015),
(4, 'Austin Reaves', 'Lakers', 'SG', 15.9, 4.3, 5.5, 82, 2021),

-- Warriors
(5, 'Stephen Curry', 'Warriors', 'PG', 26.4, 4.5, 5.1, 74, 2009),
(6, 'Klay Thompson', 'Warriors', 'SG', 17.9, 3.3, 2.3, 77, 2011),
(7, 'Andrew Wiggins', 'Warriors', 'SF', 13.2, 4.5, 1.7, 71, 2014),
(8, 'Draymond Green', 'Warriors', 'PF', 8.6, 7.2, 6.0, 55, 2012),

-- Celtics
(9, 'Jayson Tatum', 'Celtics', 'SF', 26.9, 8.1, 4.9, 74, 2017),
(10, 'Jaylen Brown', 'Celtics', 'SG', 23.0, 5.5, 3.6, 70, 2016),
(11, 'Kristaps Porzingis', 'Celtics', 'C', 20.1, 7.2, 2.0, 57, 2015),
(12, 'Derrick White', 'Celtics', 'PG', 15.2, 4.2, 5.2, 73, 2017),

-- Nuggets
(13, 'Nikola Jokic', 'Nuggets', 'C', 26.4, 12.4, 9.0, 79, 2014),
(14, 'Jamal Murray', 'Nuggets', 'PG', 21.2, 4.1, 6.5, 59, 2016),
(15, 'Michael Porter Jr', 'Nuggets', 'SF', 16.7, 7.0, 1.8, 62, 2018),
(16, 'Aaron Gordon', 'Nuggets', 'PF', 13.9, 6.5, 3.5, 73, 2014),

-- Bucks
(17, 'Giannis Antetokounmpo', 'Bucks', 'PF', 30.4, 11.5, 6.5, 73, 2013),
(18, 'Damian Lillard', 'Bucks', 'PG', 24.3, 4.4, 7.0, 73, 2012),
(19, 'Khris Middleton', 'Bucks', 'SF', 15.1, 4.7, 5.3, 55, 2012),
(20, 'Brook Lopez', 'Bucks', 'C', 12.5, 5.2, 2.4, 79, 2008),

-- Mavericks
(21, 'Luka Doncic', 'Mavericks', 'PG', 33.9, 9.2, 9.8, 70, 2018),
(22, 'Kyrie Irving', 'Mavericks', 'SG', 25.6, 5.0, 5.2, 58, 2011),
(23, 'Derrick Jones Jr', 'Mavericks', 'SF', 8.6, 3.3, 1.0, 76, 2016),
(24, 'Daniel Gafford', 'Mavericks', 'C', 11.0, 7.6, 1.4, 76, 2019);

-- =====================================================
-- TABLE 2: NFL Game Results (2024 Season Sample)
-- =====================================================
CREATE TABLE game_results (
    game_id INT PRIMARY KEY,
    week INT,
    home_team VARCHAR(50),
    away_team VARCHAR(50),
    home_score INT,
    away_score INT,
    game_date DATE,
    attendance INT
);

INSERT INTO game_results VALUES
-- Week 1
(1, 1, 'Chiefs', 'Ravens', 27, 20, '2024-09-05', 73000),
(2, 1, 'Eagles', 'Patriots', 25, 20, '2024-09-08', 69000),
(3, 1, '49ers', 'Steelers', 30, 7, '2024-09-08', 71000),
(4, 1, 'Cowboys', 'Giants', 40, 0, '2024-09-08', 93000),

-- Week 2
(5, 2, 'Bills', 'Raiders', 38, 10, '2024-09-15', 71000),
(6, 2, 'Dolphins', 'Patriots', 24, 17, '2024-09-15', 65000),
(7, 2, 'Saints', 'Cowboys', 44, 19, '2024-09-15', 93000),
(8, 2, 'Packers', 'Colts', 16, 10, '2024-09-15', 77000),

-- Week 3
(9, 3, 'Ravens', 'Cowboys', 28, 25, '2024-09-22', 93000),
(10, 3, 'Chiefs', 'Falcons', 22, 17, '2024-09-22', 71000),
(11, 3, 'Seahawks', 'Dolphins', 24, 3, '2024-09-22', 68000),
(12, 3, 'Buccaneers', 'Broncos', 26, 7, '2024-09-22', 65000);

-- Verify data loaded
SELECT 'NBA Player Stats loaded!' as status, COUNT(*) as total_players FROM player_stats;
SELECT 'NFL Games loaded!' as status, COUNT(*) as total_games FROM game_results;

-- Quick preview
SELECT team, COUNT(*) as players, ROUND(AVG(points_per_game), 1) as avg_ppg
FROM player_stats
GROUP BY team
ORDER BY avg_ppg DESC;

-- =====================================================
-- NOW YOU'RE READY FOR SPORTS-THEMED PRACTICE!
-- =====================================================
-- Use the problems from sports_row_number_practice.md
-- =====================================================

-- Example: Find the top scorer on each team
-- YOUR SOLUTION HERE:



-- Example: Find the 3 highest-scoring games
-- YOUR SOLUTION HERE:
