
import os
import sys

path = r"c:\Users\ksank\training\.venv\Lib\site-packages\pyspark\accumulators.py"

try:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "socketserver.UnixStreamServer = UnixStreamServer" in content:
        print("Already patched.")
    else:
        # We replace "import socketserver" with the patched version
        # using a unique string from the file to ensure we target the right place
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
        # strict replacement to avoid messing up if "import socketserver" appears elsewhere
        # We know it appears at the top imports.
        # Let's find the first occurrence.
        if target not in content:
            print("Could not find target string 'import socketserver'")
            sys.exit(1)
            
        new_content = content.replace(target, patch, 1)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully patched accumulators.py")

except Exception as e:
    print(f"Error patching file: {e}")
    sys.exit(1)
