import pandas as pd

# Load the data
df = pd.read_csv('fact_orders_grubhub.csv')
print(f"Loaded {len(df)} orders.")

# 1. Convert Time Columns to Datetime
# We need to combine 'order_date' with the time strings to get full datetime objects
order_dt = pd.to_datetime(df['order_date'] + ' ' + df['order_time'])
picked_dt = pd.to_datetime(df['order_date'] + ' ' + df['order_picked_time'])

# 2. Convert Duration to Timedelta
# CRITICAL: Must specify unit='m' so 45 becomes 45 minutes, not 45 nanoseconds!
delivery_duration_td = pd.to_timedelta(df['delivery_duration'], unit='m')

# 3. Calculate Total Time
# Formula: (Picked Time - Order Time) + Delivery Duration
#          (Prep Time)                + (Drive Time)
df['total_time_diff'] = (picked_dt - order_dt) + delivery_duration_td

# Convert to minutes for easy reading/filtering
df['total_minutes'] = df['total_time_diff'].dt.total_seconds() / 60

print("\n--- CALCULATION SAMPLE ---")
print(df[['order_time', 'order_picked_time', 'delivery_duration', 'total_minutes']].head())

# 4. Filter for Late Orders (> 45 minutes)
late_orders = df[df['total_minutes'] > 45]

print(f"\n--- RESULTS ---")
print(f"Total Late Orders: {len(late_orders)}")
print(f"Percentage Late:   {(len(late_orders) / len(df) * 100):.1f}%")

if len(late_orders) > 0:
    print("\nSAMPLE LATE ORDERS:")
    print(late_orders[['order_id', 'total_minutes', 'road_traffic']].head())
else:
    print("\nNo late orders found. Check logic!")
