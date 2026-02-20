import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )
    
    cur = conn.cursor()
    
    # 1. Create Stage (Verified working code from debug_stage.py)
    print("Creating Stage...")
    create_stage_sql = """
    CREATE OR REPLACE TEMPORARY STAGE TEMP_WALMART_RELOAD_FINAL
    URL = 's3://deacademy-walmart-bucket/raw/'
    STORAGE_INTEGRATION = S3_WALMART_INTEGRATION
    FILE_FORMAT = (TYPE = CSV);
    """
    cur.execute(create_stage_sql)
    print("Stage created successfully.")

    # 2. List Files
    print("Listing files...")
    cur.execute("LIST @TEMP_WALMART_RELOAD_FINAL")
    files = cur.fetchall()
    
    features_file = None
    for f in files:
        filename = f[0]
        # Check for features csv
        if 'features' in filename.lower() and filename.lower().endswith('.csv'):
            features_file = filename.split('/')[-1] # Extract just filename
            break
            
    if not features_file:
        print("Features file not found in list. Checking for ANY csv...")
        for f in files:
             if f[0].lower().endswith('.csv') and 'walmart' in f[0].lower():
                 features_file = f[0].split('/')[-1]
                 break
    
    if features_file:
        print(f"File identified: {features_file}")
        
        # 3. Truncate
        print("Truncating table...")
        cur.execute("TRUNCATE TABLE WALMART_PROJECT.PUBLIC.STG_FEATURES")
        
        # 4. Copy
        print("Loading data...")
        copy_sql = f"""
        COPY INTO WALMART_PROJECT.PUBLIC.STG_FEATURES
        FROM @TEMP_WALMART_RELOAD_FINAL/{features_file}
        FILE_FORMAT = (TYPE = CSV, SKIP_HEADER = 1)
        ON_ERROR = 'CONTINUE'
        FORCE = TRUE
        """
        cur.execute(copy_sql)
        print("Data loaded.")
        
        # 5. Verify
        cur.execute("SELECT COUNT(*) FROM WALMART_PROJECT.PUBLIC.STG_FEATURES")
        count = cur.fetchone()[0]
        print(f"Total Rows: {count}")
    else:
        print("Could not identify a file to load.")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
