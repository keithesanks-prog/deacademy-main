"""
Pandas Apply vs Vectorization - Practice Exercises
===================================================

This script contains hands-on exercises to practice the concepts from
the visual guide. Work through each exercise to build your understanding.

INSTRUCTIONS:
1. Read each exercise description
2. Try to solve it yourself first
3. Check your answer against the solution
4. Run the code to verify it works
"""

import pandas as pd
import numpy as np
import time

print("=" * 70)
print("PANDAS APPLY VS VECTORIZATION - PRACTICE EXERCISES")
print("=" * 70)

# ============================================================================
# EXERCISE 1: Refactor Apply to Vectorized
# ============================================================================
print("\n" + "=" * 70)
print("EXERCISE 1: Refactor Apply to Vectorized")
print("=" * 70)
print("""
GOAL: You have been given slow code that uses apply(). Your job is to
      refactor it to use vectorized operations for better performance.

SCENARIO: An e-commerce company has a DataFrame with product prices.
          They want to calculate the final price after applying a 20% discount.
""")

# Setup data
df_ex1 = pd.DataFrame({
    'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
    'price': [1000, 25, 75, 300, 150]
})

print("\nOriginal DataFrame:")
print(df_ex1)

# ❌ SLOW CODE (Using apply)
print("\n--- SLOW APPROACH (Using apply) ---")
start = time.time()
df_ex1['discounted_apply'] = df_ex1.apply(lambda row: row['price'] * 0.8, axis=1)
time_apply = time.time() - start
print(f"Time taken: {time_apply:.6f} seconds")
print(df_ex1[['product', 'price', 'discounted_apply']])

# YOUR TASK: Refactor the above code to use vectorization
print("\n--- YOUR TURN: Write vectorized version below ---")
print("# df_ex1['discounted_vector'] = ???")

# SOLUTION (Uncomment to see)
# ============================================================================
# start = time.time()
# df_ex1['discounted_vector'] = df_ex1['price'] * 0.8
# time_vector = time.time() - start
# print(f"\n✅ SOLUTION:")
# print(f"df_ex1['discounted_vector'] = df_ex1['price'] * 0.8")
# print(f"Time taken: {time_vector:.6f} seconds")
# print(f"Speedup: {time_apply/time_vector:.1f}x faster!")
# print(df_ex1[['product', 'price', 'discounted_vector']])
# ============================================================================


# ============================================================================
# EXERCISE 2: The NaN Trap - Fix the Bug
# ============================================================================
print("\n\n" + "=" * 70)
print("EXERCISE 2: The NaN Trap - Fix the Bug")
print("=" * 70)
print("""
GOAL: Fix code that is creating garbage "nan" strings in the output.

SCENARIO: A customer database has some missing first or last names.
          The current code is producing "John nan" and "nan Smith" instead
          of properly handling missing values.
""")

# Setup data with missing values
df_ex2 = pd.DataFrame({
    'first_name': ['John', 'Jane', np.nan, 'Bob', 'Alice'],
    'last_name': ['Smith', np.nan, 'Doe', 'Johnson', np.nan]
})

print("\nOriginal DataFrame:")
print(df_ex2)

# ❌ BUGGY CODE (Creates "nan" strings)
print("\n--- BUGGY CODE (Using apply) ---")
df_ex2['full_name_buggy'] = df_ex2.apply(
    lambda row: f"{row['first_name']} {row['last_name']}", 
    axis=1
)
print(df_ex2[['first_name', 'last_name', 'full_name_buggy']])
print("\n🚨 PROBLEM: Notice 'Jane nan' and 'nan Doe' - this is garbage data!")

# YOUR TASK: Fix this using vectorization
print("\n--- YOUR TURN: Fix this bug using vectorization ---")
print("# df_ex2['full_name_fixed'] = ???")

# SOLUTION (Uncomment to see)
# ============================================================================
# df_ex2['full_name_fixed'] = df_ex2['first_name'] + ' ' + df_ex2['last_name']
# print(f"\n✅ SOLUTION:")
# print(f"df_ex2['full_name_fixed'] = df_ex2['first_name'] + ' ' + df_ex2['last_name']")
# print(df_ex2[['first_name', 'last_name', 'full_name_fixed']])
# print("\n✅ FIXED: NaN values are now properly preserved as NaN, not 'nan' strings!")
# ============================================================================


