import zipfile
import os
import shutil
import tempfile

zip_path = r"C:\Users\ksank\training\.venv312\Lib\site-packages\pyspark\python\lib\pyspark.zip"
backup_path = zip_path + ".bak2"

print(f"Patching: {zip_path}")

if not os.path.exists(backup_path):
    shutil.copy2(zip_path, backup_path)
    print("Backup created")

# Create a temp file for the new zip
fd, tmp_zip_path = tempfile.mkstemp()
os.close(fd)

try:
    with zipfile.ZipFile(zip_path, 'r') as zin:
        with zipfile.ZipFile(tmp_zip_path, 'w') as zout:
            for item in zin.infolist():
                buffer = zin.read(item.filename)
                
                if item.filename.endswith('pyspark/accumulators.py'):
                    print(f"Found {item.filename}, patching...")
                    content = buffer.decode('utf-8')
                    
                    if "if hasattr(socketserver, 'UnixStreamServer'):" in content:
                        print("  Already patched!")
                        zout.writestr(item, buffer)
                        continue
                        
                    # Apply patch
                    old_class = "class AccumulatorUnixServer(socketserver.UnixStreamServer):"
                    if old_class not in content:
                        print("  WARNING: Could not find class definition to patch!")
                        zout.writestr(item, buffer)
                        continue
                        
                    new_class = """# Only define AccumulatorUnixServer if UnixStreamServer is available (not on Windows)
if hasattr(socketserver, 'UnixStreamServer'):
    class AccumulatorUnixServer(socketserver.UnixStreamServer):"""
                    
                    content = content.replace(old_class, new_class)
                    
                    # Need to indent the body of the class?
                    # No, simply replacing the class def line works IF we also handle the ELSE case
                    # But Python indentation is significant.
                    
                    # Let's do it line by line to be safe
                    lines = buffer.decode('utf-8').splitlines()
                    new_lines = []
                    in_class = False
                    
                    for line in lines:
                        if line.startswith("class AccumulatorUnixServer(socketserver.UnixStreamServer):"):
                            new_lines.append("# Only define AccumulatorUnixServer if UnixStreamServer is available (not on Windows)")
                            new_lines.append("if hasattr(socketserver, 'UnixStreamServer'):")
                            new_lines.append("    class AccumulatorUnixServer(socketserver.UnixStreamServer):")
                            in_class = True
                        elif in_class:
                            if line.strip() == "" or line.startswith("    "):
                                # Ensure extra indentation
                                new_lines.append("    " + line)
                            elif line.startswith("class ") or line.startswith("def ") or line.startswith("if __name__"):
                                # End of class
                                new_lines.append("else:")
                                new_lines.append("    # On Windows, UnixStreamServer doesn't exist")
                                new_lines.append("    AccumulatorUnixServer = None")
                                new_lines.append("")
                                new_lines.append(line)
                                in_class = False
                            else:
                                # Some other top level thing?
                                new_lines.append(line) 
                        else:
                            new_lines.append(line)
                            
                    # If we ended while still in class
                    if in_class:
                         new_lines.append("else:")
                         new_lines.append("    AccumulatorUnixServer = None")
                    
                    zout.writestr(item, "\n".join(new_lines).encode('utf-8'))
                    print("  Patch applied to content")
                else:
                    zout.writestr(item, buffer)
                    
    # Replace original
    shutil.move(tmp_zip_path, zip_path)
    print("Zip file updated successfully")

except Exception as e:
    print(f"FAILED: {e}")
    if os.path.exists(tmp_zip_path):
        os.remove(tmp_zip_path)
