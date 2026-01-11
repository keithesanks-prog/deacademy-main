import pandas as pd

# ==========================================
# PRACTICE EXERCISE: Date and Time Handling
# ==========================================

# 1. Create the DataFrame
data = {
    'DateTime': pd.to_datetime([
        '2025-01-01', '2025-01-02', '2025-01-03', 
        '2025-01-04', '2025-01-05', '2025-01-06',
        '2025-01-07', '2025-01-08', '2025-01-09', 
        '2025-01-10'
    ]),
    'City': [
        'New York', 'Chicago', 'Los Angeles', 
        'New York', 'Chicago', 'Los Angeles', 
        'New York', 'Chicago', 'Los Angeles', 
        'New York'
    ],
    'Sales': [
        1200, 800, 1500, 
        600, 750, 1700, 
        950, 1800, 500, 
        1300
    ]
}

df = pd.DataFrame(data)
print("--- ORIGINAL DATAFRAME ---")
print(df)
print("\n")

# 2. Extract Year, Month, and Day
print("--- 1. EXTRACT COMPONENTS ---")
df['Year'] = df['DateTime'].dt.year
df['Month'] = df['DateTime'].dt.month
df['Day'] = df['DateTime'].dt.day
print(df[['DateTime', 'Year', 'Month', 'Day']])
print("\n")

# 3. Filter data for sales greater than 1000
print("--- 2. FILTER SALES > 1000 ---")
high_sales = df[df['Sales'] > 1000]
print(high_sales)
print("\n")

# 4. Add a new column Next Week that shows the date one week later
print("--- 3. ADD NEXT WEEK ---")
df['Next Week'] = df['DateTime'] + pd.Timedelta(days=7)
print(df[['DateTime', 'Next Week']])
