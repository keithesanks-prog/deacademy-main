import json

nb_path = 'training.ipynb'

try:
    with open(nb_path, 'r') as f:
        nb = json.load(f)
    
    # Cell 19 is index 18
    target_idx = 18 
    
    if target_idx < len(nb['cells']):
        cell = nb['cells'][target_idx]
        original_source = "".join(cell['source'])
        print(f"Original Code:\n{original_source}")
        
        # New correct source code with proper indentation
        new_source = [
            "def first_non_repeat(my_string):\n",
            "    char_count = {}\n",
            "    print(char_count)\n",
            "    for char in my_string:\n",
            "        char_count[char] = char_count.get(char, 0) + 1\n",
            "    print(char_count)\n",
            "    # for char in my_string:\n",
            "    # \tif char_count[char] == 1:\n",
            "    # \t\treturn char\n",
            "\n",
            "my_string = \"hello world\"\n",
            "print(first_non_repeat(my_string))\n"
        ]
        
        cell['source'] = new_source
        nb['cells'][target_idx] = cell
        
        with open(nb_path, 'w') as f:
            json.dump(nb, f, indent=1)
            
        print("\n\u2705 Successfully fixed indentation in Cell 19.")
    else:
        print(f"Error: Cell {target_idx} not found.")

except Exception as e:
    print(f"Error: {e}")
