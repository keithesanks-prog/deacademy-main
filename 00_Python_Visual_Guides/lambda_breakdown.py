import pandas as pd

# 1. Create a "Fake Group" (representing one implementation of 'x')
# This visualizes what happens inside just ONE group (e.g., "High" traffic)
data_inside_one_group = {
    'order_id': ['Order A', 'Order B', 'Order C', 'Order D'],
    'total_delivery_time': [50, 30, 60, 40]  # Two are late (>45), two are on time
}
x = pd.DataFrame(data_inside_one_group)

print("--- STEP 1: WHAT IS 'x'? ---")
print("x is just a small DataFrame containing only the rows for this group:")
print(x)
print("\n")

# 2. The Logic: (x["total_delivery_time"] > 45)
print("--- STEP 2: FIND LATE ORDERS ---")
is_late = x["total_delivery_time"] > 45
print("Code: x['total_delivery_time'] > 45")
print(is_late)
print("\n")

# 3. The Logic: .sum()
print("--- STEP 3: COUNT LATE ORDERS ---")
late_count = is_late.sum()
print("Code: (x['total_delivery_time'] > 45).sum()")
print(f"Result: {late_count} (True=1, False=0, so 1+0+1+0 = 2)")
print("\n")

# 4. The Logic: / len(x)
print("--- STEP 4: CALCULATE FRACTION ---")
total_rows = len(x)
fraction = late_count / total_rows
print(f"Code: ... / len(x)")
print(f"Calculation: {late_count} / {total_rows}")
print(f"Result: {fraction}")
print("\n")

# 5. The Logic: f'{...:.2%}'
print("--- STEP 5: FORMAT AS PERCENTAGE ---")
formatted_result = f'{fraction:.2%}'
print(f"Code: f'{{...:.2%}}'")
print(f"Result: '{formatted_result}'")
print("\n")

print("--- SUMMARY ---")
print(f"The lambda function turns the DataFrame x into the string '{formatted_result}'")
