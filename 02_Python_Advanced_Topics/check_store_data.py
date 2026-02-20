import snowflake.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema=os.getenv('SNOWFLAKE_SCHEMA')
)

try:
    print("Checking STG_STORE table...")
    df_store = pd.read_sql("SELECT COUNT(*) as CNT FROM WALMART_PROJECT.PUBLIC.STG_STORE", conn)
    print(f"STG_STORE COUNT: {df_store.iloc[0,0]}")
    
    if df_store.iloc[0,0] > 0:
        print("\nSample data from STG_STORE:")
        df_sample = pd.read_sql("SELECT * FROM WALMART_PROJECT.PUBLIC.STG_STORE LIMIT 5", conn)
        print(df_sample.to_string())
        
        print("\n\nColumn names in STG_STORE:")
        print(df_sample.columns.tolist())
    
    print("\n\nChecking WALMART_STORE_DIM table...")
    df_dim = pd.read_sql("SELECT COUNT(*) as CNT FROM WALMART_PROJECT.PUBLIC.WALMART_STORE_DIM", conn)
    print(f"WALMART_STORE_DIM COUNT: {df_dim.iloc[0,0]}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
