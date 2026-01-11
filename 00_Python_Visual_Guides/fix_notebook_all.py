import json

nb_path = 'training.ipynb'

try:
    with open(nb_path, 'r') as f:
        nb = json.load(f)
    
    # Cell 19 is index 18
    target_idx = 18 
    
    if target_idx < len(nb['cells']):
        cell = nb['cells'][target_idx]
        
        # New code showing both approaches
        new_source = [
            "def first_non_repeat(my_string):\n",
            "    char_count = {}\n",
            "    for char in my_string:\n",
            "        char_count[char] = char_count.get(char, 0) + 1\n",
            "    \n",
            "    # APPROACH 1: Return the FIRST one (stops immediately)\n",
            "    for char in my_string:\n",
            "        if char_count[char] == 1:\n",
            "            return char\n",
            "\n",
            "def get_all_non_repeats(my_string):\n",
            "    char_count = {}\n",
            "    for char in my_string:\n",
            "        char_count[char] = char_count.get(char, 0) + 1\n",
            "    \n",
            "    # APPROACH 2: Collect ALL of them\n",
            "    results = []\n",
            "    for char in my_string:\n",
            "        if char_count[char] == 1:\n",
            "            results.append(char)\n",
            "    return results\n",
            "\n",
            "my_string = \"hello world\"\n",
            "print(f\"First non-repeat: {first_non_repeat(my_string)}\")\n",
            "print(f\"All non-repeats:  {get_all_non_repeats(my_string)}\")\n"
        ]
        
        cell['source'] = new_source
        nb['cells'][target_idx] = cell
        
        with open(nb_path, 'w') as f:
            json.dump(nb, f, indent=1)
            
        print("\n\u2705 Updated Cell 19 to show both examples.")
    else:
        print(f"Error: Cell {target_idx} not found.")

except Exception as e:
    print(f"Error: {e}")
