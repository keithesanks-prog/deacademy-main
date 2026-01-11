-- ============================================
-- SPORTS ANALYTICS PRACTICE ENVIRONMENT
-- ============================================

DROP TABLE IF EXISTS player_game_stats CASCADE;
DROP TABLE IF EXISTS games CASCADE;
DROP TABLE IF EXISTS players CASCADE;

-- 1. Players Table
CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT,
    team_name TEXT
);

INSERT INTO players VALUES
(1, 'LeBron James', 'Lakers'),
(2, 'Anthony Davis', 'Lakers'),
(3, 'Austin Reaves', 'Lakers'),
(4, 'D''Angelo Russell', 'Lakers'),
(5, 'Steph Curry', 'Warriors'),
(6, 'Klay Thompson', 'Warriors'),
(7, 'Draymond Green', 'Warriors'),
(8, 'Andrew Wiggins', 'Warriors');

-- 2. Games Table
CREATE TABLE games (
    game_id INTEGER PRIMARY KEY,
    game_date DATE
);

INSERT INTO games VALUES
(101, '2025-01-01'),
(102, '2025-01-03'),
(103, '2025-01-05'),
(104, '2025-01-07'),
(105, '2025-01-09');

-- 3. Player Stats per Game
CREATE TABLE player_game_stats (
    stat_id INTEGER PRIMARY KEY,
    player_id INTEGER,
    game_id INTEGER,
    points INTEGER,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

-- Insert data for last 5 games
INSERT INTO player_game_stats VALUES
-- Game 101
(1, 1, 101, 25), (2, 2, 101, 20), (3, 3, 101, 15), (4, 4, 101, 10), -- Lakers
(5, 5, 101, 30), (6, 6, 101, 25), (7, 7, 101, 10), (8, 8, 101, 15), -- Warriors
-- Game 102
(9, 1, 102, 28), (10, 2, 102, 22), (11, 3, 102, 12), (12, 4, 102, 14),
(13, 5, 102, 32), (14, 6, 102, 20), (15, 7, 102, 8), (16, 8, 102, 18),
-- Game 103 (Last 3 starts here)
(17, 1, 103, 30), (18, 2, 103, 25), (19, 3, 103, 18), (20, 4, 103, 12),
(21, 5, 103, 35), (22, 6, 103, 22), (23, 7, 103, 12), (24, 8, 103, 10),
-- Game 104
(25, 1, 104, 22), (26, 2, 104, 28), (27, 3, 104, 20), (28, 4, 104, 15),
(29, 5, 104, 28), (30, 6, 104, 24), (31, 7, 104, 14), (32, 8, 104, 12),
-- Game 105
(33, 1, 105, 35), (34, 2, 105, 24), (35, 3, 105, 16), (36, 4, 105, 18),
(37, 5, 105, 40), (38, 6, 105, 18), (39, 7, 105, 10), (40, 8, 105, 20);

-- ============================================
-- VERIFICATION
-- ============================================
SELECT * FROM players;
SELECT * FROM games;
SELECT * FROM player_game_stats LIMIT 10;
