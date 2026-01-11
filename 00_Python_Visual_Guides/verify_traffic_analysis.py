import pandas as pd

# Load Data
df = pd.read_csv('fact_orders_grubhub.csv')

# 1. Calculate Total Time (The logic we just fixed)
df['total_minutes'] = (
    (pd.to_datetime(df['order_date'] + ' ' + df['order_picked_time']) - 
     pd.to_datetime(df['order_date'] + ' ' + df['order_time'])) + 
    pd.to_timedelta(df['delivery_duration'], unit='m')
).dt.total_seconds() / 60

# 2. Flag Late Orders
df['is_late'] = df['total_minutes'] > 45
print(f"Total Late Orders: {df['is_late'].sum()}")

# 3. Group by Traffic and Calculate %
# The mean of a boolean column is the % occurring!
traffic_stats = df.groupby('road_traffic')['is_late'].mean() * 100
traffic_stats = traffic_stats.round(1) # Round to 1 decimal

print("\n--- Late Orders by Traffic Condition (%) ---")
print(traffic_stats)

print("\n--- Detailed Count ---")
detailed = df.groupby('road_traffic')['is_late'].agg(['count', 'sum'])
detailed.columns = ['Total Orders', 'Late Orders']
print(detailed)
