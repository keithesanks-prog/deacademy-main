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
    print("Checking all tables in WALMART_PROJECT.PUBLIC schema...")
    df = pd.read_sql("""
        SELECT TABLE_NAME, ROW_COUNT 
        FROM WALMART_PROJECT.INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'PUBLIC'
        ORDER BY TABLE_NAME
    """, conn)
    print(df.to_string())
    
    print("\n\nChecking for STORE data in STG_STORE table...")
    df_store = pd.read_sql("SELECT COUNT(*) as CNT FROM WALMART_PROJECT.PUBLIC.STG_STORE", conn)
    print(f"STG_STORE COUNT: {df_store.iloc[0,0]}")
    
    if df_store.iloc[0,0] > 0:
        print("\nSample data from STG_STORE:")
        df_sample = pd.read_sql("SELECT * FROM WALMART_PROJECT.PUBLIC.STG_STORE LIMIT 5", conn)
        print(df_sample.to_string())
        
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
