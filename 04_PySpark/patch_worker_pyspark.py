import zipfile
import os
import tempfile
import shutil

# Path to the pyspark.zip used by workers
zip_path = r"C:\Users\ksank\training\.venv\Lib\site-packages\pyspark\python\lib\pyspark.zip"

print(f"Patching {zip_path}...")

# Create a temporary directory
with tempfile.TemporaryDirectory() as temp_dir:
    # Extract the zip
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Path to accumulators.py inside the extracted zip
    accumulators_path = os.path.join(temp_dir, "pyspark", "accumulators.py")
    
    # Read the file
    with open(accumulators_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already patched
    if "socketserver.UnixStreamServer = UnixStreamServer" in content:
        print("Already patched!")
    else:
        # Apply the patch
        target = "import socketserver"
        patch = """import socketserver
import sys
# PATCHED BY AGENT: Fix for Windows missing UnixStreamServer
if sys.platform == 'win32' and not hasattr(socketserver, "UnixStreamServer"):
    class UnixStreamServer(object):
        def __init__(self, server_address, RequestHandlerClass):
            pass
        def shutdown(self):
            pass
        def server_close(self):
            pass
    socketserver.UnixStreamServer = UnixStreamServer
"""
        
        if target not in content:
            print("ERROR: Could not find 'import socketserver' in the file")
            exit(1)
        
        new_content = content.replace(target, patch, 1)
        
        # Write back
        with open(accumulators_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Patch applied to extracted file")
    
    # Re-create the zip file
    print("Re-creating zip file...")
    
    # Backup original
    backup_path = zip_path + ".backup"
    if not os.path.exists(backup_path):
        shutil.copy2(zip_path, backup_path)
        print(f"Backup created: {backup_path}")
    
    # Create new zip
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zip_ref.write(file_path, arcname)
    
    print("Successfully patched pyspark.zip!")
