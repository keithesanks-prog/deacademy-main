"""
============================================
STRING CASE DETECTION - SETUP SCRIPT
============================================
Learn how to detect and count uppercase/lowercase characters in Python

Your Tasks:
1. Check if individual characters are uppercase or lowercase
2. Count uppercase and lowercase letters in a string
3. Analyze mixed-case strings

Key Methods to Learn:
- char.isupper()  # Returns True if character is uppercase
- char.islower()  # Returns True if character is lowercase
- Using generator expressions with sum()
"""

# ============================================
# SAMPLE DATA
# ============================================

sample_strings = [
    "HelloWorld",
    "PYTHON",
    "programming",
    "DataEngineering2024",
    "SQL_Training_123"
]

# ============================================
# EXERCISE 1: Check individual characters
# ============================================
print("=" * 50)
print("EXERCISE 1: Check Individual Characters")
print("=" * 50)

# TODO: Check if 'H' is uppercase
# TODO: Check if 'e' is lowercase
# TODO: Check if '1' is uppercase or lowercase (what happens?)


# ============================================
# EXERCISE 2: Count uppercase and lowercase
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Count Uppercase and Lowercase")
print("=" * 50)

s = "HelloWorld"

# TODO: Count uppercase letters in s
# Hint: Use sum(1 for char in s if char.isupper())

# TODO: Count lowercase letters in s
# Hint: Use sum(1 for char in s if char.islower())

# TODO: Print the results


# ============================================
# EXERCISE 3: Analyze all sample strings
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Analyze All Sample Strings")
print("=" * 50)

# TODO: Loop through sample_strings
# TODO: For each string, count and print:
#       - Total characters
#       - Uppercase count
#       - Lowercase count
#       - Other characters (numbers, symbols, spaces)


# ============================================
# EXERCISE 4: Find strings with specific patterns
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Pattern Detection")
print("=" * 50)

# TODO: Find strings that have MORE uppercase than lowercase
# TODO: Find strings that are ALL uppercase
# TODO: Find strings that are ALL lowercase


# ============================================
# EXPECTED OUTPUT (for reference)
# ============================================
"""
When complete, your output should look similar to:

==================================================
EXERCISE 1: Check Individual Characters
==================================================
Is 'H' uppercase? True
Is 'e' lowercase? True
Is '1' uppercase? False
Is '1' lowercase? False

==================================================
EXERCISE 2: Count Uppercase and Lowercase
==================================================
String: HelloWorld
Uppercase letters: 2
Lowercase letters: 8

==================================================
EXERCISE 3: Analyze All Sample Strings
==================================================
String: HelloWorld
  Total: 10 | Upper: 2 | Lower: 8 | Other: 0

String: PYTHON
  Total: 6 | Upper: 6 | Lower: 0 | Other: 0

... (and so on)
"""
