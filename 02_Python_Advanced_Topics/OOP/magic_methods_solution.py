"""
============================================
MAGIC METHODS (DUNDER METHODS) - SOLUTION
============================================
Run magic_methods_setup.py FIRST to try it yourself!

🎬 THE "DUNDIES" - Python's Special Awards!
"""

# ============================================
# WHAT ARE DUNDER METHODS?
# ============================================
print("=" * 60)
print("🎭 WHAT ARE DUNDER METHODS?")
print("=" * 60)

print("""
DUNDER = "Double Underscore"
- Written as: __method__()
- Also called: "Magic Methods" or "Special Methods"
- Fun nickname: "Dundies" (like The Office awards!)

WHY "MAGIC"?
Python calls them AUTOMATICALLY when you do certain things:
- print(obj) → Python calls obj.__str__()
- len(obj) → Python calls obj.__len__()
- obj1 + obj2 → Python calls obj1.__add__(obj2)

ANALOGY RECAP:
🎂 __init__() = Birth Certificate (records who you are)
👋 __str__() = Party Introduction (friendly greeting)
🪪 __repr__() = Driver's License (official ID)
📏 __len__() = Measuring Tape (how big are you?)
➕ __add__() = Teaching Addition (what does + mean?)
⚖️ __eq__() = Twin Checker (are we identical?)
""")


# ============================================
# EXERCISE 1: __init__() - The Birth Certificate
# ============================================
print("\n" + "=" * 60)
print("EXERCISE 1: __init__() - The Birth Certificate 🎂")
print("=" * 60)

class Person:
    """A person with a name and age"""
    
    def __init__(self, name, age):
        """
        The constructor - runs AUTOMATICALLY when creating a Person
        
        ANALOGY: Like filling out a birth certificate
        - Record the name
        - Record the age (or birthday)
        
        This is called AUTOMATICALLY:
        person = Person("Alice", 25)  ← __init__ runs here!
        """
        print(f"  🎂 Birth certificate created for {name}!")
        self.name = name  # Write name on certificate
        self.age = age    # Write age on certificate

# Create a person (watch __init__ run automatically!)
print("\nCreating a person:")
person1 = Person("Alice", 25)
print(f"Person created: {person1.name}, age {person1.age}")


# ============================================
# EXERCISE 2: __str__() - The Friendly Introduction
# ============================================
print("\n" + "=" * 60)
print("EXERCISE 2: __str__() - Party Introduction 👋")
print("=" * 60)

class Person:
    """Person with friendly introduction"""
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        """
        Called when you print() the object
        
        ANALOGY: How you introduce yourself at a party
        - Friendly and casual
        - Easy to understand
        - For humans to read
        
        Automatically called by:
        - print(person)
        - str(person)
        - f"{person}"
        """
        return f"Hi, I'm {self.name}, {self.age} years old"

person1 = Person("Alice", 25)

print("\nUsing print() - calls __str__() automatically:")
print(person1)  # Python calls person1.__str__()

print("\nUsing str() - also calls __str__():")
print(str(person1))

print("\nUsing f-string - also calls __str__():")
print(f"Person info: {person1}")


# ============================================
# EXERCISE 3: __repr__() - The Official ID
# ============================================
print("\n" + "=" * 60)
print("EXERCISE 3: __repr__() - Driver's License 🪪")
print("=" * 60)

class Person:
    """Person with both friendly and official representations"""
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        """Friendly introduction (for humans)"""
        return f"Hi, I'm {self.name}, {self.age} years old"
    
    def __repr__(self):
        """
        Official representation (for developers/debugging)
        
        ANALOGY: Like your driver's license
        - __str__ = "Hi, I'm Alice!" (casual)
        - __repr__ = "Person(name='Alice', age=25)" (official)
        
        GOAL: Should be unambiguous and ideally recreate the object
        Person(name='Alice', age=25) ← You could copy/paste this!
        
        Automatically called by:
        - repr(person)
        - In Python console when you type: person
        - In lists: [person1, person2]
        """
        return f"Person(name='{self.name}', age={self.age})"

person1 = Person("Alice", 25)

print("\n__str__() - Friendly (for print):")
print(str(person1))

print("\n__repr__() - Official (for debugging):")
print(repr(person1))

print("\nIn a list (uses __repr__):")
people = [Person("Alice", 25), Person("Bob", 30)]
print(people)


# ============================================
# EXERCISE 4: __len__() - Measuring Size
# ============================================
print("\n" + "=" * 60)
print("EXERCISE 4: __len__() - Measuring Tape 📏")
print("=" * 60)

class Playlist:
    """A music playlist that knows its length"""
    
    def __init__(self, name):
        self.name = name
        self.songs = []
    
    def add_song(self, song):
        """Add a song to the playlist"""
        self.songs.append(song)
        print(f"  ♪ Added: {song}")
    
    def __len__(self):
        """
        Return the "length" of this object
        
        ANALOGY: Like asking "How big are you?"
        - For a string: How many letters?
        - For a list: How many items?
        - For a playlist: How many songs?
        
        YOU decide what "length" means for your class!
        
        Automatically called by:
        - len(playlist)
        """
        return len(self.songs)
    
    def __str__(self):
        return f"Playlist '{self.name}' with {len(self)} songs"

# Create and use playlist
print("\nCreating playlist:")
my_playlist = Playlist("Favorites")
my_playlist.add_song("Bohemian Rhapsody")
my_playlist.add_song("Stairway to Heaven")
my_playlist.add_song("Hotel California")

