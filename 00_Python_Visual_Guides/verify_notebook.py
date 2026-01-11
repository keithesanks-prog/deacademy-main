import json

# Read the notebook
with open('notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell with the date dimension code
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'DIM_DATE' in source and 'date_list' in source:
            print(f"Found DIM_DATE cell at index {i}")
            print("\n" + "="*60)
            print("Current code in the file:")
            print("="*60)
            print(source)
            print("="*60)
            
            # Check for the problematic line
            if "strftime('%Q')" in source:
                print("\n❌ ERROR: Found the OLD buggy code with strftime('%Q')")
            elif 'quarter = (dt.month - 1) // 3 + 1' in source:
                print("\n✅ CORRECT: Found the FIXED code with manual quarter calculation")
            else:
                print("\n⚠️  UNKNOWN: Code doesn't match expected patterns")
            break
