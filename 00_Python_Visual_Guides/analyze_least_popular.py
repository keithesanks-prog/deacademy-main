import pandas as pd
import ast

# 1. Load the DataFrames
# In a real scenario, you might load from SQL or other sources.
# Here we load the CSVs we just created.
dim_restaurants = pd.read_csv('dim_restaurants_grubhub_python.csv')
fact_orders = pd.read_csv('fact_orders_grubhub_python.csv')

# 2. Merge Orders with Restaurant Info
# We need to know which restaurant (and thus which cuisines) are associated with each order.
df_merged = pd.merge(fact_orders, dim_restaurants, on='restaurant_id', how='left')

# 3. Process Cuisines
# The Cuisines are stored as a string looking like: "[Asian, Vegan, Vegetarian]"
# We need to parse this custom format (strip brackets, split by comma)
df_merged['restaurant_cuisine_offered'] = df_merged['restaurant_cuisine_offered'].apply(
    lambda x: [item.strip() for item in x.strip("[]").split(',')]
)

# 4. Explode the Cuisines
# If an order has 2 cuisines (Asian, Vegan), we split it into 2 rows.
# This way we can count "Asian" orders and "Vegan" orders separately.
df_exploded = df_merged.explode('restaurant_cuisine_offered')

# 5. Count Cuisines by Order Type
# Group by [Order Type, Cuisine] and count how many times they appear.
cuisine_counts = df_exploded.groupby(['order_type', 'restaurant_cuisine_offered']).size().reset_index(name='count')

# 6. Find the Least Popular
# Sort by count (Ascending = Smallest First)
# CRITICAL FIX: Add 'restaurant_cuisine_offered' as a tie-breaker so the order doesn't jump around randomly.
cuisine_counts_sorted = cuisine_counts.sort_values(['order_type', 'count', 'restaurant_cuisine_offered'], ascending=[True, True, True])

# Take the top 3 for each group (which are the smallest counts because we sorted ascending)
least_popular = cuisine_counts_sorted.groupby('order_type').head(3)

# 7. Format the Output
# The user wants "Order Type" and "Least Popular Cuisines" (Names)
# We group the 3 names back into a list/string for display
final_output = least_popular.groupby('order_type')['restaurant_cuisine_offered'].apply(list).reset_index()
final_output.columns = ['order_type', 'least_popular_cuisines']

print("--- Final Result: Least Popular Cuisines per Order Type ---")
print(final_output)

# Optional: Verify by printing the full counts
# print("\n--- Reference: All Counts ---")
# print(cuisine_counts_sorted)
