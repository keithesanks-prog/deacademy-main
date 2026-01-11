import pandas as pd

# 1. Setup Sample Data
data = {
    'order_date': ['3/13/22'],
    'order_time': ['11:55:00'],
    'order_picked_time': ['12:05:00'],
    'delivery_duration': [42]
}
df = pd.DataFrame(data)

print("--- VALUES ---")
print("Picked: 12:05")
print("Order:  11:55")
print("Drive:  42 mins")
print("----------------")

# 2. YOUR FORMULA
# (Picked) - (Order + Duration)
df['user_result'] = (
    pd.to_datetime(df['order_date'] + ' ' + df['order_picked_time']) - 
    (pd.to_datetime(df['order_date'] + ' ' + df['order_time']) + pd.to_timedelta(df['delivery_duration'], unit='m'))
).dt.total_seconds() / 60

print(f"\nYOUR FORMULA RESULT: {df['user_result'][0]} minutes")
print("Why? Because Picked - (Order + Drive) = Picked - Order - Drive")
print("     (12:05 - 11:55) - 42")
print("     10 mins - 42 mins = -32 mins")

# 3. CORRECT FORMULA
# (Picked - Order) + Duration
df['correct_result'] = (
    (pd.to_datetime(df['order_date'] + ' ' + df['order_picked_time']) - pd.to_datetime(df['order_date'] + ' ' + df['order_time'])) + 
    pd.to_timedelta(df['delivery_duration'], unit='m')
).dt.total_seconds() / 60

print(f"\nCORRECT RESULT: {df['correct_result'][0]} minutes")
print("Why? Because (Picked - Order) + Drive")
print("     10 mins + 42 mins = 52 mins")
