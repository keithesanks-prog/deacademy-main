"""
============================================
VOWEL COUNTING - SOLUTION
============================================
Run vowel_counting_setup.py FIRST to try it yourself!
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

# METHOD 1: Traditional for loop (EXPLICIT AND CLEAR)
count = 0
for i in text:
    if i in 'aeiou':
        count += 1

print(f"Text: {text}")
print(f"Number of Vowels: {count}")  # 1 (only 'o')

# Show which characters are vowels
print("\nCharacter breakdown:")
for char in text:
    if char in 'aeiou':
        print(f"  '{char}' - VOWEL ✓")
    else:
        print(f"  '{char}' - consonant")


# ============================================
# EXERCISE 2: Count Vowels with Generator Expression
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Generator Expression Method")
print("=" * 50)

string = "Python".lower()
vowels = "aeiou"

# METHOD 2: Generator expression with sum() (MOST PYTHONIC!)
vowel_count = sum(1 for char in string if char in vowels)

print(f"Text: {string}")
print(f"Number of vowels: {vowel_count}")  # 1

# How it works step by step:
print("\nHow generator expression works:")
print(f"1. Loop through: {list(string)}")
print(f"2. Filter vowels: {[char for char in string if char in vowels]}")
print(f"3. Generate 1 for each: {[1 for char in string if char in vowels]}")
print(f"4. Sum them up: {sum(1 for char in string if char in vowels)}")


# ============================================
# EXERCISE 3: Case-Insensitive Counting
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Case-Insensitive Counting")
print("=" * 50)

text = "HELLO WORLD"

# Without lowercase - misses uppercase vowels!
count_wrong = sum(1 for char in text if char in 'aeiou')
print(f"Text: {text}")
print(f"Counting without .lower(): {count_wrong}")  # 0 (misses all!)

# With lowercase - CORRECT!
count_correct = sum(1 for char in text.lower() if char in 'aeiou')
print(f"Counting with .lower(): {count_correct}")  # 3 (E, O, O)

# Alternative: Check both lowercase and uppercase
count_alt = sum(1 for char in text if char in 'aeiouAEIOU')
print(f"Checking both cases: {count_alt}")  # 3


# ============================================
# EXERCISE 4: Count Each Vowel Separately
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Count Each Vowel")
print("=" * 50)

text = "Programming is fun"
text_lower = text.lower()

# Count each vowel individually
print(f"Text: {text}")
print("\nVowel breakdown:")
for vowel in 'aeiou':
    count = text_lower.count(vowel)
    print(f"  '{vowel}': {count}")

# Total vowels
total = sum(text_lower.count(v) for v in 'aeiou')
print(f"\nTotal vowels: {total}")


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

print("Vowel analysis:")
max_vowels = 0
max_sentence = ""

for sentence in sentences:
    vowel_count = sum(1 for char in sentence.lower() if char in 'aeiou')
    print(f"  '{sentence}': {vowel_count} vowels")
    
    if vowel_count > max_vowels:
        max_vowels = vowel_count
        max_sentence = sentence

print(f"\nSentence with most vowels:")
print(f"  '{max_sentence}' with {max_vowels} vowels")


# ============================================
# BONUS: Comparison of All Methods
# ============================================
print("\n" + "=" * 50)
print("BONUS: All Methods Side by Side")
print("=" * 50)

text = "Hello World"

# METHOD 1: For loop
count1 = 0
for char in text:
    if char.lower() in 'aeiou':
        count1 += 1

# METHOD 2: Generator expression (RECOMMENDED)
count2 = sum(1 for char in text.lower() if char in 'aeiou')

# METHOD 3: List comprehension with len()
count3 = len([char for char in text.lower() if char in 'aeiou'])

# METHOD 4: Using filter()
count4 = len(list(filter(lambda c: c in 'aeiou', text.lower())))

print(f"Text: {text}")
print(f"Method 1 (for loop): {count1}")
print(f"Method 2 (generator): {count2}")
print(f"Method 3 (list comp): {count3}")
print(f"Method 4 (filter): {count4}")
print("\nAll methods give the same result!")


# ============================================
# BONUS: Get Actual Vowels (Not Just Count)
# ============================================
print("\n" + "=" * 50)
print("BONUS: Extract Vowels")
print("=" * 50)

text = "Programming"

# Get list of all vowels in the text
vowels_found = [char for char in text.lower() if char in 'aeiou']
print(f"Text: {text}")
print(f"Vowels found: {vowels_found}")  # ['o', 'a', 'i']
print(f"Count: {len(vowels_found)}")    # 3

# Get unique vowels
unique_vowels = list(set(vowels_found))
print(f"Unique vowels: {sorted(unique_vowels)}")  # ['a', 'i', 'o']


# ============================================
# KEY TAKEAWAYS
# ============================================
"""
VOWEL COUNTING METHODS:

1. FOR LOOP METHOD (EXPLICIT)
   count = 0
   for char in text:
       if char in 'aeiou':
           count += 1
   - Easy to understand
   - Good for beginners
   - Can add debug prints

2. GENERATOR EXPRESSION (PYTHONIC) ⭐ RECOMMENDED
   vowel_count = sum(1 for char in string if char in vowels)
   - Most concise
   - Memory efficient
   - Pythonic style

3. LIST COMPREHENSION
   count = len([char for char in text if char in 'aeiou'])
   - Useful when you need the actual vowels
   - Creates intermediate list

IMPORTANT NOTES:
- Always use .lower() for case-insensitive counting
- Vowels are: a, e, i, o, u
- Can check both cases: 'aeiouAEIOU'
- Generator expression is more memory efficient than list comprehension

COMMON PATTERNS:
- Count vowels: sum(1 for c in text.lower() if c in 'aeiou')
- Get vowels: [c for c in text.lower() if c in 'aeiou']
- Count specific vowel: text.lower().count('a')
- Unique vowels: set(c for c in text.lower() if c in 'aeiou')
"""