# ============================================================================
# EXERCISE 3: When Apply IS the Right Choice
# ============================================================================
print("\n\n" + "=" * 70)
print("EXERCISE 3: When Apply IS the Right Choice")
print("=" * 70)
print("""
GOAL: Implement complex business logic that CANNOT be vectorized.

SCENARIO: A retail company wants to categorize customers based on
          multiple complex rules:
          
          - VIP: total_spend > 1000 AND loyalty_years >= 5
          - At Risk: total_spend < 100 AND days_since_purchase > 180
          - New: loyalty_years < 1
          - Standard: Everyone else
""")

# Setup data
df_ex3 = pd.DataFrame({
    'customer_id': [101, 102, 103, 104, 105, 106],
    'total_spend': [1500, 50, 200, 2000, 80, 500],
    'loyalty_years': [6, 3, 0.5, 8, 2, 4],
    'days_since_purchase': [10, 200, 5, 15, 190, 30]
})

print("\nCustomer DataFrame:")
print(df_ex3)

# YOUR TASK: Write a function and use apply to categorize customers
print("\n--- YOUR TURN: Write the categorization function ---")
print("""
def categorize_customer(row):
    # YOUR CODE HERE
    pass

df_ex3['category'] = df_ex3.apply(categorize_customer, axis=1)
""")

# SOLUTION (Uncomment to see)
# ============================================================================
# def categorize_customer(row):
#     if row['total_spend'] > 1000 and row['loyalty_years'] >= 5:
#         return 'VIP'
#     elif row['total_spend'] < 100 and row['days_since_purchase'] > 180:
#         return 'At Risk'
#     elif row['loyalty_years'] < 1:
#         return 'New'
#     else:
#         return 'Standard'
# 
# df_ex3['category'] = df_ex3.apply(categorize_customer, axis=1)
# print("\n✅ SOLUTION:")
# print(df_ex3)
# print("\n✅ This is a valid use of apply() because the logic is too complex")
# print("   to express cleanly with vectorized operations!")
# ============================================================================


# ============================================================================
# BONUS EXERCISE: String Accessor (.str)
# ============================================================================
print("\n\n" + "=" * 70)
print("BONUS EXERCISE: Use .str Accessor Instead of Apply")
print("=" * 70)
print("""
GOAL: Learn to use the .str accessor for string operations instead of apply.

SCENARIO: You have email addresses and want to extract the domain.
""")

# Setup data
df_bonus = pd.DataFrame({
    'email': ['john@gmail.com', 'jane@yahoo.com', 'bob@company.co.uk', 'alice@outlook.com']
})

print("\nEmail DataFrame:")
print(df_bonus)

# ❌ SLOW WAY (Using apply)
print("\n--- SLOW WAY (Using apply) ---")
df_bonus['domain_apply'] = df_bonus['email'].apply(lambda x: x.split('@')[1])
print(df_bonus[['email', 'domain_apply']])

# YOUR TASK: Use .str accessor instead
print("\n--- YOUR TURN: Use .str accessor ---")
print("# df_bonus['domain_str'] = df_bonus['email'].str.???")

# SOLUTION (Uncomment to see)
# ============================================================================
# df_bonus['domain_str'] = df_bonus['email'].str.split('@').str[1]
# # Alternative: df_bonus['domain_str'] = df_bonus['email'].str.split('@').str.get(1)
# print(f"\n✅ SOLUTION:")
# print(f"df_bonus['domain_str'] = df_bonus['email'].str.split('@').str[1]")
# print(df_bonus[['email', 'domain_str']])
# print("\n✅ The .str accessor is vectorized and much faster than apply!")
# ============================================================================


# ============================================================================
# SUMMARY
# ============================================================================
print("\n\n" + "=" * 70)
print("SUMMARY - KEY TAKEAWAYS")
print("=" * 70)
print("""
1. ⚡ ALWAYS TRY VECTORIZATION FIRST
   - Use basic operators: +, -, *, /, etc.
   - 100-300x faster than apply()
   
2. 🚨 BEWARE THE NaN TRAP
   - apply() converts NaN to string "nan"
   - Vectorization preserves NaN correctly
   
3. 🔧 USE BUILT-IN ACCESSORS
   - .str for string operations
   - .dt for datetime operations
   
4. ✅ APPLY IS OK FOR:
   - Complex multi-column conditional logic
   - External library/API calls
   - Processing lists/dicts in columns
   
5. ❌ NEVER USE APPLY FOR:
   - Simple math operations
   - String concatenation
   - Basic transformations
""")

print("\n" + "=" * 70)
print("To see solutions, uncomment the solution blocks in the code!")
print("=" * 70)
