"""
============================================
PALINDROME CHECKING - SOLUTION
============================================
Run palindrome_check_setup.py FIRST to try it yourself!
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

# Check if string reads the same forwards and backwards
if text == text[::-1]:
    print(f"Text: {text}")
    print("Palindrome")
else:
    print(f"Text: {text}")
    print("Not a Palindrome")

# How it works:
print(f"\nHow it works:")
print(f"Original: {text}")
print(f"Reversed: {text[::-1]}")
print(f"Are they equal? {text == text[::-1]}")


# ============================================
# EXERCISE 2: Check Multiple Strings
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Check Multiple Strings")
print("=" * 50)

words = ["madam", "racecar", "hello", "noon", "python"]

for word in words:
    if word == word[::-1]:
        print(f"{word}: Palindrome ✓")
    else:
        print(f"{word}: Not a Palindrome ✗")


# ============================================
# EXERCISE 3: Case-Insensitive Check
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Case-Insensitive Check")
print("=" * 50)

text = "Madam"  # Capital M

# Without .lower() - fails!
print(f"Text: {text}")
print(f"Without .lower(): {text == text[::-1]}")  # False (M != m)

# With .lower() - works!
text_lower = text.lower()
is_palindrome = text_lower == text_lower[::-1]
print(f"With .lower(): {is_palindrome}")  # True

# One-liner
if text.lower() == text.lower()[::-1]:
    print("Result: Palindrome")


# ============================================
# EXERCISE 4: Ignore Spaces and Punctuation
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Ignore Spaces and Punctuation")
print("=" * 50)

phrase = "A man a plan a canal Panama"

# Clean the phrase: remove spaces and lowercase
cleaned = phrase.replace(" ", "").lower()

print(f"Original: {phrase}")
print(f"Cleaned: {cleaned}")
print(f"Reversed: {cleaned[::-1]}")

if cleaned == cleaned[::-1]:
    print("Result: Palindrome ✓")
else:
    print("Result: Not a Palindrome ✗")

# More complex example with punctuation
phrase2 = "A man, a plan, a canal: Panama!"

# Remove all non-alphanumeric characters
import string
cleaned2 = ''.join(char.lower() for char in phrase2 if char.isalnum())

print(f"\nOriginal: {phrase2}")
print(f"Cleaned: {cleaned2}")
print(f"Is palindrome: {cleaned2 == cleaned2[::-1]}")


# ============================================
# EXERCISE 5: Palindrome Function
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Create a Palindrome Function")
print("=" * 50)

def is_palindrome(text, ignore_spaces=True, ignore_case=True):
    """
    Check if text is a palindrome
    
    Args:
        text: String to check
        ignore_spaces: If True, ignore spaces
        ignore_case: If True, ignore case differences
    
    Returns:
        bool: True if palindrome, False otherwise
    """
    # Clean the text
    cleaned = text
    
    if ignore_spaces:
        cleaned = cleaned.replace(" ", "")
    
    if ignore_case:
        cleaned = cleaned.lower()
    
    # Check if palindrome
    return cleaned == cleaned[::-1]


# Test the function
test_cases = [
    "madam",
    "Madam",
    "A man a plan a canal Panama",
    "racecar",
    "hello",
    "Was it a car or a cat I saw",
    "python"
]

print("Testing palindrome function:")
for test in test_cases:
    result = is_palindrome(test)
    status = "✓" if result else "✗"
    print(f"  {status} '{test}': {result}")


# ============================================
# BONUS: Different Palindrome Checking Methods
# ============================================
print("\n" + "=" * 50)
print("BONUS: Different Methods")
print("=" * 50)

text = "racecar"

# METHOD 1: Using slicing (RECOMMENDED)
method1 = text == text[::-1]
print(f"Method 1 (slicing): {method1}")

# METHOD 2: Using reversed() and join
method2 = text == ''.join(reversed(text))
print(f"Method 2 (reversed): {method2}")

# METHOD 3: Manual comparison (for learning)
def is_palindrome_manual(text):
    left = 0
    right = len(text) - 1
    
    while left < right:
        if text[left] != text[right]:
            return False
        left += 1
        right -= 1
    
    return True

method3 = is_palindrome_manual(text)
print(f"Method 3 (manual): {method3}")

# METHOD 4: Using list comparison
method4 = list(text) == list(reversed(text))
print(f"Method 4 (list): {method4}")


# ============================================
# BONUS: Palindrome Numbers
# ============================================
print("\n" + "=" * 50)
print("BONUS: Palindrome Numbers")
print("=" * 50)

# Check if a number is a palindrome
numbers = [121, 12321, 123, 1001, 12345]

print("Palindrome numbers:")
for num in numbers:
    num_str = str(num)
    if num_str == num_str[::-1]:
        print(f"  {num}: Palindrome ✓")
    else:
        print(f"  {num}: Not a Palindrome ✗")


# ============================================
# KEY TAKEAWAYS
# ============================================
"""
PALINDROME CHECKING:

1. BASIC CHECK ⭐ MOST COMMON
   if text == text[::-1]:
       print("Palindrome")
   - Simple and readable
   - Uses string slicing
   - Works for any string

2. CASE-INSENSITIVE
   if text.lower() == text.lower()[::-1]:
   - Handles "Madam" and "madam" the same
   - Always use .lower() for real palindromes

3. IGNORE SPACES
   cleaned = text.replace(" ", "").lower()
   if cleaned == cleaned[::-1]:
   - Handles phrases like "A man a plan a canal Panama"
   - Remove spaces before checking

4. IGNORE PUNCTUATION
   cleaned = ''.join(c.lower() for c in text if c.isalnum())
   if cleaned == cleaned[::-1]:
   - Removes all non-alphanumeric characters
   - Most robust method

IMPORTANT NOTES:
- [::-1] reverses the string
- Always clean text before checking (spaces, case, punctuation)
- Works for numbers too: str(121) == str(121)[::-1]

COMMON PALINDROMES:
- Words: madam, racecar, noon, level, radar
- Phrases: "A man a plan a canal Panama"
- Numbers: 121, 12321, 1001

EXAMPLES:
- Simple: "madam" == "madam"[::-1] → True
- Case: "Madam".lower() == "madam"[::-1] → True
- Phrase: "amanaplanacanalpanama" == "amanaplanacanalpanama"[::-1] → True
"""
