"""
============================================
STRING METHODS PRACTICE - SOLUTION
============================================
Run string_methods_practice_setup.py FIRST to try it yourself!
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

print(f"Original: {s}")
print(f"Upper: {s.upper()}")           # HELLO WORLD
print(f"Lower: {s.lower()}")           # hello world
print(f"Swapcase: {s.swapcase()}")     # hELLO wORLD
print(f"Title: {s.title()}")           # Hello World
print(f"Capitalize: {s.capitalize()}") # Hello world

# Note the differences:
# - .title() capitalizes first letter of EACH word
# - .capitalize() capitalizes ONLY the first letter of the string


# ============================================
# EXERCISE 2: String Searching
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: String Searching")
print("=" * 50)

text = "Python is awesome. Python is powerful."

# .find() returns the index of first occurrence (-1 if not found)
position = text.find("Python")
print(f"Position of 'Python': {position}")  # 0

# .count() returns how many times substring appears
count = text.count("Python")
print(f"Count of 'Python': {count}")  # 2

# .startswith() checks if string starts with substring
starts = text.startswith("Python")
print(f"Starts with 'Python': {starts}")  # True

# .endswith() checks if string ends with substring
ends = text.endswith("powerful.")
print(f"Ends with 'powerful.': {ends}")  # True

# Bonus: .index() is like .find() but raises error if not found
try:
    idx = text.index("Python")
    print(f"Index of 'Python': {idx}")  # 0
except ValueError:
    print("Not found!")


# ============================================
# EXERCISE 3: String Cleaning
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: String Cleaning")
print("=" * 50)

messy = "  Python Programming  "

print(f"Original: '{messy}'")
print(f"Strip: '{messy.strip()}'")      # 'Python Programming'
print(f"Lstrip: '{messy.lstrip()}'")    # 'Python Programming  '
print(f"Rstrip: '{messy.rstrip()}'")    # '  Python Programming'

# You can also strip specific characters
text = "***Hello***"
print(f"\nStrip asterisks: '{text.strip('*')}'")  # 'Hello'


# ============================================
# EXERCISE 4: String Transformation
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: String Transformation")
print("=" * 50)

phone = "Apple - iPhone 13"

# .split() splits string into a list
parts = phone.split(" - ")
print(f"Split result: {parts}")  # ['Apple', 'iPhone 13']

# Extract parts
brand = parts[0]
model = parts[1]
print(f"Brand: {brand}")  # Apple
print(f"Model: {model}")  # iPhone 13

# .replace() replaces substring
new_phone = phone.replace("iPhone", "iPad")
print(f"Replaced: {new_phone}")  # Apple - iPad 13


# ============================================
# EXERCISE 5: Combining Methods (Like SQL!)
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Combining Methods")
print("=" * 50)

# This is similar to SQL's TRIM and SPLIT_PART!
data = "  Samsung - Galaxy S21  "

# METHOD 1: Step by step (easier to understand)
cleaned = data.strip()              # "Samsung - Galaxy S21"
parts = cleaned.split(" - ")        # ['Samsung', 'Galaxy S21']
brand = parts[0]                    # 'Samsung'
model = parts[1]                    # 'Galaxy S21'
brand_upper = brand.upper()         # 'SAMSUNG'

print(f"Original: '{data}'")
print(f"Cleaned: '{cleaned}'")
print(f"Brand: {brand_upper}")
print(f"Model: {model}")

# METHOD 2: Chained (more Pythonic, like SQL function chains!)
brand_chained = data.strip().split(" - ")[0].upper()
model_chained = data.strip().split(" - ")[1]

print(f"\nChained method:")
print(f"Brand: {brand_chained}")
print(f"Model: {model_chained}")


# ============================================
# BONUS: Real-World Example (Like SQL apple_phones!)
# ============================================
print("\n" + "=" * 50)
print("BONUS: Parse Phone Data (Like SQL Example)")
print("=" * 50)

# Similar to your SQL apple_phones exercise!
phones = [
    "Acer - Iconia Talk S",
    "Acer - Liquid Z6 Plus",
    "Samsung - Galaxy S21",
    "Apple - iPhone 13",
    "Google - Pixel 6"
]

print("\nParsed Phone Data:")
print("-" * 50)
for phone in phones:
    parts = phone.split(" - ")
    brand = parts[0].strip()
    model = parts[1].strip()
    
    # Count uppercase and lowercase in model name
    upper_count = sum(1 for c in model if c.isupper())
    lower_count = sum(1 for c in model if c.islower())
    
    print(f"Brand: {brand:10} | Model: {model:20} | Upper: {upper_count} | Lower: {lower_count}")


# ============================================
# KEY TAKEAWAYS
# ============================================
"""
COMMON STRING METHODS:

Case Conversion:
- .upper()      - Convert to uppercase
- .lower()      - Convert to lowercase
- .swapcase()   - Swap upper/lower case
- .title()      - Capitalize each word
- .capitalize() - Capitalize first letter only

Searching:
- .find(sub)       - Find position (-1 if not found)
- .index(sub)      - Find position (error if not found)
- .count(sub)      - Count occurrences
- .startswith(sub) - Check if starts with
- .endswith(sub)   - Check if ends with

Cleaning:
- .strip()   - Remove leading/trailing whitespace
- .lstrip()  - Remove leading whitespace
- .rstrip()  - Remove trailing whitespace

Transformation:
- .split(delimiter)    - Split into list
- .replace(old, new)   - Replace substring
- .join(list)          - Join list into string

Checking:
- .isupper()  - Check if uppercase
- .islower()  - Check if lowercase
- .isalpha()  - Check if alphabetic
- .isdigit()  - Check if numeric
- .isalnum()  - Check if alphanumeric

CHAINING METHODS (like SQL function chains!):
data.strip().split(" - ")[0].upper()
└─────┘ └────────────┘ └─┘ └─────┘
  1st       2nd        3rd   4th
  
Read from left to right, each method operates on the result of the previous one!
"""
