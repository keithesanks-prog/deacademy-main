import pandas as pd

# 1. Setup Sample Data (First row from your CSV)
data = {
    'order_date': ['3/13/22'],
    'order_time': ['11:55:00'],
    'order_picked_time': ['12:05:00'],
    'delivery_duration': [42]  # 42 Minutes
}
df = pd.DataFrame(data)

print(f"--- SAMPLE DATA ---")
print(f"Order:  {df['order_time'][0]}")
print(f"Picked: {df['order_picked_time'][0]}")
print(f"Drive:  {df['delivery_duration'][0]} mins")
print("-" * 30)

# 2. YOUR FORMULA
# Construct datetimes
order_dt = pd.to_datetime(df['order_date'] + ' ' + df['order_time'])
picked_dt = pd.to_datetime(df['order_date'] + ' ' + df['order_picked_time'])

# The ERROR: Defaults to nanoseconds!
wrong_duration = pd.to_timedelta(df['delivery_duration']) 
# The ERROR: Logic is backwards!
# Picked - (Order + Duration)  == Picked - Order - Duration
wrong_total = (picked_dt - (order_dt + wrong_duration))

# Convert to minutes to see what happened
wrong_mins = wrong_total.dt.total_seconds() / 60

print(f"\n❌ YOUR FORMULA:")
print(f"Interpretation: Prep Time - 42 nanoseconds")
print(f"Result: {wrong_mins[0]} minutes")
print(f"Why > 15 found data: Because Prep Time ({wrong_mins[0]:.0f} min) >= 15")
print(f"Why > 45 found ZERO: Because Prep Time is never 45 mins!")

# 3. THE FIX
# Fix 1: Add unit='m'
correct_duration = pd.to_timedelta(df['delivery_duration'], unit='m')

# Fix 2: (Picked - Order) + Drive Time
correct_total = (picked_dt - order_dt) + correct_duration
correct_mins = correct_total.dt.total_seconds() / 60

print(f"\n✅ CORRECT FORMULA:")
print(f"Math: (12:05 - 11:55) + 42 mins")
print(f"      10 mins + 42 mins")
print(f"Result: {correct_mins[0]} minutes")
print(f"Is this > 45? {correct_mins[0] > 45}")
