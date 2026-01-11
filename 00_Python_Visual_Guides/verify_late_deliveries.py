"""
Calculate percentage of late deliveries (>45 min total) by road traffic condition
"""
import pandas as pd

# Load the data
fog_df = pd.read_csv('fact_orders_grubhub.csv')

print("=" * 70)
print("LATE DELIVERY ANALYSIS (>45 minutes total)")
print("=" * 70)

# Convert to datetime
fog_df['order_datetime'] = pd.to_datetime(
    fog_df['order_date'] + ' ' + fog_df['order_time'],
    format='%m/%d/%y %H:%M:%S'
)
fog_df['picked_datetime'] = pd.to_datetime(
    fog_df['order_date'] + ' ' + fog_df['order_picked_time'],
    format='%m/%d/%y %H:%M:%S'
)

# Calculate TOTAL delivery time (prep + pickup + driving)
fog_df['total_delivery_time'] = (
    (fog_df['picked_datetime'] - fog_df['order_datetime']).dt.total_seconds() / 60
    + fog_df['delivery_duration']
)

# Identify late deliveries (> 45 minutes)
fog_df['is_late'] = fog_df['total_delivery_time'] > 45

# Calculate percentage by road traffic
result = (
    fog_df.groupby('road_traffic')
    .agg(
        total_orders=('order_id', 'count'),
        late_orders=('is_late', 'sum'),
        avg_total_time=('total_delivery_time', 'mean')
    )
    .reset_index()
)

result['late_percentage'] = (result['late_orders'] / result['total_orders'] * 100).round(2)
result['avg_total_time'] = result['avg_total_time'].round(2)

# Sort by late percentage descending
result = result.sort_values('late_percentage', ascending=False)

print("\n📊 RESULTS BY TRAFFIC CONDITION:")
print(result.to_string(index=False))

print("\n\n✅ Expected pattern: Jam should have highest %, followed by High, Medium, Low")
