"""
Detailed breakdown to verify late delivery calculations
"""
import pandas as pd

# Load the data
fog_df = pd.read_csv('fact_orders_grubhub.csv')

# Convert to datetime
fog_df['order_datetime'] = pd.to_datetime(fog_df['order_date'] + ' ' + fog_df['order_time'])
fog_df['picked_datetime'] = pd.to_datetime(fog_df['order_date'] + ' ' + fog_df['order_picked_time'])

# Calculate prep + pickup time in minutes
fog_df['prep_pickup_time'] = (fog_df['picked_datetime'] - fog_df['order_datetime']).dt.total_seconds() / 60

# Calculate total delivery time
fog_df['total_delivery_time'] = fog_df['prep_pickup_time'] + fog_df['delivery_duration']

# Mark late deliveries
fog_df['is_late'] = fog_df['total_delivery_time'] > 45

# Show detailed breakdown
print("=" * 100)
print("DETAILED BREAKDOWN OF ALL ORDERS")
print("=" * 100)

columns_to_show = [
    'order_id', 'road_traffic', 'order_time', 'order_picked_time', 
    'prep_pickup_time', 'delivery_duration', 'total_delivery_time', 'is_late'
]

pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

print(fog_df[columns_to_show].to_string(index=False))

print("\n" + "=" * 100)
print("SUMMARY BY TRAFFIC CONDITION")
print("=" * 100)

result = fog_df.groupby('road_traffic').agg(
    total_orders=('is_late', 'count'),
    late_orders=('is_late', 'sum'),
    avg_total_time=('total_delivery_time', 'mean')
).reset_index()

result['late_percentage'] = (result['late_orders'] / result['total_orders'] * 100).round(2)
result['avg_total_time'] = result['avg_total_time'].round(2)

print(result.to_string(index=False))

print("\n" + "=" * 100)
print("VERIFICATION: Let's check a few specific orders manually")
print("=" * 100)

# Check first order from each traffic type
for traffic in ['Jam', 'High', 'Medium', 'Low']:
    sample = fog_df[fog_df['road_traffic'] == traffic].iloc[0]
    print(f"\n{traffic} Traffic - Order {sample['order_id']}:")
    print(f"  Order time:     {sample['order_time']}")
    print(f"  Picked time:    {sample['order_picked_time']}")
    print(f"  Prep+Pickup:    {sample['prep_pickup_time']:.1f} minutes")
    print(f"  Delivery dur:   {sample['delivery_duration']} minutes")
    print(f"  TOTAL:          {sample['total_delivery_time']:.1f} minutes")
    print(f"  Is Late (>45)?  {sample['is_late']} {'✓ LATE' if sample['is_late'] else '✓ ON TIME'}")
