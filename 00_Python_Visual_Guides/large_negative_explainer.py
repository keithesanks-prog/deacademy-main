import pandas as pd
from datetime import datetime

print("--- WHY YOU GET -1,000,000+ ---")

# 1. Real Order Date (from your CSV)
# Your data is from 2022
real_order_date = pd.to_datetime("2022-03-13 11:55:00")
print(f"Correct Start Time: {real_order_date}")

# 2. The Typo Date
# Typo: pd.to_datetime("12:15:00 12:15:00")
# Because there is NO DATE in that string, Pandas guesses "Today's Date"
# (Since the computer's clock thinks it is 2025...)
typo_string = "12:15:00 12:15:00"
typo_date = pd.to_datetime(typo_string)
print(f"Typo End Time (Guesses Today): {typo_date}")

# 3. The Resulting Calculation
# 2022 minus 2025 = -3 YEARS
diff = real_order_date - typo_date
print(f"\nMath: {real_order_date} - {typo_date}")
print(f"Difference: {diff}")

minutes = diff.total_seconds() / 60
print(f"Difference in Minutes: {minutes:,.0f}")
print("(This matches the 'horrendously wrong' number you see!)")

print("\n--- THE SOLUTION ---")
print("Pandas needs the DATE from 2022 to know what day it is.")
print("Fix: pd.to_datetime(df['order_date'] + ' ' + df['order_picked_time'])")
