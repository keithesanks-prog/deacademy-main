"""
============================================
LIST REVERSAL - SOLUTION
============================================
Run list_reversal_setup.py FIRST to try it yourself!
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

print(f"Original: {my_list}")
print(f"Reversed: {my_list[::-1]}")  # [5, 4, 3, 2, 1]


# ============================================
# EXERCISE 2: In-Place vs Copy Reversal
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: In-Place vs Copy Reversal")
print("=" * 50)

# METHOD 1: Using .reverse() (modifies original!)
print("METHOD 1 - .reverse() (in-place):")
list1 = [1, 2, 3, 4, 5]
print(f"Before: {list1}")
list1.reverse()  # Modifies list1 directly, returns None
print(f"After: {list1}")  # [5, 4, 3, 2, 1]

# METHOD 2: Using [::-1] (creates new list)
print("\nMETHOD 2 - [::-1] (creates copy):")
list2 = [1, 2, 3, 4, 5]
reversed_list2 = list2[::-1]
print(f"Original: {list2}")           # [1, 2, 3, 4, 5] - unchanged!
print(f"Reversed copy: {reversed_list2}")  # [5, 4, 3, 2, 1]
print(f"Original unchanged: {list2}")  # [1, 2, 3, 4, 5]


# ============================================
# EXERCISE 3: Using reversed() Function
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Using reversed() Function")
print("=" * 50)

my_list = [1, 2, 3, 4, 5]

# reversed() returns an iterator, need to convert to list
reversed_list = list(reversed(my_list))
print(f"Original: {my_list}")
print(f"Reversed: {reversed_list}")

# You can also use it in a loop
print("\nIterating with reversed():")
for item in reversed(my_list):
    print(item, end=" ")  # 5 4 3 2 1
print()


# ============================================
# EXERCISE 4: Reverse Different Data Types
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Reverse Different Data Types")
print("=" * 50)

# Reverse a list of strings
names = ["Alice", "Bob", "Charlie"]
print(f"Names: {names}")
print(f"Reversed: {names[::-1]}")  # ['Charlie', 'Bob', 'Alice']

# Reverse a list of mixed types
mixed = [1, "two", 3.0, True]
print(f"\nMixed: {mixed}")
print(f"Reversed: {mixed[::-1]}")  # [True, 3.0, 'two', 1]

# Reverse a string (two methods)
text = "Python"
print(f"\nString: {text}")

# Method 1: Convert to list, reverse, join back
reversed_text1 = ''.join(list(text)[::-1])
print(f"Reversed (method 1): {reversed_text1}")  # nohtyP

# Method 2: Use string slicing directly
reversed_text2 = text[::-1]
print(f"Reversed (method 2): {reversed_text2}")  # nohtyP

# Method 3: Using reversed() and join
reversed_text3 = ''.join(reversed(text))
print(f"Reversed (method 3): {reversed_text3}")  # nohtyP


# ============================================
# EXERCISE 5: Practical Applications
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Practical Applications")
print("=" * 50)

# Check if a list is a palindrome
test_list1 = [1, 2, 3, 2, 1]
test_list2 = [1, 2, 3, 4, 5]

is_palindrome1 = test_list1 == test_list1[::-1]
is_palindrome2 = test_list2 == test_list2[::-1]

print(f"{test_list1} is palindrome: {is_palindrome1}")  # True
print(f"{test_list2} is palindrome: {is_palindrome2}")  # False

# Get the last 3 elements in reverse order
numbers = [10, 20, 30, 40, 50, 60, 70]
last_three_reversed = numbers[-3:][::-1]
print(f"\nOriginal: {numbers}")
print(f"Last 3 reversed: {last_three_reversed}")  # [70, 60, 50]

# Alternative: Get last 3 in reverse using negative slicing
last_three_alt = numbers[:-4:-1]
print(f"Last 3 reversed (alt): {last_three_alt}")  # [70, 60, 50]


# ============================================
# BONUS: Performance Comparison
# ============================================
print("\n" + "=" * 50)
print("BONUS: When to Use Each Method")
print("=" * 50)

print("""
METHOD COMPARISON:

1. list[::-1]
   - Creates a NEW reversed list
   - Original list unchanged
   - Most common and readable
   - Example: [1,2,3][::-1] → [3,2,1]

2. list.reverse()
   - Modifies list IN-PLACE
   - Returns None (not the list!)
   - Use when you want to change original
   - Example: nums.reverse() → nums is now reversed

3. reversed(list)
   - Returns an ITERATOR (not a list)
   - Memory efficient for large lists
   - Need to convert: list(reversed(...))
   - Good for loops: for x in reversed(nums)

RECOMMENDATION:
- Use [::-1] for most cases (clear and creates copy)
- Use .reverse() when you want to modify original
- Use reversed() in loops to save memory
""")


# ============================================
# BONUS: Common Mistakes
# ============================================
print("\n" + "=" * 50)
print("BONUS: Common Mistakes to Avoid")
print("=" * 50)

# MISTAKE 1: Trying to assign result of .reverse()
nums = [1, 2, 3]
result = nums.reverse()  # Returns None!
print(f"Mistake 1 - result of .reverse(): {result}")  # None
print(f"But nums is reversed: {nums}")  # [3, 2, 1]

# MISTAKE 2: Forgetting to convert reversed() to list
nums = [1, 2, 3]
rev = reversed(nums)
print(f"\nMistake 2 - reversed() without list(): {rev}")  # <list_reverseiterator object>
print(f"Correct - list(reversed()): {list(reversed(nums))}")  # [3, 2, 1]


# ============================================
# KEY TAKEAWAYS
# ============================================
"""
THREE WAYS TO REVERSE A LIST:

1. SLICING [::-1] ⭐ RECOMMENDED
   my_list[::-1]
   - Creates new reversed list
   - Original unchanged
   - Most Pythonic

2. .reverse() METHOD
   my_list.reverse()
   - Modifies original list
   - Returns None
   - Use when you want in-place reversal

3. reversed() FUNCTION
   list(reversed(my_list))
   - Returns iterator
   - Need to convert to list
   - Good for loops

REMEMBER:
- [::-1] creates a copy
- .reverse() modifies original
- reversed() returns iterator
"""
