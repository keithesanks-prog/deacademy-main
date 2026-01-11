import pymysql
import sys

# CHANGE THIS TO YOUR PASSWORD
# (Ideally we wouldn't hardcode this but for a quick debug script it's the fastest way to test)
# The user said they changed it, but I don't know what it is.
# I will ask the script to take it as input or just try to connect with a dummy to see the handshake.

print("--- DETAILED CONNECTION TEST ---")

try:
    # 1. Test 127.0.0.1 (IPv4 Force)
    print("\n[TEST 1] Connecting to 127.0.0.1...", end=" ")
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='wrong_password_on_purpose_to_test_handshake',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5
    )
    print("SUCCESS (Unexpectedly logged in with wrong pw?)")
    connection.close()

except pymysql.err.OperationalError as e:
    code, msg = e.args
    print(f"FAILED (As expected or Error?) -> Code: {code}")
    print(f"Message: {msg}")
    
    if code == 1045:
        print("RESULT: ✅ SERVER REACHABLE! It rejected the password (which means it's working).")
        print("SOLUTION: Your Python code just has the wrong password or spaces in it.")
    elif code == 2003:
        print("RESULT: ❌ CONNECTION REFUSED. Creating a socket failed.")
    elif "caching_sha2_password" in str(msg):
        print("RESULT: ⚠️ AUTH PLUG-IN ERROR. You need to upgrade pymysql or change server settings.")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")

try:
    # 2. Test localhost (DNS Resolution)
    print("\n[TEST 2] Connecting to localhost...", end=" ")
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='wrong_password_on_purpose_to_test_handshake',
        connect_timeout=5
    )
    print("SUCCESS")
    connection.close()
except Exception as e:
    print(f"FAILED -> {e}")
