"""
============================================
LIST REVERSAL - SETUP SCRIPT
============================================
Learn different methods to reverse lists in Python

Your Tasks:
1. Reverse a list using different methods
2. Understand the difference between in-place and copy reversal
3. Practice with different data types

Key Methods to Learn:
- list.reverse()     # In-place reversal (modifies original)
- reversed(list)     # Returns iterator
- list[::-1]         # Slicing (creates new list)
"""

# ============================================
# SAMPLE DATA
# ============================================

numbers = [1, 2, 3, 4, 5]
names = ["Alice", "Bob", "Charlie", "David"]
mixed = [1, "two", 3.0, True, None]

# ============================================
# EXERCISE 1: Basic List Reversal
# ============================================
print("=" * 50)
print("EXERCISE 1: Basic List Reversal")
print("=" * 50)

my_list = [1, 2, 3, 4, 5]

# TODO: Print the original list
# TODO: Reverse and print using slicing [::-1]
# Expected output: [5, 4, 3, 2, 1]


# ============================================
# EXERCISE 2: In-Place vs Copy Reversal
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: In-Place vs Copy Reversal")
print("=" * 50)

# METHOD 1: Using .reverse() (modifies original!)
list1 = [1, 2, 3, 4, 5]
# TODO: Print list1 before reversal
# TODO: Use list1.reverse()
# TODO: Print list1 after reversal (it's changed!)

# METHOD 2: Using [::-1] (creates new list)
list2 = [1, 2, 3, 4, 5]
# TODO: Print list2 before
# TODO: Create reversed_list2 = list2[::-1]
# TODO: Print both list2 and reversed_list2
# Notice: list2 is unchanged!


# ============================================
# EXERCISE 3: Using reversed() Function
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Using reversed() Function")
print("=" * 50)

my_list = [1, 2, 3, 4, 5]

# TODO: Use reversed(my_list) and convert to list
# Hint: list(reversed(my_list))


# ============================================
# EXERCISE 4: Reverse Different Data Types
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Reverse Different Data Types")
print("=" * 50)

# TODO: Reverse a list of strings
names = ["Alice", "Bob", "Charlie"]

# TODO: Reverse a list of mixed types
mixed = [1, "two", 3.0, True]

# TODO: Reverse a string (convert to list first!)
text = "Python"
# Hint: list(text)[::-1] or ''.join(reversed(text))


# ============================================
# EXERCISE 5: Practical Applications
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Practical Applications")
print("=" * 50)

# TODO: Check if a list is a palindrome
# A palindrome reads the same forwards and backwards
test_list = [1, 2, 3, 2, 1]
# Hint: Compare test_list == test_list[::-1]

# TODO: Get the last 3 elements in reverse order
numbers = [10, 20, 30, 40, 50, 60, 70]
# Hint: numbers[-3:][::-1]


# ============================================
# EXPECTED OUTPUT (for reference)
# ============================================
"""
==================================================
EXERCISE 1: Basic List Reversal
==================================================
Original: [1, 2, 3, 4, 5]
Reversed: [5, 4, 3, 2, 1]

==================================================
EXERCISE 2: In-Place vs Copy Reversal
==================================================
METHOD 1 - .reverse() (in-place):
Before: [1, 2, 3, 4, 5]
After: [5, 4, 3, 2, 1]

METHOD 2 - [::-1] (creates copy):
Original: [1, 2, 3, 4, 5]
Reversed copy: [5, 4, 3, 2, 1]
Original unchanged: [1, 2, 3, 4, 5]

... (and so on)
"""
