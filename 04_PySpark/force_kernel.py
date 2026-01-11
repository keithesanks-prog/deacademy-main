import json
import os

notebook_path = "pyspark_quickstart.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Force the kernelspec
nb['metadata']['kernelspec'] = {
    "display_name": "Python 3.11 (PySpark)",
    "language": "python",
    "name": "python311_pyspark"
}

# Also update language info to be safe
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

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=4)

print("Notebook kernelspec forced to 'python311_pyspark'.")
