import os
import snowflake.connector
import pandas as pd
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

print("Connected to Snowflake")
print(f"Current Database: {os.getenv('SNOWFLAKE_DATABASE')}")

try:
    # Check for WALMART_STORE_DIM count
    print("\n--- Checking for WALMART_STORE_DIM Count ---")
    
    count_df = pd.read_sql("SELECT COUNT(*) as CNT FROM WALMART_PROJECT.PUBLIC.WALMART_STORE_DIM", conn)
    print(f"Row Count: {count_df.iloc[0,0]}")
    
    # 1. Just select * columns to confirm names again
    df_store = pd.read_sql("SELECT * FROM WALMART_PROJECT.PUBLIC.WALMART_STORE_DIM LIMIT 5", conn)
    print("Columns:", df_store.columns.tolist())
    print("First 5 rows:\n", df_store.to_string())
    
    # 2. Try selecting SIZE directly
    try:
        print("Attempting to SELECT SIZE...")
        pd.read_sql("SELECT SIZE FROM WALMART_PROJECT.PUBLIC.WALMART_STORE_DIM LIMIT 1", conn)
        print("Success: SELECT SIZE")
    except Exception as e:
        print(f"Failed SELECT SIZE: {e}")

    # 3. Try selecting with Alias
    try:
        print("Attempting to SELECT s.SIZE...")
        pd.read_sql("SELECT s.SIZE FROM WALMART_PROJECT.PUBLIC.WALMART_STORE_DIM s LIMIT 1", conn)
        print("Success: SELECT s.SIZE")
    except Exception as e:
        print(f"Failed SELECT s.SIZE: {e}")

    # 4. Try joining
    try:
        print("Attempting Join...")
        q = """
        SELECT s.SIZE 
        FROM WALMART_PROJECT.PUBLIC.STG_DEPARTMENT d 
        JOIN WALMART_PROJECT.PUBLIC.WALMART_STORE_DIM s 
        ON d.STORE_ID = s.STORE_ID 
        LIMIT 1
        """
        pd.read_sql(q, conn)
        print("Success: Join with s.SIZE")
    except Exception as e:
        print(f"Failed Join: {e}")
    try:
        print("Listing all tables in PUBLIC:")
        print(pd.read_sql("SHOW TABLES IN SCHEMA WALMART_PROJECT.PUBLIC", conn)['name'].tolist())
    except:
        pass

finally:
    conn.close()
