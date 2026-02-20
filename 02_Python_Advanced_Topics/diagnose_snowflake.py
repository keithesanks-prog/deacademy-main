import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

output_file = "snowflake_diagnostic_output.txt"

with open(output_file, "w") as f:
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
        
        f.write("Checking context...\n")
        cur.execute("SELECT CURRENT_REGION(), CURRENT_VERSION()")
        f.write(f"Region/Version: {cur.fetchone()}\n")
        
        f.write("\nChecking STG_FEATURES View Definition...\n")
        try:
            cur.execute("SELECT GET_DDL('VIEW', 'WALMART_PROJECT.PUBLIC.STG_FEATURES')")
            ddl = cur.fetchone()[0]
            f.write(f"DDL:\n{ddl}\n")
        except Exception as e:
            f.write(f"Could not get DDL (might not be a view?): {e}\n")

        f.write("\nInspecting available files in WALMART_RAW_STAGE...\n")
        files_to_check = ['fact.csv', 'department.csv', 'stores.csv']
        for file in files_to_check:
            f.write(f"\n--- Head of {file} ---\n")
            try:
                # Assuming simple CSV structure, read first line or so
                # Use query on stage
                sql = f"SELECT $1, $2, $3, $4, $5 FROM @WALMART_PROJECT.PUBLIC.WALMART_RAW_STAGE/{file} LIMIT 5"
                cur.execute(sql)
                rows = cur.fetchall()
                for r in rows:
                    f.write(f"{r}\n")
            except Exception as e:
                f.write(f"Could not read {file}: {e}\n")
        
        f.write("\nChecking tables in WALMART_PROJECT.PUBLIC...\n")
        try:
            cur.execute("SHOW TABLES LIKE 'STG_%' IN SCHEMA WALMART_PROJECT.PUBLIC")
            tables = cur.fetchall()
            for t in tables:
                f.write(f" - {t[1]} (Owner: {t[5]})\n")
        except Exception as e:
            f.write(f"Could not show tables: {e}\n")

        f.write("\nChecking STG_FEATURES definition...\n")
        try:
            cur.execute("DESC TABLE WALMART_PROJECT.PUBLIC.STG_FEATURES")
            cols = cur.fetchall()
            for c in cols:
                f.write(f" - {c[0]} {c[1]}\n")
        except Exception as e:
            f.write(f"Could not desc STG_FEATURES: {e}\n")

        f.write("\nChecking if we can read from STG_FEATURES...\n")
        try:
            cur.execute("SELECT COUNT(*) FROM WALMART_PROJECT.PUBLIC.STG_FEATURES")
            f.write(f"Count: {cur.fetchone()[0]}\n")
        except Exception as e:
            f.write(f"Could not count STG_FEATURES: {e}\n")
            
        f.write("\nChecking WALMART_FACT_TABLE definition...\n")
        try:
            cur.execute("DESC TABLE WALMART_PROJECT.PUBLIC.WALMART_FACT_TABLE")
            cols = cur.fetchall()
            for c in cols:
                f.write(f" - {c[0]} {c[1]}\n")
        except Exception as e:
            f.write(f"Could not desc WALMART_FACT_TABLE: {e}\n")

        f.write("\nChecking STG_FACT definition...\n")
        try:
            cur.execute("DESC TABLE WALMART_PROJECT.PUBLIC.STG_FACT")
            cols = cur.fetchall()
            for c in cols:
                f.write(f" - {c[0]} {c[1]}\n")
        except Exception as e:
            f.write(f"Could not desc STG_FACT: {e}\n")

    except Exception as e:
        f.write(f"Connection failed: {e}\n")
    finally:
        if 'conn' in locals():
            conn.close()
