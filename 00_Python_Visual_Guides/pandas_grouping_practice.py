import pandas as pd

# ==========================================
# PRACTICE EXERCISE: Grouping and Aggregation
# ==========================================

# 1. Create the DataFrame
data = {
    'Item': ['Apple', 'Banana', 'Orange', 'Milk', 'Cheese', 'Bread', 'Butter', 'Eggs', 'Apple', 'Banana'],
    'Category': ['Fruit', 'Fruit', 'Fruit', 'Dairy', 'Dairy', 'Bakery', 'Dairy', 'Dairy', 'Fruit', 'Fruit'],
    'Price': [1.2, 0.5, 0.8, 1.5, 2.0, 1.0, 1.8, 0.3, 1.1, 0.6],
    'Quantity': [10, 20, 15, 5, 2, 30, 3, 12, 8, 18]
}

df = pd.DataFrame(data)
print("--- ORIGINAL DATAFRAME ---")
print(df)
print("\n")

# 2. Total Price and Quantity using sum()
print("--- 1. TOTAL PRICE & QUANTITY (sum) ---")
total_sum = df.groupby('Category')[['Price', 'Quantity']].sum()
print(total_sum)
print("\n")

# 3. Average Price and Quantity using mean()
print("--- 2. AVERAGE PRICE & QUANTITY (mean) ---")
avg_mean = df.groupby('Category')[['Price', 'Quantity']].mean()
print(avg_mean)
print("\n")

# 4. Count of items in each category
print("--- 3. COUNT OF ITEMS ---")
counts = df.groupby('Category')['Item'].count()
print(counts)
print("\n")

# 5. Maximum and Minimum Price for each category
print("--- 4. MAX AND MIN PRICE ---")
max_min = df.groupby('Category')['Price'].agg(['max', 'min'])
print(max_min)
print("\n")

# 6. Total and Average using agg()
print("--- 5. TOTAL & AVERAGE (agg) ---")
summary = df.groupby('Category').agg({
    'Price': ['sum', 'mean'],
    'Quantity': ['sum', 'mean']
})
print(summary)
