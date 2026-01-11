import pandas as pd

# 1. Setup the "Group" DataFrame
print("--- STEP 1: The Original Group ---")
data = {
    'order_id': ['A', 'B', 'C', 'D'],
    'delivery_duration': [50, 30, 60, 40]
}
group_df = pd.DataFrame(data)
print(group_df)
print("\n")

# 2. The "Question" (Creating the Mask)
# This is the inner part: group_df['delivery_duration'] > 45
print("--- STEP 2: The Question (True/False Mask) ---")
print("Code: mask = group_df['delivery_duration'] > 45")
mask = group_df['delivery_duration'] > 45
print(mask)
print("\nNotice roughly:\n0    True  (50 > 45)\n1    False (30 < 45)\n2    True  (60 > 45)\n3    False (40 < 45)")
print("\n")

# 3. The "Filter" (Applying the Mask)
# This is the outer part: group_df[mask]
print("--- STEP 3: Applying the Filter ---")
print("Pandas keeps ONLY the rows where the Mask says 'True'")
print("Code: late_orders = group_df[mask]")
late_orders = group_df[mask]
print(late_orders)
print("\n")

# 4. Counting
print("--- STEP 4: The Result ---")
print(f"Code: len(late_orders)")
print(f"Count: {len(late_orders)}")
print("(It counted 2 rows because 2 rows were True)")
