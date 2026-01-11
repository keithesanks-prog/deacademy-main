"""
GrubHub Data Analysis - Loading Real CSV Files
===============================================

This script teaches you how to:
1. Load CSV files using pd.read_csv()
2. Explore the data structure
3. Join multiple tables
4. Perform aggregations
5. Answer business questions

FILES NEEDED (in the same directory):
- dim_delivery_person_grubhub.csv
- dim_restaurants_grubhub.csv
- fact_orders_grubhub.csv
"""

import pandas as pd

print("=" * 70)
print("GRUBHUB DATA ANALYSIS - WORKING WITH REAL CSV FILES")
print("=" * 70)

# ============================================================================
# STEP 1: Load the CSV Files
# ============================================================================
print("\n📂 STEP 1: Loading CSV Files...")
print("-" * 70)

# Load delivery person data
dim_delivery_person = pd.read_csv('dim_delivery_person_grubhub.csv')
print("✅ Loaded dim_delivery_person_grubhub.csv")

# Load restaurant data
dim_restaurants = pd.read_csv('dim_restaurants_grubhub.csv')
print("✅ Loaded dim_restaurants_grubhub.csv")

# Load orders data
fact_orders = pd.read_csv('fact_orders_grubhub.csv')
print("✅ Loaded fact_orders_grubhub.csv")

# ============================================================================
# STEP 2: Explore the Data
# ============================================================================
print("\n\n📊 STEP 2: Exploring the Data")
print("=" * 70)

print("\n--- Delivery Person Table ---")
print(f"Shape: {dim_delivery_person.shape} (rows, columns)")
print(f"Columns: {list(dim_delivery_person.columns)}")
print("\nFirst 5 rows:")
print(dim_delivery_person.head())

print("\n--- Restaurant Table ---")
print(f"Shape: {dim_restaurants.shape}")
print(f"Columns: {list(dim_restaurants.columns)}")
print("\nFirst 5 rows:")
print(dim_restaurants.head())

print("\n--- Orders Table ---")
print(f"Shape: {fact_orders.shape}")
print(f"Columns: {list(fact_orders.columns)}")
print("\nFirst 5 rows:")
print(fact_orders.head())

# ============================================================================
# STEP 3: Check Data Types
# ============================================================================
print("\n\n🔍 STEP 3: Checking Data Types")
print("=" * 70)
print("\nDelivery Person Data Types:")
print(dim_delivery_person.dtypes)

print("\nOrders Data Types:")
print(fact_orders.dtypes)

# ============================================================================
# STEP 4: Basic Data Exploration
# ============================================================================
print("\n\n📈 STEP 4: Basic Exploration")
print("=" * 70)

print("\n--- Summary Statistics for Delivery Persons ---")
print(dim_delivery_person.describe())

print("\n--- Unique City Types ---")
print(fact_orders['city_type'].unique())

print("\n--- Count of Orders per City Type ---")
print(fact_orders['city_type'].value_counts())

# ============================================================================
# QUESTION 1: Average Age and Rating per City Type
# ============================================================================
print("\n\n" + "=" * 70)
print("QUESTION 1: Average Age and Rating per City Type")
print("=" * 70)

print("\n🎯 GOAL: Calculate avg_age and avg_rating for each city_type")
print("\n💡 APPROACH:")
print("   1. Merge fact_orders with dim_delivery_person")
print("   2. Group by city_type")
print("   3. Calculate mean of Age and Ratings")
print("   4. Round to 2 decimals")

# Solution
result_q1 = (
    fact_orders.merge(dim_delivery_person, on='Delivery_person_ID')
    .groupby('city_type', as_index=False)
    .agg(
        avg_age=('Delivery_person_Age', 'mean'),
        avg_rating=('Delivery_person_Ratings', 'mean')
    )
    .round(2)
)

print("\n✅ ANSWER:")
print(result_q1)

# ============================================================================
# QUESTION 2: Average Delivery Duration per City Type
# ============================================================================
print("\n\n" + "=" * 70)
print("QUESTION 2: Average Delivery Duration per City Type")
print("=" * 70)

print("\n🎯 GOAL: Calculate avg_delivery_duration for each city_type")
print("\n💡 APPROACH:")
print("   1. Group fact_orders by city_type")
print("   2. Calculate mean of delivery_duration")
print("   3. Round to 2 decimals")

result_q2 = (
    fact_orders
    .groupby('city_type', as_index=False)
    .agg(avg_delivery_duration=('delivery_duration', 'mean'))
    .round(2)
)

