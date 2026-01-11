import pandas as pd
import numpy as np

# Load Data
print("Command: df = pd.read_csv('dim_job_listings_linkedin_python.csv')")
df = pd.read_csv('dim_job_listings_linkedin_python.csv')

# keep only relevant columns for the demo
print("Command: df = df[['company_name', 'company_location', 'company_headquarter', 'job_rating']]")
df = df[['company_name', 'company_location', 'company_headquarter', 'job_rating']]
print(df.head(10))

# ---------------------------------------------------------
# Step 1: Filter Companies that have at least one HQ listing
# ---------------------------------------------------------
print("\nCommand: companies_with_hq = df[df['company_location'] == df['company_headquarter']]['company_name'].unique()")
companies_with_hq = df[df['company_location'] == df['company_headquarter']]['company_name'].unique()
print(f"Result: {companies_with_hq}")

print("\nCommand: df = df[df['company_name'].isin(companies_with_hq)]")
df = df[df['company_name'].isin(companies_with_hq)]
print(df.head(10))

# ---------------------------------------------------------
# Step 2: Create Helper Columns for Ratings
# ---------------------------------------------------------
# CORRECTION: The user snippet used '0', which incorrectly drags down the average.
# We use 'np.nan' so that the mean() function ignores non-matches.

print("\nCommand: df['base_location_rating'] = df['job_rating'].where(df['company_location'] == df['company_headquarter'], np.nan)")
df['base_location_rating'] = df['job_rating'].where(df['company_location'] == df['company_headquarter'], np.nan)

print("Command: df['other_location_rating'] = df['job_rating'].where(df['company_location'] != df['company_headquarter'], np.nan)")
df['other_location_rating'] = df['job_rating'].where(df['company_location'] != df['company_headquarter'], np.nan)

print(df[['company_name', 'base_location_rating', 'other_location_rating']].head(10))

# ---------------------------------------------------------
# Step 3: Group and Average
# ---------------------------------------------------------
print("\nCommand: df = df.groupby('company_name')[['base_location_rating', 'other_location_rating']].mean().round(2)")
df = df.groupby('company_name')[['base_location_rating', 'other_location_rating']].mean().round(2)
print(df)

# ---------------------------------------------------------
# Step 4: Final Filter (Other >= Base)
# ---------------------------------------------------------
print("\nCommand: df = df[df['other_location_rating'] >= df['base_location_rating']]")
df = df[df['other_location_rating'] >= df['base_location_rating']]

print("Command: df = df.sort_values('other_location_rating', ascending=False)")
df = df.sort_values('other_location_rating', ascending=False)

print("Command: df = df[['other_location_rating', 'base_location_rating']]")
df = df[['other_location_rating', 'base_location_rating']]

print(df)
