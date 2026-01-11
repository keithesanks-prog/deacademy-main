"""
============================================
DICTIONARY MERGING - SETUP SCRIPT
============================================
Learn how to merge dictionaries in Python

Your Tasks:
1. Merge dictionaries using {**dict1, **dict2}
2. Handle duplicate keys
3. Merge multiple dictionaries
4. Use other merging methods

Key Concepts to Learn:
- Dictionary unpacking with **
- .update() method
- | operator (Python 3.9+)
- Handling key conflicts
"""

# ============================================
# SAMPLE DATA
# ============================================

dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}

# ============================================
# EXERCISE 1: Basic Dictionary Merging
# ============================================
print("=" * 50)
print("EXERCISE 1: Basic Dictionary Merging")
print("=" * 50)

dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}

# TODO: Merge dict1 and dict2 using {**dict1, **dict2}
# TODO: Print the merged dictionary


# ============================================
# EXERCISE 2: Handling Duplicate Keys
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Handling Duplicate Keys")
print("=" * 50)

dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}  # 'b' exists in both!

# TODO: Merge the dictionaries
# TODO: Observe which value for 'b' is kept
# TODO: Try reversing the order: {**dict2, **dict1}


# ============================================
# EXERCISE 3: Merge Multiple Dictionaries
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Merge Multiple Dictionaries")
print("=" * 50)

dict1 = {"a": 1}
dict2 = {"b": 2}
dict3 = {"c": 3}

# TODO: Merge all three dictionaries
# Hint: {**dict1, **dict2, **dict3}


# ============================================
# EXERCISE 4: Other Merging Methods
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Other Merging Methods")
print("=" * 50)

dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}

# TODO: Method 1 - Using .update()
# TODO: Method 2 - Using | operator (Python 3.9+)


# ============================================
# EXERCISE 5: Practical Application
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Practical Application")
print("=" * 50)

user_defaults = {"theme": "light", "language": "en", "notifications": True}
user_preferences = {"theme": "dark", "font_size": 14}

# TODO: Merge with user preferences overriding defaults
# TODO: Print the final settings


# ============================================
# EXPECTED OUTPUT (for reference)
# ============================================
"""
==================================================
EXERCISE 1: Basic Dictionary Merging
==================================================
Dict 1: {'a': 1, 'b': 2}
Dict 2: {'c': 3, 'd': 4}
Merged Dictionary: {'a': 1, 'b': 2, 'c': 3, 'd': 4}

==================================================
EXERCISE 2: Handling Duplicate Keys
==================================================
Dict 1: {'a': 1, 'b': 2}
Dict 2: {'b': 3, 'c': 4}
Merged: {'a': 1, 'b': 3, 'c': 4}
(dict2's value for 'b' wins!)

... (and so on)
"""
