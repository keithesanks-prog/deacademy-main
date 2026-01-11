import json
import shutil

source = "pyspark_quickstart.ipynb"
dest = "pyspark_quickstart_v2.ipynb"

# Load original
with open(source, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Force kernelspec
nb['metadata']['kernelspec'] = {
    "display_name": "Python 3.11 (PySpark)",
    "language": "python",
    "name": "python311_pyspark"
}
nb['metadata']['language_info'] = {
    "codemirror_mode": {
        "name": "ipython",
        "version": 3
    },
    "file_extension": ".py",
    "mimetype": "text/x-python",
    "name": "python",
    "nbconvert_exporter": "python",
    "pygments_lexer": "ipython3",
    "version": "3.11.9"
}

# Write new file
with open(dest, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=4)

print(f"Created {dest} with forced kernel.")
