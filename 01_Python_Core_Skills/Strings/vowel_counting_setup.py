"""
============================================
VOWEL COUNTING - SETUP SCRIPT
============================================
Learn how to count vowels in strings using different methods

Your Tasks:
1. Count vowels using a for loop
2. Count vowels using generator expressions
3. Handle case-insensitive counting

Key Concepts to Learn:
- Looping through strings
- Checking membership with 'in'
- Generator expressions with sum()
- String methods (.lower())
"""

# ============================================
# SAMPLE DATA
# ============================================

text1 = "Python"
text2 = "Hello World"
text3 = "AEIOU"
text4 = "Programming is fun"

# ============================================
# EXERCISE 1: Count Vowels with For Loop
# ============================================
print("=" * 50)
print("EXERCISE 1: Count Vowels with For Loop")
print("=" * 50)

text = "Python"

# TODO: Initialize count = 0
# TODO: Loop through each character in text
# TODO: Check if character is in 'aeiou'
# TODO: If yes, increment count
# TODO: Print the result


# ============================================
# EXERCISE 2: Count Vowels with Generator Expression
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Generator Expression Method")
print("=" * 50)

string = "Python".lower()
vowels = "aeiou"

# TODO: Use sum(1 for char in string if char in vowels)
# TODO: Print the result


# ============================================
# EXERCISE 3: Case-Insensitive Counting
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Case-Insensitive Counting")
print("=" * 50)

text = "HELLO WORLD"

# TODO: Convert to lowercase first
# TODO: Count vowels
# TODO: Compare with counting without lowercase conversion


# ============================================
# EXERCISE 4: Count Each Vowel Separately
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Count Each Vowel")
print("=" * 50)

text = "Programming is fun"

# TODO: Count how many times each vowel (a, e, i, o, u) appears
# Hint: Use text.lower().count('a'), etc.


# ============================================
# EXERCISE 5: Practical Applications
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Analyze Multiple Strings")
print("=" * 50)

sentences = [
    "Python is awesome",
    "Data Engineering",
    "SQL and Python"
]

# TODO: For each sentence, count and print vowels
# TODO: Find which sentence has the most vowels


# ============================================
# EXPECTED OUTPUT (for reference)
# ============================================
"""
==================================================
EXERCISE 1: Count Vowels with For Loop
==================================================
Text: Python
Number of Vowels: 1

==================================================
EXERCISE 2: Generator Expression Method
==================================================
Text: python
Number of vowels: 1

... (and so on)
"""
