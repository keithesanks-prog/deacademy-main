import csv

def extract_data(path="data/input.csv"):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    ## This Changes are done to test Feature Extract step Branch.
    ## This is the second Change done to test Feature Extract step Branch.

    return rows 
