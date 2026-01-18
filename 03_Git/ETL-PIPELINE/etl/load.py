import json

def load_data(rows, path="data/output.json"):
    with open(path, "w") as f:
        json.dump(rows, f, indent=2)

