import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv(r"c:\Users\ksank\training\02_Python_Advanced_Topics\.env")

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)
cur = conn.cursor()

print("="*60)
print("SNOWFLAKE TABLE VERIFICATION")
print("="*60)

tables = [
    "DIM_PROVIDER",
    "DIM_QUALITY", 
    "FACT_STAFFING",
    "FACT_QUALITY_MDS",
    "FACT_CITATIONS",
    "FACT_PENALTIES"
]

for table in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        status = "✅" if count > 0 else "❌ EMPTY"
        print(f"{table:25} {count:>15,} rows  {status}")
    except Exception as e:
        print(f"{table:25} ERROR: {str(e)}")

print("="*60)
cur.close()
conn.close()
