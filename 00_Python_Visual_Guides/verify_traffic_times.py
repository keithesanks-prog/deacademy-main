"""
Verify that delivery times make sense by traffic condition
"""
import pandas as pd

# Load the data
fog_df = pd.read_csv('fact_orders_grubhub.csv')

# Calculate average delivery duration by traffic condition
avg_by_traffic = (
    fog_df.groupby('road_traffic')['delivery_duration']
    .agg(['mean', 'min', 'max', 'count'])
    .round(2)
    .sort_values('mean', ascending=False)
)

print("=" * 60)
print("AVERAGE DELIVERY DURATION BY TRAFFIC CONDITION")
print("=" * 60)
print(avg_by_traffic)
print("\n✅ Expected order: Jam > High > Medium > Low")
