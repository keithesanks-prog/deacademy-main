import os
import sys
import subprocess

# Run the test and capture output
result = subprocess.run(
    [sys.executable, "simple_pyspark_test.py"],
    cwd=r"C:\Users\ksank\training\04_PySpark",
    capture_output=True,
    text=True
)

print("=== STDOUT ===")
print(result.stdout)
print("\n=== STDERR ===")
print(result.stderr)
print(f"\n=== EXIT CODE: {result.returncode} ===")

# Save to file
with open(r"C:\Users\ksank\training\04_PySpark\captured_output.txt", "w", encoding="utf-8") as f:
    f.write("=== STDOUT ===\n")
    f.write(result.stdout)
    f.write("\n\n=== STDERR ===\n")
    f.write(result.stderr)
    f.write(f"\n\n=== EXIT CODE: {result.returncode} ===\n")

print("\nOutput saved to captured_output.txt")
