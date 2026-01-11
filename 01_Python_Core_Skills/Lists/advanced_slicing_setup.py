"""
============================================
ADVANCED SLICING TECHNIQUES - SETUP SCRIPT
============================================
Learn all the different ways to slice lists and strings in Python

Your Tasks:
1. Master basic slicing syntax [start:stop:step]
2. Use negative indices
3. Practice advanced slicing patterns
4. Apply slicing to both lists and strings

Key Concepts to Learn:
- [start:stop:step] syntax
- Negative indices
- Omitting start, stop, or step
- Common slicing patterns
"""

# ============================================
# SAMPLE DATA
# ============================================

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
text = "Python Programming"

# ============================================
# EXERCISE 1: Basic Slicing [start:stop]
# ============================================
print("=" * 50)
print("EXERCISE 1: Basic Slicing")
print("=" * 50)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# TODO: Get elements from index 2 to 5 (exclusive)
# Hint: numbers[2:5]

# TODO: Get first 3 elements
# Hint: numbers[:3]

# TODO: Get elements from index 5 to end
# Hint: numbers[5:]

# TODO: Get all elements (copy the list)
# Hint: numbers[:]


# ============================================
# EXERCISE 2: Negative Indices
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Negative Indices")
print("=" * 50)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# TODO: Get last 3 elements
# Hint: numbers[-3:]

# TODO: Get all except last 2 elements
# Hint: numbers[:-2]

# TODO: Get elements from index -5 to -2
# Hint: numbers[-5:-2]


# ============================================
# EXERCISE 3: Step Parameter [start:stop:step]
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Using Step")
print("=" * 50)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# TODO: Get every 2nd element
# Hint: numbers[::2]

# TODO: Get every 3rd element
# Hint: numbers[::3]

# TODO: Reverse the list
# Hint: numbers[::-1]

# TODO: Get every 2nd element in reverse
# Hint: numbers[::-2]


# ============================================
# EXERCISE 4: String Slicing
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: String Slicing")
print("=" * 50)

text = "Python Programming"

# TODO: Get first word
# TODO: Get second word
# TODO: Get every other character
# TODO: Reverse the string


# ============================================
# EXERCISE 5: Advanced Patterns
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Advanced Patterns")
print("=" * 50)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# TODO: Get middle elements (skip first 2 and last 2)
# TODO: Get first half
# TODO: Get second half
# TODO: Get elements at even indices
# TODO: Get elements at odd indices


# ============================================
# EXPECTED OUTPUT (for reference)
# ============================================
"""
==================================================
EXERCISE 1: Basic Slicing
==================================================
numbers[2:5]: [2, 3, 4]
numbers[:3]: [0, 1, 2]
numbers[5:]: [5, 6, 7, 8, 9]
numbers[:]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

... (and so on)
"""
