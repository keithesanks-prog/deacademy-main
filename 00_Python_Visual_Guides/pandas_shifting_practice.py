import pandas as pd

# ==========================================
# PRACTICE EXERCISE: Shifting and Lagging
# ==========================================

# 1. Create the DataFrame
data = {
    'Date': pd.date_range(start='2025-02-01', periods=12, freq='D'),
    'Sales': [120, 150, 180, 210, 250, 300, 280, 270, 260, 310, 320, 330]
}

df = pd.DataFrame(data)
df.set_index('Date', inplace=True)

print("--- ORIGINAL DATAFRAME ---")
print(df.head())
print("\n")

# 2. Shift the Sales column by 1 period (lagging)
print("--- 1. PREVIOUS SALES (Lag=1) ---")
df['Prev_Sales'] = df['Sales'].shift(1)
print(df[['Sales', 'Prev_Sales']].head())
print("\n")

# 3. Shift the Sales column by -1 period (leading)
print("--- 2. NEXT SALES (Lead=-1) ---")
df['Next_Sales'] = df['Sales'].shift(-1)
print(df[['Sales', 'Next_Sales']].head())
print("\n")

# 4. Calculate the difference from the previous row
print("--- 3. SALES DIFFERENCE ---")
df['Diff'] = df['Sales'] - df['Prev_Sales']
print(df[['Sales', 'Prev_Sales', 'Diff']].head())
print("\n")

# 5. Calculate the percentage change from the previous row
print("--- 4. GROWTH PERCENTAGE ---")
df['Growth_%'] = df['Sales'].pct_change() * 100

# Final Output
print("--- FINAL DATAFRAME ---")
print(df)
