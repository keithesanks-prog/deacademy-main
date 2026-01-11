"""
============================================
PALINDROME CHECKING - SETUP SCRIPT
============================================
Learn how to check if a string is a palindrome

Your Tasks:
1. Check if a string reads the same forwards and backwards
2. Handle case sensitivity
3. Ignore spaces and punctuation

Key Concepts to Learn:
- String reversal with [::-1]
- String comparison
- String cleaning (.lower(), .replace())
"""

# ============================================
# SAMPLE DATA
# ============================================

word1 = "madam"
word2 = "racecar"
word3 = "hello"
phrase1 = "A man a plan a canal Panama"

# ============================================
# EXERCISE 1: Basic Palindrome Check
# ============================================
print("=" * 50)
print("EXERCISE 1: Basic Palindrome Check")
print("=" * 50)

text = "madam"

# TODO: Check if text == text[::-1]
# TODO: Print "Palindrome" or "Not a Palindrome"


# ============================================
# EXERCISE 2: Check Multiple Strings
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Check Multiple Strings")
print("=" * 50)

words = ["madam", "racecar", "hello", "noon", "python"]

# TODO: Loop through words
# TODO: Check each one and print result


# ============================================
# EXERCISE 3: Case-Insensitive Check
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Case-Insensitive Check")
print("=" * 50)

text = "Madam"  # Capital M

# TODO: Convert to lowercase before checking
# TODO: Check if palindrome


# ============================================
# EXERCISE 4: Ignore Spaces and Punctuation
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Ignore Spaces and Punctuation")
print("=" * 50)

phrase = "A man a plan a canal Panama"

# TODO: Remove spaces and convert to lowercase
# TODO: Check if palindrome
# Hint: phrase.replace(" ", "").lower()


# ============================================
# EXERCISE 5: Palindrome Function
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Create a Palindrome Function")
print("=" * 50)

# TODO: Create a function is_palindrome(text)
# TODO: Function should handle spaces and case
# TODO: Test with multiple inputs


# ============================================
# EXPECTED OUTPUT (for reference)
# ============================================
"""
==================================================
EXERCISE 1: Basic Palindrome Check
==================================================
Text: madam
Palindrome

==================================================
EXERCISE 2: Check Multiple Strings
==================================================
madam: Palindrome
racecar: Palindrome
hello: Not a Palindrome
noon: Palindrome
python: Not a Palindrome

... (and so on)
"""
