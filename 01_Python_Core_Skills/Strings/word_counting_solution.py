"""
============================================
WORD COUNTING - SOLUTION
============================================
Run word_counting_setup.py FIRST to try it yourself!
"""

# ============================================
# SAMPLE DATA
# ============================================

sentence1 = "Python is fun to learn"
sentence2 = "The quick brown fox jumps over the lazy dog"
paragraph = """Python is a great language.
Python is easy to learn.
Many people love Python."""

# ============================================
# EXERCISE 1: Basic Word Counting
# ============================================
print("=" * 50)
print("EXERCISE 1: Basic Word Counting")
print("=" * 50)

sentence = "Python is fun to learn"

# METHOD 1: Using split() and len() (MOST COMMON!)
word_count = len(sentence.split())
print(f"Sentence: {sentence}")
print(f"Word Count: {word_count}")  # 5

# How it works:
# 1. sentence.split() → ['Python', 'is', 'fun', 'to', 'learn']
# 2. len([...]) → 5

print("\nStep by step:")
words = sentence.split()
print(f"1. Split into words: {words}")
print(f"2. Count words: {len(words)}")


# ============================================
# EXERCISE 2: Count Words in Different Texts
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Count Words in Different Texts")
print("=" * 50)

texts = [
    "Hello World",
    "The quick brown fox",
    "Python is awesome",
    "Data Engineering with Python and SQL"
]

for text in texts:
    word_count = len(text.split())
    print(f"Text: {text}")
    print(f"Word Count: {word_count}")
    print()


# ============================================
# EXERCISE 3: Count Specific Words
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Count Specific Words")
print("=" * 50)

text = "Python is great. Python is easy. Python is fun."

# METHOD 1: Using .count() (counts substring occurrences)
python_count = text.count("Python")
is_count = text.count("is")

print(f"Text: {text}")
print(f"'Python' appears: {python_count} times")  # 3
print(f"'is' appears: {is_count} times")  # 3

# METHOD 2: Count words in split list (more accurate for whole words)
words = text.split()
python_count_v2 = words.count("Python")
print(f"\nUsing split and count on list:")
print(f"Words: {words}")
print(f"'Python' appears: {python_count_v2} times")

# METHOD 3: Case-insensitive counting
text_lower = text.lower()
python_count_case_insensitive = text_lower.count("python")
print(f"\nCase-insensitive count of 'python': {python_count_case_insensitive}")


# ============================================
# EXERCISE 4: Advanced Word Analysis
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Advanced Word Analysis")
print("=" * 50)

sentence = "The quick brown fox jumps over the lazy dog"

# Split into words
words = sentence.split()

# Count total words
total_words = len(words)

# Count unique words (using set)
unique_words = len(set(words))

# Find longest word
longest_word = max(words, key=len)

# Find shortest word
shortest_word = min(words, key=len)

print(f"Sentence: {sentence}")
print(f"Total words: {total_words}")  # 9
print(f"Unique words: {unique_words}")  # 9 (all different)
print(f"Longest word: '{longest_word}' ({len(longest_word)} letters)")  # 'quick' or 'brown' or 'jumps'
print(f"Shortest word: '{shortest_word}' ({len(shortest_word)} letters)")  # 'The' or 'fox' or 'the' or 'dog'

# Show all word lengths
print("\nWord lengths:")
for word in words:
    print(f"  {word}: {len(word)} letters")


# ============================================
# EXERCISE 5: Multi-line Text
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Multi-line Text")
print("=" * 50)

paragraph = """Python is a great language.
Python is easy to learn.
Many people love Python."""

# Count total words
total_words = len(paragraph.split())

# Count "Python" occurrences
python_count = paragraph.count("Python")

# Count lines
lines = paragraph.split('\n')
line_count = len(lines)

print(f"Paragraph:\n{paragraph}\n")
print(f"Total words: {total_words}")  # 13
print(f"'Python' appears: {python_count} times")  # 3
print(f"Number of lines: {line_count}")  # 3

# Analyze each line
print("\nPer-line analysis:")
for i, line in enumerate(lines, 1):
    word_count = len(line.split())
    print(f"Line {i}: {word_count} words - '{line}'")


# ============================================
# BONUS: Advanced Techniques
# ============================================
print("\n" + "=" * 50)
print("BONUS: Advanced Techniques")
print("=" * 50)

# Count word frequencies (how many times each word appears)
text = "the cat and the dog and the bird"
words = text.split()

# METHOD 1: Using dictionary
word_freq = {}
for word in words:
    if word in word_freq:
        word_freq[word] += 1
    else:
        word_freq[word] = 1

print("Word frequencies (dictionary):")
for word, count in word_freq.items():
    print(f"  '{word}': {count}")

# METHOD 2: Using Counter (from collections module)
from collections import Counter
word_freq_v2 = Counter(words)
print("\nWord frequencies (Counter):")
print(word_freq_v2)

# Get most common words
print("\nMost common words:")
for word, count in word_freq_v2.most_common(3):
    print(f"  '{word}': {count} times")


# ============================================
# BONUS: Handling Punctuation
# ============================================
print("\n" + "=" * 50)
print("BONUS: Handling Punctuation")
print("=" * 50)

text_with_punct = "Hello, world! How are you? I'm fine, thanks."

# Problem: Punctuation is included in words
words_with_punct = text_with_punct.split()
print(f"With punctuation: {words_with_punct}")
# ['Hello,', 'world!', 'How', 'are', 'you?', "I'm", 'fine,', 'thanks.']

# Solution: Remove punctuation
import string
# Remove all punctuation
text_clean = text_with_punct.translate(str.maketrans('', '', string.punctuation))
words_clean = text_clean.split()
print(f"Without punctuation: {words_clean}")
# ['Hello', 'world', 'How', 'are', 'you', 'Im', 'fine', 'thanks']

print(f"\nWord count with punctuation: {len(words_with_punct)}")  # 8
print(f"Word count without punctuation: {len(words_clean)}")  # 8


# ============================================
# KEY TAKEAWAYS
# ============================================
"""
WORD COUNTING METHODS:

1. BASIC WORD COUNT ⭐ MOST COMMON
   word_count = len(sentence.split())
   - Splits by whitespace
   - Returns number of words
   - Simple and effective

2. COUNT SPECIFIC WORD
   count = text.count("word")
   - Counts substring occurrences
   - Case-sensitive
   - Can count partial matches

3. COUNT IN WORD LIST
   words = text.split()
   count = words.count("word")
   - Counts whole words only
   - More accurate than .count()

4. UNIQUE WORD COUNT
   unique = len(set(text.split()))
   - Uses set to remove duplicates
   - Counts distinct words

IMPORTANT NOTES:
- .split() splits by any whitespace (space, tab, newline)
- .split() without arguments handles multiple spaces
- Punctuation is included in words unless removed
- Case matters: "Python" ≠ "python"

COMMON PATTERNS:
- Total words: len(text.split())
- Unique words: len(set(text.split()))
- Longest word: max(text.split(), key=len)
- Shortest word: min(text.split(), key=len)
"""
