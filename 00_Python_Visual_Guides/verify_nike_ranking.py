import pandas as pd

# Load
df_cat = pd.read_csv('dim_category_nike_python.csv')
df_prod = pd.read_csv('dim_product_nike_python.csv')

# Merge
df = pd.merge(df_prod, df_cat, on='category_id', how='left')

# Extract Year
df['order_year'] = pd.to_datetime(df['order_date']).dt.year

# Aggregation: Mean Review by [Year, Gender, Category]
grouped = df.groupby(['order_year', 'gender', 'category_name'])['product_reviews'].mean().reset_index()

print("--- Grouped Data Snapshot ---")
print(grouped.head())

# Simple verification: Do we have Men/Women for 2020?
y2020 = grouped[grouped['order_year'] == 2020]
print("\n--- 2020 Data ---")
print(y2020)

if not y2020.empty:
    print("\nSUCCESS: Data exists for 2020 aggregation.")
else:
    print("\nFAILURE: No 2020 data found.")
