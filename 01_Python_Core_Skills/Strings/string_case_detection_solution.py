"""
============================================
STRING CASE DETECTION - SOLUTION
============================================
Run string_case_detection_setup.py FIRST to try it yourself!

This solution demonstrates multiple methods for detecting and counting
uppercase and lowercase characters in Python strings.
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

# METHOD 1: Using .isupper() and .islower()
char1 = 'H'
char2 = 'e'
char3 = '1'

print(f"Is '{char1}' uppercase? {char1.isupper()}")  # True
print(f"Is '{char2}' lowercase? {char2.islower()}")  # True
print(f"Is '{char3}' uppercase? {char3.isupper()}")  # False (numbers aren't upper/lower)
print(f"Is '{char3}' lowercase? {char3.islower()}")  # False


# ============================================
# EXERCISE 2: Count uppercase and lowercase
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Count Uppercase and Lowercase")
print("=" * 50)

s = "HelloWorld"

# METHOD 1: Using generator expression with sum() (MOST PYTHONIC!)
uppercase_count = sum(1 for char in s if char.isupper())
lowercase_count = sum(1 for char in s if char.islower())

print(f"String: {s}")
print(f"Uppercase letters: {uppercase_count}")
print(f"Lowercase letters: {lowercase_count}")

print("\n--- Alternative Methods ---")

# METHOD 2: Using a traditional for loop (more explicit)
upper_count = 0
lower_count = 0
for char in s:
    if char.isupper():
        upper_count += 1
    elif char.islower():
        lower_count += 1

print(f"Method 2 - Upper: {upper_count}, Lower: {lower_count}")

# METHOD 3: Using list comprehension and len()
upper_chars = [char for char in s if char.isupper()]
lower_chars = [char for char in s if char.islower()]
print(f"Method 3 - Upper: {len(upper_chars)}, Lower: {len(lower_chars)}")


# ============================================
# EXERCISE 3: Analyze all sample strings
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Analyze All Sample Strings")
print("=" * 50)

for string in sample_strings:
    total = len(string)
    upper = sum(1 for char in string if char.isupper())
    lower = sum(1 for char in string if char.islower())
    other = total - upper - lower  # Numbers, symbols, spaces, etc.
    
    print(f"\nString: {string}")
    print(f"  Total: {total} | Upper: {upper} | Lower: {lower} | Other: {other}")


# ============================================
# EXERCISE 4: Find strings with specific patterns
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Pattern Detection")
print("=" * 50)

# Find strings with MORE uppercase than lowercase
print("\nStrings with more UPPERCASE than lowercase:")
for string in sample_strings:
    upper = sum(1 for char in string if char.isupper())
    lower = sum(1 for char in string if char.islower())
    if upper > lower:
        print(f"  - {string} (Upper: {upper}, Lower: {lower})")

# Find ALL UPPERCASE strings
print("\nStrings that are ALL UPPERCASE:")
for string in sample_strings:
    # Check if string has letters AND all letters are uppercase
    if string.isupper() and any(char.isalpha() for char in string):
        print(f"  - {string}")

# Find ALL LOWERCASE strings
print("\nStrings that are ALL LOWERCASE:")
for string in sample_strings:
    # Check if string has letters AND all letters are lowercase
    if string.islower() and any(char.isalpha() for char in string):
        print(f"  - {string}")


# ============================================
# BONUS: Advanced Techniques
# ============================================
print("\n" + "=" * 50)
print("BONUS: Advanced Techniques")
print("=" * 50)

# Get lists of actual uppercase and lowercase characters
s = "HelloWorld123"
uppercase_letters = [char for char in s if char.isupper()]
lowercase_letters = [char for char in s if char.islower()]

print(f"\nString: {s}")
print(f"Uppercase letters: {uppercase_letters}")  # ['H', 'W']
print(f"Lowercase letters: {lowercase_letters}")  # ['e', 'l', 'l', 'o', 'o', 'r', 'l', 'd']

# Using filter() function (functional programming approach)
uppercase_filtered = list(filter(str.isupper, s))
lowercase_filtered = list(filter(str.islower, s))
print(f"\nUsing filter():")
print(f"Uppercase: {uppercase_filtered}")
print(f"Lowercase: {lowercase_filtered}")


# ============================================
# KEY TAKEAWAYS
# ============================================
"""
COMPARISON: All methods work, choose based on:

1. Generator expression with sum() - RECOMMENDED
   - Most Pythonic and concise
   - Memory efficient (doesn't create intermediate lists)
   - Example: sum(1 for char in s if char.isupper())

2. Traditional for loop
   - Most explicit and easy to understand
   - Good for beginners
   - Easy to debug

3. List comprehension with len()
   - Useful when you need the actual characters, not just count
   - Example: len([char for char in s if char.isupper()])

IMPORTANT NOTES:
- .isupper() and .islower() return False for non-letter characters (numbers, symbols)
- Use .isalpha() to check if a character is a letter
- String methods like .isupper() work on both single characters and full strings
"""
