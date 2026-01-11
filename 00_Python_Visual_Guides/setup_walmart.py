import pandas as pd
import numpy as np
import sqlalchemy
import random
from datetime import datetime, timedelta
import sys

# --- CONFIGURATION ---
NUM_PRODUCTS = 50
NUM_STORES = 10
NUM_CUSTOMERS = 200
NUM_TRANSACTIONS = 2000

print("⏳ Initializing Walmart Star Schema Generator...")

# CREDENTIALS
username = 'python_user'
password = 'password'
host = '127.0.0.1'
port = '3306'
db_name = "walmart_db"

try:
    # 1. Create DB if not exists
    print("🔌 Connecting to MySQL Root...")
    root_conn = f"mysql+pymysql://{username}:{password}@{host}:{port}"
    engine = sqlalchemy.create_engine(root_conn)
    with engine.connect() as conn:
         conn.execute(sqlalchemy.text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
    print(f"✅ Database '{db_name}' ready.")

    # 2. Connect to the DB
    db_connection_str = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"
    db_engine = sqlalchemy.create_engine(db_connection_str)

    # ==========================================
    # 1. DIM_PRODUCTS
    # ==========================================
    categories = ['Electronics', 'Home & Garden', 'Clothing', 'Grocery', 'Toys']
    products = []
    for i in range(1, NUM_PRODUCTS + 1):
        cat = random.choice(categories)
        price = round(random.uniform(5.0, 500.0), 2)
        cost = round(price * random.uniform(0.4, 0.8), 2)
        products.append([i, f"Product {i}", cat, price, cost])

    df_products = pd.DataFrame(products, columns=['product_id', 'product_name', 'category', 'price', 'cost'])
    df_products.to_sql('dim_products', db_engine, if_exists='replace', index=False)
    print("✅ Table 'dim_products' created.")

    # ==========================================
    # 2. DIM_STORES
    # ==========================================
    cities = [('Austin', 'TX', 'South'), ('New York', 'NY', 'East'), 
              ('San Francisco', 'CA', 'West'), ('Chicago', 'IL', 'Midwest'),
              ('Miami', 'FL', 'South')]
    stores = []
    for i in range(1, NUM_STORES + 1):
        city, state, region = random.choice(cities)
        stores.append([i, f"Store {i} - {city}", city, state, region])

    df_stores = pd.DataFrame(stores, columns=['store_id', 'store_name', 'city', 'state', 'region'])
    df_stores.to_sql('dim_stores', db_engine, if_exists='replace', index=False)
    print("✅ Table 'dim_stores' created.")

    # ==========================================
    # 3. DIM_CUSTOMERS
    # ==========================================
    segments = ['Consumer', 'Corporate', 'Home Office']
    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        customers.append([i, f"Customer {i}", random.choice(segments)])

    df_customers = pd.DataFrame(customers, columns=['customer_id', 'customer_name', 'segment'])
    df_customers.to_sql('dim_customers', db_engine, if_exists='replace', index=False)
    print("✅ Table 'dim_customers' created.")

    # ==========================================
    # 4. DIM_DATE
    # ==========================================
    start_date = datetime(2023, 1, 1)
    date_list = [start_date + timedelta(days=x) for x in range(365)]
    dates = []
    for dt in date_list:
        date_key = int(dt.strftime('%Y%m%d'))
        quarter = (dt.month - 1) // 3 + 1
        dates.append([date_key, dt, dt.year, dt.month, f"Q{quarter}", dt.strftime('%A')])

    df_date = pd.DataFrame(dates, columns=['date_key', 'date', 'year', 'month', 'quarter', 'day_name'])
    df_date.to_sql('dim_date', db_engine, if_exists='replace', index=False)
    print("✅ Table 'dim_date' created.")

    # ==========================================
    # 5. FACT_SALES (The Big One)
    # ==========================================
    sales_data = []
    product_ids = df_products['product_id'].tolist()
    store_ids = df_stores['store_id'].tolist()
    customer_ids = df_customers['customer_id'].tolist()
    date_keys = df_date['date_key'].tolist()

    for i in range(1, NUM_TRANSACTIONS + 1):
        pid = random.choice(product_ids)
        sid = random.choice(store_ids)
        cid = random.choice(customer_ids)
        dkey = random.choice(date_keys)
        
        # Get price from product
        base_price = df_products.loc[df_products['product_id'] == pid, 'price'].values[0]
        qty = random.randint(1, 5)
        total = round(base_price * qty, 2)
        
        sales_data.append([i, dkey, pid, sid, cid, qty, total])

    df_sales = pd.DataFrame(sales_data, columns=['transaction_id', 'date_key', 'product_id', 'store_id', 'customer_id', 'quantity', 'total_amount'])
    df_sales.to_sql('fact_sales', db_engine, if_exists='replace', index=False)
    print(f"✅ Table 'fact_sales' created with {NUM_TRANSACTIONS} rows.")
    print("\n🎉 DONE! The 'walmart_db' is fully populated.")
    print("You can now go back to the Notebook and just run the %%sql QUERY cells!")

except Exception as e:
    print("\n❌ FAILED:", e)
