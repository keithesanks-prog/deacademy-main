"""
============================================
MAGIC METHODS (DUNDER METHODS) - SETUP
============================================
Learn Python's special "magic" methods that give your classes superpowers!

🎬 THE "DUNDIES" - Like The Office Awards, but for Python!

What's a "Dunder"?
- Dunder = "Double Underscore" 
- Written as: __method__()
- Think of them as "Dundies" (like The Office awards!)
- They're MAGIC because Python calls them automatically

ANALOGY: Think of dunder methods like AUTOMATIC RESPONSES
- When someone says "Hi!" → You automatically say "Hi!" back
- When Python sees print(obj) → It automatically calls obj.__str__()
- When Python sees len(obj) → It automatically calls obj.__len__()

Your Tasks:
1. Learn what dunder methods are
2. Implement __init__, __str__, __repr__
3. Implement __len__, __add__, __eq__
4. See how Python uses them automatically
"""

# ============================================
# EXERCISE 1: The Constructor - __init__()
# ============================================
print("=" * 50)
print("EXERCISE 1: __init__() - The Birth Certificate")
print("=" * 50)

# ANALOGY: __init__ is like a BIRTH CERTIFICATE
# When a baby is born, you record: name, birthday, weight
# When an object is created, __init__ records its attributes!

# TODO: Create a Person class with __init__
# TODO: Store name and age as attributes
# TODO: Create a person instance

"""
class Person:
    def __init__(self, name, age):
        # This runs AUTOMATICALLY when you create a Person!
        self.name = name  # Like writing name on birth certificate
        self.age = age    # Like writing birthday on birth certificate

# Creating a person = "giving birth" to an object
person1 = Person("Alice", 25)  # __init__ runs automatically!
"""


# ============================================
# EXERCISE 2: __str__() - The Friendly Introduction
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: __str__() - How You Introduce Yourself")
print("=" * 50)

# ANALOGY: __str__ is like HOW YOU INTRODUCE YOURSELF
# At a party: "Hi, I'm Alice, I'm 25 years old"
# When someone asks about you, you give a friendly description

# TODO: Add __str__ method to Person class
# TODO: Return a friendly string like "Hi, I'm Alice, 25 years old"
# TODO: Test with print(person1)

"""
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        # This is called when you do: print(person)
        # Like introducing yourself at a party!
        return f"Hi, I'm {self.name}, {self.age} years old"

person1 = Person("Alice", 25)
print(person1)  # Automatically calls __str__()!
"""


# ============================================
# EXERCISE 3: __repr__() - The Technical ID
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: __repr__() - Your Official ID Card")
print("=" * 50)

# ANALOGY: __repr__ is like your DRIVER'S LICENSE
# __str__ = "Hi, I'm Alice!" (friendly)
# __repr__ = "Person(name='Alice', age=25)" (official/technical)

# TODO: Add __repr__ method
# TODO: Return technical representation
# TODO: Compare str() vs repr()


# ============================================
# EXERCISE 4: __len__() - Measuring Size
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: __len__() - What's Your Size?")
print("=" * 50)

# ANALOGY: __len__ is like asking "HOW BIG ARE YOU?"
# For a string: len("hello") → 5 letters
# For a list: len([1,2,3]) → 3 items
# For your class: You decide what "length" means!

# TODO: Create a Playlist class
# TODO: Add __len__ to return number of songs
# TODO: Test with len(playlist)

"""
class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []
    
    def add_song(self, song):
        self.songs.append(song)
    
    def __len__(self):
        # When someone asks: "How many songs?"
        # Python calls this automatically!
        return len(self.songs)

my_playlist = Playlist("Favorites")
my_playlist.add_song("Song 1")
my_playlist.add_song("Song 2")
print(len(my_playlist))  # Calls __len__() automatically!
"""


# ============================================
# EXERCISE 5: __add__() - Addition Operator
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: __add__() - Making + Work")
print("=" * 50)

# ANALOGY: __add__ is like TEACHING YOUR OBJECT TO ADD
# Numbers know: 5 + 3 = 8
# Strings know: "Hello" + "World" = "HelloWorld"
# Your class? You teach it what + means!

# TODO: Create a Money class
# TODO: Implement __add__ to add amounts
# TODO: Test: money1 + money2


# ============================================
# EXERCISE 6: __eq__() - Equality Check
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 6: __eq__() - Are We Equal?")
print("=" * 50)

# ANALOGY: __eq__ is like CHECKING IF TWINS ARE IDENTICAL
# Same name? Same age? Then they're equal!
# You decide what makes two objects "equal"

# TODO: Add __eq__ to Person class
# TODO: Two people are equal if same name and age
# TODO: Test: person1 == person2


# ============================================
# EXPECTED OUTPUT (for reference)
# ============================================
"""
==================================================
EXERCISE 1: __init__() - The Birth Certificate
==================================================
Created person: Alice, age 25

==================================================
EXERCISE 2: __str__() - How You Introduce Yourself
==================================================
Hi, I'm Alice, 25 years old

==================================================
EXERCISE 3: __repr__() - Your Official ID Card
==================================================
str(): Hi, I'm Alice, 25 years old
repr(): Person(name='Alice', age=25)

... (and so on)
"""
