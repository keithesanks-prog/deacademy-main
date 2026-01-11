import pandas as pd

# Creating our sample data again
data = {'delivery_duration': [50, 30, 60, 40]} # 2 late, 2 on time
x_data = pd.DataFrame(data)

print("--- THE INTUITIVE WAY (No Memorization Needed) ---")
print("Instead of writing a complex one-liner lambda, just write a normal Python function!")

# 1. Write a normal function that makes sense to you
def calculate_percent_late(group_df):
    # Step A: Filter
    late_orders = group_df[group_df['delivery_duration'] > 45]
    
    # Step B: Count
    number_late = len(late_orders)
    total_orders = len(group_df)
    
    # Step C: Math
    fraction = number_late / total_orders
    
    # Step D: Format
    return f"{fraction:.2%}"

print("\nRunning the normal function...")
# 2. Tell Pandas to use YOUR function
# Notice: No 'lambda' keyword needed!
result = calculate_percent_late(x_data)

print(f"Result: {result}")

print("\n------------------------------------------------")
print("KEY TAKEAWAY: You typically only use 'lambda' for tiny 1-line operations.")
print("If the logic is complex like this one, it is BETTER code to write a full function.")
print("You are NOT expected to memorize how to squash 5 lines of code into 1 line.")
