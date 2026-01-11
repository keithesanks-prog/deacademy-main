"""
============================================
PANDAS DATAFRAMES & SERIES - SETUP
============================================
Learn pandas - Python's spreadsheet library!

🎯 ANALOGY: Think of pandas like Excel in Python
- Series = One column in Excel
- DataFrame = Entire Excel spreadsheet

Your Tasks:
1. Understand what Series and DataFrames are
2. Create Series from lists
3. Create DataFrames from dictionaries
4. Know when to use each

Key Concepts:
- Series = 1D labeled array (one column)
- DataFrame = 2D labeled data (table/spreadsheet)
- Index = Row labels
- Columns = Column labels
"""

import pandas as pd

# ============================================
# EXERCISE 1: Creating a Series (One Column)
# ============================================
print("=" * 50)
print("EXERCISE 1: Creating a Series")
print("=" * 50)

# ANALOGY: Series = ONE COLUMN in Excel
# Like a list of prices, or names, or ages

# TODO: Create a Series of prices
# prices = pd.Series([10.99, 25.50, 5.75, 15.00])

# TODO: Print the Series
# TODO: Print the data type


# ============================================
# EXERCISE 2: Series with Custom Index
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 2: Series with Labels")
print("=" * 50)

# ANALOGY: Like labeling rows in Excel
# Instead of 0, 1, 2... use "Apple", "Banana", "Orange"

# TODO: Create a Series with fruit names as index
# prices = pd.Series([1.50, 0.75, 2.00], 
#                    index=['Apple', 'Banana', 'Orange'])

# TODO: Access price of 'Apple'
# TODO: Print the Series


# ============================================
# EXERCISE 3: Creating a DataFrame (Table)
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 3: Creating a DataFrame")
print("=" * 50)

# ANALOGY: DataFrame = ENTIRE EXCEL SPREADSHEET
# Multiple columns, multiple rows

# TODO: Create a DataFrame from a dictionary
# data = {
#     'Name': ['Alice', 'Bob', 'Charlie'],
#     'Age': [25, 30, 35],
#     'City': ['NYC', 'LA', 'Chicago']
# }
# df = pd.DataFrame(data)

# TODO: Print the DataFrame
# TODO: Print the shape (rows, columns)


# ============================================
# EXERCISE 4: Accessing DataFrame Data
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 4: Accessing Data")
print("=" * 50)

# TODO: Get one column (returns a Series)
# names = df['Name']

# TODO: Get multiple columns (returns DataFrame)
# subset = df[['Name', 'Age']]

# TODO: Get one row by index
# first_row = df.iloc[0]


# ============================================
# EXERCISE 5: When to Use Series vs DataFrame
# ============================================
print("\n" + "=" * 50)
print("EXERCISE 5: Series vs DataFrame")
print("=" * 50)

# ANALOGY TIME!
# Series = Shopping list (one column of items)
# DataFrame = Grocery receipt (items, prices, quantities)

# TODO: Create a Series for a shopping list
# shopping_list = pd.Series(['Milk', 'Bread', 'Eggs'])

# TODO: Create a DataFrame for a receipt
# receipt = pd.DataFrame({
#     'Item': ['Milk', 'Bread', 'Eggs'],
#     'Price': [3.99, 2.50, 4.25],
#     'Quantity': [1, 2, 1]
# })


# ============================================
# EXPECTED OUTPUT (for reference)
# ============================================
"""
==================================================
EXERCISE 1: Creating a Series
==================================================
0    10.99
1    25.50
2     5.75
3    15.00
dtype: float64

==================================================
EXERCISE 2: Series with Labels
==================================================
Apple     1.50
Banana    0.75
Orange    2.00
dtype: float64

Price of Apple: 1.50

... (and so on)
"""
