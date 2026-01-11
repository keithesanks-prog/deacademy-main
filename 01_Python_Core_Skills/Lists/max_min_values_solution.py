"""
============================================
MAX AND MIN VALUES - SOLUTION
============================================
Run max_min_values_setup.py FIRST to try it yourself!
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

# Using max() and min() - SIMPLE AND DIRECT!
largest = max(numbers)
smallest = min(numbers)

print(f"Numbers: {numbers}")
print(f"Largest Number: {largest}")   # 8
print(f"Smallest Number: {smallest}") # 1


# ============================================
# EXERCISE 2: Max/Min with Different Data Types
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Different Data Types")
print("=" * 50)

# Works with floats
prices = [19.99, 5.50, 12.75, 8.00, 25.00]
print(f"Prices: {prices}")
print(f"Max Price: ${max(prices)}")  # 25.0
print(f"Min Price: ${min(prices)}")  # 5.5

# Works with strings (alphabetical order)
names = ["Alice", "Bob", "Charlie", "David"]
print(f"\nNames: {names}")
print(f"Max (alphabetically): {max(names)}")  # 'David'
print(f"Min (alphabetically): {min(names)}")  # 'Alice'

# Note: Uppercase comes before lowercase in ASCII
mixed_names = ["alice", "Bob", "Charlie"]
print(f"\nMixed case: {mixed_names}")
print(f"Max: {max(mixed_names)}")  # 'alice' (lowercase 'a' > uppercase 'C')


# ============================================
# EXERCISE 3: Find Index of Max/Min
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Find Index of Max/Min")
print("=" * 50)

numbers = [4, 1, 7, 3, 8, 2]

# Find the index of max/min values
max_value = max(numbers)
min_value = min(numbers)

max_index = numbers.index(max_value)
min_index = numbers.index(min_value)

print(f"Numbers: {numbers}")
print(f"Max value {max_value} is at index {max_index}")  # 8 at index 4
print(f"Min value {min_value} is at index {min_index}")  # 1 at index 1

# One-liner version
print(f"\nOne-liner:")
print(f"Max index: {numbers.index(max(numbers))}")
print(f"Min index: {numbers.index(min(numbers))}")


# ============================================
# EXERCISE 4: Max/Min with Key Function
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Custom Comparison")
print("=" * 50)

words = ["Python", "is", "awesome", "to", "learn"]

# Find longest and shortest words using key=len
longest_word = max(words, key=len)
shortest_word = min(words, key=len)

print(f"Words: {words}")
print(f"Longest word: '{longest_word}' ({len(longest_word)} letters)")   # 'awesome' (7)
print(f"Shortest word: '{shortest_word}' ({len(shortest_word)} letters)") # 'is' or 'to' (2)

# Show all word lengths
print("\nAll word lengths:")
for word in words:
    print(f"  {word}: {len(word)} letters")


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

# Find student with highest and lowest scores
top_student = max(students, key=lambda x: x['score'])
lowest_student = min(students, key=lambda x: x['score'])

print("Students:")
for student in students:
    print(f"  {student['name']}: {student['score']}")

print(f"\nTop student: {top_student['name']} with score {top_student['score']}")
print(f"Lowest student: {lowest_student['name']} with score {lowest_student['score']}")


# ============================================
# BONUS: Alternative Methods
# ============================================
print("\n" + "=" * 50)
print("BONUS: Alternative Methods")
print("=" * 50)

numbers = [4, 1, 7, 3, 8, 2]

# METHOD 1: Using max() and min() (RECOMMENDED)
print("Method 1 - Built-in functions:")
print(f"Max: {max(numbers)}, Min: {min(numbers)}")

# METHOD 2: Using sorted()
print("\nMethod 2 - Using sorted():")
sorted_nums = sorted(numbers)
print(f"Max: {sorted_nums[-1]}, Min: {sorted_nums[0]}")

# METHOD 3: Manual loop (for learning purposes)
print("\nMethod 3 - Manual loop:")
current_max = numbers[0]
current_min = numbers[0]
for num in numbers:
    if num > current_max:
        current_max = num
    if num < current_min:
        current_min = num
print(f"Max: {current_max}, Min: {current_min}")


# ============================================
# BONUS: Edge Cases
# ============================================
print("\n" + "=" * 50)
print("BONUS: Edge Cases")
print("=" * 50)

# Single element
single = [42]
print(f"Single element {single}: max={max(single)}, min={min(single)}")

# All same values
same = [5, 5, 5, 5]
print(f"All same {same}: max={max(same)}, min={min(same)}")

# Negative numbers
negatives = [-5, -2, -8, -1]
print(f"Negatives {negatives}: max={max(negatives)}, min={min(negatives)}")

# Mixed positive and negative
mixed = [-3, 5, -1, 8, 0]
print(f"Mixed {mixed}: max={max(mixed)}, min={min(mixed)}")


# ============================================
# KEY TAKEAWAYS
# ============================================
"""
FINDING MAX AND MIN VALUES:

1. BASIC USAGE ⭐ MOST COMMON
   largest = max(numbers)
   smallest = min(numbers)
   - Works with numbers, strings, any comparable type
   - Simple and readable

2. WITH KEY FUNCTION
   longest = max(words, key=len)
   - Custom comparison criteria
   - Use lambda for complex objects
   - Example: max(students, key=lambda x: x['score'])

3. FINDING INDEX
   max_index = numbers.index(max(numbers))
   - Combines max() with .index()
   - Returns position of max/min value

IMPORTANT NOTES:
- max() and min() work on any iterable
- Strings are compared alphabetically
- Empty lists will raise ValueError
- For ties, returns first occurrence

COMMON PATTERNS:
- Largest number: max(numbers)
- Smallest number: min(numbers)
- Longest word: max(words, key=len)
- Highest score: max(students, key=lambda x: x['score'])
"""
