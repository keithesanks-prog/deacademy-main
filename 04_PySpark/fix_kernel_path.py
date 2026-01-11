
import json
import os
import sys

# Define the path to the kernel.json
appdata = os.getenv('APPDATA')
kernel_json_path = os.path.join(appdata, r"jupyter\kernels\python311_pyspark\kernel.json")

print(f"Checking kernel spec at: {kernel_json_path}")

if not os.path.exists(kernel_json_path):
    print("Error: kernel.json not found!")
    sys.exit(1)

# Read the current content
with open(kernel_json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check the argv[0] to see if it needs fixing
current_exe = data['argv'][0]
print(f"Current Python path: {current_exe}")

# The incorrect path has 'Scripts\\python.exe', the correct one is just 'python.exe' in the root of the env
# Or specifically for the embedded python zip extraction we saw earlier:
# The user has: c:\Users\ksank\training\04_PySpark\python311_env
# And we saw python.exe in the root of that dir.

if "Scripts\\python.exe" in current_exe:
    new_exe = current_exe.replace("Scripts\\python.exe", "python.exe")
    data['argv'][0] = new_exe
    
    # Write back
    with open(kernel_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1)
        
    print(f"Fixed Python path to: {new_exe}")
    print("Kernel spec updated successfully.")
else:
    print("Path does not look like the expected incorrect path (Scripts\\python.exe). No changes made.")
