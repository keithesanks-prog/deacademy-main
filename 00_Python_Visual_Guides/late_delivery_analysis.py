"""
GrubHub Late Delivery Analysis
================================

OBJECTIVE: Calculate the percentage of orders that took longer than 45 minutes
           to deliver, grouped by road traffic condition.

STEPS:
1. Load the orders data
2. Calculate delivery time (order_picked_time - order_time)
3. Identify late deliveries (> 45 minutes)
4. Calculate percentage of late deliveries per road traffic condition
"""

import pandas as pd

# Load the data
fog_df = pd.read_csv('fact_orders_grubhub.csv')

print("=" * 70)
print("LATE DELIVERY ANALYSIS BY ROAD TRAFFIC CONDITION")
print("=" * 70)

# ============================================================================
# STEP 1: Convert time columns to datetime
# ============================================================================
print("\n📊 STEP 1: Converting time columns to datetime...")

# Combine date and time for proper datetime conversion
fog_df['order_datetime'] = pd.to_datetime(
    fog_df['order_date'] + ' ' + fog_df['order_time'],
    format='%m/%d/%y %H:%M:%S'
)

fog_df['picked_datetime'] = pd.to_datetime(
    fog_df['order_date'] + ' ' + fog_df['order_picked_time'],
    format='%m/%d/%y %H:%M:%S'
)

print("✅ Time columns converted")

# ============================================================================
# STEP 2: Calculate delivery duration in minutes
# ============================================================================
print("\n⏱️ STEP 2: Calculating delivery duration...")

fog_df['delivery_time_minutes'] = (
    (fog_df['picked_datetime'] - fog_df['order_datetime']).dt.total_seconds() / 60
)

print(f"✅ Delivery times calculated")
print(f"\nSample delivery times:")
print(fog_df[['order_id', 'road_traffic', 'delivery_time_minutes']].head(10))

# ============================================================================
# STEP 3: Identify late deliveries (> 45 minutes)
# ============================================================================
print("\n\n🚨 STEP 3: Identifying late deliveries (> 45 minutes)...")

fog_df['is_late'] = fog_df['delivery_time_minutes'] > 45

late_count = fog_df['is_late'].sum()
total_count = len(fog_df)

print(f"✅ Late deliveries identified")
print(f"   Total orders: {total_count}")
print(f"   Late orders: {late_count}")
print(f"   Overall late %: {(late_count/total_count*100):.2f}%")

# ============================================================================
# STEP 4: Calculate percentage by road traffic condition
# ============================================================================
print("\n\n📈 STEP 4: Calculating late % by road traffic condition...")

result = (
    fog_df.groupby('road_traffic')
    .agg(
        total_orders=('order_id', 'count'),
        late_orders=('is_late', 'sum')
    )
    .reset_index()
)

# Calculate percentage
result['late_percentage'] = (result['late_orders'] / result['total_orders'] * 100).round(2)

print("\n✅ FINAL RESULT:")
print(result)

# ============================================================================
# BONUS: Show the actual late deliveries
# ============================================================================
print("\n\n📋 BONUS: List of Late Deliveries (> 45 minutes)")
print("=" * 70)

late_deliveries = fog_df[fog_df['is_late']][
    ['order_id', 'road_traffic', 'delivery_time_minutes', 'weather_condition']
].sort_values('delivery_time_minutes', ascending=False)

print(late_deliveries)

# ============================================================================
# ALTERNATIVE: More detailed breakdown
# ============================================================================
print("\n\n📊 DETAILED BREAKDOWN BY ROAD TRAFFIC")
print("=" * 70)

detailed = (
    fog_df.groupby('road_traffic')
    .agg(
        total_orders=('order_id', 'count'),
        late_orders=('is_late', 'sum'),
        avg_delivery_time=('delivery_time_minutes', 'mean'),
        max_delivery_time=('delivery_time_minutes', 'max')
    )
    .reset_index()
)

detailed['late_percentage'] = (detailed['late_orders'] / detailed['total_orders'] * 100).round(2)
detailed['avg_delivery_time'] = detailed['avg_delivery_time'].round(2)

print(detailed)

# ============================================================================
# KEY INSIGHTS
# ============================================================================
print("\n\n💡 KEY INSIGHTS")
print("=" * 70)

worst_traffic = result.loc[result['late_percentage'].idxmax()]
print(f"🚗 Worst road condition: {worst_traffic['road_traffic']}")
print(f"   Late percentage: {worst_traffic['late_percentage']}%")
print(f"   Late orders: {worst_traffic['late_orders']}/{worst_traffic['total_orders']}")

print("\n" + "=" * 70)
print("Analysis complete!")
print("=" * 70)
