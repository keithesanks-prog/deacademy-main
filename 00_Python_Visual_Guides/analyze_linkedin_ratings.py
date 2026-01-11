import pandas as pd

# 1. Load Data
df = pd.read_csv('dim_job_listings_linkedin_python.csv')

# 2. Identify Location Type (Base vs Other)
# Base Location = Matches Headquarter
df['is_headquarter'] = df['company_location'] == df['company_headquarter']

# 3. Calculate Average Ratings per Company per Type
# We want to pivot this: One row per Company, with columns for BaseRating and OtherRating
# First, groupby Company and IsHQ
ratings = df.groupby(['company_name', 'is_headquarter'])['job_rating'].mean().unstack()

# Rename columns for clarity (False -> Other, True -> Base)
ratings.columns = ['other_location_rating', 'base_location_rating']

# 4. Filter
# Condition 1: Must have a Base Listing (base_location_rating is not NaN)
has_hq_listings = ratings['base_location_rating'].notna()

# Condition 2: Other Rating > Base Rating
better_elsewhere = ratings['other_location_rating'] > ratings['base_location_rating']

# Apply filters
final_companies = ratings[has_hq_listings & better_elsewhere].reset_index()

# 5. Format Output
# Columns: base_location_rating, other_location_rating, company_name
# (Note: 'company_name' is currently a column after reset_index)
final_output = final_companies[['base_location_rating', 'other_location_rating', 'company_name']]

# Round to 2 decimal places? (Good practice for ratings)
final_output['base_location_rating'] = final_output['base_location_rating'].round(2)
final_output['other_location_rating'] = final_output['other_location_rating'].round(2)

print("--- Companies with Better Ratings Outside HQ ---")
print(final_output)
