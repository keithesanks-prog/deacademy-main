import pandas as pd

# 1. Load Data
df_titles = pd.read_csv('dim_titles_roku_python.csv')

# 2. Filter for MOVIES only (per instructions "count of movies")
df_movies = df_titles[df_titles['type'] == 'MOVIE'].copy()

# 3. Parse Genres
# Input format: "[horror, thriller]"
# Logic: Strip brackets, split by comma
df_movies['genres'] = df_movies['genres'].apply(
    lambda x: [item.strip() for item in x.strip("[]").split(',') if item.strip()]
)

# 4. Explode
df_exploded = df_movies.explode('genres')

# 5. Count Frequencies
# Value Counts is a shortcut for GroupBy -> Size -> Sort Descending
genre_counts = df_exploded['genres'].value_counts().reset_index()

# 6. Rename Columns
# "genre name and total shows" -> "genre", "frequency"
genre_counts.columns = ['genre', 'frequency']

# 7. Get Top 10
top_10_genres = genre_counts.head(10)

print("--- Top 10 Genres (Movies) ---")
print(top_10_genres)
