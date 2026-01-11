import pandas as pd

# Creating a sample row
print("--- PREPARING SAMPLE DATA ---")
data = {
    'order_date': ['2023-01-01'],
    'order_time': ['12:00:00'],
    'order_picked_time': ['12:15:00']
}
df = pd.DataFrame(data)
print(df)

print("\n--- 1. THE ERROR (Your Typo) ---")
# You wrote: pd.to_datetime(df['order_picked_time'] + ' ' + df['order_picked_time'])
# This creates: "12:15:00 12:15:00"

bad_string = df['order_picked_time'] + ' ' + df['order_picked_time']
print(f"What you asked Pandas to read: '{bad_string.iloc[0]}'")

try:
    bad_date = pd.to_datetime(bad_string)
    print(f"What Pandas thought it was: {bad_date.iloc[0]}")
    # If this works, it might be interpreting the first time as a date?
except Exception as e:
    print(f"Pandas Error: {e}")

print("\n--- 2. THE FIX ---")
# You want: order_date + ' ' + order_picked_time
correct_string = df['order_date'] + ' ' + df['order_picked_time']
print(f"What you WANTED: '{correct_string.iloc[0]}'")

correct_date = pd.to_datetime(correct_string)
print(f"Correct Date Object: {correct_date.iloc[0]}")

print("\n--- 3. THE CALCULATION ---")
# Calculating the difference
start_time = pd.to_datetime(df['order_date'] + ' ' + df['order_time'])
diff = correct_date - start_time
print(f"Time Difference: {diff.iloc[0]}")
print(f"Minutes: {diff.dt.total_seconds().iloc[0] / 60}")
