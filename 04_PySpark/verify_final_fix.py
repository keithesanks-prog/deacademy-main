
import os
import sys
from pyspark.sql import SparkSession

# 1. Setup Java and Hadoop paths regarding the user's environment
java_home = r"C:\Users\ksank\.gemini\java\jdk-17.0.9+8"
hadoop_home = r"C:\Users\ksank\.hadoop"
os.environ["JAVA_HOME"] = java_home
os.environ["HADOOP_HOME"] = hadoop_home

# 2. FIX: Set python executable for worker and driver
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# 3. Update PATH
os.environ["PATH"] = java_home + r"\bin;" + hadoop_home + r"\bin;" + os.environ["PATH"]

print(f"Using Python: {sys.executable}")

try:
    spark = SparkSession.builder \
        .appName("FinalVerification") \
        .master("local[*]") \
        .config("spark.sql.warehouse.dir", "file:///C:/tmp/hive") \
        .getOrCreate()
    
    print("[OK] Spark Session Created")
    
    data = [("Alice", 34), ("Bob", 45)]
    columns = ["Name", "Age"]
    df = spark.createDataFrame(data, columns)
    
    print("[OK] DataFrame Created")
    print("Attempting to show data...")
    df.show()
    print("[OK] df.show() Successful")
    
    spark.stop()

except Exception as e:
    print("\n[ERROR] FAILED")
    print(e)
    import traceback
    traceback.print_exc()
