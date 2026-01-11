import socket
import sys

def check_port(host, port):
    print(f"Checking {host}:{port}...", end=" ")
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (host, port)
    result_of_check = a_socket.connect_ex(location)
    a_socket.close()
    
    if result_of_check == 0:
        print("OPEN ✅")
        return True
    else:
        print("CLOSED ❌")
        return False

print("--- MySQL DEBUGGER ---")
print(f"Python Version: {sys.version}")

# 1. Check if the server is even reachable
server_running = check_port("127.0.0.1", 3306)

if not server_running:
    print("\n[DIAGNOSIS]: The MySQL Server does not seem to be listening on port 3306.")
    print("Possibilities:")
    print("1. The service is stopped.")
    print("2. It installed on a different port.")
    print("3. Firewall is blocking it.")
else:
    print("\n[DIAGNOSIS]: The Server is network-reachable.")
    print("If you still cannot connect, it is likely a PASSWORD or USERNAME issue.")
    print("Try using 'root' and the password you set.")
