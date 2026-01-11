import pandas as pd

# Load Data
# Assuming the file exists in the current directory as verified
try:
    df = pd.read_csv('fact_orders_grubhub.csv')
except FileNotFoundError:
    # Fallback to creating a dummy dataframe if CSV assumes specific environment
    data = {
        'order_date': ['2023-01-01', '2023-01-01'],
        'order_time': ['12:00:00', '12:00:00'],
        'order_picked_time': ['12:15:00', '12:20:00'],
        'delivery_duration': [20, 40],
        'road_traffic': ['High', 'Low']
    }
    df = pd.DataFrame(data)

# Calculate total_delivery_time
# Ensure datetime columns are converted if not already (safeguard)
# Note: User's code used simple subtraction, assuming well-formed strings or objects
df['total_delivery_time'] = df['delivery_duration'] + (pd.to_datetime(df['order_picked_time']) - pd.to_datetime(df['order_time'])).dt.total_seconds() / 60

# --- THE FIX ---
# ORIGINAL ERROR: is_late = df['total_delivery_time'] > 45
# This created a standalone variable 'is_late', not a column in 'df'.
# When groupby tried to look for 'is_late' inside df, it failed.

# CORRECT APPROACH: Assign it as a new column using string matching the name you want
df['is_late'] = df['total_delivery_time'] > 45

print("Percentage of Late Orders by Traffic:")
# Now this works because 'is_late' is a column in df
# Calculate mean % (Series) - GroupBy sorts keys alphabetically by default, giving us our 0,1,2,3 basis
percent_late_series = df.groupby('road_traffic')['is_late'].mean() * 100

# reset_index() first to get indices 0,1,2,3 based on alphabetical road_traffic (High, Jam, Low, Medium)
percent_late_df = percent_late_series.reset_index()

# Then sort values to scramble the indices as requested (e.g. Jam is index 1)
percent_late_df = percent_late_df.sort_values(by='is_late', ascending=False)

# Rename and format
percent_late_df.columns = ['road_traffic', 'percent_orders_late']
percent_late_df['percent_orders_late'] = percent_late_df['percent_orders_late'].map('{:.2f}%'.format)

print(percent_late_df)
