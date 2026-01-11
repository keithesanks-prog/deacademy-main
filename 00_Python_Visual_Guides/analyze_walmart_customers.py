import pandas as pd

# 1. Load Data
df_cust = pd.read_csv('dim_customers_walmart_python.csv')
df_trans = pd.read_csv('fact_daily_transactions_walmart_python.csv')

# 2. Identify Top 10 Oldest Customers
# Convert 'customer_since' to datetime
df_cust['customer_since_dt'] = pd.to_datetime(df_cust['customer_since'], format='%m/%d/%y')

# Rank by Date (Ascending = Oldest First)
df_cust['oldest_customer'] = df_cust['customer_since_dt'].rank(method='min', ascending=True).astype(int)

# Sort and take Top 10
top_10_oldest = df_cust.sort_values('oldest_customer').head(10)

# 3. Calculate Transaction Totals
# We need 'Total Sales' = quantity * unit_price
df_trans['sales_amount'] = df_trans['quantity_sold'] * df_trans['unit_price']

# 4. Aggregate Transactions by Customer
# We sum up Quantity and Sales Amount
trans_agg = df_trans.groupby('customer_id')[['quantity_sold', 'sales_amount']].sum().reset_index()
trans_agg.rename(columns={'quantity_sold': 'total_quantities', 'sales_amount': 'total_sales'}, inplace=True)

# 5. Join Top 10 Customers with Aggregated Transactions
# Use Left Join: We want all of the Top 10 customers, even if they have 0 sales.
final_df = pd.merge(top_10_oldest, trans_agg, on='customer_id', how='left')

# Fill NaN with 0 for customers with no transactions
final_df['total_quantities'] = final_df['total_quantities'].fillna(0)
final_df['total_sales'] = final_df['total_sales'].fillna(0)

# 6. Format Output
# Columns: customer_name, oldest_customer, total_quantities, total_sales
result = final_df[['customer_name', 'oldest_customer', 'total_quantities', 'total_sales']]

print("--- Top 10 Oldest Walmart Customers & Their Sales ---")
print(result)
