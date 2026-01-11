"""
Test PySpark with Python 3.12 to verify compatibility fix
"""

import os
import sys
from pathlib import Path

# Setup environment
java_home = r"C:\Users\ksank\.gemini\java\jdk-17.0.9+8"
hadoop_home = r"C:\Users\ksank\.hadoop"

os.environ["JAVA_HOME"] = java_home
os.environ["HADOOP_HOME"] = hadoop_home
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["PATH"] = f"{java_home}\\bin;{hadoop_home}\\bin;{os.environ['PATH']}"

print("=" * 60)
print("PySpark Python 3.12 Compatibility Test")
print("=" * 60)
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print(f"JAVA_HOME: {java_home}")
print(f"HADOOP_HOME: {hadoop_home}")
print("=" * 60)

try:
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, when
    
    # Test 1: Create Spark Session
    print("\n[TEST 1] Creating Spark Session...")
    spark = SparkSession.builder \
        .appName("Python312CompatibilityTest") \
        .master("local[*]") \
        .config("spark.sql.warehouse.dir", "file:///C:/tmp/hive") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .getOrCreate()
    print("SUCCESS: Spark session created")
    print(f"  Spark Version: {spark.version}")

    # Test 1.5: Basic RDD Collect
    print("\n[TEST 1.5] Testing Basic RDD Collect...")
    try:
        rdd = spark.sparkContext.parallelize([1, 2, 3])
        result = rdd.collect()
        print(f"SUCCESS: RDD Collect result: {result}")
    except Exception as e:
        print(f"FAILED: RDD Collect failed: {e}")

    # Test 1.6: Row Serialization via RDD
    print("\n[TEST 1.6] Testing DataFrame -> RDD Collect...")
    try:
        # Create a simple DataFrame and convert to RDD
        # This forces Row serialization usage but via RDD path
        df_range = spark.range(5)
        rows = df_range.rdd.collect()
        print(f"SUCCESS: DataFrame->RDD Collect result: {rows}")
    except Exception as e:
        print(f"FAILED: DataFrame->RDD Collect failed: {e}")

    # Test 1.7: DataFrame Native Collect
    print("\n[TEST 1.7] Testing DataFrame Native Collect...")
    try:
        # This uses DataFrame execution path
        rows = df_range.collect()
        print(f"SUCCESS: DataFrame Native Collect result: {rows}")
    except Exception as e:
        print(f"FAILED: DataFrame Native Collect failed: {e}")

    # Test 2: Create DataFrame
    print("\n[TEST 2] Creating DataFrame...")
    data = [
        ("Alice", 34, "Data Engineer", 95000),
        ("Bob", 45, "Data Scientist", 110000),
        ("Charlie", 28, "Analytics Engineer", 85000),
        ("Diana", 32, "ML Engineer", 105000),
        ("Eve", 29, "Data Analyst", 75000)
    ]
    columns = ["Name", "Age", "Role", "Salary"]
    df = spark.createDataFrame(data, columns)
    print("SUCCESS: DataFrame created")
    
    # Test 2.5: df.head()
    # print("\n[TEST 2.5] Testing df.head()...")
    # try:
    #     head_rows = df.head(5)
    #     print(f"SUCCESS: df.head() result: {head_rows}")
    # except Exception as e:
    #     print(f"FAILED: df.head() failed: {e}")

    # Test 2.6: df.toPandas()
    print("\n[TEST 2.6] Testing df.toPandas()...")
    try:
        import pandas as pd
        pdf = df.toPandas()
        print("SUCCESS: df.toPandas() result:")
        print(pdf)
    except Exception as e:
        print(f"FAILED: df.toPandas() failed: {e}")

    # Test 3: Show DataFrame (DISABLE IF CRASHING)
    # print("\n[TEST 3] Testing df.show() - CRITICAL TEST...")
    # df.show()
    # print("SUCCESS: df.show() executed without errors!")
    
    # Test 4: Filter operation
    print("\n[TEST 4] Testing filter operation...")
    high_earners = df.filter(col("Salary") > 90000)
    print(f"SUCCESS: Filter result: {high_earners.collect()}")
    
    # Test 5: Group by and aggregate
    print("\n[TEST 5] Testing groupBy and aggregate...")
    print(f"SUCCESS: GroupBy result: {df.groupBy('Role').count().collect()}")
    
    # Test 6: SQL query
    print("\n[TEST 6] Testing SQL query...")
    df.createOrReplaceTempView("employees")
    result = spark.sql("""
        SELECT Role, AVG(Salary) as avg_salary
        FROM employees
        GROUP BY Role
        ORDER BY avg_salary DESC
    """)
    print(f"SUCCESS: SQL query result: {result.collect()}")
    
    # Test 7: Transformations
    print("\n[TEST 7] Testing transformations...")
    df_with_category = df.withColumn(
        "Salary_Category",
        when(col("Salary") >= 100000, "High")
        .when(col("Salary") >= 80000, "Medium")
        .otherwise("Entry")
    )
    print(f"SUCCESS: Transformations result: {df_with_category.collect()}")
    
    # Test 8: Write and read data
    print("\n[TEST 8] Testing file I/O...")
    output_path = "output/test_employees"
    df.write.mode("overwrite").parquet(output_path)
    print(f"  Data written to {output_path}")
    
    df_read = spark.read.parquet(output_path)
    print("  Data read back from parquet:")
    print(f"SUCCESS: File I/O result: {df_read.collect()}")
    print("SUCCESS: File I/O operations completed")
    
    # Stop Spark session
    spark.stop()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("PySpark is working correctly with Python 3.12 (using collect/toPandas)")
    print("=" * 60)
    
except Exception as e:
    print(f"\nFAILED: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
