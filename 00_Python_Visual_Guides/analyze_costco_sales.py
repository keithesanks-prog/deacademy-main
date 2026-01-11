import pandas as pd

# 1. Load Data
sales_df = pd.read_csv('fact_weekly_sales_costco_python.csv')
dept_df = pd.read_csv('dim_departments_costco_python.csv')

# 2. Filter for 2021
# Convert date column to datetime objects
sales_df['week_date_dt'] = pd.to_datetime(sales_df['week_date'], format='%m/%d/%y')
# Select only rows where year is 2021
sales_2021 = sales_df[sales_df['week_date_dt'].dt.year == 2021]

# 3. Merge with Departments to get Names
merged_df = pd.merge(sales_2021, dept_df, on='dept_id', how='left')

# 4. Calculate Average Sales per Department
# Group by Name, mean of Sales
avg_sales = merged_df.groupby('dept_name')['weekly_sales'].mean().reset_index()

# 5. Format Output
# Columns: dept_name, avg_sales
avg_sales.columns = ['dept_name', 'avg_sales']

print("--- Department-wise Average Sales in 2021 ---")
print(avg_sales)
