"""
============================================
PANDAS DATAFRAMES & SERIES - SOLUTION
============================================
Run pandas_basics_setup.py FIRST to try it yourself!
"""

import pandas as pd

# ============================================
# WHAT IS PANDAS?
# ============================================
print("=" * 60)
print("🐼 WHAT IS PANDAS?")
print("=" * 60)

print("""
PANDAS = Python's Excel/Spreadsheet Library

ANALOGY: Think of pandas like Excel in Python
- Series = ONE COLUMN in Excel (1D)
- DataFrame = ENTIRE SPREADSHEET (2D)

WHY USE PANDAS?
✅ Work with tabular data (like CSV, Excel files)
✅ Clean and transform data
✅ Analyze and visualize data
✅ Much faster than Excel for large datasets!
""")


# ============================================
# EXERCISE 1: Creating a Series (One Column)
# ============================================
print("\n" + "=" * 60)
print("EXERCISE 1: Creating a Series 📊")
print("=" * 60)

print("""
ANALOGY: Series = ONE COLUMN in Excel
- Like a column of prices
- Like a column of names
- Like a column of ages

Think: Shopping list (just items, no prices)
""")

# Create a Series
prices = pd.Series([10.99, 25.50, 5.75, 15.00])

print("\nSeries of prices:")
print(prices)
print(f"\nData type: {type(prices)}")
print(f"Values: {prices.values}")
print(f"Index: {prices.index}")

# How it looks:
print("""
Visual representation:
┌─────┬────────┐
│ Idx │ Price  │
├─────┼────────┤
│  0  │ 10.99  │
│  1  │ 25.50  │
│  2  │  5.75  │
│  3  │ 15.00  │
└─────┴────────┘
""")


# ============================================
# EXERCISE 2: Series with Custom Index
# ============================================
print("\n" + "=" * 60)
print("EXERCISE 2: Series with Labels 🏷️")
print("=" * 60)

print("""
ANALOGY: Like labeling rows in Excel
Instead of 0, 1, 2... use meaningful names!

Think: Price tags on items in a store
""")

# Create Series with custom index
prices = pd.Series([1.50, 0.75, 2.00], 
                   index=['Apple', 'Banana', 'Orange'])

print("\nFruit prices:")
print(prices)

# Access by label
print(f"\nPrice of Apple: ${prices['Apple']}")
print(f"Price of Banana: ${prices['Banana']}")

# Visual representation
print("""
Visual representation:
┌─────────┬────────┐
│  Fruit  │ Price  │
├─────────┼────────┤
│  Apple  │  1.50  │
│ Banana  │  0.75  │
│ Orange  │  2.00  │
└─────────┴────────┘
""")


# ============================================
# EXERCISE 3: Creating a DataFrame (Table)
# ============================================
print("\n" + "=" * 60)
print("EXERCISE 3: Creating a DataFrame 📋")
print("=" * 60)

print("""
ANALOGY: DataFrame = ENTIRE EXCEL SPREADSHEET
- Multiple columns
- Multiple rows
- Like a database table

Think: Contact list with Name, Phone, Email
""")

# Create DataFrame from dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['NYC', 'LA', 'Chicago']
}
df = pd.DataFrame(data)

