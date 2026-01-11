import pandas as pd

print("--- WHY ARE THE NUMBERS NEGATIVE? ---")

# Setup: Start and End Times
start_time = pd.to_datetime("2022-03-13 12:00:00")
end_time   = pd.to_datetime("2022-03-13 12:15:00")

print(f"Order Placed (Start): {start_time.time()}")
print(f"Order Picked (End)  : {end_time.time()}")
print("(Duration should be 15 minutes)")

print("\n--- SCENARIO 1: YOUR CODE (Start - End) ---")
# You wrote: Order - Picked
diff_1 = start_time - end_time
minutes_1 = diff_1.total_seconds() / 60
print(f"Math: 12:00 - 12:15")
print(f"Difference: {diff_1}")
print(f"Minutes: {minutes_1}")
print("❌ NEGATIVE! (Because you subtracted the big number from the small number)")

print("\n--- SCENARIO 2: CORRECT CODE (End - Start) ---")
# Correct: Picked - Order
diff_2 = end_time - start_time
minutes_2 = diff_2.total_seconds() / 60
print(f"Math: 12:15 - 12:00")
print(f"Difference: {diff_2}")
print(f"Minutes: {minutes_2}")
print("✅ POSITIVE! (This is what you want)")

print("\n--- SUMMARY ---")
print("FLIP YOUR SUBTRACTION!")
print("Instead of: (Order - Picked)")
print("Write:      (Picked - Order)")
