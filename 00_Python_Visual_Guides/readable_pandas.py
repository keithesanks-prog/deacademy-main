import pandas as pd

# Creating our sample "group" again
data = {'delivery_duration': [50, 30, 60, 40]} 
group_df = pd.DataFrame(data)

print("--- 1. THE 'INSANE' WAY (Complex Syntax) ---")
# The "Double Bracket" issue you hated:
# late_orders = group_df[ group_df['delivery_duration'] > 45 ]
print("Code: group_df[ group_df['delivery_duration'] > 45 ]")
print("Result: Uses boolean indexing (Masks)")


print("\n--- 2. THE 'INTUITIVE' WAY (.query) ---")
print("Pandas has a 'secret' function that lets you write string queries (like SQL).")
print("It reads exactly like English:")

# Look how clean this is!
# "Select from group_df where delivery_duration > 45"
late_orders = group_df.query('delivery_duration > 45')

print(f"Code: group_df.query('delivery_duration > 45')")
print(late_orders)

print("\n--- 3. USING IT IN THE FUNCTION ---")
def calculate_percent_late_clean(df):
    # READABLE: "Query the dataframe for duration > 45"
    late_orders = df.query('delivery_duration > 45')
    
    # Simple division
    return f"{len(late_orders) / len(df):.2%}"

print("Function Result:", calculate_percent_late_clean(group_df))
