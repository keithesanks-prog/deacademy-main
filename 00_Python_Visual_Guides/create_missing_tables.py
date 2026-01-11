# This script will create the missing tables directly
# Run this instead of the notebook if Jupyter keeps caching the old code

import pandas as pd
import numpy as np
import sqlalchemy
import random
from datetime import datetime, timedelta

print("🔧 Creating missing Walmart DB tables...")
print("=" * 60)

# Connect to database
username = 'python_user'
password = 'password'
host = '127.0.0.1'
port = '3306'
db_name = "walmart_db"

db_connection_str = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"
db_engine = sqlalchemy.create_engine(db_connection_str)

# ==========================================
# 4. DIM_DATE (THE FIXED VERSION)
# ==========================================
print("\n📅 Creating dim_date table...")
start_date = datetime(2023, 1, 1)
date_list = [start_date + timedelta(days=x) for x in range(365)]
dates = []

for dt in date_list:
    date_key = int(dt.strftime('%Y%m%d'))
    quarter = (dt.month - 1) // 3 + 1  # ✅ FIXED: Manual quarter calculation
    dates.append([date_key, dt, dt.year, dt.month, f"Q{quarter}", dt.strftime('%A')])

df_date = pd.DataFrame(dates, columns=['date_key', 'date', 'year', 'month', 'quarter', 'day_name'])
df_date.to_sql('dim_date', db_engine, if_exists='replace', index=False)
print("✅ Table 'dim_date' created with 365 rows")

# ==========================================
# 5. FACT_SALES
# ==========================================
print("\n💰 Creating fact_sales table...")

# Get existing dimension data
df_products = pd.read_sql("SELECT * FROM dim_products", db_engine)
df_stores = pd.read_sql("SELECT * FROM dim_stores", db_engine)
df_customers = pd.read_sql("SELECT * FROM dim_customers", db_engine)

NUM_TRANSACTIONS = 2000
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
print(f"✅ Table 'fact_sales' created with {NUM_TRANSACTIONS} rows")

print("\n" + "=" * 60)
print("🎉 SUCCESS! All tables created!")
print("=" * 60)
print("\nYou can now run: python walmart_sql_practice.py")
