import pymysql
import sys

print("--- FINAL VERIFICATION ---")
print("Trying to connect as 'python_user'...")

try:
    connection = pymysql.connect(
        host='127.0.0.1',
        user='python_user',
        password='password',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✅ SUCCESS! The 'python_user' is working perfectly.")
    connection.close()

except Exception as e:
    print(f"❌ IT FAILED: {e}")
