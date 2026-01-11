"""
============================================
DICTIONARY MERGING - SOLUTION
============================================
Run dict_merging_setup.py FIRST to try it yourself!
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

# METHOD 1: Using ** unpacking (MOST COMMON!)
merged_dict = {**dict1, **dict2}

print(f"Dict 1: {dict1}")
print(f"Dict 2: {dict2}")
print(f"Merged Dictionary: {merged_dict}")
# Output: {'a': 1, 'b': 2, 'c': 3, 'd': 4}


# ============================================
# EXERCISE 2: Handling Duplicate Keys
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Handling Duplicate Keys")
print("=" * 50)

dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}  # 'b' exists in both!

# The LAST dictionary's value wins!
merged = {**dict1, **dict2}
print(f"Dict 1: {dict1}")
print(f"Dict 2: {dict2}")
print(f"Merged {**dict1, **dict2}: {merged}")
# Output: {'a': 1, 'b': 3, 'c': 4}
# dict2's value for 'b' (3) overwrites dict1's value (2)

# Reverse order - dict1 wins
merged_reversed = {**dict2, **dict1}
print(f"Merged {**dict2, **dict1}: {merged_reversed}")
# Output: {'b': 2, 'c': 4, 'a': 1}
# dict1's value for 'b' (2) overwrites dict2's value (3)

print("\nKey takeaway: Later dictionaries override earlier ones!")


# ============================================
# EXERCISE 3: Merge Multiple Dictionaries
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Merge Multiple Dictionaries")
print("=" * 50)

dict1 = {"a": 1}
dict2 = {"b": 2}
dict3 = {"c": 3}

# Merge all three at once
merged_all = {**dict1, **dict2, **dict3}
print(f"Dict 1: {dict1}")
print(f"Dict 2: {dict2}")
print(f"Dict 3: {dict3}")
print(f"Merged: {merged_all}")
# Output: {'a': 1, 'b': 2, 'c': 3}

# With overlapping keys
dict1 = {"a": 1, "x": 10}
dict2 = {"b": 2, "x": 20}
dict3 = {"c": 3, "x": 30}

merged_overlap = {**dict1, **dict2, **dict3}
print(f"\nWith overlapping 'x' key:")
print(f"Merged: {merged_overlap}")
# Output: {'a': 1, 'x': 30, 'b': 2, 'c': 3}
# dict3's value for 'x' wins (30)


# ============================================
# EXERCISE 4: Other Merging Methods
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Other Merging Methods")
print("=" * 50)

dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}

# METHOD 1: Using ** unpacking (already shown)
merged1 = {**dict1, **dict2}
print(f"Method 1 (** unpacking): {merged1}")

# METHOD 2: Using .update() (MODIFIES ORIGINAL!)
dict1_copy = dict1.copy()  # Make a copy to preserve original
dict1_copy.update(dict2)
print(f"Method 2 (.update()): {dict1_copy}")
# Note: .update() modifies dict1_copy in place, returns None

# METHOD 3: Using | operator (Python 3.9+)
merged3 = dict1 | dict2
print(f"Method 3 (| operator): {merged3}")

# METHOD 4: Using dict() constructor
merged4 = dict(dict1, **dict2)
print(f"Method 4 (dict()): {merged4}")


# ============================================
# EXERCISE 5: Practical Application
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Practical Application")
print("=" * 50)

user_defaults = {"theme": "light", "language": "en", "notifications": True}
user_preferences = {"theme": "dark", "font_size": 14}

# Merge with user preferences overriding defaults
final_settings = {**user_defaults, **user_preferences}

print("Default settings:")
for key, value in user_defaults.items():
    print(f"  {key}: {value}")

print("\nUser preferences:")
for key, value in user_preferences.items():
    print(f"  {key}: {value}")

print("\nFinal settings:")
for key, value in final_settings.items():
    print(f"  {key}: {value}")

# Output shows:
# - theme: 'dark' (from user_preferences, overrides default)
# - language: 'en' (from defaults, no override)
# - notifications: True (from defaults, no override)
# - font_size: 14 (from user_preferences, new key)


# ============================================
# BONUS: Comparison of All Methods
# ============================================
print("\n" + "=" * 50)
print("BONUS: Method Comparison")
print("=" * 50)

dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}

print("""
METHOD COMPARISON:

1. {**dict1, **dict2} ⭐ RECOMMENDED
   - Creates NEW dictionary
   - Original dicts unchanged
   - Works in Python 3.5+
   - Most readable

2. dict1.update(dict2)
   - Modifies dict1 IN-PLACE
   - Returns None (not the dict!)
   - Use when you want to modify original

3. dict1 | dict2
   - Creates NEW dictionary
   - Clean syntax
   - Requires Python 3.9+
   - Similar to {**dict1, **dict2}

4. dict(dict1, **dict2)
   - Creates NEW dictionary
   - Only works if dict2 keys are strings
   - Less common
""")

# Demonstrate the difference
print("Demonstration:")
original = {"a": 1}
dict2 = {"b": 2}

# Method 1: ** unpacking (creates new)
merged = {**original, **dict2}
print(f"After {{**original, **dict2}}:")
print(f"  original: {original}")  # Unchanged
print(f"  merged: {merged}")

# Method 2: .update() (modifies original)
original2 = {"a": 1}
original2.update(dict2)
print(f"\nAfter original.update(dict2):")
print(f"  original: {original2}")  # Changed!


# ============================================
# BONUS: Common Mistakes
# ============================================
print("\n" + "=" * 50)
print("BONUS: Common Mistakes")
print("=" * 50)

# MISTAKE 1: Trying to assign result of .update()
dict1 = {"a": 1}
result = dict1.update({"b": 2})
print(f"Mistake 1 - result of .update(): {result}")  # None!
print(f"But dict1 is updated: {dict1}")  # {'a': 1, 'b': 2}

# MISTAKE 2: Forgetting order matters with duplicates
dict1 = {"x": 1}
dict2 = {"x": 2}
print(f"\nMistake 2 - Order matters:")
print(f"{{**dict1, **dict2}}: {{{**dict1, **dict2}}}")  # x: 2
print(f"{{**dict2, **dict1}}: {{{**dict2, **dict1}}}")  # x: 1


# ============================================
# KEY TAKEAWAYS
# ============================================
"""
DICTIONARY MERGING METHODS:

1. ** UNPACKING ⭐ RECOMMENDED
   merged = {**dict1, **dict2}
   - Creates new dictionary
   - Original dicts unchanged
   - Later dicts override earlier ones
   - Works in Python 3.5+

2. .update() METHOD
   dict1.update(dict2)
   - Modifies dict1 in place
   - Returns None
   - Use when you want to modify original

3. | OPERATOR (Python 3.9+)
   merged = dict1 | dict2
   - Creates new dictionary
   - Clean syntax
   - Same behavior as ** unpacking

IMPORTANT NOTES:
- Order matters: {**dict1, **dict2} - dict2 wins on conflicts
- .update() modifies original, returns None
- ** unpacking creates new dict
- Can merge multiple: {**d1, **d2, **d3}

COMMON PATTERNS:
- Basic merge: {**dict1, **dict2}
- Override defaults: {**defaults, **user_prefs}
- Merge many: {**d1, **d2, **d3, **d4}
- Add single key: {**dict1, "new_key": "value"}
"""
