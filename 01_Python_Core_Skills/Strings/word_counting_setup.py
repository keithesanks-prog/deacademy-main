"""
============================================
WORD COUNTING - SETUP SCRIPT
============================================
Learn how to count words in strings using Python

Your Tasks:
1. Count words in a sentence
2. Handle different types of text
3. Count specific words
4. Analyze text statistics

Key Methods to Learn:
- str.split()           # Split string into list of words
- len(list)             # Count items in list
- str.count(word)       # Count occurrences of specific word
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

# TODO: Split the sentence into words using .split()
# TODO: Count the words using len()
# TODO: Print the word count
# Expected: 5 words


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

# TODO: Loop through texts
# TODO: For each text, count and print the word count


# ============================================
# EXERCISE 3: Count Specific Words
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Count Specific Words")
print("=" * 50)

text = "Python is great. Python is easy. Python is fun."

# TODO: Count how many times "Python" appears
# Hint: Use .count("Python")

# TODO: Count how many times "is" appears


# ============================================
# EXERCISE 4: Advanced Word Analysis
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Advanced Word Analysis")
print("=" * 50)

sentence = "The quick brown fox jumps over the lazy dog"

# TODO: Count total words
# TODO: Count unique words (hint: use set())
# TODO: Find the longest word
# TODO: Find the shortest word


# ============================================
# EXERCISE 5: Multi-line Text
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Multi-line Text")
print("=" * 50)

paragraph = """Python is a great language.
Python is easy to learn.
Many people love Python."""

# TODO: Count total words in the paragraph
# TODO: Count how many times "Python" appears
# TODO: Count number of lines


# ============================================
# EXPECTED OUTPUT (for reference)
# ============================================
"""
==================================================
EXERCISE 1: Basic Word Counting
==================================================
Sentence: Python is fun to learn
Word Count: 5

==================================================
EXERCISE 2: Count Words in Different Texts
==================================================
Text: Hello World
Word Count: 2

Text: The quick brown fox
Word Count: 4

... (and so on)
"""
