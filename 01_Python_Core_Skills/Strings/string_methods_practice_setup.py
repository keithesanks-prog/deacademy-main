"""
============================================
STRING METHODS PRACTICE - SETUP SCRIPT
============================================
Practice common Python string methods including case manipulation,
searching, and transformation.

Your Tasks:
1. Practice case conversion methods (upper, lower, swapcase, title, capitalize)
2. Practice string searching (find, index, count)
3. Practice string checking (startswith, endswith, isalpha, isdigit)
4. Practice string transformation (strip, replace, split, join)
"""

# ============================================
# SAMPLE DATA
# ============================================

sample_text = "Hello World"
phone_data = "Apple - iPhone 13"
messy_text = "  Python Programming  "
mixed_case = "hELLO wORLD"

# ============================================
# EXERCISE 1: Case Conversion Methods
# ============================================
print("=" * 50)
print("EXERCISE 1: Case Conversion")
print("=" * 50)

s = "Hello World"

# TODO: Convert to uppercase using .upper()
# TODO: Convert to lowercase using .lower()
# TODO: Swap case using .swapcase()
# TODO: Convert to title case using .title()
# TODO: Capitalize first letter using .capitalize()

print(f"Original: {s}")
# Print each transformation


# ============================================
# EXERCISE 2: String Searching
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: String Searching")
print("=" * 50)

text = "Python is awesome. Python is powerful."

# TODO: Find the position of "Python" using .find()
# TODO: Count how many times "Python" appears using .count()
# TODO: Check if text starts with "Python" using .startswith()
# TODO: Check if text ends with "powerful." using .endswith()


# ============================================
# EXERCISE 3: String Cleaning
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: String Cleaning")
print("=" * 50)

messy = "  Python Programming  "

# TODO: Remove leading/trailing spaces using .strip()
# TODO: Remove only leading spaces using .lstrip()
# TODO: Remove only trailing spaces using .rstrip()


# ============================================
# EXERCISE 4: String Transformation
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: String Transformation")
print("=" * 50)

phone = "Apple - iPhone 13"

# TODO: Split the string by " - " using .split()
# TODO: Extract the brand (first part)
# TODO: Extract the model (second part)
# TODO: Replace "iPhone" with "iPad" using .replace()


# ============================================
# EXERCISE 5: Combining Methods (Like SQL!)
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Combining Methods")
print("=" * 50)

# Similar to SQL's TRIM and SPLIT_PART
data = "  Samsung - Galaxy S21  "

# TODO: Clean the data (strip spaces)
# TODO: Split by " - "
# TODO: Get brand and model
# TODO: Convert brand to uppercase
# TODO: Print formatted result


# ============================================
# EXPECTED OUTPUT (for reference)
# ============================================
"""
==================================================
EXERCISE 1: Case Conversion
==================================================
Original: Hello World
Upper: HELLO WORLD
Lower: hello world
Swapcase: hELLO wORLD
Title: Hello World
Capitalize: Hello world

==================================================
EXERCISE 2: String Searching
==================================================
Position of 'Python': 0
Count of 'Python': 2
Starts with 'Python': True
Ends with 'powerful.': True

... (and so on)
"""
