"""
============================================
MAX AND MIN VALUES - SETUP SCRIPT
============================================
Learn how to find the largest and smallest values in lists

Your Tasks:
1. Find maximum and minimum values using max() and min()
2. Work with different data types
3. Find max/min with custom criteria

Key Functions to Learn:
- max(list)        # Returns largest value
- min(list)        # Returns smallest value
- max(list, key=)  # Custom comparison
"""

# ============================================
# SAMPLE DATA
# ============================================

numbers = [4, 1, 7, 3, 8, 2]
prices = [19.99, 5.50, 12.75, 8.00, 25.00]
names = ["Alice", "Bob", "Charlie", "David"]

# ============================================
# EXERCISE 1: Basic Max and Min
# ============================================
print("=" * 50)
print("EXERCISE 1: Basic Max and Min")
print("=" * 50)

numbers = [4, 1, 7, 3, 8, 2]

# TODO: Find the largest number using max()
# TODO: Find the smallest number using min()
# TODO: Print both results


# ============================================
# EXERCISE 2: Max/Min with Different Data Types
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Different Data Types")
print("=" * 50)

# TODO: Find max and min of prices
prices = [19.99, 5.50, 12.75, 8.00, 25.00]

# TODO: Find max and min of strings (alphabetically)
names = ["Alice", "Bob", "Charlie", "David"]


# ============================================
# EXERCISE 3: Find Index of Max/Min
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Find Index of Max/Min")
print("=" * 50)

numbers = [4, 1, 7, 3, 8, 2]

# TODO: Find the index of the maximum value
# Hint: Use numbers.index(max(numbers))

# TODO: Find the index of the minimum value


# ============================================
# EXERCISE 4: Max/Min with Key Function
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Custom Comparison")
print("=" * 50)

words = ["Python", "is", "awesome", "to", "learn"]

# TODO: Find the longest word
# Hint: max(words, key=len)

# TODO: Find the shortest word


# ============================================
# EXERCISE 5: Practical Applications
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Practical Applications")
print("=" * 50)

students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78}
]

# TODO: Find the student with the highest score
# Hint: max(students, key=lambda x: x['score'])

# TODO: Find the student with the lowest score


# ============================================
# EXPECTED OUTPUT (for reference)
# ============================================
"""
==================================================
EXERCISE 1: Basic Max and Min
==================================================
Numbers: [4, 1, 7, 3, 8, 2]
Largest Number: 8
Smallest Number: 1

==================================================
EXERCISE 2: Different Data Types
==================================================
Prices: [19.99, 5.5, 12.75, 8.0, 25.0]
Max Price: 25.0
Min Price: 5.5

... (and so on)
"""
