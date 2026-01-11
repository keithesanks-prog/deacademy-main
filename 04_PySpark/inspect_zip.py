import zipfile
import sys
import os

zip_path = r"C:\Users\ksank\training\.venv312\Lib\site-packages\pyspark\python\lib\pyspark.zip"
dump_file = "worker_dump.txt"

print(f"Inspecting: {zip_path}")

try:
    with zipfile.ZipFile(zip_path, 'r') as z:
        if "pyspark/worker.py" in z.namelist():
            with z.open("pyspark/worker.py") as f, open(dump_file, "w", encoding="utf-8") as out:
                content = f.read().decode('utf-8')
                out.write(content)
                print(f"Dumped content to {dump_file}")
        else:
            print("pyspark/worker.py not found in zip")
            
except Exception as e:
    print(f"Error dumping: {e}")
