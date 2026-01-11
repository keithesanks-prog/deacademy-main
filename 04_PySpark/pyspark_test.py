# PySpark Test Script for Jupyter Notebook
# This verifies PySpark is installed correctly

from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder \
    .appName("PySpark Test") \
    .master("local[*]") \
    .getOrCreate()

print("✅ PySpark installed successfully!")
print(f"Spark version: {spark.version}")

# Create a simple DataFrame to test
data = [
    ("Alice", 34, "Data Engineer"),
    ("Bob", 45, "Data Scientist"),
    ("Charlie", 28, "Analytics Engineer")
]

columns = ["Name", "Age", "Role"]
df = spark.createDataFrame(data, columns)

print("\n📊 Sample DataFrame:")
df.show()

# Stop the Spark session
spark.stop()
print("\n✅ Test completed successfully!")
