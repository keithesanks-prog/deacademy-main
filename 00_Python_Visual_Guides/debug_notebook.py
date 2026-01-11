import json

try:
    with open('training.ipynb', 'r') as f:
        nb = json.load(f)
    
    cells = nb['cells']
    print(f"Total cells: {len(cells)}")
    
    # Print Cell 19 (Check both 0-indexed index 18 and 19)
    indices_to_check = [18, 19]
    
    for i in indices_to_check:
        if i < len(cells):
            print(f"\n--- Cell {i} (0-indexed) / Cell {i+1} (1-indexed) ---")
            cell = cells[i]
            print(f"Type: {cell['cell_type']}")
            print("Source:")
            print("".join(cell['source']))
        else:
            print(f"\nCell {i} does not exist.")

except Exception as e:
    print(f"Error: {e}")