print("\n✅ ANSWER:")
print(result_q2)

# ============================================================================
# QUESTION 3: Which restaurants have the most orders?
# ============================================================================
print("\n\n" + "=" * 70)
print("QUESTION 3: Top 5 Restaurants by Order Count")
print("=" * 70)

print("\n🎯 GOAL: Find which restaurants are most popular")
print("\n💡 APPROACH:")
print("   1. Merge fact_orders with dim_restaurants")
print("   2. Group by restaurant_name")
print("   3. Count orders")
print("   4. Sort and get top 5")

result_q3 = (
    fact_orders.merge(dim_restaurants, on='Restaurant_ID')
    .groupby('restaurant_name', as_index=False)
    .agg(order_count=('order_id', 'count'))
    .sort_values('order_count', ascending=False)
    .head(5)
)

print("\n✅ ANSWER:")
print(result_q3)

# ============================================================================
# QUESTION 4: Orders during festivals vs non-festivals
# ============================================================================
print("\n\n" + "=" * 70)
print("QUESTION 4: Average Delivery Duration - Festival vs Non-Festival")
print("=" * 70)

print("\n🎯 GOAL: Compare delivery times during festivals")
print("\n💡 APPROACH:")
print("   1. Group by is_festival")
print("   2. Calculate mean delivery_duration")
print("   3. Round to 2 decimals")

result_q4 = (
    fact_orders
    .groupby('is_festival', as_index=False)
    .agg(avg_delivery_duration=('delivery_duration', 'mean'))
    .round(2)
)

print("\n✅ ANSWER:")
print(result_q4)

# ============================================================================
# PRACTICE EXERCISES
# ============================================================================
print("\n\n" + "=" * 70)
print("YOUR TURN - PRACTICE EXERCISES")
print("=" * 70)

print("""
Try to solve these on your own:

1️⃣ EXERCISE 1: Average delivery duration per weather condition
   - Group by: weather_condition
   - Calculate: mean of delivery_duration
   - Round to 2 decimals

2️⃣ EXERCISE 2: Top 3 delivery persons by number of orders
   - Merge: fact_orders with dim_delivery_person
   - Group by: Delivery_person_ID and Delivery_person_Age
   - Count: orders
   - Sort and get top 3

3️⃣ EXERCISE 3: Orders per order_type in Metropolitan cities
   - Filter: city_type == 'Metropolitan'
   - Group by: order_type
   - Count: orders

HINT: Use the patterns you learned above!
""")

# ============================================================================
# KEY COMMANDS REFERENCE
# ============================================================================
print("\n" + "=" * 70)
print("KEY PANDAS COMMANDS REFERENCE")
print("=" * 70)
print("""
📂 LOADING DATA
   pd.read_csv('filename.csv')          # Load CSV file
   
🔍 EXPLORING DATA
   df.head()                            # First 5 rows
   df.tail()                            # Last 5 rows
   df.shape                             # (rows, columns)
   df.columns                           # Column names
   df.dtypes                            # Data types
   df.info()                            # Summary info
   df.describe()                        # Statistics
   df['column'].unique()                # Unique values
   df['column'].value_counts()          # Count per value

🔗 JOINING DATA
   df1.merge(df2, on='key')             # Inner join
   df1.merge(df2, on='key', how='left') # Left join
   df1.merge(df2, on='key', how='outer')# Outer join

📊 GROUPING & AGGREGATING
   df.groupby('col').agg({'col2': 'mean'})
   df.groupby('col', as_index=False).agg(new_name=('col2', 'mean'))
   
   Aggregation functions:
   - 'mean'   : Average
   - 'sum'    : Total
   - 'count'  : Count
   - 'min'    : Minimum
   - 'max'    : Maximum
   - 'median' : Median
   - 'std'    : Standard deviation

🔢 TRANSFORMING
   df.round(2)                          # Round to 2 decimals
   df.sort_values('col', ascending=False) # Sort descending
   df.rename(columns={'old': 'new'})    # Rename columns

🎯 FILTERING
   df[df['col'] > 100]                  # Filter rows
   df[df['col'] == 'value']             # Exact match
   df[df['col'].isin(['A', 'B'])]       # Multiple values
""")

print("\n" + "=" * 70)
print("All CSV files are loaded and ready to use!")
print("Try the practice exercises above to test your skills!")
print("=" * 70)
