"""
🐼 Pandas Series Creation - Practice Examples
Run this file to see all the examples in action!
"""

import pandas as pd

print("=" * 70)
print("🐼 PANDAS SERIES CREATION EXAMPLES")
print("=" * 70)

# ==========================================
# 1. FROM A LIST (DEFAULT INDEX)
# ==========================================
print("\n1️⃣ Creating Series from a List (Default Index)")
print("-" * 70)

data = [10, 20, 30, 40]
series = pd.Series(data)
print(series)
print(f"\nData type: {series.dtype}")

# ==========================================
# 2. FROM A LIST WITH CUSTOM INDEX
# ==========================================
print("\n\n2️⃣ Creating Series from a List (Custom Index)")
print("-" * 70)

data = [10, 20, 30, 40]
index = ['a', 'b', 'c', 'd']
series = pd.Series(data, index=index)
print(series)

# ==========================================
# 3. FROM A DICTIONARY
# ==========================================
print("\n\n3️⃣ Creating Series from a Dictionary")
print("-" * 70)

data = {'Alice': 25, 'Bob': 30, 'Charlie': 35}
series = pd.Series(data)
print(series)

# ==========================================
# 4. FROM A SCALAR VALUE
# ==========================================
print("\n\n4️⃣ Creating Series from a Scalar Value")
print("-" * 70)

value = 5
index = ['a', 'b', 'c']
series = pd.Series(value, index=index)
print(series)

# ==========================================
# 5. ACCESSING PROPERTIES
# ==========================================
print("\n\n5️⃣ Accessing Series Properties")
print("-" * 70)

data = [10, 20, 30]
index = ['a', 'b', 'c']
series = pd.Series(data, index=index)

print(f"Index: {series.index}")
print(f"Values: {series.values}")
print(f"Data Type: {series.dtype}")
print(f"Shape: {series.shape}")
print(f"Size: {series.size}")

# ==========================================
# PRACTICE EXERCISES
# ==========================================
print("\n\n" + "=" * 70)
print("🏋️ PRACTICE EXERCISE SOLUTIONS")
print("=" * 70)

# Exercise 1
print("\n📝 Exercise 1: Create from list [100, 200, 300, 400]")
print("-" * 70)
ex1_data = [100, 200, 300, 400]
ex1_series = pd.Series(ex1_data)
print(ex1_series)

# Exercise 2
print("\n\n📝 Exercise 2: Create from grades dictionary")
print("-" * 70)
grades = {'Math': 90, 'Science': 85, 'English': 88}
ex2_series = pd.Series(grades)
print(ex2_series)

# Exercise 3
print("\n\n📝 Exercise 3: Create from scalar 10 with index ['a','b','c','d']")
print("-" * 70)
ex3_value = 10
ex3_index = ['a', 'b', 'c', 'd']
ex3_series = pd.Series(ex3_value, index=ex3_index)
print(ex3_series)

# ==========================================
# BONUS: DIFFERENT DATA TYPES
# ==========================================
print("\n\n" + "=" * 70)
print("🎁 BONUS: Series with Different Data Types")
print("=" * 70)

# String Series
print("\n📝 String Series:")
string_series = pd.Series(['apple', 'banana', 'cherry'])
print(string_series)
print(f"Data type: {string_series.dtype}")

# Float Series
print("\n📝 Float Series:")
float_series = pd.Series([1.5, 2.7, 3.9, 4.2])
print(float_series)
print(f"Data type: {float_series.dtype}")

# Mixed Type Series (becomes 'object')
print("\n📝 Mixed Type Series:")
mixed_series = pd.Series([1, 'hello', 3.14, True])
print(mixed_series)
print(f"Data type: {mixed_series.dtype}")

print("\n" + "=" * 70)
print("✅ All examples completed!")
print("=" * 70)
