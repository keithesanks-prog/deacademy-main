import pandas as pd

# Load the data we created
df_cat = pd.read_csv('dim_category_nike_python.csv')
df_prod = pd.read_csv('dim_product_nike_python.csv')
df = pd.merge(df_prod, df_cat, on='category_id', how='left')
df['order_year'] = pd.to_datetime(df['order_date']).dt.year

print("--- DEBUGGING USER CODE ---")

# ERROR 1: .ascending() is not a method on groupby
try:
    print("Attempting: df.groupby(...).ascending(...)")
    # This fails because 'groupby' returns a GroupBy object, which has no 'ascending' method.
    # You usually need to Aggregate first (mean/sum) THEN Sort.
    summary = df.groupby(["order_year", "gender", "category_name"])["product_reviews"].ascending(True,True,False)
except AttributeError as e:
    print(f"FAIL 1: {e}")

# Let's create the valid summary first so we can test Error 2
summary = df.groupby(["order_year", "gender", "category_name"])["product_reviews"].mean().reset_index()

# ERROR 2: Syntax placement of ascending
try:
    print("\nAttempting: summary.sort_values(...),ascending(...)")
    # This fails because 'ascending' is an ARGUMENT inside the parentheses, not a thing outside.
    # User Code: summary.sort_values([...]),ascending(...)
    # Python sees this as variables separated by comma (creating a tuple), and 'ascending' isn't defined.
    # We simulate the exact syntax error structure:
    # summary = summary.sort_values(['order_year']), ascending=True 
    # (SyntaxError or NameError depending on context)
    pass 
except Exception as e:
    print(f"FAIL 2: {e}")

print("\n--- THE CORRECT SYNTAX ---")
# 1. Aggregate
summary = df.groupby(["order_year", "gender", "category_name"])["product_reviews"].mean().reset_index()

# 2. Sort
# 'ascending' goes INSIDE the parentheses.
# You pass a LIST of True/False to match the LIST of columns.
summary_sorted = summary.sort_values(
    by=['order_year', 'gender', 'product_reviews'], 
    ascending=[True, True, False]
)

print(summary_sorted.head())
print("\nSUCCESS: Sorted correctly.")
