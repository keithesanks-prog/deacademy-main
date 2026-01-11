import pandas as pd

# ---------------------------------------------------------
# SETUP: Create a tiny dataset (One "Group")
# ---------------------------------------------------------
print("--- THE DATA (One Group of Orders) ---")
data = {'delivery_duration': [50, 30, 60]} 
# 50 is Late (>45), 30 is OK, 60 is Late (>45)
# So 2 out of 3 are late.
x = pd.DataFrame(data)
print(x)
print("\n")


# ---------------------------------------------------------
# METHOD 1: The "For Loop" Way (How a human thinks)
# ---------------------------------------------------------
print("--- METHOD 1: The 'For Loop' Way ---")

late_count = 0
total_items = 0

for time in x['delivery_duration']:
    total_items += 1
    if time > 45:
        late_count += 1

math_result = late_count / total_items
print(f"Loop Result: {math_result:.2%}")


# ---------------------------------------------------------
# METHOD 2: The "Standard Function" Way (Clean Code)
# ---------------------------------------------------------
print("\n--- METHOD 2: The 'Standard Function' Way ---")

def calculate_late_percentage(group_df):
    # 1. Logic
    late_orders = group_df['delivery_duration'] > 45
    # 2. Count
    count_late = late_orders.sum()
    # 3. Math
    fraction = count_late / len(group_df)
    # 4. Format
    return f"{fraction:.2%}"

# Run the function on 'x'
function_result = calculate_late_percentage(x)
print(f"Function Result: {function_result}")


# ---------------------------------------------------------
# METHOD 3: The "Lambda" Way (The One-Liner)
# ---------------------------------------------------------
print("\n--- METHOD 3: The 'Lambda' Way ---")

# This is the exact same logic as Method 2, just squashed onto one line.
lambda_func = lambda x: f'{(x["delivery_duration"] > 45).sum() / len(x):.2%}'

# Run the lambda on 'x'
lambda_result = lambda_func(x)
print(f"Lambda Result: {lambda_result}")
