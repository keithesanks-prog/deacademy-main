import pandas as pd
data = [
    {'ID': 1, 'Name': 'John', 'Age': 30},
    {'ID': 2, 'Name': 'Jane', 'Age': 25},
    {'ID': 3, 'Name': 'Bob', 'Age': 35}
]
df = pd.DataFrame(data)
df['City'] = ['New York', 'Los Angeles', 'Chicago']
df.loc[3] = [4, 'Alice', 28, 'San Francisco']
df.loc[4] = [5, 'Bob', 32, 'San Francisco']
print(df)

df.drop('City', axis=1, inplace=True)
print(df)