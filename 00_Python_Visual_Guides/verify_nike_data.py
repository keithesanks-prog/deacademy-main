import pandas as pd

try:
    print("Loading dim_category_nike_python.csv...")
    dim_cat = pd.read_csv('dim_category_nike_python.csv')
    print(dim_cat.head(2))
    print("\n----------------\n")
    
    print("Loading dim_product_nike_python.csv...")
    dim_prod = pd.read_csv('dim_product_nike_python.csv')
    print(dim_prod.head(2))
    print("\n----------------\n")
    
    print("SUCCESS: Data loaded correctly.")
except Exception as e:
    print(f"FAILED: {e}")
