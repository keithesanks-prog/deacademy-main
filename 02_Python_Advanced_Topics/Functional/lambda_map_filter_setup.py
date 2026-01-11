"""
============================================
LAMBDA, MAP, AND FILTER - SETUP SCRIPT
============================================
Learn functional programming concepts in Python

Your Tasks:
1. Create lambda functions
2. Use map() to transform data
3. Use filter() to select data
4. Combine lambda with map and filter

Key Concepts to Learn:
- lambda arguments: expression
- map(function, iterable)
- filter(function, iterable)
"""

# ============================================
# SAMPLE DATA
# ============================================

numbers = [1, 2, 3, 4, 5]
names = ["alice", "bob", "charlie"]
prices = [10.50, 25.00, 5.75, 15.25]

# ============================================
# EXERCISE 1: Lambda Functions
# ============================================
print("=" * 50)
print("EXERCISE 1: Lambda Functions")
print("=" * 50)

# TODO: Create a lambda that doubles a number
# Hint: double = lambda x: x * 2

# TODO: Create a lambda that adds two numbers
# Hint: add = lambda x, y: x + y

# TODO: Test your lambdas


# ============================================
# EXERCISE 2: map() Function
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Using map()")
print("=" * 50)

numbers = [1, 2, 3, 4, 5]

# TODO: Use map() to square all numbers
# Hint: list(map(lambda x: x**2, numbers))

# TODO: Use map() to convert to strings
# Hint: list(map(str, numbers))


# ============================================
# EXERCISE 3: filter() Function
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Using filter()")
print("=" * 50)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# TODO: Filter even numbers
# Hint: list(filter(lambda x: x % 2 == 0, numbers))

# TODO: Filter numbers greater than 5
# Hint: list(filter(lambda x: x > 5, numbers))


# ============================================
# EXERCISE 4: Combining map() and filter()
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Combining map() and filter()")
print("=" * 50)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# TODO: Get squares of even numbers
# Hint: Filter evens first, then map to squares


# ============================================
# EXERCISE 5: Practical Applications
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Practical Applications")
print("=" * 50)

names = ["alice", "bob", "charlie", "david"]

# TODO: Capitalize all names using map()
# TODO: Filter names with more than 4 letters
# TODO: Get lengths of all names


# ============================================
# EXPECTED OUTPUT (for reference)
# ============================================
"""
==================================================
EXERCISE 1: Lambda Functions
==================================================
double(5): 10
add(3, 4): 7

... (and so on)
"""
