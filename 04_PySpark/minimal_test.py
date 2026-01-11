import os
import sys

# Minimal configuration
os.environ["JAVA_HOME"] = r"C:\Users\ksank\.gemini\java\jdk-17.0.9+8"
os.environ["HADOOP_HOME"] = r"C:\Users\ksank\.hadoop"
os.environ["PATH"] = os.environ["JAVA_HOME"] + r"\bin;" + os.environ["HADOOP_HOME"] + r"\bin;" + os.environ["PATH"]
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession

# Try with explicit loopback configuration to avoid socket issues
spark = SparkSession.builder \
    .appName("MinimalTest") \
    .master("local[1]") \
    .config("spark.driver.host", "127.0.0.1") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .config("spark.sql.warehouse.dir", "file:///C:/tmp/hive") \
    .getOrCreate()

print("[OK] Spark Session Created")

# Simple test without DataFrame operations
print(f"Spark Version: {spark.version}")
print(f"Master: {spark.sparkContext.master}")

# Try a simple RDD operation first (lower level than DataFrame)
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])
result = rdd.collect()
print(f"[OK] RDD collect worked: {result}")

# Now try DataFrame
df = spark.createDataFrame([(1, "a"), (2, "b")], ["id", "val"])
print("[OK] DataFrame created")

# The critical test
df.show()
print("[OK] df.show() worked!")

spark.stop()