print("\nPeople DataFrame:")
print(df)
print(f"\nShape (rows, columns): {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"Number of rows: {len(df)}")

# Visual representation
print("""
Visual representation:
┌─────┬─────────┬─────┬─────────┐
│ Idx │  Name   │ Age │  City   │
├─────┼─────────┼─────┼─────────┤
│  0  │  Alice  │ 25  │   NYC   │
│  1  │   Bob   │ 30  │   LA    │
│  2  │ Charlie │ 35  │ Chicago │
└─────┴─────────┴─────┴─────────┘
""")


# ============================================
# EXERCISE 4: Accessing DataFrame Data
# ============================================
print("\n" + "=" * 60)
print("EXERCISE 4: Accessing Data 🔍")
print("=" * 60)

print("""
ANALOGY: Like selecting cells/columns in Excel
- Click column header → Get entire column
- Click row number → Get entire row
- Click cell → Get single value
""")

# Get one column (returns a Series!)
print("\nGet 'Name' column (returns Series):")
names = df['Name']
print(names)
print(f"Type: {type(names)}")

# Get multiple columns (returns DataFrame!)
print("\nGet 'Name' and 'Age' columns (returns DataFrame):")
subset = df[['Name', 'Age']]
print(subset)
print(f"Type: {type(subset)}")

# Get one row
print("\nGet first row (index 0):")
first_row = df.iloc[0]
print(first_row)
print(f"Type: {type(first_row)}")  # Also a Series!

# Get specific value
print(f"\nGet specific value (row 0, 'Name'): {df.loc[0, 'Name']}")


# ============================================
# EXERCISE 5: When to Use Series vs DataFrame
# ============================================
print("\n" + "=" * 60)
print("EXERCISE 5: Series vs DataFrame 🤔")
print("=" * 60)

print("""
WHEN TO USE SERIES:
✅ Single column of data
✅ One measurement (temperatures, prices, ages)
✅ Simple list with labels

WHEN TO USE DATAFRAME:
✅ Multiple columns of related data
✅ Table/spreadsheet structure
✅ Complex datasets (CSV, Excel files)
""")

# Example: Shopping list (Series)
print("\nShopping List (Series):")
shopping_list = pd.Series(['Milk', 'Bread', 'Eggs', 'Butter'])
print(shopping_list)

print("""
ANALOGY: Just a list of items
┌─────┬────────┐
│  0  │  Milk  │
│  1  │ Bread  │
│  2  │  Eggs  │
│  3  │ Butter │
└─────┴────────┘
""")

# Example: Grocery receipt (DataFrame)
print("\nGrocery Receipt (DataFrame):")
receipt = pd.DataFrame({
    'Item': ['Milk', 'Bread', 'Eggs', 'Butter'],
    'Price': [3.99, 2.50, 4.25, 5.00],
    'Quantity': [1, 2, 1, 1],
    'Total': [3.99, 5.00, 4.25, 5.00]
})
print(receipt)

print("""
ANALOGY: Complete receipt with details
┌─────┬────────┬───────┬──────────┬───────┐
│ Idx │  Item  │ Price │ Quantity │ Total │
├─────┼────────┼───────┼──────────┼───────┤
│  0  │  Milk  │ 3.99  │    1     │ 3.99  │
│  1  │ Bread  │ 2.50  │    2     │ 5.00  │
│  2  │  Eggs  │ 4.25  │    1     │ 4.25  │
│  3  │ Butter │ 5.00  │    1     │ 5.00  │
└─────┴────────┴───────┴──────────┴───────┘
""")


# ============================================
# BONUS: Creating DataFrames Different Ways
# ============================================
print("\n" + "=" * 60)
print("BONUS: Different Ways to Create DataFrames")
print("=" * 60)

# Method 1: From dictionary (most common)
print("\nMethod 1: From Dictionary")
df1 = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})
print(df1)

# Method 2: From list of lists
print("\nMethod 2: From List of Lists")
df2 = pd.DataFrame(
    [[1, 4], [2, 5], [3, 6]],
    columns=['A', 'B']
)
print(df2)

# Method 3: From list of dictionaries
print("\nMethod 3: From List of Dictionaries")
df3 = pd.DataFrame([
    {'A': 1, 'B': 4},
    {'A': 2, 'B': 5},
    {'A': 3, 'B': 6}
])
print(df3)

print("\nAll three methods create the same DataFrame!")


# ============================================
# BONUS: Real-World Examples
# ============================================
print("\n" + "=" * 60)
print("BONUS: Real-World Examples")
print("=" * 60)

# Example 1: Student grades (DataFrame)
print("\nExample 1: Student Grades")
grades = pd.DataFrame({
    'Student': ['Alice', 'Bob', 'Charlie'],
    'Math': [95, 87, 92],
    'English': [88, 91, 85],
    'Science': [92, 89, 94]
})
print(grades)

# Example 2: Stock prices over time (Series)
print("\nExample 2: Stock Prices (Series)")
stock_prices = pd.Series(
    [150.25, 152.10, 149.80, 153.50, 155.00],
    index=['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
)
print(stock_prices)

# Example 3: Sales data (DataFrame)
print("\nExample 3: Sales Data")
sales = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
    'Product': ['Laptop', 'Mouse', 'Keyboard'],
    'Quantity': [5, 20, 15],
    'Revenue': [5000, 400, 750]
})
print(sales)


# ============================================
# KEY TAKEAWAYS
# ============================================
print("\n" + "=" * 60)
print("KEY TAKEAWAYS")
print("=" * 60)

print("""
🎯 SERIES vs DATAFRAME:

SERIES (1D):
📊 One column of data
📝 Like a shopping list
🏷️ Has index (row labels)
💡 Use for: Single measurement, one variable

DATAFRAME (2D):
📋 Multiple columns (table/spreadsheet)
🧾 Like a grocery receipt
🏷️ Has index (rows) AND columns
💡 Use for: Related data, CSV files, databases

REMEMBER:
• Series = ONE column in Excel
• DataFrame = ENTIRE Excel spreadsheet
• DataFrame column = Series
• DataFrame row = Series

COMMON OPERATIONS:
• Create Series: pd.Series([1, 2, 3])
• Create DataFrame: pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
• Get column: df['Name']
• Get row: df.iloc[0]
• Get value: df.loc[0, 'Name']
""")
