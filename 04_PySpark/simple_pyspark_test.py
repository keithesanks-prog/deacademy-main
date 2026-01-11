import os
import sys

# Setup environment
java_home = r"C:\Users\ksank\.gemini\java\jdk-17.0.9+8"
hadoop_home = r"C:\Users\ksank\.hadoop"

os.environ["JAVA_HOME"] = java_home
os.environ["HADOOP_HOME"] = hadoop_home
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# Create dedicated temp directory
import pathlib
spark_temp = pathlib.Path(r"C:\tmp\spark-temp")
spark_temp.mkdir(parents=True, exist_ok=True)

# Set temp directory
os.environ["JAVA_OPTS"] = f"-Djava.io.tmpdir={spark_temp}"
os.environ["TEMP"] = str(spark_temp)
os.environ["TMP"] = str(spark_temp)

# Update PATH
os.environ["PATH"] = f"{java_home}\\bin;{hadoop_home}\\bin;{os.environ['PATH']}"

print("Environment configured")
print(f"Python: {sys.executable}")
print(f"Temp: {spark_temp}")

try:
    from pyspark.sql import SparkSession
    
    spark = SparkSession.builder \
        .appName("SimpleTest") \
        .master("local[*]") \
        .config("spark.local.dir", str(spark_temp)) \
        .config("spark.driver.extraJavaOptions", f"-Djava.io.tmpdir={spark_temp}") \
        .config("spark.executor.extraJavaOptions", f"-Djava.io.tmpdir={spark_temp}") \
        .getOrCreate()
    
    print("Spark session created")
    
    data = [("Alice", 34), ("Bob", 45)]
    df = spark.createDataFrame(data, ["Name", "Age"])
    
    print("DataFrame created")
    df.show()
    print("SUCCESS")
    
    spark.stop()
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
