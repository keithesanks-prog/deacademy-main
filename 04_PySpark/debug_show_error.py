
import os
import sys
from pyspark.sql import SparkSession

# FORCE environment variables for this process
os.environ["JAVA_HOME"] = r"C:\Users\ksank\.gemini\java\jdk-17.0.9+8"
os.environ["HADOOP_HOME"] = r"C:\Users\ksank\.hadoop"
os.environ["PATH"] = r"C:\Users\ksank\.hadoop\bin;" + os.environ["JAVA_HOME"] + r"\bin;" + os.environ["PATH"]

# Print to verify
print(f"JAVA_HOME: {os.environ['JAVA_HOME']}")
print(f"HADOOP_HOME: {os.environ['HADOOP_HOME']}")

try:
    # Aggressive configuration to disable ALL hadoop native interaction
    spark = SparkSession.builder \
        .appName("DebugApp") \
        .master("local[*]") \
        .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem") \
        .config("spark.hadoop.io.native.lib.available", "false") \
        .getOrCreate()
    
    print("Session created.")
    
    # Simple dataframe
    df = spark.createDataFrame([(1, "a")], ["id", "val"])
    
    print("DataFrame created. Attempting show()...")
    # This is where it fails
    df.show() 
    print("Show successful.")

except Exception as e:
    print("\nXXX CAUGHT ERROR XXX")
    print(e)
    # Print the java stack trace if available (often wrapped in the exception)
    import traceback
    traceback.print_exc()

