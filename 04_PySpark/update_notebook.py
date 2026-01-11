
import json
import os

notebook_path = r"C:\Users\ksank\training\04_PySpark\pyspark_quickstart.ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# The robust setup code to inject
new_source = [
    "import os\n",
    "import sys\n",
    "from pyspark.sql import SparkSession\n",
    "import pandas as pd\n",
    "\n",
    "# --- WINDOWS ENVIRONMENT SETUP ---\n",
    "os.environ['PYSPARK_PYTHON'] = sys.executable\n",
    "os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable\n",
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
    "spark = SparkSession.builder \\\n",
    "    .appName(\"MyFirstSparkApp\") \\\n",
    "    .master(\"local[*]\") \\\n",
    "    .config(\"spark.sql.warehouse.dir\", \"file:///C:/tmp/hive\") \\\n",
    "    .config(\"spark.python.worker.reuse\", \"false\") \\\n",
    "    .getOrCreate()\n",
    "\n",
    "print(f\"✅ Spark {spark.version} session created!\")\n",
    "print(f\"📊 Running on: {spark.sparkContext.master}\")"
]

# Find and replace the cell
cells = nb["cells"]
replaced_setup = False

for cell in cells:
    if cell["cell_type"] == "code":
        source_str = "".join(cell["source"])
        
        # 1. Inject Setup Code (Only in the first definition cell)
        if "SparkSession.builder" in source_str:
            cell["source"] = new_source
            replaced_setup = True
            print("Successfully updated Setup/Spark Session cell.")
        
        # 2. Replace all .show() calls with display_df()
        # Handle cases like df.show(), df.select(...).show(), df.show(truncate=False)
        new_lines = []
        for line in cell["source"]:
            # Skip comments to avoid corrupting explanatory text
            if line.strip().startswith("#"):
                new_lines.append(line)
                continue

            if ".show(" in line:
                # Naive but effective replacement for this specific notebook structure
                # Capturing indentation
                indent = line[:len(line) - len(line.lstrip())]
                content = line.strip()
                
                # Check if it has arguments like truncate=False
                args = ""
                if "(" in content and ")" in content:
                    start = content.rfind("(") + 1
                    end = content.rfind(")")
                    args = content[start:end]
                
                # Extract the dataframe part: df.show() -> df
                # or df.select(...).show() -> df.select(...)
                df_part = content.split(".show(")[0]
                
                # Construct new call
                if args:
                     new_line = f"{indent}display_df({df_part}, {args})\n"
                else:
                     new_line = f"{indent}display_df({df_part})\n"
                
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        cell["source"] = new_lines

if replaced_setup:
    # Add a markdown cell warning about df.show()
    warning_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 💡 Important Note for Windows Users\n",
            "If you experience crashes with `df.show()`, please use our `display_df(df)` helper function defined above. It uses `collect()` internally which is stable on Windows."
        ]
    }
    # Insert after the setup cell
    for i, cell in enumerate(cells):
        if cell["source"] == new_source:
             # Only insert if not already there to avoid duplicates on re-run
             if i + 1 < len(cells) and "Important Note for Windows Users" not in "".join(cells[i+1]["source"]):
                cells.insert(i + 1, warning_cell)
             break

# ALWAYS save the file to capture .show() replacements
with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=4)
print("Notebook saved with widespread replacements.")
