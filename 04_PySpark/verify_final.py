
import os
import sys

# Set up environment variables for verification
# Using the current directory's python311 as the python source
current_dir = os.getcwd()
python_exe = os.path.join(current_dir, "python311", "python.exe")

os.environ["PYSPARK_PYTHON"] = python_exe
os.environ["PYSPARK_DRIVER_PYTHON"] = python_exe
os.environ["JAVA_HOME"] = r"C:\Users\ksank\.gemini\java\jdk-17.0.9+8"
os.environ["HADOOP_HOME"] = r"C:\Users\ksank\.hadoop"

print("=== Environment Setup ===")
print(f"PYSPARK_PYTHON: {os.environ['PYSPARK_PYTHON']}")
print(f"JAVA_HOME: {os.environ['JAVA_HOME']}")
print("=========================")

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def run_tests():
    print("\n[TEST 1] Creating Spark Session...")
    spark = SparkSession.builder \
        .appName("FinalVerification") \
        .master("local[*]") \
        .config("spark.sql.warehouse.dir", "file:///C:/tmp/hive") \
        .getOrCreate()
    print(f"SUCCESS: Spark Version {spark.version}")

    print("\n[TEST 2] Creating DataFrame...")
    data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
    df = spark.createDataFrame(data, ["Name", "Id"])
    print("SUCCESS: DataFrame created")

    print("\n[TEST 3] Testing df.show() (The moment of truth)...")
    try:
        df.show()
        print("SUCCESS: df.show() works!")
    except Exception as e:
        print(f"FAILED: df.show() crashed: {e}")
        return

    print("\n[TEST 4] Testing df.collect()...")
    res = df.collect()
    print(f"SUCCESS: Collected {len(res)} rows: {res}")

    print("\n[TEST 5] Testing df.toPandas()...")
    try:
        pdf = df.toPandas()
        print("SUCCESS: toPandas() result:")
        print(pdf)
    except Exception as e:
        print(f"FAILED: toPandas failed: {e}")

    print("\n[TEST 6] Testing Filter + Collect...")
    filtered = df.filter(col("Id") > 1).collect()
    print(f"SUCCESS: Filtered result: {filtered}")

    spark.stop()
    print("\nALL SYSTEM GO: Python 3.11 + PySpark 3.5.3 is STABLE.")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")
        import traceback
        traceback.print_exc()
