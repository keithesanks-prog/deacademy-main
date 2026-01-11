import json
import os

notebook_path = "pyspark_quickstart.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Find the setup cell
setup_cell_index = -1
for i, cell in enumerate(cells):
    if cell['cell_type'] == 'code' and '# --- WINDOWS ENVIRONMENT SETUP ---' in ''.join(cell['source']):
        setup_cell_index = i
        break

if setup_cell_index != -1:
    print("Found setup cell, updating...")
    cell = cells[setup_cell_index]
    source = cell['source']
    
    new_source = [
        "# --- KERNEL CHECK ---\n",
        "import sys\n",
        "if sys.version_info < (3, 11) or sys.version_info >= (3, 12):\n",
        "    print(f\"\\033[91m\u26a0\ufe0f WARNING: You are running Python {sys.version.split()[0]}!\\033[0m\")\n",
        "    print(\"Please select the kernel: 'Python 3.11 (PySpark)' from the top right menu.\")\n",
        "    print(\"Using the wrong Python version will cause crashes on Windows.\")\n",
        "else:\n",
        "    print(\"\u2705 Correct Python Kernel (3.11) detected!\")\n",
        "\n",
        "import os\n",
        "import sys\n",
        "from pyspark.sql import SparkSession\n",
        "import pandas as pd\n",
        "import tempfile\n",
        "from pathlib import Path\n",
        "\n",
        "# --- WINDOWS ENVIRONMENT SETUP ---\n",
        "# Use the local Python 3.11 environment we created\n",
        "current_dir = os.getcwd()\n",
        "python_path = os.path.join(current_dir, \"python311_env\", \"python.exe\")\n",
        "\n",
        "os.environ['PYSPARK_PYTHON'] = python_path\n",
        "os.environ['PYSPARK_DRIVER_PYTHON'] = python_path\n",
        "os.environ['JAVA_HOME'] = r'C:\\Users\\ksank\\.gemini\\java\\jdk-17.0.9+8'\n",
        "os.environ['HADOOP_HOME'] = r'C:\\Users\\ksank\\.hadoop'\n",
        "\n",
        "# --- CRASH FIX: Display Helper ---\n",
        "def display_df(df, limit=10):\n",
        "    \"\"\"Safely display a Spark DataFrame using RDD collection.\"\"\"\n",
        "    # Use rdd.collect() as it proved more stable on Windows than direct df.collect()\n",
        "    rows = df.limit(limit).rdd.collect()\n",
        "    return pd.DataFrame(rows, columns=df.columns)\n",
        "\n",
        "# Create Spark session with stability configs\n",
        "# Use a custom temp directory to avoid Java NIO errors\n",
        "spark_temp_dir = Path(r\"C:\\tmp\\spark-temp\")\n",
        "spark_temp_dir.mkdir(parents=True, exist_ok=True)\n",
        "\n",
        "spark = SparkSession.builder \\\n",
        "    .appName(\"MyFirstSparkApp\") \\\n",
        "    .master(\"local[*]\") \\\n",
        "    .config(\"spark.sql.warehouse.dir\", \"file:///C:/tmp/hive\") \\\n",
        "    .config(\"spark.python.worker.reuse\", \"false\") \\\n",
        "    .config(\"spark.pyspark.python\", python_path) \\\n",
        "    .config(\"spark.pyspark.driver.python\", python_path) \\\n",
        "    .config(\"spark.python.use.daemon\", \"false\") \\\n",
        "    .config(\"spark.local.dir\", str(spark_temp_dir)) \\\n",
        "    .config(\"spark.driver.extraJavaOptions\", f\"-Djava.io.tmpdir={str(spark_temp_dir)}\") \\\n",
        "    .config(\"spark.executor.extraJavaOptions\", f\"-Djava.io.tmpdir={str(spark_temp_dir)}\") \\\n",
        "    .getOrCreate()\n",
        "\n",
        "print(f\"\u2705 Spark {spark.version} session created!\")\n",
        "print(f\"\ud83d\udcca Running on: {spark.sparkContext.master}\")"
    ]
    cell['source'] = new_source

# Update the version text
for cell in cells:
    if cell['cell_type'] == 'markdown':
        source = cell['source']
        if isinstance(source, list):
             for i, line in enumerate(source):
                 if "PySpark 4.1.0 is installed" in line:
                     source[i] = "PySpark 3.5.3 (Stable) is installed and ready to use!"

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=4)

print("Notebook updated successfully.")
