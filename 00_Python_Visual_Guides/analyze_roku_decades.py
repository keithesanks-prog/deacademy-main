import pandas as pd

# 1. Load Data
df = pd.read_csv('dim_titles_roku_python.csv')

# 2. Calculate Decade
# 1952 // 10 = 195. 195 * 10 = 1950.
df['decade'] = (df['release_year'] // 10) * 10

# 3. Handle Duplicates
# The prompt says "Assume there are multiple Records". We should drop exact duplicates or keep the highest score.
# Here we strip exact duplicates first.
df = df.drop_duplicates(subset=['title_name', 'release_year', 'imdb_score'])

# 4. Find Best Movie per Decade
# Sort by Decade ASC, Score DESC (Best movies at top of each decade chunk)
df_sorted = df.sort_values(['decade', 'imdb_score'], ascending=[True, False])

# Group by Decade and take the first one (which is the max score)
best_per_decade = df_sorted.groupby('decade').head(1).reset_index(drop=True)

# 5. Format Output
# Columns: decade, title_name, age_certification, production_countries, score
best_per_decade = best_per_decade.rename(columns={'imdb_score': 'score'})
final_cols = ['decade', 'title_name', 'age_certification', 'production_countries', 'score']
final_output = best_per_decade[final_cols]

print("--- Best Movies per Decade (1950s+) ---")
print(final_output)
