"""
Verification script for Python 3.11 + PySpark 3.5.3 environment.
"""
import os
import sys
import pandas as pd
from pyspark.sql import SparkSession
from pathlib import Path

def setup_env():
    # Set Java/Hadoop paths (User's paths)
    os.environ["JAVA_HOME"] = r"C:\Users\ksank\.gemini\java\jdk-17.0.9+8"
    os.environ["HADOOP_HOME"] = r"C:\Users\ksank\.hadoop"
    # Ensure they are in PATH
    os.environ["PATH"] = f"{os.environ['JAVA_HOME']}\\bin;{os.environ['HADOOP_HOME']}\\bin;{os.environ['PATH']}"
    
    # Set Temp Dir
    spark_temp_dir = Path(r"C:\tmp\spark-temp")
    spark_temp_dir.mkdir(parents=True, exist_ok=True)
    os.environ["JAVA_OPTS"] = f"-Djava.io.tmpdir={str(spark_temp_dir)}"
    return str(spark_temp_dir)

def test_spark():
    temp_dir = setup_env()
    print(f"Environment Configured. Temp Dir: {temp_dir}")
    print(f"Python Executable: {sys.executable}")
    
    # Explicitly set PYSPARK_PYTHON in env
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    
    spark = SparkSession.builder \
        .appName("PySpark_3.5.3_Test_Py311") \
        .master("local[*]") \
        .config("spark.sql.warehouse.dir", "file:///C:/tmp/hive") \
        .config("spark.local.dir", temp_dir) \
        .config("spark.pyspark.python", sys.executable) \
        .config("spark.pyspark.driver.python", sys.executable) \
        .config("spark.python.use.daemon", "false") \
        .config("spark.python.worker.reuse", "false") \
        .config("spark.driver.extraJavaOptions", f"-Djava.io.tmpdir={temp_dir}") \
        .config("spark.executor.extraJavaOptions", f"-Djava.io.tmpdir={temp_dir}") \
        .getOrCreate()
        
    print(f"Spark Session Created. Version: {spark.version}")
    
    data = [("Alice", 1), ("Bob", 2)]
    df = spark.createDataFrame(data, ["Name", "Id"])
    
    # Test display helper logic (collect)
    print("Testing collect()...")
    rows = df.limit(5).rdd.collect()
    pdf = pd.DataFrame(rows, columns=df.columns, dtype=str) # simplified
    print(pdf)
    
    print("Test Passed!")
    spark.stop()

if __name__ == "__main__":
    test_spark()
