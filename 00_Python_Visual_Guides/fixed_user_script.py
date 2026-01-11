import pandas as pd

df = pd.read_csv("dim_restaurants_grubhub_python.csv")
fact_orders = pd.read_csv("fact_orders_grubhub_python.csv")

# 1. Parse string lists
df['restaurant_cuisine_offered'] = df['restaurant_cuisine_offered'].apply(lambda x: x.strip('[]').split(','))

# 2. Explode
df_exploded = df.explode('restaurant_cuisine_offered')
# CLEANUP: Remove whitespace from cuisine names after splitting (surrounding AND internal)
# " Pad Thai " -> "PadThai"
df_exploded['restaurant_cuisine_offered'] = df_exploded['restaurant_cuisine_offered'].str.strip().str.replace(' ', '')

# 3. Merge
df_exploded = pd.merge(df_exploded, fact_orders, on='restaurant_id', how='left')

# --- MISSING STEP: YOU NEED TO COUNT THE ORDERS ---
# You cannot find "Least Popular" without counting them first!
cuisine_counts = df_exploded.groupby(['order_type', 'restaurant_cuisine_offered']).size().reset_index(name='total_orders')

# 4. Sort
# FIX: Use 'cuisine_counts' (the new counted table), not 'df' (the original restaurant table)
# FIX: Typo 'total_orers' -> 'total_orders'
# FIX: Add secondary sort key for consistent ordering
result = cuisine_counts.sort_values(by=["order_type", "total_orders", "restaurant_cuisine_offered"])

# 5. Take Top 3 (which are the least popular because we sorted Ascending by default)
result = result.groupby("order_type").head(3).reset_index(drop=True)

# 6. Format
result.rename(columns={'restaurant_cuisine_offered':'least_popular_cuisines'}, inplace=True)
result = result[['order_type', 'least_popular_cuisines']]

print(result)
