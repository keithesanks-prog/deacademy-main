import snowflake.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(r"c:\Users\ksank\training\02_Python_Advanced_Topics\.env")

def verify_counts():
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )
        cur = conn.cursor()

        tables = ["DIM_PROVIDER", "FACT_STAFFING", "DIM_QUALITY"]

        for table in tables:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                print(f"I found {count} rows in {table}")
                import time
                time.sleep(1)
            except Exception as e:
                print(f"Error querying {table}: {e}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    verify_counts()