print(f"\nPlaylist info: {my_playlist}")
print(f"Number of songs: {len(my_playlist)}")  # Calls __len__()!


# ============================================
# EXERCISE 5: __add__() - Addition Operator
# ============================================
print("\n" + "=" * 60)
print("EXERCISE 5: __add__() - Teaching Addition ➕")
print("=" * 60)

class Money:
    """Money that knows how to add itself"""
    
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency
    
    def __add__(self, other):
        """
        Define what + means for Money objects
        
        ANALOGY: Teaching your class to add
        - Numbers know: 5 + 3 = 8
        - Strings know: "Hi" + "!" = "Hi!"
        - Money should know: $10 + $5 = $15
        
        Automatically called by:
        - money1 + money2
        """
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies!")
        
        new_amount = self.amount + other.amount
        return Money(new_amount, self.currency)
    
    def __str__(self):
        return f"${self.amount} {self.currency}"

# Create and add money
print("\nCreating money objects:")
wallet1 = Money(10)
wallet2 = Money(5)

print(f"Wallet 1: {wallet1}")
print(f"Wallet 2: {wallet2}")

print("\nAdding money (calls __add__):")
total = wallet1 + wallet2  # Python calls wallet1.__add__(wallet2)
print(f"Total: {total}")


# ============================================
# EXERCISE 6: __eq__() - Equality Check
# ============================================
print("\n" + "=" * 60)
print("EXERCISE 6: __eq__() - Twin Checker ⚖️")
print("=" * 60)

class Person:
    """Person with equality checking"""
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __eq__(self, other):
        """
        Define what == means for Person objects
        
        ANALOGY: Checking if twins are identical
        - Same name? ✓
        - Same age? ✓
        - Then they're equal!
        
        YOU decide what makes two objects "equal"
        
        Automatically called by:
        - person1 == person2
        - person1 != person2 (uses opposite of __eq__)
        """
        return self.name == other.name and self.age == other.age
    
    def __str__(self):
        return f"{self.name} ({self.age})"

# Create people
print("\nCreating people:")
person1 = Person("Alice", 25)
person2 = Person("Alice", 25)
person3 = Person("Bob", 25)

print(f"Person 1: {person1}")
print(f"Person 2: {person2}")
print(f"Person 3: {person3}")

print("\nEquality checks (calls __eq__):")
print(f"person1 == person2: {person1 == person2}")  # True (same name and age)
print(f"person1 == person3: {person1 == person3}")  # False (different names)


# ============================================
# BONUS: All Common Dunder Methods
# ============================================
print("\n" + "=" * 60)
print("BONUS: Complete Dunder Methods Reference")
print("=" * 60)

print("""
🎬 THE COMPLETE "DUNDIES" COLLECTION:

📋 OBJECT CREATION & REPRESENTATION:
__init__(self, ...)     🎂 Birth Certificate - Initialize object
__str__(self)           👋 Party Intro - Friendly string (for print)
__repr__(self)          🪪 Official ID - Technical string (for debugging)
__del__(self)           ⚰️ Obituary - Called when object is deleted

📏 SIZE & CONTAINER:
__len__(self)           📏 Measuring Tape - Return length
__getitem__(self, key)  🗂️ Filing Cabinet - obj[key]
__setitem__(self, key)  ✍️ Write in Cabinet - obj[key] = value
__contains__(self, item) 🔍 Detective - item in obj

➕ ARITHMETIC OPERATORS:
__add__(self, other)    ➕ Addition - obj1 + obj2
__sub__(self, other)    ➖ Subtraction - obj1 - obj2
__mul__(self, other)    ✖️ Multiplication - obj1 * obj2
__truediv__(self, other) ➗ Division - obj1 / obj2

⚖️ COMPARISON OPERATORS:
__eq__(self, other)     ⚖️ Equal - obj1 == obj2
__ne__(self, other)     ≠ Not Equal - obj1 != obj2
__lt__(self, other)     < Less Than - obj1 < obj2
__gt__(self, other)     > Greater Than - obj1 > obj2
__le__(self, other)     ≤ Less or Equal - obj1 <= obj2
__ge__(self, other)     ≥ Greater or Equal - obj1 >= obj2

🎯 CALLABLE & CONTEXT:
__call__(self, ...)     📞 Phone Call - obj()
__enter__(self)         🚪 Enter Room - with obj:
__exit__(self, ...)     🚪 Exit Room - End of with block
""")


# ============================================
# KEY TAKEAWAYS
# ============================================
print("\n" + "=" * 60)
print("KEY TAKEAWAYS")
print("=" * 60)

print("""
🎯 WHAT ARE DUNDER METHODS?
- "Dunder" = Double Underscore
- Also called "Magic Methods" or "Dundies"
- Python calls them AUTOMATICALLY
- They give your classes superpowers!

🎭 THE BIG 6 (Most Important):
1. __init__()  - Constructor (birth certificate)
2. __str__()   - Friendly string (party intro)
3. __repr__()  - Official string (driver's license)
4. __len__()   - Length (measuring tape)
5. __add__()   - Addition (teaching +)
6. __eq__()    - Equality (twin checker)

💡 REMEMBER:
- YOU define what these methods do
- Python calls them automatically
- They make your objects behave like built-in types
- Use analogies to remember them!

🎬 THINK OF IT LIKE:
Your class is an actor, and dunder methods are the scripts
that tell it how to act in different situations!
""")
