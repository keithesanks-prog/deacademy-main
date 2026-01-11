
import os
import sys

target_path = r"C:\Users\ksank\AppData\Roaming\Python\Python313\site-packages\pyspark\accumulators.py"

if not os.path.exists(target_path):
    print(f"Error: {target_path} not found.")
    sys.exit(1)

print(f"Patching {target_path}...")

with open(target_path, "r", encoding="utf-8") as f:
    content = f.read()

old_line = "class AccumulatorUnixServer(socketserver.UnixStreamServer):"
new_line = "class AccumulatorUnixServer(getattr(socketserver, 'UnixStreamServer', object)):"

if old_line in content:
    new_content = content.replace(old_line, new_line)
    try:
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Success: File patched.")
    except PermissionError:
        print("Error: Permission denied. Run as admin or check file permissions.")
elif new_line in content:
    print("Info: File already patched.")
else:
    print("Error: Target line not found in file. Maybe versions differ?")
    # Print context to debug
    idx = content.find("class AccumulatorUnixServer")
    if idx != -1:
        print("Found context:")
        print(content[idx:idx+100])
    else:
        print("Context not found.")

