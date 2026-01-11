"""
Fix for PySpark temporary file creation issue on Windows

This script addresses the java.nio.file.NoSuchFileException error that occurs
when Spark's PythonGatewayServer tries to create temporary files.

The fix involves:
1. Creating a dedicated temp directory for Spark
2. Setting Java system properties to use this directory
3. Configuring environment variables properly
"""

import os
import sys
import tempfile
from pathlib import Path

def setup_pyspark_environment():
    """Configure environment for PySpark on Windows"""
    
    # 1. Setup Java and Hadoop paths
    java_home = r"C:\Users\ksank\.gemini\java\jdk-17.0.9+8"
    hadoop_home = r"C:\Users\ksank\.hadoop"
    
    os.environ["JAVA_HOME"] = java_home
    os.environ["HADOOP_HOME"] = hadoop_home
    
    # 2. Set Python executables for worker and driver
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    
    # 3. Create a dedicated temp directory for Spark
    spark_temp_dir = Path(r"C:\tmp\spark-temp")
    spark_temp_dir.mkdir(parents=True, exist_ok=True)
    
    # 4. Set Java temp directory to our custom location
    os.environ["JAVA_OPTS"] = f"-Djava.io.tmpdir={spark_temp_dir}"
    
    # 5. Also set the system TEMP and TMP to a stable location
    # This prevents Windows from cleaning up temp files too quickly
    os.environ["TEMP"] = str(spark_temp_dir)
    os.environ["TMP"] = str(spark_temp_dir)
    
    # 6. Update PATH
    os.environ["PATH"] = f"{java_home}\\bin;{hadoop_home}\\bin;{os.environ['PATH']}"
    
    print(f"✅ Environment configured:")
    print(f"   JAVA_HOME: {java_home}")
    print(f"   HADOOP_HOME: {hadoop_home}")
    print(f"   Python: {sys.executable}")
    print(f"   Spark Temp Dir: {spark_temp_dir}")
    
    return spark_temp_dir

def create_spark_session():
    """Create a Spark session with proper configuration"""
    from pyspark.sql import SparkSession
    
    spark_temp_dir = setup_pyspark_environment()
    
    # Create Spark session with additional configurations
    spark = SparkSession.builder \
        .appName("PySpark_Windows_Fixed") \
        .master("local[*]") \
        .config("spark.sql.warehouse.dir", "file:///C:/tmp/hive") \
        .config("spark.local.dir", str(spark_temp_dir)) \
        .config("spark.driver.extraJavaOptions", f"-Djava.io.tmpdir={spark_temp_dir}") \
        .config("spark.executor.extraJavaOptions", f"-Djava.io.tmpdir={spark_temp_dir}") \
        .getOrCreate()
    
    return spark

if __name__ == "__main__":
    print("🚀 Starting PySpark with Windows temp fix...\n")
    
    try:
        # Create Spark session
        spark = create_spark_session()
        print("\n✅ Spark Session Created Successfully!")
        print(f"   Spark Version: {spark.version}")
        print(f"   Master: {spark.sparkContext.master}\n")
        
        # Test with a simple DataFrame
        print("📊 Testing DataFrame creation and operations...\n")
        data = [
            ("Alice", 34, "Data Engineer"),
            ("Bob", 45, "Data Scientist"),
            ("Charlie", 28, "Analytics Engineer")
        ]
        columns = ["Name", "Age", "Role"]
        
        df = spark.createDataFrame(data, columns)
        print("✅ DataFrame created successfully!")
        
        print("\n📋 Showing DataFrame:")
        df.show()
        
        print("✅ df.show() executed successfully!")
        
        # Test some operations
        print("\n🔍 Testing filter operation:")
        df.filter(df.Age > 30).show()
        
        print("\n✅ All tests passed! PySpark is working correctly.")
        
        # Stop the session
        spark.stop()
        print("\n🛑 Spark session stopped cleanly.")
        
    except Exception as e:
        print("\n❌ ERROR occurred:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        print("\n📋 Full traceback:")
        traceback.print_exc()
        sys.exit(1)
