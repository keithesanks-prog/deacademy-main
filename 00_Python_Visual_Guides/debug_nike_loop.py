import pandas as pd
import numpy as np

# Load Data
df_prod = pd.read_csv('dim_product_nike_python.csv')
df_cat = pd.read_csv('dim_category_nike_python.csv')
df = pd.merge(df_prod, df_cat, on='category_id', how='left')
df['order_year'] = pd.to_datetime(df['order_date'], format='%m/%d/%y').dt.year

# Create summary (Mean Review)
summary = df.groupby(["order_year", "gender", "category_name"])["product_reviews"].mean().reset_index()
# Sort High to Low (Best reviewed on top)
summary = summary.sort_values(by=['order_year', 'gender', 'product_reviews'], ascending=[True, True, False])

print("--- Available Gender Values in Data ---")
print(summary['gender'].unique()) 
# Expected: ['Men', 'Women'] in the CSV I created earlier

results = []
years = summary['order_year'].unique()

print("\n--- RUNNING USER LOOP ---")
for year in years:
    row = {'order_year': year}
    
    # USER BUG 1: List values ['men', 'woman'] likely do not match 'Men', 'Women' in data
    for g in ['men', 'woman']: 
        
        # This filter likely returns Empty DataFrame because 'men' != 'Men'
        subset = summary[(summary['order_year'] == year) & (summary['gender'] == g)]
        
        if not subset.empty:
            row[f'{g.title()}_Top_Category'] = subset.iloc[0]['category_name']
            row[f'{g.title()}_Bottom_Category'] = subset.iloc[-1]['category_name'] if len(subset) > 1 else np.nan
        else:
            row[f'{g.title()}_Top_Category'] = np.nan
            row[f'{g.title()}_Bottom_Category'] = np.nan
        
        # USER BUG 2: This append is INSIDE the loop. 
        # It appends the row TWICE (once partially full, once fully full).
        results.append(row)

results_df = pd.DataFrame(results)
print("\n--- RESULT (Notice duplicates and likely NaNs) ---")
print(results_df)
