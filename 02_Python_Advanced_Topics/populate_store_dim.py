import snowflake.connector
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

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
    print("Checking what store IDs exist in STG_DEPARTMENT (sales data)...")
    df_stores = pd.read_sql("""
        SELECT DISTINCT STORE_ID 
        FROM WALMART_PROJECT.PUBLIC.STG_DEPARTMENT 
        ORDER BY STORE_ID
    """, conn)
    print(f"Found {len(df_stores)} unique stores in sales data:")
    print(df_stores['STORE_ID'].tolist())
    
    print("\n\nNow let's populate WALMART_STORE_DIM with store size data...")
    print("Generating random store sizes for each store (100,000 - 250,000 sq ft)...")
    
    # Generate random sizes for each store
    import numpy as np
    np.random.seed(42)  # For reproducibility
    df_stores['STORE_SIZE'] = np.random.randint(100000, 250000, size=len(df_stores))
    # Use string format for timestamp that Snowflake accepts
    df_stores['UPDATE_DATE'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Show what we're about to insert
    print("\nData to insert (first 10 rows):")
    print(df_stores.head(10).to_string())
    
    # Insert into WALMART_STORE_DIM
    cursor = conn.cursor()
    
    # First, clear the table (in case there's old data)
    cursor.execute("TRUNCATE TABLE WALMART_PROJECT.PUBLIC.WALMART_STORE_DIM")
    print("\nCleared WALMART_STORE_DIM table")
    
    # Insert the data
    insert_count = 0
    for _, row in df_stores.iterrows():
        cursor.execute(
            "INSERT INTO WALMART_PROJECT.PUBLIC.WALMART_STORE_DIM (STORE_ID, STORE_SIZE, UPDATE_DATE) VALUES (%s, %s, %s)",
            (int(row['STORE_ID']), int(row['STORE_SIZE']), row['UPDATE_DATE'])
        )
        insert_count += 1
    
    conn.commit()
    print(f"\nSuccessfully inserted {insert_count} rows into WALMART_STORE_DIM")
    
    # Verify
    df_verify = pd.read_sql("SELECT COUNT(*) as CNT FROM WALMART_PROJECT.PUBLIC.WALMART_STORE_DIM", conn)
    print(f"Verification - WALMART_STORE_DIM now has {df_verify.iloc[0,0]} rows")
    
    # Show sample of inserted data
    print("\nSample of inserted data:")
    df_sample = pd.read_sql("SELECT * FROM WALMART_PROJECT.PUBLIC.WALMART_STORE_DIM LIMIT 5", conn)
    print(df_sample.to_string())
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if 'conn' in locals():
        conn.close()
