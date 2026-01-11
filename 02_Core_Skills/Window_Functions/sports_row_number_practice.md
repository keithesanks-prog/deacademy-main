# 🏀 ROW_NUMBER() Practice - Sports Edition ⚾
## Learn SQL While Analyzing Real Sports Stats!

---

## 🎯 Setup Instructions

1. Open [DB Fiddle](https://www.db-fiddle.com/) (PostgreSQL)
2. Copy **all contents** from [`sports_database_setup.sql`](file:///c:/Users/ksank/training/02_Core_Skills/Window_Functions/sports_database_setup.sql)
3. Paste into left panel and click "Run"
4. You now have NBA player stats and NFL game results to practice with! 🏈🏀

---

## 📊 Your Data

### **NBA Player Stats Table:**
- 24 players across 6 teams (Lakers, Warriors, Celtics, Nuggets, Bucks, Mavericks)
- Stats: points_per_game, rebounds_per_game, assists_per_game, games_played, draft_year

### **NFL Game Results Table:**
- 12 games from 2024 season (Weeks 1-3)
- Data: home/away teams, scores, attendance, game dates

---

## 🏀 NBA Problems (Beginner)

### **Problem 1: MVP Race - Top Scorer**
Who's leading the league in scoring? Find the player with the highest points per game.

<details>
<summary>💡 Hint</summary>
No PARTITION BY needed - just ORDER BY points_per_game DESC and get rn = 1
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT player_name, team, points_per_game
FROM (
    SELECT 
        player_name,
        team,
        points_per_game,
        ROW_NUMBER() OVER (ORDER BY points_per_game DESC) as rn
    FROM player_stats
) ranked
WHERE rn = 1;
```

**Result:** Luka Doncic, Mavericks, 33.9 PPG 🔥
</details>

---

### **Problem 2: Team Leaders - Top Scorer Per Team**
Find the leading scorer on each team (the go-to guy!).

<details>
<summary>💡 Hint</summary>
PARTITION BY team, ORDER BY points_per_game DESC
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT player_name, team, points_per_game
FROM (
    SELECT 
        player_name,
        team,
        points_per_game,
        ROW_NUMBER() OVER (PARTITION BY team ORDER BY points_per_game DESC) as rn
    FROM player_stats
) ranked
WHERE rn = 1
ORDER BY points_per_game DESC;
```

**Result:**
```
player_name              | team       | points_per_game
-------------------------|------------|----------------
Luka Doncic             | Mavericks  | 33.9
Giannis Antetokounmpo   | Bucks      | 30.4
Jayson Tatum            | Celtics    | 26.9
Nikola Jokic            | Nuggets    | 26.4
Stephen Curry           | Warriors   | 26.4
LeBron James            | Lakers     | 25.7
```
</details>

---

### **Problem 3: The Big 3 - Top 3 Scorers Per Team**
Every contender needs their "Big 3". Find the top 3 scorers on each team.

<details>
<summary>✅ Solution</summary>

```sql
SELECT player_name, team, points_per_game, rn as team_rank
FROM (
    SELECT 
        player_name,
        team,
        points_per_game,
        ROW_NUMBER() OVER (PARTITION BY team ORDER BY points_per_game DESC) as rn
    FROM player_stats
) ranked
WHERE rn <= 3
ORDER BY team, rn;
```

**Lakers Big 3:** LeBron (25.7), AD (24.7), D'Angelo (18.0) 💜💛
</details>

---

### **Problem 4: Bench Warmers - Lowest Scorer Per Team**
Find the lowest-scoring player on each team.

<details>
<summary>💡 Hint</summary>
Change ORDER BY to ASC instead of DESC
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT player_name, team, points_per_game
FROM (
    SELECT 
        player_name,
        team,
        points_per_game,
        ROW_NUMBER() OVER (PARTITION BY team ORDER BY points_per_game ASC) as rn
    FROM player_stats
) ranked
WHERE rn = 1
ORDER BY team;
```
</details>

---

### **Problem 5: Rookie vs Veteran - Oldest Players**
Find the 3 players who've been in the league longest (earliest draft year).

<details>
<summary>💡 Hint</summary>
ORDER BY draft_year ASC (earliest = oldest)
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT player_name, team, draft_year, 
       2024 - draft_year as years_in_league
FROM (
    SELECT 
        player_name,
        team,
        draft_year,
        ROW_NUMBER() OVER (ORDER BY draft_year ASC) as rn
    FROM player_stats
) ranked
WHERE rn <= 3
ORDER BY draft_year;
```

**Result:** LeBron (2003 - 21 years!), Brook Lopez (2008), Steph Curry (2009) 👴
</details>

---

## 🏀 NBA Problems (Intermediate)

### **Problem 6: Triple-Double Threats - Best Playmakers Per Team**
Find the player with the most assists per game on each team (the floor general).

<details>
<summary>✅ Solution</summary>

```sql
SELECT player_name, team, position, assists_per_game
FROM (
    SELECT 
        player_name,
        team,
        position,
        assists_per_game,
        ROW_NUMBER() OVER (PARTITION BY team ORDER BY assists_per_game DESC) as rn
    FROM player_stats
) ranked
WHERE rn = 1
ORDER BY assists_per_game DESC;
```

**Top Playmaker:** Luka (9.8 APG), Nikola Jokic (9.0 APG) 🎯
</details>

---

### **Problem 7: Iron Man Award - Most Games Played Per Team**
Find the most durable player (most games played) on each team.

<details>
<summary>✅ Solution</summary>

```sql
SELECT player_name, team, games_played
FROM (
    SELECT 
        player_name,
        team,
        games_played,
        ROW_NUMBER() OVER (PARTITION BY team ORDER BY games_played DESC) as rn
    FROM player_stats
) ranked
WHERE rn = 1
ORDER BY games_played DESC;
```

**Iron Men:** Austin Reaves (82 games - played every game!) 💪
</details>

---

### **Problem 8: Position Rankings - Top 2 Point Guards**
Find the top 2 point guards in the league by scoring.

<details>
<summary>💡 Hint</summary>
Add WHERE position = 'PG' before the window function, or filter in outer query
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT player_name, team, points_per_game
FROM (
    SELECT 
        player_name,
        team,
        points_per_game,
        ROW_NUMBER() OVER (ORDER BY points_per_game DESC) as rn
    FROM player_stats
    WHERE position = 'PG'
) ranked
WHERE rn <= 2;
```

**Top PGs:** Luka Doncic (33.9), Stephen Curry (26.4) 🎯
</details>

---

### **Problem 9: All-Around Excellence - Top 5 in Points + Rebounds**
Find top 5 players by combined points and rebounds per game.

<details>
<summary>💡 Hint</summary>
ORDER BY (points_per_game + rebounds_per_game) DESC
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT player_name, team, points_per_game, rebounds_per_game,
       (points_per_game + rebounds_per_game) as total_production
FROM (
    SELECT 
        player_name,
        team,
        points_per_game,
        rebounds_per_game,
        ROW_NUMBER() OVER (ORDER BY (points_per_game + rebounds_per_game) DESC) as rn
    FROM player_stats
) ranked
WHERE rn <= 5
ORDER BY rn;
```

**All-Around Stars:** Giannis, Luka, AD, Nikola Jokic... 🌟
</details>

---

### **Problem 10: Second Fiddle - #2 Scorers Per Team**
Find the second-best scorer on each team (the Robin to their Batman).

<details>
<summary>✅ Solution</summary>

```sql
SELECT player_name, team, points_per_game
FROM (
    SELECT 
        player_name,
        team,
        points_per_game,
        ROW_NUMBER() OVER (PARTITION BY team ORDER BY points_per_game DESC) as rn
    FROM player_stats
) ranked
WHERE rn = 2
ORDER BY points_per_game DESC;
```

**Best #2 Options:** Kyrie (25.6), Damian Lillard (24.3), AD (24.7) 🦸‍♂️
</details>

---

## 🏈 NFL Problems

### **Problem 11: Blowout Alert - Biggest Wins**
Find the 3 games with the largest point differential (biggest blowouts).

<details>
<summary>💡 Hint</summary>
Calculate ABS(home_score - away_score) and order by that
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT home_team, away_team, home_score, away_score,
       ABS(home_score - away_score) as point_differential
FROM (
    SELECT 
        home_team,
        away_team,
        home_score,
        away_score,
        ROW_NUMBER() OVER (ORDER BY ABS(home_score - away_score) DESC) as rn
    FROM game_results
) ranked
WHERE rn <= 3
ORDER BY point_differential DESC;
```

**Biggest Blowout:** Cowboys 40, Giants 0 (40-point differential!) 💥
</details>

---

### **Problem 12: Highest-Scoring Games**
Find the top 5 highest-scoring games (total points).

<details>
<summary>💡 Hint</summary>
ORDER BY (home_score + away_score) DESC
</details>

<details>
<summary>✅ Solution</summary>

```sql
SELECT home_team, away_team, home_score, away_score,
       (home_score + away_score) as total_points
FROM (
    SELECT 
        home_team,
        away_team,
        home_score,
        away_score,
        ROW_NUMBER() OVER (ORDER BY (home_score + away_score) DESC) as rn
    FROM game_results
) ranked
WHERE rn <= 5
ORDER BY total_points DESC;
```

**Highest Scoring:** Saints 44, Cowboys 19 (63 total points) 🔥
</details>

---

### **Problem 13: Home Field Advantage - Best Home Performances Per Week**
Find the highest-scoring home team in each week.

<details>
<summary>✅ Solution</summary>

```sql
SELECT week, home_team, home_score
FROM (
    SELECT 
        week,
        home_team,
        home_score,
        ROW_NUMBER() OVER (PARTITION BY week ORDER BY home_score DESC) as rn
    FROM game_results
) ranked
WHERE rn = 1
ORDER BY week;
```

**Week 1 Winner:** Cowboys (40 points at home) 🏟️
</details>

---

### **Problem 14: Attendance Kings - Most Popular Games**
Find the 3 games with the highest attendance.

<details>
<summary>✅ Solution</summary>

```sql
SELECT home_team, away_team, attendance, game_date
FROM (
    SELECT 
        home_team,
        away_team,
        attendance,
        game_date,
        ROW_NUMBER() OVER (ORDER BY attendance DESC) as rn
    FROM game_results
) ranked
WHERE rn <= 3
ORDER BY attendance DESC;
```

**Most Popular:** Cowboys games (93,000 attendance - America's Team!) 🇺🇸
</details>

---

### **Problem 15: Nail-Biters - Closest Games**
Find the 5 closest games (smallest point differential).

<details>
<summary>✅ Solution</summary>

```sql
SELECT home_team, away_team, home_score, away_score,
       ABS(home_score - away_score) as point_differential
FROM (
    SELECT 
        home_team,
        away_team,
        home_score,
        away_score,
        ROW_NUMBER() OVER (ORDER BY ABS(home_score - away_score) ASC) as rn
    FROM game_results
) ranked
WHERE rn <= 5
ORDER BY point_differential;
```

**Closest Game:** Ravens 28, Cowboys 25 (3-point game!) 😰
</details>

---

## 🏆 Advanced Challenges

### **Challenge 1: Dynasty Building - Best Young Core**
Find the top 3 scorers who were drafted in 2015 or later (young stars).

<details>
<summary>✅ Solution</summary>

```sql
SELECT player_name, team, draft_year, points_per_game,
       2024 - draft_year as years_in_league
FROM (
    SELECT 
        player_name,
        team,
        draft_year,
        points_per_game,
        ROW_NUMBER() OVER (ORDER BY points_per_game DESC) as rn
    FROM player_stats
    WHERE draft_year >= 2015
) ranked
WHERE rn <= 3
ORDER BY points_per_game DESC;
```

**Young Stars:** Luka (2018), Jayson Tatum (2017), Jaylen Brown (2016) 🌟
</details>

---

### **Challenge 2: Efficiency Kings - Best Scorers Who Play Most Games**
Find players in top 10 for PPG who also played 70+ games (availability matters!).

<details>
<summary>✅ Solution</summary>

```sql
SELECT player_name, team, points_per_game, games_played
FROM (
    SELECT 
        player_name,
        team,
        points_per_game,
        games_played,
        ROW_NUMBER() OVER (ORDER BY points_per_game DESC) as rn
    FROM player_stats
    WHERE games_played >= 70
) ranked
WHERE rn <= 10
ORDER BY points_per_game DESC;
```

**Iron Men Scorers:** Giannis, Steph, Jayson Tatum (elite + durable) 💪
</details>

---

### **Challenge 3: Home vs Away - Best Road Performances**
Find the top 3 away teams by points scored (road warriors).

<details>
<summary>✅ Solution</summary>

```sql
SELECT away_team, away_score, home_team, game_date
FROM (
    SELECT 
        away_team,
        away_score,
        home_team,
        game_date,
        ROW_NUMBER() OVER (ORDER BY away_score DESC) as rn
    FROM game_results
) ranked
WHERE rn <= 3
ORDER BY away_score DESC;
```

**Best Road Performance:** Ravens (20), Eagles (20), Chiefs (20) 🛣️
</details>

---

## 🎯 Your Practice Routine

**Daily Sports SQL (15 minutes):**
1. Pick 3 random problems
2. Write query from memory
3. Test in DB Fiddle
4. Check solution

**Weekly Challenge:**
- Complete all 15 problems
- Track your accuracy
- Aim for 80%+ correct on first try

---

## 🏅 Achievement Unlocked!

Once you can solve these confidently, you've mastered `ROW_NUMBER()`! 

**Next level:** Learn `RANK()` and `DENSE_RANK()` for handling ties in sports rankings!

---

## 💡 Why Sports Data?

- **More engaging** than employee tables
- **Real-world scenarios** you actually care about
- **Easier to remember** patterns (top scorer = ORDER BY DESC)
- **Fun to explore** - discover interesting stats!

Now go crush these problems like Luka crushing defenses! 🏀💪
