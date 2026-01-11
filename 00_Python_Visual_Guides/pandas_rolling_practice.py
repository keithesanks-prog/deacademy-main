import pandas as pd

# ==========================================
# PRACTICE EXERCISE: Rolling and Moving Averages
# ==========================================

# 1. Create the DataFrame
data = {
    'Date': pd.date_range(start='2025-02-01', periods=12, freq='D'),
    'Sales': [120, 150, 180, 210, 250, 300, 280, 270, 260, 310, 320, 330]
}

df = pd.DataFrame(data)
print("--- ORIGINAL DATAFRAME ---")
print(df.head())
print("\n")

# 2. Set 'Date' column as the index
print("--- 1. SET INDEX ---")
df.set_index('Date', inplace=True)
print(df.head())
print("\n")

# 3. Calculate a 3-day rolling average for the Sales column
print("--- 2. ROLLING AVERAGE (Window=3) ---")
df['Rolling_Avg'] = df['Sales'].rolling(window=3).mean()
print(df.head())
print("\n")

# 4. Calculate an Exponential Moving Average (EMA) with a span of 3
print("--- 3. EXPONENTIAL MOVING AVERAGE (Span=3) ---")
df['EMA'] = df['Sales'].ewm(span=3, adjust=False).mean()

# 5. Print the Final Dataframe
print("--- FINAL DATAFRAME ---")
print(df)
