import pandas as pd

# Load Data (files verified to exist from previous steps)
df = pd.read_csv("dim_restaurants_grubhub_python.csv")
fact_orders = pd.read_csv("fact_orders_grubhub_python.csv")

# User Code Logic
df['restaurant_cuisine_offered'] = df['restaurant_cuisine_offered'].apply(lambda x: x.strip('[]').split(','))

df_exploded = df.explode('restaurant_cuisine_offered')

df_exploded = pd.merge(df_exploded, fact_orders, on='restaurant_id', how='left')
df_exploded.rename(columns={'order_id': 'total_orders'}, inplace=True)

# THE ERROR LINE
# 1. 'df' is just restaurants. It does NOT have 'order_type' (that's in fact_orders/df_exploded)
# 2. 'total_orers' is a typo
result = df.sort_values(by=["order_type", "total_orers"]).groupby("order_type").head(3).reset_index(drop=True)

result.rename(columns={'cuisine_category':'least_popular_cuisines'}, inplace=True)
result = result[['order_type', 'least_popular_cuisines']]
print(result)
