# PySpark Windows Setup Cell
# Add this as the FIRST cell in your notebook

import os
import sys

# 1. Configure environment paths
java_home = r"C:\Users\ksank\.gemini\java\jdk-17.0.9+8"
hadoop_home = r"C:\Users\ksank\.hadoop"

os.environ["JAVA_HOME"] = java_home
os.environ["HADOOP_HOME"] = hadoop_home
os.environ["PATH"] = java_home + r"\bin;" + hadoop_home + r"\bin;" + os.environ["PATH"]

# 2. Configure PySpark to use the correct Python executable
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

print(f"Environment configured:")
print(f"  JAVA_HOME: {java_home}")
print(f"  HADOOP_HOME: {hadoop_home}")
print(f"  Python: {sys.executable}")
print("\nYou can now create your SparkSession in the next cell.")
