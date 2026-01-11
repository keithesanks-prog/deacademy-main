import pandas as pd
import numpy as np

# 1. Load Data
df_cat = pd.read_csv('dim_category_nike_python.csv')
df_prod = pd.read_csv('dim_product_nike_python.csv')

# 2. Merge and Date
df = pd.merge(df_prod, df_cat, on='category_id', how='left')
df['order_year'] = pd.to_datetime(df['order_date'], format='%m/%d/%y').dt.year

# 3. Aggregate (Mean Reviews)
summary = df.groupby(["order_year", "gender", "category_name"])["product_reviews"].mean().reset_index()

# 4. Sort: High Reviews first (Top), Low Reviews last (Bottom)
summary = summary.sort_values(by=['order_year', 'gender', 'product_reviews'], ascending=[True, True, False])

# 5. Logic Loop
results = []
years = sorted(summary['order_year'].unique())

for year in years:
    row = {'order_year': year}
    
    # FIX: Use exact string match for the data ['Men', 'Women']
    # The user wanted columns like "Men_..." and "Woman_..." (Singular 'Woman' per request? or 'Women'?)
    # User prompt said: "Woman_Top_Ctaegory" (sic). 
    # I will map 'Women' (Data) -> 'Woman' (Column Name) to be safe/consistent with request.
    
    gender_map = {'Men': 'Men', 'Women': 'Woman'} 
    
    for g_data, g_col in gender_map.items():
        subset = summary[(summary['order_year'] == year) & (summary['gender'] == g_data)]
        
        if not subset.empty:
            # First item is TOP (Highest Mean)
            row[f'{g_col}_Top_Category'] = subset.iloc[0]['category_name']
            
            # Last item is BOTTOM (Lowest Mean), only if strictly more than 1 item
            if len(subset) > 1:
                row[f'{g_col}_Bottom_Category'] = subset.iloc[-1]['category_name']
            else:
                row[f'{g_col}_Bottom_Category'] = np.nan
        else:
            row[f'{g_col}_Top_Category'] = np.nan
            row[f'{g_col}_Bottom_Category'] = np.nan
            
    # FIX: Append OUTSIDE the inner loop
    results.append(row)

# 6. Create DataFrame
results_df = pd.DataFrame(results)

# 7. Reorder Columns per request
# "order_year, Men_Bottom_Category, Men_Top_Category, Woman_Bottom_Category, Woman_Top_Category"
wanted_cols = ['order_year', 'Men_Bottom_Category', 'Men_Top_Category', 'Woman_Bottom_Category', 'Woman_Top_Category']
results_df = results_df[wanted_cols]

print("--- Final Nike Ranking Report ---")
print(results_df)
